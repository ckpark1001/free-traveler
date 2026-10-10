# Free Traveler — Architecture

- **문서 목적:** Free Traveler MVP의 구현 경계(어디까지 만들고 어디서 멈추는지)를 확정한다. 일반적인 Next.js 안내서가 아니라 이 프로젝트에만 적용되는 결정을 기록한다.
- **근거 문서:** `app/package.json`, `app/docs/06_SRS_UIUX_REVISED.md`, `app/docs/PROJECT_SCOPE.md`, `design-reference/D-001/DESIGN.md`, `design-reference/UI_CONTRACT.md`, `design-reference/SCREEN_ROUTE_CONTRACT.json`, `TASKS/TASK_MANIFEST.csv`
- **상태:** 코드 작성 이전 시점의 아키텍처 확정본. 실제 구현 여부는 `TASKS/TASK_MANIFEST.csv`와 각 `TASKS/TASK-*.md`를 따른다.

---

## 1. 기술 스택

`app/package.json` 기준 현재 설치된 스택:

| 영역 | 기술 | 비고 |
|---|---|---|
| 프레임워크 | Next.js 16(App Router) | `app/src/app` 디렉터리 기반 라우팅만 사용, Pages Router 사용 안 함 |
| 언어 | TypeScript 5 | 모든 소스는 `.ts`/`.tsx` (`.js` 신규 작성 금지) |
| UI 런타임 | React 19 | Server Component가 기본값 |
| 스타일 | Tailwind CSS v4 | `design-reference/D-001/DESIGN.md` 토큰을 `@theme`로 이식 |
| Lint | ESLint 9 (`eslint-config-next`) | `next lint`로 실행 |

Supabase SDK, Vitest, Playwright는 **아직 `package.json`에 없다** — §9 착수 차단 참고.

---

## 2. 화면 구성 — 핵심 4개 + 보조 1개

`design-reference/SCREEN_ROUTE_CONTRACT.json`이 Screen 목록의 정본이다.

| Screen ID | 분류 | Route | Page Entry |
|---|---|---|---|
| SCR-001 | 핵심 | `/` | `src/app/page.tsx` |
| SCR-002 | 핵심 | `/about` | `src/app/about/page.tsx` |
| SCR-003 | 핵심 | `/travel-tools` | `src/app/travel-tools/page.tsx` |
| SCR-004 | 핵심 | `/mates` | `src/app/mates/page.tsx` |
| SCR-005 | 보조 | `/account` | `src/app/account/page.tsx` |

Page Entry는 정확히 이 5개뿐이며, 각 Page Entry는 하나의 Page Owner Task(`TASKS/TASK_MANIFEST.csv`의 `PAGE-SCR00N`)만 소유한다.

---

## 3. Server Component와 Client Component 경계

Next.js App Router의 기본값은 **Server Component**다. `"use client"`를 명시한 파일만 Client Component다.

| 위치 | 기본 유형 | 이유 |
|---|---|---|
| 5개 Page Entry(`page.tsx`) | Server Component | `src/data` 정적 데이터 import, Supabase 서버 클라이언트로 읽기 전용 조회, 하위 Component 조립만 수행 |
| `src/components/**` 중 표시 전용(카드 그리드, Timeline, Gallery, Drawer의 정적 내용 등) | Server Component | 상호작용이 없으면 클라이언트 번들에 포함시키지 않는다 |
| `src/components/**` 중 상호작용 컴포넌트(항공/숙소 Form, 탭, 필터 바, Drawer/Modal 열고 닫기, 신고·차단 Dialog, 인증 Form, Admin Form) | Client Component(`"use client"`) | `useState`/이벤트 핸들러/브라우저 API(Web Share, `window.open`)가 필요 |
| `src/app/api/**/route.ts` | Route Handler(서버 전용) | Client Component의 쓰기 요청을 받아 Supabase 서버 클라이언트로 처리 |

원칙: **상호작용이 없는 코드는 기본값(Server)으로 두고, `"use client"`는 실제로 이벤트·상태·브라우저 API가 필요한 최소 단위에만 붙인다.**

---

## 4. 항공·숙소 입력 폼 — Client Component의 일시 상태만 사용

- `CMP-SCR003-FLIGHT-FORM`, `CMP-SCR003-HOTEL-FORM`은 각각 하나의 Client Component이며, 국가·지역·시작일·종료일(또는 체크인·체크아웃) 값을 **그 컴포넌트의 React state(`useState`)로만** 보관한다.
- 폼 → 요약 전환은 같은 컴포넌트 안에서 로컬 상태로 뷰만 바꾸는 것이며, 라우트 이동이나 서버 요청을 동반하지 않는다.
- `localStorage`/`sessionStorage`/쿠키에 이 값을 쓰지 않는다. 페이지를 벗어나거나 새로고침하면 값은 사라진다 — 이는 버그가 아니라 의도된 동작이다.
- 즐겨찾기(`SHARED-FAVORITES-LOCALSTORAGE`)만 `localStorage`를 쓰며, 이는 여행지 ID 집합일 뿐 항공·숙소 조건과 무관하다.

---

## 5. 항공·숙소 입력값 비전송 보장

다음 중 어느 것도 국가·지역·날짜 원시값을 포함해서는 안 된다.

- `src/app/api/**/route.ts`로의 요청 본문·쿼리 파라미터
- Supabase 테이블(어떤 테이블에도 항공·숙소 조건 컬럼을 만들지 않는다)
- 외부 이동 URL(`FLIGHT_OUTBOUND_URL`, `HOTEL_OUTBOUND_URL`)의 쿼리 스트링 — `SHARED-OUTBOUND-LINK-UTIL`은 목적지 URL을 그대로 새 탭으로 열 뿐 파라미터를 추가하지 않는다
- `console.log`/서버 로그/향후 도입될 분석 이벤트

검증 방법: `E2E-TRAVEL-TOOLS`(Playwright에서 새 탭 URL과 네트워크 요청 어서션), 코드 리뷰. 이 보장은 `CON-01`·`CON-02`(SRS)와 직접 연결된다.

---

## 6. 정적 데이터 — 여행지·안전정보·대표 소개

세 도메인은 Supabase 테이블이 아니라 **`src/data`의 TypeScript 정적 모듈**로 관리한다.

| 파일 | 도메인 |
|---|---|
| `src/data/destinations.ts` | 국내·해외 여행지(국내 10개 이상, 해외 15개국 30도시 이상) |
| `src/data/country-safety.ts` | 국가별 안전정보(8개 필수 카테고리) |
| `src/data/representative-profile.ts` | `free_traveler` 대표 프로필 |

Server Component가 이 모듈을 직접 `import`해서 렌더링한다 — 런타임 API 호출도, DB 조회도 없다. 콘텐츠 갱신은 이 파일을 코드로 수정하고 재배포하는 방식이며, 별도 CMS는 없다(§10).

---

## 7. Supabase 사용 범위 — Auth와 동행(Mate) 기능 중심

Supabase는 다음 두 가지 목적에만 쓴다.

1. **Auth**: 이메일 가입·인증·로그인·로그아웃·비밀번호 재설정, 세션 관리.
2. **동행(Mate) 기능의 쓰기 데이터**: 모집글, 참가 요청, 차단, 신고, 관리자 외부 URL 설정.

여행지·안전정보·대표 소개(§6)는 Supabase를 쓰지 않는다. Supabase Storage도 쓰지 않는다(이미지는 URL+alt만 사용).

---

## 8. Database — 정확히 6개 Table

`TASKS/TASK-DB-SCHEMA-BASE.md`가 정의한 범위를 그대로 따른다. 이 6개를 넘는 테이블을 추가하지 않는다.

| Table | 목적 |
|---|---|
| `profiles` | 동행 프로필(닉네임·연령대·성별·여행스타일), 성인 확인 상태(`is_adult`, `adult_verified_at` — 정확한 생년월일 없음), 관리자 여부(`is_admin`) |
| `mate_posts` | 동행 모집글 |
| `mate_applications` | 참가 요청(비공개 메시지, 상태) |
| `blocks` | 사용자 차단 관계 |
| `reports` | 신고 접수·처리 상태 |
| `app_settings` | 관리자가 설정하는 항공·호텔 외부 URL |

---

## 9. Supabase Client — Browser와 Server 분리

`@supabase/ssr` 기반으로 두 개의 클라이언트 헬퍼를 둔다(서비스 롤 키는 어디에서도 사용하지 않는다 — Admin도 인증된 사용자 세션 + RLS로 처리한다).

| 파일 | 실행 위치 | 용도 |
|---|---|---|
| `src/lib/supabase/server-client.ts` | Server Component, Route Handler | 쿠키 기반 세션으로 RLS가 적용된 조회·쓰기(`DB-ACCESS` Task 범위) |
| `src/lib/supabase/browser-client.ts` | Client Component | 로그인/가입/로그아웃/비밀번호 재설정 등 브라우저에서 직접 호출하는 Supabase Auth 흐름(`CMP-SCR005-AUTH` Task 범위) |

두 클라이언트 모두 `anon key`만 사용하고 `service_role` 키를 클라이언트 번들이나 서버 코드 어디에도 포함하지 않는다.

---

## 10. 간단한 RLS 원칙

정교한 역할 시스템 대신 아래 세 가지 규칙만 사용한다(`TASKS/TASK-DB-RLS-BASE.md`와 동일).

1. **본인 소유**: `user_id = auth.uid()`인 행은 본인이 읽고 쓸 수 있다.
2. **관계자 예외**: `mate_applications`은 모집글 작성자(`mate_posts.owner_id`)도 조회할 수 있다(참가 요청을 봐야 하므로).
3. **Admin 예외**: `profiles.is_admin = true`인 사용자는 `reports`, `mate_applications`, `blocks`, `app_settings`을 추가로 조회·수정할 수 있다.

차단 관계(`blocks`)에 있는 두 사용자는 위 규칙과 별개로 서로의 `mate_posts`/`reports`가 조회 결과에서 제외된다. 역할은 커스텀 JWT 클레임이나 별도 역할 테이블 없이 `profiles.is_admin` 컬럼 하나로 판별한다.

---

## 11. ORM 미사용

Prisma, Drizzle 등 어떤 ORM도 쓰지 않는다.

- 스키마·RLS는 `supabase/migrations/*.sql`에 순수 SQL로 작성한다(Supabase CLI 마이그레이션).
- 쿼리는 `src/lib/supabase/queries.ts`에서 `@supabase/supabase-js`의 쿼리 빌더를 직접 호출한다.
- 테이블 타입은 손으로 작성한 TypeScript 인터페이스를 쓰거나, 필요 시 `supabase gen types typescript`로 생성한다(선택 사항이며 별도 ORM이 아니다).

---

## 12. 테스트 — Vitest + Playwright Chromium Smoke

| 계층 | 도구 | Task | 대상 |
|---|---|---|---|
| Unit | Vitest | `UNIT-TRAVEL-DATES`, `UNIT-CONTACT-DETECTION`, `UNIT-MATE-STATE` | 날짜 검증, 연락처 탐지, 동행 상태 전이 |
| Integration | Vitest(+로컬 Supabase) | `TEST-RLS-BASIC` | RLS 정책 |
| E2E | Playwright, **Chromium 프로젝트만** | `E2E-PUBLIC-SMOKE`, `E2E-TRAVEL-TOOLS`, `E2E-MATE-AUTH` | 핵심 흐름 Smoke(`app/docs/PROJECT_SCOPE.md` §9 SM-01~SM-10) |

Playwright 설정에 Firefox/WebKit/Safari 프로젝트를 추가하지 않는다. 별도의 부하 테스트·시각 회귀 테스트 도구는 도입하지 않는다.

---

## 13. CI/CD — GitHub Actions + Vercel Preview

- **GitHub Actions**: PR마다 타입체크(`tsc --noEmit`), Lint(`next lint`), Vitest, Playwright(Chromium)를 실행한다. 커스텀 배포 스크립트나 셀프호스팅 러너는 두지 않는다.
- **Vercel**: PR마다 자동 Preview 배포, `main` 병합 후 Production 배포. Vercel이 기본 제공하는 흐름을 그대로 쓰고 별도 배포 파이프라인을 만들지 않는다.
- 병합은 **사람이 리뷰 후 수동으로** 한다 — 자동 Merge 봇/워크플로를 두지 않는다(§14).

---

## 14. 명시적으로 쓰지 않는 인프라

- **AWS·EC2**: 사용하지 않는다. 배포는 Vercel, 데이터베이스는 Supabase로 한정한다. 별도 VM·컨테이너·클라우드 계정을 만들지 않는다.
- **자동 Merge**: `automerge`/머지봇/GitHub Actions의 auto-merge 기능을 어떤 워크플로에도 넣지 않는다. 모든 병합은 리뷰 승인 후 사람이 직접 누른다.

---

## 15. 프로젝트 범위 밖(명시적 제외)

| 항목 | 제외 이유 및 대체 |
|---|---|
| **CMS(콘텐츠 관리 시스템)** | 여행지·안전정보·대표 소개는 개발자가 `src/data`를 코드로 직접 수정한다(§6). 작성-검수-게시 워크플로, DRAFT/REVIEW/PUBLISHED 상태 전이 UI를 만들지 않는다. |
| **외부 Email 공급자** | 회원가입·인증 메일은 Supabase Auth 기본 메일만 쓴다. SendGrid 등 트랜잭셔널 이메일 서비스를 연동하지 않는다. 참가 요청·신고 처리 알림은 인앱 Toast/화면 상태로만 제공한다. |
| **Monitoring/Observability** | Sentry, Datadog 등 별도 모니터링·에러 추적·로그 수집 도구를 도입하지 않는다. Vercel 기본 로그·Web Vitals 수준에 의존한다. |

---

## 16. 착수 차단(Onboarding Blockers)

아래는 저장소 현재 상태를 직접 확인해 실제로 없는 파일·환경변수만 기록한 것이다(가정이나 권장 사항이 아니다).

| 항목 | 없는 것 | 막히는 작업 |
|---|---|---|
| 환경변수 파일 | `.env.local`/`.env.example`이 저장소에 없음. 최소 `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `FLIGHT_OUTBOUND_URL`, `HOTEL_OUTBOUND_URL`, `MOFA_SAFETY_URL` 필요 | Supabase 연동, 외부 이동 URL 설정 |
| 패키지 의존성 | `app/package.json`에 `@supabase/supabase-js`, `@supabase/ssr`, `vitest`, `@playwright/test`가 없음 | `DB-ACCESS`, `UNIT-*`, `TEST-RLS-BASIC`, `E2E-*` Task 착수 |
| Supabase 프로젝트 구성 | `supabase/` 디렉터리(마이그레이션·시드 둘 위치)가 없고 로컬/원격 Supabase 프로젝트 연결 정보가 없음 | `DB-SCHEMA-BASE`, `DB-RLS-BASE`, `DB-SEED-BASE` Task 착수 |
| CI 설정 | `.github/workflows/`가 없음 | `CI-TYPECHECK-LINT` Task 착수 |
| 테스트 설정 파일 | `vitest.config.ts`, `playwright.config.ts`가 없음 | 모든 Unit/E2E Task 착수 |

이 표에 없는 항목(예: 특정 컴포넌트 파일, Route Handler)은 아직 구현되지 않았을 뿐 "차단"이 아니다 — `TASKS/TASK_MANIFEST.csv`의 정상적인 착수 대상이다.
