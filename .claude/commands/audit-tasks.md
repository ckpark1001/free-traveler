---
description: scripts/audit_tasks.py를 실행해 TASKS/00_TASK_LIST.md와 TASKS/TASK-*.md가 traveler-project-pipeline 규칙을 지키는지 감사한다.
---

# /audit-tasks

`TASKS/00_TASK_LIST.md`와 `TASKS/TASK-*.md`가 `traveler-project-pipeline` Skill의 규칙을 지키는지 독립적으로 재검사한다. **Task를 생성·수정하지 않는다** — 순수 감사 전용 Command다. **구현 코드도 만들지 않는다.**

Skill이 아직 컨텍스트에 없다면 먼저 `Skill(traveler-project-pipeline)`을 호출한다.

## 절차

1. `TASKS/00_TASK_LIST.md`가 실제로 존재하는지 확인한다. 없으면 "아직 Task List가 없습니다. `/gen-tasklist`를 먼저 실행하세요."라고 안내하고 중단한다.
2. 다음을 실행한다.
   ```
   python scripts/audit_tasks.py
   ```
3. 스크립트의 종료 코드와 표준출력(`AUDIT_PASS (N checks)` 또는 `AUDIT_FAIL (...)`, `TASKS/TASK_AUDIT_REPORT.md`, `TASKS/TASK_MANIFEST.csv`)을 **있는 그대로** 사용자에게 보고한다. 결과를 요약하되 실패 항목을 빠뜨리거나 "문제 없다"는 식으로 재해석하지 않는다.
   - 검사 1~18번 전체를 표로 요약한다(항목명은 스크립트 출력·`TASKS/TASK_AUDIT_REPORT.md`의 표기를 그대로 쓴다).
   - Task 개수(45~65 기대치 대비 실제 개수)는 정보성으로만 언급하고 PASS/FAIL 판정에 포함하지 않는다.
   - FAIL 항목이 있으면 관련 Task ID와 `TASKS/TASK-<ID>.md` 경로를 함께 제시해 사용자가 바로 무엇을 고쳐야 하는지 알 수 있게 한다.
4. **종료 코드가 0이 아니면 절대 "완료" 또는 "통과"로 보고하지 않는다.** 이 Command 스스로는 실패를 고치지 않는다 — 수정이 필요하면 사용자에게 `/gen-task-details`로 다시 생성하거나 해당 파일을 직접 수정한 뒤 `/audit-tasks`를 다시 실행하도록 안내한다.
