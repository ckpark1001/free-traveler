# Free Traveler — Project State

- **As of:** 2026-10-10 (CI·테스트 도구 항목을 실제 저장소 상태로 재확인·갱신)
- **작성 근거:** 이 문서는 저장소를 직접 확인해 작성한 스냅샷이다. 값을 추정하거나 낙관적으로 채우지 않았다 — 확인되지 않은 값은 "미확인"이 아니라 실제 부재 상태 그대로("없음", "미구성", "0/63") 적었다.
- **갱신 방법:** `TASKS/WAVE_STATE.json`이 생기면 그 파일이 이 문서의 1차 정본이 된다. `/run-wave`가 `WAVE_STATE.json`을 갱신할 때마다 이 문서도 그 값을 반영해 갱신한다. `WAVE_STATE.json`이 없는 지금은 저장소의 다른 실제 산출물(`TASKS/*`, `app/package.json`, `.github/`, `supabase/` 등)을 직접 확인해 채운다.

---

## 필드

| 필드 | 값 |
|---|---|
| **Harness Schema** | `traveler-screen-route-v1` (`design-reference/SCREEN_ROUTE_CONTRACT.json`의 `schema_version`과 일치, `CLAUDE.md` Harness Marker와 동일) |
| **Design Version** | `D-001` — Status: `LOCKED` (`design-reference/D-001/DESIGN.md`, `design-reference/DESIGN_MANIFEST.md`) |
| **Scope Mode** | `app/docs/PROJECT_SCOPE.md` 확정 범위 — REQ 114개 중 IMPLEMENT 90개 / EXCLUDED 24개, Guest·Member·Admin 3단계 역할, 정적 데이터 3도메인, DB 6테이블 |
| **Current Wave** | 없음 — `TASKS/WAVE_PLAN.md`가 아직 없어 어떤 Wave도 시작되지 않았다 |
| **Current Task** | 없음 — 착수된 Task 없음 |
| **Completed Tasks** | 0 / 63 (`TASKS/TASK_MANIFEST.csv` 기준. `app/src/app`에는 `create-next-app` 기본 스타터(`layout.tsx`, `page.tsx`, `globals.css`, `favicon.ico`)만 존재하고 어떤 Task도 구현되지 않았다) |
| **Blocked Tasks** | 0 — 아직 어떤 Task도 `/prepare-task`·`/implement-task`로 시도되지 않았다(시도 자체가 없어 BLOCKED 기록도 없음) |
| **Latest CI** | 워크플로 파일만 있음 — `.github/workflows/ci.yml`(format:check·lint·typecheck·test:unit 등). 실행 이력은 확인되지 않음(Git 저장소가 아니며 GitHub Actions 실행 기록 없음). `CI-TYPECHECK-LINT` Task는 `DONE`으로 기록되지 않음 |
| **Supabase State** | 미구성 — `supabase/` 디렉터리 없음, 로컬/원격 프로젝트 연결 정보 없음, `app/package.json`에 `@supabase/supabase-js`·`@supabase/ssr` 의존성 없음. 6개 Table(`profiles`, `mate_posts`, `mate_applications`, `blocks`, `reports`, `app_settings`) 중 실제로 생성된 것 0개 |
| **Vercel Preview URL** | 없음 — 배포 이력 없음 |
| **Screen Checkpoints** | 아래 표 참고(전부 `PENDING`) |
| **Playwright State** | 설치·설정됨, 실행 이력 없음 — `app/package.json`에 `@playwright/test`, `app/playwright.config.ts`, `app/tests/e2e/public-smoke.spec.ts`·`auth-smoke.spec.ts` 존재. 화면 미구현으로 통과 확인 안 됨. `E2E-*` Task는 `DONE`으로 기록되지 않음 |
| **Deferred Items** | 아래 "Deferred Items" 절 참고 |
| **Next Action** | 아래 "Next Action" 절 참고 |

### Screen Checkpoints

| Screen | Route | Checkpoint |
|---|---|---|
| SCR-001 | `/` | PENDING |
| SCR-002 | `/about` | PENDING |
| SCR-003 | `/travel-tools` | PENDING |
| SCR-004 | `/mates` | PENDING |
| SCR-005 | `/account` | PENDING |
| FINAL | — | PENDING |

각 Checkpoint는 해당 Page Owner Task가 `DONE`이고 사람이 Vercel Preview를 직접 확인했을 때만 `PASSED`로 바뀐다(`CLAUDE.md` 규칙 22, `/run-wave`의 Preview Checkpoint). `FINAL`은 `/release-check`가 `RELEASE_READY`를 낸 시점에만 `PASSED`로 바뀐다.

---

## Deferred Items

### EXCLUDED 요구사항 (24개, `app/docs/PROJECT_SCOPE.md` 확정, 삭제되지 않음)

| 사유 그룹 | 개수 | 대표 항목 |
|---|---:|---|
| 콘텐츠 CMS·미디어 라이선스 워크플로 미구축 | 6 | REQ-FUNC-007, 061, 072, 073, 074, REQ-NF-029 |
| Editor/Moderator 세분화 권한·감사 로그 미구축 | 10 | REQ-FUNC-045, 055, 056, 075, 076, REQ-NF-018, 020, 021, 022, 032 |
| 행동 분석·성능 CI·장애 알림 자동화 미구축 | 8 | REQ-FUNC-071, REQ-NF-007, 008, 009, 010, 011, 024, 033 |

전체 목록과 근거·후속 방향은 `TASKS/00_TASK_LIST.md` §2(NON_IMPLEMENTATION)에 있다.

### 착수 차단(Onboarding Blockers) — `app/docs/ARCHITECTURE.md` §16과 동일, 재확인됨

| 항목 | 상태 |
|---|---|
| `.env.local`/`.env.example` | 없음 — `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `FLIGHT_OUTBOUND_URL`, `HOTEL_OUTBOUND_URL`, `MOFA_SAFETY_URL` 미정의 |
| Supabase 의존성 | `app/package.json`에 `@supabase/supabase-js`·`@supabase/ssr` 없음 (Vitest·Playwright는 설치됨) |
| `supabase/` 디렉터리 | 없음 |
| `.github/workflows/` | `ci.yml` 있음 (해소됨) |
| `vitest.config.ts`/`playwright.config.ts` | 둘 다 `app/`에 있음 (해소됨) |
| `TASKS/WAVE_PLAN.md` | 없음 — `/run-wave`·`/prepare-task`가 실행될 수 없는 상태 |

---

## Next Action

1. `TASKS/WAVE_PLAN.md`를 작성한다(Wave별 Task 순서, Preview Checkpoint 지정) — 이것이 없으면 `/run-wave`·`/prepare-task`가 전부 `BLOCKED_INPUT`을 낸다.
2. 착수 차단 항목 중 최소한 첫 Wave에 필요한 것부터 해소한다: `.env.local` 생성, `app/package.json`에 Supabase 의존성 추가(`@supabase/supabase-js`, `@supabase/ssr`). Vitest·Playwright는 이미 설치됨.
3. 위 두 가지가 끝나면 `/run-wave W01`(또는 `WAVE_PLAN.md`가 정의하는 첫 Wave ID)로 실행을 시작한다.
4. 각 Screen의 Page Owner Wave가 끝날 때마다 이 문서의 해당 Screen Checkpoint를 사람이 Preview 확인 후 `PASSED`로 갱신한다.
