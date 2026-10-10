# Design Manifest — Free Traveler

- **Active Design Version:** D-001
- **Status:** LOCKED
- **Active File:** `design-reference/D-001/DESIGN.md`
- **Vendor Reference:** `design-reference/vendor/airbnb/DESIGN.md`
- **Approved Screens:** SCR-001, SCR-002, SCR-003, SCR-004, SCR-005
- **Mobile Variants:** SCR-001, SCR-003

## Screen Inventory

| Screen ID | 화면명 | 대응 Route | Mobile 변형 |
|---|---|---|:---:|
| SCR-001 | 홈 | `/` | O |
| SCR-002 | 여행지 상세 | `/destinations/[slug]` | - |
| SCR-003 | 여행 준비 허브 (항공·숙소·동행 구하기 탭) | `/flights`, `/hotels`, `/mates` 통합 | O |
| SCR-004 | 동행 모집글 목록·상세 | `/mates`, `/mates/[id]` | - |
| SCR-005 | 인증·계정 허브 (Member/Admin 영역 포함) | `/auth/*`, `/my/*`, `/admin/*` 진입점 | - |

> 각 화면의 Section 순서·최소 콘텐츠 수·탭 구성 계약은 `design-reference/D-001/DESIGN.md` §15-5에 정의되어 있다. 이 매니페스트는 어떤 버전이 현재 유효한지를 가리키는 색인이며, 화면 규칙 본문은 Active File에서만 관리한다.

## 근거 문서

| 문서 | 역할 |
|---|---|
| `docs/00_PRD_Travel_v1.md` | 제품 요구사항, 사이트맵, 콘텐츠 최소 기준 |
| `docs/05_SRS_Travel_v1.md` | 기능/비기능 요구사항, Route Inventory, 데이터 모델 |
| `design-reference/vendor/airbnb/DESIGN.md` | 레이아웃 문법 참고용 벤더 분석(색상·폰트·상표는 이식 금지) |
| `docs/STITCH_VALIDATION_REPORT.md` | Stitch 프로젝트 자동 시각 검증 결과(BLOCKED — 사람 검수 필요, 참고 각주 §서두) |

## 변경 이력

| 버전 | 날짜 | 상태 | 변경 내용 |
|---|---|---|---|
| D-001 | 2026-09-15 | LOCKED | 최초 Traveler 전용 디자인 정본 작성. Airbnb 벤더 분석의 레이아웃 문법만 계승하고 색상·폰트·상표·구매/예약 UI는 전면 재설계. SCR-001~005 및 Mobile 변형(SCR-001, SCR-003) 화면 계약 정의. |

## 정본 변경 규칙

1. `Active Design Version`을 바꾸려면 새 `design-reference/D-00N/DESIGN.md`를 작성하고 이 매니페스트의 `Active Design Version`, `Active File`, `Status`, 변경 이력을 함께 갱신한다.
2. `Status: LOCKED`인 동안 Active File은 오탈자·오류 수정 외의 구조 변경을 허용하지 않는다. 구조 변경이 필요하면 새 버전을 발행한다.
3. Approved Screens/Mobile Variants 목록을 변경하려면 화면 승인 근거(재검증 리포트 등)를 함께 기록한다.
4. 이 매니페스트에 없는 색상·폰트·컴포넌트를 Active File 밖에서 임의로 추가하지 않는다.
