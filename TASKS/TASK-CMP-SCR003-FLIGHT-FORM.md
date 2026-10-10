# CMP-SCR003-FLIGHT-FORM

항공 조건 입력·요약·외부 이동

## Context
항공 조건 입력·요약·외부 이동. 여행 준비(/travel-tools) 화면 안에서 쓰이는 개별 UI 영역이며, Page Owner Task가 이 Component를 조립해 최종 화면을 완성한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-011, REQ-FUNC-012, REQ-FUNC-013, REQ-FUNC-014, REQ-FUNC-015, REQ-FUNC-016, REQ-FUNC-017, REQ-FUNC-018, REQ-NF-017

## Screen / Route / Page Entry
Screen: **SCR-003** (여행 준비(/travel-tools))  
Route: `/travel-tools`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
`design-reference/UI_CONTRACT.md` — 여행 준비(/travel-tools)의 해당 Component/상태 정의; `design-reference/D-001/DESIGN.md` §2~§6(Color/Typography/Spacing/Radius/Shadow 토큰), §7~§14(Header·Footer, Search·Filter, Card, Form·Tabs, Drawer·Modal, Alert·Toast, Loading·Empty·Error).

## Depends On
SHARED-OUTBOUND-LINK-UTIL

## Expected Files
src/components/travel-tools/flight-form.tsx(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
국가·지역·출발일·귀국일 4필드(국가 변경 시 지역 초기화), 과거일·역전일 차단, 유효 입력 후 요약+비전달 고지, '항공편 보러 가기' 새 탭 이동. 국가·지역·날짜를 서버 DB·서버 로그·분석 이벤트·외부 URL 쿼리에 저장·전달하지 않는다(CON-01/02).

## Visual AC
비전달 고지 배너는 폼과 요약 단계에 상시 노출.

## Security/Privacy AC
원시 입력값이 네트워크 요청·DB·로그에 0건 포함되어야 한다.

## Test Cases
- 국가·지역·출발일·귀국일을 유효하게 입력하면 요약 단계가 표시되는지 확인한다.
- 출발일이 과거이거나 귀국일이 출발일보다 빠르면 제출이 차단되고 오류가 표시되는지 확인한다(UNIT-TRAVEL-DATES).
- 국가를 변경하면 이전에 선택된 지역 값이 초기화되는지 확인한다.
- '항공편 보러 가기' 클릭 시 새 탭이 열리고 URL에 목적지·날짜 query가 전혀 없는지 확인한다.
- 브라우저 네트워크 탭에서 항공 입력값이 어떤 요청에도 포함되지 않는지 확인한다.

## Verify
UNIT-TRAVEL-DATES; E2E-TRAVEL-TOOLS

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
- 국가·지역·날짜 등 입력값을 서버 DB, 서버 로그, 분석 이벤트, 외부 URL 쿼리 파라미터 어디에도 전달·저장하지 않는다(CON-01/02).
