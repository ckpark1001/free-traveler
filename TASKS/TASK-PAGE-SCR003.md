# PAGE-SCR003

여행 준비(/travel-tools) Page Owner

## Context
여행 준비(/travel-tools) Page Owner. `/travel-tools` Route의 Page Entry를 조립하는 Page Owner Task로, 하위 Component/Data/API Task가 이미 만든 결과물을 가져와 화면 하나로 완성하는 역할만 수행한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-011, REQ-FUNC-019, REQ-FUNC-031, REQ-FUNC-054, REQ-FUNC-080

## Screen / Route / Page Entry
Screen: **SCR-003** (여행 준비(/travel-tools))  
Route: `/travel-tools`  
Page Entry: `src/app/travel-tools/page.tsx`

## Design Ref
`design-reference/UI_CONTRACT.md` — 여행 준비(/travel-tools) 영역 순서·상태·Desktop·Mobile 규칙 전문; `design-reference/D-001/DESIGN.md` §15-5(Screen Inventory), §16(Placeholder/Empty State 규칙), §17(Do/Do Not); `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Depends On
SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR003-SHELL, CMP-SCR003-FLIGHT-FORM, CMP-SCR003-HOTEL-FORM, CMP-SCR003-MATE-WRITE

## Expected Files
src/app/travel-tools/page.tsx(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
Section 순서: 1) Intro(이용 순서 3단계) 2) 탭(항공/숙소/동행 구하기 — 3개 항상 함께 노출, 탭별 상태 독립) 3) 여행정보 Form(탭별 CMP-SCR003-FLIGHT-FORM/HOTEL-FORM 또는 CMP-SCR003-MATE-WRITE) 4) 입력 요약·외부 이동(항공/숙소 탭) 5) 찾기 Tip 3개 6) 동행 작성 또는 로그인 안내·안전 안내(동행 탭).<br>최소 콘텐츠 수: Tip 3개; 동행 탭 미인증 시 안내 카드 1개 필수.<br>반응형 콘텐츠 밀도: Desktop 입력(60%)/요약(40%) 좌우 분할, Mobile 세로 스택+상단 고정 Segmented 탭.<br>항공/숙소 입력값(국가·지역·날짜)은 서버 DB·로그·분석·외부 URL 쿼리에 저장·전달하지 않는다(CON-01/02, REQ-FUNC-017/025).
<br>화면 상태(UI_CONTRACT 여행 준비 상태 표, 세 탭은 상태를 서로 분리): Loading = 외부 이동 CTA 클릭 직후 새 탭 오픈 대기(약 200ms); Success = 항공/숙소 입력 요약 표시 또는 동행글 게시 완료 Toast; Empty = 해당 없음(폼 화면); Error = 필수값 누락·날짜 역전·연락처 패턴 탐지·외부 URL 미설정/오류 시 인라인 오류; Unauthorized = 동행 탭에서 비로그인·성인 미확인이면 안내 카드 + /account 로그인 CTA.

## Visual AC
데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다.

## Security/Privacy AC
외부 이동은 새 탭+noopener,noreferrer; 동행 작성 폼은 연락처 패턴 탐지 후에만 제출 허용.

## Test Cases
- 확인: Section 순서: 1) Intro(이용 순서 3단계) 2) 탭(항공/숙소/동행 구하기 — 3개 항상 함께 노출, 탭별 상태 독립) 3) 여행정보 Form(탭별 CMP-SCR003-FLIGHT-FORM/HOTEL-FORM 또는 CMP-SCR003-MATE-WRITE) 4) 입력 요약·외부 이동(항공/숙소 탭) 5) 찾기 Tip 3개 6) 동행 작성 또는 로그인 안내·안전 안내(동행 탭).
- 확인: 최소 콘텐츠 수: Tip 3개.
- 확인: 동행 탭 미인증 시 안내 카드 1개 필수.
- 확인: 반응형 콘텐츠 밀도: Desktop 입력(60%)/요약(40%) 좌우 분할, Mobile 세로 스택+상단 고정 Segmented 탭.
- 확인: 항공/숙소 입력값(국가·지역·날짜)은 서버 DB·로그·분석·외부 URL 쿼리에 저장·전달하지 않는다(CON-01/02, REQ-FUNC-017/025).
- 시각 확인: 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다.
- 확인: 화면 상태(UI_CONTRACT 여행 준비 상태 표, 세 탭은 상태를 서로 분리): Loading = 외부 이동 CTA 클릭 직후 새 탭 오픈 대기(약 200ms); Success = 항공/숙소 입력 요약 표시 또는 동행글 게시 완료 Toast; Empty = 해당 없음(폼 화면); Error = 필수값 누락·날짜 역전·연락처 패턴 탐지·외부 URL 미설정/오류 시 인라인 오류; Unauthorized = 동행 탭에서 비로그인·성인 미확인이면 안내 카드 + /account 로그인 CTA.

## Verify
E2E-TRAVEL-TOOLS; UNIT-TRAVEL-DATES; UNIT-CONTACT-DETECTION; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK

## Definition of Done
- [ ] Expected Files에 나열된 파일이 정확히 그 파일들만 생성·수정되어 있다(그 밖의 파일 변경 없음).
- [ ] Functional AC / Visual AC / Security·Privacy AC 항목이 모두 충족된다.
- [ ] Depends On에 나열된 모든 Task가 먼저 완료되어 있다.
- [ ] Verify에 명시된 테스트·점검이 통과한다(Test Cases 절 기준).
- [ ] Forbidden 항목에 해당하는 코드·문구·파일이 없다.
- [ ] 항공·숙소·동행 구하기 3개 탭이 한 화면 안에서 실제로 조립되어 있다.

## Forbidden
- Expected Files에 명시되지 않은 파일을 생성·수정하지 않는다.
- Airbnb 상표 요소(로고, Rausch 계열 색상 `#ff385c` 등, Cereal 폰트, "Guest favorite" 배지 등)를 사용하지 않는다.
- 예약하기·결제하기·가격비교·재고확인 등 구매/예약/결제 성격의 UI·API를 추가하지 않는다.
- 별점·리뷰 점수·좋아요 수·실시간 항공권/호텔 가격 배지를 추가하지 않는다.
- Lorem ipsum·'준비 중'·'정보 확인 필요' 등 미완성 Placeholder 문구와 내용 없는 Card를 사용하지 않는다.
- 이 Task 범위에서 구현 코드를 실제로 커밋하거나 Branch/PR/Issue를 생성하지 않는다(본 파일은 Task 정의 문서다).
- 하위 Component 파일을 새로 생성하지 않는다 — Depends On에 나열된 기존 Component/Data/API를 import·조립하는 것만 이 Task의 범위다(규칙 6).
