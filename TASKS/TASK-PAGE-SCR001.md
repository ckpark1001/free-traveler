# PAGE-SCR001

홈(/) Page Owner

## Context
홈(/) Page Owner. `/` Route의 Page Entry를 조립하는 Page Owner Task로, 하위 Component/Data/API Task가 이미 만든 결과물을 가져와 화면 하나로 완성하는 역할만 수행한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-047, REQ-FUNC-057, REQ-FUNC-064, REQ-FUNC-065, REQ-FUNC-067, REQ-FUNC-078

## Screen / Route / Page Entry
Screen: **SCR-001** (홈(/))  
Route: `/`  
Page Entry: `src/app/page.tsx`

## Design Ref
`design-reference/UI_CONTRACT.md` — 홈(/) 영역 순서·상태·Desktop·Mobile 규칙 전문; `design-reference/D-001/DESIGN.md` §15-5(Screen Inventory), §16(Placeholder/Empty State 규칙), §17(Do/Do Not); `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Depends On
SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR001-HERO-SEARCH, CMP-SCR001-DESTINATION-GRID, CMP-SCR001-DESTINATION-DRAWER, CMP-SCR001-SAFETY-GRID, CMP-SCR001-SAFETY-DRAWER, CMP-SCR001-MATE-TEASER, CMP-SCR001-ABOUT-SUMMARY

## Expected Files
src/app/page.tsx(수정 — 기존 create-next-app 스타터 제거)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
create-next-app 기본 스타터(Next.js 로고 Image, 'To get started, edit the page.tsx file' 문구, Vercel Deploy/Docs 버튼, next.svg/vercel.svg 참조)를 완전히 제거한다.<br>Section 순서: 1) Hero+통합검색 2) 국내 여행지 카드 6개(데이터 출처: DATA-DESTINATIONS) 3) 해외 여행지 카드 6개(DATA-DESTINATIONS) 4) 여행 동기 Chip 6개(DATA-DESTINATIONS 테마 필드) 5) 국가별 주의사항 카드 6개(DATA-SAFETY) 6) 최근 동행글 3개 또는 완성형 Empty State(API-MATES-CRUD) 7) free_traveler 소개 요약(DATA-REPRESENTATIVE).<br>최소 콘텐츠 수: 국내 6장, 해외 6장, 테마 6개, 안전정보 6장, 동행글 3장(또는 Empty State).<br>반응형 콘텐츠 밀도: Desktop 3~4열 Card Grid, Tablet 2열, Mobile 1열; Chip 목록은 가로 스크롤 유지.
<br>화면 상태(UI_CONTRACT 홈 상태 표): Loading = Section 3·4·6 Card Grid 스켈레톤; Success = 필터·검색 결과 1건 이상; Empty = Section 3·4·6 결과 0건이면 조건 완화 안내 + 전체 초기화 버튼, Section 7 동행글 0건이면 완성형 3요소 Empty State; Error = 안전정보 Drawer의 외교부 외부 링크 열기 실패 시 인라인 오류 + 재시도; Unauthorized = 없음(전체 공개 화면).

## Visual AC
데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다.

## Security/Privacy AC
항공·호텔·동행 입력값 없음(홈은 열람 전용); 안전정보 Drawer 외부 링크는 noopener,noreferrer.

## Test Cases
- 확인: create-next-app 기본 스타터(Next.js 로고 Image, 'To get started, edit the page.tsx file' 문구, Vercel Deploy/Docs 버튼, next.svg/vercel.svg 참조)를 완전히 제거한다.
- 확인: Section 순서: 1) Hero+통합검색 2) 국내 여행지 카드 6개(데이터 출처: DATA-DESTINATIONS) 3) 해외 여행지 카드 6개(DATA-DESTINATIONS) 4) 여행 동기 Chip 6개(DATA-DESTINATIONS 테마 필드) 5) 국가별 주의사항 카드 6개(DATA-SAFETY) 6) 최근 동행글 3개 또는 완성형 Empty State(API-MATES-CRUD) 7) free_traveler 소개 요약(DATA-REPRESENTATIVE).
- 확인: 최소 콘텐츠 수: 국내 6장, 해외 6장, 테마 6개, 안전정보 6장, 동행글 3장(또는 Empty State).
- 확인: 반응형 콘텐츠 밀도: Desktop 3~4열 Card Grid, Tablet 2열, Mobile 1열.
- 확인: Chip 목록은 가로 스크롤 유지.
- 시각 확인: 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다.
- 확인: 화면 상태(UI_CONTRACT 홈 상태 표): Loading = Section 3·4·6 Card Grid 스켈레톤; Success = 필터·검색 결과 1건 이상; Empty = Section 3·4·6 결과 0건이면 조건 완화 안내 + 전체 초기화 버튼, Section 7 동행글 0건이면 완성형 3요소 Empty State; Error = 안전정보 Drawer의 외교부 외부 링크 열기 실패 시 인라인 오류 + 재시도; Unauthorized = 없음(전체 공개 화면).

## Verify
E2E-PUBLIC-SMOKE; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK

## Definition of Done
- [ ] Expected Files에 나열된 파일이 정확히 그 파일들만 생성·수정되어 있다(그 밖의 파일 변경 없음).
- [ ] Functional AC / Visual AC / Security·Privacy AC 항목이 모두 충족된다.
- [ ] Depends On에 나열된 모든 Task가 먼저 완료되어 있다.
- [ ] Verify에 명시된 테스트·점검이 통과한다(Test Cases 절 기준).
- [ ] Forbidden 항목에 해당하는 코드·문구·파일이 없다.
- [ ] `create-next-app` 기본 스타터 마크업이 완전히 제거되어 있다.

## Forbidden
- Expected Files에 명시되지 않은 파일을 생성·수정하지 않는다.
- Airbnb 상표 요소(로고, Rausch 계열 색상 `#ff385c` 등, Cereal 폰트, "Guest favorite" 배지 등)를 사용하지 않는다.
- 예약하기·결제하기·가격비교·재고확인 등 구매/예약/결제 성격의 UI·API를 추가하지 않는다.
- 별점·리뷰 점수·좋아요 수·실시간 항공권/호텔 가격 배지를 추가하지 않는다.
- Lorem ipsum·'준비 중'·'정보 확인 필요' 등 미완성 Placeholder 문구와 내용 없는 Card를 사용하지 않는다.
- 이 Task 범위에서 구현 코드를 실제로 커밋하거나 Branch/PR/Issue를 생성하지 않는다(본 파일은 Task 정의 문서다).
- 하위 Component 파일을 새로 생성하지 않는다 — Depends On에 나열된 기존 Component/Data/API를 import·조립하는 것만 이 Task의 범위다(규칙 6).
- `create-next-app` 기본 스타터 잔재(Next.js 로고 Image, "To get started, edit the page.tsx file" 문구, Vercel Deploy/Docs 버튼, next.svg/vercel.svg 참조)를 남기지 않는다.
