# Free Traveler — Project Scope v1.0

- **Document ID:** SCOPE-TRAVEL-001
- **기반 문서:** `docs/01_PRD.md` (PRD-TRAVEL-001), `docs/02_SRS_BASELINE.md` (SRS-TRAVEL-001)
- **작성일:** 2026-09-10
- **상태:** Implementation Scope Baseline
- **적용 스택:** Next.js 16 (App Router) + React 19 + TypeScript + Tailwind CSS v4, Supabase(Auth·PostgreSQL), Vercel

이 문서는 SRS-TRAVEL-001의 요구사항(REQ-FUNC-001~080, REQ-NF-001~034)을 현재 저장소(`package.json`, `src/app`)를 기준으로 실제 구현할 범위와 구현하지 않는 범위로 재분류한다. 모든 요구사항 ID는 삭제 없이 한 번씩 기록하며, 각 행에 분류(IMPLEMENT/EXCLUDED), 처리 방법, 확인 방법을 명시한다.

---

## 1. 요구사항 상태 정의

| 상태 | 의미 |
|---|---|
| **IMPLEMENT** | 구현하고 테스트한다. SRS 원문 대비 축소된 방식으로 구현하는 경우 처리 방법에 축소 내용을 명시한다. |
| **EXCLUDED** | 만들지 않는다. 처리 방법에 제외 이유를 기록한다. |

---

## 2. 역할·권한 단순화

SRS 2.2의 Guest/Adult Member/Editor/Moderator/Admin 5단계 권한 매트릭스를 다음 3단계로 단순화한다.

| 역할 | 대응 |
|---|---|
| Guest | 비로그인 사용자. 열람만 가능 |
| Member | Supabase Auth 이메일 인증 + 성인 확인 완료 사용자. 동행글·참가 요청·신고·차단·즐겨찾기 가능 |
| Admin | 단일 관리자 역할. **신고 상태 변경과 항공·호텔 외부 URL 설정만** 담당. SRS의 Editor(콘텐츠 CRUD)·Moderator(세분화된 제재) 역할은 별도로 구현하지 않는다 |

콘텐츠(여행지·안전정보·대표 소개)는 관리자 UI가 아니라 개발자가 `src/data`를 직접 수정하는 방식으로 관리한다.

---

## 3. 화면 구성

### 3-1. 핵심 화면 4개

| 화면 | 라우트 | 설명 |
|---|---|---|
| 홈 | `/` | 가치 제안, 추천 여행지, 전역 내비게이션 진입점 |
| 여행지 | `/destinations`, `/destinations/domestic`, `/destinations/overseas`, `/destinations/[slug]` | 목록·필터·검색·상세, 안전정보 연결 |
| 항공·호텔 찾기 | `/flights`, `/hotels` | 조건 입력→검증→요약→외부 이동 |
| 동행 찾기 | `/mates`, `/mates/[id]`, `/mates/new` | 모집글 목록·상세·작성, 참가 요청 |

### 3-2. 보조 화면 1개

| 화면 | 라우트 | 설명 |
|---|---|---|
| 마이페이지 | `/my/*`(내 활동: 내 글·요청·차단·즐겨찾기), `/admin/*`(신고 상태·외부 URL 설정) | 로그인 사용자 활동 관리 + 축소된 관리자 탭 |

국가별 안전정보(`/safety/[countryCode]`)와 대표 소개(`/about`), 인증 화면(`/auth/*`)은 위 5개 화면 안에서 콘텐츠·진입점으로 제공되며 별도의 대형 화면 그룹을 구성하지 않는다.

---

## 4. 구현 방식 원칙

| 영역 | 방식 |
|---|---|
| 여행지·안전정보·대표 콘텐츠 | `src/data`의 정적 TypeScript/JSON 데이터. Supabase 테이블 대신 빌드에 포함 |
| 즐겨찾기 | 브라우저 `localStorage`. 서버 저장 없음 |
| 참가 요청·신고·상태 변경 알림 | 실제 이메일 발송 대신 Toast 또는 화면 내 상태 표시 |
| 동행 모집글 자동 마감 | 배치 작업 없이, 조회·렌더링 시점에 `end_date` 경과 여부를 계산해 모집중 목록에서 제외 |
| 안전정보 최신성(stale) | 배치 작업 없이, 렌더링 시점에 `verified_at`과 현재 시각 차이를 계산해 7일 초과 시 경고 표시 |
| 이미지 | 일반 인터넷 이미지 URL과 `alt` 텍스트만 사용. 출처·작가·라이선스 메타데이터 관리 체계는 구축하지 않음 |
| 관리자 | 신고 상태 변경(숨김/기각/처리완료)과 항공·호텔 외부 URL 설정(HTTPS 허용목록 검증)만 제공 |
| 인증·동행 데이터 | Supabase Auth + PostgreSQL + RLS 사용 (콘텐츠 정적 데이터와 달리 실제 쓰기가 필요한 영역) |

---

## 5. 일반 제외 기능

REQ ID에 직접 매핑되지 않는 인프라·프로세스 차원의 제외 사항이다. REQ 단위 제외 사유는 6·7장 표에 기록한다.

| 제외 항목 | 사유 |
|---|---|
| 전체 콘텐츠 CMS (Editor 작성·검수·게시 워크플로, DRAFT/REVIEW/PUBLISHED/ARCHIVED 상태 전이) | 콘텐츠 규모가 정적 데이터로 충분히 관리 가능한 MVP 범위이며, 관리자 역할을 신고·외부 URL로 한정했기 때문 |
| 미디어 업로드·라이선스 승인 워크플로 | 이미지 정책을 URL+alt 텍스트로 단순화했기 때문에 별도 업로드·심사 파이프라인 불필요 |
| 범용 감사 로그(AUDIT_LOG, before/after 이력) | 관리자 조작 범위가 신고 상태·외부 URL 설정으로 한정되어 있어 별도 이력 저장 체계 없이도 현재 상태 필드만으로 운영 가능 |
| 자동 백업·장애 알림·부하 테스트 | 운영 모니터링·재해복구 체계 구축은 이번 구현 범위 밖. Vercel/Supabase 기본 제공 수준에 의존 |
| 외부 이메일 사업자 연동 | 알림을 Toast/화면 상태로 대체하기로 결정했으므로 이메일 발송 인프라 불필요 |
| EC2·AWS 인프라 | 배포는 Vercel, 데이터는 Supabase로 한정하며 별도 클라우드 인프라를 구성하지 않음 |
| 무인 자동 Merge Runner | 코드 병합은 사람이 검토 후 수행하며 자동 병합 파이프라인을 구성하지 않음 |

---

## 6. REQ-FUNC-001~080 매핑

### 6-1. F1 Destination Guide

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-FUNC-001 | 국내·해외 여행지 목록 구분 | IMPLEMENT | `src/data` 정적 목록을 국내/해외로 구분, 탭 전환 시 해당 구분만 필터링 | Playwright SM-01 |
| REQ-FUNC-002 | 국가·도시·계절·테마·기간 필터(AND) | IMPLEMENT | 클라이언트 측 정적 배열 필터링. 다중 조건 AND 결합 | Playwright SM-01 |
| REQ-FUNC-003 | 키워드 검색(한글 부분 일치) | IMPLEMENT | 클라이언트 측 문자열 포함 검색 | 수동 QA |
| REQ-FUNC-004 | 상세 페이지 필수 콘텐츠 필드 전체 표시 | IMPLEMENT | 정적 데이터 스키마에 필수 필드를 타입으로 강제. 게시 상태 전이 게이트는 없음(모든 커밋 데이터가 곧 게시본) | 수동 콘텐츠 체크리스트 |
| REQ-FUNC-005 | 빈 결과 안내+초기화 버튼 | IMPLEMENT | 결과 0건 시 안내 UI와 필터 초기화 버튼 렌더 | Playwright SM-01 |
| REQ-FUNC-006 | 해외 상세→국가 안전정보 연결 | IMPLEMENT | `country_code`로 안전정보 정적 데이터와 상호 참조 | 수동 QA(데이터 일치 확인) |
| REQ-FUNC-007 | 대표 이미지 대체텍스트·출처·작가·라이선스 연결 | EXCLUDED | `alt` 텍스트만 관리. 출처·작가·라이선스 메타데이터는 저장하지 않음(이미지 정책 단순화, 미디어 워크플로 제외) | N/A |
| REQ-FUNC-008 | MVP 게시 수량(국내 10+, 해외 15개국 30도시+) 검증 | IMPLEMENT | 정적 데이터 개수를 수동으로 집계·확인. 자동 출시 게이트는 없음 | 수동 콘텐츠 체크리스트 |
| REQ-FUNC-009 | 관련 여행지 최대 6개 추천 | IMPLEMENT | 같은 국가/테마 기준 정적 데이터 필터, 현재 여행지 제외 | 수동 QA |
| REQ-FUNC-010 | 필터 상태 URL query 반영·복원 | IMPLEMENT | 허용된 필터 키만 query string으로 직렬화/역직렬화 | Playwright SM-01 |

### 6-2. F2 Flight Link-out

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-FUNC-011 | 국가·지역·출발일·귀국일 필수 입력 | IMPLEMENT | 4개 필드를 라벨·도움말·오류 영역과 함께 클라이언트 폼으로 구현 | Playwright SM-02 |
| REQ-FUNC-012 | 국가 변경 시 하위 지역만 선택·초기화 | IMPLEMENT | 국가 선택값에 종속된 지역 옵션 구성, 국가 변경 시 지역값 리셋 | Playwright SM-02 |
| REQ-FUNC-013 | 과거 출발일·역전 날짜 차단 | IMPLEMENT | 클라이언트 측 날짜 검증(오늘 이전, 귀국일<출발일 차단) | Playwright SM-02(경계값) |
| REQ-FUNC-014 | 유효 입력 후 요약 단계 표시 | IMPLEMENT | 검증 통과 시 요약 화면 전환, 세션 동안 폼 값 유지(브라우저 메모리) | Playwright SM-02 |
| REQ-FUNC-015 | "입력값 비전달" 고지 표시 | IMPLEMENT | 폼과 요약 화면에 고정 안내 문구 렌더 | 수동 QA |
| REQ-FUNC-016 | 외부 항공 URL 새 탭, noopener/noreferrer | IMPLEMENT | 환경변수 `FLIGHT_OUTBOUND_URL`을 query 없이 새 탭으로 열기 | Playwright SM-02 |
| REQ-FUNC-017 | 항공 입력값 서버 미저장 | IMPLEMENT | 전 과정 클라이언트 상태로만 처리, 서버 API 호출 없음 | 코드 리뷰 + 네트워크 탭 수동 확인 |
| REQ-FUNC-018 | 외부 URL 오류 시 차단+재시도 안내 | IMPLEMENT | URL 미설정/허용목록 밖일 때 인라인 오류와 재시도 버튼 표시 | 수동 QA |

### 6-3. F3 Hotel Link-out

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-FUNC-019 | 국가·지역·체크인·체크아웃 필수 입력 | IMPLEMENT | REQ-FUNC-011과 동일 패턴 적용 | Playwright SM-03 |
| REQ-FUNC-020 | 국가 변경 시 하위 지역만 선택 | IMPLEMENT | REQ-FUNC-012와 동일 패턴 | Playwright SM-03 |
| REQ-FUNC-021 | 과거 체크인·체크아웃≤체크인 차단 | IMPLEMENT | 클라이언트 측 날짜 검증 | Playwright SM-03(경계값) |
| REQ-FUNC-022 | 유효 입력 후 요약 표시 | IMPLEMENT | REQ-FUNC-014와 동일 패턴 | Playwright SM-03 |
| REQ-FUNC-023 | 비전달 고지 표시 | IMPLEMENT | REQ-FUNC-015와 동일 패턴 | 수동 QA |
| REQ-FUNC-024 | 외부 호텔 URL 새 탭, noopener/noreferrer | IMPLEMENT | 환경변수 `HOTEL_OUTBOUND_URL` 사용 | Playwright SM-03 |
| REQ-FUNC-025 | 호텔 입력값 서버 미저장 | IMPLEMENT | REQ-FUNC-017과 동일 | 코드 리뷰 + 네트워크 탭 수동 확인 |
| REQ-FUNC-026 | 호텔 URL 오류 시 차단+재시도 | IMPLEMENT | REQ-FUNC-018과 동일 패턴 | 수동 QA |

### 6-4. F4 Travel Mate

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-FUNC-027 | 동행 쓰기에 이메일 인증 세션 요구 | IMPLEMENT | Supabase Auth 세션 미존재 시 서버에서 차단·리다이렉트 | Playwright SM-04/05 |
| REQ-FUNC-028 | 성인 확인 상태 요구, 생년월일 미저장 | IMPLEMENT | `is_adult`, `adult_verified_at`만 저장, 생년월일 컬럼 없음 | 코드 리뷰(스키마 확인)+Playwright SM-04 |
| REQ-FUNC-029 | 동행 프로필(닉네임·연령대·성별·스타일·자기소개) | IMPLEMENT | 프로필 폼에 필수/선택 필드 구분 적용 | Playwright SM-04 |
| REQ-FUNC-030 | 국가·지역·기간·연령대·성별·스타일·상태 필터 | IMPLEMENT | Supabase 쿼리 + 차단 사용자 글 제외 필터. 동시사용자 부하 테스트는 제외(부하 테스트 제외 방침) | 수동 QA(기능 정확성) |
| REQ-FUNC-031 | 모집글 필수 필드+검증(날짜 역전·과거 종료일 차단) | IMPLEMENT | 작성 폼 검증 로직 | Playwright SM-05 |
| REQ-FUNC-032 | 공개 연락처(전화·이메일·메신저 ID) 탐지·차단 | IMPLEMENT | 정규식 기반 패턴 탐지, 제출 전 차단+수정 안내. 탐지율은 큐레이션된 테스트셋으로 확인(통계적 실측 아님) | Playwright SM-05(테스트셋 케이스) |
| REQ-FUNC-033 | 모집글에 연락처 비노출 | IMPLEMENT | API/렌더링 응답에 이메일·전화번호 필드 미포함 | 코드 리뷰(응답 스키마 확인) |
| REQ-FUNC-034 | 비공개 참가 메시지(500자) PENDING 저장 | IMPLEMENT | Supabase 테이블 + RLS로 작성자·요청자만 열람 | Playwright SM-06 |
| REQ-FUNC-035 | 동일 사용자 중복 PENDING/ACCEPTED 차단 | IMPLEMENT | DB unique 제약 + UI 오류 처리 | 수동 QA(DB 제약 확인) |
| REQ-FUNC-036 | 작성자 승인/거절, 비작성자 403 | IMPLEMENT | RLS + 서버 액션으로 소유자만 상태 변경 허용 | Playwright SM-06 |
| REQ-FUNC-037 | 종료일 경과 시 자동 CLOSED 전환 | IMPLEMENT | 배치 없이 조회·렌더링 시점에 `end_date` 경과분을 CLOSED로 간주해 공개 목록에서 제외(구현 방식 3장) | 수동 QA(종료일 지난 글 미노출 확인) |
| REQ-FUNC-038 | 작성자 수동 마감·수정·삭제, 승인자 존재 시 경고 | IMPLEMENT | 작성자 전용 관리 UI + 일정 변경 시 확인 다이얼로그 | 수동 QA |
| REQ-FUNC-039 | 신고 접수(사유 코드+설명), 접수번호 표시 | IMPLEMENT | Supabase insert 후 report id·시각 즉시 반환 | Playwright SM-07 |
| REQ-FUNC-040 | 사용자 차단·해제, 상호 노출 제한 | IMPLEMENT | USER_BLOCK 테이블 + 쿼리·RLS 단계에서 상호 제외 | Playwright SM-07 |
| REQ-FUNC-041 | 관리자 신고 큐(상태 필터) | IMPLEMENT | Admin 역할에 한해 OPEN/RESOLVED/DISMISSED 상태 필터가 있는 목록 제공. Moderator 우선순위·증거 관리 등 세부 기능은 축소 | 수동 QA |
| REQ-FUNC-042 | 신고 처리(경고·숨김·제한·기각) 기록 | IMPLEMENT | 관리자는 신고 상태 변경(RESOLVED/DISMISSED)과 대상 게시물 숨김만 수행. 경고·계정 일시제한 등 세분화된 제재와 감사 로그는 제외(5장) | 수동 QA |
| REQ-FUNC-043 | 참가 요청·신고 처리 알림(인앱+선택적 이메일) | IMPLEMENT | 실제 이메일 대신 Toast/화면 상태로 알림 대체(외부 이메일 연동 제외) | 수동 QA |
| REQ-FUNC-044 | RLS로 비공개 데이터 접근 제한 | IMPLEMENT | Supabase RLS 정책으로 본인·상대방·Admin만 열람 | 권한별 부정 접근 테스트(수동) |
| REQ-FUNC-045 | 탈퇴 시 즉시 비식별화+30일 내 삭제 | EXCLUDED | 자동 비식별화·법적 보존 예외 처리 파이프라인 미구현. 로그아웃/계정 비활성화 수준으로 제한(운영 대응은 수동) | N/A |

### 6-5. F5 Country Safety

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-FUNC-046 | 게시 해외 국가 100% 안전 페이지 보유 | IMPLEMENT | 15개국 모두에 대해 `src/data` 안전정보 레코드 작성 | 수동 데이터 커버리지 확인 |
| REQ-FUNC-047 | 8개 필수 카테고리 제공 | IMPLEMENT | 정적 데이터 스키마로 8개 카테고리 필드 강제 | 수동 콘텐츠 체크리스트 |
| REQ-FUNC-048 | 출처명·URL·확인일·편집자 기록 | IMPLEMENT | 정적 데이터 필드로 기록(편집자는 고정 값 사용, 별도 편집자 계정 체계 없음) | 수동 콘텐츠 체크리스트 |
| REQ-FUNC-049 | 외교부 원문 링크 새 탭 | IMPLEMENT | MOFA URL을 noopener/noreferrer 새 탭으로 연결 | Playwright SM-08 |
| REQ-FUNC-050 | 확인 후 7일 초과 시 stale 경고 | IMPLEMENT | 렌더링 시점에 `verified_at` 대비 경과일 계산(구현 방식 3장) | Playwright SM-08(날짜 mock) |
| REQ-FUNC-051 | 중대 경보 상단 텍스트 표시 | IMPLEMENT | 색상 외 텍스트 라벨 병기, 상단 배치 | 수동 QA |
| REQ-FUNC-052 | 국가 전체/지역 경보 범위 구분 | IMPLEMENT | `scope_type`/`scope_text` 정적 필드로 구분 | 수동 콘텐츠 체크리스트 |
| REQ-FUNC-053 | 현지·영사 긴급연락처 표시 | IMPLEMENT | 정적 데이터의 emergency_contacts 필드 렌더 | 수동 QA |
| REQ-FUNC-054 | 공식 판단 대체 아님 고지 | IMPLEMENT | 안전 페이지·항공 요약 화면에 고정 고지 문구 | 수동 QA |
| REQ-FUNC-055 | Editor/Admin 작성·검수·게시·보관 워크플로 | EXCLUDED | 안전정보는 개발자가 `src/data`를 직접 작성·수정. 별도 작성-검수-게시 UI는 제공하지 않음(전체 콘텐츠 CMS 제외) | N/A |
| REQ-FUNC-056 | 안전정보 변경 이력(before/after/사유) 보존 | EXCLUDED | 별도 변경 이력 테이블 미구현. Git 커밋 이력으로 대체(범용 감사 로그 제외) | N/A |

### 6-6. F6 About free_traveler

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-FUNC-057 | 대표명·50+ Trips·30+ Countries 표시 | IMPLEMENT | 단일 정적 데이터 소스를 대표 페이지·홈 카드가 공유 참조 | 수동 QA(값 일치 확인) |
| REQ-FUNC-058 | 소개문·철학·편집 원칙 표시 | IMPLEMENT | PRD 6-2 확정 소개문을 정적 데이터로 반영 | 수동 QA |
| REQ-FUNC-059 | 방문 권역 지도/30개국 이상 목록 | IMPLEMENT | 국가 목록 UI(지도 대신 목록/그리드로 단순화 가능) | 수동 QA |
| REQ-FUNC-060 | 대표 여행 타임라인 | IMPLEMENT | 정적 데이터의 타임라인 배열 렌더 | 수동 QA |
| REQ-FUNC-061 | 대표 이미지 대체텍스트·출처·작가·라이선스 | EXCLUDED | `alt` 텍스트만 관리, 출처·작가·라이선스 메타데이터는 저장하지 않음(REQ-FUNC-007과 동일 정책) | N/A |
| REQ-FUNC-062 | 관리자 설정 기반 문의·SNS 링크 | IMPLEMENT | 코드 내 정적 설정 값으로 관리(별도 관리자 편집 UI 없음), 빈 값 미노출·허용 프로토콜만 렌더 | 수동 QA |
| REQ-FUNC-063 | 대표 추천 여행지 6개 연결 | IMPLEMENT | 정적 slug 목록으로 여행지 상세 연결 | 수동 QA |

### 6-7. F7 Common, Admin, Governance

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-FUNC-064 | 전역 내비게이션·푸터 | IMPLEMENT | 공통 레이아웃에 내비게이션·푸터 배치, 핵심 기능 2회 이내 도달 | 수동 QA |
| REQ-FUNC-065 | 320px~데스크톱 반응형 | IMPLEMENT | Tailwind 반응형 유틸리티 사용 | 수동 QA(브라우저 반응형 도구) |
| REQ-FUNC-066 | 이메일 가입·인증·로그인·로그아웃·비밀번호 재설정 | IMPLEMENT | Supabase Auth 이메일 플로우 사용(항목 6) | Playwright SM-04 |
| REQ-FUNC-067 | 여행지·안전정보 통합 검색 | IMPLEMENT | 두 정적 데이터셋을 합쳐 클라이언트 키워드 검색, 결과 유형 라벨 표시 | 수동 QA |
| REQ-FUNC-068 | 여행지 즐겨찾기(중복 방지) | IMPLEMENT | `localStorage`에 id 집합 저장(구현 방식 3장), 중복 추가 방지 | 수동 QA(localStorage 확인) |
| REQ-FUNC-069 | 공개 페이지 URL 공유 | IMPLEMENT | Web Share API 우선 사용, 실패 시 URL 클립보드 복사 폴백 | 수동 QA |
| REQ-FUNC-070 | title/description/canonical/OG 메타데이터 | IMPLEMENT | Next.js Metadata API로 페이지별 메타 설정 | 코드 리뷰(메타 태그 확인) |
| REQ-FUNC-071 | 폼·클릭·조회 이벤트 기록(정확 날짜·자유서술 제외) | EXCLUDED | 커스텀 행동 분석 이벤트 파이프라인 미구축. 운영 로그·분석 도구는 범위 밖(5장) | N/A |
| REQ-FUNC-072 | Editor/Admin 콘텐츠 CRUD+미리보기(DRAFT/REVIEW/PUBLISHED/ARCHIVED) | EXCLUDED | 여행지 콘텐츠는 `src/data` 정적 파일로 개발자가 직접 관리. 별도 CRUD/미리보기 UI 미제공(전체 콘텐츠 CMS 제외) | N/A |
| REQ-FUNC-073 | 미디어 업로드 시 출처·작가·라이선스 필수 입력 | EXCLUDED | 이미지 업로드 기능 자체가 없음(URL+alt만 사용). 미디어 업로드·라이선스 워크플로 제외 | N/A |
| REQ-FUNC-074 | 게시 전 완전성 게이트 자동 실행 | EXCLUDED | 자동 게이트 시스템 없음. 정적 데이터 작성 시 수동 체크리스트로 대체 | N/A |
| REQ-FUNC-075 | 안전정보 stale 현황 대시보드 | EXCLUDED | 관리자 범위를 신고·외부 URL로 한정. stale 표시는 각 페이지 렌더링 시 계산(REQ-FUNC-050)으로 충분히 처리 | N/A |
| REQ-FUNC-076 | 관리자 변경·신고 처리·권한 변경 감사 로그 | EXCLUDED | 범용 감사 로그 미구현. REPORT 테이블의 현재 상태 필드만 유지(5장) | N/A |
| REQ-FUNC-077 | Admin의 항공·호텔 외부 URL 허용목록(HTTPS) 설정 | IMPLEMENT | 관리자 탭에서 URL 설정, HTTPS 외 스킴(http/javascript/data) 저장 거부(항목 10 핵심 범위) | Playwright SM-10 |
| REQ-FUNC-078 | 404/500/권한없음/외부연결실패 복구 행동 | IMPLEMENT | 각 오류 화면에 홈/이전/재시도 중 최소 1개 행동 제공 | 수동 QA |
| REQ-FUNC-079 | 폼·모달·탭·알림 HTML 의미·ARIA 상태 | IMPLEMENT | 시맨틱 HTML과 ARIA 속성 적용(모범 사례 수준). 자동 axe 파이프라인은 REQ-NF-024 참고(제외) | 수동 접근성 점검(키보드/스크린리더) |
| REQ-FUNC-080 | 약관·개인정보방침·동행 안전수칙·면책 안내+동의 기록 | IMPLEMENT | 정책 페이지 제공, 모집글 작성 시 안전수칙 동의 체크박스+정책 버전·동의 시각 저장 | Playwright SM-05 |

---

## 7. REQ-NF-001~034 매핑

### 7-1. Performance

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-NF-001 | LCP p75 ≤2.5s | IMPLEMENT | 정적 콘텐츠·이미지 최적화로 목표 달성(공식 CI 게이트 없음) | 수동 Lighthouse 점검 |
| REQ-NF-002 | INP p75 ≤200ms | IMPLEMENT | 클라이언트 상호작용 최소화·경량 컴포넌트 구성 | 수동 점검 |
| REQ-NF-003 | CLS p75 ≤0.1 | IMPLEMENT | 이미지 크기 고정, 레이아웃 시프트 방지 | 수동 점검 |
| REQ-NF-004 | 필터 응답 p95≤1s(동시 50명) | IMPLEMENT | 정적 데이터 클라이언트 필터로 사실상 즉시 응답. 동시사용자 부하 테스트는 제외(5장) | 수동 QA(기능 응답성) |
| REQ-NF-005 | 쓰기 API 응답 p95≤3s | IMPLEMENT | Supabase 단순 insert/update 기준으로 목표 충족 예상(부하 테스트 미실시) | 수동 QA |
| REQ-NF-006 | 이미지 반응형·lazy load, LCP 이미지 priority | IMPLEMENT | Next.js `Image` 컴포넌트 사용 | 코드 리뷰 |
| REQ-NF-007 | 배포 전 Lighthouse Performance ≥85 CI 검사 | EXCLUDED | 자동 성능 CI 게이트 미구축. 배포 전 수동 확인으로 대체(부하/성능 자동화 제외) | N/A |

### 7-2. Reliability and Recovery

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-NF-008 | 월간 가용성 ≥99.5% | EXCLUDED | 별도 가동률 모니터링·SLA 리포팅 체계 미구축. Vercel 기본 인프라에 의존 | N/A |
| REQ-NF-009 | 내부 API 5xx ≤0.5% | EXCLUDED | 별도 오류율 모니터링/알림 파이프라인 미구축(장애 알림 제외) | N/A |
| REQ-NF-010 | DB 백업 RPO≤24h/RTO≤8h | EXCLUDED | 자동 백업 체계 미구축(5장), Supabase 기본 제공 수준에 의존 | N/A |
| REQ-NF-011 | 외부 링크 주1회 자동 검사+Admin 알림 | EXCLUDED | 자동 검사·장애 알림 인프라 미구축. 배포 전 수동 링크 점검으로 대체 | N/A |

### 7-3. Security and Privacy

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-NF-012 | TLS 1.2 이상 | IMPLEMENT | Vercel 기본 HTTPS/TLS 적용 | 브라우저 인증서 확인 |
| REQ-NF-013 | 인증·역할·RLS 서버 검증 | IMPLEMENT | Supabase Auth + RLS 정책으로 서버 측 강제 | 권한별 부정 접근 테스트(수동) |
| REQ-NF-014 | CSRF 방어·SameSite 쿠키 | IMPLEMENT | Next.js Server Actions 기본 보호 + Supabase 세션 쿠키(SameSite) 사용 | 코드 리뷰 |
| REQ-NF-015 | 입력 검증·이스케이프, 저장 XSS 차단 | IMPLEMENT | 서버 측 입력 검증 + React 자동 이스케이프 | 수동 XSS 케이스 테스트 |
| REQ-NF-016 | 비밀키 환경변수 관리, 클라이언트 번들 제외 | IMPLEMENT | Vercel 환경변수 사용, `NEXT_PUBLIC_` 접두사 최소화 | 빌드 산출물 확인 |
| REQ-NF-017 | 항공·호텔 원시 입력값 미보존 | IMPLEMENT | 서버 API·로그·분석에 값 전달하지 않음(REQ-FUNC-017/025와 동일) | 코드 리뷰+네트워크 탭 확인 |
| REQ-NF-018 | 개인정보 내보내기·탈퇴·삭제 요청 | EXCLUDED | 데이터 내보내기(export) 및 법적 보존 예외를 반영한 단계적 삭제 파이프라인 미구현(REQ-FUNC-045와 동일 사유) | N/A |

### 7-4. Safety and Moderation

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-NF-019 | 신고 접수 응답 p95≤3s | IMPLEMENT | 단순 insert 기반으로 목표 충족(REQ-FUNC-039) | 수동 QA |
| REQ-NF-020 | 신고 1차 검토 24h 이내 90% | EXCLUDED | 운영 인력 SLA를 코드로 보장할 수 없는 운영 지표. 관리자 탭 상태 변경 기능(REQ-FUNC-041/042)만 제공하고 SLA 추적 대시보드는 미구현 | N/A |
| REQ-NF-021 | 글·요청·신고 속도 제한(429) | EXCLUDED | 별도 rate limiting 인프라 미구축(간단한 신고·차단 범위 초과) | N/A |
| REQ-NF-022 | Moderator 조치 추적 가능성(감사 로그 0건 누락) | EXCLUDED | 범용 감사 로그 미구현(REQ-FUNC-076과 동일 사유) | N/A |

### 7-5. Accessibility

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-NF-023 | WCAG 2.2 Level AA 목표 | IMPLEMENT | 시맨틱 마크업·명도 대비·포커스 관리 등 모범 사례 적용(목표 수준, 공식 인증 아님) | 수동 접근성 점검 |
| REQ-NF-024 | 자동 접근성 검사(axe) serious/critical 0건 | EXCLUDED | 별도 axe 자동화 파이프라인 미구축. Playwright 핵심 Smoke Test에는 포함하지 않음 | N/A |
| REQ-NF-025 | 키보드·스크린리더 수동 검사, 핵심 UC 100% | IMPLEMENT | 배포 전 핵심 흐름(여행지 탐색, 항공/호텔, 동행, 안전정보)에 대한 수동 키보드·스크린리더 점검 수행 | 수동 접근성 점검 |

### 7-6. Content, Freshness, SEO, Copyright

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-NF-026 | 여행지 콘텐츠 완전성 100% | IMPLEMENT | 정적 데이터 작성 시 필수 필드 체크리스트 대조(REQ-FUNC-004/008) | 수동 콘텐츠 체크리스트 |
| REQ-NF-027 | 해외 국가 안전정보 커버리지 100% | IMPLEMENT | 15개국 전체 안전정보 정적 데이터 작성(REQ-FUNC-046) | 수동 데이터 커버리지 확인 |
| REQ-NF-028 | 안전정보 최신 확인 7일 이내 95%, 초과 시 경고 100% | IMPLEMENT | 경고 로직은 렌더링 시 계산(REQ-FUNC-050)으로 100% 보장. 95% 최신성 자체는 운영(콘텐츠 갱신) 지표로 코드가 보장하지 않음 | Playwright SM-08(경고 로직) |
| REQ-NF-029 | 미디어 라이선스 메타데이터 공개 미디어 100% | EXCLUDED | 이미지 정책이 URL+alt로 단순화되어 라이선스 메타데이터 자체를 관리하지 않음(REQ-FUNC-007/061과 동일) | N/A |
| REQ-NF-030 | 공개 페이지 SEO 메타데이터 누락 0건 | IMPLEMENT | Next.js Metadata API로 각 라우트에 메타데이터 정의(REQ-FUNC-070) | 코드 리뷰 |

### 7-7. Maintainability, Monitoring, Cost

| ID | 요구사항 요약 | 분류 | 처리 방법 | 확인 방법 |
|---|---|---|---|---|
| REQ-NF-031 | TypeScript strict·lint·unit test, main 병합 전 통과 | IMPLEMENT | `tsconfig` strict 모드, ESLint(`next lint`) 적용. 별도 단위 테스트 스위트는 구성하지 않고 Playwright 핵심 Smoke Test(항목 11)로 핵심 흐름만 검증 | CI(타입체크+lint) + Playwright |
| REQ-NF-032 | 구조화 로그(request_id, actor, action, result) | EXCLUDED | 별도 구조화 로깅 파이프라인 미구축. Vercel 기본 로그에 의존 | N/A |
| REQ-NF-033 | 5xx>1% 또는 외부 링크 실패 시 5분 이내 알림 | EXCLUDED | 장애 알림 자동화 미구축(5장) | N/A |
| REQ-NF-034 | MVP 월 인프라 비용 ≤100,000원 | IMPLEMENT | Vercel·Supabase 무료/저가 티어 사용, AWS/EC2 등 별도 인프라 미구성(5장) | 수동 비용 확인(배포 시점) |

---

## 8. 데이터 소스 매핑

| 엔터티(SRS 6.3) | 처리 |
|---|---|
| COUNTRY, REGION, DESTINATION, DESTINATION_CONTENT | `src/data`의 정적 파일. Supabase 테이블 미사용 |
| COUNTRY_SAFETY | `src/data`의 정적 파일 |
| MEDIA_ASSET | 별도 엔터티로 관리하지 않음. 이미지는 각 콘텐츠 항목에 `{ url, alt }` 형태로 인라인 저장 |
| REPRESENTATIVE_PROFILE | `src/data`의 정적 파일(단일 소스, `50+ Trips`/`30+ Countries` 라벨 포함) |
| USER_PROFILE | Supabase `auth.users` + 프로필 테이블(`nickname`, `is_adult`, `adult_verified_at`, `age_band`, `gender`, `travel_styles`, `bio`, `status`) |
| MATE_POST | Supabase 테이블. `status`는 `end_date` 계산에 따라 조회 시 CLOSED로 취급(실제 컬럼 값은 OPEN/CLOSED/HIDDEN/DELETED 유지) |
| MATE_APPLICATION | Supabase 테이블 + RLS |
| USER_BLOCK | Supabase 테이블 + RLS |
| REPORT | Supabase 테이블. 상태 필드(OPEN/RESOLVED/DISMISSED)만 유지, 별도 이력 테이블 없음 |
| AUDIT_LOG | 구현하지 않음(5장) |

Admin API(SRS 6.1의 `API-14` 여행지 관리, `API-15` 안전정보 관리, `API-16` 미디어 관리)는 구현하지 않으며, `API-13`(신고 큐·처리)과 `API-17`(외부 URL 설정)만 관리자 탭 범위로 구현한다.

---

## 9. Playwright 핵심 Smoke Test 시나리오

| ID | 시나리오 |
|---|---|
| SM-01 | 홈 → 여행지 목록(국내/해외 탭) → 필터·검색 → 상세 진입 → 안전정보 링크 이동 |
| SM-02 | 항공 폼: 필수값 누락/날짜 역전 차단 → 유효 입력 → 요약(비전달 고지) → 외부 새 탭 이동(query 없음) |
| SM-03 | 호텔 폼: SM-02와 동일 플로우(체크인/체크아웃 기준) |
| SM-04 | 이메일 가입 → 인증 → 로그인 → 성인 확인 → 동행 쓰기 권한 획득 |
| SM-05 | 동행글 작성(연락처 패턴 차단 케이스 포함, 안전수칙 동의) → 목록 노출 → 종료일 경과 시 모집중 목록 제외 |
| SM-06 | 참가 요청 제출(PENDING) → 작성자 승인/거절 → 상태 반영 확인 |
| SM-07 | 신고 접수(접수번호 표시) 및 사용자 차단 → 차단 후 상호 콘텐츠 비노출 확인 |
| SM-08 | 국가 안전정보 페이지: 필수 카테고리 표시, 7일 초과 시 stale 경고, 중대 경보 상단 노출 |
| SM-09 | 대표 소개 페이지: 대표명·50+/30+ 수치·추천 여행지 링크 정상 동작 |
| SM-10 | 마이페이지(내 글/요청/차단) 및 관리자 탭(비관리자 접근 차단, 신고 상태 변경, 외부 URL HTTPS 검증) |

---

## 10. 배포

- Vercel 프로젝트에 연결하여 preview/production 배포를 수행한다(항목 12).
- 외부 URL(`FLIGHT_OUTBOUND_URL`, `HOTEL_OUTBOUND_URL`, `MOFA_SAFETY_URL`)과 Supabase 키는 Vercel 환경변수로 관리한다.
- 배포 전 체크리스트: 정적 콘텐츠 수량·필수 필드 확인(6·7장 수동 확인 항목), Playwright 핵심 Smoke Test(9장) 통과, 주요 외부 링크 수동 점검.
