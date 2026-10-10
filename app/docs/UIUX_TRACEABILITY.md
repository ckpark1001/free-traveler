# Free Traveler — UI/UX Traceability Matrix

- **Document ID:** UIUXTR-TRAVEL-001
- **기반 문서:** `02_SRS_BASELINE.md`(SRS-TRAVEL-001), `PROJECT_SCOPE.md`(SCOPE-TRAVEL-001), `03_UI_COVERAGE_ANALYSIS.md`(UICOV-TRAVEL-001), `05_UIUX_APPROVED.md`, `../design-reference/UI_CONTRACT.md`, `../design-reference/SCREEN_ROUTE_CONTRACT.json`
- **작성일:** 2026-09-15
- **상태:** Traceability Baseline (구현 시작 전)
- **대상:** REQ-FUNC-001~080(80개), REQ-NF-001~034(34개), 총 114개 — 전량 유지, 삭제 없음

이 문서는 `02_SRS_BASELINE.md`의 요구사항 114개 전체를 승인된 5개 Screen(SCR-001~SCR-005)과 Next.js Route/Page Entry에 연결한다. 어떤 요구사항도 삭제·병합하지 않으며, `PROJECT_SCOPE.md`가 EXCLUDED로 확정한 항목은 EXCLUDED로 그대로 표시한다.

## 0. 열 정의(Column Legend)

| 열 | 값 집합 | 정의 |
|---|---|---|
| **Requirement** | `REQ-FUNC-xxx` / `REQ-NF-xxx` + 요약 | `02_SRS_BASELINE.md` §4 원문 ID와 요약(원문 변경 없음) |
| **Implementation Status** | `IMPLEMENT (NOT_STARTED)` \| `EXCLUDED` | `PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 분류 + 현재 코드 상태의 정직한 반영. 현재 `app/src/app`에는 `create-next-app` 기본 스타터만 존재하며 어떤 화면도 구현되지 않았으므로, IMPLEMENT로 분류된 항목도 전부 `NOT_STARTED`다. |
| **Screen** | `SCR-001`~`SCR-005` \| `COMMON`(전체 화면 공통) \| `-`(미배치) | `03_UI_COVERAGE_ANALYSIS.md` 배치 Screen을 그대로 승계 |
| **Route** | `/`, `/about`, `/travel-tools`, `/mates`, `/account` \| `공통(모든 Route)` \| `-` | `../design-reference/SCREEN_ROUTE_CONTRACT.json` 매핑 |
| **Page Entry** | `src/app/...` \| `-` | `../design-reference/SCREEN_ROUTE_CONTRACT.json` 매핑(공통 항목은 `src/app/layout.tsx`) |
| **Task** | `PENDING_TASK_GENERATION` \| `N/A (제외)` | 아직 어떤 구현 Task도 생성되지 않았으므로 IMPLEMENT 항목은 전부 `PENDING_TASK_GENERATION`. EXCLUDED 항목은 구현 Task 대상이 아니므로 `N/A (제외)` |
| **Test** | 계획된 검증 방법 | `PROJECT_SCOPE.md` §6·§7의 "확인 방법"을 그대로 인용(계획일 뿐 실행·통과를 의미하지 않음) |
| **Status** | `OPEN` \| `CLOSED_EXCLUDED` | 이 추적 행이 앞으로 계속 추적되어야 하는지(OPEN) 아니면 제외로 종결되었는지(CLOSED_EXCLUDED) |

> 어떤 행도 "구현 완료"를 의미하는 값을 갖지 않는다. 실제 코드가 작성되고 테스트가 통과한 뒤에만 Implementation Status/Status를 갱신한다.

---

## 1. F1 Destination Guide (REQ-FUNC-001~010)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-001 — 국내·해외 목록 구분 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-01 | OPEN |
| REQ-FUNC-002 — 국가·도시·계절·테마·기간 필터(AND) | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-01 | OPEN |
| REQ-FUNC-003 — 키워드 검색(한글 부분 일치) | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-004 — 상세 필수 콘텐츠 필드 전체 표시 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 콘텐츠 체크리스트 | OPEN |
| REQ-FUNC-005 — 빈 결과 안내+초기화 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-01 | OPEN |
| REQ-FUNC-006 — 해외 상세→국가 안전정보 연결 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 QA(데이터 일치 확인) | OPEN |
| REQ-FUNC-007 — 이미지 대체텍스트·출처·작가·라이선스 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-008 — 게시 수량(국내 10+, 해외 15개국 30도시+) 검증 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 콘텐츠 체크리스트 | OPEN |
| REQ-FUNC-009 — 관련 여행지 최대 6개 추천 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-010 — 필터 상태 URL query 반영·복원 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-01 | OPEN |

## 2. F2 Flight Link-out (REQ-FUNC-011~018) → SCR-003 항공 탭

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-011 — 국가·지역·출발일·귀국일 필수 입력 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-02 | OPEN |
| REQ-FUNC-012 — 국가별 하위 지역만 선택·초기화 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-02 | OPEN |
| REQ-FUNC-013 — 과거 출발일·역전 날짜 차단 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-02(경계값) | OPEN |
| REQ-FUNC-014 — 유효 입력 후 요약 단계 표시 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-02 | OPEN |
| REQ-FUNC-015 — 입력값 비전달 고지 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-016 — 외부 항공 URL 새 탭 이동 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-02 | OPEN |
| REQ-FUNC-017 — 항공 입력값 서버 미저장 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 코드 리뷰 + 네트워크 탭 수동 확인 | OPEN |
| REQ-FUNC-018 — 외부 URL 오류 시 차단+재시도 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |

## 3. F3 Hotel Link-out (REQ-FUNC-019~026) → SCR-003 숙소 탭

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-019 — 국가·지역·체크인·체크아웃 필수 입력 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-03 | OPEN |
| REQ-FUNC-020 — 국가별 하위 지역만 선택 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-03 | OPEN |
| REQ-FUNC-021 — 과거 체크인·체크아웃≤체크인 차단 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-03(경계값) | OPEN |
| REQ-FUNC-022 — 유효 입력 후 요약 표시 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-03 | OPEN |
| REQ-FUNC-023 — 입력값 비전달 고지 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-024 — 외부 호텔 URL 새 탭 이동 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-03 | OPEN |
| REQ-FUNC-025 — 호텔 입력값 서버 미저장 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 코드 리뷰 + 네트워크 탭 수동 확인 | OPEN |
| REQ-FUNC-026 — 호텔 URL 오류 시 차단+재시도 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |

## 4. F4 Travel Mate (REQ-FUNC-027~045) → SCR-003 동행 작성 탭 / SCR-004 / SCR-005

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-027 — 동행 쓰기 인증 세션 요구 | IMPLEMENT (NOT_STARTED) | SCR-003, SCR-004 | `/travel-tools`, `/mates` | `src/app/travel-tools/page.tsx`, `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-04/05 | OPEN |
| REQ-FUNC-028 — 성인 확인 상태 요구, 생년월일 미저장 | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | 코드 리뷰(스키마 확인)+Playwright SM-04 | OPEN |
| REQ-FUNC-029 — 동행 프로필(닉네임·연령대·성별·스타일·자기소개) | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-04 | OPEN |
| REQ-FUNC-030 — 국가·지역·기간·연령대·성별·스타일·상태 필터 | IMPLEMENT (NOT_STARTED) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 수동 QA(기능 정확성) | OPEN |
| REQ-FUNC-031 — 모집글 필수 필드+검증 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-05 | OPEN |
| REQ-FUNC-032 — 연락처 패턴 탐지·차단 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-05(테스트셋 케이스) | OPEN |
| REQ-FUNC-033 — 모집글에 연락처 비노출 | IMPLEMENT (NOT_STARTED) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 코드 리뷰(응답 스키마 확인) | OPEN |
| REQ-FUNC-034 — 비공개 참가 메시지(500자) PENDING 저장 | IMPLEMENT (NOT_STARTED) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-06 | OPEN |
| REQ-FUNC-035 — 동일 사용자 중복 요청 차단 | IMPLEMENT (NOT_STARTED) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 수동 QA(DB 제약 확인) | OPEN |
| REQ-FUNC-036 — 작성자 승인/거절, 비작성자 403 | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-06 | OPEN |
| REQ-FUNC-037 — 종료일 경과 시 자동 CLOSED(조회 시 계산) | IMPLEMENT (NOT_STARTED) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 수동 QA(종료일 지난 글 미노출 확인) | OPEN |
| REQ-FUNC-038 — 작성자 수동 마감·수정·삭제 | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-039 — 신고 접수(사유+설명), 접수번호 표시 | IMPLEMENT (NOT_STARTED) | SCR-004 | `/mates` | `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-07 | OPEN |
| REQ-FUNC-040 — 사용자 차단·해제, 상호 노출 제한 | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-07 | OPEN |
| REQ-FUNC-041 — 관리자 신고 큐(상태 필터) | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-042 — 신고 처리(상태 변경·게시물 숨김) | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-043 — 참가 요청·신고 처리 알림(Toast/화면 상태) | IMPLEMENT (NOT_STARTED) | SCR-004, SCR-005 | `/mates`, `/account` | `src/app/mates/page.tsx`, `src/app/account/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-044 — RLS로 비공개 데이터 접근 제한 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 권한별 부정 접근 테스트(수동) | OPEN |
| REQ-FUNC-045 — 탈퇴 시 즉시 비식별화+30일 내 삭제 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |

## 5. F5 Country Safety (REQ-FUNC-046~056) → SCR-001 안전정보 Drawer/Modal

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-046 — 게시 해외 국가 100% 안전 페이지 보유 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 데이터 커버리지 확인 | OPEN |
| REQ-FUNC-047 — 8개 필수 카테고리 제공 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 콘텐츠 체크리스트 | OPEN |
| REQ-FUNC-048 — 출처명·URL·확인일·편집자 기록 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 콘텐츠 체크리스트 | OPEN |
| REQ-FUNC-049 — 외교부 원문 링크 새 탭 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-08 | OPEN |
| REQ-FUNC-050 — 확인 후 7일 초과 시 stale 경고 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-08(날짜 mock) | OPEN |
| REQ-FUNC-051 — 중대 경보 상단 텍스트 표시 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-052 — 국가 전체/지역 경보 범위 구분 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 콘텐츠 체크리스트 | OPEN |
| REQ-FUNC-053 — 현지·영사 긴급연락처 표시 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-054 — 공식 판단 대체 아님 고지 | IMPLEMENT (NOT_STARTED) | SCR-001, SCR-003 | `/`, `/travel-tools` | `src/app/page.tsx`, `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-055 — Editor 작성·검수·게시·보관 워크플로 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-056 — 안전정보 변경 이력 보존 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |

## 6. F6 About free_traveler (REQ-FUNC-057~063) → SCR-002

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-057 — 대표명·50+ Trips·30+ Countries 표시 | IMPLEMENT (NOT_STARTED) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 수동 QA(값 일치 확인) | OPEN |
| REQ-FUNC-058 — 소개문·철학·편집 원칙 | IMPLEMENT (NOT_STARTED) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-059 — 방문 권역/30개국 이상 목록 | IMPLEMENT (NOT_STARTED) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-060 — 대표 여행 타임라인 | IMPLEMENT (NOT_STARTED) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-061 — 대표 이미지 대체텍스트·출처·작가·라이선스 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-062 — 문의·SNS 링크 | IMPLEMENT (NOT_STARTED) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-063 — 추천 여행지 6개 연결 | IMPLEMENT (NOT_STARTED) | SCR-002 | `/about` | `src/app/about/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |

## 7. F7 Common, Admin, Governance (REQ-FUNC-064~080)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-FUNC-064 — 전역 내비게이션·푸터 | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-065 — 320px~데스크톱 반응형 | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 QA(브라우저 반응형 도구) | OPEN |
| REQ-FUNC-066 — 이메일 가입·인증·로그인·로그아웃·재설정 | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-04 | OPEN |
| REQ-FUNC-067 — 여행지·안전정보 통합 검색 | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-068 — 여행지 즐겨찾기(localStorage, 중복 방지) | IMPLEMENT (NOT_STARTED) | SCR-001, SCR-005 | `/`, `/account` | `src/app/page.tsx`, `src/app/account/page.tsx` | PENDING_TASK_GENERATION | 수동 QA(localStorage 확인) | OPEN |
| REQ-FUNC-069 — 공개 페이지 URL 공유 | IMPLEMENT (NOT_STARTED) | SCR-001, SCR-004 | `/`, `/mates` | `src/app/page.tsx`, `src/app/mates/page.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-070 — title/description/canonical/OG 메타데이터 | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 코드 리뷰(메타 태그 확인) | OPEN |
| REQ-FUNC-071 — 폼·클릭·조회 이벤트 기록 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-072 — Editor/Admin 콘텐츠 CRUD+미리보기 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-073 — 미디어 업로드 시 출처·작가·라이선스 필수 입력 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-074 — 게시 전 완전성 게이트 자동 실행 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-075 — 안전정보 stale 현황 대시보드 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-076 — 관리자 변경·신고 처리 감사 로그 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-FUNC-077 — Admin 외부 URL 허용목록(HTTPS) 설정 | IMPLEMENT (NOT_STARTED) | SCR-005 | `/account` | `src/app/account/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-10 | OPEN |
| REQ-FUNC-078 — 404/500/권한없음/외부연결실패 복구 행동 | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-FUNC-079 — 폼·모달·탭·알림 HTML 의미·ARIA 상태 | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 접근성 점검(키보드/스크린리더) | OPEN |
| REQ-FUNC-080 — 정책 고지+동행 안전수칙 동의 기록 | IMPLEMENT (NOT_STARTED) | SCR-003 | `/travel-tools` | `src/app/travel-tools/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-05 | OPEN |

## 8. NFR — Performance (REQ-NF-001~007)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-001 — LCP p75 ≤2.5s | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 Lighthouse 점검 | OPEN |
| REQ-NF-002 — INP p75 ≤200ms | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 점검 | OPEN |
| REQ-NF-003 — CLS p75 ≤0.1 | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 점검 | OPEN |
| REQ-NF-004 — 필터 응답 p95≤1s(동시 50명) | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 QA(기능 응답성) | OPEN |
| REQ-NF-005 — 쓰기 API 응답 p95≤3s | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-NF-006 — 이미지 반응형·lazy load, LCP priority | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 코드 리뷰 | OPEN |
| REQ-NF-007 — 배포 전 Lighthouse CI 게이트 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |

## 9. NFR — Reliability and Recovery (REQ-NF-008~011)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-008 — 월간 가용성 ≥99.5% | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-009 — 내부 API 5xx ≤0.5% | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-010 — DB 백업 RPO/RTO | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-011 — 외부 링크 주1회 자동 검사+Admin 알림 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |

## 10. NFR — Security and Privacy (REQ-NF-012~018)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-012 — TLS 1.2 이상 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 브라우저 인증서 확인 | OPEN |
| REQ-NF-013 — 인증·역할·RLS 서버 검증 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 권한별 부정 접근 테스트(수동) | OPEN |
| REQ-NF-014 — CSRF 방어·SameSite 쿠키 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 코드 리뷰 | OPEN |
| REQ-NF-015 — 입력 검증·이스케이프, 저장 XSS 차단 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 XSS 케이스 테스트 | OPEN |
| REQ-NF-016 — 비밀키 환경변수 관리 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 빌드 산출물 확인 | OPEN |
| REQ-NF-017 — 항공·호텔 원시 입력값 미보존 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 코드 리뷰+네트워크 탭 확인 | OPEN |
| REQ-NF-018 — 개인정보 내보내기·탈퇴·삭제 요청 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |

## 11. NFR — Safety and Moderation (REQ-NF-019~022)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-019 — 신고 접수 응답 p95≤3s | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 QA | OPEN |
| REQ-NF-020 — 신고 1차 검토 24h 이내 90% | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-021 — 글·요청·신고 속도 제한(429) | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-022 — Moderator 조치 추적 가능성 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |

## 12. NFR — Accessibility (REQ-NF-023~025)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-023 — WCAG 2.2 Level AA 목표 | IMPLEMENT (NOT_STARTED) | COMMON | 공통(모든 Route) | `src/app/layout.tsx` | PENDING_TASK_GENERATION | 수동 접근성 점검 | OPEN |
| REQ-NF-024 — 자동 접근성 검사(axe) | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-025 — 키보드·스크린리더 수동 검사, 핵심 UC 100% | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 접근성 점검 | OPEN |

## 13. NFR — Content, Freshness, SEO, Copyright (REQ-NF-026~030)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-026 — 여행지 콘텐츠 완전성 100% | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 콘텐츠 체크리스트 | OPEN |
| REQ-NF-027 — 해외 국가 안전정보 커버리지 100% | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 데이터 커버리지 확인 | OPEN |
| REQ-NF-028 — 안전정보 최신 확인 7일 이내 95%, 초과 시 경고 100% | IMPLEMENT (NOT_STARTED) | SCR-001 | `/` | `src/app/page.tsx` | PENDING_TASK_GENERATION | Playwright SM-08(경고 로직) | OPEN |
| REQ-NF-029 — 미디어 라이선스 메타데이터 100% | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-030 — 공개 페이지 SEO 메타데이터 누락 0건 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 코드 리뷰 | OPEN |

## 14. NFR — Maintainability, Monitoring, Cost (REQ-NF-031~034)

| Requirement | Implementation Status | Screen | Route | Page Entry | Task | Test | Status |
|---|---|---|---|---|---|---|---|
| REQ-NF-031 — TypeScript strict·lint, main 병합 전 통과 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | CI(타입체크+lint) + Playwright | OPEN |
| REQ-NF-032 — 구조화 로그 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-033 — 5xx>1% 또는 외부 링크 실패 시 알림 | EXCLUDED | - | - | - | N/A (제외) | N/A | CLOSED_EXCLUDED |
| REQ-NF-034 — MVP 월 인프라 비용 ≤100,000원 | IMPLEMENT (NOT_STARTED) | - | - | - | PENDING_TASK_GENERATION | 수동 비용 확인(배포 시점) | OPEN |

---

## 15. 집계 검증

| 구분 | REQ-FUNC | REQ-NF | 합계 |
|---|---:|---:|---:|
| 총 개수 | 80 | 34 | 114 |
| IMPLEMENT (NOT_STARTED) | 69 | 21 | 90 |
| EXCLUDED | 11 | 13 | 24 |

- REQ-FUNC EXCLUDED 11개: 007, 045, 055, 056, 061, 071, 072, 073, 074, 075, 076
- REQ-NF EXCLUDED 13개: 007, 008, 009, 010, 011, 018, 020, 021, 022, 024, 029, 032, 033
- 위 개수·ID 목록은 `03_UI_COVERAGE_ANALYSIS.md` §5-2와 일치하며, `02_SRS_BASELINE.md`의 REQ-FUNC-001~080, REQ-NF-001~034 중 삭제되거나 누락된 항목은 없다.
- 모든 행의 Task 값은 `PENDING_TASK_GENERATION` 또는 `N/A (제외)`이며, 어떤 행도 완료·구현됨을 의미하는 값을 갖지 않는다.
