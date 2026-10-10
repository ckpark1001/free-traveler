# MANUAL-ACCESSIBILITY-CHECK

키보드·스크린리더 수동 점검

## Context
키보드·스크린리더 수동 점검. 코드 산출물이 없는 배포 전 수동 점검 절차다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-079, REQ-NF-023, REQ-NF-025

## Screen / Route / Page Entry
Screen: **ALL(SCR-001~005)** (ALL(SCR-001~005))  
Route: `-`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
해당 없음(비-UI Task). 데이터/스키마 근거는 `app/docs/06_SRS_UIUX_REVISED.md` §4·§6(Appendix, 02_SRS_BASELINE.md 데이터 모델 참고) 및 `app/docs/PROJECT_SCOPE.md` §8(데이터 소스 매핑)을 따른다.

## Depends On
PAGE-SCR001, PAGE-SCR002, PAGE-SCR003, PAGE-SCR004, PAGE-SCR005

## Expected Files
해당 없음(코드 산출물 없음 — 점검 결과만 기록)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
5개 Screen 핵심 흐름(검색, 폼 입력, 모달 닫기, 신고 제출)을 키보드만으로 완료하고 스크린리더로 주요 레이블을 확인한다.

## Visual AC
해당 없음.

## Security/Privacy AC
해당 없음.

## Test Cases
- 확인: 5개 Screen 핵심 흐름(검색, 폼 입력, 모달 닫기, 신고 제출)을 키보드만으로 완료하고 스크린리더로 주요 레이블을 확인한다.
- Verify 열에 명시된 방법(배포 전 1회 수동 실행, 결과를 릴리스 체크리스트에 기록)으로 배포 전 1회 이상 실행하고 결과를 기록한다.

## Verify
배포 전 1회 수동 실행, 결과를 릴리스 체크리스트에 기록

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
