import { test, expect } from "@playwright/test";

/**
 * 공개 열람 Smoke(Chromium, 로그인 불필요) -- E2E-001 ~ E2E-005.
 *
 * Selector 우선순위: role > label > test id > text/CSS. role/label만으로
 * 식별하기 어려운 요소(추천 여행지 카드, 화면 간 이동 CTA)는 아래 data-testid
 * 계약을 전제로 한다. 아직 구현되지 않은 Component Task가 이 훅을 마크업에
 * 부여해야 해당 assertion이 통과한다.
 *
 *  - [data-testid="destination-card"]  SCR-001 여행지 추천 카드(CMP-SCR001-DESTINATION-GRID)
 *  - [data-testid="cta-about"]         SCR-001 -> /about 이동 CTA(CMP-SCR001-ABOUT-SUMMARY)
 *  - [data-testid="cta-travel-tools"]  SCR-001 -> /travel-tools 이동 CTA(Hero 보조 CTA)
 *  - [data-testid="cta-mates"]         SCR-001 -> /mates 이동 CTA(CMP-SCR001-MATE-TEASER)
 *
 * 외부 사이트(항공/호텔 실제 목적지)는 새 탭 링크의 속성(href/target/rel)만
 * 검사하고, 실제로 열어 그 사이트의 콘텐츠를 검사하지 않는다.
 */

test.describe("public-smoke", () => {
  test("E2E-001 메인 페이지의 추천 여행지와 주요 CTA", async ({ page }) => {
    await page.goto("/");

    const destinationCards = page.getByTestId("destination-card");
    await expect(destinationCards.first()).toBeVisible();
    expect(await destinationCards.count()).toBeGreaterThan(0);

    for (const card of await destinationCards.all()) {
      // 빈 카드(제목/이미지 없이 노출되는 카드) 금지 -- 접근성 이름이 비어있지 않아야 한다.
      await expect(card).toHaveAccessibleName(/.+/);
    }

    const ctaAbout = page.getByTestId("cta-about");
    await expect(ctaAbout).toBeVisible();
    await expect(ctaAbout).toHaveAttribute("href", "/about");

    const ctaTravelTools = page.getByTestId("cta-travel-tools");
    await expect(ctaTravelTools).toBeVisible();
    await expect(ctaTravelTools).toHaveAttribute("href", "/travel-tools");

    const ctaMates = page.getByTestId("cta-mates");
    await expect(ctaMates).toBeVisible();
    await expect(ctaMates).toHaveAttribute("href", "/mates");
  });

  test("E2E-002 대표 소개의 free_traveler, 50회 이상, 30개국 이상", async ({
    page,
  }) => {
    await page.goto("/about");

    // REQ-FUNC-057: 대표명 free_traveler, 50+ Trips, 30+ Countries를 표시한다.
    await expect(page.getByText("free_traveler").first()).toBeVisible();
    await expect(page.getByText(/50\s*\+|50회\s*이상/).first()).toBeVisible();
    await expect(page.getByText(/30\s*\+|30개국\s*이상/).first()).toBeVisible();
  });

  test("E2E-003 여행 도구의 항공 외부 이동 안내와 href", async ({ page }) => {
    await page.goto("/travel-tools");

    await page.getByRole("tab", { name: "항공 찾기" }).click();

    await page.getByLabel(/국가/).fill("일본");
    await page.getByLabel(/지역|도시/).fill("도쿄");
    await page.getByLabel(/시작일|출발일/).fill("2026-11-01");
    await page.getByLabel(/종료일|도착일/).fill("2026-11-05");
    await page.getByRole("button", { name: /요약|확인/ }).click();

    // 입력값이 외부로 전달되지 않는다는 고지 배너(REQ-FUNC-015/023, 상시 노출).
    await expect(
      page.getByText("입력값은 외부 사이트로 전달되지 않습니다"),
    ).toBeVisible();

    const outboundLink = page.getByRole("link", { name: /보러\s*가기/ });
    await expect(outboundLink).toBeVisible();
    await expect(outboundLink).toHaveAttribute("target", "_blank");
    await expect(outboundLink).toHaveAttribute("rel", /noopener/);

    const href = await outboundLink.getAttribute("href");
    expect(href).toBeTruthy();
    expect(href).not.toContain("일본");
    expect(href).not.toContain("도쿄");
    expect(href).not.toMatch(
      /[?&](country|region|city|from|to|date|checkin|checkout)=/i,
    );
  });

  test("E2E-004 여행 도구의 숙소 외부 이동 안내와 href", async ({ page }) => {
    await page.goto("/travel-tools");

    await page.getByRole("tab", { name: "숙소 찾기" }).click();

    await page.getByLabel(/국가/).fill("일본");
    await page.getByLabel(/지역|도시/).fill("오사카");
    await page.getByLabel(/체크인|시작일/).fill("2026-11-01");
    await page.getByLabel(/체크아웃|종료일/).fill("2026-11-05");
    await page.getByRole("button", { name: /요약|확인/ }).click();

    await expect(
      page.getByText("입력값은 외부 사이트로 전달되지 않습니다"),
    ).toBeVisible();

    const outboundLink = page.getByRole("link", { name: /보러\s*가기/ });
    await expect(outboundLink).toBeVisible();
    await expect(outboundLink).toHaveAttribute("target", "_blank");
    await expect(outboundLink).toHaveAttribute("rel", /noopener/);

    const href = await outboundLink.getAttribute("href");
    expect(href).toBeTruthy();
    expect(href).not.toContain("일본");
    expect(href).not.toContain("오사카");
    expect(href).not.toMatch(
      /[?&](country|region|city|from|to|date|checkin|checkout)=/i,
    );
  });

  test("E2E-005 비로그인 동행글 작성의 로그인 안내", async ({ page }) => {
    await page.goto("/travel-tools");

    await page.getByRole("tab", { name: "동행 구하기" }).click();

    const writeCta = page
      .getByRole("button", { name: "모집글 작성" })
      .or(page.getByRole("link", { name: "모집글 작성" }));
    await writeCta.click();

    // 로그인/성인 확인 안내(Dialog 또는 인라인 안내 문구) + 로그인 진입점만 확인한다.
    await expect(
      page.getByText(/로그인.*(필요|해야|안내)|로그인한 회원만/).first(),
    ).toBeVisible();

    const loginEntry = page
      .getByRole("link", { name: /로그인/ })
      .or(page.getByRole("button", { name: /로그인/ }));
    await expect(loginEntry.first()).toBeVisible();
  });
});
