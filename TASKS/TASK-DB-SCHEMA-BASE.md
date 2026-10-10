# DB-SCHEMA-BASE

Supabase 테이블 스키마 정의(최대 6개)

## Context
Supabase 테이블 스키마 정의(최대 6개). 실제 쓰기가 필요한 6개 테이블 범위 안에서의 데이터베이스 작업이다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-028, REQ-FUNC-035

## Screen / Route / Page Entry
Screen: **-** (해당 없음(화면 비종속 Task))  
Route: `-`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
해당 없음(비-UI Task). 데이터/스키마 근거는 `app/docs/06_SRS_UIUX_REVISED.md` §4·§6(Appendix, 02_SRS_BASELINE.md 데이터 모델 참고) 및 `app/docs/PROJECT_SCOPE.md` §8(데이터 소스 매핑)을 따른다.

## Depends On
-

## Expected Files
supabase/migrations/0001_schema_base.sql(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
Tables: `profiles`, `mate_posts`, `mate_applications`, `blocks`, `reports`, `app_settings` — 정확히 6개, 초과 금지; 여행지·안전·대표 도메인 테이블은 만들지 않는다(정적 데이터로 대체, DATA-* Task).

## Visual AC
해당 없음(비-UI Task).

## Security/Privacy AC
profiles은 정확한 생년월일을 저장하지 않고 is_adult(BOOLEAN)/adult_verified_at(TIMESTAMPTZ)만 저장한다(REQ-FUNC-028).

## Test Cases
- 마이그레이션 적용 후 정확히 6개 테이블(profiles, mate_posts, mate_applications, blocks, reports, app_settings)이 존재하는지 확인한다.
- profiles 테이블에 정확한 생년월일 컬럼이 없고 is_adult(BOOLEAN)/adult_verified_at(TIMESTAMPTZ)만 있는지 확인한다.
- 7번째 테이블(예: destination, country_safety)을 추가하는 변경은 리뷰에서 거부되는지 확인한다.

## Verify
코드 리뷰(스키마 확인)

## Definition of Done
- [ ] Expected Files에 나열된 파일이 정확히 그 파일들만 생성·수정되어 있다(그 밖의 파일 변경 없음).
- [ ] Functional AC / Visual AC / Security·Privacy AC 항목이 모두 충족된다.
- [ ] Depends On에 나열된 모든 Task가 먼저 완료되어 있다.
- [ ] Verify에 명시된 테스트·점검이 통과한다(Test Cases 절 기준).
- [ ] Forbidden 항목에 해당하는 코드·문구·파일이 없다.
- [ ] 정확히 6개 테이블만 존재하며 정적 데이터 도메인 테이블이 없다.

## Forbidden
- Expected Files에 명시되지 않은 파일을 생성·수정하지 않는다.
- Airbnb 상표 요소(로고, Rausch 계열 색상 `#ff385c` 등, Cereal 폰트, "Guest favorite" 배지 등)를 사용하지 않는다.
- 예약하기·결제하기·가격비교·재고확인 등 구매/예약/결제 성격의 UI·API를 추가하지 않는다.
- 별점·리뷰 점수·좋아요 수·실시간 항공권/호텔 가격 배지를 추가하지 않는다.
- Lorem ipsum·'준비 중'·'정보 확인 필요' 등 미완성 Placeholder 문구와 내용 없는 Card를 사용하지 않는다.
- 이 Task 범위에서 구현 코드를 실제로 커밋하거나 Branch/PR/Issue를 생성하지 않는다(본 파일은 Task 정의 문서다).
- 6개 테이블(profiles, mate_posts, mate_applications, blocks, reports, app_settings) 외의 테이블을 추가하지 않는다.
- 여행지(destination)·안전정보(country_safety)·대표(representative_profile) 도메인을 테이블로 만들지 않는다 — 이 도메인은 DATA-* 정적 데이터 Task로만 구현한다.
