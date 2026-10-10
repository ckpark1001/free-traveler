---
description: Wave 단위로 Task를 하나씩 prepare-task→implement-task 순서로 처리하는 오케스트레이터. /run-wave W03, /run-wave W03 --status, /run-wave W03 --resume, /run-wave W03 --dry-run을 지원한다.
argument-hint: WXX | WXX --dry-run | WXX --resume | [WXX] --status
---

# /run-wave

`traveler-project-pipeline` Skill, `CLAUDE.md`(DEC-010/011/022), `/prepare-task`, `/implement-task`의 규칙을 그대로 따르는 Wave 오케스트레이터다. 이 Command 자체는 코드를 짜지 않는다 — Task 선택과 `/prepare-task`·`/implement-task` 호출, 상태 갱신만 한다(실제 `app/src/**` 변경은 `/implement-task` 절차 안에서 일어난다).

Skill이 아직 컨텍스트에 없다면 먼저 `Skill(traveler-project-pipeline)`을 호출한다.

## 입력

- **`WAVE_ID`**(예: `W03`) — 기본 동작과 `--dry-run`에는 필수다. `--status`/`--resume`에서는 생략할 수 있으며, 생략 시 `TASKS/WAVE_STATE.json`의 `active_wave`를 대상으로 한다. `active_wave`도 없으면 중단하고 안내한다.
- **`--status`**(선택) — 읽기 전용. 현재 Wave와 그 안의 Task 상태만 보여주고 아무것도 바꾸지 않는다.
- **`--dry-run`**(선택) — 실행할 Task·Expected Files·최소 검증·Browser Checkpoint 여부만 시뮬레이션해 보여주고, 코드도 `WAVE_STATE.json`도 바꾸지 않는다.
- **`--resume`**(선택) — 중단된 Wave를, 그 Wave 안에서 아직 `DONE`이 아닌 Task 중 가장 앞(`READY`=pending 또는 `BLOCKED`)부터 다시 시작한다.
- 옵션이 전혀 없으면 **기본 동작**이다: `WXX`의 pending(`READY`) Task를 한 개씩 prepare(`/prepare-task`)하고 implement(`/implement-task`)한다.
- `--dry-run`·`--resume`·`--status`는 동시에 두 개 이상 줄 수 없다. 여러 개가 오면 `BLOCKED_INPUT`으로 보고하고 중단한다.

## 상태 파일

이 Command는 두 파일을 근거로 동작한다. 둘 다 없으면 아래 절차에 따라 처리한다.

### `TASKS/WAVE_PLAN.md` (사람이 작성/승인, 이 Command는 쓰지 않음)

```markdown
| Wave ID | 목표 | Task ID 목록(Depends On 순서) | Preview Checkpoint |
|---|---|---|---|
| W01 | ... | TASK-A, TASK-B, ... | 없음 |
| W02 | ... | TASK-C, TASK-D, ... | SCR-001 Preview 확인 |
```

`Preview Checkpoint`가 "없음"이 아니면, 그 Wave가 전부 끝난 뒤 사람이 Preview를 확인하기 전까지 다음 Wave로 넘어가지 않는다(`CLAUDE.md` 규칙 22). 이 컬럼과 `TASKS/TASK_MANIFEST.csv`를 함께 근거로 삼아 Wave마다 **Browser Checkpoint**(아래 "Browser Checkpoint 판정 규칙" 참고)가 필요한지 판단한다.

**이 파일이 없으면**: `/run-wave`는 아무 Task도 실행하지 않는다. "`TASKS/WAVE_PLAN.md`가 없어 Wave를 실행할 수 없습니다 — 먼저 Wave 계획을 작성하세요"라고 보고하고 중단한다. 이 Command가 임의로 Wave 계획을 만들어내지 않는다.

### `TASKS/WAVE_STATE.json` (이 Command가 갱신하는 유일한 파일)

```json
{
  "active_wave": "W03",
  "updated_at": "2026-09-16T00:00:00Z",
  "waves": { "W01": { "status": "DONE" }, "W03": { "status": "IN_PROGRESS" } },
  "tasks": {
    "PAGE-SCR001": { "status": "DONE", "completed_at": "..." },
    "CMP-SCR001-HERO-SEARCH": { "status": "READY" }
  }
}
```

Task `status`는 `READY`(Depends On 전부 DONE, 아직 미착수 = "pending") / `IN_PROGRESS` / `DONE` / `BLOCKED`(사유 포함) 중 하나다. Wave `status`는 `PENDING` / `IN_PROGRESS` / `WAITING_FOR_PREVIEW`(Browser Checkpoint 대기) / `DONE` / `BLOCKED` 중 하나다.

**이 파일이 없으면**: `TASKS/WAVE_PLAN.md`와 `TASKS/TASK_MANIFEST.csv`의 Depends On을 근거로 새로 만든다. Depends On이 없거나 전부 완료로 확인되는 Task만 `READY`로, 나머지는 상태 없음(=아직 시작 불가)으로 둔다. `TASKS/TASK-*.md`의 `## Definition of Done`이 이미 실제로 충족되어 있는 것이 명백한 Task가 있어도 임의로 `DONE`으로 채우지 않는다 — 확인되지 않은 완료는 기록하지 않는다.

## 사전 조건: 이전 Wave 완료 확인 (규칙 1)

`WXX`를 새로 시작하기 전에(=`WXX`가 아직 `WAVE_STATE.json`에 없거나 `PENDING`일 때) 항상 먼저 확인한다:

1. `TASKS/WAVE_PLAN.md`의 표에서 `WXX`보다 앞에 나열된 모든 Wave ID를 구한다.
2. 그중 하나라도 `WAVE_STATE.json`에서 `status`가 `DONE`이 아니면(기록 자체가 없는 경우 포함, `WAITING_FOR_PREVIEW`도 `DONE`이 아니므로 포함) **시작하지 않는다.** 어떤 이전 Wave가 아직 끝나지 않았는지 그대로 보고하고 중단한다.
3. 이 확인은 기본 동작과 `--dry-run` 모두에 적용한다(`--dry-run`은 이 Gate에서 막히는 것도 시뮬레이션 결과로 보여준다). 이미 `IN_PROGRESS`/`BLOCKED`로 시작된 `WXX`를 이어가는 `--resume`에는 이 Gate를 다시 적용하지 않는다 — 최초 시작 시점에 이미 통과했기 때문이다.

## `/run-wave WXX` (기본 동작)

1. `TASKS/WAVE_PLAN.md`와 `TASKS/WAVE_STATE.json`을 실제로 읽는다(추측 금지). `WXX`가 `WAVE_PLAN.md`에 없으면 중단하고 안내한다. 위 "사전 조건"을 통과하지 못하면 여기서 멈추고 "종료 보고"를 낸다.
2. `WXX`에 속한 Task 중 `WAVE_STATE.json`에서 `status`가 `DONE`이 아니고, 그 Task의 모든 Depends On이 `DONE`인 것을 찾는다. `TASKS/WAVE_PLAN.md`에 나열된 순서(=Depends On 위상 순서) 상 가장 앞의 것 **하나만** 고른다.
   - 그런 Task가 없고 아직 `DONE`이 아닌 Task도 없으면 → 7번으로 간다.
   - 그런 Task가 없는데 `DONE`이 아닌 Task가 남아 있으면(=전부 Depends On 미해결) → 중단하고 "Wave 안에서 진행 가능한 Task가 없음(선행 Task 미완료)"으로 보고한다.
3. 고른 Task ID에 대해 `/prepare-task WXX <TASK_ID>`의 8가지 검사를 그대로 수행한다.
   - `READY_TO_IMPLEMENT`가 아니면: `WAVE_STATE.json`에 해당 Task를 `BLOCKED`(사유 포함)로 기록하고, **`WXX` 자체의 Wave `status`도 `BLOCKED`로 기록한다**(규칙 2). **Wave 실행을 여기서 멈춘다** — 다른 Task로 건너뛰지 않는다. Single Agent 순차 실행 원칙(`CLAUDE.md` 규칙 7, 11)에 따라 막힌 Task를 넘기고 계속 진행하지 않는다. `BLOCKED_*` 판정과 근거를 "종료 보고" 형식으로 낸다.
4. `READY_TO_IMPLEMENT`면 `WAVE_STATE.json`에서 그 Task를 `IN_PROGRESS`로 표시하고(Wave `status`도 아직 `PENDING`이면 `IN_PROGRESS`로 올린다), `/implement-task WXX <TASK_ID>`의 절차를 그대로 수행해 그 Task 하나를 구현한다. 이때 Task의 `## Verify`/Test Cases에 지정된 최소 검증(관련 Unit Test, 필요 시 Playwright)을 건너뛰지 않는다(규칙 3) — `/implement-task`의 5·6단계 그대로.
5. `/implement-task`가 보고하는 검증 결과(관련 Unit Test, 해당 시 Playwright)가 전부 PASS면 `WAVE_STATE.json`에서 그 Task를 `DONE`으로 갱신한다(완료 시각 포함). 하나라도 PASS가 아니면(FAIL 또는 "실행하지 않음") `DONE`으로 바꾸지 않고, `IN_PROGRESS` 상태로 두거나 사유와 함께 `BLOCKED`로 바꾼다 — `BLOCKED`로 바꾸는 경우 **`WXX`의 Wave `status`도 함께 `BLOCKED`로 기록한다**(규칙 2). 두 경우 모두 **Wave 실행을 멈추고** "종료 보고" 형식으로 낸다.
6. 5번이 `DONE`으로 끝났으면 2번으로 돌아가 같은 Wave의 다음 `READY`(pending) Task를 계속 처리한다.
7. `WXX`의 모든 Task가 `DONE`이면 Wave를 끝낸다. "Browser Checkpoint 판정 규칙"으로 이 Wave에 Browser Checkpoint가 필요한지 판정한다.
   - **필요 없음**이면 Wave `status`를 `DONE`으로 기록하고, 다음 Wave를 `/run-wave <다음 WXX>`로 실행할 수 있다고 "종료 보고"에 안내한다.
   - **필요함**이면 Wave `status`를 `WAITING_FOR_PREVIEW`로 기록하고 **여기서 종료한다**(규칙 5). 사람이 Browser Checkpoint를 확인하기 전에는 다음 Wave를 자동으로 시작하지 않는다(`CLAUDE.md` 규칙 22). "종료 보고"에 "남은 수동 Browser 확인" 항목으로 무엇을 확인해야 하는지 구체적으로 적는다.
8. 모든 단계에서 `WAVE_STATE.json`을 그때그때 갱신한다 — 중간에 중단되어도 `/run-wave <WXX> --resume`이 이어받을 수 있게 한다.
9. 이 기본 동작이 멈추는 모든 지점(2번 진행 불가, 3번 BLOCKED, 5번 검증 실패/BLOCKED, 7번 완료/WAITING_FOR_PREVIEW)에서 아래 "종료 보고" 형식을 그대로 따른다.

## `/run-wave [WXX] --status`

읽기 전용. `WXX`를 생략하면 `TASKS/WAVE_STATE.json`의 `active_wave`를 쓴다. `WAVE_STATE.json`(없으면 `TASKS/WAVE_PLAN.md`만)을 읽어 해당 Wave의 상태와, 그 Wave 안 Task별 상태(READY=pending/IN_PROGRESS/DONE/BLOCKED)를 표로 보고한다. 아무것도 실행하거나 갱신하지 않는다.

## `/run-wave WXX --resume`

1. `WXX`를 생략하면 `TASKS/WAVE_STATE.json`의 `active_wave`를 쓴다. 그마저 없으면 "재개할 Wave가 없습니다"라고 보고하고 중단한다.
2. 그 Wave의 상태에 따라 분기한다.
   - **`WAITING_FOR_PREVIEW`**: 다음 Wave로 바로 넘어가지 않는다(규칙 5). 사용자에게 "이 Wave의 Browser Checkpoint를 확인했습니까?"를 명시적으로 확인받은 뒤에만, 사용자가 지정한 다음 Wave에 대해 `/run-wave <다음 WXX>`를 시작한다. 확인 없이 자동으로 다음 Wave를 시작하지 않는다.
   - **`PENDING`/`IN_PROGRESS`/`BLOCKED`**: 그 Wave에 속한 Task들을 `TASKS/WAVE_PLAN.md`에 나열된 순서대로 훑어, `DONE`이 아닌 **첫 번째 Task**(=`READY`=pending 이거나 `BLOCKED`인 첫 Task)를 찾는다. 그 Task부터 `/run-wave WXX` 기본 동작의 3번 단계(그 Task에 대해 다시 `/prepare-task` 실행)부터 이어간다.
     - 그 Task가 `IN_PROGRESS`로 남아 있었다면(중단 전 구현 도중이었다면) 먼저 `/prepare-task`로 Working Tree 등 상태를 재확인한 뒤 이어간다 — 중단 전에 이미 반영된 변경을 다시 만들지 않는다.
     - 그 Task가 `BLOCKED`였다면 `/prepare-task`를 다시 실행해 이제 `READY_TO_IMPLEMENT`인지 확인한다. 여전히 막혀 있으면 "종료 보고" 형식으로 그대로 보고하고 멈춘다(Wave `status`도 `BLOCKED`로 유지/갱신).
   - **`DONE`**: 재개할 것이 없다고 보고한다.

## `/run-wave WXX --dry-run`

- 코드도, `TASKS/WAVE_STATE.json`도 바꾸지 않는다. 순수 시뮬레이션이다.
- 먼저 "사전 조건: 이전 Wave 완료 확인"을 시뮬레이션한다 — 여기서 막히면 그 사실만 보고하고 끝낸다.
- `WXX`의 전체 Task 목록에 대해 기본 동작 2번 단계(다음 처리 순서 계산)를 끝까지 반복해 **처리 순서 전체**를 계산한다.
- 각 Task에 대해 `/prepare-task`의 8가지 검사를 실제로 수행해 지금 시점 기준 `READY_TO_IMPLEMENT` 여부와 사유를 확인한다.
- `/implement-task`는 호출하지 않는다(코드 변경 없음).
- 각 Task마다 다음 4가지를 표로 보고한다(사용자가 실제 `/run-wave WXX` 실행 전에 무엇이 바뀌고 어디서 막힐지 미리 볼 수 있게 하는 것이 목적):
  1. **Task**: 처리 예정 순서 + Task ID + 현재 판정(`READY_TO_IMPLEMENT` 또는 `BLOCKED_*`+사유).
  2. **파일**: 그 Task의 `## Expected Files` 목록(신규/수정 표시 그대로).
  3. **검증**: 그 Task의 `## Verify`/Test Cases에 지정된 최소 검증 항목(예: `UNIT-TRAVEL-DATES`, `E2E-PUBLIC-SMOKE`).
  4. **Checkpoint**: 이 Task가 속한 Wave에 "Browser Checkpoint 판정 규칙"을 적용한 결과(필요/불필요, 필요하면 근거).

## Browser Checkpoint 판정 규칙 (규칙 4)

Wave 하나가 끝났을 때 Browser Checkpoint(=사람이 실제 브라우저/Preview에서 화면을 확인하는 절차, `WAVE_STATE.json`에서는 `WAITING_FOR_PREVIEW`로 표현)가 필요한지는 아래 두 근거를 **OR**로 판정한다 — 둘 중 하나라도 "필요"를 가리키면 필요하다:

- **A. `TASKS/WAVE_PLAN.md`의 `Preview Checkpoint` 컬럼**: 그 Wave 행의 값이 "없음"이 아니면 필요.
- **B. Page Owner 존재 여부**: `TASKS/TASK_MANIFEST.csv`에서 그 Wave에 속한 Task 중 `category`가 `PAGE_OWNER`인 것이 하나라도 있으면 필요(`CLAUDE.md` 규칙 22 — 화면 단위 Wave는 항상 사람 확인을 거친다).

A가 "없음"인데 B가 "필요"를 가리키면(=`WAVE_PLAN.md` 작성 시 Page Owner Wave에 Preview Checkpoint 지정을 빠뜨린 경우) 이를 모순으로 그대로 보고하고, 안전한 쪽(**필요**)을 택해 `WAITING_FOR_PREVIEW`로 멈춘다. 이 Command는 `WAVE_PLAN.md`를 스스로 고치지 않으므로, 사람이 그 컬럼을 바로잡아야 한다고 안내만 한다.

## 종료 보고

`/run-wave WXX`(기본 동작)와 `/run-wave WXX --resume`이 멈추는 모든 지점(정상 완료, `WAITING_FOR_PREVIEW`, `BLOCKED`, 진행 가능한 Task 없음 등)에서 아래 5가지를 빠짐없이 보고한다. `--status`/`--dry-run`은 각자의 절 형식(표)을 따른다.

1. **완료 Task**: 이번 실행에서 새로 `DONE`이 된 Task ID 목록(없으면 "없음").
2. **변경 파일**: 이번 실행에서 실제로 만들거나 고친 파일 전체 목록 — 각 `/implement-task` 완료 보고의 "변경 파일"을 그대로 모은다.
3. **통과한 검사**: 각 Task에서 실행해 PASS한 검증(Lint/타입체크/Unit Test/Playwright 등)을 Task별로 나열한다. 실행하지 않았거나 실패한 항목은 숨기지 말고 별도로 그대로 남긴다.
4. **남은 수동 Browser 확인**: 이번에 `WAITING_FOR_PREVIEW`로 멈췄다면 어떤 Wave의 무엇을(어느 Screen/URL) 확인해야 하는지 구체적으로 적는다. 해당 없으면 "없음".
5. **다음에 입력할 명령**: 지금 상태에서 사용자가 다음에 칠 명령을 정확히 제안한다 — 예: `/run-wave WXX`(같은 Wave 계속), `/run-wave WXX --resume`(중단 후 재개), `/prepare-task WXX <TASK_ID>`(막힌 Task 재확인), 또는 Browser Checkpoint 확인 후 `/run-wave W(다음) --resume`.

## 공통 규칙

1. **이전 Wave 미완료 시 시작 금지** — "사전 조건: 이전 Wave 완료 확인" 절 그대로.
2. **Task 하나가 BLOCKED면 Wave도 BLOCKED로 기록하고 멈춘다** — 기본 동작 3번·5번에서 Task와 Wave `status`를 함께 갱신한다.
3. **Task마다 지정된 최소 검증을 건너뛰지 않는다** — `/implement-task`의 Unit Test/Playwright 단계를 그대로 물려받는다. 실행하지 못했으면 "실행하지 않음 — 이유"를 그대로 보고하며, 통과로 위장하지 않는다.
4. **Page Owner가 있는 Wave는 Browser Checkpoint가 필요하다** — "Browser Checkpoint 판정 규칙" 절 그대로.
5. **사람의 확인 전에는 다음 Wave를 자동 실행하지 않는다** — `WAITING_FOR_PREVIEW`에서 멈추고, `--resume`도 이 상태에서는 사용자 확인 없이 다음 Wave로 넘어가지 않는다. `run-wave`에서 유일하게 "다 됐어도 멈추는" 지점이다.
6. **자동 Commit·Push·PR·Merge를 하지 않는다** — Commit 여부는 `/implement-task`의 기본 정책을 그대로 물려받는다(기본은 Commit도 하지 않음). 사용자가 `/run-wave` 호출 시 "Task마다 Commit"을 명시적으로 요청한 경우에만, 각 Task가 `DONE`이 될 때마다 그 Task 범위의 Commit 1개를 만든다(`/implement-task`의 Commit 규칙 그대로 — Task당 Commit 1개, `git add -A` 금지). 이 경우에도 **Push·PR·Merge는 절대 하지 않는다**. Branch 생성도 어떤 하위 동작에서도 하지 않는다.

추가로:
- 한 번에 정확히 Task 하나만 진행한다 — 여러 Task를 동시에 구현하거나, 막힌 Task를 건너뛰고 다음 Task로 임의로 넘어가지 않는다.
- `/prepare-task`나 `/implement-task`가 낸 판정·검증 결과를 축소하거나 재해석하지 않는다. 실패는 실패로, 차단은 차단으로 그대로 보고한다.
