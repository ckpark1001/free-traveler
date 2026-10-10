# PAGE-SCR004

동행 찾기(/mates) Page Owner

## Context
동행 찾기(/mates) Page Owner. `/mates` Route의 Page Entry를 조립하는 Page Owner Task로, 하위 Component/Data/API Task가 이미 만든 결과물을 가져와 화면 하나로 완성하는 역할만 수행한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-030, REQ-FUNC-033, REQ-FUNC-034, REQ-FUNC-039, REQ-FUNC-040

## Screen / Route / Page Entry
Screen: **SCR-004** (동행 찾기(/mates))  
Route: `/mates`  
Page Entry: `src/app/mates/page.tsx`

## Design Ref
`design-reference/UI_CONTRACT.md` — 동행 찾기(/mates) 영역 순서·상태·Desktop·Mobile 규칙 전문; `design-reference/D-001/DESIGN.md` §15-5(Screen Inventory), §16(Placeholder/Empty State 규칙), §17(Do/Do Not); `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Depends On
SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR004-FILTER-LIST, CMP-SCR004-DETAIL-PANEL, CMP-SCR004-APPLICATION, CMP-SCR004-REPORT-BLOCK

## Expected Files
src/app/mates/page.tsx(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
Section 순서: 1) Intro+작성 CTA 2) Filter·결과 요약(CMP-SCR004-FILTER-LIST) 3) 동행 목록(API-MATES-CRUD, 최소 3장 우선 노출) 4) 상세(CMP-SCR004-DETAIL-PANEL, CMP-SCR004-APPLICATION) 5) 신청 방법 3단계 6) 안전·신고·차단 안내와 CTA(CMP-SCR004-REPORT-BLOCK).<br>최소 콘텐츠 수: 목록 카드 3장 이상(0건 시 Empty State), 신청 방법 3단계.<br>반응형 콘텐츠 밀도: Desktop 좌 목록(40%)/우 상세(60%) 좌우 분할 동시 노출, Mobile 목록 1열→탭 시 상세 전체화면 전환.
<br>화면 상태(UI_CONTRACT 동행 찾기 상태 표): Loading = 목록 스켈레톤과 상세 패널 스켈레톤; Success = 목록·상세 정상 표시, 참가 요청/신고/차단 완료 Toast; Empty = 검색 결과 0건이면 조건 초기화 + 동행글 작성 CTA + 이용 방법 요약(완성형 3요소), 종료일 경과 글은 목록에서 자동 제외; Error = 상세 로드 실패, 참가 요청/신고/차단 제출 실패 시 인라인 오류 + 재시도; Unauthorized = 글쓰기·참가 요청 시도 시 비로그인/성인 미확인이면 안내 배너 + /account 로그인 유도.

## Visual AC
데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다.

## Security/Privacy AC
모집글·상세 어디에도 전화번호·이메일·메신저ID 노출 금지; 차단 사용자 간 상호 콘텐츠 비노출.

## Test Cases
- 확인: Section 순서: 1) Intro+작성 CTA 2) Filter·결과 요약(CMP-SCR004-FILTER-LIST) 3) 동행 목록(API-MATES-CRUD, 최소 3장 우선 노출) 4) 상세(CMP-SCR004-DETAIL-PANEL, CMP-SCR004-APPLICATION) 5) 신청 방법 3단계 6) 안전·신고·차단 안내와 CTA(CMP-SCR004-REPORT-BLOCK).
- 확인: 최소 콘텐츠 수: 목록 카드 3장 이상(0건 시 Empty State), 신청 방법 3단계.
- 확인: 반응형 콘텐츠 밀도: Desktop 좌 목록(40%)/우 상세(60%) 좌우 분할 동시 노출, Mobile 목록 1열→탭 시 상세 전체화면 전환.
- 시각 확인: 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다.
- 확인: 화면 상태(UI_CONTRACT 동행 찾기 상태 표): Loading = 목록 스켈레톤과 상세 패널 스켈레톤; Success = 목록·상세 정상 표시, 참가 요청/신고/차단 완료 Toast; Empty = 검색 결과 0건이면 조건 초기화 + 동행글 작성 CTA + 이용 방법 요약(완성형 3요소), 종료일 경과 글은 목록에서 자동 제외; Error = 상세 로드 실패, 참가 요청/신고/차단 제출 실패 시 인라인 오류 + 재시도; Unauthorized = 글쓰기·참가 요청 시도 시 비로그인/성인 미확인이면 안내 배너 + /account 로그인 유도.

## Verify
E2E-MATE-AUTH; UNIT-MATE-STATE; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK

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
