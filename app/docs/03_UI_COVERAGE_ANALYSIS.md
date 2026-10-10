# Free Traveler — UI Coverage Analysis v1.0

- **Document ID:** UICOV-TRAVEL-001
- **기반 문서:** `docs/02_SRS_BASELINE.md`(SRS-TRAVEL-001), `docs/PROJECT_SCOPE.md`(SCOPE-TRAVEL-001)
- **작성일:** 2026-09-10
- **상태:** UI Coverage Baseline
- **대상 Requirement:** REQ-FUNC-001~080(80개), REQ-NF-001~034(34개), 총 114개

이 문서는 SRS-TRAVEL-001의 요구사항 114개 전체를 5개의 고정 디자인 Screen에 배치하고, 각 요구사항이 화면에 어떻게 나타나는지(직접 UI 요소인지, 화면 상태인지, 비가시 기술 요건인지, 운영 프로세스인지)를 기록한다. `docs/PROJECT_SCOPE.md`의 IMPLEMENT/EXCLUDED 분류는 그대로 유지하며 변경하지 않는다.

---

## 1. 분류 기준

### 1-1. PROJECT_SCOPE 분류(변경 없이 인용)

| 값 | 의미 |
|---|---|
| IMPLEMENT | `docs/PROJECT_SCOPE.md`에서 구현·테스트 대상으로 확정한 요구사항 |
| EXCLUDED | `docs/PROJECT_SCOPE.md`에서 제외 사유와 함께 구현하지 않기로 확정한 요구사항 |

### 1-2. UI 분류(본 문서에서 신규 부여)

| 값 | 의미 |
|---|---|
| **UI_DIRECT** | 화면에 눈에 보이는 구성요소(폼, 목록, 버튼, 패널, Drawer/Modal, 링크 등)로 직접 나타나는 요구사항 |
| **UI_STATE** | 새 구성요소를 만들지는 않지만 화면의 동작·데이터 흐름·표시 조건에 반영되는 요구사항(검증 결과 반영, 자동 상태 전환, URL 동기화 등) |
| **NON_UI** | 화면 요소로 드러나지 않는 기술적 보장(성능, 보안, 데이터 미저장, 메타데이터 등) |
| **OPERATIONS** | 코드가 아니라 콘텐츠 작성·운영 절차·정책으로 충족되는 요구사항(수동 체크리스트, SLA, 감사, 인프라 운영 등) |

EXCLUDED로 분류된 요구사항도 UI 분류값은 "만약 구현했다면 어떤 성격이었을지"를 나타내는 참고 정보이며, 이 경우 배치 Screen은 항상 `-`(미배치)로 기록한다.

---

## 2. Screen 정의(정확히 5개, 고정)

| Screen | 라우트 | 사용자 목표 | 주요 영역 | 상태 | 이동 목적지 |
|---|---|---|---|---|---|
| **SCR-001** | `/` 메인 | 국내·해외 여행지를 탐색하고, 여행지·국가 안전정보를 확인한 뒤 다음 행동(항공/호텔/동행)을 정한다 | 히어로/가치 제안, 통합 검색, 국내·해외 탭, 필터 바, 여행지 카드 목록, 여행지 상세 Drawer/Modal, 안전정보 상세 Drawer/Modal, 대표 추천 요약, 즐겨찾기 토글 | 초기 로딩, 필터 결과 있음/없음(빈 상태+초기화), 여행지 Drawer 열림/닫힘, 안전정보 Drawer 열림/닫힘(최신/7일초과 stale/중대경보), 즐겨찾기 추가/해제 | SCR-002(대표 추천 클릭), SCR-003(상세 내 항공/호텔 CTA), SCR-004(동행 찾기 CTA), SCR-005(로그인·내 활동 진입), 외부 외교부 안전정보 원문(새 탭) |
| **SCR-002** | `/about` 대표 소개 | free_traveler의 경험·철학을 확인해 콘텐츠 신뢰도를 판단하고 추천 여행지로 이동한다 | 대표 소개 히어로, `50+ Trips`/`30+ Countries` 수치 카드, 철학·편집원칙, 방문 국가 목록, 타임라인, 추천 여행지 6, 문의·SNS 링크 | 정적 콘텐츠 표시 상태 위주, 추천 카드 hover/클릭 상태 | SCR-001(추천 여행지 클릭 시 상세 Drawer), 외부 SNS/문의 링크(새 탭) |
| **SCR-003** | `/travel-tools` 통합 여행 준비 | 항공·숙소 조건을 정리해 외부 예약 사이트로 이동하거나, 동행 모집글을 작성해 게시한다 | **탭1 항공**(국가·지역·출발일·귀국일 입력→검증→요약→외부 이동), **탭2 숙소**(국가·지역·체크인·체크아웃 입력→검증→요약→외부 이동), **탭3 동행 작성**(모집 조건·설명 입력, 연락처 탐지, 안전수칙 동의→게시) | 탭 전환, 폼 미입력/검증실패/유효 상태, 요약 표시 상태, 외부 이동 성공/URL 오류 상태(항공·숙소), 연락처 탐지 오류 상태(동행), 게시 완료 상태(동행), 비로그인·성인미확인 상태(동행) | 외부 항공/호텔 사이트(새 탭), SCR-005(비로그인·성인미확인 시 인증 유도), SCR-004(동행 게시 완료 후 이동) |
| **SCR-004** | `/mates` 동행 조회 | 조건이 맞는 동행 모집글을 찾아 참가를 요청하거나 신고·차단으로 자신을 보호한다 | 필터(국가/지역/기간/연령대/성별/스타일/상태), 모집글 목록, **상세 패널**(조건·설명·작성자 요약, 연락처 비노출, 참가 요청 폼, 신고·차단 버튼) | 목록 로딩/빈 상태, 필터 적용 상태, 상세 패널 열림/닫힘, 모집중/마감(자동·수동) 상태, 참가 요청 제출 전/PENDING/중복차단 오류, 신고 접수 완료, 차단 완료(상호 비노출 반영) | SCR-003(새 모집글 작성 CTA), SCR-005(비로그인·미인증 시 유도, 내 활동에서 요청 상태 확인) |
| **SCR-005** | `/account` 계정·관리 | 로그인·인증 상태를 관리하고 내 글·요청·차단·즐겨찾기를 확인하며, 관리자는 신고와 외부 URL을 처리한다 | **탭1 로그인/인증**(가입·이메일인증·로그인·로그아웃·비밀번호 재설정·성인확인), **탭2 프로필**(닉네임·연령대·성별·스타일·자기소개), **탭3 내 활동**(내 모집글 관리·참가 요청 승인/거절·차단 목록·즐겨찾기 목록), **탭4 관리자**(신고 큐·상태 변경, 외부 URL 설정 — Admin 역할만 노출) | 비로그인/로그인, 이메일 인증 대기/완료, 성인확인 미완료/완료, 탭별 목록 비어있음/있음, 관리자 탭 접근 허용/차단(403), 외부 URL 저장 성공/유효성 오류 | SCR-001(즐겨찾기 항목 클릭), SCR-003(동행 글 재작성), SCR-004(내 모집글·요청과 연결된 상세로 이동) |

### 2-1. 기술 Route(디자인 Screen으로 집계하지 않음)

다음은 사용자가 목적을 갖고 머무는 화면이 아니라 처리 후 위 5개 Screen 중 하나로 귀결되는 기술적 경로이므로 별도 Screen으로 세지 않는다.

| 기술 Route | 설명 | 결과 반영 위치 |
|---|---|---|
| `/api/*` | 데이터 조회·쓰기용 서버 Route | 5개 Screen의 UI_DIRECT/UI_STATE 요구사항을 통해 간접 반영 |
| Supabase 인증 콜백(예: `/auth/callback`) | 이메일 인증·OAuth 리다이렉트 처리 | 처리 후 SCR-005로 복귀 |
| 404 / 500 / 권한 없음 오류 라우트 | 공통 오류 처리 | 전체 화면 공통(REQ-FUNC-078) 상태로 표현, 5개 Screen 어디서든 발생 가능 |

"전체 화면 공통"은 6번째 Screen이 아니라 5개 Screen 모두에 적용되는 공통 레이아웃/상태(전역 내비게이션, 반응형, 접근성, 오류 복구, 메타데이터 등)를 가리키는 표기이며 별도 Screen으로 집계하지 않는다.

---

## 3. REQ-FUNC-001~080 배치

### 3-1. F1 Destination Guide → SCR-001

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-001 | 국내·해외 목록 구분 | IMPLEMENT | UI_DIRECT | SCR-001 | 탭 전환 |
| REQ-FUNC-002 | 국가·도시·계절·테마·기간 필터(AND) | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-003 | 키워드 검색(한글 부분 일치) | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-004 | 상세 필수 콘텐츠 필드 전체 표시 | IMPLEMENT | UI_DIRECT | SCR-001 | 여행지 카드 클릭 → Drawer/Modal |
| REQ-FUNC-005 | 빈 결과 안내+초기화 | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-006 | 해외 상세→국가 안전정보 연결 | IMPLEMENT | UI_DIRECT | SCR-001 | 여행지 Drawer → 안전정보 Drawer |
| REQ-FUNC-007 | 이미지 대체텍스트·출처·작가·라이선스 | EXCLUDED | UI_DIRECT | - | 대체텍스트만 REQ-FUNC-004 상세 표시에 포함, 출처·작가·라이선스는 미구현 |
| REQ-FUNC-008 | 게시 수량(국내 10+, 해외 15개국 30도시+) 검증 | IMPLEMENT | OPERATIONS | - | 콘텐츠 체크리스트, 결과는 SCR-001 목록 분량에 반영 |
| REQ-FUNC-009 | 관련 여행지 최대 6개 추천 | IMPLEMENT | UI_DIRECT | SCR-001 | Drawer 하단, 다른 여행지 Drawer로 전환 |
| REQ-FUNC-010 | 필터 상태 URL query 반영·복원 | IMPLEMENT | UI_STATE | SCR-001 | - |

### 3-2. F2 Flight Link-out → SCR-003 (항공 탭)

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-011 | 국가·지역·출발일·귀국일 필수 입력 | IMPLEMENT | UI_DIRECT | SCR-003(항공 탭) | - |
| REQ-FUNC-012 | 국가별 하위 지역만 선택·초기화 | IMPLEMENT | UI_DIRECT | SCR-003(항공 탭) | - |
| REQ-FUNC-013 | 과거 출발일·역전 날짜 차단 | IMPLEMENT | UI_DIRECT | SCR-003(항공 탭) | 검증 오류 표시 |
| REQ-FUNC-014 | 유효 입력 후 요약 단계 표시 | IMPLEMENT | UI_DIRECT | SCR-003(항공 탭) | - |
| REQ-FUNC-015 | 입력값 비전달 고지 | IMPLEMENT | UI_DIRECT | SCR-003(항공 탭) | - |
| REQ-FUNC-016 | 외부 항공 URL 새 탭 이동 | IMPLEMENT | UI_DIRECT | SCR-003(항공 탭) | 외부 항공 사이트(새 탭) |
| REQ-FUNC-017 | 항공 입력값 서버 미저장 | IMPLEMENT | NON_UI | - | - |
| REQ-FUNC-018 | 외부 URL 오류 시 차단+재시도 | IMPLEMENT | UI_DIRECT | SCR-003(항공 탭) | - |

### 3-3. F3 Hotel Link-out → SCR-003 (숙소 탭)

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-019 | 국가·지역·체크인·체크아웃 필수 입력 | IMPLEMENT | UI_DIRECT | SCR-003(숙소 탭) | - |
| REQ-FUNC-020 | 국가별 하위 지역만 선택 | IMPLEMENT | UI_DIRECT | SCR-003(숙소 탭) | - |
| REQ-FUNC-021 | 과거 체크인·체크아웃≤체크인 차단 | IMPLEMENT | UI_DIRECT | SCR-003(숙소 탭) | 검증 오류 표시 |
| REQ-FUNC-022 | 유효 입력 후 요약 표시 | IMPLEMENT | UI_DIRECT | SCR-003(숙소 탭) | - |
| REQ-FUNC-023 | 입력값 비전달 고지 | IMPLEMENT | UI_DIRECT | SCR-003(숙소 탭) | - |
| REQ-FUNC-024 | 외부 호텔 URL 새 탭 이동 | IMPLEMENT | UI_DIRECT | SCR-003(숙소 탭) | 외부 호텔 사이트(새 탭) |
| REQ-FUNC-025 | 호텔 입력값 서버 미저장 | IMPLEMENT | NON_UI | - | - |
| REQ-FUNC-026 | 호텔 URL 오류 시 차단+재시도 | IMPLEMENT | UI_DIRECT | SCR-003(숙소 탭) | - |

### 3-4. F4 Travel Mate → SCR-003(동행 작성 탭) / SCR-004(동행 상세) / SCR-005(내 활동·관리자)

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-027 | 동행 쓰기 인증 세션 요구 | IMPLEMENT | UI_STATE | SCR-003(동행 작성 탭), SCR-004 | 미인증 시 SCR-005 로그인 탭으로 유도 |
| REQ-FUNC-028 | 성인 확인 상태 요구, 생년월일 미저장 | IMPLEMENT | UI_STATE | SCR-005(로그인/인증 탭) | SCR-003·SCR-004 진입 시 미확인이면 SCR-005로 유도 |
| REQ-FUNC-029 | 동행 프로필(닉네임·연령대·성별·스타일·자기소개) | IMPLEMENT | UI_DIRECT | SCR-005(프로필 탭) | - |
| REQ-FUNC-030 | 국가·지역·기간·연령대·성별·스타일·상태 필터 | IMPLEMENT | UI_DIRECT | SCR-004 | - |
| REQ-FUNC-031 | 모집글 필수 필드+검증 | IMPLEMENT | UI_DIRECT | SCR-003(동행 작성 탭) | 게시 완료 시 SCR-004로 이동 |
| REQ-FUNC-032 | 연락처 패턴 탐지·차단 | IMPLEMENT | UI_DIRECT | SCR-003(동행 작성 탭) | 검증 오류 표시 |
| REQ-FUNC-033 | 모집글에 연락처 비노출 | IMPLEMENT | UI_DIRECT | SCR-004(상세 패널) | - |
| REQ-FUNC-034 | 비공개 참가 메시지(500자) PENDING 저장 | IMPLEMENT | UI_DIRECT | SCR-004(상세 패널) | - |
| REQ-FUNC-035 | 동일 사용자 중복 요청 차단 | IMPLEMENT | UI_STATE | SCR-004(상세 패널) | - |
| REQ-FUNC-036 | 작성자 승인/거절, 비작성자 403 | IMPLEMENT | UI_DIRECT | SCR-005(내 활동 탭) | 대상 글은 SCR-004 상세로 연결 |
| REQ-FUNC-037 | 종료일 경과 시 자동 CLOSED(조회 시 계산) | IMPLEMENT | UI_STATE | SCR-004 | 목록에서 자동 제외 |
| REQ-FUNC-038 | 작성자 수동 마감·수정·삭제 | IMPLEMENT | UI_DIRECT | SCR-005(내 활동 탭) | 수정 시 SCR-003 동행 작성 탭 재사용 |
| REQ-FUNC-039 | 신고 접수(사유+설명), 접수번호 표시 | IMPLEMENT | UI_DIRECT | SCR-004(상세 패널) | - |
| REQ-FUNC-040 | 사용자 차단·해제, 상호 노출 제한 | IMPLEMENT | UI_DIRECT | SCR-005(내 활동 탭) | 진입점은 SCR-004 상세 패널 |
| REQ-FUNC-041 | 관리자 신고 큐(상태 필터) | IMPLEMENT | UI_DIRECT | SCR-005(관리자 탭) | - |
| REQ-FUNC-042 | 신고 처리(상태 변경·게시물 숨김) | IMPLEMENT | UI_DIRECT | SCR-005(관리자 탭) | - |
| REQ-FUNC-043 | 참가 요청·신고 처리 알림(Toast/화면 상태) | IMPLEMENT | UI_STATE | SCR-004(주 발생 지점), SCR-005(상태 반영) | - |
| REQ-FUNC-044 | RLS로 비공개 데이터 접근 제한 | IMPLEMENT | NON_UI | - | - |
| REQ-FUNC-045 | 탈퇴 시 즉시 비식별화+30일 내 삭제 | EXCLUDED | OPERATIONS | - | 수동 운영 대응으로 대체, 화면 요소 없음 |

### 3-5. F5 Country Safety → SCR-001 (안전정보 Drawer/Modal)

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-046 | 게시 해외 국가 100% 안전 페이지 보유 | IMPLEMENT | OPERATIONS | - | 콘텐츠 커버리지 확인, 결과는 SCR-001 안전정보 Drawer로 반영 |
| REQ-FUNC-047 | 8개 필수 카테고리 제공 | IMPLEMENT | UI_DIRECT | SCR-001 | 안전정보 Drawer 구성요소 |
| REQ-FUNC-048 | 출처명·URL·확인일·편집자 기록 | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-049 | 외교부 원문 링크 새 탭 | IMPLEMENT | UI_DIRECT | SCR-001 | 외교부 해외안전여행(새 탭) |
| REQ-FUNC-050 | 확인 후 7일 초과 시 stale 경고 | IMPLEMENT | UI_STATE | SCR-001 | 렌더링 시점 계산 |
| REQ-FUNC-051 | 중대 경보 상단 텍스트 표시 | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-052 | 국가 전체/지역 경보 범위 구분 | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-053 | 현지·영사 긴급연락처 표시 | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-054 | 공식 판단 대체 아님 고지 | IMPLEMENT | UI_DIRECT | SCR-001, SCR-003(항공/숙소 요약) | - |
| REQ-FUNC-055 | Editor 작성·검수·게시·보관 워크플로 | EXCLUDED | OPERATIONS | - | 개발자가 데이터 직접 관리, 화면 요소 없음 |
| REQ-FUNC-056 | 안전정보 변경 이력 보존 | EXCLUDED | OPERATIONS | - | Git 커밋 이력으로 대체, 화면 요소 없음 |

### 3-6. F6 About free_traveler → SCR-002

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-057 | 대표명·50+ Trips·30+ Countries 표시 | IMPLEMENT | UI_DIRECT | SCR-002 | - |
| REQ-FUNC-058 | 소개문·철학·편집 원칙 | IMPLEMENT | UI_DIRECT | SCR-002 | - |
| REQ-FUNC-059 | 방문 권역/30개국 이상 목록 | IMPLEMENT | UI_DIRECT | SCR-002 | - |
| REQ-FUNC-060 | 대표 여행 타임라인 | IMPLEMENT | UI_DIRECT | SCR-002 | - |
| REQ-FUNC-061 | 대표 이미지 대체텍스트·출처·작가·라이선스 | EXCLUDED | UI_DIRECT | - | 대체텍스트만 SCR-002 이미지에 포함, 출처·작가·라이선스는 미구현 |
| REQ-FUNC-062 | 문의·SNS 링크 | IMPLEMENT | UI_DIRECT | SCR-002 | 외부 링크(새 탭) |
| REQ-FUNC-063 | 추천 여행지 6개 연결 | IMPLEMENT | UI_DIRECT | SCR-002 | SCR-001 여행지 Drawer로 이동 |

### 3-7. F7 Common, Admin, Governance → SCR-005(관리자) / 전체 화면 공통

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-FUNC-064 | 전역 내비게이션·푸터 | IMPLEMENT | UI_DIRECT | 전체 화면 공통 | 5개 Screen 간 이동 제공 |
| REQ-FUNC-065 | 320px~데스크톱 반응형 | IMPLEMENT | UI_STATE | 전체 화면 공통 | - |
| REQ-FUNC-066 | 이메일 가입·인증·로그인·로그아웃·재설정 | IMPLEMENT | UI_DIRECT | SCR-005(로그인/인증 탭) | - |
| REQ-FUNC-067 | 여행지·안전정보 통합 검색 | IMPLEMENT | UI_DIRECT | SCR-001 | - |
| REQ-FUNC-068 | 여행지 즐겨찾기(localStorage, 중복 방지) | IMPLEMENT | UI_DIRECT | SCR-001(토글), SCR-005(내 활동 탭 목록) | - |
| REQ-FUNC-069 | 공개 페이지 URL 공유 | IMPLEMENT | UI_DIRECT | SCR-001, SCR-004 | - |
| REQ-FUNC-070 | title/description/canonical/OG 메타데이터 | IMPLEMENT | NON_UI | - | 전체 화면 공통, 비가시 head 메타데이터 |
| REQ-FUNC-071 | 폼·클릭·조회 이벤트 기록 | EXCLUDED | OPERATIONS | - | 미구현, 화면 요소 없음 |
| REQ-FUNC-072 | Editor/Admin 콘텐츠 CRUD+미리보기 | EXCLUDED | OPERATIONS | - | 개발자 직접 데이터 관리, 화면 요소 없음 |
| REQ-FUNC-073 | 미디어 업로드 시 출처·작가·라이선스 필수 입력 | EXCLUDED | OPERATIONS | - | 업로드 기능 자체 없음 |
| REQ-FUNC-074 | 게시 전 완전성 게이트 자동 실행 | EXCLUDED | OPERATIONS | - | 수동 체크리스트로 대체 |
| REQ-FUNC-075 | 안전정보 stale 현황 대시보드 | EXCLUDED | OPERATIONS | - | SCR-001 렌더링 계산(REQ-FUNC-050)으로 대체, 별도 대시보드 없음 |
| REQ-FUNC-076 | 관리자 변경·신고 처리 감사 로그 | EXCLUDED | OPERATIONS | - | 미구현, 화면 요소 없음 |
| REQ-FUNC-077 | Admin 외부 URL 허용목록(HTTPS) 설정 | IMPLEMENT | UI_DIRECT | SCR-005(관리자 탭) | - |
| REQ-FUNC-078 | 404/500/권한없음/외부연결실패 복구 행동 | IMPLEMENT | UI_DIRECT | 전체 화면 공통 | 홈(SCR-001)/이전/재시도 중 최소 1개 |
| REQ-FUNC-079 | 폼·모달·탭·알림 HTML 의미·ARIA 상태 | IMPLEMENT | UI_STATE | 전체 화면 공통 | - |
| REQ-FUNC-080 | 정책 고지+동행 안전수칙 동의 기록 | IMPLEMENT | UI_DIRECT | SCR-003(동행 작성 탭 동의 체크박스) | 정책 본문은 전체 화면 공통 푸터 링크 |

---

## 4. REQ-NF-001~034 배치

### 4-1. Performance

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-001 | LCP p75 ≤2.5s | IMPLEMENT | NON_UI | - | 전체 화면 공통 성능 목표 |
| REQ-NF-002 | INP p75 ≤200ms | IMPLEMENT | NON_UI | - | - |
| REQ-NF-003 | CLS p75 ≤0.1 | IMPLEMENT | NON_UI | - | - |
| REQ-NF-004 | 필터 응답 p95≤1s(동시 50명) | IMPLEMENT | NON_UI | - | SCR-001/SCR-004 필터 대상 |
| REQ-NF-005 | 쓰기 API 응답 p95≤3s | IMPLEMENT | NON_UI | - | SCR-003/SCR-004 쓰기 동작 대상 |
| REQ-NF-006 | 이미지 반응형·lazy load, LCP priority | IMPLEMENT | UI_STATE | 전체 화면 공통 | - |
| REQ-NF-007 | 배포 전 Lighthouse CI 게이트 | EXCLUDED | OPERATIONS | - | 수동 점검으로 대체 |

### 4-2. Reliability and Recovery

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-008 | 월간 가용성 ≥99.5% | EXCLUDED | OPERATIONS | - | - |
| REQ-NF-009 | 내부 API 5xx ≤0.5% | EXCLUDED | OPERATIONS | - | - |
| REQ-NF-010 | DB 백업 RPO/RTO | EXCLUDED | OPERATIONS | - | - |
| REQ-NF-011 | 외부 링크 주1회 자동 검사+Admin 알림 | EXCLUDED | OPERATIONS | - | - |

### 4-3. Security and Privacy

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-012 | TLS 1.2 이상 | IMPLEMENT | NON_UI | - | - |
| REQ-NF-013 | 인증·역할·RLS 서버 검증 | IMPLEMENT | NON_UI | - | - |
| REQ-NF-014 | CSRF 방어·SameSite 쿠키 | IMPLEMENT | NON_UI | - | - |
| REQ-NF-015 | 입력 검증·이스케이프, 저장 XSS 차단 | IMPLEMENT | NON_UI | - | - |
| REQ-NF-016 | 비밀키 환경변수 관리 | IMPLEMENT | NON_UI | - | - |
| REQ-NF-017 | 항공·호텔 원시 입력값 미보존 | IMPLEMENT | NON_UI | - | REQ-FUNC-017/025와 동일 성격 |
| REQ-NF-018 | 개인정보 내보내기·탈퇴·삭제 요청 | EXCLUDED | OPERATIONS | - | - |

### 4-4. Safety and Moderation

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-019 | 신고 접수 응답 p95≤3s | IMPLEMENT | NON_UI | - | SCR-004 신고 흐름 대상 |
| REQ-NF-020 | 신고 1차 검토 24h 이내 90% | EXCLUDED | OPERATIONS | - | - |
| REQ-NF-021 | 글·요청·신고 속도 제한(429) | EXCLUDED | NON_UI | - | - |
| REQ-NF-022 | Moderator 조치 추적 가능성 | EXCLUDED | OPERATIONS | - | - |

### 4-5. Accessibility

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-023 | WCAG 2.2 Level AA 목표 | IMPLEMENT | UI_STATE | 전체 화면 공통 | - |
| REQ-NF-024 | 자동 접근성 검사(axe) | EXCLUDED | OPERATIONS | - | - |
| REQ-NF-025 | 키보드·스크린리더 수동 검사 | IMPLEMENT | OPERATIONS | - | 전체 화면 공통 대상 QA 활동 |

### 4-6. Content, Freshness, SEO, Copyright

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-026 | 여행지 콘텐츠 완전성 100% | IMPLEMENT | OPERATIONS | - | 결과는 SCR-001 콘텐츠에 반영 |
| REQ-NF-027 | 해외 국가 안전정보 커버리지 100% | IMPLEMENT | OPERATIONS | - | 결과는 SCR-001 안전정보 Drawer에 반영 |
| REQ-NF-028 | 안전정보 최신 확인 7일 이내 95%, 초과 시 경고 100% | IMPLEMENT | UI_STATE | SCR-001 | 경고 로직은 REQ-FUNC-050과 동일 |
| REQ-NF-029 | 미디어 라이선스 메타데이터 100% | EXCLUDED | OPERATIONS | - | - |
| REQ-NF-030 | 공개 페이지 SEO 메타데이터 누락 0건 | IMPLEMENT | NON_UI | - | 전체 화면 공통, REQ-FUNC-070과 동일 |

### 4-7. Maintainability, Monitoring, Cost

| ID | 요구사항 요약 | PROJECT_SCOPE | UI 분류 | 배치 Screen | 비고 |
|---|---|---|---|---|---|
| REQ-NF-031 | TypeScript strict·lint, main 병합 전 통과 | IMPLEMENT | NON_UI | - | - |
| REQ-NF-032 | 구조화 로그 | EXCLUDED | NON_UI | - | - |
| REQ-NF-033 | 5xx>1% 또는 외부 링크 실패 시 알림 | EXCLUDED | OPERATIONS | - | - |
| REQ-NF-034 | MVP 월 인프라 비용 ≤100,000원 | IMPLEMENT | OPERATIONS | - | - |

---

## 5. 집계 검증

### 5-1. 총 개수

| 구분 | 개수 |
|---|---:|
| REQ-FUNC-001~080 | 80 |
| REQ-NF-001~034 | 34 |
| **합계** | **114** |

### 5-2. PROJECT_SCOPE 분류별 개수

| 분류 | REQ-FUNC | REQ-NF | 합계 |
|---|---:|---:|---:|
| IMPLEMENT | 69 | 21 | 90 |
| EXCLUDED | 11 | 13 | 24 |
| 합계 | 80 | 34 | 114 |

### 5-3. UI 분류별 개수

| UI 분류 | REQ-FUNC | REQ-NF | 합계 | 비고 |
|---|---:|---:|---:|---|
| UI_DIRECT | 56 | 0 | 56 | 화면에 직접 나타나는 구성요소(EXCLUDED 2건 포함: REQ-FUNC-007, 061 — 대체텍스트 외 출처·작가·라이선스는 미배치) |
| UI_STATE | 9 | 3 | 12 | 화면 상태·동작 로직 |
| NON_UI | 4 | 16 | 20 | 비가시 기술 요건 |
| OPERATIONS | 11 | 15 | 26 | 콘텐츠·운영 프로세스 |
| **합계** | **80** | **34** | **114** | - |

### 5-4. Screen별 배치 개수(전체 화면 공통 및 미배치 `-` 제외)

| Screen | 주로 배치된 요구사항 수(대표 그룹) |
|---|---|
| SCR-001 | F1(10) + F5 UI 항목(8) + F7 일부(067, 068, 069) 등 |
| SCR-002 | F6(7, 그 중 1건 EXCLUDED로 미배치) |
| SCR-003 | F2(8) + F3(8) + F4 작성 관련(027, 031, 032, 054, 080) |
| SCR-004 | F4 조회·상세 관련(030, 033, 034, 035, 037, 039, 043) |
| SCR-005 | F4 계정·관리 관련(028, 029, 036, 038, 040, 041, 042) + F7 관리자(066, 077) |
| 전체 화면 공통 | F7 공통 UI(064, 065, 078, 079) + NF 접근성/이미지(NF-006, NF-023) |
| `-`(미배치, EXCLUDED 또는 순수 OPERATIONS/NON_UI) | 나머지 항목 |

모든 REQ-FUNC-001~080, REQ-NF-001~034가 정확히 한 번씩 3·4장에 등장하며, 삭제되거나 중복 기록된 항목은 없다. EXCLUDED로 유지된 항목은 본 문서에서도 EXCLUDED로 기록되었으며 구현 범위로 변경되지 않았다. 배치된 디자인 Screen은 SCR-001~SCR-005 5개로 고정되어 있으며 이를 초과하는 별도 핵심 Screen은 정의하지 않았다.
