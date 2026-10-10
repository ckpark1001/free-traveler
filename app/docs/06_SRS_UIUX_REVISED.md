# Software Requirements Specification (SRS) — Free Traveler — UI/UX Revised

- **Document ID:** SRS-TRAVEL-001-UIUX
- **Revision:** 2.0 (UI/UX Screen·Route 연결 개정판)
- **기반 문서:** `02_SRS_BASELINE.md`(SRS-TRAVEL-001 Rev 1.0, 변경 없이 유지되는 원본), `PROJECT_SCOPE.md`(SCOPE-TRAVEL-001), `03_UI_COVERAGE_ANALYSIS.md`(UICOV-TRAVEL-001), `05_UIUX_APPROVED.md`(UIUXAPR-TRAVEL-001)
- **작성일:** 2026-09-15
- **상태:** Implementation Baseline — UI/UX Revised

| 항목 | 내용 |
|---|---|
| 프로젝트명 | Free Traveler 여행 탐색·외부 연결·동행·안전정보 플랫폼 |
| 제품 대표 | `free_traveler` |
| 기본 언어 | 한국어 (`ko-KR`) |
| 기본 플랫폼 | 반응형 웹, Mobile First |
| Owner | Product & Engineering |

## 개정 요약(Rev 1.0 → Rev 2.0)

이 개정판은 요구사항을 추가·삭제·변경하지 않는다. `02_SRS_BASELINE.md`의 REQ-FUNC-001~080(80개)과 REQ-NF-001~034(34개), 총 114개는 원문 그대로 §4에 재수록되어 있다. 변경된 것은 다음 두 가지뿐이다.

1. **§3.5 Page and Route Inventory**를 승인된 5개 Screen(SCR-001~SCR-005) 구조로 교체한다. 기존에 나열되던 개별 공개 Route(`/destinations/*`, `/flights`, `/hotels`, `/safety/*`, `/auth/*`, `/my/*`, `/admin/*`)는 삭제되는 것이 아니라 5개 Screen의 탭·패널·모달·Drawer로 통합된다(상세 대응표는 `05_UIUX_APPROVED.md` §2).
2. **§4의 모든 요구사항 행에 `Scope`(PROJECT_SCOPE 분류)와 `Screen`(배치 Screen) 열을 추가**한다. Requirement/Priority/Source/Acceptance Criteria 원문은 변경하지 않는다.

> 현재 저장소(`app/src/app`)에는 `create-next-app` 기본 스타터만 존재하며 어떤 요구사항도 코드로 구현되지 않았다. 본 문서의 `Scope=IMPLEMENT` 표기는 "구현 대상으로 확정됨"을 의미할 뿐 "구현 완료"를 의미하지 않는다. 실제 진행 상태는 `UIUX_TRACEABILITY.md`의 Implementation Status/Task/Test/Status 열에서만 추적한다.

---

## 1. Introduction

### 1.1 Purpose

`02_SRS_BASELINE.md` §1.1과 동일하다. Free Traveler는 다음 여섯 가지 사용자 가치를 제공한다: (1) 국내·해외 유명 여행지의 정형화된 심층 정보, (2) 국가·지역·여행 기간 입력과 요약 확인 후 외부 항공 사이트 이동, (3) 국가·지역·숙박 기간 입력과 요약 확인 후 외부 호텔 사이트 이동, (4) 만 19세 이상 회원을 위한 동행 모집·참가 요청·신고·차단, (5) 공식 출처와 최종 확인일을 포함한 국가별 여행 주의사항, (6) 여행 50회 이상·30개국 이상을 경험한 `free_traveler` 대표 소개.

### 1.2 Scope, Constraints, Assumptions, Contingency Plans, Definitions, References

`02_SRS_BASELINE.md` §1.2~§1.4(In-Scope IS-01~11, Out-of-Scope OS-01~11, Constraints CON-01~14, Assumptions ASM-01~06, Contingency Plans CP-01~06, 용어 정의, 참고문헌)는 이번 개정으로 변경되지 않는다. 원문을 그대로 유지하며 본 문서에서 재수록하지 않는다.

---

## 2. Stakeholders and Permissions

`02_SRS_BASELINE.md` §2(Stakeholders, Role Permission Matrix)는 변경 없이 유지된다. `PROJECT_SCOPE.md` §2가 이를 Guest/Member/Admin 3단계로 단순화했다는 점만 참고하며, 이는 이번 UI/UX 개정과 무관하게 이미 `PROJECT_SCOPE.md`에서 확정된 사항이다.

---

## 3. System Context and Interfaces

### 3.1~3.4, 3.6~3.7

`02_SRS_BASELINE.md` §3.1(Architecture)~§3.4(Client Applications), §3.6(Use Cases), §3.7(Core Interaction Sequences)은 변경 없이 유지된다.

### 3.5 Page and Route Inventory (개정)

기존 §3.5의 16행 개별 Route 표는 아래 승인된 5개 Screen 구조로 대체한다. 전체 계약은 `05_UIUX_APPROVED.md`와 `../design-reference/SCREEN_ROUTE_CONTRACT.json`을 정본으로 한다.

| Screen ID | Route | Page Entry | Access | 분류 |
|---|---|---|---|---|
| SCR-001 | `/` | `src/app/page.tsx` | Public | 핵심 |
| SCR-002 | `/about` | `src/app/about/page.tsx` | Public | 핵심 |
| SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | Public(동행 탭 작성은 Adult Member) | 핵심 |
| SCR-004 | `/mates` | `src/app/mates/page.tsx` | Public(참가 요청은 Adult Member) | 핵심 |
| SCR-005 | `/account` | `src/app/account/page.tsx` | Public/Member/Admin(탭별 역할 게이팅) | 보조 |

기술 Route(Screen으로 집계하지 않음):

| 유형 | Route | 파일 |
|---|---|---|
| Supabase 인증 콜백 | `/auth/callback` | `src/app/auth/callback/route.ts` |
| API Route | `/api/*` | `src/app/api/**/route.ts` |
| Not Found | `*` | `src/app/not-found.tsx` |

기존 Route(구) → 신규 Screen 대응은 `05_UIUX_APPROVED.md` §2 표를 정본으로 한다.

---

## 4. Specific Requirements

> Requirement/P(Priority)/Source/Acceptance Criteria 열은 `02_SRS_BASELINE.md` 원문과 동일하다. `Scope`는 `PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 분류, `Screen`은 `03_UI_COVERAGE_ANALYSIS.md`의 배치 Screen이다. 어떤 행도 삭제되지 않았다.

### 4.1 Functional Requirements

#### 4.1.1 F1. Destination Guide

| ID | Requirement | P | Source | Acceptance Criteria | Scope | Screen |
|---|---|:---:|---|---|---|---|
| REQ-FUNC-001 | 시스템은 국내·해외 여행지 목록을 구분해 제공한다. | M | Story 1 | 탭 변경 시 해당 구분의 게시 여행지만 표시되고 오분류가 없다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-002 | 시스템은 국가·도시·계절·테마·권장 기간 필터를 제공한다. | M | AC-D02 | 복수 필터는 AND 조건으로 적용되고 p95 1초 이내 결과가 표시된다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-003 | 시스템은 키워드로 여행지명·국가명·테마를 검색한다. | M | Story 1 | 한글 부분 일치 검색과 결과 없음 상태가 동작한다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-004 | 시스템은 여행지 상세에 소개·명소 5개 이상·추천 시기·1일/3일 일정·예산·교통·음식 3개 이상·에티켓·출처·수정일을 표시한다. | M | PRD 3-4 | 필수 필드가 하나라도 없으면 게시 상태로 변경할 수 없다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-005 | 시스템은 필터 결과가 없으면 조건 완화 안내와 전체 초기화 버튼을 제공한다. | M | AC-D04 | 빈 결과 300ms 이내 안내가 표시되고 초기화 후 전체 목록이 복원된다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-006 | 시스템은 해외 여행지 상세에서 해당 국가의 안전 페이지를 연결한다. | M | AC-D05 | destination.country_code와 safety.country_code가 일치한다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-007 | 시스템은 대표 이미지에 대체텍스트·출처·작가·라이선스를 연결한다. | M | PRD 6-4 | 공개 이미지의 메타데이터 충족률이 100%다. | EXCLUDED | - |
| REQ-FUNC-008 | 시스템은 MVP 게시 기준 국내 10개 이상, 해외 15개국 30개 도시 이상을 검증한다. | M | PRD 3-3 | 출시 게이트에서 수량 미달 시 실패한다. | IMPLEMENT | - |
| REQ-FUNC-009 | 시스템은 같은 국가·테마의 관련 여행지를 상세 하단에 최대 6개 표시한다. | S | Discover | 비공개·현재 여행지는 추천에서 제외된다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-010 | 시스템은 목록 필터 상태를 URL query에 반영해 새로고침·공유 시 복원한다. | S | Discover | 허용 필터만 직렬화되고 잘못된 값은 무시된다. | IMPLEMENT | SCR-001 |

#### 4.1.2 F2. Flight Link-out

| ID | Requirement | P | Source | Acceptance Criteria | Scope | Screen |
|---|---|:---:|---|---|---|---|
| REQ-FUNC-011 | 시스템은 항공 폼에 목적 국가, 지역·도시, 출발일, 귀국일을 필수 입력으로 제공한다. | M | Story 2 | 네 필드가 라벨·도움말·오류 영역과 함께 표시된다. | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-012 | 시스템은 선택 국가에 속하는 지역·도시만 선택 가능하게 한다. | M | AC-F01 | 국가 변경 시 유효하지 않은 기존 지역값을 초기화한다. | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-013 | 시스템은 출발일이 오늘 이전이거나 귀국일이 출발일보다 빠르면 진행을 차단한다. | M | AC-F02 | 경계값 테스트에서 잘못된 날짜 제출이 0건이다. | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-014 | 시스템은 유효한 입력 후 국가·지역·출발일·귀국일 요약 단계를 표시한다. | M | AC-F03 | 수정 버튼으로 폼에 돌아가도 값이 브라우저 세션 동안 유지된다. | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-015 | 시스템은 폼과 요약에 "입력값은 외부 사이트로 전달되지 않습니다"를 표시한다. | M | CON-02 | 외부 이동 전 고지가 시각적·프로그램적으로 노출된다. | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-016 | 시스템은 외부 이동 시 설정된 항공 일반 URL을 새 탭으로 열고 `noopener,noreferrer`를 적용한다. | M | AC-F04 | 목적지·날짜 query가 없고 opener 접근이 불가하다. | IMPLEMENT | SCR-003(항공 탭) |
| REQ-FUNC-017 | 시스템은 항공 입력값을 서버 DB, 서버 로그, 분석 이벤트에 저장하지 않는다. | M | AC-F06 | 네트워크·DB·로그 검사에서 원시 입력값이 0건이다. | IMPLEMENT | - |
| REQ-FUNC-018 | 시스템은 외부 URL이 없거나 허용목록 밖이면 이동을 차단하고 오류와 재시도를 제공한다. | M | AC-F05 | 동일 탭 손실 없이 오류가 표시되고 운영 로그가 생성된다. | IMPLEMENT | SCR-003(항공 탭) |

#### 4.1.3 F3. Hotel Link-out

| ID | Requirement | P | Source | Acceptance Criteria | Scope | Screen |
|---|---|:---:|---|---|---|---|
| REQ-FUNC-019 | 시스템은 호텔 폼에 숙박 국가, 지역·도시, 체크인, 체크아웃을 필수 입력으로 제공한다. | M | Story 3 | 네 필드가 라벨·도움말·오류 영역과 함께 표시된다. | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-020 | 시스템은 선택 국가에 속하는 지역·도시만 선택 가능하게 한다. | M | Story 3 | 국가 변경 시 유효하지 않은 지역값이 초기화된다. | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-021 | 시스템은 체크인이 오늘 이전이거나 체크아웃이 체크인과 같거나 빠르면 진행을 차단한다. | M | AC-H02 | 잘못된 날짜 제출이 0건이다. | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-022 | 시스템은 유효한 입력 후 국가·지역·체크인·체크아웃 요약을 표시한다. | M | AC-H03 | 요약값이 폼 입력과 정확히 일치한다. | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-023 | 시스템은 폼과 요약에 입력값 비전달 안내를 표시한다. | M | AC-H03 | 외부 이동 전 고지가 누락되지 않는다. | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-024 | 시스템은 설정된 호텔 일반 URL을 새 탭으로 열고 `noopener,noreferrer`를 적용한다. | M | AC-H04 | 외부 URL에 입력 query가 없고 성공률 99% 이상이다. | IMPLEMENT | SCR-003(숙소 탭) |
| REQ-FUNC-025 | 시스템은 호텔 입력값을 서버 DB, 서버 로그, 분석 이벤트에 저장하지 않는다. | M | AC-H05 | 네트워크·DB·로그 검사에서 원시 입력값이 0건이다. | IMPLEMENT | - |
| REQ-FUNC-026 | 시스템은 호텔 URL 오류 시 이동을 차단하고 재시도와 운영 오류 로그를 제공한다. | M | CP-01 | 현재 페이지 입력은 유지되고 오류가 표시된다. | IMPLEMENT | SCR-003(숙소 탭) |

#### 4.1.4 F4. Travel Mate

| ID | Requirement | P | Source | Acceptance Criteria | Scope | Screen |
|---|---|:---:|---|---|---|---|
| REQ-FUNC-027 | 시스템은 동행 쓰기 작업에 이메일 인증 세션을 요구한다. | M | AC-M01 | 비회원 POST는 401 또는 로그인 리다이렉트로 차단된다. | IMPLEMENT | SCR-003(동행 작성 탭), SCR-004 |
| REQ-FUNC-028 | 시스템은 동행 글·요청 전에 만 19세 이상 확인 상태를 요구하며 정확한 생년월일은 저장하지 않는다. | M | CON-04 | `is_adult=true`, `adult_verified_at`만 영속화한다. | IMPLEMENT | SCR-005(로그인/인증 탭) |
| REQ-FUNC-029 | 시스템은 동행 프로필에 닉네임, 연령대, 선택형 성별, 여행 스타일, 자기소개를 제공한다. | M | Story 4 | 닉네임·연령대·여행 스타일은 필수, 성별은 선택이다. | IMPLEMENT | SCR-005(프로필 탭) |
| REQ-FUNC-030 | 시스템은 국가·지역·여행 기간 겹침·연령대·성별·여행 스타일·모집 상태로 동행글을 필터한다. | M | AC-M02 | 차단 사용자의 글은 제외되고 p95 1초 이내다. | IMPLEMENT | SCR-004 |
| REQ-FUNC-031 | 시스템은 모집글에 제목, 국가, 지역, 시작일, 종료일, 모집 인원, 선호 조건, 여행 스타일, 상세 설명, 안전수칙 동의를 입력받는다. | M | AC-M03 | 필수값 누락·역전 날짜·과거 종료일은 제출 차단된다. | IMPLEMENT | SCR-003(동행 작성 탭) |
| REQ-FUNC-032 | 시스템은 본문에서 전화번호·이메일·일반 메신저 ID 패턴을 탐지해 제출을 차단한다. | M | AC-M08 | 기준 테스트셋 탐지율 95% 이상, 오탐 5% 이하이며 수정 안내를 제공한다. | IMPLEMENT | SCR-003(동행 작성 탭) |
| REQ-FUNC-033 | 시스템은 모집글 작성자·상태·조건·설명을 표시하되 이메일과 외부 연락처를 노출하지 않는다. | M | Story 4 | HTML·JSON 응답에 이메일·전화번호가 포함되지 않는다. | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-034 | 시스템은 모집중 글에 최대 500자의 참가 메시지를 비공개로 제출하게 한다. | M | AC-M04 | 요청은 PENDING으로 저장되고 작성자와 요청자만 열람한다. | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-035 | 시스템은 동일 사용자의 동일 글 중복 PENDING·ACCEPTED 요청을 차단한다. | M | Data Integrity | DB unique 정책과 UI 오류가 동작한다. | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-036 | 시스템은 글 작성자가 참가 요청을 ACCEPTED 또는 REJECTED로 변경하게 한다. | M | AC-M05 | 비작성자 변경은 403이며 상태 전이가 감사 로그에 기록된다. | IMPLEMENT | SCR-005(내 활동 탭) |
| REQ-FUNC-037 | 시스템은 여행 종료일 다음 날 모집글을 CLOSED로 자동 전환한다. | M | AC-M07 | 종료 후 24시간 이내 공개 모집중 목록에서 제거된다. | IMPLEMENT | SCR-004 |
| REQ-FUNC-038 | 시스템은 작성자가 모집글을 수동 마감·수정·삭제하게 한다. | M | Story 4 | 승인 요청자가 있으면 중요 일정 변경 전 경고한다. | IMPLEMENT | SCR-005(내 활동 탭) |
| REQ-FUNC-039 | 시스템은 글·사용자·참가 요청을 사유 코드와 설명으로 신고하게 한다. | M | AC-M06 | 신고 ID와 접수 시각이 3초 이내 표시된다. | IMPLEMENT | SCR-004(상세 패널) |
| REQ-FUNC-040 | 시스템은 사용자가 다른 사용자를 차단·해제하게 한다. | M | AC-M06 | 차단 후 상호 글·프로필·요청이 노출되지 않는다. | IMPLEMENT | SCR-005(내 활동 탭) |
| REQ-FUNC-041 | 시스템은 Moderator에게 신고 우선순위·상태·대상·증거·접수 시각 큐를 제공한다. | M | Admin | OPEN, REVIEWING, RESOLVED, DISMISSED 필터가 동작한다. | IMPLEMENT | SCR-005(관리자 탭) |
| REQ-FUNC-042 | 시스템은 Moderator가 경고, 콘텐츠 숨김, 계정 일시 제한, 신고 기각 조치를 기록하게 한다. | M | Admin | 사유·담당자·시각이 감사 로그에 남고 원본은 일반 사용자에게 숨겨진다. | IMPLEMENT | SCR-005(관리자 탭) |
| REQ-FUNC-043 | 시스템은 참가 요청 접수·승인·거절·신고 처리 결과를 인앱 알림으로 제공하고 이메일은 선택적으로 발송한다. | M | AC-M05 | 알림 상태는 1분 이내 생성되고 이메일 장애가 상태 변경을 롤백하지 않는다. | IMPLEMENT | SCR-004, SCR-005 |
| REQ-FUNC-044 | 시스템은 RLS로 본인 글·요청, 요청 대상 작성자, Moderator/Admin만 비공개 데이터를 열람하게 한다. | M | Security | 권한별 부정 접근 테스트가 모두 403 또는 빈 결과다. | IMPLEMENT | - |
| REQ-FUNC-045 | 시스템은 회원 탈퇴 시 공개 프로필을 즉시 비식별화하고 법적·분쟁 보존 대상이 아닌 개인정보를 30일 이내 삭제한다. | M | Privacy | 삭제 작업·예외 사유가 감사 로그에 기록된다. | EXCLUDED | - |

#### 4.1.5 F5. Country Safety

| ID | Requirement | P | Source | Acceptance Criteria | Scope | Screen |
|---|---|:---:|---|---|---|---|
| REQ-FUNC-046 | 시스템은 게시된 모든 해외 국가에 하나 이상의 공개 안전 페이지를 요구한다. | M | GOAL-03 | 해외 국가 수와 안전 페이지 국가 수의 차이가 0이다. | IMPLEMENT | - |
| REQ-FUNC-047 | 시스템은 치안, 흔한 사기, 현지 법규, 교통, 재난·기후, 보건, 문화·복장, 긴급연락처 섹션을 제공한다. | M | Story 5 | 필수 카테고리 누락 시 게시가 차단된다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-048 | 시스템은 각 안전 페이지에 공식 출처명·URL·최종 확인일·편집자를 기록한다. | M | AC-S01 | 공개 페이지와 관리자 레코드에 메타데이터가 존재한다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-049 | 시스템은 외교부 해외안전여행 원문 링크를 새 탭으로 제공한다. | M | AC-S02 | 링크에 `noopener,noreferrer`가 적용되고 주간 검사에 통과한다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-050 | 시스템은 최종 확인 후 7일이 지나면 stale 상태와 재확인 경고를 표시한다. | M | AC-S03 | 기준 시각 7일 초과 시 자동 경고되고 일반 최신 배지를 숨긴다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-051 | 시스템은 출국권고·여행금지·특별여행주의보 등 중대 경보를 본문 상단에 텍스트로 표시한다. | M | AC-S05 | 색상만 사용하지 않고 단계·행동요령·범위를 표시한다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-052 | 시스템은 국가 전체 경보와 특정 지역 경보를 별도 범위로 모델링한다. | M | AC-S04 | `scope_type`과 `scope_text`가 없으면 지역 경보를 게시할 수 없다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-053 | 시스템은 현지 긴급전화와 대한민국 재외공관 또는 영사콜센터 연결 정보를 표시한다. | M | Story 5 | 번호·링크·출처·확인일을 표시한다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-054 | 시스템은 안전정보가 공식 판단을 대체하지 않으며 출국 직전 원문 재확인이 필요함을 고지한다. | M | OS-09 | 안전 페이지와 항공 외부 이동 요약에서 고지가 노출된다. | IMPLEMENT | SCR-001, SCR-003(항공/숙소 요약) |
| REQ-FUNC-055 | 시스템은 Editor/Admin이 안전 콘텐츠를 작성·검수·게시·보관하게 한다. | M | F7 | 편집자와 게시 승인자가 구분되고 모든 변경이 기록된다. | EXCLUDED | - |
| REQ-FUNC-056 | 시스템은 안전정보 변경 이력을 이전 값·새 값·사유·담당자·시각과 함께 보존한다. | M | Governance | Admin은 국가별 이력을 시간순 조회할 수 있다. | EXCLUDED | - |

#### 4.1.6 F6. About free_traveler

| ID | Requirement | P | Source | Acceptance Criteria | Scope | Screen |
|---|---|:---:|---|---|---|---|
| REQ-FUNC-057 | 시스템은 대표명 `free_traveler`, `50+ Trips`, `30+ Countries`를 표시한다. | M | AC-A01 | 세 값이 대표 페이지와 홈 소개 카드에서 일치한다. | IMPLEMENT | SCR-002 |
| REQ-FUNC-058 | 시스템은 대표 소개문·여행 철학·콘텐츠 편집 원칙을 표시한다. | M | PRD 6 | 확정 소개문이 줄임 없이 대표 페이지에 제공된다. | IMPLEMENT | SCR-002 |
| REQ-FUNC-059 | 시스템은 방문 권역 지도 또는 30개국 이상의 국가 목록을 제공한다. | M | AC-A03 | 국가마다 이름·권역이 있고 연결 오류가 없다. | IMPLEMENT | SCR-002 |
| REQ-FUNC-060 | 시스템은 대표 여행 타임라인과 대표 여행 기록을 제공한다. | M | PRD 6-3 | 타임라인 항목에 연도·장소·요약이 있다. | IMPLEMENT | SCR-002 |
| REQ-FUNC-061 | 시스템은 대표 이미지에 대체텍스트·출처·작가·라이선스 URL을 제공한다. | M | AC-A02 | 메타데이터가 없으면 기본 플레이스홀더로 대체된다. | EXCLUDED | - |
| REQ-FUNC-062 | 시스템은 관리자 설정 기반 문의·SNS 링크를 제공한다. | S | PRD 6-3 | 빈 링크는 렌더링하지 않고 허용 프로토콜만 연다. | IMPLEMENT | SCR-002 |
| REQ-FUNC-063 | 시스템은 대표 추천 여행지 6개를 공개 여행지 상세로 연결한다. | S | PRD 6-3 | 비공개 여행지는 자동 제외되고 대체 후보가 표시된다. | IMPLEMENT | SCR-002 |

#### 4.1.7 F7. Common, Admin, Governance

| ID | Requirement | P | Source | Acceptance Criteria | Scope | Screen |
|---|---|:---:|---|---|---|---|
| REQ-FUNC-064 | 시스템은 모든 공개 페이지에 일관된 전역 내비게이션과 푸터를 제공한다. | M | Sitemap | 핵심 6개 기능과 정책 페이지에 2회 이내 이동할 수 있다. | IMPLEMENT | COMMON |
| REQ-FUNC-065 | 시스템은 320px부터 데스크톱까지 레이아웃을 반응형으로 제공한다. | M | Platform | 가로 스크롤·겹침 없이 주요 기능이 동작한다. | IMPLEMENT | COMMON |
| REQ-FUNC-066 | 시스템은 이메일 가입·인증·로그인·로그아웃·비밀번호 재설정을 제공한다. | M | IS-06 | 인증되지 않은 이메일은 동행 쓰기 권한을 얻지 못한다. | IMPLEMENT | SCR-005(로그인/인증 탭) |
| REQ-FUNC-067 | 시스템은 여행지·국가 안전정보를 통합 검색한다. | M | Discover | 결과 유형 라벨과 하이라이트를 표시한다. | IMPLEMENT | SCR-001 |
| REQ-FUNC-068 | 시스템은 회원이 여행지를 즐겨찾기·해제·조회하게 한다. | S | MoSCoW | 중복 즐겨찾기가 생성되지 않는다. | IMPLEMENT | SCR-001, SCR-005(내 활동 탭) |
| REQ-FUNC-069 | 시스템은 여행지·안전·동행 공개 페이지의 URL 공유를 제공한다. | S | MoSCoW | Web Share API 실패 시 URL 복사로 폴백한다. | IMPLEMENT | SCR-001, SCR-004 |
| REQ-FUNC-070 | 시스템은 공개 페이지별 title, description, canonical, Open Graph, 구조화 데이터를 제공한다. | M | SEO | SEO 자동 검사에서 필수 메타 누락이 0건이다. | IMPLEMENT | COMMON |
| REQ-FUNC-071 | 시스템은 폼 시작·검증 완료·외부 클릭·안전 섹션 조회·동행 요청 이벤트를 기록하되 정확한 날짜와 자유서술은 기록하지 않는다. | M | KPI/CON-01 | 이벤트 스키마 검사에서 금지 속성이 0건이다. | EXCLUDED | - |
| REQ-FUNC-072 | 시스템은 Editor/Admin에게 여행지·콘텐츠 CRUD와 미리보기를 제공한다. | M | F7 | 공개 전 미리보기와 상태 DRAFT/REVIEW/PUBLISHED/ARCHIVED가 동작한다. | EXCLUDED | - |
| REQ-FUNC-073 | 시스템은 미디어 업로드 시 출처·작가·라이선스·원문 URL·대체텍스트를 필수 입력받는다. | M | CON-08 | 누락 미디어의 게시 연결이 차단된다. | EXCLUDED | - |
| REQ-FUNC-074 | 시스템은 여행지·안전·대표 콘텐츠의 게시 전 완전성 게이트를 실행한다. | M | GOAL-04 | 누락 목록을 반환하고 통과 전 PUBLISHED 전환을 거부한다. | EXCLUDED | - |
| REQ-FUNC-075 | 시스템은 안전정보 stale 현황, 최근 확인일, 검토 담당자 대시보드를 제공한다. | M | ASM-04 | 7일 초과 항목이 상단 정렬되고 담당자 필터가 동작한다. | EXCLUDED | - |
| REQ-FUNC-076 | 시스템은 관리자 변경·신고 처리·권한 변경을 감사 로그로 남긴다. | M | Governance | actor, action, target, before, after, reason, timestamp를 기록한다. | EXCLUDED | - |
| REQ-FUNC-077 | 시스템은 Admin이 항공·호텔 외부 URL을 허용목록 내 HTTPS 주소로 설정하게 한다. | M | CP-01 | HTTP·javascript·data URL은 저장할 수 없다. | IMPLEMENT | SCR-005(관리자 탭) |
| REQ-FUNC-078 | 시스템은 404·500·권한 없음·외부 연결 실패 화면에 복구 행동을 제공한다. | M | Reliability | 홈·이전·재시도 중 해당 행동이 최소 1개 제공된다. | IMPLEMENT | COMMON |
| REQ-FUNC-079 | 시스템은 폼·모달·탭·알림에 올바른 HTML 의미와 ARIA 상태를 제공한다. | M | WCAG | 자동 검사와 키보드 수동 검사에 통과한다. | IMPLEMENT | COMMON |
| REQ-FUNC-080 | 시스템은 이용약관, 개인정보 처리방침, 동행 안전수칙, 콘텐츠 면책 안내를 제공하고 동행 글 작성 시 안전수칙 동의를 기록한다. | M | Safety/Privacy | 정책 버전과 동의 시각이 저장된다. | IMPLEMENT | SCR-003(동행 작성 탭) |

### 4.2 Non-Functional Requirements

#### 4.2.1 Performance

| ID | Requirement | Metric | Target | Condition | Scope | Screen |
|---|---|---|---:|---|---|---|
| REQ-NF-001 | 공개 핵심 페이지의 LCP를 제한한다. | LCP p75 | ≤2.5s | 중급 모바일, 4G | IMPLEMENT | COMMON |
| REQ-NF-002 | 상호작용 지연을 제한한다. | INP p75 | ≤200ms | 실제 사용자 필드 데이터 | IMPLEMENT | COMMON |
| REQ-NF-003 | 레이아웃 이동을 제한한다. | CLS p75 | ≤0.1 | 공개 페이지 | IMPLEMENT | COMMON |
| REQ-NF-004 | 여행지·동행 필터 응답을 제한한다. | p95 | ≤1s | 동시 사용자 50명 | IMPLEMENT | - |
| REQ-NF-005 | 쓰기 API 응답을 제한한다. | p95 | ≤3s | 글·요청·신고 | IMPLEMENT | - |
| REQ-NF-006 | 이미지 성능을 최적화한다. | 초기 로드 | responsive size + lazy load | LCP 이미지는 priority | IMPLEMENT | COMMON |
| REQ-NF-007 | 배포 전 성능 예산을 검사한다. | Lighthouse Performance | ≥85 | 모바일 CI | EXCLUDED | - |

#### 4.2.2 Reliability and Recovery

| ID | Requirement | Target | Scope | Screen |
|---|---|---:|---|---|
| REQ-NF-008 | 월간 서비스 가용성 | ≥99.5% | EXCLUDED | - |
| REQ-NF-009 | 내부 API 5xx 비율 | ≤0.5% | EXCLUDED | - |
| REQ-NF-010 | DB 백업 RPO/RTO | RPO ≤24h, RTO ≤8h | EXCLUDED | - |
| REQ-NF-011 | 항공·호텔·공식 출처 링크 자동 검사 | 주 1회, 실패 시 Admin 알림 | EXCLUDED | - |

#### 4.2.3 Security and Privacy

| ID | Requirement | Verification | Scope | Screen |
|---|---|---|---|---|
| REQ-NF-012 | 모든 통신에 TLS 1.2 이상을 사용한다. | SSL 설정 검사 | IMPLEMENT | - |
| REQ-NF-013 | 인증·역할·RLS 정책을 서버에서 검증한다. | 권한별 부정 테스트 | IMPLEMENT | - |
| REQ-NF-014 | 상태 변경 요청에 CSRF 방어·SameSite 쿠키를 적용한다. | 보안 통합 테스트 | IMPLEMENT | - |
| REQ-NF-015 | 사용자 입력을 검증·이스케이프하고 저장 XSS를 차단한다. | OWASP 기반 테스트 | IMPLEMENT | - |
| REQ-NF-016 | 비밀키는 환경변수로 관리하고 클라이언트 번들에 포함하지 않는다. | 빌드 산출물 검사 | IMPLEMENT | - |
| REQ-NF-017 | 항공·호텔 원시 입력값을 서버·분석에 보존하지 않는다. | 네트워크·로그·DB 검사 | IMPLEMENT | - |
| REQ-NF-018 | 개인정보 내보내기·탈퇴·삭제 요청을 제공한다. | E2E와 삭제 감사 로그 | EXCLUDED | - |

#### 4.2.4 Safety and Moderation

| ID | Requirement | Target | Scope | Screen |
|---|---|---:|---|---|
| REQ-NF-019 | 신고 접수 응답 | p95 ≤3s | IMPLEMENT | - |
| REQ-NF-020 | 신고 1차 검토 | 24h 이내 90% 이상 | EXCLUDED | - |
| REQ-NF-021 | 동일 사용자의 글·요청·신고 속도 제한 | 정책 초과 시 429 | EXCLUDED | - |
| REQ-NF-022 | Moderator 조치 추적 가능성 | 감사 로그 누락 0건 | EXCLUDED | - |

#### 4.2.5 Accessibility

| ID | Requirement | Target | Scope | Screen |
|---|---|---:|---|---|
| REQ-NF-023 | WCAG 2.2 준수 목표 | Level AA | IMPLEMENT | COMMON |
| REQ-NF-024 | 자동 접근성 검사 | axe serious/critical 0건 | EXCLUDED | - |
| REQ-NF-025 | 키보드·스크린리더 수동 검사 | 핵심 UC 100% 통과 | IMPLEMENT | - |

#### 4.2.6 Content, Freshness, SEO, Copyright

| ID | Requirement | Target | Scope | Screen |
|---|---|---:|---|---|
| REQ-NF-026 | 여행지 콘텐츠 완전성 | 게시 콘텐츠 100% | IMPLEMENT | - |
| REQ-NF-027 | 해외 국가 안전정보 커버리지 | 게시 국가 100% | IMPLEMENT | - |
| REQ-NF-028 | 안전정보 최신 확인 | 7일 이내 95% 이상, 초과 시 경고 100% | IMPLEMENT | SCR-001 |
| REQ-NF-029 | 미디어 라이선스 메타데이터 | 공개 미디어 100% | EXCLUDED | - |
| REQ-NF-030 | 공개 페이지 SEO 메타데이터 | 누락 0건 | IMPLEMENT | - |

#### 4.2.7 Maintainability, Monitoring, Cost

| ID | Requirement | Target | Scope | Screen |
|---|---|---:|---|---|
| REQ-NF-031 | TypeScript strict·lint·unit test | main 병합 전 통과 | IMPLEMENT | - |
| REQ-NF-032 | 구조화 로그 | request_id, actor, action, result; 개인정보 제외 | EXCLUDED | - |
| REQ-NF-033 | 핵심 오류 알림 | 5xx>1% 또는 외부 링크 실패 시 5분 이내 | EXCLUDED | - |
| REQ-NF-034 | MVP 월 인프라 비용 | 콘텐츠 인건비 제외 100,000원 이하 목표 | IMPLEMENT | - |

---

## 5. Traceability Matrix

### 5.1 PRD Story to Requirement to Test (원문 유지)

| PRD Source | Requirements | Test Cases | Priority |
|---|---|---|---|
| Story 1 / AC-D01~D05 | REQ-FUNC-001~010 | TC-FUNC-001~010 | M/S |
| Story 2 / AC-F01~F06 | REQ-FUNC-011~018 | TC-FUNC-011~018 | M |
| Story 3 / AC-H01~H05 | REQ-FUNC-019~026 | TC-FUNC-019~026 | M |
| Story 4 / AC-M01~M08 | REQ-FUNC-027~045 | TC-FUNC-027~045 | M |
| Story 5 / AC-S01~S05 | REQ-FUNC-046~056 | TC-FUNC-046~056 | M |
| Story 6 / AC-A01~A03 | REQ-FUNC-057~063 | TC-FUNC-057~063 | M/S |
| Common/Admin/Governance | REQ-FUNC-064~080 | TC-FUNC-064~080 | M/S |

### 5.2 NFR Traceability (원문 유지)

| Category | Requirements | Test Cases |
|---|---|---|
| Performance | REQ-NF-001~007 | TC-NF-001~007 |
| Reliability | REQ-NF-008~011 | TC-NF-008~011 |
| Security/Privacy | REQ-NF-012~018 | TC-NF-012~018 |
| Safety/Moderation | REQ-NF-019~022 | TC-NF-019~022 |
| Accessibility | REQ-NF-023~025 | TC-NF-023~025 |
| Content/SEO/Copyright | REQ-NF-026~030 | TC-NF-026~030 |
| Maintainability/Monitoring/Cost | REQ-NF-031~034 | TC-NF-031~034 |

### 5.3 UI/UX 연결(신규)

Screen/Route/Page Entry/Task/Test/Status 단위의 상세 추적은 이 문서가 아니라 `UIUX_TRACEABILITY.md`를 정본으로 한다. §4의 Scope/Screen 열은 요약 참조이며, 행 단위 진행 상태(Task 생성 여부, 실제 테스트 실행 결과)는 `UIUX_TRACEABILITY.md`에서만 갱신한다.

---

## 6. Appendix

`02_SRS_BASELINE.md` §6(Internal API and Server Actions, External URLs, Data Model, Entity Relationship Diagram, State Models, Analytics Event Schema, Content Completeness Rules, Validation Plan)은 이번 개정으로 변경되지 않는다. 원문을 그대로 유지하며 본 문서에서 재수록하지 않는다.

---

## 7. UI Route Contract (신규)

전체 계약은 `05_UIUX_APPROVED.md` §3과 `../design-reference/SCREEN_ROUTE_CONTRACT.json`(`schema_version: traveler-screen-route-v1`)을 정본으로 한다. 요약:

- Screen 5개(SCR-001~SCR-005), Route·Page Entry 각각 중복 없음.
- 모든 Screen에 `page_owner_task_required=true`, `preview_required=true`. SCR-001은 추가로 `starter_template_forbidden=true`.
- 기술 Route(auth callback, API Route, not-found)는 Screen 수에 포함하지 않는다.
- 필수 화면 간 이동 15건은 `05_UIUX_APPROVED.md` §3-3에 기록되어 있다.

---

## 8. Release Acceptance Criteria (신규)

전체 기준은 `05_UIUX_APPROVED.md` §5를 정본으로 한다. 요약:

1. Screen·Route 구조가 §3.5·§7과 일치하고 SCR-001에 `create-next-app` 기본 스타터가 남아있지 않다.
2. Priority M(Must)로 표시된 IMPLEMENT 요구사항이 `UIUX_TRACEABILITY.md`에서 완료 상태로 전환된다(현재는 전부 미착수).
3. EXCLUDED 24개 요구사항이 암묵적으로 재도입되지 않는다.
4. `../design-reference/UI_CONTRACT.md`와 `../design-reference/D-001/DESIGN.md`의 금지 기능(구매·예약·결제 UI, Airbnb 상표 요소, 별점·리뷰, Proprietary 폰트, 플레이스홀더 문구 등)이 어떤 화면에도 없다.
5. 국내 10개 이상·해외 15개국 30개 도시 이상 콘텐츠, 해외 국가 100% 안전정보 커버리지가 충족된다.
6. `PROJECT_SCOPE.md` §9의 Playwright 핵심 Smoke Test SM-01~SM-10이 통과한다.

이 기준이 충족되기 전까지 본 문서의 어떤 요구사항도 "구현 완료"로 표시하지 않는다.
