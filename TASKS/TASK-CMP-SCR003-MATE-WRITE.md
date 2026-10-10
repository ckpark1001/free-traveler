# CMP-SCR003-MATE-WRITE

동행 모집글 작성(연락처 탐지·안전수칙 동의)

## Context
동행 모집글 작성(연락처 탐지·안전수칙 동의). 여행 준비(/travel-tools) 화면 안에서 쓰이는 개별 UI 영역이며, Page Owner Task가 이 Component를 조립해 최종 화면을 완성한다.

## Project Scope
`app/docs/PROJECT_SCOPE.md` 기준 **IMPLEMENT**로 확정된 범위다. 이 저장소는 Next.js App Router + TypeScript + Tailwind CSS(v4) + Supabase(Auth/PostgreSQL/RLS) 스택이며, 콘텐츠(여행지·안전정보·대표 소개)는 Supabase 테이블이 아니라 `src/data` 정적 파일로 관리한다(PROJECT_SCOPE §4, §8).

## Requirement Ref
REQ-FUNC-027, REQ-FUNC-031, REQ-FUNC-032, REQ-FUNC-080

## Screen / Route / Page Entry
Screen: **SCR-003** (여행 준비(/travel-tools))  
Route: `/travel-tools`  
Page Entry: 해당 없음(Page Owner가 아님 — 규칙 16: 이 Task는 어떤 Page Entry도 소유하지 않는다)

## Design Ref
`design-reference/UI_CONTRACT.md` — 여행 준비(/travel-tools)의 해당 Component/상태 정의; `design-reference/D-001/DESIGN.md` §2~§6(Color/Typography/Spacing/Radius/Shadow 토큰), §7~§14(Header·Footer, Search·Filter, Card, Form·Tabs, Drawer·Modal, Alert·Toast, Loading·Empty·Error).

## Depends On
API-MATES-CRUD, CMP-SCR005-AUTH

## Expected Files
src/components/travel-tools/mate-write-form.tsx(신규); src/components/travel-tools/auth-required-notice.tsx(신규)

**이 목록 밖의 파일은 만들거나 수정하지 않는다.**

## Functional AC
제목·국가·지역·시작일·종료일·모집인원·선호조건·여행스타일·설명·안전수칙 동의 필드; 전화번호·이메일·메신저ID 패턴 탐지 시 제출 차단+수정 안내; 비로그인/성인 미확인 시 `/account` 로그인 유도.

## Visual AC
데이터 0건 영역은 Lorem ipsum·'준비 중'·'정보 확인 필요'·내용 없는 Card를 두지 않는다; 안내 문장 + 이용 방법 + 실행 가능한 CTA를 갖춘 완성형 Empty State로 대체한다.

## Security/Privacy AC
연락처 탐지 실패(오탐 포함)를 사용자에게 명확히 안내하고 제출을 차단한다.

## Test Cases
- 전화번호 패턴(예: 010-1234-5678)을 본문에 포함하면 제출이 차단되고 수정 안내가 표시되는지 확인한다(UNIT-CONTACT-DETECTION).
- 이메일·메신저 ID 패턴도 동일하게 차단되는지 확인한다.
- 비로그인 상태에서 작성을 시도하면 `/account` 로그인 안내로 전환되는지 확인한다.
- 안전수칙 동의 체크 없이는 제출 버튼이 비활성화되는지 확인한다.

## Verify
UNIT-CONTACT-DETECTION; E2E-TRAVEL-TOOLS

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
- 전화번호·이메일·메신저 ID 등 공개 연락처가 포함된 모집글의 저장을 허용하지 않는다.
