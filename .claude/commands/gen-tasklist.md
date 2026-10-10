---
description: Traveler 승인 산출물(SRS/Scope/UI Contract/Screen Route Contract)로부터 TASKS/00_TASK_LIST.md를 생성하거나 갱신한다.
---

# /gen-tasklist

`traveler-project-pipeline` Skill의 규칙에 따라 Task List를 생성 또는 갱신한다. 이 Command는 **실제 파일을 읽어서** 작업하며, 기억이나 이전 대화 내용으로 내용을 추측해 채우지 않는다. **구현 코드(`app/src/**`)는 만들지 않는다** — `TASKS/00_TASK_LIST.md` 문서만 다룬다.

Skill이 아직 컨텍스트에 없다면 먼저 `Skill(traveler-project-pipeline)`을 호출해 규칙 전문을 로드한 뒤 아래 절차를 수행한다.

## 절차

1. `python scripts/validate_inputs.py`를 저장소 루트에서 실행한다. 종료 코드가 0이 아니면 오류 내용을 사용자에게 그대로 보여주고 **여기서 중단**한다 — 오류를 추측으로 고치거나 무시하고 진행하지 않는다.
2. `TASKS/00_TASK_LIST.md`가 이미 존재하는지 확인한다.
   - **존재하면**: 먼저 그 파일 전체를 읽는다. 이번 실행은 "새로 만들기"가 아니라 "무엇이 실제로 달라졌는지"를 반영하는 갱신 작업이다. 입력 문서(SRS/Scope/UI Contract/Screen Route Contract) 대비 이미 정확한 행은 그대로 두고, 실제로 달라진 부분만 고친다.
   - **없으면**: 처음부터 만든다.
3. 다음 문서를 실제로 열어 읽는다 — 요약해서 알고 있다고 가정하지 않는다.
   - `app/docs/06_SRS_UIUX_REVISED.md` §4 (Requirement 원문·Scope·Screen)
   - `app/docs/PROJECT_SCOPE.md` (REQ별 IMPLEMENT/EXCLUDED 1차 정본, 처리 방법, Playwright SM-01~10, §5 일반 제외 기능)
   - `design-reference/UI_CONTRACT.md` (Screen별 영역 순서·주요 Component·상태·이동·반응형·금지 기능)
   - `design-reference/D-001/DESIGN.md` (Section 계약, 최소 콘텐츠 수, Empty State/Placeholder 금지 규칙, Do/Do Not)
   - `design-reference/SCREEN_ROUTE_CONTRACT.json` (Screen/Route/Page Entry 정본)
   - `app/src/app/**`(실제 파일 트리) — Expected Files 작성 전 반드시 스캔한다.
4. `traveler-project-pipeline` Skill §4의 분해 알고리즘을 그대로 실행해 Task를 확정한다. 특히 다음을 스스로 점검한다.
   - Screen 5개당 Page Owner Task 정확히 1개, Route/Page Entry는 `SCREEN_ROUTE_CONTRACT.json` 값 그대로
   - `PAGE-SCR001`에 스타터 제거 AC
   - `PAGE-SCR003`에 항공·숙소·동행 3탭 조립 AC + 3개 이상 Component Task 의존
   - `PAGE-SCR005`에 Guest·Member·Admin 3상태 조립 AC + Component Task 의존
   - 여행지·안전·대표 = `DATA-*` 정적 데이터 Task, DB는 6개 테이블 목표(`DB-SCHEMA-BASE`/`DB-RLS-BASE`/`DB-ACCESS`/`DB-SEED-BASE` 4역할)
   - 항공·호텔 Task AC에 서버·DB·URL·로그 비전달 문구
   - Playwright Task는 Chromium Smoke 2~3개(`E2E-*`)
   - 자동 Merge/EC2/AWS Task 없음
   - Task ID 중복 없음, Depends On 전부 존재, 순환 의존 없음
   - 모든 Page Owner AC에 영역 순서 + 최소 콘텐츠 수, Empty State/Placeholder 금지 고정 문구
5. `TASKS/00_TASK_LIST.md`를 다음 세 섹션으로 작성한다.
   - **§1 Task List**: `| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |` 16열 표.
   - **§2 NON_IMPLEMENTATION**: `app/docs/PROJECT_SCOPE.md`가 EXCLUDED로 확정한 요구사항을 `| Requirement | 근거 | 후속 방향 |`로 기록한다. 이 요구사항들에는 §1에 Task를 만들지 않는다.
   - **§3 Requirement Coverage Verification**: REQ-FUNC 80개·REQ-NF 34개 전부를 `| Requirement | Status | Task ID(s) |` 한 줄씩으로 기록한다. IMPLEMENT는 §1의 Task ID(s)를 연결하고, EXCLUDED는 Task ID(s)를 항상 `-`로 둔다.
6. 파일 저장 후 Task 개수를 세어 보고하되, 45~65 범위를 벗어나도 실패로 취급하지 않는다 — 참고 정보로만 알린다.
7. 다음 단계로 `/gen-task-details`를 실행할 수 있음을 안내한다. 이 Command는 상세 파일(`TASKS/TASK-*.md`)까지 만들지 않는다.
8. 이후 `python scripts/audit_tasks.py`가 `AUDIT_FAIL`(종료 코드 1)을 내면 실패를 무시하거나 축소하지 않는다 — 실패 항목을 그대로 보고하고 Task List를 고친 뒤 감사를 다시 실행하도록 안내한다.
