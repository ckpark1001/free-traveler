# DB-SEED-BASE

로컬/스테이징 시드 데이터

## Context
로컬/스테이징 시드 데이터. 실제 쓰기가 필요한 6개 테이블 범위 안에서의 데이터베이스 작업이다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8). 이 Task는 특정 REQ ID 1:1 대응이 아닌 기반/지원 성격이며, 근거는 Requirement Ref 열에 기술한 바와 같다.

## Requirement Ref
N/A(개발·QA 지원 — E2E-MATE-AUTH, TEST-RLS-BASIC 선행 조건)

## Screen / Route / Page Entry
Screen: **-** (해당 없음(화면 비종속 Task))  
Route: `-`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
해당 없음(비-UI Task). 데이터/스키마 근거는 `app/docs/06_SRS_UIUX_REVISED.md` §4·§6(Appendix, 02_SRS_BASELINE.md 데이터 모델 참고) 및 `app/docs/PROJECT_SCOPE.md` §8(데이터 소스 매핑)을 따른다.

## Depends On
DB-SCHEMA-BASE

## Expected Files
supabase/seed.sql(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
테스트용 profiles 2~3명, mate_posts 3건 이상, mate_applications/blocks/reports 샘플을 생성해 E2E·RLS 테스트가 재현 가능하게 한다.

## Visual AC
해당 없음(비-UI Task).

## Security/Privacy AC
실사용자 개인정보를 포함하지 않는다(테스트 전용 더미 데이터).

## Test Cases
- 시드 실행 후 mate_posts가 3건 이상 존재하는지 확인한다.
- 시드 데이터에 실제 식별 가능한 개인정보(실명, 실전화번호 등)가 없는지 확인한다.

## Verify
TEST-RLS-BASIC, E2E-MATE-AUTH 실행 성공 여부로 확인

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
