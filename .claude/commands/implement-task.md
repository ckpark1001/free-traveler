---
description: prepare-task가 READY_TO_IMPLEMENT로 확인한 Task 정확히 1개를 Expected Files 범위 안에서 구현하고, 관련 검증을 실행한 뒤 변경/검증/제약을 보고한다.
argument-hint: WAVE_ID TASK_ID
---

# /implement-task

`traveler-project-pipeline` Skill, 저장소 루트 `CLAUDE.md`, `TASKS/TASK-<TASK_ID>.md`를 근거로 Task **정확히 1개**를 실제로 구현한다. 이 Command만이 이 파이프라인에서 `app/src/**`(실제 소스 코드)를 고치는 Command다.

Skill이 아직 컨텍스트에 없다면 먼저 `Skill(traveler-project-pipeline)`을 호출한다.

## 절차

### 0. 준비 상태 재확인 (규칙 1)

이전에 `/prepare-task`를 실행했다는 말만 믿지 않는다. **이 Command 실행 시점에 다시** `/prepare-task WAVE_ID TASK_ID`의 8가지 검사를 그대로 수행하고, 결과가 정확히 `READY_TO_IMPLEMENT`인지 확인한다.

- `READY_TO_IMPLEMENT`가 아니면 여기서 중단하고, 어떤 `BLOCKED_*` 판정이 나왔는지와 그 근거를 그대로 보고한다. **막힌 상태에서 구현을 시도하지 않는다.**
- 한 번의 실행에서 Task는 정확히 하나만 다룬다. 여러 Task ID를 한 번에 받았거나 "관련된 김에 다른 Task도" 같은 확장을 하지 않는다.

### 1. Task 내용 실제로 읽기

`TASKS/TASK-<TASK_ID>.md` 전체를 읽는다(Context, Project Scope, Requirement Ref, Screen/Route/Page Entry, Design Ref, Depends On, Expected Files, Functional AC, Visual AC, Security/Privacy AC, Test Cases, Verify, Definition of Done, Forbidden). 필요하면 Design Ref가 가리키는 `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json` 해당 절도 실제로 읽는다.

### 2. Expected Files 범위 안에서만 작업 (규칙 2)

- `## Expected Files`에 나열된 파일만 만들거나 고친다. 그 밖의 파일은 절대 건드리지 않는다.
- 구현 도중 Expected Files에 없는 변경이 꼭 필요해 보이면(예: 새 의존성을 추가하려면 `app/package.json`/`package-lock.json`을 고쳐야 하는데 Expected Files에 없는 경우) **그 변경을 임의로 확장해서 하지 않는다.** 구현을 중단하고 "Expected Files 범위 밖 변경이 필요함"을 제약사항으로 보고하며, Task 정의를 먼저 보완해야 한다고 안내한다.
- Page Owner가 아닌 Task는 자신의 Screen에 속하지 않는 파일이나 다른 Task의 Expected Files를 건드리지 않는다.

### 3. Functional / Visual / Security AC 그대로 따르기 (규칙 3)

- `## Functional AC`의 항목을 전부 코드로 충족시킨다. Page Owner라면 Section 순서와 최소 콘텐츠 수까지 정확히 맞춘다.
- `## Visual AC`를 그대로 지킨다 — Page Owner라면 Empty State/Placeholder 금지 규칙(Lorem ipsum·"준비 중"·"정보 확인 필요"·빈 Card 금지, 안내+이용 방법+CTA)을 실제 컴포넌트 동작으로 구현한다.
- `## Security/Privacy AC`를 그대로 지킨다 — 특히 항공·숙소 입력값 비전송, RLS 우회 금지, `service_role` 키 클라이언트 미사용 같은 항목은 타협하지 않는다.
- `## Forbidden`에 적힌 항목을 만들지 않았는지 스스로 대조한다.

### 4. Page Owner는 실제 Page Entry를 조립 (규칙 4)

Task Category가 `PAGE_OWNER`면:
- 지금 이 Task에서 새 Component 파일을 만들지 않는다 — `## Depends On`에 나열된, 이미 완료된 Component/Data/API Task의 결과물을 실제로 import해서 `Page Entry`(예: `app/src/app/page.tsx`) 하나를 완성한다.
- `PAGE-SCR001`이면 `create-next-app` 기본 스타터 잔재(Next.js 로고, "To get started" 문구, Vercel/Docs 버튼, `next.svg`/`vercel.svg` 참조 등)를 완전히 제거했는지 직접 diff로 확인한다.
- `PAGE-SCR003`이면 항공·숙소·동행 구하기 3탭이 실제로 한 화면에 조립되어 있는지 확인한다.
- `PAGE-SCR005`이면 Guest·Member·Admin 상태가 역할에 따라 실제로 분기 렌더링되는지 확인한다(권한 없는 사용자에게 관리자 영역이 렌더링되지 않는지 직접 확인).

### 5. 관련 Unit Test 실행 (규칙 5)

- Task의 `## Verify`에 `UNIT-*`가 있으면 해당 Vitest 테스트를 실행한다. 없어도 이 Task가 만드는 로직에 대응하는 기존 단위 테스트가 있으면 함께 돌린다.
- `app/package.json`에 Vitest가 아직 없다면(=`ARCHITECTURE.md` §16의 착수 차단 항목) 실행할 수 없다는 사실을 그대로 보고한다 — 실행한 것처럼 보고하지 않는다.
- 관련 Unit Test가 없는 Task(예: 순수 정적 데이터, 문서성 SHARED 유틸)는 왜 없는지 한 줄로 남긴다.

### 6. Page Owner 또는 E2E Task일 때만 Playwright Smoke 실행 (규칙 6)

- Task Category가 `PAGE_OWNER`이거나(그 Page Owner를 커버하는 `E2E-*` 시나리오가 있으면) **또는** 지금 구현 중인 Task 자체가 `E2E_TEST`(`E2E-PUBLIC-SMOKE`/`E2E-TRAVEL-TOOLS`/`E2E-MATE-AUTH`)일 때만 Playwright Chromium Smoke를 실행한다.
- 그 외 Category(`COMPONENT`, `DATA`, `DB`, `API`, `SHARED`, `UNIT_TEST`, `INTEGRATION_TEST`, `CI`, `MANUAL_CHECK`, `RELEASE_CHECK`)에서는 Playwright를 실행하지 않는다 — "확인 삼아" 돌리지 않는다.
- Playwright가 아직 설치되어 있지 않거나(`ARCHITECTURE.md` §16) 의존 Page Owner가 아직 조립되지 않아 화면이 뜨지 않으면, 실행하지 못했다는 사실과 이유를 그대로 보고한다.
- Chromium 프로젝트 외 브라우저를 추가하거나 실행하지 않는다.

### 7. 금지 기술 (규칙 7)

다음을 이번 구현에 추가하지 않는다: AWS·EC2 등 Vercel/Supabase 이외의 클라우드 인프라, Prisma를 포함한 어떤 ORM, GitHub Actions의 자동 Merge/auto-merge 기능. Task의 Functional AC를 만족시키기 위해 이런 것이 필요해 보이면 구현을 멈추고 그 사실을 보고한다 — 우회하거나 대체 구현을 임의로 만들지 않는다.

### 8. Diff 자체 검토

구현을 마치면 `git diff`(또는 상태 확인)로 다음을 스스로 확인한다.
- 변경된 파일이 `## Expected Files` 목록과 정확히 일치하는가(그 밖의 파일 변경 없음).
- `## Forbidden`에 해당하는 코드·문구가 없는가.
- `## Definition of Done` 체크리스트 항목이 실제로 충족되는가.

### 9. 완료 보고 (규칙 8)

항상 다음 세 가지를 포함해 보고한다(`CLAUDE.md` 규칙 23과 동일한 형식).
1. **변경 파일**: 실제로 만들거나 고친 파일 전체 목록(경로 그대로).
2. **검증 결과**: Lint/타입체크, 5단계 Unit Test, (해당 시) 6단계 Playwright 각각을 실행했는지와 통과 여부. 실행하지 않았다면 "실행하지 않음 — 이유"를 명시한다. 통과했다고 확인하지 않은 것을 통과했다고 말하지 않는다.
3. **남은 제약사항**: Definition of Done 중 아직 충족하지 못한 항목, Expected Files 밖 변경이 필요해서 멈춘 부분, 설치되지 않은 도구 때문에 검증하지 못한 부분 등을 전부 남긴다.

## Git 동작 — 기본적으로 Commit·Push·PR 자동 수행 안 함

- 이 Command는 기본적으로 `git add`/`git commit`/`git push`/PR 생성을 **하지 않는다**. 구현과 검증, 보고까지만 한다.
- **사용자가 명시적으로 요청한 경우에만** 이번 Task 단위로 Commit까지 수행할 수 있다.
  - Commit 범위는 이번 Task의 Expected Files로 실제로 변경된 파일에 한정한다(`git add <파일...>`로 필요한 파일만 스테이징 — `git add -A`/`git add .` 금지).
  - Commit 전에 `git status`/`git diff --staged`로 실제 스테이징된 내용을 확인한다.
  - Commit 메시지는 무엇을 왜 바꿨는지 간결하게 담고, 세션 시스템 리마인더에 지정된 Co-Authored-By 형식을 그대로 따른다.
  - Task 여러 개를 하나의 Commit으로 묶지 않는다 — 하나의 Commit은 하나의 Task에 대응한다.
- 사용자가 요청해도 **Push와 PR 생성은 이 Command의 범위 밖이다** — 절대 자동으로 하지 않는다(`CLAUDE.md` 규칙 20·21, DEC-012). Push/PR/Merge는 사용자가 직접 하거나, 별도의 명시적 지시로만 진행한다.
