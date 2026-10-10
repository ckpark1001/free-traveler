# CMP-SCR001-DESTINATION-GRID

국내·해외 여행지 Card Grid + 필터

## Context
국내·해외 여행지 Card Grid + 필터. 홈(/) 화면 안에서 쓰이는 개별 UI 영역이며, Page Owner Task가 이 Component를 조립해 최종 화면을 완성한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-005, REQ-FUNC-010, REQ-NF-004

## Screen / Route / Page Entry
Screen: **SCR-001** (홈(/))  
Route: `/`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
`design-reference/UI_CONTRACT.md` — 홈(/)의 해당 Component/상태 정의; `design-reference/D-001/DESIGN.md` §2~§6(Color/Typography/Spacing/Radius/Shadow 토큰), §7~§14(Header·Footer, Search·Filter, Card, Form·Tabs, Drawer·Modal, Alert·Toast, Loading·Empty·Error).

## Depends On
DATA-DESTINATIONS, SHARED-DESIGN-TOKENS

## Expected Files
src/components/home/destination-card-grid.tsx(신규); src/components/home/theme-chip-row.tsx(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
국내 6장/해외 6장 카드 그리드, 국가·도시·계절·테마(칩 6개)·기간 AND 필터, 필터 상태 URL query 반영·복원; 결과 0건 시 조건 완화 안내+전체 초기화 버튼.

## Visual AC
별점·리뷰·가격 배지 없음; Empty State는 데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다.

## Security/Privacy AC
해당 없음(공개 콘텐츠).

## Test Cases
- 확인: 국내 6장/해외 6장 카드 그리드, 국가·도시·계절·테마(칩 6개)·기간 AND 필터, 필터 상태 URL query 반영·복원.
- 확인: 결과 0건 시 조건 완화 안내+전체 초기화 버튼.
- 시각 확인: 별점·리뷰·가격 배지 없음.

## Verify
E2E-PUBLIC-SMOKE

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
