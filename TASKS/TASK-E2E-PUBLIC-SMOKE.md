# E2E-PUBLIC-SMOKE

공개 열람 Smoke(Chromium)

## Context
공개 열람 Smoke(Chromium). Chromium 전용 Playwright Smoke 테스트다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-006, REQ-FUNC-047, REQ-FUNC-057

## Screen / Route / Page Entry
Screen: **SCR-001, SCR-002** (SCR-001, SCR-002)  
Route: `-`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
해당 없음(비-UI Task). 데이터/스키마 근거는 `app/docs/06_SRS_UIUX_REVISED.md` §4·§6(Appendix, 02_SRS_BASELINE.md 데이터 모델 참고) 및 `app/docs/PROJECT_SCOPE.md` §8(데이터 소스 매핑)을 따른다.

## Depends On
PAGE-SCR001, PAGE-SCR002

## Expected Files
tests/e2e/public-smoke.spec.ts(신규); playwright.config.ts(신규, Chromium 프로젝트만)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
SM-01(여행지 탐색·필터·상세·안전정보 이동), SM-08(안전정보 필수요소·stale 경고), SM-09(대표 소개 수치·추천 링크) 흐름을 하나의 Chromium 전용 Smoke 스펙으로 묶는다.

## Visual AC
해당 없음(테스트 코드).

## Security/Privacy AC
해당 없음.

## Test Cases
- SM-01: 홈에서 여행지 필터·검색 후 상세 Drawer를 열고 안전정보로 이동한다.
- SM-08: 안전정보 Drawer에서 8개 카테고리와 stale 경고가 표시되는지 확인한다.
- SM-09: 대표 소개 페이지의 50+/30+ 수치와 추천 여행지 링크가 정상 동작하는지 확인한다.

## Verify
CI에서 Chromium만 실행(Firefox/WebKit 프로젝트 추가 금지)

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
- Chromium 외 브라우저 프로젝트(Firefox/WebKit/Safari)를 Playwright 설정에 추가하지 않는다.
