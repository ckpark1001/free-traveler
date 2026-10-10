# UI Contract — Free Traveler (Next.js App Router)

- **근거 문서:** `app/docs/03_UI_COVERAGE_ANALYSIS.md`, `app/docs/04_UIUX_PLAN.md`, `app/docs/PROJECT_SCOPE.md`, `docs/STITCH_VALIDATION_REPORT.md`, `design-reference/D-001/DESIGN.md`
- **대상 Screen:** SCR-001~SCR-005 (5개 고정)
- **프레임워크:** Next.js App Router (`app/src/app/*`)
- **Stitch 검수 상태 참고:** `docs/STITCH_VALIDATION_REPORT.md`는 Google Stitch 프로젝트의 자동 시각 검증이 인증 문제로 BLOCKED(→ STITCH_VALIDATION_NEEDS_HUMAN)였음을 기록한다. 본 계약은 Stitch 화면의 픽셀 재현이 아니라 `app/docs/03_UI_COVERAGE_ANALYSIS.md`·`app/docs/04_UIUX_PLAN.md`가 이미 확정한 Section·상태·이동 규칙을 Next.js 구현 계약으로 옮긴 것이다.
- **경로 표기 관례:** 아래 모든 `src/app/...` 경로는 Next.js 프로젝트 루트인 `app/` 기준 상대 경로다(저장소 전체 기준으로는 `app/src/app/...`).

## 0. Screen 분류 (핵심 4 · 보조 1)

`app/docs/PROJECT_SCOPE.md` §3의 "핵심 화면 4개·보조 화면 1개" 구분을 새 라우트 체계(SCR-001~005)에 맞춰 재확인한다.

| 구분 | Screen ID | 사유 |
|---|---|---|
| 핵심(core) | SCR-001 | 여행지 탐색·안전정보 확인이라는 1차 가치 제안의 진입점 |
| 핵심(core) | SCR-002 | PRD "Trust the Curator" 가치 제안(대표 신뢰도) 담당, MoSCoW Must |
| 핵심(core) | SCR-003 | 항공·호텔 외부 연결 + 동행 작성이라는 핵심 전환 행동 담당 |
| 핵심(core) | SCR-004 | 동행 모집글 탐색·참가 요청이라는 핵심 전환 행동 담당 |
| 보조(auxiliary) | SCR-005 | 로그인·프로필·내 활동·관리자 기능은 위 4개 핵심 화면을 보조하는 계정 유틸리티이며 그 자체가 1차 방문 목적이 아님 |

---

## SCR-001 — 홈

| 항목 | 내용 |
|---|---|
| **Route** | `/` |
| **Page Entry** | `src/app/page.tsx` |
| **분류** | 핵심 |

### 영역 순서
1. Header(공통)
2. 여행지 검색 Hero(H1 + 통합 검색창 + `/travel-tools` 보조 CTA)
3. 국내 인기 여행지 Card Grid(6장)
4. 해외 인기 여행지 Card Grid(6장, 국가 안전정보 배지 포함)
5. 여행 동기·테마 Chip 목록(6개, 가로 스크롤)
6. 국가별 주의사항 Card Grid(6장, 경보 단계 텍스트 라벨 + 최종 확인일)
7. 최근 동행 소식 Card Grid(3장) 또는 Empty State
8. free_traveler 요약 CTA Banner(좌우 분할)
9. Footer(공통)

### 주요 Component
- `SearchHero`, `DestinationCardGrid`(국내/해외 공용), `ThemeChipRow`, `SafetyCountryCardGrid`, `MateTeaserGrid`, `AboutSummaryBanner`
- `DestinationDetailDrawer`(같은 화면 내 오버레이, 페이지 이동 없음)
- `SafetyInfoDrawer`(여행지 Drawer 위에 스택으로 열림)

### 상태
| 상태 | 정의 |
|---|---|
| Loading | Section 3·4·6 Card Grid 스켈레톤 |
| Success | 필터·검색 결과 1건 이상 |
| Empty | Section 3·4·6 결과 0건 → 조건 완화 안내 + 전체 초기화 버튼. Section 7은 동행글 0건 시 완성형 3요소 Empty State |
| Error | 안전정보 Drawer 내 외교부 외부 링크 열기 실패 → 인라인 오류 + 재시도 |
| Unauthorized | 없음(전체 공개 화면) |

### 사용자 행동
- 통합 검색어 입력 → 여행지·안전정보 결과 필터링(같은 화면)
- 국내/해외 카드 클릭 → `DestinationDetailDrawer` 오픈(라우트 이동 없음)
- 해외 상세 Drawer 내 "국가별 주의사항 보기" 클릭 → `SafetyInfoDrawer` 스택 오픈
- 테마 Chip 선택/해제 → Section 3·4 카드 즉시 재필터, 필터 상태 URL query 반영
- 안전정보 카드 클릭 → `SafetyInfoDrawer` 단독 오픈
- 동행 카드 클릭 → SCR-004로 이동
- free_traveler 배너 CTA 클릭 → SCR-002로 이동

### 다른 화면으로의 이동
| 트리거 | 대상 |
|---|---|
| 대표소개 요약 카드 CTA | SCR-002 |
| 항공·호텔 보조 CTA(Hero) | SCR-003 |
| 동행 카드/CTA | SCR-004 |
| 안전정보 Drawer 내 외교부 원문 링크 | 외부(새 탭, `noopener,noreferrer`) |

### Desktop · Mobile 규칙
- Desktop(1440px): Hero 높이 560px 내외로 스크롤 없이 Section 3 상단이 보임. Card Grid 3열.
- Tablet(744~1439px): Card Grid 2열, Chip 목록 가로 스크롤 유지.
- Mobile(390px): Hero 검색창 풀폭 pill, Card Grid 1열, `SafetyInfoDrawer`/`DestinationDetailDrawer`는 Bottom Sheet(상단 `radius.lg`)로 전환.

### 금지 기능
- 별점·리뷰 점수·좋아요 수·실시간 가격 배지 표시 금지
- 광고·스폰서 카드 삽입 금지
- Airbnb 로고·Rausch 계열 색상·"Guest favorite" 배지 등 상표 요소 이식 금지
- `starter_template_forbidden`: create-next-app 기본 스타터 마크업(Next.js 로고, "To get started, edit..." 문구, Vercel/Docs 링크 버튼) 잔존 금지 — 현재 `app/src/app/page.tsx`는 이 기본 스타터 상태이므로 반드시 교체 대상
- Lorem ipsum·"준비 중"·"정보 확인 필요" 플레이스홀더 및 빈 카드 노출 금지

---

## SCR-002 — 대표 소개

| 항목 | 내용 |
|---|---|
| **Route** | `/about` |
| **Page Entry** | `src/app/about/page.tsx` |
| **분류** | 핵심 |

### 영역 순서
1. Header(공통)
2. free_traveler Hero(좌우 분할: 대표 이미지 + 한 문장 소개)
3. 여행 지표 Stat Row(`50+ Trips`, `30+ Countries`, 전문 영역 배지)
4. 소개·철학 좌우 분할(소제목 Nav + 본문 2~4문단)
5. 여행 Timeline(세로, 최소 6개 시점)
6. 방문 국가 Chip 목록(권역별 그룹, 30개국 이상)
7. 여행 사진 Gallery(8장 이상)
8. 기억에 남는 여행지 Card Grid(4장) + CTA Banner
9. Footer(공통)

### 주요 Component
- `AboutHero`, `StatRow`, `PhilosophySplit`, `TravelTimeline`, `CountryChipGroup`, `PhotoGallery`, `RecommendedDestinationGrid`, `CrossLinkCtaBanner`

### 상태
| 상태 | 정의 |
|---|---|
| Loading | Gallery 이미지 lazy load 중 블러 플레이스홀더 |
| Success | 기본 상태(정적 데이터, 대부분 이 상태) |
| Empty | 해당 없음(정적 콘텐츠는 항상 존재) |
| Error | SNS/문의 외부 링크 열기 실패 시 인라인 안내 |
| Unauthorized | 없음(전체 공개) |

### 사용자 행동
- 방문 국가 Chip 클릭 → 관련 여행지가 있으면 SCR-001 여행지 Drawer로 이동
- 추천 여행지 카드 클릭 → SCR-001 여행지 Drawer로 이동
- 하단 CTA Banner 클릭 → SCR-003 또는 SCR-004로 이동
- 문의·SNS 링크 클릭 → 외부(새 탭)

### 다른 화면으로의 이동
| 트리거 | 대상 |
|---|---|
| 추천 여행지 카드 | SCR-001 |
| CTA Banner "여행 조건 정리하기" | SCR-003 |
| CTA Banner "동행 찾기" | SCR-004 |
| 문의·SNS 링크 | 외부(새 탭) |

### Desktop · Mobile 규칙
- Desktop: Section 2·4 좌우 분할(약 55/45), Section 8 Card Grid 4열.
- Mobile: 좌우 분할 Section은 이미지 위·텍스트 아래 세로 스택, Gallery 2열, Card Grid 1열.

### 금지 기능
- Airbnb 상표 요소(로고, 서체명, 상품 탭 구조, 배지 명칭) 인용 금지 — 스타일 철학만 참고
- `50+ Trips`/`30+ Countries` 외 임의로 과장·변경된 수치 표기 금지(전역 단일 소스 원칙)
- 이미지 자체를 로고·상표처럼 사용하거나 특정 서비스의 보증인으로 오인될 수 있는 연출 금지
- Lorem ipsum·"준비 중" 플레이스홀더 금지

---

## SCR-003 — 항공·호텔·동행 준비

| 항목 | 내용 |
|---|---|
| **Route** | `/travel-tools` |
| **Page Entry** | `src/app/travel-tools/page.tsx` |
| **분류** | 핵심 |

### 영역 순서
1. Header(공통)
2. 페이지 Intro Hero(축소형, 이용 순서 3단계 요약)
3. 탭 전환(`항공편` / `숙소` / `동행 구하기`) — 3탭 항상 함께 노출, 각 탭 독립 상태 유지
4. 조건 입력 Form(탭별: 항공=국가·지역·출발일·귀국일 / 숙소=국가·지역·체크인·체크아웃)
5. 입력 요약 Action Card(검증 통과 후 노출, 외부 이동 CTA)
6. 비전달 고지 Info Banner + Tip 3단계 안내 카드
7. 동행 탭 콘텐츠(Guest/미인증: 로그인·성인확인 안내 카드 / Member: 작성 Form + 안전 안내 배너)
8. Footer(공통)

### 주요 Component
- `TravelToolsIntro`, `TripToolTabs`, `TripConditionForm`(항공/숙소 공용 패턴), `TripSummaryActionCard`, `NonTransferNoticeBanner`, `MatePostForm`, `ContactPatternValidator`, `SafetyPledgeCheckbox`, `AuthRequiredNotice`

### 상태
| 상태 | 정의 |
|---|---|
| Loading | 외부 이동 CTA 클릭 직후 새 탭 오픈 대기(약 200ms) |
| Success | 요약 표시(항공/숙소) 또는 동행글 게시 완료 Toast |
| Empty | 해당 없음(폼 화면). 동행 탭 미인증은 Unauthorized로 별도 처리 |
| Error | 필수값 누락, 날짜 역전, 연락처 패턴 탐지, 외부 URL 미설정/오류 |
| Unauthorized | 동행 탭에서 비로그인·성인 미확인 → 안내 카드 + `/account` 로그인 CTA로 전환 |

### 사용자 행동
- 탭 전환(항공/숙소/동행), 탭별 값은 서로 독립 보존
- 국가 선택 → 하위 지역 옵션 갱신(국가 변경 시 지역값 초기화)
- 날짜 입력 검증(과거 출발일, 역전 날짜, 체크인=체크아웃 등 차단)
- 유효 입력 제출 → 요약 확인 → "항공편/호텔 보러 가기" 클릭(새 탭, `noopener,noreferrer`)
- 동행 탭: 모집 조건·설명 입력 → 연락처 패턴 검증 → 안전수칙 동의 → 게시

### 다른 화면으로의 이동
| 트리거 | 대상 |
|---|---|
| 항공/호텔 "보러 가기" | 외부 항공/호텔 사이트(새 탭, query 없음) |
| 동행 게시 완료 | SCR-004 |
| 동행 탭 미인증 안내 | SCR-005 |

### Desktop · Mobile 규칙
- Desktop: Section 4·5가 좌우 분할(입력 60% / 요약 40%)로 동시에 보임.
- Mobile: Form 작성 후 "요약 보기"로 Section 5가 아래에 이어 붙는 세로 스택. 탭은 상단 고정 Segmented Control.

### 금지 기능
- **예약하기·결제하기·가격 비교·재고 확인·장바구니 등 구매/예약/결제 성격의 UI·CTA 절대 금지.** 외부 일반 페이지로의 링크 이동만 허용.
- 항공·호텔 입력값(국가·지역·날짜)을 서버 DB·로그·분석 이벤트·외부 URL 쿼리에 저장·전달 금지
- 동행 작성 폼 제출 결과물(모집글)에 전화번호·이메일·메신저 ID 등 공개 연락처 노출 금지
- 실시간 항공권/호텔 가격, 좌석·객실 재고 표시 금지
- Proprietary 폰트 파일, Airbnb 상표 요소 금지

---

## SCR-004 — 동행 찾기

| 항목 | 내용 |
|---|---|
| **Route** | `/mates` |
| **Page Entry** | `src/app/mates/page.tsx` |
| **분류** | 핵심 |

### 영역 순서
1. Header(공통)
2. Intro Hero(축소형) + "동행글 작성하기" CTA
3. 검색 Filter Bar(국가·지역·기간·연령대·성별·스타일·모집 상태) + 결과 카운트
4. 동행글 목록 Card/List(최대 8개 우선 노출)
5. 목록+상세 분할(Desktop 좌우 분할 / Mobile 목록→상세 전환): 조건·설명·작성자 요약, 참가 요청 폼(500자), 신고·차단 버튼
6. 동행 신청 방법 3단계 안내
7. 안전 안내 Banner + CTA Banner
8. Footer(공통)

### 주요 Component
- `MatesIntro`, `MateFilterBar`, `MatePostList`, `MatePostDetailPanel`, `MateApplicationForm`, `ReportDialog`, `BlockConfirmDialog`, `MateHowToSteps`, `SafetyNoticeBanner`

### 상태
| 상태 | 정의 |
|---|---|
| Loading | 목록 스켈레톤(Section 4), 상세 패널 스켈레톤(Section 5) |
| Success | 목록·상세 정상 표시, 참가 요청/신고/차단 완료 Toast |
| Empty | 검색 결과 0건 → 조건 초기화 + 동행글 작성 CTA + 이용 방법 요약(완성형 3요소). 종료일 경과 글은 목록에서 자동 제외 |
| Error | 상세 로드 실패, 참가 요청/신고/차단 제출 실패 → 인라인 오류 + 재시도 |
| Unauthorized | 글쓰기·참가 요청 시도 시 비로그인/성인 미확인 → 안내 배너 + `/account` 로그인 유도 |

### 사용자 행동
- 필터 조합 적용(AND) → 목록 즉시 갱신
- 카드 클릭 → 상세 패널(Desktop 동시 노출 / Mobile 전체화면 전환)
- 참가 요청 메시지(500자) 제출 → PENDING 저장, 중복 요청은 버튼 비활성화
- 신고 사유 코드+설명 제출 → 접수번호 Toast
- 차단 확인 다이얼로그 승인 → 상호 콘텐츠 즉시 비노출

### 다른 화면으로의 이동
| 트리거 | 대상 |
|---|---|
| "동행글 작성하기" CTA | SCR-003(동행 탭) |
| 비로그인·성인 미확인 안내 | SCR-005 |

### Desktop · Mobile 규칙
- Desktop(1440px): Section 5는 좌 목록(약 40%)/우 상세(약 60%) 고정 좌우 분할.
- Mobile(390px): Section 4 목록 1열 Card, 카드 클릭 시 Section 5 상세가 전체 화면 Drawer(하단→상단)로 전환, 상단 "목록으로" 버튼으로 복귀.

### 금지 기능
- 모집글 카드·상세 어디에도 전화번호·이메일·메신저 ID 등 공개 연락처 노출 금지
- 실시간 채팅·영상통화·실시간 위치 공유 UI 금지(Out of Scope)
- 별점·좋아요·리뷰 점수 표시 금지
- 신고 대상·처리 이력을 일반 사용자에게 공개 노출 금지(관리자 전용)
- 미성년자 동행 모집·참가를 허용하는 UI 요소 금지

---

## SCR-005 — 계정

| 항목 | 내용 |
|---|---|
| **Route** | `/account` |
| **Page Entry** | `src/app/account/page.tsx` |
| **분류** | 보조 |

### 영역 순서(역할별로 노출 탭이 다름)
1. Header(공통, 간소화 가능)
2. **Guest:** Intro(계정으로 할 수 있는 것 요약) + 로그인/가입/비밀번호 재설정 Card + "로그인 후 가능한 기능" 3단계 안내 + 보안 안내 Banner
3. **Member:** 프로필 탭(닉네임·연령대·성별·스타일·자기소개 Form + 성인 확인 상태 배지) + 내 활동 탭(내 동행글 관리, 참가 요청함, 차단 목록, 즐겨찾기 목록, "새 동행글 작성" CTA)
4. **Admin:** 관리자 탭(Intro 범위 고지 + 신고 큐(OPEN/RESOLVED/DISMISSED) + 항공·호텔 외부 URL 설정 Form)
5. Footer(공통)

### 주요 Component
- `AuthTabs`(로그인/가입/재설정), `ProfileForm`, `MyActivityPanel`(내 글/요청/차단/즐겨찾기 하위 리스트), `AdminReportQueue`, `AdminOutboundUrlForm`, `RoleGate`

### 상태
| 상태 | 정의 |
|---|---|
| Loading | 탭 전환 시 목록/폼 스켈레톤 |
| Success | 로그인 완료, 프로필 저장 완료, 외부 URL 저장 완료 Toast |
| Empty | 내 글/참가 요청/차단/즐겨찾기 각 목록이 비어있을 때 개별 완성형 Empty State(예: "아직 작성한 동행글이 없습니다" + 작성 CTA) |
| Error | 회원가입/로그인 실패, 프로필 저장 실패, 외부 URL 유효성 오류(HTTPS 외 스킴 거부) |
| Unauthorized | Member 탭에 비로그인 접근 시 로그인 탭으로 리다이렉트, Admin 탭에 비관리자 접근 시 403 안내(홈 복귀 CTA 포함) |

### 사용자 행동
- 이메일 가입/인증/로그인/로그아웃/비밀번호 재설정
- 성인 확인 절차 진행(정확한 생년월일 미저장, `is_adult`/`adult_verified_at`만 저장)
- 프로필 정보 수정·저장
- 내 활동 탭에서 모집글 수정/마감, 참가 요청 승인/거절, 차단 해제, 즐겨찾기 해제
- (Admin) 신고 상태 변경, 외부 URL(HTTPS 허용목록) 설정·저장

### 다른 화면으로의 이동
| 트리거 | 대상 |
|---|---|
| 내 글/요청 상세 이동 | SCR-004 |
| 동행글 재작성 | SCR-003(동행 탭) |
| 로그인 전 진입 트리거였던 화면으로 복귀 | 진입 이전 화면(SCR-003 또는 SCR-004) |

### Desktop · Mobile 규칙
- Desktop: 좌측 세로 탭 Nav + 우측 콘텐츠 좌우 분할.
- Mobile: 상단 가로 스크롤 탭 + 콘텐츠 세로 스택.

### 금지 기능
- 정확한 생년월일 저장·표시 금지(연령대만 저장·노출)
- Admin 탭에서 HTTPS가 아닌 스킴(`http:`, `javascript:`, `data:`) 외부 URL 저장 금지
- 비관리자에게 관리자 탭·기능 노출 금지(역할 검증 없이 UI만 숨기는 방식 금지, 서버 측 검증 필수)
- 콘텐츠 CMS(여행지·안전정보 CRUD, DRAFT/REVIEW/PUBLISHED 상태 전이) 등 Scope 밖 관리자 기능 추가 금지
- Lorem ipsum·"준비 중" 플레이스홀더 및 빈 목록 카드 노출 금지

---

## 공통 규칙 (5개 Screen 전체 적용)

### Header · Footer
- Header: Desktop 72px / Mobile 56px, sticky top. 좌측 워드마크(텍스트, 상표 이미지 아님) → SCR-001. 중앙/우측: 여행지(SCR-001) · 항공·호텔 찾기(SCR-003) · 동행 찾기(SCR-004) · 대표 소개(SCR-002) 텍스트 내비게이션 + 검색·즐겨찾기·계정(SCR-005) 아이콘.
- Footer: 브랜드/바로가기/이용정책/공식 출처 4개 컬럼(Desktop) → 1열(Mobile). 외교부 링크(새 탭) + "예약을 대행하지 않으며 외부 서비스로 안내만 합니다" 고정 고지.

### 공통 오류 상태
| 오류 유형 | 복구 행동 |
|---|---|
| 404 | 홈(SCR-001)으로 이동 CTA |
| 500 | 다시 시도 + 홈으로 이동 |
| 권한 없음(403) | 로그인(Guest) 또는 홈으로 이동(Member) |
| 외부 연결 실패 | 다시 시도 버튼(같은 화면 유지) |

### 공통 금지 기능(5개 Screen 전체)
- Airbnb 로고·워드마크·Rausch 계열(`#ff385c`) 색상·Airbnb Cereal 폰트·"Guest favorite" 배지 등 Airbnb 고유 상표·UI 요소 이식 금지
- 구매·예약·결제 성격의 UI/CTA(예약하기, 결제하기, 가격비교, 재고확인, 장바구니) 금지
- 라이선스가 확인되지 않은 Proprietary 폰트 파일 추가 금지
- `design-reference/D-001/DESIGN.md`에 정의되지 않은 임의 색상 hex 값 추가 금지
- 별점·리뷰 점수·좋아요 수·실시간 항공권/호텔 가격 배지 금지
- 광고·스폰서 콘텐츠 삽입 금지
- Lorem ipsum·"준비 중"·"정보 확인 필요" 플레이스홀더 및 빈 Card 노출 금지
- Hero만 있고 스크롤 없이는 다음 콘텐츠가 전혀 보이지 않는 레이아웃 금지

---

## 기술 Route (Screen으로 집계하지 않음)

| 유형 | 경로 예시 | 설명 | 귀결 위치 |
|---|---|---|---|
| Supabase 인증 콜백 | `/auth/callback` (`src/app/auth/callback/route.ts`) | 이메일 인증·비밀번호 재설정 리다이렉트 처리 | 처리 후 SCR-005로 복귀 |
| API Route | `/api/*` (`src/app/api/**/route.ts`) | 동행/신고/외부 URL 등 서버 쓰기·조회 | SCR-003·SCR-004·SCR-005의 UI_DIRECT/UI_STATE를 통해 간접 반영 |
| Not Found | `src/app/not-found.tsx` | 404 공통 처리 | 5개 Screen 어디서든 발생 가능, 홈(SCR-001) 복귀 CTA 제공 |

---

## 완료 조건 자가 점검

| 조건 | 결과 |
|---|---|
| Route 중복 없음 | `/`, `/about`, `/travel-tools`, `/mates`, `/account` — 5개 모두 고유 |
| Page Entry 중복 없음 | `src/app/page.tsx`, `src/app/about/page.tsx`, `src/app/travel-tools/page.tsx`, `src/app/mates/page.tsx`, `src/app/account/page.tsx` — 5개 모두 고유 |
| Screen 수 5 | SCR-001~SCR-005 정확히 5개 |
| 핵심 4개·보조 1개 구분 존재 | 핵심: SCR-001, SCR-002, SCR-003, SCR-004 / 보조: SCR-005 (§0) |
