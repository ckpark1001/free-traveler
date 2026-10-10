---
description: 구현 착수 전 Task 1개(WAVE_ID/TASK_ID)가 실제로 시작 가능한 상태인지 8가지를 검사하고 READY_TO_IMPLEMENT 또는 BLOCKED_* 판정을 낸다. 코드를 수정하지 않는다.
argument-hint: WAVE_ID TASK_ID
---

# /prepare-task

`traveler-project-pipeline` Skill과 저장소 루트 `CLAUDE.md`의 규칙을 근거로, 특정 Task를 지금 구현해도 되는지 순수 점검만 한다. **이 Command는 어떤 파일도 만들거나 고치지 않는다** — `app/src/**`는 물론 `TASKS/**` 문서도 수정하지 않는다. 판정과 근거만 보고한다.

Skill이 아직 컨텍스트에 없다면 먼저 `Skill(traveler-project-pipeline)`을 호출한다.

## 입력

- `WAVE_ID` — 지금 진행 중인 Wave 식별자(예: `W01`). 사용자가 인자로 준다.
- `TASK_ID` — 점검할 Task ID(예: `PAGE-SCR001`). 사용자가 인자로 준다.
- **선택된 상세 Task 파일** — `TASKS/TASK-<TASK_ID>.md`. 별도 인자가 아니라 `TASK_ID`로부터 파생되는 실제 파일이며, 반드시 이 파일을 직접 읽는다(내용을 추측하지 않는다).

인자가 없거나 `TASKS/TASK-<TASK_ID>.md`가 존재하지 않으면 즉시 `BLOCKED_INPUT`으로 보고하고 중단한다.

## 검사 절차

아래 8가지를 순서대로, 전부 실제로 확인한다. 하나라도 실패하면 그 시점에서 판정을 확정하고 나머지 검사도 계속 수행해 보고서에 함께 남긴다(사용자가 한 번에 여러 문제를 볼 수 있게).

### 1. Working Tree 상태
`git status --porcelain`을 실행한다. 추적되지 않는 파일을 포함해 어떤 변경이라도 있으면 — 특히 이번 Task의 Expected Files 밖에서 변경이 있으면 — **`BLOCKED_DIRTY_TREE`** 후보로 기록한다. 완전히 깨끗하면 통과.

### 2. Task가 현재 Wave에 포함되는지
`TASKS/WAVE_PLAN.md`가 있는지 확인한다.
- **있으면** 그 문서에서 `WAVE_ID`에 속한 Task 목록을 찾아 `TASK_ID`가 포함되는지 확인한다. 없으면 **`BLOCKED_INPUT`**.
- **없으면**(현재 저장소 상태) — Wave를 검증할 정본이 없다는 뜻이다. 이 경우 임의로 통과시키지 말고 **`BLOCKED_INPUT`**으로 보고하며, 사유를 "TASKS/WAVE_PLAN.md가 없어 WAVE_ID 소속을 검증할 수 없음 — 먼저 Wave 계획 문서를 만들어야 함"이라고 명시한다.

### 3. Depends On 완료 여부
`TASKS/TASK-<TASK_ID>.md`의 `## Depends On`에 나열된 각 Task ID에 대해, 그 Task가 실제로 끝났다는 증거(예: Expected Files가 실제로 존재하고, 관련 Verify/테스트가 통과했다는 기록)를 확인한다. 증거가 없거나 Depends On Task 자체가 아직 미착수 상태면 **`BLOCKED_DEPENDENCY`**로 기록하고 어떤 Depends On이 안 끝났는지 전부 나열한다.

### 4. Expected Files
`## Expected Files`를 읽고 각 항목의 "신규 생성"/"수정" 표시가 `app/` 실제 파일 트리와 맞는지 확인한다(신규라는데 이미 있음, 수정이라는데 없음 등 불일치가 있으면 표시). Expected Files 목록이 비어 있거나 형식이 불명확하면 **`BLOCKED_INPUT`**. 목록에 있는 파일이 1단계에서 이미 변경 상태로 잡혔다면 **`BLOCKED_DIRTY_TREE`**로 합산한다.

### 5. SRS·Scope·Design·Screen Ref 무결성
- `## Requirement Ref`의 각 REQ ID가 `app/docs/06_SRS_UIUX_REVISED.md`에 실제로 존재하는지 확인한다.
- 그 REQ ID들의 분류가 `app/docs/PROJECT_SCOPE.md`에서 **IMPLEMENT**인지 확인한다(8번 검사와 연동).
- `## Design Ref`가 가리키는 절이 `design-reference/D-001/DESIGN.md`/`design-reference/UI_CONTRACT.md`에 실제로 존재하는지 확인한다.
- `## Screen / Route / Page Entry`가 `design-reference/SCREEN_ROUTE_CONTRACT.json`의 값과 정확히 일치하는지 확인한다(Page Owner Task에 한함).
- 어느 하나라도 실제 문서에서 확인되지 않으면(존재하지 않는 REQ ID, 없는 절, Screen 정본과 불일치 등) **`BLOCKED_INPUT`**.

### 6. 필요한 환경변수 이름
Task의 Context/Functional AC/Security-Privacy AC를 읽고 이 Task가 실행 중 참조해야 하는 환경변수 이름을 추출한다(예: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `FLIGHT_OUTBOUND_URL`, `HOTEL_OUTBOUND_URL`, `MOFA_SAFETY_URL`). `.env.local` 또는 `.env.example`이 저장소에 있는지, 그 안에 필요한 이름이 선언되어 있는지 확인한다(값 자체가 맞는지는 확인하지 않는다 — 이름 존재 여부만). 이 Task에 필요한 이름이 어디에도 없으면 **`BLOCKED_INPUT`**이고, 어떤 이름이 없는지 나열한다. 이 Task가 환경변수를 쓰지 않으면 통과.

### 7. Secret 하드코딩 위험
Task 설명·AC 어디에도 실제 키·토큰·비밀번호 값처럼 보이는 문자열이 없는지, 그리고 Task가 `service_role` 키나 다른 비밀값을 Client Component/공개 파일에 넣도록 요구하고 있지 않은지 확인한다. Expected Files 중 이미 존재하는 파일이 있다면 그 파일도 훑어 하드코딩된 비밀값 패턴(긴 base64/hex 문자열이 `NEXT_PUBLIC_` 이외의 이름으로 소스에 박혀 있는 경우 등)이 없는지 확인한다. 위험이 발견되면 **`BLOCKED_SCOPE`**.

### 8. EXCLUDED 범위 침범 여부
`## Requirement Ref`의 REQ ID 중 하나라도 `app/docs/PROJECT_SCOPE.md`에서 **EXCLUDED**로 분류되어 있으면, 또는 Task 설명이 `app/docs/PROJECT_SCOPE.md` §5 "일반 제외 기능"(CMS, 외부 Email 공급자, Monitoring, EC2·AWS, 자동 Merge 등)에 해당하는 것을 만들라고 하면 **`BLOCKED_SCOPE`**로 기록한다.

## 판정 규칙

- 8가지 검사가 전부 통과해야 **`READY_TO_IMPLEMENT`**다.
- 하나라도 실패하면 다음 우선순위로 최종 판정을 하나 선택해 보고한다(가장 근본적인 문제부터): `BLOCKED_INPUT` > `BLOCKED_DEPENDENCY` > `BLOCKED_DIRTY_TREE` > `BLOCKED_SCOPE`. 단, 실패한 검사는 우선순위와 무관하게 **전부** 보고서에 나열한다 — 하나만 골라 나머지를 숨기지 않는다.
- 판정 결과는 보고 마지막 줄에 다음 형식 그대로 낸다(자동화가 파싱할 수 있도록).
  ```
  PREPARE_TASK_RESULT: <READY_TO_IMPLEMENT|BLOCKED_INPUT|BLOCKED_DEPENDENCY|BLOCKED_DIRTY_TREE|BLOCKED_SCOPE>
  ```

## 금지 사항

- 이 Command는 코드를 수정하지 않는다 — `app/src/**`뿐 아니라 `TASKS/**` 문서도 고치지 않는다. 문제를 발견해도 스스로 고치지 말고 판정과 근거만 보고한다.
- 확인되지 않은 사실을 근거로 `READY_TO_IMPLEMENT`를 내지 않는다 — 8가지 중 하나라도 실제로 확인하지 못했다면(파일을 못 읽었다 등) 그 항목을 실패로 처리하고 `BLOCKED_INPUT`으로 보고한다.
