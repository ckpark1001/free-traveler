# CLAUDE.md — Traveler Repository Root

이 파일은 `traveler` 저장소 전체에 적용되는 규칙을 담는다. 다른 Agent 규칙 파일(`AGENTS.md` 등)을 참조하지 않고, 필요한 규칙을 이 파일 안에 직접 적는다. 이 저장소에서 작업하는 모든 세션은 이 파일을 읽은 것으로 간주하고 행동한다.

## Harness Marker

```
HARNESS_SCHEMA=traveler-screen-route-v1
DESIGN_PATH=design-reference/D-001/DESIGN.md
SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json
PROJECT_SCOPE=docs/PROJECT_SCOPE.md
PLAYWRIGHT_ENABLED=true
PLAYWRIGHT_SCOPE=chromium-smoke
AUTO_MERGE=false
AWS_ENABLED=false
```

### 경로 해석 규칙 (마커 값을 실제 파일로 바꾸는 법)

이 저장소의 실제 Next.js 개발 루트는 저장소 루트가 아니라 **`app/`** 다.

| 마커/표기 | 실제 경로 |
|---|---|
| `PROJECT_SCOPE=docs/PROJECT_SCOPE.md` | `app/docs/PROJECT_SCOPE.md` |
| (SRS 정본) `docs/06_SRS_UIUX_REVISED.md` | `app/docs/06_SRS_UIUX_REVISED.md` |
| `DESIGN_PATH=design-reference/D-001/DESIGN.md` | 저장소 루트의 `design-reference/D-001/DESIGN.md` (그대로, `app/` 아래 아님) |
| `SCREEN_CONTRACT=design-reference/SCREEN_ROUTE_CONTRACT.json` | 저장소 루트의 `design-reference/SCREEN_ROUTE_CONTRACT.json` (그대로) |
| Page Entry (`src/app/...`) | `app/src/app/...` |
| `TASKS/`, `scripts/` | 저장소 루트 그대로 (`app/` 아래 아님) |

즉 "`docs/`"로 시작하는 문서 경로와 "`src/app/`"로 시작하는 코드 경로는 앞에 `app/`을 붙여서 찾고, `design-reference/`·`TASKS/`·`scripts/`는 저장소 루트에서 그대로 찾는다.

---

## 필수 규칙

1. **작업 전 확인**: 코드를 작성하기 전에 `app/package.json`(현재 설치된 버전)과 현재 세션에서 확인 가능한 Next.js 문서를 확인한다. 버전에 안 맞는 오래된 지식으로 API를 추측해서 쓰지 않는다.
2. **SRS 정본**: `app/docs/06_SRS_UIUX_REVISED.md`가 요구사항(REQ-FUNC-001~080, REQ-NF-001~034)의 유일한 정본이다. 다른 문서의 요구사항 서술과 충돌하면 이 문서가 이긴다.
3. **Scope 분류 정본**: `app/docs/PROJECT_SCOPE.md`가 각 요구사항의 IMPLEMENT/EXCLUDED 분류와 처리 방식의 정본이다.
4. **디자인 정본**: `design-reference/D-001/DESIGN.md`가 색상·타이포·간격·컴포넌트·화면별 Section 계약의 유일한 정본이다. `design-reference/vendor/**`(Airbnb 등)는 레이아웃 문법 참고용일 뿐이며 색상·폰트·상표를 그대로 가져오지 않는다.
5. **Screen 정본**: `design-reference/SCREEN_ROUTE_CONTRACT.json`이 Screen 목록·Route·Page Entry의 유일한 정본이다(`schema_version`은 `HARNESS_SCHEMA` 값과 일치해야 한다). Screen은 정확히 5개(SCR-001~005), 핵심 4개(SCR-001~004)·보조 1개(SCR-005)다.
6. **표준 개발 명령**: 실제 구현 착수는 `/run-wave WXX` 명령을 표준으로 사용한다. Task를 하나씩 개별로 지시하지 않는다.
7. **Wave 내부 순차 실행**: 한 Wave 안에서는 여러 Task를 동시에 건드리지 않는다. `TASKS/TASK_MANIFEST.csv`의 Depends On 순서(위상 정렬)를 따라 한 번에 정확히 하나의 Task만 구현한다.
8. **Expected Files 경계**: 지금 수행 중인 Task의 `TASKS/TASK-<ID>.md`에 적힌 Expected Files 목록 밖의 파일은 만들거나 수정하지 않는다. 공용 파일(레이아웃, 유틸 등)을 고쳐야 할 것 같으면 먼저 그 파일을 소유한 Task로 범위를 옮긴다.
9. **Page Owner는 조립만**: Page Owner Task(`PAGE-SCR00N`)는 자신의 Page Entry(`app/src/app/.../page.tsx`)에서 이미 만들어진 Component/Data/API Task 결과물을 import해서 조립하는 것까지만 한다. 새 Component 파일을 직접 만들지 않는다.
10. **SCR-001 완료 조건**: SCR-001(`/`, `app/src/app/page.tsx`) 작업을 완료로 보고하려면 `create-next-app` 기본 스타터(Next.js 로고, "To get started" 문구, Vercel Deploy/Docs 버튼 등)가 완전히 제거되어 있어야 한다.
11. **SCR-003 3탭 필수**: SCR-003(`/travel-tools`)은 항공·숙소·동행 구하기 3개 탭을 모두 한 화면에 조립해야 완료로 본다. 한 탭만 만들고 완료로 보고하지 않는다.
12. **항공·숙소 입력값 비전송**: 항공·숙소 조건(국가·지역·날짜)은 서버 API, DB, 외부 URL 쿼리, 서버/클라이언트 로그, 분석 이벤트 어디로도 보내지 않는다. Client Component의 React state에만 존재한다.
13. **Supabase 쓰기 범위 제한**: Supabase에 쓰기 작업을 하는 코드는 Auth(회원가입/로그인/세션), 동행(`mate_posts`, `mate_applications`, `blocks`), 신고(`reports`), 설정(`app_settings`) 범위를 벗어나지 않는다. 여행지·안전정보·대표 소개용 테이블을 새로 만들지 않는다.
14. **RLS 우회 금지**: Client 코드에서 RLS 정책을 우회하는 방식(예: `service_role` 키 사용, RLS가 걸리지 않은 별도 엔드포인트로 원본 데이터 직접 조회)을 쓰지 않는다. 모든 조회·쓰기는 인증된 사용자 세션 기준으로 RLS를 통과해야 한다.
15. **Service Role Key 사용 금지(Client)**: `service_role` 키는 어떤 Client Component/브라우저 코드/클라이언트 번들에도 포함하지 않는다. 서버 코드에서도 기본적으로 사용하지 않는다(이 프로젝트는 RLS만으로 권한을 처리한다).
16. **정적 데이터 사용**: 여행지·국가별 안전정보·대표 소개는 `app/src/data/*.ts` 정적 TypeScript 모듈로 관리한다. 이 세 도메인을 위한 Supabase 테이블이나 런타임 API를 만들지 않는다.
17. **금지 기술**: Prisma를 포함한 어떤 ORM도 추가하지 않는다. AWS·EC2 등 Vercel/Supabase 이외의 클라우드 인프라를 추가하지 않는다(`AWS_ENABLED=false`).
18. **Playwright 범위**: Playwright는 핵심 Smoke 흐름만 작성한다(`PLAYWRIGHT_SCOPE=chromium-smoke`) — Chromium 프로젝트만 사용하고 Firefox/WebKit/Safari 프로젝트를 추가하지 않는다. 시각 회귀·부하 테스트 도구를 도입하지 않는다.
19. **EXCLUDED 임의 구현 금지**: `app/docs/PROJECT_SCOPE.md`·`app/docs/UIUX_TRACEABILITY.md`·`TASKS/00_TASK_LIST.md` §2에서 EXCLUDED로 분류된 요구사항을 스스로 판단해 구현하지 않는다. 필요하다고 생각되면 구현 대신 사용자에게 먼저 확인한다.
20. **destructive Git 명령 금지**: `git push --force`, `git reset --hard`, `git clean -f`, `git branch -D` 등 되돌리기 어려운 Git 명령을 사용자의 명시적 지시 없이 실행하지 않는다.
21. **자동 PR·Merge 금지**: `AUTO_MERGE=false` — 어떤 자동화(GitHub Actions 포함)에도 자동 PR 생성이나 자동 Merge 기능을 넣지 않는다. PR 생성과 Merge는 사람이 수동으로 한다.
22. **Preview 확인 후 다음 Wave**: 화면(Screen) 단위 Wave를 끝내면 사람이 Preview(Vercel Preview 등)를 직접 확인하기 전까지 다음 화면 Wave로 넘어가지 않는다.
23. **완료 보고 형식**: 작업을 완료로 보고할 때는 항상 (1) 변경된 파일 목록, (2) 실행한 검증 결과(포맷/Lint/Unit Test/Playwright 등, 통과 여부 포함), (3) 남은 제한사항(아직 안 된 것, 알려진 한계)을 함께 보고한다. 검증을 실행하지 않았으면 "실행하지 않음"이라고 명시하고 통과했다고 말하지 않는다.

---

## Task 완료 순서

Task 하나를 수행할 때는 항상 아래 순서를 따른다. 순서를 건너뛰거나 뒤바꾸지 않는다.

1. **Task 읽기** — `TASKS/TASK-<ID>.md`의 Context/Requirement Ref/Screen·Route·Page Entry/Design Ref/Depends On/Expected Files/Functional·Visual·Security AC/Forbidden을 전부 읽는다.
2. **입력 확인** — Depends On에 나열된 Task가 실제로 끝나 있는지, 참조할 정본 문서(SRS/PROJECT_SCOPE/D-001/SCREEN_ROUTE_CONTRACT)가 Task 내용과 어긋나지 않는지 확인한다.
3. **구현** — Expected Files 목록 안의 파일만 만들거나 고친다. Functional/Visual/Security AC를 코드로 충족시킨다.
4. **관련 포맷·Unit Test** — 변경한 파일에 대해 `next lint`/타입체크(`tsc --noEmit`)를 돌리고, 이 Task와 관련된 Vitest 유닛 테스트가 있으면 실행한다.
5. **필요 시 Playwright** — Task의 Verify 열에 E2E Task(`E2E-*`)가 걸려 있고 해당 화면 흐름이 실제로 동작 가능한 상태면 Chromium Smoke를 실행한다. 아직 실행할 수 없는 상태면(의존 Task 미완료 등) 왜 못 돌렸는지 남긴다.
6. **Diff 확인** — 변경 사항이 Expected Files 범위를 벗어나지 않았는지, Forbidden 항목에 해당하는 코드가 없는지 diff를 직접 검토한다.
7. **완료 보고** — 규칙 23의 형식(변경 파일/검증 결과/남은 제한사항)으로 보고한다.
