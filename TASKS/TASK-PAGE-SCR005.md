# PAGE-SCR005

계정(/account) Page Owner

## Context
계정(/account) Page Owner. `/account` Route의 Page Entry를 조립하는 Page Owner Task로, 하위 Component/Data/API Task가 이미 만든 결과물을 가져와 화면 하나로 완성하는 역할만 수행한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-028, REQ-FUNC-029, REQ-FUNC-041, REQ-FUNC-066, REQ-FUNC-077

## Screen / Route / Page Entry
Screen: **SCR-005** (계정(/account))  
Route: `/account`  
Page Entry: `src/app/account/page.tsx`

## Design Ref
`design-reference/UI_CONTRACT.md` — 계정(/account) 영역 순서·상태·Desktop·Mobile 규칙 전문; `design-reference/D-001/DESIGN.md` §15-5(Screen Inventory), §16(Placeholder/Empty State 규칙), §17(Do/Do Not); `design-reference/SCREEN_ROUTE_CONTRACT.json`(Route/Page Entry 정본).

## Depends On
SHARED-LAYOUT-NAV-FOOTER, SHARED-SEO-METADATA, CMP-SCR005-AUTH, CMP-SCR005-PROFILE, CMP-SCR005-MY-ACTIVITY, CMP-SCR005-ADMIN-REPORTS, CMP-SCR005-ADMIN-OUTBOUND

## Expected Files
src/app/account/page.tsx(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
Guest·Member·Admin 중 현재 역할의 Section만 조립한다(역할에 없는 관리 영역은 렌더링하지 않음): 1) 현재 역할 Intro(무엇을 할 수 있는지) 2) 핵심 작업 — Guest=로그인/가입/재설정(CMP-SCR005-AUTH), Member=프로필+내 활동(CMP-SCR005-PROFILE, CMP-SCR005-MY-ACTIVITY), Admin=신고 큐+외부 URL 설정(CMP-SCR005-ADMIN-REPORTS, CMP-SCR005-ADMIN-OUTBOUND) 3) 도움말 또는 다음 행동(로그인 후 가능한 기능 안내 / 작성 CTA / 관리 범위 고지).<br>최소 콘텐츠 수: Member 내 활동 카드(내 글/요청/차단/즐겨찾기) 각 목록당 최소 1개 Empty 또는 실제 항목; Admin 카드 2개(신고 큐, 외부 URL) 이상.<br>반응형 콘텐츠 밀도: Desktop 좌측 세로 탭 Nav+우측 콘텐츠 분할, Mobile 상단 가로 스크롤 탭+세로 스택.
<br>화면 상태(UI_CONTRACT 계정 상태 표): Loading = 탭 전환 시 목록/폼 스켈레톤; Success = 로그인 완료·프로필 저장 완료·외부 URL 저장 완료 Toast; Empty = 내 글/참가 요청/차단/즐겨찾기 각 목록이 비면 개별 완성형 Empty State(안내 + 다음 행동 CTA); Error = 회원가입/로그인 실패, 프로필 저장 실패, 외부 URL 유효성 오류(HTTPS 외 스킴 거부) 시 인라인 오류; Unauthorized = Member 탭에 비로그인 접근 시 로그인 탭으로 리다이렉트, Admin 탭에 비관리자 접근 시 403 안내(홈 복귀 CTA 포함).

## Visual AC
데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다. Hero 아래로 스크롤 없이 다음 Section 일부가 보여야 하며 목적 없는 큰 빈 공간을 두지 않는다.

## Security/Privacy AC
Admin 영역은 서버 역할 검증 없이 클라이언트에서만 숨기지 않는다(RoleGate + API 403 이중 검증); 정확한 생년월일 미표시.

## Test Cases
- 확인: Guest·Member·Admin 중 현재 역할의 Section만 조립한다(역할에 없는 관리 영역은 렌더링하지 않음): 1) 현재 역할 Intro(무엇을 할 수 있는지) 2) 핵심 작업 — Guest=로그인/가입/재설정(CMP-SCR005-AUTH), Member=프로필+내 활동(CMP-SCR005-PROFILE, CMP-SCR005-MY-ACTIVITY), Admin=신고 큐+외부 URL 설정(CMP-SCR005-ADMIN-REPORTS, CMP-SCR005-ADMIN-OUTBOUND) 3) 도움말 또는 다음 행동(로그인 후 가능한 기능 안내 / 작성 CTA / 관리 범위 고지).
- 확인: 최소 콘텐츠 수: Member 내 활동 카드(내 글/요청/차단/즐겨찾기) 각 목록당 최소 1개 Empty 또는 실제 항목.
- 확인: Admin 카드 2개(신고 큐, 외부 URL) 이상.
- 확인: 반응형 콘텐츠 밀도: Desktop 좌측 세로 탭 Nav+우측 콘텐츠 분할, Mobile 상단 가로 스크롤 탭+세로 스택.
- 시각 확인: 데이터가 없는 모든 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card 없이, 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다.
- 확인: 화면 상태(UI_CONTRACT 계정 상태 표): Loading = 탭 전환 시 목록/폼 스켈레톤; Success = 로그인 완료·프로필 저장 완료·외부 URL 저장 완료 Toast; Empty = 내 글/참가 요청/차단/즐겨찾기 각 목록이 비면 개별 완성형 Empty State(안내 + 다음 행동 CTA); Error = 회원가입/로그인 실패, 프로필 저장 실패, 외부 URL 유효성 오류(HTTPS 외 스킴 거부) 시 인라인 오류; Unauthorized = Member 탭에 비로그인 접근 시 로그인 탭으로 리다이렉트, Admin 탭에 비관리자 접근 시 403 안내(홈 복귀 CTA 포함).

## Verify
E2E-MATE-AUTH; MANUAL-ACCESSIBILITY-CHECK; MANUAL-RESPONSIVE-CHECK

## Definition of Done
- [ ] Expected Files에 나열된 파일이 정확히 그 파일들만 생성·수정되어 있다(그 밖의 파일 변경 없음).
- [ ] Functional AC / Visual AC / Security·Privacy AC 항목이 모두 충족된다.
- [ ] Depends On에 나열된 모든 Task가 먼저 완료되어 있다.
- [ ] Verify에 명시된 테스트·점검이 통과한다(Test Cases 절 기준).
- [ ] Forbidden 항목에 해당하는 코드·문구·파일이 없다.
- [ ] 현재 역할(Guest/Member/Admin)에 해당하는 영역만 렌더링되고, 역할에 없는 관리 영역은 렌더링되지 않는다.

## Forbidden
- Expected Files에 명시되지 않은 파일을 생성·수정하지 않는다.
- Airbnb 상표 요소(로고, Rausch 계열 색상 `#ff385c` 등, Cereal 폰트, "Guest favorite" 배지 등)를 사용하지 않는다.
- 예약하기·결제하기·가격비교·재고확인 등 구매/예약/결제 성격의 UI·API를 추가하지 않는다.
- 별점·리뷰 점수·좋아요 수·실시간 항공권/호텔 가격 배지를 추가하지 않는다.
- Lorem ipsum·'준비 중'·'정보 확인 필요' 등 미완성 Placeholder 문구와 내용 없는 Card를 사용하지 않는다.
- 이 Task 범위에서 구현 코드를 실제로 커밋하거나 Branch/PR/Issue를 생성하지 않는다(본 파일은 Task 정의 문서다).
- 하위 Component 파일을 새로 생성하지 않는다 — Depends On에 나열된 기존 Component/Data/API를 import·조립하는 것만 이 Task의 범위다(규칙 6).
