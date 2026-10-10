# DB-ACCESS

타입 세이프 Supabase 클라이언트·쿼리 헬퍼

## Context
타입 세이프 Supabase 클라이언트·쿼리 헬퍼. 실제 쓰기가 필요한 6개 테이블 범위 안에서의 데이터베이스 작업이다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-NF-014, REQ-NF-015

## Screen / Route / Page Entry
Screen: **-** (해당 없음(화면 비종속 Task))  
Route: `-`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
해당 없음(비-UI Task). 데이터/스키마 근거는 `app/docs/06_SRS_UIUX_REVISED.md` §4·§6(Appendix, 02_SRS_BASELINE.md 데이터 모델 참고) 및 `app/docs/PROJECT_SCOPE.md` §8(데이터 소스 매핑)을 따른다.

## Depends On
DB-SCHEMA-BASE, DB-RLS-BASE

## Expected Files
src/lib/supabase/server-client.ts(신규); src/lib/supabase/queries.ts(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
Server Component/Route Handler 전용 Supabase 클라이언트와 도메인별 쿼리 함수(mate_posts/mate_applications/blocks/reports/app_settings)를 제공한다.

## Visual AC
해당 없음(비-UI Task).

## Security/Privacy AC
Server Action 기반 CSRF 방어·SameSite 세션 쿠키를 전제로 하고, 모든 입력을 서버 측에서 검증·이스케이프한다(저장 XSS 차단).

## Test Cases
- server-client.ts가 클라이언트 번들에 포함되지 않는지 빌드 산출물로 확인한다.
- queries.ts의 각 함수가 파라미터 바인딩을 사용하고 문자열 concat으로 SQL을 구성하지 않는지 코드 리뷰로 확인한다.

## Verify
코드 리뷰; 수동 XSS 케이스 테스트

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
