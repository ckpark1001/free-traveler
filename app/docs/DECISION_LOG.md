# Free Traveler — Decision Log

- **문서 목적:** 프로젝트 진행 중 확정된 핵심 결정을 한곳에 모아, 왜 그렇게 정했는지와 어떤 문서·Task에 반영되어 있는지를 추적한다. 결정을 바꾸려면 새 항목을 추가하고 기존 항목은 `Status: Superseded by DEC-0XX`로 표시한다 — 지우지 않는다.
- **적용 범위:** `traveler` 저장소 전체(설계·범위·기술 스택·운영 방식).

## 요약

| ID | 결정 | Status |
|---|---|---|
| DEC-001 | 실제 개발 루트는 `traveler/app` | Accepted |
| DEC-002 | 디자인 Screen은 핵심 4개·보조 1개 | Accepted |
| DEC-003 | `/travel-tools`에 항공·숙소·동행 작성을 통합 | Accepted |
| DEC-004 | 여행지·안전·대표는 정적 TypeScript Data | Accepted |
| DEC-005 | Supabase는 Auth와 동행 기능 중심 | Accepted |
| DEC-006 | DB는 6개 Table로 제한 | Superseded by DEC-015(테이블명만) |
| DEC-007 | 항공·숙소 입력은 Browser Memory에만 유지 | Accepted |
| DEC-008 | Airbnb DESIGN.md는 vendor 참고본, D-001이 실제 정본 | Accepted |
| DEC-009 | Playwright는 Chromium Smoke만 필수 | Accepted |
| DEC-010 | 사용자의 개발 실행 단위는 Wave | Accepted |
| DEC-011 | Single Agent가 Wave 내부 Task를 순차 수행 | Accepted |
| DEC-012 | PR·Merge는 사용자가 수동 수행 | Accepted |
| DEC-013 | EC2·AWS는 사용하지 않음 | Accepted |
| DEC-014 | 제외 기능은 EXCLUDED로 관리 | Accepted |
| DEC-015 | DB 6개 Table명을 `profiles`/`mate_posts`/`mate_applications`/`blocks`/`reports`/`app_settings`로 확정 | Accepted |

---

## DEC-001 — 실제 개발 루트는 `traveler/app`

- **결정:** 실제 Next.js 프로젝트(`package.json`, `src/app`, `node_modules`)는 저장소 루트가 아니라 `app/` 아래에 있다. 이후 어떤 지시에서 "docs/X"라고 하면 별도 언급이 없는 한 `app/docs/X`를 가리키고, "src/app/X"는 `app/src/app/X`를 가리킨다. `design-reference/`와 `TASKS/`는 예외로 저장소 루트에 둔다.
- **배경:** 저장소 루트의 `docs/`에는 이 프로젝트 초기의 다른 계보 문서(`00_PRD_Travel_v1.md`, `05_SRS_Travel_v1.md`, `DESIGN-airbnb.md`, `STITCH_VALIDATION_REPORT.md`)가 남아 있고, 실제로 계속 갱신되는 스펙 체계(`01_PRD.md` ~ `06_SRS_UIUX_REVISED.md`, `PROJECT_SCOPE.md`, `UIUX_TRACEABILITY.md`, `ARCHITECTURE.md`)는 전부 `app/docs/`에 있다. 두 경로가 같은 이름의 저장소 안에 공존해 혼동 소지가 있어 명확히 고정한다.
- **근거 문서:** `app/package.json`, `app/docs/PROJECT_SCOPE.md`
- **영향:** `scripts/validate_inputs.py`, `scripts/audit_tasks.py`는 모두 `ROOT/app/docs/...`, `ROOT/app/src/app/...` 경로를 기준으로 동작한다. 새 문서를 "docs/"에 만들라는 지시를 받으면 `app/docs/`에 만든다.

## DEC-002 — 디자인 Screen은 핵심 4개·보조 1개

- **결정:** SCR-001(홈)·SCR-002(대표소개)·SCR-003(여행준비)·SCR-004(동행찾기)를 핵심 Screen으로, SCR-005(계정)를 보조 Screen으로 확정한다.
- **배경:** `PROJECT_SCOPE.md` §3이 원래 구 라우트 체계(`/destinations`, `/flights`, `/hotels`, `/my`, `/admin`)로 "핵심 4개·보조 1개"를 정의했다. `03_UI_COVERAGE_ANALYSIS.md`/`04_UIUX_PLAN.md`가 5개 Screen(신 라우트 체계)으로 통합한 뒤에도 이 4:1 분류의 취지(대표소개=핵심 가치 제안, 계정=보조 유틸리티)는 그대로 유지하기로 재확인했다.
- **근거 문서:** `design-reference/UI_CONTRACT.md` §0, `design-reference/SCREEN_ROUTE_CONTRACT.json`(`classification` 필드)
- **영향:** `scripts/validate_inputs.py`가 core 4개/auxiliary 1개 분포를 하드 검증한다. Screen을 추가·재분류하려면 `SCREEN_ROUTE_CONTRACT.json`과 이 항목을 함께 갱신해야 한다.

## DEC-003 — `/travel-tools`에 항공·숙소·동행 작성을 통합

- **결정:** 기존에 개별 라우트로 상정됐던 항공(`/flights`), 숙소(`/hotels`), 동행 작성(`/mates/new`)을 하나의 Screen(SCR-003, `/travel-tools`) 안의 3개 탭으로 통합한다.
- **배경:** 세 기능 모두 "여행 조건을 정리하고 다음 행동(외부 이동 또는 동행 게시)으로 넘어간다"는 동일한 사용자 여정이며, 별도 페이지로 나누면 전역 내비게이션과 컨텍스트 전환 비용이 커진다.
- **근거 문서:** `app/docs/05_UIUX_APPROVED.md` §2(Route 통합표), `design-reference/UI_CONTRACT.md`(SCR-003)
- **영향:** `PAGE-SCR003` Task가 `CMP-SCR003-FLIGHT-FORM`·`CMP-SCR003-HOTEL-FORM`·`CMP-SCR003-MATE-WRITE` 3개 Component Task에 의존해야 감사(`audit_tasks.py` #9)를 통과한다. `E2E-TRAVEL-TOOLS`가 이 통합 흐름을 검증한다.

## DEC-004 — 여행지·안전·대표는 정적 TypeScript Data

- **결정:** `DESTINATION`, `COUNTRY_SAFETY`, `REPRESENTATIVE_PROFILE` 도메인은 Supabase 테이블이 아니라 `src/data`의 정적 TypeScript 모듈로 구현한다.
- **배경:** 콘텐츠 규모(국내 10곳, 해외 15개국 30도시, 안전정보 15개국)가 MVP 범위에서 정적 파일로 충분히 관리 가능하고, 이를 통해 콘텐츠 CMS·게시 워크플로·미디어 업로드 파이프라인을 통째로 만들지 않아도 된다(DEC-014와 연결).
- **근거 문서:** `app/docs/PROJECT_SCOPE.md` §4·§8, `app/docs/ARCHITECTURE.md` §6
- **영향:** `DB-SCHEMA-BASE`가 이 세 도메인의 테이블을 만들지 않는다(DEC-006의 6개 한도에도 직접 영향). 대신 `DATA-DESTINATIONS`·`DATA-SAFETY`·`DATA-REPRESENTATIVE` Task로 구현한다.

## DEC-005 — Supabase는 Auth와 동행 기능 중심

- **결정:** Supabase는 (1) 이메일 인증·로그인 등 Auth, (2) 동행(Mate) 기능의 쓰기 데이터, 이 두 목적에만 사용한다. Storage도 사용하지 않는다.
- **배경:** DEC-004로 콘텐츠 도메인이 빠지면서, 실제로 서버 상태와 권한 검증(RLS)이 필요한 영역은 회원·동행 관련뿐이다.
- **근거 문서:** `app/docs/PROJECT_SCOPE.md` §8, `app/docs/ARCHITECTURE.md` §7
- **영향:** 이미지 정책이 URL+alt로 단순화되고(별도 REQ), Storage 관련 Task가 생성되지 않는다.

## DEC-006 — DB는 6개 Table로 제한

- **Status: Superseded by [[DEC-015]]** — 테이블을 6개로 제한한다는 결정 자체는 그대로 유효하다. 아래 원문에 적힌 6개 테이블의 **이름**만 DEC-015에서 교체되었다. 원문은 당시 결정을 그대로 보존하기 위해 수정하지 않는다.
- **결정:** Supabase Postgres 테이블은 `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_link_setting` 정확히 6개로 제한한다.
- **배경:** DEC-004·DEC-005로 실제 쓰기가 필요한 도메인만 남기면 6개로 충분하며, 테이블 수를 고정해두면 범위가 은근히 넓어지는 것(scope creep)을 막을 수 있다.
- **근거 문서:** `TASKS/TASK-DB-SCHEMA-BASE.md`, `scripts/audit_tasks.py`(검사 #12, 기준 6개·허용 한도 8개)
- **영향:** 7번째 테이블이 필요해 보이는 요구가 생기면, 먼저 기존 6개 테이블의 컬럼 확장으로 해결 가능한지 검토하고, 정말 새 테이블이 필요하면 이 항목을 개정하고 근거를 남긴 뒤에만 추가한다.

## DEC-007 — 항공·숙소 입력은 Browser Memory에만 유지

- **결정:** 항공·숙소 조건 입력값(국가·지역·날짜)은 해당 Client Component의 React state로만 존재하며, 서버 API·DB·외부 URL 쿼리·로그·`localStorage`/`sessionStorage`/쿠키 어디에도 전달·저장하지 않는다.
- **배경:** 이 서비스는 예약을 대행하지 않는 "조건 정리 후 외부 이동" 서비스이며, 입력값을 서버에 남기면 사용자에게 예약/검색 서비스로 오인될 위험과 불필요한 개인정보 보관 위험이 생긴다.
- **근거 문서:** SRS `CON-01`/`CON-02`, `app/docs/ARCHITECTURE.md` §4·§5
- **영향:** `CMP-SCR003-FLIGHT-FORM`/`HOTEL-FORM` Task의 Security/Privacy AC와 Forbidden 절에 이 제약이 명시되어 있고, `E2E-TRAVEL-TOOLS`가 새 탭 URL에 쿼리가 없는지 검증한다.

## DEC-008 — Airbnb DESIGN.md는 vendor 참고본, D-001이 실제 정본

- **결정:** `design-reference/vendor/airbnb/DESIGN.md`(및 `app/design-reference/vendor/airbnb/DESIGN-airbnb.md`)는 레이아웃 문법(포토 퍼스트 카드, 섹션 리듬 등)만 참고하는 벤더 분석 자료다. 색상·폰트·상표·컴포넌트명을 그대로 쓰지 않으며, 실제 디자인 정본은 `design-reference/D-001/DESIGN.md`다.
- **배경:** Airbnb 참고본을 그대로 베끼면 상표·브랜드 요소(Rausch 컬러, Cereal 폰트, "Guest favorite" 배지 등)가 섞여 들어갈 위험이 있어, 벤더 자료와 프로젝트 정본을 문서 단계에서부터 명확히 분리했다.
- **근거 문서:** `design-reference/D-001/DESIGN.md`(서두), `design-reference/UI_CONTRACT.md`(상단 표기)
- **영향:** 모든 Task 상세 파일의 Forbidden 절에 "Airbnb 상표 요소 금지"가 반복 명시되고, 정의되지 않은 임의 색상 추가도 금지된다.

## DEC-009 — Playwright는 Chromium Smoke만 필수

- **결정:** E2E 테스트는 Playwright의 Chromium 프로젝트만 사용하고, 5~7개 핵심 흐름을 `E2E-PUBLIC-SMOKE`·`E2E-TRAVEL-TOOLS`·`E2E-MATE-AUTH` 2~3개 Task로 묶는다. Firefox/WebKit/Safari 프로젝트나 별도의 시각 회귀·부하 테스트 도구는 도입하지 않는다.
- **배경:** MVP 단계에서 크로스 브라우저 매트릭스를 넓히는 것보다 핵심 흐름의 회귀를 빠르게 잡는 것이 우선이며, CI 실행 시간과 유지보수 비용도 줄어든다.
- **근거 문서:** `TASKS/TASK-E2E-PUBLIC-SMOKE.md` 등, `scripts/audit_tasks.py`(검사 #15), `app/docs/ARCHITECTURE.md` §12
- **영향:** 새 E2E 시나리오가 필요해도 새 브라우저 프로젝트를 추가하지 않고 기존 3개 Task 중 하나에 시나리오를 추가하는 방식으로 확장한다.

## DEC-010 — 사용자의 개발 실행 단위는 Wave

- **결정:** 실제 구현 착수는 `TASKS/TASK_MANIFEST.csv`의 Task를 하나씩 개별 지시하는 대신, 의존성 순서를 반영해 여러 Task를 묶은 **Wave** 단위로 사용자가 실행을 지시한다.
- **배경:** Task 63개를 하나씩 개별 요청하면 조율 비용이 크고, 반대로 전부 한 번에 지시하면 검증·롤백 단위가 너무 커진다. Depends On 그래프(위상 순서)가 이미 "먼저 끝나야 하는 것 → 나중에 조립하는 것" 순서를 담고 있으므로, 이를 실행 가능한 배치로 나눈 것이 Wave다.
- **근거 문서:** `TASKS/TASK_MANIFEST.csv`(Depends On 열)
- **영향:** Wave의 구체적 구성(어떤 Task가 몇 번째 Wave에 속하는지)은 이 로그가 아니라 별도의 실행 계획에서 정의한다. 이 항목은 "실행 단위가 Task 개별이 아니라 Wave"라는 원칙만 확정한다.

## DEC-011 — Single Agent가 Wave 내부 Task를 순차 수행

- **결정:** 하나의 Wave 안에서는 여러 Agent를 동시에 투입하지 않고, 단일 Agent가 Depends On 순서에 따라 Task를 하나씩 순차적으로 수행한다.
- **배경:** 병렬 Agent를 쓰면 같은 파일(예: 공용 레이아웃, 공용 유틸)을 서로 다른 Agent가 동시에 건드려 충돌할 위험이 있고, 각 Task의 "Expected Files 밖 수정 금지" 원칙과도 병렬 실행은 상성이 나쁘다. 순차 실행은 느리지만 예측 가능하고 검증하기 쉽다.
- **근거 문서:** 각 `TASKS/TASK-*.md`의 Forbidden 절("Expected Files에 명시되지 않은 파일을 생성·수정하지 않는다")
- **영향:** Wave 내부에서 여러 서브에이전트를 동시에 배정하는 자동화를 만들지 않는다. Task 순서는 Depends On 위상 정렬을 그대로 따른다.

## DEC-012 — PR·Merge는 사용자가 수동 수행

- **결정:** Agent가 코드를 작성하고 커밋까지는 할 수 있어도, Pull Request 생성 여부와 Merge 실행은 항상 사용자가 직접 한다.
- **배경:** 자동 Merge를 허용하면 리뷰 없이 잘못된 변경이 `main`에 들어갈 위험이 있고, 이는 DEC-013(무인 인프라 자동화 배제) 및 "무인 자동 Merge Runner"를 제외 기능으로 못박은 결정과 같은 원칙을 따른다.
- **근거 문서:** `app/docs/PROJECT_SCOPE.md` §5(일반 제외 기능 — 무인 자동 Merge Runner), 각 `TASKS/TASK-*.md`의 Forbidden 절("Branch/PR/Issue 생성 금지")
- **영향:** GitHub Actions 등 어떤 자동화 파이프라인에도 auto-merge 또는 자동 PR 병합 기능을 넣지 않는다(DEC-013·DEC-009와 함께 CI 설계 시 적용).

## DEC-013 — EC2·AWS는 사용하지 않음

- **결정:** 배포·인프라는 Vercel(애플리케이션)과 Supabase(DB/Auth)로 한정하고, AWS EC2 등 별도 클라우드 인프라를 구성하지 않는다.
- **배경:** MVP 규모에서 별도 클라우드 계정·VM 운영은 관리 비용 대비 이득이 없고, 월 인프라 비용 목표(₩100,000 이하)와도 맞지 않는다.
- **근거 문서:** `app/docs/PROJECT_SCOPE.md` §5, `app/docs/ARCHITECTURE.md` §14, `scripts/audit_tasks.py`(검사 #16)
- **영향:** 모든 Task/문서에서 EC2·AWS 키워드가 발견되면 감사가 실패하도록 강제되어 있다.

## DEC-014 — 제외 기능은 EXCLUDED로 관리

- **결정:** 구현하지 않기로 한 요구사항은 목록에서 삭제하지 않고 `EXCLUDED` 상태로 남기며, 반드시 제외 근거와 후속 방향(재검토 조건)을 함께 기록한다.
- **배경:** 요구사항을 조용히 지우면 나중에 "이게 원래 있었는지" 추적할 수 없고, 왜 뺐는지도 사라진다. 근거와 후속 방향을 남기면 범위가 커질 때 무엇을 먼저 재검토해야 하는지 바로 알 수 있다.
- **근거 문서:** `app/docs/PROJECT_SCOPE.md`(REQ별 IMPLEMENT/EXCLUDED), `app/docs/UIUX_TRACEABILITY.md`, `TASKS/00_TASK_LIST.md` §2(NON_IMPLEMENTATION), `scripts/audit_tasks.py`(검사 #17·#18)
- **영향:** 현재 REQ-FUNC-001~080·REQ-NF-001~034 중 24개가 EXCLUDED로 표에 남아 있다(예: 콘텐츠 CMS, 미디어 라이선스 워크플로, 범용 감사 로그, 자동 성능/장애 알림). 이 24개에 대해서는 상세 구현 Task 파일을 만들지 않는다.

## DEC-015 — DB 6개 Table명을 `profiles`/`mate_posts`/`mate_applications`/`blocks`/`reports`/`app_settings`로 확정

- **결정:** DEC-006에서 정한 6개 테이블의 실제 이름을 `user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_link_setting`(초안 표기)에서 `profiles`, `mate_posts`, `mate_applications`, `blocks`, `reports`, `app_settings`(Supabase/Postgres 관례상 복수형 스네이크케이스)로 확정한다. 테이블 개수·용도(DEC-006)는 바뀌지 않으며 이름만 교체한다.
- **배경:** 초안 단계에서 쓰인 단수형 명명(`user_profile` 등)이 이후 `TASKS/TASK-DB-SCHEMA-BASE.md`·`CLAUDE.md`·`scripts/audit_tasks.py`·`scripts/validate_harness.py` 등 실제 구현·감사 산출물 전반에서 복수형 명명(`profiles` 등)으로 이미 통일되어 쓰이고 있었다. 이 결정 자체가 문서화되지 않아 `DEC-006` 본문과 나머지 저장소 사이에 이름 불일치가 있었고, 이번에 `docs/DECISION_LOG.md` 점검 중 발견해 정식 항목으로 기록한다.
- **근거 문서:** `TASKS/TASK-DB-SCHEMA-BASE.md`(`Tables: ...` 선언), `CLAUDE.md` 규칙 13, `.claude/skills/traveler-project-pipeline/SKILL.md` §5-1·규칙 10, `scripts/validate_harness.py`(`EXPECTED_DB_TABLES`), `scripts/audit_tasks.py`(검사 #12)
- **영향:** `profiles`/`mate_posts`/`mate_applications`/`blocks`/`reports`/`app_settings`가 유일한 정본 이름이다. **미해결 항목:** `.claude/commands/release-check.md` §5(Supabase 6개 Table 확인 절차)가 아직 옛 이름(`user_profile`, `mate_post`, `mate_application`, `user_block`, `report`, `outbound_link_setting`)을 검사 기준으로 쓰고 있어, 실제 마이그레이션이 생기면 잘못된 이름을 대조해 오탐(false fail)을 낼 수 있다 — 별도로 `release-check.md`를 이 항목의 이름으로 갱신해야 한다(이번 작업 범위 밖이라 이 로그에만 기록하고 코드는 고치지 않았다).
