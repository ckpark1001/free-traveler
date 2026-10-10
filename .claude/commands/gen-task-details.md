---
description: TASKS/00_TASK_LIST.md의 각 Task에 대해 TASKS/TASK-<TASK_ID>.md를 1:1로 생성·갱신하고 scripts/audit_tasks.py를 실행한다.
---

# /gen-task-details

`traveler-project-pipeline` Skill의 규칙에 따라 Task 상세 파일을 생성·갱신한다. 이 Command는 **실제 파일을 읽어서** 작업하며, `TASKS/00_TASK_LIST.md`나 기존 상세 파일의 내용을 추측하지 않는다. **구현 코드(`app/src/**`)는 만들지 않는다** — `TASKS/TASK-*.md` 문서만 다룬다.

Skill이 아직 컨텍스트에 없다면 먼저 `Skill(traveler-project-pipeline)`을 호출한다. `TASKS/00_TASK_LIST.md`가 없으면 먼저 `/gen-tasklist`를 실행하라고 안내하고 중단한다.

## 절차

1. `TASKS/00_TASK_LIST.md` §1 Task List를 실제로 읽어 전체 Task ID 목록을 확보한다.
2. `TASKS/` 아래 이미 존재하는 `TASK-*.md` 파일 목록을 확인한다.
   - Task List에 있고 상세 파일도 이미 있는 Task는 **내용이 실제로 달라져야 할 때만** 고친다. 이미 정확하면 새로 쓰지 않는다(멱등성).
   - Task List에 없는 Task ID의 상세 파일이 남아 있으면 정리 대상으로 보고한다(1:1 유지).
3. `python scripts/validate_inputs.py`를 다시 실행해 `app/src/app` 실제 트리 기준으로 Expected Files를 판단할 수 있게 한다(신규 생성 vs. 기존 파일 수정 구분).
4. Task List의 각 행에 대해 `TASKS/TASK-<Task ID>.md`를 Skill §5의 14개 절 형식으로 정확히 1개씩 작성한다(프런트매터 없음).
   - `Depends On`, `Requirement Ref`는 Task List 값과 정확히 일치시킨다.
   - `Expected Files`는 2~3단계에서 확인한 실제 트리와 대조해 신규/수정을 구분하고, "이 목록 밖의 파일은 만들거나 수정하지 않는다"를 명시한다.
   - Page Owner Task(`PAGE-SCR00N`)의 Functional AC/Visual AC는 다음을 모두 포함해야 한다.
     1. `design-reference/UI_CONTRACT.md`에서 가져온 해당 Screen의 영역 순서(번호 목록)
     2. 화면별 최소 콘텐츠 수(카드/타임라인/갤러리 등, 숫자로 명시)
     3. `PAGE-SCR001`이라면 스타터 제거 조건
     4. `PAGE-SCR003`이라면 항공·숙소·동행 3탭 조립 조건
     5. `PAGE-SCR005`이라면 Guest·Member·Admin 3상태 조립 조건
     6. Empty State/Placeholder 금지 고정 문구
   - 항공·숙소 관련 Task는 서버·DB·URL·로그 비전달 AC를 포함한다.
   - `DB-SCHEMA-BASE`는 Skill §5-1의 `Tables: ...` 줄을 정확히 1개 포함한다.
   - 모든 Task는 `Definition of Done`에 "Expected Files만 변경/AC 충족/Depends On 완료/Verify 통과/Forbidden 위반 없음"을, `Forbidden`에 "Expected Files 밖 수정 금지"를 포함한다.
5. 모든 상세 파일 작성이 끝나면 반드시 다음을 실행한다.
   ```
   python scripts/audit_tasks.py
   ```
6. 종료 코드와 출력(`AUDIT_PASS`/`AUDIT_FAIL`, `TASKS/TASK_AUDIT_REPORT.md`)을 사용자에게 **그대로** 보고한다. 실패를 축소하거나 "사소하다"고 재해석하지 않는다.
   - **`AUDIT_PASS`**: 통과한 검사 개수와 Task/Requirement 개수를 보고한다.
   - **`AUDIT_FAIL`**: 실패한 검사 번호와 상세 메시지를 전부 나열하고, 관련 `TASKS/TASK-*.md` 또는 `TASKS/00_TASK_LIST.md`를 수정한 뒤 감사를 다시 실행한다. **감사가 통과할 때까지 이 작업을 완료로 보고하지 않는다.**
7. 이 Command는 실제 소스 코드(`app/src/**`)를 수정하지 않는다 — Task 정의 문서만 다룬다.
