# Traveler Task List

- **Document:** TASKS/00_TASK_LIST.md
- **근거 문서:** `app/docs/06_SRS_UIUX_REVISED.md`, `app/docs/PROJECT_SCOPE.md`, `app/docs/UIUX_TRACEABILITY.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, 실제 `app/src/app` 파일 트리
- **선행 검사:** `python3 scripts/validate_inputs.py` 실행 — PASS (HARNESS_SCHEMA=traveler-screen-route-v1, Screen 5개, Requirement 114개 확인됨)
- **상태 고지:** 본 문서는 Task '정의'만 다룬다. 구현 코드는 작성되지 않았으며 (`app/src/app`에는 create-next-app 기본 스타터만 존재), 모든 Task는 착수 전이다. Implementation Status의 `IMPLEMENT`는 구현 대상 확정을 의미할 뿐 완료를 의미하지 않는다.

## 0. 요약

- **Task 총 개수:** 63
- **Requirement 총 개수:** 114 (REQ-FUNC 80 + REQ-NF 34) — `app/docs/UIUX_TRACEABILITY.md`와 100% 일치, 누락 없음
- **IMPLEMENT:** 90개 — 아래 Task List에 전부 연결됨
- **EXCLUDED:** 24개 — §2 NON_IMPLEMENTATION 표에 근거·후속 방향 기록, 상세 구현 Task 없음

### Category별 Task 수

| Category | 개수 |
|---|---:|
| PAGE_OWNER | 5 |
| COMPONENT | 25 |
| DATA | 3 |
| DB | 4 |
| API | 5 |
| SHARED | 6 |
| UNIT_TEST | 3 |
| INTEGRATION_TEST | 1 |
| E2E_TEST | 3 |
| CI | 1 |
| MANUAL_CHECK | 3 |
| RELEASE_CHECK | 4 |
| **합계** | **63** |

> Task 개수는 참고 정보이며 완료 조건으로 사용하지 않는다.

## 1. Task List

열: Seq, Task ID, 제목, Category, Implementation Status, Requirement Ref, Screen, Route, Page Entry, Depends On, Expected Files, Functional AC, Visual AC, Security/Privacy AC, Verify, Priority

| Seq | Task ID | 제목 | Category | Implementation Status | Requirement Ref | Screen | Route | Page Entry | Depends On | Expected Files | Functional AC | Visual AC | Security/Privacy AC | Verify | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `SHARED-DESIGN-TOKENS` | Tailwind 테마를 D-001 디자인 토큰으로 교체 | SHARED | IMPLEMENT | N/A(기반 인프라 — design-reference/D-001/DESIGN.md 근거) | - | - | - | - | src/app/globals.css(수정, @theme 토큰); src/lib/design-tokens.ts(신규) | D-001 DESIGN.md의 Color/Typography/Spacing/Radius/Shadow 토큰을 Tailwind @theme 및 TS 상수로 이식한다; create-next-app 기본 Geist 폰트·기본 팔레트를 제거한다. | Airbnb 상표 색상(#ff385c 등)·Proprietary 폰트 파일을 포함하지 않는다; 토큰 외 임의 색상 추가 금지. | 해당 없음(정적 스타일 자산). | 코드 리뷰(토큰 값 대조) | M |
| 2 | `DATA-DESTINATIONS` | 국내·해외 여행지 정적 데이터 스키마·시드 | DATA | IMPLEMENT | REQ-FUNC-004, REQ-FUNC-008, REQ-FUNC-063, REQ-NF-026 | - | - | - | - | src/data/destinations.ts(신규); src/data/types/destination.ts(신규) | PRD 3-4 필수 11항목(소개 300자+, 명소 5+, 추천/비추천 시기, 1일·3일 일정, 예산, 교통, 음식 3+, 에티켓 3+, 안전연결, 출처, 수정일)을 TypeScript 타입으로 강제한다; DB 테이블이 아닌 src/data 정적 파일로 관리한다(Supabase 미사용). | 해당 없음(비-UI Task, 데이터 정의). | 개인정보 없음. 이미지는 URL+alt만 저장(출처·작가·라이선스 메타데이터는 REQ-FUNC-007 EXCLUDED). | 수동 콘텐츠 체크리스트(국내 10+, 해외 15개국 30도시+) | M |
| 3 | `DATA-SAFETY` | 국가별 안전정보 정적 데이터 스키마·시드 | DATA | IMPLEMENT | REQ-FUNC-046, REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-052, REQ-FUNC-053, REQ-NF-027 | - | - | - | - | src/data/country-safety.ts(신규); src/data/types/country-safety.ts(신규) | 8개 필수 카테고리(치안·사기·법규·교통·재난·보건·문화·긴급연락처), scope_type(COUNTRY/REGION), source_name/source_url/verified_at를 타입으로 강제한다; src/data 정적 파일로 관리(DB 미사용). | 해당 없음(비-UI Task, 데이터 정의). | 개인정보 없음(공개 공식 정보). | 수동 데이터 커버리지 확인(해외 15개국 100%) | M |
| 4 | `DATA-REPRESENTATIVE` | 대표(free_traveler) 프로필 정적 데이터 | DATA | IMPLEMENT | REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060 | - | - | - | - | src/data/representative-profile.ts(신규) | display_name, `50+ Trips`/`30+ Countries` 라벨(CON-09 전역 고정), bio, philosophy, visited_countries(30개국 이상), timeline(6개 이상)을 단일 정적 소스로 정의한다. | 해당 없음(비-UI Task, 데이터 정의). | 개인정보 없음(공개 프로필). | 수동 QA(홈 요약 카드와 값 일치 확인) | M |
| 5 | `DB-SCHEMA-BASE` | Supabase 테이블 스키마 정의(최대 6개) | DB | IMPLEMENT | REQ-FUNC-028, REQ-FUNC-035 | - | - | - | - | supabase/migrations/0001_schema_base.sql(신규) | Tables: `profiles`, `mate_posts`, `mate_applications`, `blocks`, `reports`, `app_settings` — 정확히 6개, 초과 금지; 여행지·안전·대표 도메인 테이블은 만들지 않는다(정적 데이터로 대체, DATA-* Task). | 해당 없음(비-UI Task). | profiles은 정확한 생년월일을 저장하지 않고 is_adult(BOOLEAN)/adult_verified_at(TIMESTAMPTZ)만 저장한다(REQ-FUNC-028). | 코드 리뷰(스키마 확인) | M |
| 6 | `DB-RLS-BASE` | Row Level Security 정책 | DB | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | - | - | - | DB-SCHEMA-BASE | supabase/migrations/0002_rls_base.sql(신규) | 본인 글·요청, 요청 대상 작성자, Admin만 비공개 데이터(mate_applications.message, reports, blocks)를 열람하도록 정책을 정의한다; 차단 관계는 조회 단계에서 상호 제외한다. | 해당 없음(비-UI Task). | 권한별 부정 접근 시 403 또는 빈 결과를 반환하도록 정책을 강제한다. | TEST-RLS-BASIC | M |
| 7 | `DB-ACCESS` | 타입 세이프 Supabase 클라이언트·쿼리 헬퍼 | DB | IMPLEMENT | REQ-NF-014, REQ-NF-015 | - | - | - | DB-SCHEMA-BASE, DB-RLS-BASE | src/lib/supabase/server-client.ts(신규); src/lib/supabase/queries.ts(신규) | Server Component/Route Handler 전용 Supabase 클라이언트와 도메인별 쿼리 함수(mate_posts/mate_applications/blocks/reports/app_settings)를 제공한다. | 해당 없음(비-UI Task). | Server Action 기반 CSRF 방어·SameSite 세션 쿠키를 전제로 하고, 모든 입력을 서버 측에서 검증·이스케이프한다(저장 XSS 차단). | 코드 리뷰; 수동 XSS 케이스 테스트 | M |
| 8 | `DB-SEED-BASE` | 로컬/스테이징 시드 데이터 | DB | IMPLEMENT | N/A(개발·QA 지원 — E2E-MATE-AUTH, TEST-RLS-BASIC 선행 조건) | - | - | - | DB-SCHEMA-BASE | supabase/seed.sql(신규) | 테스트용 profiles 2~3명, mate_posts 3건 이상, mate_applications/blocks/reports 샘플을 생성해 E2E·RLS 테스트가 재현 가능하게 한다. | 해당 없음(비-UI Task). | 실사용자 개인정보를 포함하지 않는다(테스트 전용 더미 데이터). | TEST-RLS-BASIC, E2E-MATE-AUTH 실행 성공 여부로 확인 | S |
| 9 | `API-MATES-CRUD` | 동행 모집글 CRUD API | API | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-030, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-033, REQ-FUNC-037, REQ-FUNC-038, REQ-NF-005, REQ-NF-015 | - | - | - | DB-ACCESS | src/app/api/mates/route.ts(신규); src/app/api/mates/[id]/route.ts(신규) | GET(목록·필터·차단 사용자 제외·종료일 경과 CLOSED 처리), POST(생성, 인증+성인확인 필요), PATCH/DELETE(작성자 전용 수정·마감·삭제)를 제공한다; 본문 전화번호·이메일·메신저ID 패턴 탐지 시 제출을 차단한다(연락처 정규식은 UNIT-CONTACT-DETECTION과 동일 모듈 공유). | 해당 없음(비-UI Task). | 응답 JSON에 이메일·전화번호를 포함하지 않는다(REQ-FUNC-033); 비회원 POST는 401 또는 로그인 리다이렉트. | UNIT-CONTACT-DETECTION; UNIT-MATE-STATE; E2E-MATE-AUTH | M |
| 10 | `API-APPLICATIONS` | 참가 요청 API | API | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-036, REQ-FUNC-043, REQ-NF-005 | - | - | - | DB-ACCESS, API-MATES-CRUD | src/app/api/mates/[id]/applications/route.ts(신규); src/app/api/applications/[id]/route.ts(신규) | POST(500자 이하 비공개 메시지, PENDING 저장, 동일 글 중복 PENDING/ACCEPTED 차단), PATCH(작성자만 ACCEPTED/REJECTED 전이, 비작성자 403)을 제공하고 상태 변경 시 인앱 알림(Toast) 트리거용 상태를 반환한다. | 해당 없음(비-UI Task). | RLS로 작성자·요청자 외 열람 차단(DB-RLS-BASE 의존). | UNIT-MATE-STATE; E2E-MATE-AUTH | M |
| 11 | `API-REPORTS-BLOCKS` | 신고·차단 API | API | IMPLEMENT | REQ-FUNC-039, REQ-FUNC-040, REQ-FUNC-041, REQ-FUNC-042, REQ-NF-005, REQ-NF-019 | - | - | - | DB-ACCESS | src/app/api/reports/route.ts(신규); src/app/api/blocks/route.ts(신규); src/app/api/blocks/[id]/route.ts(신규); src/app/api/admin/reports/route.ts(신규) | 신고 접수(사유코드+설명, 접수번호 즉시 반환), 차단·해제(상호 노출 제한), 관리자 신고 큐(OPEN/RESOLVED/DISMISSED 필터·상태 변경·게시물 숨김)를 제공한다. | 해당 없음(비-UI Task). | 신고자·피신고자 상세 정보는 Admin만 조회 가능(RLS); 응답 p95 3초 이내(REQ-NF-019). | E2E-MATE-AUTH | M |
| 12 | `API-ADMIN-OUTBOUND` | 관리자 외부 URL 설정 API | API | IMPLEMENT | REQ-FUNC-077 | - | - | - | DB-ACCESS | src/app/api/admin/settings/outbound/route.ts(신규) | Admin 역할만 PATCH 가능; FLIGHT_OUTBOUND_URL/HOTEL_OUTBOUND_URL을 HTTPS 허용목록 내 주소로만 저장하고 http/javascript/data 스킴은 거부한다. | 해당 없음(비-UI Task). | 비관리자 요청은 403; 저장 전 URL 스킴·허용목록 서버 측 검증. | 수동 QA(HTTPS 외 스킴 저장 거부 확인) | M |
| 13 | `API-AUTH-PROFILE` | Supabase Auth 연동·프로필 API | API | IMPLEMENT | REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-066 | - | - | - | DB-ACCESS | src/app/api/profile/route.ts(신규); src/app/auth/callback/route.ts(신규, 기술 Route) | 이메일 가입·인증·로그인·로그아웃·비밀번호 재설정(Supabase Auth), 성인 확인(정확한 생년월일 미저장, is_adult/adult_verified_at만 기록), 프로필(닉네임 필수·연령대 필수·성별 선택·여행스타일 필수·자기소개 선택) upsert를 제공한다. | 해당 없음(비-UI Task). | 인증되지 않은 이메일은 동행 쓰기 권한을 얻지 못한다. | E2E-MATE-AUTH | M |
| 14 | `SHARED-LAYOUT-NAV-FOOTER` | 전역 레이아웃·Header·Footer | SHARED | IMPLEMENT | REQ-FUNC-064, REQ-FUNC-065, REQ-FUNC-079, REQ-FUNC-080, REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-006, REQ-NF-023 | COMMON | 공통(모든 Route) | - | SHARED-DESIGN-TOKENS | src/app/layout.tsx(수정, 기존 스타터 레이아웃 제거); src/components/shared/header.tsx(신규); src/components/shared/footer.tsx(신규) | 5개 Screen 공통 Header(여행지/항공·호텔/동행/대표소개 내비 + 계정 진입점) + Footer(바로가기/정책/공식출처 고지)를 제공한다; 320px~데스크톱 반응형, 폼·탭·알림에 시맨틱 HTML/ARIA 적용. | D-001 토큰만 사용, Airbnb 상표 요소 금지; LCP 이미지 priority, lazy load 적용. | 해당 없음(레이아웃 셸, 민감정보 없음). | MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK | M |
| 15 | `SHARED-ERROR-NOTFOUND` | 404/500/외부연결실패 공통 상태 | SHARED | IMPLEMENT | REQ-FUNC-078 | COMMON | 공통(모든 Route) | - | SHARED-DESIGN-TOKENS, SHARED-LAYOUT-NAV-FOOTER | src/app/not-found.tsx(신규); src/app/error.tsx(신규) | 404·500·권한없음·외부연결실패 각 화면에 홈/이전/재시도 중 최소 1개 복구 행동을 제공한다. | 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 해당 없음. | 수동 QA | M |
| 16 | `SHARED-SEO-METADATA` | 페이지별 SEO 메타데이터 헬퍼 | SHARED | IMPLEMENT | REQ-FUNC-070, REQ-NF-030 | - | - | - | - | src/lib/seo.ts(신규, buildMetadata 헬퍼) | title/description/canonical/Open Graph를 라우트별로 생성하는 공용 헬퍼를 제공한다(각 Page Owner가 자신의 page_entry에서 호출). | 해당 없음(비-UI Task). | 해당 없음. | 코드 리뷰(메타 태그 확인) | M |
| 17 | `SHARED-FAVORITES-LOCALSTORAGE` | 여행지 즐겨찾기(localStorage) | SHARED | IMPLEMENT | REQ-FUNC-068 | - | - | - | - | src/lib/favorites.ts(신규) | localStorage에 즐겨찾기 id Set을 저장한다(서버 저장 없음); 중복 추가를 방지하는 add/remove/has/list API를 제공한다. | 해당 없음(비-UI Task, 유틸리티). | 브라우저 로컬 저장소만 사용, 서버 전송 없음. | 수동 QA(localStorage 확인) | S |
| 18 | `SHARED-OUTBOUND-LINK-UTIL` | 외부 이동 링크 유틸(noopener+허용목록) | SHARED | IMPLEMENT | REQ-FUNC-016, REQ-FUNC-018, REQ-FUNC-024, REQ-FUNC-026, REQ-FUNC-049, REQ-FUNC-077 | - | - | - | - | src/lib/outbound-link.ts(신규) | 새 탭 오픈 + noopener,noreferrer를 강제하고, HTTPS 허용목록 밖 URL은 이동을 차단하며 오류·재시도 상태를 반환한다; 목적지·날짜 등 어떤 사용자 입력값도 쿼리·본문·쿠키로 URL에 첨부하지 않는다. | 해당 없음(비-UI Task, 유틸리티). | opener 접근 불가(window.opener 차단); 허용목록 외 스킴(javascript:, data:) 실행 금지. | RELEASE-EXTERNAL-LINKS-CHECK | M |
| 19 | `CMP-SCR001-HERO-SEARCH` | 홈 Hero + 통합 검색 | COMPONENT | IMPLEMENT | REQ-FUNC-003, REQ-FUNC-067 | SCR-001 | / | - | DATA-DESTINATIONS, SHARED-DESIGN-TOKENS | src/components/home/hero-search.tsx(신규) | 완성 문장 헤드라인 + 여행지·국가·안전정보 통합 키워드 검색(한글 부분 일치) + `/travel-tools` 보조 CTA를 제공한다. | Hero 높이는 뷰포트 100%를 차지하지 않고 아래 Section 상단이 스크롤 없이 보인다. | 해당 없음(공개 검색). | E2E-PUBLIC-SMOKE | M |
| 20 | `CMP-SCR001-DESTINATION-GRID` | 국내·해외 여행지 Card Grid + 필터 | COMPONENT | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-005, REQ-FUNC-010, REQ-NF-004 | SCR-001 | / | - | DATA-DESTINATIONS, SHARED-DESIGN-TOKENS | src/components/home/destination-card-grid.tsx(신규); src/components/home/theme-chip-row.tsx(신규) | 국내 6장/해외 6장 카드 그리드, 국가·도시·계절·테마(칩 6개)·기간 AND 필터, 필터 상태 URL query 반영·복원; 결과 0건 시 조건 완화 안내+전체 초기화 버튼. | 별점·리뷰·가격 배지 없음; Empty State는 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 해당 없음(공개 콘텐츠). | E2E-PUBLIC-SMOKE | M |
| 21 | `CMP-SCR001-DESTINATION-DRAWER` | 여행지 상세 Drawer | COMPONENT | IMPLEMENT | REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-009, REQ-FUNC-069 | SCR-001 | / | - | DATA-DESTINATIONS, SHARED-FAVORITES-LOCALSTORAGE | src/components/home/destination-detail-drawer.tsx(신규) | PRD 3-4 필수 11항목 전체 표시; 해외 여행지는 안전정보 Drawer로 연결; 관련 여행지 최대 6개; URL 공유(Web Share API, 실패 시 복사 폴백). | 필수 필드 중 하나라도 없는 Card를 노출하지 않는다. | 해당 없음. | E2E-PUBLIC-SMOKE | M |
| 22 | `CMP-SCR001-SAFETY-GRID` | 국가별 주의사항 Card Grid | COMPONENT | IMPLEMENT | - | SCR-001 | / | - | DATA-SAFETY, SHARED-DESIGN-TOKENS | src/components/home/safety-card-grid.tsx(신규) | 국가 카드 6개(국가명+경보 단계 텍스트 라벨+최종 확인일)를 표시한다. | 경보 단계를 색상만으로 구분하지 않고 텍스트 라벨을 병기한다. | 해당 없음(공개 정보). | E2E-PUBLIC-SMOKE | M |
| 23 | `CMP-SCR001-SAFETY-DRAWER` | 안전정보 상세 Drawer | COMPONENT | IMPLEMENT | REQ-FUNC-047, REQ-FUNC-048, REQ-FUNC-049, REQ-FUNC-050, REQ-FUNC-051, REQ-FUNC-052, REQ-FUNC-053, REQ-FUNC-054, REQ-NF-028 | SCR-001 | / | - | DATA-SAFETY, SHARED-OUTBOUND-LINK-UTIL | src/components/home/safety-info-drawer.tsx(신규) | 8개 필수 카테고리, 출처·확인일, 외교부 원문 링크(새 탭), 7일 초과 stale 경고, 중대경보 상단 텍스트, 국가/지역 범위 구분, 긴급연락처, '공식 판단 대체 아님' 고지를 표시한다. | 중대 경보는 색상+텍스트 라벨을 함께 표시한다. | 해당 없음(공개 정보). | E2E-PUBLIC-SMOKE | M |
| 24 | `CMP-SCR001-MATE-TEASER` | 최근 동행글 미리보기 3개 | COMPONENT | IMPLEMENT | N/A(PAGE-SCR001 콘텐츠 계약 — 최근 동행글 3개 또는 Empty State) | SCR-001 | / | - | API-MATES-CRUD | src/components/home/mate-teaser-grid.tsx(신규) | 공개 모집중 글 최신 3개(국가·기간·모집상태만, 연락처 비노출)를 요약 표시하고 `/mates` 및 `/travel-tools` 동행 작성 CTA를 제공한다. | 0건이면 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 이메일·전화번호 등 연락처를 노출하지 않는다. | E2E-PUBLIC-SMOKE | S |
| 25 | `CMP-SCR001-ABOUT-SUMMARY` | free_traveler 소개 요약 배너 | COMPONENT | IMPLEMENT | REQ-FUNC-057 | SCR-001 | / | - | DATA-REPRESENTATIVE | src/components/home/about-summary-banner.tsx(신규) | 한 줄 소개 + `50+ Trips`/`30+ Countries` 수치 + `/about` CTA를 좌우 분할로 표시한다. | 대표 페이지와 수치가 100% 일치한다(단일 데이터 소스). | 해당 없음(공개 프로필). | E2E-PUBLIC-SMOKE | M |
| 26 | `CMP-SCR002-HERO-STATS` | About Hero + 여행 지표 | COMPONENT | IMPLEMENT | REQ-FUNC-057 | SCR-002 | /about | - | DATA-REPRESENTATIVE | src/components/about/hero-stats.tsx(신규) | 대표 이미지+한 문장 소개, `50+ Trips`/`30+ Countries`/전문영역 배지 Stat Row를 표시한다. | 이미지 alt는 실제 장소를 설명하는 문장이어야 한다. | 식별 가능한 인물이 특정 서비스의 보증인으로 오인될 수 있는 연출을 사용하지 않는다. | E2E-PUBLIC-SMOKE | M |
| 27 | `CMP-SCR002-PHILOSOPHY` | 소개·철학·편집 원칙 | COMPONENT | IMPLEMENT | REQ-FUNC-058 | SCR-002 | /about | - | DATA-REPRESENTATIVE | src/components/about/philosophy-split.tsx(신규) | PRD 6-2 확정 소개문·여행 철학·콘텐츠 편집 원칙을 줄임 없이 표시한다. | 좌측 소제목 Nav + 우측 본문 좌우 분할(Desktop), 세로 스택(Mobile). | 해당 없음. | E2E-PUBLIC-SMOKE | M |
| 28 | `CMP-SCR002-TIMELINE` | 여행 Timeline | COMPONENT | IMPLEMENT | REQ-FUNC-060 | SCR-002 | /about | - | DATA-REPRESENTATIVE | src/components/about/travel-timeline.tsx(신규) | 연도·장소·요약을 포함한 타임라인 항목 6개 이상을 세로로 표시한다. | 6개 미만이면 배포하지 않는다(완성형 콘텐츠 원칙). | 해당 없음. | E2E-PUBLIC-SMOKE | M |
| 29 | `CMP-SCR002-COUNTRIES-GALLERY` | 방문 국가 30개 + 사진 Gallery 8장 | COMPONENT | IMPLEMENT | REQ-FUNC-059 | SCR-002 | /about | - | DATA-REPRESENTATIVE | src/components/about/countries-gallery.tsx(신규) | 권역별(아시아/유럽/북미/오세아니아) 그룹으로 30개국 이상 Chip을 표시하고, 서로 다른 장소의 사진 8장 이상 Gallery를 제공한다; Chip 클릭 시 관련 여행지가 있으면 SCR-001 Drawer로 연결. | Gallery는 Desktop 균등 그리드, Mobile 2열로 축소. | 이미지 alt는 실제 장소 설명 문장. | E2E-PUBLIC-SMOKE | M |
| 30 | `CMP-SCR002-RECOMMENDED-CTA` | 추천 여행지 4개 + CTA Banner | COMPONENT | IMPLEMENT | REQ-FUNC-062, REQ-FUNC-063 | SCR-002 | /about | - | DATA-DESTINATIONS, DATA-REPRESENTATIVE | src/components/about/recommended-destination-grid.tsx(신규) | 추천 여행지 카드 4개(SCR-001 Drawer로 연결, 비공개 여행지 자동 제외) + 문의/SNS 링크(빈 값 미노출, 허용 프로토콜만) + `/travel-tools`·`/mates` CTA Banner. | 빈 카드 노출 금지. | 허용되지 않은 프로토콜(javascript: 등) 링크를 렌더링하지 않는다. | E2E-PUBLIC-SMOKE | S |
| 31 | `CMP-SCR003-SHELL` | 여행 준비 Intro + Tab 뼈대 + Tip | COMPONENT | IMPLEMENT | REQ-FUNC-054 | SCR-003 | /travel-tools | - | SHARED-OUTBOUND-LINK-UTIL, SHARED-DESIGN-TOKENS | src/components/travel-tools/intro-tabs-shell.tsx(신규); src/components/travel-tools/tip-cards.tsx(신규) | 이용 순서 3단계 Intro, 항공/숙소/동행 구하기 3탭 네비게이션(탭별 값 독립 유지), 찾기 Tip 3개, '공식 판단 대체 아님' 고지를 제공한다. | 3탭은 항상 함께 노출한다(한 탭만 보이는 변형 금지). | 해당 없음. | E2E-TRAVEL-TOOLS | M |
| 32 | `CMP-SCR003-FLIGHT-FORM` | 항공 조건 입력·요약·외부 이동 | COMPONENT | IMPLEMENT | REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-NF-017 | SCR-003 | /travel-tools | - | SHARED-OUTBOUND-LINK-UTIL | src/components/travel-tools/flight-form.tsx(신규) | 국가·지역·출발일·귀국일 4필드(국가 변경 시 지역 초기화), 과거일·역전일 차단, 유효 입력 후 요약+비전달 고지, '항공편 보러 가기' 새 탭 이동. 국가·지역·날짜를 서버 DB·서버 로그·분석 이벤트·외부 URL 쿼리에 저장·전달하지 않는다(CON-01/02). | 비전달 고지 배너는 폼과 요약 단계에 상시 노출. | 원시 입력값이 네트워크 요청·DB·로그에 0건 포함되어야 한다. | UNIT-TRAVEL-DATES; E2E-TRAVEL-TOOLS | M |
| 33 | `CMP-SCR003-HOTEL-FORM` | 숙소 조건 입력·요약·외부 이동 | COMPONENT | IMPLEMENT | REQ-FUNC-019, REQ-FUNC-020, REQ-FUNC-021, REQ-FUNC-022, REQ-FUNC-023, REQ-FUNC-024, REQ-FUNC-025, REQ-FUNC-026, REQ-NF-017 | SCR-003 | /travel-tools | - | SHARED-OUTBOUND-LINK-UTIL | src/components/travel-tools/hotel-form.tsx(신규) | 국가·지역·체크인·체크아웃 4필드, 과거 체크인·체크아웃≤체크인 차단, 요약+비전달 고지, '호텔 보러 가기' 새 탭 이동. 입력값을 서버 DB·로그·URL에 저장·전달하지 않는다. | 비전달 고지 배너는 폼과 요약 단계에 상시 노출. | 원시 입력값이 네트워크 요청·DB·로그에 0건 포함되어야 한다. | UNIT-TRAVEL-DATES; E2E-TRAVEL-TOOLS | M |
| 34 | `CMP-SCR003-MATE-WRITE` | 동행 모집글 작성(연락처 탐지·안전수칙 동의) | COMPONENT | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-080 | SCR-003 | /travel-tools | - | API-MATES-CRUD, CMP-SCR005-AUTH | src/components/travel-tools/mate-write-form.tsx(신규); src/components/travel-tools/auth-required-notice.tsx(신규) | 제목·국가·지역·시작일·종료일·모집인원·선호조건·여행스타일·설명·안전수칙 동의 필드; 전화번호·이메일·메신저ID 패턴 탐지 시 제출 차단+수정 안내; 비로그인/성인 미확인 시 `/account` 로그인 유도. | 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 연락처 탐지 실패(오탐 포함)를 사용자에게 명확히 안내하고 제출을 차단한다. | UNIT-CONTACT-DETECTION; E2E-TRAVEL-TOOLS | M |
| 35 | `CMP-SCR004-FILTER-LIST` | 동행 Intro + Filter + 목록 | COMPONENT | IMPLEMENT | REQ-FUNC-030, REQ-FUNC-037, REQ-NF-004 | SCR-004 | /mates | - | API-MATES-CRUD | src/components/mates/mates-intro.tsx(신규); src/components/mates/filter-bar.tsx(신규); src/components/mates/mate-post-list.tsx(신규) | 국가·지역·기간 겹침·연령대·성별·스타일·모집상태 필터(AND, 차단 사용자 제외), 결과 카운트, 종료일 경과 글 자동 제외. | 0건이면 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 차단된 사용자의 글은 목록에 노출하지 않는다. | E2E-MATE-AUTH | M |
| 36 | `CMP-SCR004-DETAIL-PANEL` | 동행 상세 패널 + 신청 방법 안내 | COMPONENT | IMPLEMENT | REQ-FUNC-033, REQ-FUNC-069 | SCR-004 | /mates | - | API-MATES-CRUD, SHARED-OUTBOUND-LINK-UTIL | src/components/mates/mate-detail-panel.tsx(신규); src/components/mates/how-to-steps.tsx(신규) | 조건·설명·작성자 요약(연락처 비노출) 표시, 신청 방법 3단계 안내, URL 공유(Web Share API+복사 폴백). | Desktop 좌목록/우상세 분할, Mobile 전체화면 전환. | 이메일·전화번호를 HTML/JSON 어디에도 포함하지 않는다. | E2E-MATE-AUTH | M |
| 37 | `CMP-SCR004-APPLICATION` | 참가 신청 Form | COMPONENT | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-034, REQ-FUNC-035, REQ-FUNC-043 | SCR-004 | /mates | - | API-APPLICATIONS, CMP-SCR005-AUTH | src/components/mates/application-form.tsx(신규) | 500자 이하 비공개 메시지 제출, PENDING 저장, 중복 요청 시 버튼 비활성화+안내, 접수 Toast. | 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 비로그인·성인 미확인 시 제출 차단. | UNIT-MATE-STATE; E2E-MATE-AUTH | M |
| 38 | `CMP-SCR004-REPORT-BLOCK` | 신고·차단 Dialog + 안전 안내 | COMPONENT | IMPLEMENT | REQ-FUNC-039, REQ-FUNC-040 | SCR-004 | /mates | - | API-REPORTS-BLOCKS, CMP-SCR005-AUTH | src/components/mates/report-dialog.tsx(신규); src/components/mates/block-confirm-dialog.tsx(신규); src/components/mates/safety-notice-banner.tsx(신규) | 사유코드+설명 신고 제출(접수번호 Toast), 차단 확인 Dialog(완료 후 상호 콘텐츠 즉시 비노출), 안전 만남 안내 Banner. | Modal은 role=dialog, aria-modal, 포커스 트랩, Esc 닫기를 지원한다. | 신고 대상·처리 이력을 일반 사용자에게 노출하지 않는다. | E2E-MATE-AUTH | M |
| 39 | `CMP-SCR005-AUTH` | Auth 영역(로그인/가입/재설정) — Guest | COMPONENT | IMPLEMENT | REQ-FUNC-028, REQ-FUNC-066 | SCR-005 | /account | - | API-AUTH-PROFILE | src/components/account/auth-tabs.tsx(신규); src/components/account/role-gate.tsx(신규) | 이메일 가입·인증·로그인·로그아웃·비밀번호 재설정, 성인 확인 안내(정확한 생년월일 입력 없음), 로그인 후 가능한 기능 3단계 안내. | 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 비밀번호·인증 토큰을 클라이언트 로그에 남기지 않는다. | E2E-MATE-AUTH | M |
| 40 | `CMP-SCR005-PROFILE` | Profile 영역 — Member | COMPONENT | IMPLEMENT | REQ-FUNC-029 | SCR-005 | /account | - | API-AUTH-PROFILE, CMP-SCR005-AUTH | src/components/account/profile-form.tsx(신규) | 닉네임·연령대·여행스타일(필수), 성별·자기소개(선택) Form + 성인 확인 상태 배지. | 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 정확한 생년월일 필드를 두지 않는다. | E2E-MATE-AUTH | M |
| 41 | `CMP-SCR005-MY-ACTIVITY` | My Activity 영역 — Member | COMPONENT | IMPLEMENT | REQ-FUNC-036, REQ-FUNC-038, REQ-FUNC-040, REQ-FUNC-043, REQ-FUNC-068 | SCR-005 | /account | - | API-MATES-CRUD, API-APPLICATIONS, API-REPORTS-BLOCKS, CMP-SCR005-AUTH | src/components/account/my-activity-panel.tsx(신규) | 내 모집글 관리(수정/마감/삭제, 중요 일정 변경 시 경고), 참가 요청함(승인/거절), 차단 목록(해제), 즐겨찾기 목록(SHARED-FAVORITES-LOCALSTORAGE 연동), 상태 변경 인앱 알림. | 목록별(내 글/요청/차단/즐겨찾기) 개별 완성형 Empty State: 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 비작성자의 승인/거절 시도는 403. | E2E-MATE-AUTH | M |
| 42 | `CMP-SCR005-ADMIN-REPORTS` | Admin 신고 큐 영역 | COMPONENT | IMPLEMENT | REQ-FUNC-041, REQ-FUNC-042 | SCR-005 | /account | - | API-REPORTS-BLOCKS, CMP-SCR005-AUTH | src/components/account/admin-report-queue.tsx(신규) | OPEN/RESOLVED/DISMISSED 필터, 상태 변경, 게시물 숨김; Admin 역할에서만 렌더링(비관리자에게는 이 영역 자체를 렌더링하지 않음). | 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | 비관리자 접근 시 컴포넌트를 렌더링하지 않고, API도 403으로 이중 차단. | E2E-MATE-AUTH | M |
| 43 | `CMP-SCR005-ADMIN-OUTBOUND` | Admin 외부 URL 설정 영역 | COMPONENT | IMPLEMENT | REQ-FUNC-077 | SCR-005 | /account | - | API-ADMIN-OUTBOUND, CMP-SCR005-AUTH | src/components/account/admin-outbound-url-form.tsx(신규) | FLIGHT_OUTBOUND_URL/HOTEL_OUTBOUND_URL 설정 Form(HTTPS 허용목록 검증), Admin 역할에서만 렌더링. | 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. | HTTP·javascript·data 스킴은 저장 UI 단계에서부터 거부. | E2E-MATE-AUTH | M |
| 44 | `PAGE-SCR001` | 홈(/) Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-047, REQ-FUNC-057, REQ-FUNC-064, REQ-FUNC-065, REQ-FUNC-067, REQ-FUNC-078 | SCR-001 | / | `src/app/page.tsx` | SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR001-HERO-SEARCH, CMP-SCR001-DESTINATION-GRID, CMP-SCR001-DESTINATION-DRAWER, CMP-SCR001-SAFETY-GRID, CMP-SCR001-SAFETY-DRAWER, CMP-SCR001-MATE-TEASER, CMP-SCR001-ABOUT-SUMMARY | src/app/page.tsx(수정 — 기존 create-next-app 스타터 제거) | create-next-app 기본 스타터(Next.js 로고 Image, 'To get started, edit the page.tsx file' 문구, Vercel Deploy/Docs 버튼, next.svg/vercel.svg 참조)를 완전히 제거한다.<br>Section 순서: 1) Hero+통합검색 2) 국내 여행지 카드 6개(데이터 출처: DATA-DESTINATIONS) 3) 해외 여행지 카드 6개(DATA-DESTINATIONS) 4) 여행 동기 Chip 6개(DATA-DESTINATIONS 테마 필드) 5) 국가별 주의사항 카드 6개(DATA-SAFETY) 6) 최근 동행글 3개 또는 완성형 Empty State(API-MATES-CRUD) 7) free_traveler 소개 요약(DATA-REPRESENTATIVE).<br>최소 콘텐츠 수: 국내 6장, 해외 6장, 테마 6개, 안전정보 6장, 동행글 3장(또는 Empty State).<br>반응형 콘텐츠 밀도: Desktop 3~4열 Card Grid, Tablet 2열, Mobile 1열; Chip 목록은 가로 스크롤 유지. | 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다. | 항공·호텔·동행 입력값 없음(홈은 열람 전용); 안전정보 Drawer 외부 링크는 noopener,noreferrer. | E2E-PUBLIC-SMOKE; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK | M |
| 45 | `PAGE-SCR002` | 대표 소개(/about) Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-062, REQ-FUNC-063 | SCR-002 | /about | `src/app/about/page.tsx` | SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR002-HERO-STATS, CMP-SCR002-PHILOSOPHY, CMP-SCR002-TIMELINE, CMP-SCR002-COUNTRIES-GALLERY, CMP-SCR002-RECOMMENDED-CTA | src/app/about/page.tsx(신규) | Section 순서: 1) Profile Hero(대표 이미지+한 문장 소개, DATA-REPRESENTATIVE) 2) 여행 지표(50+ Trips/30+ Countries/전문영역, DATA-REPRESENTATIVE) 3) 소개·철학(DATA-REPRESENTATIVE) 4) Timeline 6개 이상(DATA-REPRESENTATIVE) 5) 방문 국가 30개국 이상(DATA-REPRESENTATIVE) 6) 사진 Gallery 8장 이상(DATA-REPRESENTATIVE) 7) 기억에 남는 여행지 4개 + CTA(DATA-DESTINATIONS, DATA-REPRESENTATIVE).<br>최소 콘텐츠 수: Timeline 6개, 방문국가 30개국, Gallery 8장, 추천 여행지 4개.<br>반응형 콘텐츠 밀도: Desktop 좌우 분할(Hero/철학), Gallery Desktop 4열→Mobile 2열, 추천 Grid Desktop 4열→Mobile 1열. | 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다. | 이미지가 특정 서비스 보증인으로 오인되는 연출 금지; SNS/문의 링크는 허용 프로토콜만 렌더링. | E2E-PUBLIC-SMOKE; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK | M |
| 46 | `PAGE-SCR003` | 여행 준비(/travel-tools) Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-011, REQ-FUNC-019, REQ-FUNC-031, REQ-FUNC-054, REQ-FUNC-080 | SCR-003 | /travel-tools | `src/app/travel-tools/page.tsx` | SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR003-SHELL, CMP-SCR003-FLIGHT-FORM, CMP-SCR003-HOTEL-FORM, CMP-SCR003-MATE-WRITE | src/app/travel-tools/page.tsx(신규) | Section 순서: 1) Intro(이용 순서 3단계) 2) 탭(항공/숙소/동행 구하기 — 3개 항상 함께 노출, 탭별 상태 독립) 3) 여행정보 Form(탭별 CMP-SCR003-FLIGHT-FORM/HOTEL-FORM 또는 CMP-SCR003-MATE-WRITE) 4) 입력 요약·외부 이동(항공/숙소 탭) 5) 찾기 Tip 3개 6) 동행 작성 또는 로그인 안내·안전 안내(동행 탭).<br>최소 콘텐츠 수: Tip 3개; 동행 탭 미인증 시 안내 카드 1개 필수.<br>반응형 콘텐츠 밀도: Desktop 입력(60%)/요약(40%) 좌우 분할, Mobile 세로 스택+상단 고정 Segmented 탭.<br>항공/숙소 입력값(국가·지역·날짜)은 서버 DB·로그·분석·외부 URL 쿼리에 저장·전달하지 않는다(CON-01/02, REQ-FUNC-017/025). | 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다. | 외부 이동은 새 탭+noopener,noreferrer; 동행 작성 폼은 연락처 패턴 탐지 후에만 제출 허용. | E2E-TRAVEL-TOOLS; UNIT-TRAVEL-DATES; UNIT-CONTACT-DETECTION; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK | M |
| 47 | `PAGE-SCR004` | 동행 찾기(/mates) Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-030, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-039, REQ-FUNC-040 | SCR-004 | /mates | `src/app/mates/page.tsx` | SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR004-FILTER-LIST, CMP-SCR004-DETAIL-PANEL, CMP-SCR004-APPLICATION, CMP-SCR004-REPORT-BLOCK | src/app/mates/page.tsx(신규) | Section 순서: 1) Intro+작성 CTA 2) Filter·결과 요약(CMP-SCR004-FILTER-LIST) 3) 동행 목록(API-MATES-CRUD, 최소 3장 우선 노출) 4) 상세(CMP-SCR004-DETAIL-PANEL, CMP-SCR004-APPLICATION) 5) 신청 방법 3단계 6) 안전·신고·차단 안내와 CTA(CMP-SCR004-REPORT-BLOCK).<br>최소 콘텐츠 수: 목록 카드 3장 이상(0건 시 Empty State), 신청 방법 3단계.<br>반응형 콘텐츠 밀도: Desktop 좌 목록(40%)/우 상세(60%) 좌우 분할 동시 노출, Mobile 목록 1열→탭 시 상세 전체화면 전환. | 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다. | 모집글·상세 어디에도 전화번호·이메일·메신저ID 노출 금지; 차단 사용자 간 상호 콘텐츠 비노출. | E2E-MATE-AUTH; UNIT-MATE-STATE; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK | M |
| 48 | `PAGE-SCR005` | 계정(/account) Page Owner | PAGE_OWNER | IMPLEMENT | REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-041, REQ-FUNC-066, REQ-FUNC-077 | SCR-005 | /account | `src/app/account/page.tsx` | SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR005-AUTH, CMP-SCR005-PROFILE, CMP-SCR005-MY-ACTIVITY, CMP-SCR005-ADMIN-REPORTS, CMP-SCR005-ADMIN-OUTBOUND | src/app/account/page.tsx(신규) | Guest·Member·Admin 중 현재 역할의 Section만 조립한다(역할에 없는 관리 영역은 렌더링하지 않음): 1) 현재 역할 Intro(무엇을 할 수 있는지) 2) 핵심 작업 — Guest=로그인/가입/재설정(CMP-SCR005-AUTH), Member=프로필+내 활동(CMP-SCR005-PROFILE, CMP-SCR005-MY-ACTIVITY), Admin=신고 큐+외부 URL 설정(CMP-SCR005-ADMIN-REPORTS, CMP-SCR005-ADMIN-OUTBOUND) 3) 도움말 또는 다음 행동(로그인 후 가능한 기능 안내 / 작성 CTA / 관리 범위 고지).<br>최소 콘텐츠 수: Member 내 활동 카드(내 글/요청/차단/즐겨찾기) 각 목록당 최소 1개 Empty 또는 실제 항목; Admin 카드 2개(신고 큐, 외부 URL) 이상.<br>반응형 콘텐츠 밀도: Desktop 좌측 세로 탭 Nav+우측 콘텐츠 분할, Mobile 상단 가로 스크롤 탭+세로 스택. | 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다. | Admin 영역은 서버 역할 검증 없이 클라이언트에서만 숨기지 않는다(RoleGate + API 403 이중 검증); 정확한 생년월일 미표시. | E2E-MATE-AUTH; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK | M |
| 49 | `UNIT-TRAVEL-DATES` | 날짜 검증 Unit Test | UNIT_TEST | IMPLEMENT | REQ-FUNC-013, REQ-FUNC-021 | - | - | - | CMP-SCR003-FLIGHT-FORM, CMP-SCR003-HOTEL-FORM | tests/unit/travel-dates.test.ts(신규) | 과거 출발일/체크인, 역전 날짜, 체크아웃=체크인 등 경계값을 statement 80% 이상 커버한다. | 해당 없음. | 해당 없음. | CI-TYPECHECK-LINT 파이프라인에서 실행 | M |
| 50 | `UNIT-CONTACT-DETECTION` | 연락처 탐지 Unit Test | UNIT_TEST | IMPLEMENT | REQ-FUNC-032 | - | - | - | CMP-SCR003-MATE-WRITE | tests/unit/contact-detection.test.ts(신규) | 전화번호·이메일·메신저ID 패턴 테스트셋 기준 탐지율 95% 이상, 오탐 5% 이하를 검증한다. | 해당 없음. | 해당 없음. | CI-TYPECHECK-LINT 파이프라인에서 실행 | M |
| 51 | `UNIT-MATE-STATE` | 동행 상태 전이 Unit Test | UNIT_TEST | IMPLEMENT | REQ-FUNC-035, REQ-FUNC-036, REQ-FUNC-037 | - | - | - | API-MATES-CRUD, API-APPLICATIONS | tests/unit/mate-state.test.ts(신규) | MATE_POST(OPEN/CLOSED/HIDDEN/DELETED), MATE_APPLICATION(PENDING/ACCEPTED/REJECTED/WITHDRAWN) 상태 전이표를 검증하고 중복 PENDING/ACCEPTED, 비작성자 전이 시도를 차단하는지 확인한다. | 해당 없음. | 해당 없음. | CI-TYPECHECK-LINT 파이프라인에서 실행 | M |
| 52 | `TEST-RLS-BASIC` | RLS 정책 통합 테스트 | INTEGRATION_TEST | IMPLEMENT | REQ-FUNC-044, REQ-NF-013 | - | - | - | DB-RLS-BASE, DB-SEED-BASE | tests/integration/rls-basic.test.ts(신규) | 본인/타인/차단관계/Admin 조합으로 mate_applications, reports, blocks에 대한 부정 접근을 시도해 모두 403 또는 빈 결과를 반환하는지 검증한다. | 해당 없음. | 이 Task 자체가 보안 검증 Task다. | Supabase 로컬/스테이징 DB against 실행 | M |
| 53 | `E2E-PUBLIC-SMOKE` | 공개 열람 Smoke(Chromium) | E2E_TEST | IMPLEMENT | REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-047, REQ-FUNC-057 | SCR-001, SCR-002 | - | - | PAGE-SCR001, PAGE-SCR002 | tests/e2e/public-smoke.spec.ts(신규); playwright.config.ts(신규, Chromium 프로젝트만) | SM-01(여행지 탐색·필터·상세·안전정보 이동), SM-08(안전정보 필수요소·stale 경고), SM-09(대표 소개 수치·추천 링크) 흐름을 하나의 Chromium 전용 Smoke 스펙으로 묶는다. | 해당 없음(테스트 코드). | 해당 없음. | CI에서 Chromium만 실행(Firefox/WebKit 프로젝트 추가 금지) | M |
| 54 | `E2E-TRAVEL-TOOLS` | 항공·호텔·동행작성 Smoke(Chromium) | E2E_TEST | IMPLEMENT | REQ-FUNC-011, REQ-FUNC-016, REQ-FUNC-019, REQ-FUNC-024, REQ-FUNC-031 | SCR-003 | - | - | PAGE-SCR003 | tests/e2e/travel-tools.spec.ts(신규) | SM-02(항공 폼→요약→외부 새탭, query 없음), SM-03(호텔 동일 흐름)을 하나의 Chromium Smoke 스펙으로 묶는다. | 해당 없음(테스트 코드). | 새 탭 URL에 목적지·날짜 query가 없음을 어서션한다. | CI에서 Chromium만 실행 | M |
| 55 | `E2E-MATE-AUTH` | 가입·동행·신고차단 Smoke(Chromium) | E2E_TEST | IMPLEMENT | REQ-FUNC-027, REQ-FUNC-034, REQ-FUNC-036, REQ-FUNC-039, REQ-FUNC-040 | SCR-004, SCR-005 | - | - | PAGE-SCR004, PAGE-SCR005, DB-SEED-BASE | tests/e2e/mate-auth.spec.ts(신규) | SM-04(가입→인증→로그인→성인확인), SM-05(동행글 작성+연락처 차단 케이스), SM-06(참가요청→승인), SM-07(신고+차단), SM-10(마이페이지/관리자 탭 접근 제어)을 2~3개 Chromium Smoke 스펙으로 묶는다. | 해당 없음(테스트 코드). | 비관리자의 Admin 탭 접근이 차단되는지 어서션한다. | CI에서 Chromium만 실행 | M |
| 56 | `CI-TYPECHECK-LINT` | CI: TypeScript strict + ESLint + 테스트 실행 | CI | IMPLEMENT | REQ-NF-031 | - | - | - | - | .github/workflows/ci.yml(신규) | main 병합 전 `tsc --noEmit`, `next lint`, UNIT-*/TEST-RLS-BASIC/E2E-* 실행을 CI 파이프라인에 연결한다. | 해당 없음. | CI 환경변수(Supabase 키 등)는 저장소 Secrets로만 관리한다. | CI 파이프라인 자체 실행 결과 | M |
| 57 | `MANUAL-CONTENT-COMPLETENESS` | 콘텐츠 완전성 수동 체크리스트 | MANUAL_CHECK | IMPLEMENT | REQ-FUNC-008, REQ-FUNC-046, REQ-NF-026, REQ-NF-027 | ALL(SCR-001~005) | - | - | DATA-DESTINATIONS, DATA-SAFETY | 해당 없음(코드 산출물 없음 — 점검 결과만 기록) | 국내 10개 이상, 해외 15개국 30개 도시 이상, 해외 국가 100% 안전정보 커버리지를 브라우저에서 직접 세어 확인한다. | 해당 없음. | 해당 없음. | 배포 전 1회 수동 실행, 결과를 릴리스 체크리스트에 기록 | M |
| 58 | `MANUAL-ACCESSIBILITY-CHECK` | 키보드·스크린리더 수동 점검 | MANUAL_CHECK | IMPLEMENT | REQ-FUNC-079, REQ-NF-023, REQ-NF-025 | ALL(SCR-001~005) | - | - | PAGE-SCR001, PAGE-SCR002, PAGE-SCR003, PAGE-SCR004, PAGE-SCR005 | 해당 없음(코드 산출물 없음 — 점검 결과만 기록) | 5개 Screen 핵심 흐름(검색, 폼 입력, 모달 닫기, 신고 제출)을 키보드만으로 완료하고 스크린리더로 주요 레이블을 확인한다. | 해당 없음. | 해당 없음. | 배포 전 1회 수동 실행, 결과를 릴리스 체크리스트에 기록 | M |
| 59 | `MANUAL-RESPONSIVE-CHECK` | 반응형(320px~Desktop) 수동 점검 | MANUAL_CHECK | IMPLEMENT | REQ-FUNC-065 | ALL(SCR-001~005) | - | - | PAGE-SCR001, PAGE-SCR002, PAGE-SCR003, PAGE-SCR004, PAGE-SCR005 | 해당 없음(코드 산출물 없음 — 점검 결과만 기록) | 320px, 390px, 744px, 1128px, 1440px 뷰포트에서 가로 스크롤·겹침 없이 5개 Screen이 동작하는지 브라우저 반응형 도구로 확인한다. | 해당 없음. | 해당 없음. | 배포 전 1회 수동 실행, 결과를 릴리스 체크리스트에 기록 | M |
| 60 | `RELEASE-VERCEL-SUPABASE-CHECK` | Vercel/Supabase 배포 환경 확인 | RELEASE_CHECK | IMPLEMENT | REQ-NF-012, REQ-NF-016 | - | - | - | DB-SCHEMA-BASE, DB-RLS-BASE | 해당 없음(코드 산출물 없음 — 점검 결과만 기록) | Vercel 프로젝트 연결, TLS 1.2+ 적용, Supabase 프로젝트·환경변수(FLIGHT/HOTEL_OUTBOUND_URL, MOFA_SAFETY_URL, Supabase 키)가 클라이언트 번들에 노출되지 않았는지 확인한다. | 해당 없음. | 비밀키가 `NEXT_PUBLIC_` 접두사로 잘못 노출되지 않았는지 빌드 산출물을 검사한다. | 배포 전 1회 수동 실행 | M |
| 61 | `RELEASE-EXTERNAL-LINKS-CHECK` | 외부 링크 실제 브라우저 점검 | RELEASE_CHECK | IMPLEMENT | REQ-FUNC-016, REQ-FUNC-018, REQ-FUNC-024, REQ-FUNC-026, REQ-FUNC-049, REQ-FUNC-062 | - | - | - | SHARED-OUTBOUND-LINK-UTIL | 해당 없음(코드 산출물 없음 — 점검 결과만 기록) | 항공·호텔 외부 URL, 외교부 안전정보 링크, 문의·SNS 링크가 실제 브라우저에서 정상 오픈되는지 배포 전 점검한다(ASM-01). | 해당 없음. | 모든 외부 링크가 noopener,noreferrer를 포함하는지 함께 확인한다. | 배포 전 1회 수동 실행 | M |
| 62 | `RELEASE-LIGHTHOUSE-CHECK` | Core Web Vitals 수동 Lighthouse 점검 | RELEASE_CHECK | IMPLEMENT | REQ-NF-001, REQ-NF-002, REQ-NF-003, REQ-NF-006 | ALL(SCR-001~005) | - | - | PAGE-SCR001, PAGE-SCR002, PAGE-SCR003, PAGE-SCR004, PAGE-SCR005 | 해당 없음(코드 산출물 없음 — 점검 결과만 기록) | 5개 Screen에서 LCP p75 ≤2.5s, INP p75 ≤200ms, CLS p75 ≤0.1 목표를 모바일 Lighthouse로 확인한다. | 해당 없음. | 해당 없음. | 배포 전 1회 수동 실행 | S |
| 63 | `RELEASE-COST-CHECK` | MVP 월 인프라 비용 확인 | RELEASE_CHECK | IMPLEMENT | REQ-NF-034 | - | - | - | - | 해당 없음(코드 산출물 없음 — 점검 결과만 기록) | Vercel·Supabase 무료/저가 티어 사용료가 콘텐츠 인건비 제외 월 100,000원 이하인지 배포 시점에 확인한다. | 해당 없음. | 해당 없음. | 배포 시점 1회 수동 실행 | S |

## 2. NON_IMPLEMENTATION (EXCLUDED Requirements)

`app/docs/PROJECT_SCOPE.md`가 확정한 EXCLUDED 24개. 상세 구현 Task는 만들지 않으며, 이 표에서 삭제하지 않는다.

| Requirement | 근거 | 후속 방향 |
|---|---|---|
| REQ-FUNC-007 | 대체텍스트만 REQ-FUNC-004 상세 표시에 포함하고, 이미지 출처·작가·라이선스 메타데이터 저장 체계는 만들지 않는다. | 미디어 워크플로가 필요해지면 MEDIA_ASSET 테이블과 관리자 업로드 UI를 별도 Task로 재검토한다. |
| REQ-FUNC-045 | 탈퇴 시 자동 비식별화·법적 보존 예외 처리 파이프라인을 구현하지 않고 로그아웃/계정 비활성화 수준으로 제한한다. | 회원 수가 늘어나면 Supabase Edge Function 기반 비식별화 배치 Task를 추가한다. |
| REQ-FUNC-055 | 안전정보는 개발자가 src/data를 직접 작성·수정하며 별도 작성-검수-게시 워크플로 UI는 제공하지 않는다. | 콘텐츠 팀이 별도로 생기면 Editor 역할과 DRAFT/REVIEW/PUBLISHED 상태 전이를 재검토한다. |
| REQ-FUNC-056 | 안전정보 변경 이력 테이블을 만들지 않고 Git 커밋 이력으로 대체한다. | 규제 대응이 필요해지면 별도 이력 테이블과 Admin 조회 UI를 Task화한다. |
| REQ-FUNC-061 | 대표 이미지도 REQ-FUNC-007과 동일하게 대체텍스트만 관리한다. | REQ-FUNC-007과 함께 재검토한다. |
| REQ-FUNC-071 | 커스텀 행동 분석 이벤트 파이프라인을 구축하지 않는다(운영 로그·분석 도구는 범위 밖). | KPI 측정이 필요해지면 Vercel Analytics 등 경량 도구 도입을 별도 Task로 검토한다. |
| REQ-FUNC-072 | 여행지 콘텐츠는 src/data 정적 파일로 개발자가 직접 관리하며 CRUD/미리보기 UI를 제공하지 않는다. | REQ-FUNC-055와 함께 콘텐츠 팀 규모에 따라 재검토한다. |
| REQ-FUNC-073 | 이미지 업로드 기능 자체가 없다(URL+alt만 사용). | REQ-FUNC-007/061과 함께 재검토한다. |
| REQ-FUNC-074 | 자동 게이트 시스템 없이 정적 데이터 작성 시 수동 체크리스트(MANUAL-CONTENT-COMPLETENESS)로 대체한다. | 콘텐츠 양이 커지면 CI 단계의 스키마 검증 스크립트를 별도 Task로 추가한다. |
| REQ-FUNC-075 | 관리자 범위를 신고·외부 URL로 한정하고 stale 대시보드는 만들지 않는다(표시 로직은 REQ-FUNC-050으로 충분). | 운영 인력이 늘면 Admin 대시보드 Task를 재검토한다. |
| REQ-FUNC-076 | 범용 감사 로그 테이블을 만들지 않는다(REPORT 테이블의 현재 상태 필드만 유지). | 컴플라이언스 요구가 생기면 AUDIT_LOG 테이블과 기록 Task를 추가한다. |
| REQ-NF-007 | 자동 성능 CI 게이트를 구축하지 않고 RELEASE-LIGHTHOUSE-CHECK 수동 점검으로 대체한다. | 트래픽이 늘면 Lighthouse CI Action을 CI-TYPECHECK-LINT에 추가하는 Task를 검토한다. |
| REQ-NF-008 | 가동률 모니터링·SLA 리포팅 체계를 구축하지 않고 Vercel 기본 인프라에 의존한다. | 유료 모니터링 도구 도입 시 재검토. |
| REQ-NF-009 | 오류율 모니터링/알림 파이프라인을 구축하지 않는다. | Vercel/Sentry 연동이 필요해지면 재검토. |
| REQ-NF-010 | 자동 백업 체계를 구축하지 않고 Supabase 기본 제공 수준에 의존한다. | 데이터 규모가 커지면 백업 정책 Task를 추가한다. |
| REQ-NF-011 | 외부 링크 자동 검사·장애 알림 인프라를 구축하지 않고 RELEASE-EXTERNAL-LINKS-CHECK 수동 점검으로 대체한다. | 정기 알림이 필요해지면 스케줄러 기반 링크체커 Task를 추가한다. |
| REQ-NF-018 | 개인정보 내보내기·삭제 요청 파이프라인을 구현하지 않는다(REQ-FUNC-045와 동일 사유). | 법적 요구가 생기면 재검토한다. |
| REQ-NF-020 | 신고 1차 검토 24시간 SLA는 운영 인력 지표이며 코드로 보장할 수 없다. | 운영 인력 확보 시 SLA 추적 대시보드를 검토한다. |
| REQ-NF-021 | 글·요청·신고 속도 제한(rate limiting) 인프라를 구축하지 않는다. | 악용 사례가 발생하면 Vercel Edge Middleware 기반 rate limit Task를 추가한다. |
| REQ-NF-022 | 범용 감사 로그 미구현으로 Moderator 조치 추적 체계도 만들지 않는다(REQ-FUNC-076과 동일 사유). | REQ-FUNC-076과 함께 재검토. |
| REQ-NF-024 | axe 자동 접근성 검사 파이프라인을 구축하지 않고 MANUAL-ACCESSIBILITY-CHECK 수동 점검으로 대체한다. | CI 리소스가 확보되면 axe-core CI Task를 추가한다. |
| REQ-NF-029 | 이미지 정책이 URL+alt로 단순화되어 라이선스 메타데이터 자체를 관리하지 않는다(REQ-FUNC-007/061과 동일). | REQ-FUNC-007과 함께 재검토한다. |
| REQ-NF-032 | 구조화 로그 파이프라인을 구축하지 않고 Vercel 기본 로그에 의존한다. | 운영 규모가 커지면 로깅 인프라 Task를 추가한다. |
| REQ-NF-033 | 5xx/외부 링크 실패 자동 알림을 구축하지 않는다. | REQ-NF-011과 함께 알림 인프라 도입 시 재검토. |

## 3. Requirement Coverage Verification (114개 전수)

| Requirement | Status | Task ID(s) |
|---|---|---|
| REQ-FUNC-001 | IMPLEMENT | `CMP-SCR001-DESTINATION-GRID` |
| REQ-FUNC-002 | IMPLEMENT | `CMP-SCR001-DESTINATION-GRID` |
| REQ-FUNC-003 | IMPLEMENT | `CMP-SCR001-HERO-SEARCH` |
| REQ-FUNC-004 | IMPLEMENT | `CMP-SCR001-DESTINATION-DRAWER`, `DATA-DESTINATIONS` |
| REQ-FUNC-005 | IMPLEMENT | `CMP-SCR001-DESTINATION-GRID` |
| REQ-FUNC-006 | IMPLEMENT | `CMP-SCR001-DESTINATION-DRAWER`, `CMP-SCR001-SAFETY-DRAWER` |
| REQ-FUNC-007 | EXCLUDED | - |
| REQ-FUNC-008 | IMPLEMENT | `DATA-DESTINATIONS`, `MANUAL-CONTENT-COMPLETENESS` |
| REQ-FUNC-009 | IMPLEMENT | `CMP-SCR001-DESTINATION-DRAWER` |
| REQ-FUNC-010 | IMPLEMENT | `CMP-SCR001-DESTINATION-GRID` |
| REQ-FUNC-011 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM` |
| REQ-FUNC-012 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM` |
| REQ-FUNC-013 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM`, `UNIT-TRAVEL-DATES` |
| REQ-FUNC-014 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM` |
| REQ-FUNC-015 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM` |
| REQ-FUNC-016 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM`, `SHARED-OUTBOUND-LINK-UTIL` |
| REQ-FUNC-017 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM` |
| REQ-FUNC-018 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM`, `SHARED-OUTBOUND-LINK-UTIL` |
| REQ-FUNC-019 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM` |
| REQ-FUNC-020 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM` |
| REQ-FUNC-021 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM`, `UNIT-TRAVEL-DATES` |
| REQ-FUNC-022 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM` |
| REQ-FUNC-023 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM` |
| REQ-FUNC-024 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM`, `SHARED-OUTBOUND-LINK-UTIL` |
| REQ-FUNC-025 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM` |
| REQ-FUNC-026 | IMPLEMENT | `CMP-SCR003-HOTEL-FORM`, `SHARED-OUTBOUND-LINK-UTIL` |
| REQ-FUNC-027 | IMPLEMENT | `CMP-SCR003-MATE-WRITE`, `CMP-SCR004-APPLICATION`, `API-MATES-CRUD`, `API-APPLICATIONS` |
| REQ-FUNC-028 | IMPLEMENT | `CMP-SCR005-AUTH`, `DB-SCHEMA-BASE` |
| REQ-FUNC-029 | IMPLEMENT | `CMP-SCR005-PROFILE`, `API-AUTH-PROFILE` |
| REQ-FUNC-030 | IMPLEMENT | `CMP-SCR004-FILTER-LIST`, `API-MATES-CRUD` |
| REQ-FUNC-031 | IMPLEMENT | `CMP-SCR003-MATE-WRITE`, `API-MATES-CRUD` |
| REQ-FUNC-032 | IMPLEMENT | `CMP-SCR003-MATE-WRITE`, `API-MATES-CRUD`, `UNIT-CONTACT-DETECTION` |
| REQ-FUNC-033 | IMPLEMENT | `CMP-SCR004-DETAIL-PANEL`, `API-MATES-CRUD` |
| REQ-FUNC-034 | IMPLEMENT | `CMP-SCR004-APPLICATION`, `API-APPLICATIONS` |
| REQ-FUNC-035 | IMPLEMENT | `CMP-SCR004-APPLICATION`, `API-APPLICATIONS`, `DB-SCHEMA-BASE`, `UNIT-MATE-STATE` |
| REQ-FUNC-036 | IMPLEMENT | `CMP-SCR005-MY-ACTIVITY`, `API-APPLICATIONS`, `UNIT-MATE-STATE` |
| REQ-FUNC-037 | IMPLEMENT | `CMP-SCR004-FILTER-LIST`, `API-MATES-CRUD`, `UNIT-MATE-STATE` |
| REQ-FUNC-038 | IMPLEMENT | `CMP-SCR005-MY-ACTIVITY`, `API-MATES-CRUD` |
| REQ-FUNC-039 | IMPLEMENT | `CMP-SCR004-REPORT-BLOCK`, `API-REPORTS-BLOCKS` |
| REQ-FUNC-040 | IMPLEMENT | `CMP-SCR004-REPORT-BLOCK`, `CMP-SCR005-MY-ACTIVITY`, `API-REPORTS-BLOCKS` |
| REQ-FUNC-041 | IMPLEMENT | `CMP-SCR005-ADMIN-REPORTS`, `API-REPORTS-BLOCKS` |
| REQ-FUNC-042 | IMPLEMENT | `CMP-SCR005-ADMIN-REPORTS`, `API-REPORTS-BLOCKS` |
| REQ-FUNC-043 | IMPLEMENT | `CMP-SCR004-APPLICATION`, `CMP-SCR005-MY-ACTIVITY` |
| REQ-FUNC-044 | IMPLEMENT | `DB-RLS-BASE`, `TEST-RLS-BASIC` |
| REQ-FUNC-045 | EXCLUDED | - |
| REQ-FUNC-046 | IMPLEMENT | `DATA-SAFETY`, `MANUAL-CONTENT-COMPLETENESS` |
| REQ-FUNC-047 | IMPLEMENT | `DATA-SAFETY`, `CMP-SCR001-SAFETY-DRAWER` |
| REQ-FUNC-048 | IMPLEMENT | `DATA-SAFETY`, `CMP-SCR001-SAFETY-DRAWER` |
| REQ-FUNC-049 | IMPLEMENT | `CMP-SCR001-SAFETY-DRAWER`, `SHARED-OUTBOUND-LINK-UTIL` |
| REQ-FUNC-050 | IMPLEMENT | `CMP-SCR001-SAFETY-DRAWER` |
| REQ-FUNC-051 | IMPLEMENT | `CMP-SCR001-SAFETY-DRAWER` |
| REQ-FUNC-052 | IMPLEMENT | `DATA-SAFETY`, `CMP-SCR001-SAFETY-DRAWER` |
| REQ-FUNC-053 | IMPLEMENT | `DATA-SAFETY`, `CMP-SCR001-SAFETY-DRAWER` |
| REQ-FUNC-054 | IMPLEMENT | `CMP-SCR001-SAFETY-DRAWER`, `CMP-SCR003-SHELL` |
| REQ-FUNC-055 | EXCLUDED | - |
| REQ-FUNC-056 | EXCLUDED | - |
| REQ-FUNC-057 | IMPLEMENT | `CMP-SCR002-HERO-STATS`, `DATA-REPRESENTATIVE`, `CMP-SCR001-ABOUT-SUMMARY` |
| REQ-FUNC-058 | IMPLEMENT | `CMP-SCR002-PHILOSOPHY`, `DATA-REPRESENTATIVE` |
| REQ-FUNC-059 | IMPLEMENT | `CMP-SCR002-COUNTRIES-GALLERY`, `DATA-REPRESENTATIVE` |
| REQ-FUNC-060 | IMPLEMENT | `CMP-SCR002-TIMELINE`, `DATA-REPRESENTATIVE` |
| REQ-FUNC-061 | EXCLUDED | - |
| REQ-FUNC-062 | IMPLEMENT | `CMP-SCR002-RECOMMENDED-CTA` |
| REQ-FUNC-063 | IMPLEMENT | `CMP-SCR002-RECOMMENDED-CTA`, `DATA-DESTINATIONS` |
| REQ-FUNC-064 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER` |
| REQ-FUNC-065 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER`, `MANUAL-RESPONSIVE-CHECK` |
| REQ-FUNC-066 | IMPLEMENT | `CMP-SCR005-AUTH`, `API-AUTH-PROFILE` |
| REQ-FUNC-067 | IMPLEMENT | `CMP-SCR001-HERO-SEARCH` |
| REQ-FUNC-068 | IMPLEMENT | `SHARED-FAVORITES-LOCALSTORAGE`, `CMP-SCR005-MY-ACTIVITY` |
| REQ-FUNC-069 | IMPLEMENT | `CMP-SCR001-DESTINATION-DRAWER`, `CMP-SCR004-DETAIL-PANEL` |
| REQ-FUNC-070 | IMPLEMENT | `SHARED-SEO-METADATA` |
| REQ-FUNC-071 | EXCLUDED | - |
| REQ-FUNC-072 | EXCLUDED | - |
| REQ-FUNC-073 | EXCLUDED | - |
| REQ-FUNC-074 | EXCLUDED | - |
| REQ-FUNC-075 | EXCLUDED | - |
| REQ-FUNC-076 | EXCLUDED | - |
| REQ-FUNC-077 | IMPLEMENT | `CMP-SCR005-ADMIN-OUTBOUND`, `API-ADMIN-OUTBOUND`, `SHARED-OUTBOUND-LINK-UTIL` |
| REQ-FUNC-078 | IMPLEMENT | `SHARED-ERROR-NOTFOUND` |
| REQ-FUNC-079 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER`, `MANUAL-ACCESSIBILITY-CHECK` |
| REQ-FUNC-080 | IMPLEMENT | `CMP-SCR003-MATE-WRITE`, `SHARED-LAYOUT-NAV-FOOTER` |
| REQ-NF-001 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER`, `RELEASE-LIGHTHOUSE-CHECK` |
| REQ-NF-002 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER`, `RELEASE-LIGHTHOUSE-CHECK` |
| REQ-NF-003 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER`, `RELEASE-LIGHTHOUSE-CHECK` |
| REQ-NF-004 | IMPLEMENT | `CMP-SCR001-DESTINATION-GRID`, `CMP-SCR004-FILTER-LIST` |
| REQ-NF-005 | IMPLEMENT | `API-MATES-CRUD`, `API-APPLICATIONS`, `API-REPORTS-BLOCKS` |
| REQ-NF-006 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER`, `RELEASE-LIGHTHOUSE-CHECK` |
| REQ-NF-007 | EXCLUDED | - |
| REQ-NF-008 | EXCLUDED | - |
| REQ-NF-009 | EXCLUDED | - |
| REQ-NF-010 | EXCLUDED | - |
| REQ-NF-011 | EXCLUDED | - |
| REQ-NF-012 | IMPLEMENT | `RELEASE-VERCEL-SUPABASE-CHECK` |
| REQ-NF-013 | IMPLEMENT | `DB-RLS-BASE`, `TEST-RLS-BASIC` |
| REQ-NF-014 | IMPLEMENT | `DB-ACCESS` |
| REQ-NF-015 | IMPLEMENT | `DB-ACCESS`, `API-MATES-CRUD` |
| REQ-NF-016 | IMPLEMENT | `RELEASE-VERCEL-SUPABASE-CHECK` |
| REQ-NF-017 | IMPLEMENT | `CMP-SCR003-FLIGHT-FORM`, `CMP-SCR003-HOTEL-FORM` |
| REQ-NF-018 | EXCLUDED | - |
| REQ-NF-019 | IMPLEMENT | `API-REPORTS-BLOCKS` |
| REQ-NF-020 | EXCLUDED | - |
| REQ-NF-021 | EXCLUDED | - |
| REQ-NF-022 | EXCLUDED | - |
| REQ-NF-023 | IMPLEMENT | `SHARED-LAYOUT-NAV-FOOTER`, `MANUAL-ACCESSIBILITY-CHECK` |
| REQ-NF-024 | EXCLUDED | - |
| REQ-NF-025 | IMPLEMENT | `MANUAL-ACCESSIBILITY-CHECK` |
| REQ-NF-026 | IMPLEMENT | `DATA-DESTINATIONS`, `MANUAL-CONTENT-COMPLETENESS` |
| REQ-NF-027 | IMPLEMENT | `DATA-SAFETY`, `MANUAL-CONTENT-COMPLETENESS` |
| REQ-NF-028 | IMPLEMENT | `CMP-SCR001-SAFETY-DRAWER` |
| REQ-NF-029 | EXCLUDED | - |
| REQ-NF-030 | IMPLEMENT | `SHARED-SEO-METADATA` |
| REQ-NF-031 | IMPLEMENT | `CI-TYPECHECK-LINT` |
| REQ-NF-032 | EXCLUDED | - |
| REQ-NF-033 | EXCLUDED | - |
| REQ-NF-034 | IMPLEMENT | `RELEASE-COST-CHECK` |

- 검증 결과: 114/114 Requirement 전수 포함, 누락 0건, IMPLEMENT 90건 전부 Task 연결, EXCLUDED 24건 전부 §2에 기록.
- 참고: 아래 Task는 특정 REQ ID에 1:1로 연결되지 않는 기반/QA 지원 Task로, 해당 Task의 `Requirement Ref` 열에 근거를 별도 기술했다: `CMP-SCR001-MATE-TEASER`, `CMP-SCR001-SAFETY-GRID`, `DB-SEED-BASE`, `E2E-MATE-AUTH`, `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `PAGE-SCR001`, `PAGE-SCR002`, `PAGE-SCR003`, `PAGE-SCR004`, `PAGE-SCR005`, `RELEASE-EXTERNAL-LINKS-CHECK`, `SHARED-DESIGN-TOKENS`
