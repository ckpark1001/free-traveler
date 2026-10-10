# DATA-DESTINATIONS

국내·해외 여행지 정적 데이터 스키마·시드

## Context
국내·해외 여행지 정적 데이터 스키마·시드. Supabase 대신 `src/data` 정적 파일로 관리하기로 확정된 콘텐츠 도메인이다(`app/docs/PROJECT_SCOPE.md` §8).

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-004, REQ-FUNC-008, REQ-FUNC-063, REQ-NF-026

## Screen / Route / Page Entry
Screen: **-** (해당 없음(화면 비종속 Task))  
Route: `-`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
해당 없음(비-UI Task). 데이터/스키마 근거는 `app/docs/06_SRS_UIUX_REVISED.md` §4·§6(Appendix, 02_SRS_BASELINE.md 데이터 모델 참고) 및 `app/docs/PROJECT_SCOPE.md` §8(데이터 소스 매핑)을 따른다.

## Depends On
-

## Expected Files
src/data/destinations.ts(신규); src/data/types/destination.ts(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
PRD 3-4 필수 11항목(소개 300자+, 명소 5+, 추천/비추천 시기, 1일·3일 일정, 예산, 교통, 음식 3+, 에티켓 3+, 안전연결, 출처, 수정일)을 TypeScript 타입으로 강제한다; DB 테이블이 아닌 src/data 정적 파일로 관리한다(Supabase 미사용).

## Visual AC
해당 없음(비-UI Task, 데이터 정의).

## Security/Privacy AC
개인정보 없음. 이미지는 URL+alt만 저장(출처·작가·라이선스 메타데이터는 REQ-FUNC-007 EXCLUDED).

## Test Cases
- 확인: PRD 3-4 필수 11항목(소개 300자+, 명소 5+, 추천/비추천 시기, 1일·3일 일정, 예산, 교통, 음식 3+, 에티켓 3+, 안전연결, 출처, 수정일)을 TypeScript 타입으로 강제한다.
- 확인: DB 테이블이 아닌 src/data 정적 파일로 관리한다(Supabase 미사용).

## Verify
수동 콘텐츠 체크리스트(국내 10+, 해외 15개국 30도시+)

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
