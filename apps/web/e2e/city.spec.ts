import { test, expect } from "@playwright/test";

test("the parish index links each city to its prerendered city page", async ({
  page,
}) => {
  await page.goto("/churches/");
  const cityLink = page.locator('h2 a[href^="/mass-times/"]').first();
  const label = (await cityLink.textContent())!.trim();
  await cityLink.click();

  await expect(page).toHaveURL(/\/mass-times\/[a-z0-9-]+\/$/);
  await expect(
    page.getByRole("heading", { level: 1, name: `Mass Times in ${label}` }),
  ).toBeVisible();
  await expect(
    page.getByRole("navigation", { name: "Breadcrumb" }),
  ).toContainText(label);
});

test("a church page's breadcrumb leads back to its city page", async ({
  page,
}) => {
  await page.goto("/churches/");
  const cityLink = page.locator('h2 a[href^="/mass-times/"]').first();
  const cityHref = (await cityLink.getAttribute("href"))!;
  await cityLink.click();

  await page.getByRole("link", { name: "Full schedule" }).first().click();
  await expect(page).toHaveURL(/\/churches\/[^/]+\/$/);

  const breadcrumb = page.getByRole("navigation", { name: "Breadcrumb" });
  await breadcrumb.locator(`a[href="${cityHref}"]`).click();
  await expect(page).toHaveURL(cityHref);
});

test("a city with no parishes renders the not-found page", async ({ page }) => {
  const response = await page.goto("/mass-times/no-such-town-zz/");
  expect(response?.status()).toBe(200);
  await expect(
    page.getByRole("heading", { name: "City not found" }),
  ).toBeVisible({ timeout: 15_000 });
});
