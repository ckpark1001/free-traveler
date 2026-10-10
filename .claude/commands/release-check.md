---
description: 배포 전 7가지(Task·Wave 상태/Page Owner 5개/CI/Playwright Smoke/Supabase 6 Table·RLS/Vercel Preview Checkpoint/EXCLUDED 목록)를 검사해 RELEASE_READY 또는 RELEASE_BLOCKED를 낸다.
---

# /release-check

`traveler-project-pipeline` Skill, `CLAUDE.md`, `app/docs/ARCHITECTURE.md`, `app/docs/PROJECT_SCOPE.md`를 근거로 지금 시점에 배포해도 되는지 최종 판정한다. **이 Command는 코드를 만들거나 고치지 않고, 배포를 실행하지도 않는다** — 순수 검사와 판정만 한다. 문제를 발견해도 스스로 고치지 않는다.

Skill이 아직 컨텍스트에 없다면 먼저 `Skill(traveler-project-pipeline)`을 호출한다.

## 검사 절차

7가지를 전부 실제로 확인한다. 하나를 확인하지 못했으면(파일이 없다, 실행 권한이 없다 등) "통과"로 치지 않고 그 항목을 실패로 기록한다 — 확인되지 않은 것을 통과했다고 가정하지 않는다.

### 1. Task·Wave 상태

`TASKS/WAVE_STATE.json`과 `TASKS/WAVE_PLAN.md`를 읽는다.
- `TASKS/WAVE_STATE.json`이 없으면 이 검사는 즉시 실패다("실행 이력을 확인할 수 없음").
- `TASKS/WAVE_PLAN.md`에 정의된 모든 Wave의 `status`가 `DONE`이어야 한다. 하나라도 `PENDING`/`IN_PROGRESS`/`BLOCKED`/`WAITING_FOR_PREVIEW`면 실패이고, 어떤 Wave·Task가 남아 있는지 나열한다.
- `TASKS/TASK_MANIFEST.csv`의 모든 Task ID가 `WAVE_STATE.json`에서 `DONE`인지 대조한다. 빠진 Task가 있으면 실패.

### 2. 5개 Page Owner DONE

`TASKS/TASK_MANIFEST.csv`에서 Category가 `PAGE_OWNER`인 5개 Task(`PAGE-SCR001`~`PAGE-SCR005`)를 찾아 `WAVE_STATE.json`에서 전부 `DONE`인지 확인한다. 하나라도 아니면 실패이고 어떤 Screen이 남았는지 명시한다(핵심 4개/보조 1개 구분 없이 5개 전부 필요).

### 3. CI PASS

- `.github/workflows/`에 워크플로 파일이 존재하는지 확인한다(`CI-TYPECHECK-LINT` Task 완료 여부와 연결).
- `gh run list --branch main --limit 1`(또는 동등한 `gh` 명령)로 `main` 브랜치의 가장 최근 CI 실행 결과를 조회한다. `conclusion`이 `success`가 아니면 실패다.
- CI 자체가 아직 구성되어 있지 않거나 실행 이력이 없으면("아직 CI가 없음") 통과로 치지 않고 실패로 기록한다.

### 4. Playwright Smoke PASS

- `TASKS/WAVE_STATE.json`에서 `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH` 3개 Task가 전부 `DONE`인지 확인한다.
- 3번 검사에서 조회한 최근 CI 실행(또는 그에 준하는 기록)에 Playwright Chromium Smoke 실행 결과가 포함되어 있고 통과했는지 확인한다. `DONE` 상태만 있고 실제 통과 기록이 없으면 실패로 본다("상태만 있고 근거 없음").
- Chromium 외 브라우저가 추가되어 있으면(구성 파일에서 확인) 실패로 기록한다(`CLAUDE.md` 규칙 18 위반).

### 5. Supabase 6개 Table·기본 RLS 확인 기록

- `python scripts/audit_tasks.py`를 실행한다. 종료 코드가 0이 아니면(=`AUDIT_FAIL`) 이 검사는 실패이고, 특히 검사 #11(DB Schema/RLS/Access/Seed 존재)과 #12(테이블 개수) 결과를 인용한다.
- `TASKS/WAVE_STATE.json`에서 `DB-SCHEMA-BASE`, `DB-RLS-BASE`, `DB-ACCESS`, `DB-SEED-BASE`, `TEST-RLS-BASIC` 5개 Task가 전부 `DONE`인지 확인한다.
- `supabase/migrations/*.sql`이 실제로 존재하면 그 안의 테이블 정의가 정확히 6개(`user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_link_setting`)와 일치하는지 확인한다. 마이그레이션 디렉터리 자체가 없으면 실패로 본다.

### 6. Vercel Preview Checkpoint

- `TASKS/WAVE_PLAN.md`에서 `Preview Checkpoint`가 "없음"이 아닌 모든 Wave를 찾는다.
- 그 Wave들이 `TASKS/WAVE_STATE.json`에서 전부 `DONE`(즉 `WAITING_FOR_PREVIEW`에 머물러 있지 않고 사람 확인 후 정상적으로 다음으로 넘어간 상태)인지 확인한다. 하나라도 `WAITING_FOR_PREVIEW`로 남아 있으면 실패다 — 사람이 아직 그 Preview를 확인하지 않았다는 뜻이다.
- Vercel CLI/대시보드 접근이 가능하면 해당 Wave 시점의 Preview 배포가 실제로 존재했는지 추가로 대조한다(선택 사항 — 접근 불가하면 `WAVE_STATE.json` 기록만으로 판단하고 그 사실을 보고서에 남긴다).

### 7. EXCLUDED 목록

- `app/docs/PROJECT_SCOPE.md`의 EXCLUDED 요구사항 개수(REQ-FUNC 11개 + REQ-NF 13개 = 24개)와 `TASKS/00_TASK_LIST.md` §2(NON_IMPLEMENTATION)·§3(Requirement Coverage Verification)의 EXCLUDED 표기가 정확히 일치하는지 확인한다(5번 검사에서 이미 실행한 `scripts/audit_tasks.py`의 검사 #17·#18 결과를 그대로 인용해도 된다).
- EXCLUDED 24개 중 어느 것도 `TASKS/TASK-*.md`로 상세 구현 Task가 만들어지지 않았는지 재확인한다(임의 구현 금지, `CLAUDE.md` 규칙 19).
- 24개 목록이 하나라도 빠졌거나, EXCLUDED인데 구현된 흔적이 있으면 실패다.

## 판정

- 7가지 검사가 전부 통과해야 **`RELEASE_READY`**다.
- 하나라도 실패하면 **`RELEASE_BLOCKED`**다. 실패한 검사 번호와 구체적 사유를 **전부** 나열한다(첫 번째 실패만 보고하고 멈추지 않는다).
- 보고 마지막 줄에 다음 형식을 그대로 낸다.
  ```
  RELEASE_CHECK_RESULT: <RELEASE_READY|RELEASE_BLOCKED>
  ```

## 금지 사항

- 이 Command는 배포를 실행하지 않는다(Vercel Production 배포, `git push`, 태그 생성 등을 하지 않는다) — 판정만 낸다.
- 실패한 검사를 이 Command 안에서 고치지 않는다. 무엇을 고쳐야 하는지만 안내한다(예: 특정 Wave에서 `/run-wave <WXX> --resume`, 특정 Task에서 `/prepare-task`·`/implement-task` 재실행).
- 확인할 수 없는 항목(도구 미설치, 접근 권한 없음 등)을 "문제 없음"으로 넘기지 않는다 — 실패로 기록하고 이유를 남긴다.
