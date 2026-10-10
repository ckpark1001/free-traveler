# SHARED-FAVORITES-LOCALSTORAGE

여행지 즐겨찾기(localStorage)

## Context
여행지 즐겨찾기(localStorage). 5개 Screen이 공통으로 재사용하는 인프라/유틸리티다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-068

## Screen / Route / Page Entry
Screen: **-** (해당 없음(화면 비종속 Task))  
Route: `-`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
`design-reference/D-001/DESIGN.md` 전문(토큰·Header/Footer·공통 오류 상태 규칙); `design-reference/UI_CONTRACT.md` 공통 규칙 절.

## Depends On
-

## Expected Files
src/lib/favorites.ts(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
localStorage에 즐겨찾기 id Set을 저장한다(서버 저장 없음); 중복 추가를 방지하는 add/remove/has/list API를 제공한다.

## Visual AC
해당 없음(비-UI Task, 유틸리티).

## Security/Privacy AC
브라우저 로컬 저장소만 사용, 서버 전송 없음.

## Test Cases
- 확인: localStorage에 즐겨찾기 id Set을 저장한다(서버 저장 없음).
- 확인: 중복 추가를 방지하는 add/remove/has/list API를 제공한다.

## Verify
수동 QA(localStorage 확인)

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
