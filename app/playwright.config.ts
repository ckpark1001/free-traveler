import { defineConfig, devices } from "@playwright/test";

const LOCAL_PORT = 3000;
const LOCAL_BASE_URL = `http://127.0.0.1:${LOCAL_PORT}`;

// PLAYWRIGHT_BASE_URL이 있으면 Vercel Preview 등 원격 URL을 기본값 대신 사용한다.
const baseURL = process.env.PLAYWRIGHT_BASE_URL || LOCAL_BASE_URL;
const isRemoteTarget = Boolean(process.env.PLAYWRIGHT_BASE_URL);

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["html", { outputFolder: "playwright-report" }]],
  use: {
    baseURL,
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  // Chromium 프로젝트만 사용한다(CLAUDE.md 규칙 18: Firefox/WebKit 추가 금지).
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  // PLAYWRIGHT_BASE_URL로 원격(Preview) URL을 가리킬 때는 로컬 dev 서버를 띄우지 않는다.
  webServer: isRemoteTarget
    ? undefined
    : {
        command: "npm run dev",
        url: LOCAL_BASE_URL,
        reuseExistingServer: !process.env.CI,
        timeout: 120_000,
      },
});
