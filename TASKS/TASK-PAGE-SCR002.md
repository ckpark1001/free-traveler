# PAGE-SCR002

대표 소개(/about) Page Owner

## Context
대표 소개(/about) Page Owner. `/about` Route의 Page Entry를 조립하는 Page Owner Task로, 하위 Component/Data/API Task가 이미 만든 결과물을 가져와 화면 하나로 완성하는 역할만 수행한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-057, REQ-FUNC-058, REQ-FUNC-059, REQ-FUNC-060, REQ-FUNC-062, REQ-FUNC-063

## Screen / Route / Page Entry
Screen: **SCR-002** (대표 소개(/about))  
Route: `/about`  
Page Entry: `src/app/about/page.tsx`

## Design Ref
`design-reference/UI_CONTRACT.md` — 대표 소개(/about) 영역 순서·상태·Desktop·Mobile 규칙 전문; `design-reference/D-001/DESIGN.md` §15-5(Screen Inventory), §16(Placeholder/Empty State 규칙), §17(Do/Do Not); `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Depends On
SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR002-HERO-STATS, CMP-SCR002-PHILOSOPHY, CMP-SCR002-TIMELINE, CMP-SCR002-COUNTRIES-GALLERY, CMP-SCR002-RECOMMENDED-CTA

## Expected Files
src/app/about/page.tsx(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
Section 순서: 1) Profile Hero(대표 이미지+한 문장 소개, DATA-REPRESENTATIVE) 2) 여행 지표(50+ Trips/30+ Countries/전문영역, DATA-REPRESENTATIVE) 3) 소개·철학(DATA-REPRESENTATIVE) 4) Timeline 6개 이상(DATA-REPRESENTATIVE) 5) 방문 국가 30개국 이상(DATA-REPRESENTATIVE) 6) 사진 Gallery 8장 이상(DATA-REPRESENTATIVE) 7) 기억에 남는 여행지 4개 + CTA(DATA-DESTINATIONS, DATA-REPRESENTATIVE).<br>최소 콘텐츠 수: Timeline 6개, 방문국가 30개국, Gallery 8장, 추천 여행지 4개.<br>반응형 콘텐츠 밀도: Desktop 좌우 분할(Hero/철학), Gallery Desktop 4열→Mobile 2열, 추천 Grid Desktop 4열→Mobile 1열.
<br>화면 상태(UI_CONTRACT 대표 소개 상태 표): Loading = Gallery 이미지 lazy load 중 블러 플레이스홀더; Success = 기본 상태(정적 데이터); Empty = 해당 없음(정적 콘텐츠는 항상 존재); Error = SNS/문의 외부 링크 열기 실패 시 인라인 안내; Unauthorized = 없음(전체 공개).

## Visual AC
데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다.

## Security/Privacy AC
이미지가 특정 서비스 보증인으로 오인되는 연출 금지; SNS/문의 링크는 허용 프로토콜만 렌더링.

## Test Cases
- 확인: Section 순서: 1) Profile Hero(대표 이미지+한 문장 소개, DATA-REPRESENTATIVE) 2) 여행 지표(50+ Trips/30+ Countries/전문영역, DATA-REPRESENTATIVE) 3) 소개·철학(DATA-REPRESENTATIVE) 4) Timeline 6개 이상(DATA-REPRESENTATIVE) 5) 방문 국가 30개국 이상(DATA-REPRESENTATIVE) 6) 사진 Gallery 8장 이상(DATA-REPRESENTATIVE) 7) 기억에 남는 여행지 4개 + CTA(DATA-DESTINATIONS, DATA-REPRESENTATIVE).
- 확인: 최소 콘텐츠 수: Timeline 6개, 방문국가 30개국, Gallery 8장, 추천 여행지 4개.
- 확인: 반응형 콘텐츠 밀도: Desktop 좌우 분할(Hero/철학), Gallery Desktop 4열→Mobile 2열, 추천 Grid Desktop 4열→Mobile 1열.
- 시각 확인: 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다.
- 확인: 화면 상태(UI_CONTRACT 대표 소개 상태 표): Loading = Gallery 이미지 lazy load 중 블러 플레이스홀더; Success = 기본 상태(정적 데이터); Empty = 해당 없음(정적 콘텐츠는 항상 존재); Error = SNS/문의 외부 링크 열기 실패 시 인라인 안내; Unauthorized = 없음(전체 공개).

## Verify
E2E-PUBLIC-SMOKE; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK

## Definition of Done
- [ ] Expected Files에 나열된 파일이 정확히 그 파일들만 생성·수정되어 있다(그 밖의 파일 변경 없음).
- [ ] Functional AC / Visual AC / Security·Privacy AC 항목이 모두 충족된다.
- [ ] Depends On에 나열된 모든 Task가 먼저 완료되어 있다.
- [ ] Verify에 명시된 테스트·점검이 통과한다(Test Cases 절 기준).
- [ ] Forbidden 항목에 해당하는 코드·문구·파일이 없다.

## Forbidden
- Expected Files에 명시되지 않은 파일을 생성·수정하지 않는다.
- Airbnb 상표 요소(로고, Rausch 계열 색상 `#ff385c` 등, Cereal 폰트, "Guest favorite" 배지 등)를 사용하지 않는다.
- 예약하기·결제하기·가격비교·재고확인 등 구매/예약/결제 성격의 UI·API를 추가하지 않는다.
- 별점·리뷰 점수·좋아요 수·실시간 항공권/호텔 가격 배지를 추가하지 않는다.
- Lorem ipsum·'준비 중'·'정보 확인 필요' 등 미완성 Placeholder 문구와 내용 없는 Card를 사용하지 않는다.
- 이 Task 범위에서 구현 코드를 실제로 커밋하거나 Branch/PR/Issue를 생성하지 않는다(본 파일은 Task 정의 문서다).
- 하위 Component 파일을 새로 생성하지 않는다 — Depends On에 나열된 기존 Component/Data/API를 import·조립하는 것만 이 Task의 범위다(규칙 6).
