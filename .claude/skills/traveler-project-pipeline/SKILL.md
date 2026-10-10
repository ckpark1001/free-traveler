---
name: traveler-project-pipeline
description: Free Traveler의 승인된 5개 Screen·SRS·범위 문서를 근거로 구현 Task List/상세/감사를 생성·검증하는 파이프라인. /gen-tasklist, /gen-task-details, /audit-tasks 명령과 함께 사용한다.
---

# Traveler Project Pipeline

이 Skill은 Free Traveler 저장소에서 "승인된 UI/UX 산출물 → 구현 Task"로 이어지는 생성 파이프라인의 규칙을 정의한다. `/gen-tasklist`, `/gen-task-details`, `/audit-tasks` 세 Command가 이 Skill의 규칙을 그대로 따른다. 이 Skill 자체는 코드를 생성하지 않는다 — Task 정의와 그 정합성만 다룬다.

> 이 문서는 저장소 루트 `CLAUDE.md`와 함께 갱신된 최신본이다. `CLAUDE.md`가 저장소 전체(개발 실행 규칙)를 다룬다면, 이 Skill은 그중 "Task 생성·상세화·감사" 파이프라인만 좁게 다룬다. 두 문서의 Harness Marker/상수는 항상 같은 값을 가져야 한다.

## 0. 상수

```
HARNESS_SCHEMA = "traveler-screen-route-v1"
```

`design-reference/SCREEN_ROUTE_CONTRACT.json`의 `schema_version`이 `HARNESS_SCHEMA`와 정확히 일치하지 않으면 파이프라인의 어떤 단계도 진행하지 않는다(하드 실패).

## 1. 정본 입력(Canonical Inputs)

모든 경로는 저장소 루트(`C:\AI_SERVICE\traveler`) 기준이다. 실제 Next.js 개발 루트는 `app/`이므로 "docs/"·"src/app/"로 시작하는 경로는 앞에 `app/`을 붙인다(`CLAUDE.md` DEC-001과 동일).

| 문서 | 경로 | 역할 |
|---|---|---|
| SRS(개정) | `app/docs/06_SRS_UIUX_REVISED.md` | REQ-FUNC-001~080, REQ-NF-001~034 원문·Scope·Screen |
| 프로젝트 범위 | `app/docs/PROJECT_SCOPE.md` | **REQ IMPLEMENT/EXCLUDED 분류의 1차 정본**(`scripts/audit_tasks.py`가 이 파일을 직접 파싱한다) |
| 추적표(보조) | `app/docs/UIUX_TRACEABILITY.md` | PROJECT_SCOPE.md에서 파생된 114개 Requirement × Screen/Route/Page Entry 상세 매핑. PROJECT_SCOPE.md와 분류가 어긋나면 PROJECT_SCOPE.md가 이긴다 |
| 디자인 정본 | `design-reference/D-001/DESIGN.md` | 색상·타이포·간격·Section 계약·화면별 최소 콘텐츠 수·Empty State 금지 규칙 |
| UI 계약 | `design-reference/UI_CONTRACT.md` | 화면별 영역 순서·주요 Component·상태·이동·반응형·금지 기능 |
| Screen Route 정본 | `design-reference/SCREEN_ROUTE_CONTRACT.json` | **Screen 목록·Route·Page Entry의 유일한 정본**(규칙 2) |
| 앱 매니페스트 | `app/package.json` | 기술 스택 확인(Next.js/React/TypeScript/Tailwind 버전, 아직 없는 의존성 확인) |
| 실제 코드 트리 | `app/src/app/**` | Expected Files 작성 전 반드시 스캔(규칙 4) |
| 아키텍처·결정 | `app/docs/ARCHITECTURE.md`, `app/docs/DECISION_LOG.md` | 구현 경계와 그 근거(왜 6개 테이블인지, 왜 정적 데이터인지 등)의 서술적 근거 |
| 기존 산출물 | `TASKS/00_TASK_LIST.md`, `TASKS/TASK-*.md` | 이미 생성된 Task List/상세가 있으면 **처음부터 다시 만들지 않고** 이 파일들을 먼저 읽어 갱신 대상만 바꾼다(규칙 21) |

`design-reference/UI_CONTRACT.md`의 서술과 `SCREEN_ROUTE_CONTRACT.json`의 값이 다르면 **JSON이 항상 이긴다**(규칙 2). 어떤 Command도 JSON 없이 Screen 목록을 임의로 나열하지 않는다.

## 2. 핵심 규칙

| # | 규칙 | 적용 시점 |
|---|---|---|
| 1 | `HARNESS_SCHEMA`는 `traveler-screen-route-v1`이다. | validate_inputs.py, 모든 Command 진입 시 |
| 2 | Screen 목록의 정본은 `SCREEN_ROUTE_CONTRACT.json`이다. | gen-tasklist |
| 3 | 정확히 5개 Screen 각각에 Page Owner Task를 하나 만든다(`PAGE-SCR00N`). | gen-tasklist, audit_tasks.py(#5) |
| 4 | 실제 `app/src/app` 파일 트리를 확인한 뒤 Expected Files를 쓴다. | gen-tasklist, gen-task-details |
| 5 | Page Owner와 Component Task를 구분한다. | gen-tasklist |
| 6 | Page Owner는 같은 Screen의 Component Task에 의존한다. | gen-tasklist, audit_tasks.py(#4, #7) |
| 7 | `src/app/page.tsx`(SCR-001) Owner는 Next.js Starter 제거 AC를 가진다. | gen-tasklist, audit_tasks.py(#8) |
| 8 | `/travel-tools`(SCR-003) Owner는 항공·숙소·동행 탭을 실제 조립한다. | gen-tasklist, audit_tasks.py(#9) |
| 9 | `/account`(SCR-005) Owner는 Guest·Member·Admin 상태를 실제 조립한다. | gen-tasklist, audit_tasks.py(#10) |
| 10 | DB는 6개 테이블(`profiles`, `mate_posts`, `mate_applications`, `blocks`, `reports`, `app_settings`)을 목표로 하고 절대 크게 넘기지 않는다(감사 하드 한도 8개). | gen-tasklist, audit_tasks.py(#12) |
| 11 | 여행지·안전·대표는 정적 데이터 Task(`DATA-*`)로 만든다. | gen-tasklist, audit_tasks.py(#9 문서 카테고리 확인) |
| 12 | 항공·숙소 입력값을 서버·DB·URL·로그·분석으로 보내지 않는다. | gen-tasklist, audit_tasks.py(#13) |
| 13 | 자동 Merge·EC2·AWS를 만드는 Task를 만들지 않는다. | gen-tasklist, audit_tasks.py(#16) |
| 14 | REQ-FUNC 80개·REQ-NF 34개 전부에 IMPLEMENT 또는 EXCLUDED 상태를 기록한다. | gen-tasklist, audit_tasks.py(#17) |
| 15 | EXCLUDED는 상세 구현 Task/파일을 만들지 않지만 표에서 삭제하지 않는다. | gen-tasklist, gen-task-details, audit_tasks.py(#18) |
| 16 | Task List와 상세 파일이 1:1이어야 한다. | gen-task-details, audit_tasks.py(#1) |
| 17 | Task ID는 중복되지 않고, Depends On은 존재하는 Task만 가리키며, 순환 의존이 없어야 한다. | gen-tasklist, audit_tasks.py(#2, #3, #4) |
| 18 | 모든 Page Owner의 Route·Page Entry는 `SCREEN_ROUTE_CONTRACT.json`과 정확히 일치하고, Expected Files에 그 Page Entry가 포함되어야 한다. | gen-tasklist, audit_tasks.py(#6) |
| 19 | Component만 있고 Page Owner가 없는 Screen(오타 포함)이 없어야 한다. | audit_tasks.py(#7) |
| 20 | 상세 생성 후 반드시 `python scripts/audit_tasks.py`를 실행하고, 실패를 무시하거나 축소 보고하지 않는다. | gen-task-details, audit-tasks |
| 21 | 기존 `TASKS/00_TASK_LIST.md`/`TASKS/TASK-*.md`가 있으면 처음부터 새로 만들지 않고, 실제로 달라진 부분만 갱신한다(멱등성). | gen-tasklist, gen-task-details |
| 22 | Page Owner AC에 화면별 Section 순서와 최소 콘텐츠 수를 기록한다. | gen-tasklist, audit_tasks.py(#15) |
| 23 | Page Owner는 큰 빈 영역·Placeholder 문구를 금지하고 완성형 Empty State(안내+이용 방법+CTA)를 요구한다. | gen-tasklist, audit_tasks.py(#16) |
| 24 | Playwright는 Chromium 프로젝트만 쓰는 Smoke Task 2~3개로 5~7개 핵심 흐름을 묶는다(그 이상 늘리지 않는다). | gen-tasklist, audit_tasks.py(#15) |
| 25 | Auth 관련 Task는 성인 확인을, RLS 관련 Task는 RLS/정책을 명시적으로 언급해야 한다. | gen-tasklist, audit_tasks.py(#14) |
| 26 | DB Task는 Schema·RLS·Access·Seed 4가지 역할이 모두 존재해야 한다. | gen-tasklist, audit_tasks.py(#11) |

## 3. Task 산출물 위치 규약

```
TASKS/
  00_TASK_LIST.md         # §1 Task List(16열 표) + §2 NON_IMPLEMENTATION + §3 Requirement Coverage Verification
  TASK-<TASK_ID>.md        # Task 1개당 파일 1개, 14개 절(§5) — 예: TASK-PAGE-SCR001.md
  TASK_MANIFEST.csv        # scripts/audit_tasks.py 산출물 — 전체 Task 평면 나열(CSV)
  TASK_AUDIT_REPORT.md     # scripts/audit_tasks.py 산출물 — 검사 1~18 PASS/FAIL 표
```

`tasks/`(소문자)나 `tasks/details/` 같은 경로는 **쓰지 않는다** — Windows에서는 대소문자 구분이 없어 헷갈리지 않지만, GitHub Actions(Linux, 대소문자 구분)에서는 다른 경로로 취급되어 CI가 깨진다.

Task ID 접두사(실제 `TASKS/TASK_MANIFEST.csv`에서 쓰는 표기):

| 접두사 예시 | Category | 의미 |
|---|---|---|
| `PAGE-SCR001` ~ `PAGE-SCR005` | PAGE_OWNER | Screen당 정확히 1개 |
| `CMP-SCR001-HERO-SEARCH` 등 | COMPONENT | 해당 Screen 전용 컴포넌트/영역 단위 작업 |
| `DATA-DESTINATIONS`, `DATA-SAFETY`, `DATA-REPRESENTATIVE` | DATA | 여행지·안전·대표 정적 데이터(규칙 11) |
| `DB-SCHEMA-BASE`, `DB-RLS-BASE`, `DB-ACCESS`, `DB-SEED-BASE` | DB | Supabase 스키마·RLS·클라이언트·시드(규칙 26, 최대 6개 테이블) |
| `API-MATES-CRUD` 등 | API | Route Handler |
| `SHARED-LAYOUT-NAV-FOOTER` 등 | SHARED | 레이아웃·SEO·즐겨찾기·외부링크 유틸 등 전체 화면 공통 |
| `UNIT-TRAVEL-DATES` 등 | UNIT_TEST | Vitest 단위 테스트 |
| `TEST-RLS-BASIC` | INTEGRATION_TEST | 로컬 Supabase 대상 통합 테스트 |
| `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH` | E2E_TEST | Playwright Chromium Smoke(정확히 2~3개, 규칙 24) |
| `CI-TYPECHECK-LINT` | CI | GitHub Actions 파이프라인 설정 |
| `MANUAL-*` | MANUAL_CHECK | 코드 산출물 없는 배포 전 수동 점검 |
| `RELEASE-*` | RELEASE_CHECK | 배포 전/배포 시점 확인 절차 |

## 4. Task 분해 지침(gen-tasklist가 따르는 알고리즘)

1. `python scripts/validate_inputs.py`를 실행하고 실패 시 중단한다.
2. `TASKS/00_TASK_LIST.md`가 이미 있으면 먼저 읽는다(규칙 21). 처음 만드는 것이 아니라면 이 단계부터는 "무엇이 실제로 바뀌었는가"만 반영하는 갱신 작업이다.
3. `SCREEN_ROUTE_CONTRACT.json.screens`를 순회하며 Screen당 `PAGE-SCR00N` 1개를 만든다(규칙 3). Route/Page Entry는 JSON 값을 그대로 쓴다(규칙 2, 18).
4. 각 Screen의 `design-reference/UI_CONTRACT.md` "주요 Component" 목록을 3~7개의 응집된 그룹으로 묶어 `CMP-SCR00N-*` Task를 만든다(규칙 5).
   - SCR-003은 반드시 항공 탭, 숙소 탭, 동행 작성 탭을 별개의 Component Task로 만든다(규칙 8 준비).
   - SCR-005는 반드시 인증(Guest), 프로필/내 활동(Member), 관리자(Admin) 상태를 별개의 Component Task로 만든다(규칙 9 준비).
5. 여행지·국가 안전정보·대표 프로필은 각각 `DATA-DESTINATIONS`, `DATA-SAFETY`, `DATA-REPRESENTATIVE` Task로 만든다(규칙 11). 이 세 도메인은 DB 테이블을 만들지 않는다.
6. 실제 쓰기가 필요한 도메인만 `DB-SCHEMA-BASE`(스키마), `DB-RLS-BASE`(정책), `DB-ACCESS`(클라이언트/쿼리), `DB-SEED-BASE`(시드) 4개 Task로 나눠 6개 테이블을 설계한다(규칙 10, 26). 6개를 크게 초과하는 테이블이 필요하면 Task를 만들지 말고 범위를 재검토한다.
7. 항공·호텔 조건 입력 Component/Owner Task의 AC에는 "국가·지역·날짜를 서버 DB·서버 로그·분석 이벤트·외부 URL 쿼리에 전달하지 않는다"를 문자 그대로 포함한다(규칙 12).
8. 테스트는 `UNIT-*`(날짜 검증/연락처 탐지/상태 전이), `TEST-RLS-BASIC`(RLS 통합), `E2E-*` 2~3개(Chromium Smoke, 규칙 24)로 구성한다. Chromium 외 브라우저 프로젝트나 4개 이상의 E2E 스위트를 만들지 않는다.
9. 다음 Task는 절대 만들지 않는다: 자동 Merge/머지 봇, EC2, AWS(또는 Vercel/Supabase 외의 별도 클라우드 인프라)(규칙 13).
10. `app/docs/PROJECT_SCOPE.md`를 1차 정본으로 해서 REQ-FUNC 80개·REQ-NF 34개를 전수 순회해 `00_TASK_LIST.md` **§3 Requirement Coverage Verification**에 `| Requirement | Status | Task ID(s) |` 형태로 한 줄씩 기록한다(규칙 14). EXCLUDED 항목은 **§2 NON_IMPLEMENTATION**에 근거·후속 방향과 함께 기록하고, §3에서는 Task ID(s)를 항상 `-`로 둔다(규칙 15) — 어느 표에서도 행을 지우지 않는다.
11. `app/src/app`를 실제로 스캔한 뒤(규칙 4) 각 Task의 Expected Files를 작성한다. 이미 존재하는 파일은 "수정"으로, 존재하지 않는 파일은 "신규 생성"으로 표시한다.
12. `PAGE-SCR001`(Route `/`, `src/app/page.tsx`)의 AC에는 `create-next-app` 기본 스타터 제거를 명시적인 완료 조건으로 포함한다(규칙 7).
13. `PAGE-SCR003`(Route `/travel-tools`)의 AC에는 항공 탭·숙소 탭·동행 구하기 탭 3개를 **한 페이지 안에서 실제로 조립**했다는 조건을 포함하고, 대응하는 3개 이상의 `CMP-SCR003-*` Task를 Depends On에 명시한다(규칙 6, 8).
14. `PAGE-SCR005`(Route `/account`)의 AC에는 Guest·Member·Admin 3개 상태를 **한 페이지 안에서 역할에 따라** 조립했다는 조건을 포함하고, 대응하는 Component Task를 Depends On에 명시한다(규칙 6, 9).
15. 모든 Page Owner Task의 Functional AC에 `design-reference/UI_CONTRACT.md`의 "영역 순서"를 번호 목록(`1) ... 2) ...`)으로 옮기고, 최소 콘텐츠 수를 숫자로 명시한다(규칙 22).
16. 모든 Page Owner Task의 Visual AC에 Empty State/Placeholder 금지 고정 문구(규칙 23, Lorem ipsum·'준비 중'·'정보 확인 필요' 명시)를 포함한다.
17. Task ID 중복이 없는지, Depends On이 전부 존재하는 Task를 가리키는지, 순환 의존이 없는지 스스로 점검한다(규칙 17).
18. 완성된 `00_TASK_LIST.md`의 Task 개수를 세되, 45~65개 범위는 참고용 기대치일 뿐 통과/실패 기준으로 사용하지 않는다.

## 5. Task 상세 파일 규칙(gen-task-details가 따르는 규칙)

- `00_TASK_LIST.md` §1에 있는 Task 각각에 대해 `TASKS/TASK-<TASK_ID>.md`를 정확히 1개 생성한다(규칙 16). 이미 같은 ID의 파일이 있으면 새로 만들지 않는다(규칙 21) — 내용을 실제로 바꿔야 할 때만 그 파일을 고친다.
- 상세 파일은 프런트매터 없이 아래 14개 절만 이 순서로 포함한다.

```markdown
# <TASK_ID>

<한 줄 제목>

## Context
(이 Task가 무엇이고 전체에서 어떤 역할인지 한 문단)

## Project Scope
(app/docs/PROJECT_SCOPE.md 기준 IMPLEMENT 확정 범위, 관련 처리 방식)

## Requirement Ref
(REQ-FUNC-xxx, REQ-NF-xxx 목록 — Task List Requirement Ref 열과 동일)

## Screen / Route / Page Entry
Screen: ... / Route: ... / Page Entry: ...(Page Owner가 아니면 "해당 없음")

## Design Ref
(design-reference/UI_CONTRACT.md, design-reference/D-001/DESIGN.md, SCREEN_ROUTE_CONTRACT.json 중 관련 부분)

## Depends On
(Task ID 목록 또는 "-")

## Expected Files
(신규/수정 구분) + "이 목록 밖의 파일은 만들거나 수정하지 않는다."

## Functional AC
(Page Owner는 영역 순서 번호 목록 + 최소 콘텐츠 수 포함 — 규칙 22)

## Visual AC
(Page Owner는 Empty State/Placeholder 금지 고정 문구 포함 — 규칙 23)

## Security/Privacy AC
(해당 없으면 "해당 없음"과 이유)

## Test Cases
(구체적 시나리오 bullet — Functional/Visual AC에서 파생)

## Verify
(관련 Test Task ID 또는 수동 QA 방법)

## Definition of Done
(체크리스트, 최소 "Expected Files만 변경", "AC 충족", "Depends On 완료", "Verify 통과", "Forbidden 위반 없음")

## Forbidden
(공통 금지 목록 + 이 Task 특유의 금지 사항, "Expected Files 밖 수정 금지" 반드시 포함)
```

- 상세 파일 생성을 마치면 반드시 `python scripts/audit_tasks.py`를 실행하고 결과를 보고한다(규칙 20). 감사가 실패하면 실패 항목을 고친 뒤 다시 실행한다 — 실패한 채로, 또는 실패를 숨기거나 축소해서 작업을 종료하지 않는다.

### 5-1. `DB-*` Task 전용 규칙

`scripts/audit_tasks.py`가 테이블 개수(규칙 10)를 기계적으로 셀 수 있도록, `DB-SCHEMA-BASE`의 `## Context` 또는 `## Functional AC` 안에 다음 형식의 줄을 정확히 1개 포함한다.

```
Tables: `profiles`, `mate_posts`, `mate_applications`, `blocks`, `reports`, `app_settings`
```

- 백틱으로 감싼 테이블명만 개수를 센다.
- `destination`, `country_safety`, `representative_profile`, `region`, `media_asset` 등 정적 데이터 도메인에 해당하는 이름을 여기에 포함하지 않는다(규칙 11).

## 6. 감사 규칙(audit-tasks / scripts/audit_tasks.py)

`scripts/audit_tasks.py`는 `TASKS/00_TASK_LIST.md` + `TASKS/TASK-*.md`를 `app/docs/PROJECT_SCOPE.md`와 `design-reference/SCREEN_ROUTE_CONTRACT.json`을 정본 삼아 검사 1~18번(§2 규칙 표의 audit_tasks.py 대응 항목)을 자동 점검한다. 상세 내용은 스크립트 상단 docstring에 있다. 성공 시 `AUDIT_PASS`와 검사 개수를, 실패 시 `AUDIT_FAIL`과 실패 항목을 표준출력에 낸다. Command는 이 종료 코드와 출력을 **그대로** 신뢰하고 전달한다 — 일부만 골라 보고하거나 실패를 "경미함"으로 재해석하지 않는다.

## 7. 금지 사항(모든 Command 공통)

- `app/docs/PROJECT_SCOPE.md` §5 "일반 제외 기능"에 나열된 것(전체 콘텐츠 CMS, 미디어 업로드 워크플로, 범용 감사 로그, 자동 백업·장애 알림·부하 테스트, 외부 이메일 사업자 연동, EC2·AWS 인프라, 무인 자동 Merge Runner)에 대응하는 Task를 만들지 않는다.
- `design-reference/UI_CONTRACT.md`의 "공통 금지 기능"(Airbnb 상표 요소, 구매·예약·결제 UI, Proprietary 폰트, 정의되지 않은 색상, 별점·좋아요·실시간 가격, 광고, Placeholder 문구·빈 Card)을 구현하는 Task를 만들지 않는다.
- 이 세 Command(`/gen-tasklist`, `/gen-task-details`, `/audit-tasks`) 중 어느 것도 `app/src/app/**`, `app/src/components/**`, `app/src/lib/**` 같은 실제 소스 코드를 만들거나 고치지 않는다 — Task 정의 문서(`TASKS/**`)만 다룬다.
- 없는 사실을 있다고 기록하지 않는다 — 코드가 없는 시점에 Task를 "구현 완료"로 표시하지 않는다.
