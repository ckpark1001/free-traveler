# Traveler Design Canon — D-001

- **Design Version:** D-001
- **Status:** LOCKED
- **제품:** Free Traveler 여행 탐색·외부 연결·동행·안전정보 플랫폼
- **근거 문서:** `docs/00_PRD_Travel_v1.md`, `docs/05_SRS_Travel_v1.md`, `design-reference/vendor/airbnb/DESIGN.md`(참고용 벤더 분석, 그대로 이식 금지)
- **Stitch 시각 검수 상태:** `docs/STITCH_VALIDATION_REPORT.md` 기준 자동 검증 불가(BLOCKED) → 본 정본은 PRD/SRS의 확정 요구사항과 Airbnb 벤더 분석의 구조적 패턴(레이아웃 문법)만 참고하여 작성되었으며, Stitch 프로젝트의 픽셀 단위 재현을 주장하지 않는다. 실제 화면 구현 후 사람 검수가 필요하다.

---

## 0. 문서 목적과 사용 규칙

이 문서는 Free Traveler의 유일한 디자인 정본이다. `design-reference/vendor/airbnb/DESIGN.md`는 레이아웃 문법(포토 퍼스트 카드, 필 형태 검색바, 섹션 리듬)을 참고하기 위한 벤더 분석일 뿐이며, Airbnb의 색상·폰트·상표·컴포넌트명을 그대로 가져오지 않는다. 화면을 구현하는 모든 사람은 이 문서의 토큰과 규칙만 사용한다. 토큰에 없는 값이 필요하면 이 문서를 먼저 개정한다.

---

## 1. Visual Theme

Free Traveler는 "예약 마켓플레이스"가 아니라 **여행 준비 허브**다. 따라서 시각 언어는 Airbnb류의 상거래 톤(구매 유도, 별점, 즉시 예약)을 배제하고 다음 세 가지 인상을 준다.

1. **신뢰(Trust):** 안전정보·출처·최종 확인일이 눈에 띄는 차분한 딥 틸(deep teal) 브랜드 컬러.
2. **발견(Discover):** 사진 중심의 여행지 카드와 여유로운 여백으로 탐색을 즐겁게 만든다.
3. **절제된 연결(Connect, not Transact):** 항공·호텔·동행은 모두 "정리하고 다음으로 이동"하는 흐름이며, 가격·재고·결제처럼 보이는 요소를 만들지 않는다.

바탕은 따뜻한 오프화이트(off-white) 캔버스, 텍스트는 짙은 차콜, 브랜드 액센트는 하나의 딥 틸 컬러로 제한한다. 안전·경고 관련 색상만 별도 semantic 토큰으로 분리한다.

---

## 2. Color Token

토큰 이외의 색상은 어떤 화면에도 추가하지 않는다(§16 Do Not).

### 2-1. Brand

| Token | Hex | 용도 |
|---|---|---|
| `color.brand.primary` | `#146F6B` | 주요 CTA 배경, 활성 탭, 링크, 포커스 링 |
| `color.brand.primary-hover` | `#0F5652` | primary 버튼 hover/press |
| `color.brand.primary-tint` | `#DCEEEC` | primary 배경 tint(칩, 활성 배지 배경) |
| `color.brand.primary-disabled` | `#AFD4D1` | 비활성 primary 버튼 |

### 2-2. Neutral / Surface

| Token | Hex | 용도 |
|---|---|---|
| `color.canvas` | `#FDFCFA` | 기본 페이지 배경 |
| `color.surface` | `#FFFFFF` | 카드·모달·드로어 표면 |
| `color.surface-soft` | `#F5F3EF` | 섹션 구분 배경, 비활성 필드 |
| `color.surface-strong` | `#ECE9E3` | 원형 아이콘 버튼, 강조 배경 |
| `color.hairline` | `#E4E1DA` | 1px 구분선 |
| `color.hairline-soft` | `#EFEDE7` | 옅은 구분선(리스트 내부) |
| `color.border-strong` | `#C7C2B8` | 입력 필드 outline, 포커스 이전 강조 |

### 2-3. Text

| Token | Hex | 용도 |
|---|---|---|
| `color.text.ink` | `#1E1B16` | 제목, 본문 기본 |
| `color.text.body` | `#4A453D` | 본문 서술 |
| `color.text.muted` | `#6F6A60` | 보조 설명, 캡션 |
| `color.text.muted-soft` | `#9A948A` | 비활성 텍스트 |
| `color.text.on-primary` | `#FFFFFF` | primary 배경 위 텍스트 |
| `color.text.link` | `#146F6B` | 인라인 링크(브랜드 컬러 재사용) |

### 2-4. Semantic (안전·상태 전용, 브랜드 컬러와 절대 혼용 금지)

| Token | Hex | 용도 |
|---|---|---|
| `color.semantic.danger` | `#B3261E` | 여행금지·중대 경보, 오류 텍스트 |
| `color.semantic.danger-bg` | `#FBEAE9` | 위험 배너 배경 |
| `color.semantic.warning` | `#8A5A00` | stale(7일 초과) 경고, 주의 배지 텍스트 |
| `color.semantic.warning-bg` | `#FCF1D9` | 경고 배너 배경 |
| `color.semantic.success` | `#276749` | 승인·완료 상태 |
| `color.semantic.success-bg` | `#E7F3EC` | 성공 배너 배경 |
| `color.semantic.info` | `#1F5FA8` | 안내 배너, 정책 고지 |
| `color.semantic.info-bg` | `#EAF1FA` | 안내 배너 배경 |
| `color.scrim` | `#141310` (50% opacity 적용) | 모달·드로어 백드롭 |

> 안전정보 경보 단계는 색상만으로 구분하지 않는다(PRD 접근성 원칙). 항상 텍스트 라벨(`여행금지`, `주의`, `보통`)을 semantic 색상과 함께 표기한다.

---

## 3. Typography

Airbnb Cereal VF 등 **라이선스가 확인되지 않은 Proprietary 폰트 파일은 프로젝트에 추가하지 않는다.**

- **본문/한글 우선 서체:** `Pretendard Variable` (SIL OFL 오픈소스 라이선스, self-host 또는 npm 패키지로 로드) → 실패 시 `-apple-system, "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif`.
- **숫자/영문 보조 서체:** `Inter` (오픈소스, OFL) → 실패 시 시스템 스택.
- 두 서체 모두 오픈소스이며 별도 상업 라이선스 파일을 배포하지 않는다. 폰트를 로드할 수 없는 환경에서는 시스템 폰트 스택만으로도 동일한 크기·굵기 규칙이 유지되어야 한다.

### 3-1. Scale

| Token | Size | Weight | Line Height | 용도 |
|---|---|---|---|---|
| `type.display-lg` | 32px | 700 | 1.25 | 홈 Hero 타이틀 |
| `type.display-md` | 26px | 700 | 1.3 | 여행지 상세 Hero 타이틀, 섹션 대제목 |
| `type.display-sm` | 22px | 600 | 1.3 | 서브 섹션 제목 |
| `type.title-md` | 18px | 600 | 1.35 | 카드 제목, 탭 라벨 |
| `type.title-sm` | 16px | 600 | 1.4 | 리스트 항목 제목 |
| `type.body-md` | 16px | 400 | 1.6 | 본문 |
| `type.body-sm` | 14px | 400 | 1.5 | 카드 메타, 캡션 |
| `type.caption` | 13px | 500 | 1.4 | 라벨, 폼 필드 라벨 |
| `type.micro` | 12px | 600 | 1.3 | 배지, 상태 텍스트 |
| `type.button` | 16px | 600 | 1.25 | 버튼 라벨 |

원칙: 여행지 상세의 rating-display 같은 "숫자 하나를 64px로 키우는" 연출은 사용하지 않는다(별점형 신뢰 신호 금지, §16). 대신 안전정보 최종 확인일과 출처는 `type.body-sm` + semantic 색상으로 항상 함께 노출해 신뢰를 표현한다.

---

## 4. Spacing

4px 베이스 스케일.

| Token | 값 |
|---|---|
| `space.2xs` | 4px |
| `space.xs` | 8px |
| `space.sm` | 12px |
| `space.md` | 16px |
| `space.lg` | 24px |
| `space.xl` | 32px |
| `space.2xl` | 48px |
| `space.section` | 72px |
| `space.section-mobile` | 40px |

카드 내부 패딩은 `space.lg`(24px), 카드 사이 간격은 `space.md`(16px), 폼 필드 사이 간격은 `space.md`(16px)를 기본으로 한다.

---

## 5. Radius

| Token | 값 | 용도 |
|---|---|---|
| `radius.none` | 0px | 전체 폭 배너, 테이블 |
| `radius.sm` | 10px | 버튼, 입력 필드 |
| `radius.md` | 16px | 카드(여행지·동행·안전) |
| `radius.lg` | 24px | 모달, 드로어 상단 코너 |
| `radius.pill` | 9999px | 필터 칩, 탭 인디케이터, 배지 |

---

## 6. Shadow

| Token | 정의 | 용도 |
|---|---|---|
| `shadow.none` | 없음 | 본문, Hero, Footer(95% 표면) |
| `shadow.sm` | `0 1px 2px rgba(20,111,107,0.08)` | 카드 hover, sticky 요약 바 |
| `shadow.md` | `0 8px 24px rgba(30,27,22,0.12)` | 드롭다운, 팝오버, 필터 드로어 |
| `shadow.lg` | `0 16px 40px rgba(30,27,22,0.18)` | 모달, 전체화면 시트 |

---

## 7. Header · Footer

### Header
- 높이: Desktop 72px / Mobile 56px, `color.surface` 배경 + 하단 `color.hairline` 1px.
- 좌측 워드마크(텍스트 로고, 상표 이미지 아님) + 중앙 또는 우측 6개 1차 내비게이션: `여행지 · 비행기 찾기 · 호텔 찾기 · 동행 찾기 · 국가별 주의사항 · 대표소개`.
- 우측: 로그인/마이페이지 진입점 1개.
- 활성 메뉴는 `color.brand.primary` 텍스트 + 하단 2px 밑줄. 비활성은 `color.text.muted`.
- Mobile(<744px): 워드마크 + 햄버거. 메뉴는 전체화면 Drawer(§10)로 펼친다. 검색 아이콘은 별도 상시 노출.

### Footer
- `color.surface-soft` 배경, 상단 `color.hairline` 구분선.
- 3열(Desktop) → 1열(Mobile) 링크 그룹: `서비스`(여행지/비행기/호텔/동행), `안전과 신뢰`(안전정보/대표소개/콘텐츠 원칙), `정책`(이용약관/개인정보처리방침/동행 안전수칙/문의).
- 최하단 legal band: 저작권 문구 + "본 서비스는 항공·호텔 예약을 대행하지 않으며 외부 사이트의 가용성·가격을 보장하지 않습니다." 고지를 상시 노출한다(PRD 원칙 2, 3).

---

## 8. Search · Filter

- **키워드 검색:** 여행지·국가·테마 통합 검색 입력 1개, `radius.pill`, 높이 48px(Desktop) / 44px(Mobile).
- **필터 바:** 국가·계절·테마·권장 기간을 칩(`radius.pill`, `type.body-sm`) 형태로 제공하며 AND 조건으로 결합된다. 활성 칩은 `color.brand.primary-tint` 배경 + `color.brand.primary` 텍스트.
- **결과 없음:** §14 Empty State 규칙을 따른다(조건 완화 안내 + 전체 초기화 버튼, AC-D04).
- **동행 필터:** 국가·지역·기간 겹침·연령대·성별·여행 스타일 칩을 동일한 시각 언어로 재사용한다(§11).
- Desktop에서는 필터 바가 상단 고정(sticky) 가능, Mobile에서는 "필터" 버튼 → Drawer(§10)로 전환한다.

---

## 9. Destination Card

Airbnb `property-card`의 포토 퍼스트 레이아웃 문법만 참고하고, 별점·좋아요·가격 배지는 넣지 않는다.

- 카드 표면 `color.surface`, `radius.md`, `shadow.sm`(hover 시).
- 이미지: 4:3 비율, 상단 코너만 `radius.md` 클리핑. 좌상단에 `국내`/`해외` 배지(`radius.pill`, `type.micro`)만 표시.
- 이미지 아래: 제목(`type.title-md`), 국가·도시(`type.body-sm` muted), 테마 태그 최대 3개(칩), "안전정보 연결됨" 아이콘 배지(해외 여행지만, 하트/별점 아님).
- 카드에는 어떤 형태의 별점·리뷰 점수·가격도 표시하지 않는다.
- 그리드: Desktop 4열 / Tablet 2열 / Mobile 1열, 간격 `space.md`.

---

## 10. Form · Tabs

### Form (항공/호텔 입력)
- 필드: 국가, 지역·도시, 시작일, 종료일(호텔은 체크인/체크아웃) — 4개 필수 필드.
- 입력 컨트롤: `radius.sm`, 높이 52px, `color.hairline` outline, 포커스 시 2px `color.brand.primary` outline(글로우 없음).
- 오류 상태: outline `color.semantic.danger`, 필드 하단 오류 텍스트(`type.caption`, danger 색상), 프로그램적으로 필드와 연결(WCAG).
- 유효성 통과 후 **요약 단계**로 전환: 입력값 요약 카드 + "입력값은 외부 사이트로 전달되지 않습니다" 고지(`color.semantic.info-bg` 배너, 상시 노출, REQ-FUNC-015/023) + 외부 이동 CTA(`radius.sm`, `color.brand.primary`, 라벨 예: "항공편 보러 가기").
- 외부 이동 CTA는 새 탭 + `noopener,noreferrer`. 구매·결제·가격 표시 요소는 포함하지 않는다(§16).

### Tabs
- 탭 인디케이터: 밑줄형, `color.brand.primary` 2px. 비활성 라벨 `color.text.muted`.
- SCR-003(여행 준비 허브)의 3탭 `항공 찾기 · 숙소 찾기 · 동행 구하기`는 항상 함께 렌더링되며, 하나만 노출하는 변형을 만들지 않는다(§15 화면 계약).
- Mobile에서는 탭을 가로 스크롤 가능한 세그먼트로 축소하되 3개 탭 모두 유지한다.

---

## 11. Mate Post Card

- 카드 표면 `color.surface`, `radius.md`, 패딩 `space.lg`.
- 상단: 상태 배지(`모집중`=`success`, `마감`=`muted-soft` 배경) + 국가·지역 + 기간(YYYY.MM.DD–MM.DD).
- 제목(`type.title-sm`), 여행 스타일 태그 최대 3개, 모집 인원(`n/capacity`).
- 하단: 작성자 닉네임 + 연령대(선택적 성별) — **전화번호·이메일·메신저 ID 등 공개 연락처는 카드 어디에도 노출하지 않는다**(REQ-FUNC-033).
- 카드 클릭 시 상세로 이동. 참가 요청은 카드가 아닌 상세 화면의 전용 CTA(모달 §10)에서만 가능하다.

---

## 12. Drawer · Modal

- **Drawer(측면/하단 시트):** 모바일 필터, 모바일 내비게이션, 참가 요청 메시지 입력에 사용. `radius.lg`(상단 코너만), `shadow.lg`, `color.scrim` 백드롭.
- **Modal(중앙 다이얼로그):** 신고 제출, 차단 확인, 성인 확인 안내, 안전수칙 동의에 사용. 최대 폭 480px, `radius.lg`, `shadow.lg`.
- 모든 Drawer/Modal은 `Esc` 및 백드롭 클릭으로 닫히고, 키보드 포커스 트랩과 닫기 버튼(최소 44×44px 터치 영역)을 갖는다.
- 결제/예약 관련 모달(가격 확인, 결제 수단 입력 등)은 어떤 화면에도 만들지 않는다(§16).

---

## 13. Alert · Toast

| 유형 | 색상 토큰 | 사용처 |
|---|---|---|
| Info Banner | `color.semantic.info` / `info-bg` | 입력값 비전달 고지, 외부 이동 안내 |
| Warning Banner | `color.semantic.warning` / `warning-bg` | 안전정보 stale(7일 초과) 경고 |
| Danger Banner | `color.semantic.danger` / `danger-bg` | 여행금지·중대 경보, 폼 검증 실패 |
| Success Toast | `color.semantic.success` | 참가 요청 접수, 신고 접수 완료 |
| Error Toast | `color.semantic.danger` | 외부 링크 오류, 저장 실패 |

- Toast는 화면 상단(Mobile) 또는 우상단(Desktop)에 3~5초 노출, `radius.sm`, `shadow.md`.
- 배너는 색상 단독이 아니라 아이콘 + 텍스트 라벨을 함께 표시한다(접근성 원칙).

---

## 14. Loading · Empty · Error 상태

### Loading
- 카드 그리드: 실제 카드와 동일한 치수의 skeleton(회색 `color.surface-strong` 블록, 은은한 shimmer)만 사용. 회전 스피너는 버튼 내부 등 좁은 영역에서만 허용.

### Empty (완성형 원칙은 §15 참고)
- 결과 없음(필터): "조건에 맞는 여행지가 없어요. 필터를 완화하면 더 많은 결과를 볼 수 있어요." + `전체 초기화` CTA.
- 동행글 없음: "아직 등록된 동행 모집글이 없어요. 첫 모집글을 남겨보세요." + `모집글 작성` CTA.
- 안전정보 확인 지연: `color.semantic.warning-bg` 배너 "최신 정보 재확인이 필요해요" + 외교부 공식 링크 CTA.

### Error
- 404: "찾으시는 페이지가 없어요." + `홈으로` / `이전으로` CTA.
- 500: "일시적인 오류가 발생했어요." + `다시 시도` CTA.
- 외부 연결 실패: "지금은 외부 사이트에 연결할 수 없어요." + `다시 시도` CTA(CP-01). 동일 탭 손실 없이 현재 입력을 保존한다.
- 권한 없음: "이 페이지는 로그인한 회원만 볼 수 있어요." + `로그인` CTA.

모든 에러/빈 화면은 최소 1개의 실행 가능한 복구 액션을 포함해야 한다(REQ-FUNC-078).

---

## 15. Desktop · Mobile 규칙

### 15-1. Breakpoint
| 이름 | 폭 |
|---|---|
| Mobile | 320–743px |
| Tablet | 744–1127px |
| Desktop | 1128–1439px |
| Wide | ≥1440px |

### 15-2. Page Section 최대 폭과 상하 여백
- **콘텐츠 최대 폭:** 1200px(Desktop 중앙 정렬), 여행지 상세 등 리딩 중심 페이지는 960px로 좁혀 가독성을 우선한다.
- **Section 상하 여백:** Desktop `space.section`(72px), Mobile `space.section-mobile`(40px). 두 Section 사이의 빈 공간이 이 값을 초과하지 않는다(§ Hero 규칙과 함께 "긴 빈 공간" 방지).
- **좌우 거터:** Desktop 32px, Mobile 16px 이상을 항상 유지한다(가로 스크롤 금지).

### 15-3. Hero 높이와 다음 Section 노출 규칙
- **Hero 높이:** Desktop viewport의 60–70%, Mobile은 최대 480px(전체 화면 강제 금지). 어떤 뷰포트에서도 Hero 하단 아래로 다음 Section의 제목 또는 카드 일부가 최소 24px 이상 보여야 한다("Hero만 보이고 스크롤해야 다음 내용이 보이는" 레이아웃 금지).
- Hero에는 항상 제목 + 1문장 설명 + 최소 1개의 CTA 또는 검색 입력이 포함된다. Hero만 있고 그 아래 콘텐츠가 없는 화면은 허용하지 않는다.

### 15-4. Section 계층과 시각적 리듬
모든 Section은 다음 4요소 중 최소 3개를 갖는다: **제목 → 설명(선택) → 본문(카드/리스트/폼) → CTA(선택이지만 액션형 Section은 필수)**.
- 제목: `type.display-sm` 또는 `type.title-md`.
- 설명: `type.body-md` muted, 1~2문장.
- 리듬: Section마다 배경을 `color.canvas`↔`color.surface-soft`로 교차시켜 스크롤 중 구간을 구분한다(카드 밀도가 높은 Section은 촘촘하게, 편집형 Section은 여유 있게 — Airbnb 벤더 분석의 "hero는 열고 목록은 촘촘히" 리듬을 계승).

### 15-5. 화면별 Section 순서와 최소 콘텐츠 수(Screen Inventory)

Stitch Screen ID는 승인된 5개 화면(SCR-001~SCR-005)에 대응한다. 각 화면은 아래 순서와 최소 수량을 계약(contract)으로 따른다.

#### SCR-001 — 홈 (Route: `/`) · Mobile 변형 있음
1. Header
2. Hero(제목+설명+통합 검색 입력)
3. 여행지 추천 카드 그리드 — 최소 **6장**
4. 테마 큐레이션 — 최소 **3개** 테마 그룹, 그룹당 최소 3장 카드
5. 국가별 안전정보 하이라이트 — 최소 **3개** 국가 카드(경보 단계 라벨 포함)
6. 동행 찾기 CTA 배너 — 1개
7. 대표소개 요약 카드 — 1개(`50+ Trips`, `30+ Countries` 수치 포함)
8. Footer

Mobile 변형: 동일 순서를 1열로 재배치, Section 6·7을 하나의 카드 스택으로 축약 가능하나 순서는 유지한다.

#### SCR-002 — 여행지 상세 (Route: `/destinations/[slug]`)
1. Header
2. Hero(대표 이미지 + 여행지명 + 국가·지역)
3. 한눈에 보는 소개(300자 이상)
4. 핵심 명소·체험 갤러리 — 최소 **5개**
5. 추천 시기(추천/비추천 계절)
6. 추천 일정 탭(1일/3일) — 1일 일정 최소 **4개** 타임라인 항목, 3일 일정 각 일자 최소 **2개** 항목
7. 예상 예산 카드
8. 현지 교통 안내
9. 대표 음식 — 최소 **3개**
10. 문화·에티켓 — 최소 **3개**
11. 안전정보 연결 카드(해외 여행지 필수, REQ-FUNC-006)
12. 관련 여행지 갤러리 — 최대 6개, 최소 **3개**
13. 출처·최종 수정일 표기
14. Footer

#### SCR-003 — 여행 준비 허브: 항공·숙소·동행 구하기 (Route: `/flights`, `/hotels`, `/mates` 통합 탭 화면) · Mobile 변형 있음
1. Header
2. Hero(제목+설명, "예약 대행이 아님" 고지 1줄)
3. 3탭 네비게이션 — `항공 찾기` / `숙소 찾기` / `동행 구하기` (§10, 3개 모두 상시 노출)
4. 탭별 본문
   - 항공/숙소 탭: 입력 폼 → 요약 → 외부 이동 CTA
   - 동행 탭: 필터 바 + 모집글 카드 미리보기 최소 **3장** + `모집글 작성` CTA
5. 안전·비전달 고지 배너
6. Footer

Mobile 변형: 탭은 가로 스크롤 세그먼트, 폼은 1열, 동행 카드 미리보기는 세로 스택.

#### SCR-004 — 동행 모집글 목록·상세 (Route: `/mates`, `/mates/[id]`)
1. Header
2. 목록 영역: 필터 바 + 모집글 카드 리스트 — 최소 **3장**
3. 상세 영역: 선택된 글의 제목·조건·설명·작성자 미니 프로필·참가 요청 CTA·신고/차단 진입점
4. Footer

Desktop: 목록(약 40% 폭)과 상세(약 60% 폭)를 좌우 분할(master-detail)로 동시에 노출한다. Mobile: 목록 전체 폭 → 카드 탭 시 상세 화면으로 전환(또는 하단 시트)하되, 두 영역의 콘텐츠 계약은 동일하게 유지한다.

#### SCR-005 — 인증·계정 허브 (Route: `/auth/*`, `/my/*`, `/admin/*` 진입점 통합) · 단순 로그인 화면 아님
1. Header(간소화, 로고만)
2. 로그인/회원가입 탭(이메일 인증 + 만 19세 이상 확인 안내)
3. **Member 영역** — 로그인 상태에서 노출: 마이페이지 요약 카드 최소 **3장**(내 모집글, 참가 요청 관리, 차단 관리)
4. **Admin 영역 진입점** — Editor/Moderator/Admin 역할에서만 노출되는 카드 최소 **3장**(콘텐츠 관리, 신고 큐, 외부 URL 설정). 권한이 없는 사용자에게는 이 Section 자체를 숨기되, 화면 설계상 반드시 이 영역의 레이아웃 계약을 포함해야 한다(§2.2 Role Permission Matrix).
5. Footer

> SCR-005는 "로그인 폼 하나"로 끝나는 화면이 아니라, 로그인 이후 Member/Admin 두 영역이 어떻게 확장되는지까지 표현하는 계정 허브 화면이다.

---

## 16. 완성형 Empty State와 Placeholder 문구 금지 규칙

- 어떤 화면에도 `Lorem ipsum`, `준비 중`, `정보 확인 필요`, `TBD`, `추후 업데이트 예정` 같은 미완성 placeholder 문구를 사용하지 않는다.
- 빈 Card(제목·설명·이미지 중 아무것도 없는 카드)를 그대로 노출하지 않는다. 콘텐츠가 없으면 §14의 완성형 Empty State 컴포넌트로 대체한다.
- 모든 Empty/Error 문구는 **완성된 한국어 문장 + 원인 또는 다음 행동 안내 + 최소 1개 CTA**의 3요소를 갖춘다.
- 안전정보처럼 최신성이 중요한 콘텐츠는 "정보 없음" 대신 "최신 정보 재확인 필요"처럼 상태를 설명하는 완성 문구를 쓴다(REQ-FUNC-050).

---

## 17. Do / Do Not

### Do
- 이 문서의 Color/Typography/Spacing/Radius/Shadow 토큰만 사용한다.
- 외부 이동(항공·호텔) CTA에는 항상 새 탭 + `noopener,noreferrer` + 비전달 고지를 함께 노출한다.
- 안전정보에는 출처명·출처 URL·최종 확인일을 항상 함께 표기한다.
- SCR-003의 항공·숙소·동행 구하기 3탭을 항상 함께 노출한다.
- SCR-004는 목록과 상세를 하나의 화면 계약 안에서 함께 설계한다.
- SCR-005는 Member 영역과 Admin 진입점을 포함해 설계한다(로그인 폼 단독 금지).
- 모든 Section에 제목·설명·본문/CTA 중 최소 3요소를 포함한다.
- Empty/Error 상태는 완성된 문장과 실행 가능한 CTA로 구성한다.

### Do Not
- Airbnb 로고·워드마크·Rausch 계열(`#ff385c` 등) 컬러·Airbnb Cereal 폰트·"Guest favorite" 배지·하트 저장 아이콘 등 **Airbnb 고유 상표·UI 요소를 이식하지 않는다.**
- "예약하기", "결제하기", 가격 비교, 재고 확인, 장바구니 등 **구매·예약·결제 성격의 UI/CTA를 만들지 않는다.** 항공·호텔은 외부 일반 페이지로의 링크 이동만 허용한다.
- **라이선스가 확인되지 않은 Proprietary 폰트 파일**(Airbnb Cereal 등)을 프로젝트 자산으로 추가하지 않는다.
- 본 문서(§2)에 정의되지 않은 임의의 색상 hex 값을 새로 추가하지 않는다.
- 별점, 리뷰 점수, 좋아요 수, 실시간 항공권/호텔 가격 배지를 표시하지 않는다(PRD Won't/Out of Scope).
- 광고 배너·스폰서 콘텐츠를 삽입하지 않는다.
- Lorem ipsum·"준비 중"·"정보 확인 필요" 등 미완성 placeholder 문구와 빈 카드를 노출하지 않는다.
- Hero만 있고 스크롤 없이는 다음 콘텐츠가 전혀 보이지 않는 레이아웃을 만들지 않는다.
