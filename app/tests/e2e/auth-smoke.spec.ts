import { test, expect, type Page } from "@playwright/test";

/**
 * 인증 필요 Smoke(Chromium) 골격 -- E2E-006 ~ E2E-007.
 *
 * E2E_TEST_EMAIL / E2E_TEST_PASSWORD 환경변수가 없으면(로컬 기본 상태) 이 파일
 * 전체를 명시적으로 skip한다(public-smoke.spec.ts는 영향받지 않는다). 실제
 * 값은 DB-SEED-BASE로 만든 테스트 계정을 CI Secret으로 주입한다.
 *
 * 아직 CMP-SCR003-MATE-WRITE / CMP-SCR004-* / CMP-SCR005-MY-ACTIVITY가
 * 구현되지 않아 정확한 필드 label/role을 알 수 없는 지점은 TODO로 남겨두고
 * data-testid로 임시 표시했다 -- 해당 Task 완료 후 role/label 기반으로
 * 교체한다.
 */

const E2E_TEST_EMAIL = process.env.E2E_TEST_EMAIL;
const E2E_TEST_PASSWORD = process.env.E2E_TEST_PASSWORD;
const hasAuthEnv = Boolean(E2E_TEST_EMAIL && E2E_TEST_PASSWORD);

test.describe("auth-smoke", () => {
  test.skip(
    !hasAuthEnv,
    "E2E_TEST_EMAIL/E2E_TEST_PASSWORD 환경변수가 없어 인증이 필요한 Smoke를 건너뜁니다.",
  );

  async function login(page: Page) {
    await page.goto("/account");
    await page.getByLabel(/이메일/).fill(E2E_TEST_EMAIL!);
    await page.getByLabel(/비밀번호/).fill(E2E_TEST_PASSWORD!);
    await page.getByRole("button", { name: /로그인/ }).click();
    await expect(page.getByText(/로그아웃|마이페이지/).first()).toBeVisible();
  }

  test("E2E-006 로그인 사용자의 동행글 작성과 목록·상세 확인", async ({
    page,
  }) => {
    await login(page);

    await page.goto("/travel-tools");
    await page.getByRole("tab", { name: "동행 구하기" }).click();
    await page
      .getByRole("button", { name: "모집글 작성" })
      .or(page.getByRole("link", { name: "모집글 작성" }))
      .click();

    const title = `E2E-006 테스트 모집글 ${Date.now()}`;
    await page.getByLabel(/제목/).fill(title);
    // TODO(E2E-006, CMP-SCR003-MATE-WRITE): 국가/지역/기간/모집 인원/여행
    // 스타일 태그 등 나머지 필수 필드를 실제 label에 맞춰 채운다.
    await page.getByRole("button", { name: /등록|작성 완료|게시/ }).click();

    await expect(
      page.getByText(/등록되었습니다|게시되었습니다/).first(),
    ).toBeVisible();

    await page.goto("/mates");
    const postLink = page.getByRole("link", { name: title });
    await expect(postLink).toBeVisible();
    await postLink.click();
    await expect(page.getByRole("heading", { name: title })).toBeVisible();
  });

  test("E2E-007 동행글 신청과 계정 화면의 내 활동 확인", async ({ page }) => {
    await login(page);

    await page.goto("/mates");
    // TODO(E2E-007, CMP-SCR004-FILTER-LIST/DETAIL-PANEL): 실제 카드 role/label로 교체한다.
    await page.getByTestId("mate-post-card").first().click();

    await page.getByRole("button", { name: /참가\s*요청/ }).click();
    await page
      .getByLabel(/참가 메시지|메시지/)
      .fill("E2E-007 참가 요청 테스트 메시지");
    await page.getByRole("button", { name: /제출|보내기/ }).click();

    await expect(
      page.getByText(/접수되었습니다|요청되었습니다/).first(),
    ).toBeVisible();

    await page.goto("/account");
    // TODO(E2E-007, CMP-SCR005-MY-ACTIVITY): "내 활동" 영역의 정확한 role/label로 교체한다.
    await expect(page.getByText(/참가 요청/).first()).toBeVisible();
  });
});
