import { test, expect } from "@playwright/test";

test("the church index links each covered diocese to its prerendered page", async ({
  page,
}) => {
  await page.goto("/churches/");
  const dioceseLink = page.locator('[data-diocese-group] h2 a[href^="/dioceses/"]').first();
  const label = (await dioceseLink.textContent())!.trim();
  await dioceseLink.click();

  await expect(page).toHaveURL(/\/dioceses\/[a-z0-9-]+\/$/);
  await expect(
    page.getByRole("heading", {
      level: 1,
      name: `Mass, Confession & Adoration Times in the ${label}`,
    }),
  ).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Breadcrumb" })).toContainText(label);
  await expect(page.getByText(/^\d+ churches in \d+ cities and towns/)).toBeVisible();
  await expect(page.getByText("not affiliated with the diocese")).toBeVisible();
});

test("a diocese page leads to its cities, whose breadcrumbs lead back", async ({ page }) => {
  await page.goto("/dioceses/");
  const dioceseLink = page.locator('h2 a[href^="/dioceses/"]').first();
  const dioceseHref = (await dioceseLink.getAttribute("href"))!;
  await dioceseLink.click();
  await expect(page).toHaveURL(dioceseHref);

  const cities = page.getByRole("region", { name: "Cities and towns" });
  await cities.locator('a[href^="/mass-times/"]').first().click();
  await expect(page).toHaveURL(/\/mass-times\/[a-z0-9-]+\/$/);

  // City › church › back to the diocese, all through breadcrumbs.
  await page.getByRole("link", { name: "Full schedule" }).first().click();
  await expect(page).toHaveURL(/\/churches\/[^/]+\/$/);
  const breadcrumb = page.getByRole("navigation", { name: "Breadcrumb" });
  await breadcrumb.locator(`a[href="${dioceseHref}"]`).click();
  await expect(page).toHaveURL(dioceseHref);
});

test("in the app, the index's diocese link opens the diocese page", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".leaflet-container")).toBeVisible({ timeout: 15_000 });
  await page.getByRole("link", { name: "All churches" }).click();
  await page.getByRole("link", { name: "Browse by diocese" }).click();
  await expect(page).toHaveURL(/\/dioceses\/$/);
  await expect(page.getByRole("heading", { level: 1, name: "Dioceses" })).toBeVisible();

  await page.locator('h2 a[href^="/dioceses/"]').first().click();
  await expect(page).toHaveURL(/\/dioceses\/[a-z0-9-]+\/$/);
  // The map preview turns live in the app as well.
  await expect(page.locator(".city-map .leaflet-container")).toBeVisible({ timeout: 15_000 });
});

test("a diocese without a page renders the not-found page", async ({ page }) => {
  const response = await page.goto("/dioceses/no-such-diocese-zz/");
  expect(response?.status()).toBe(404);
  await expect(page.getByRole("heading", { name: "Diocese not found" })).toBeVisible({
    timeout: 15_000,
  });
});
