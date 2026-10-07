import { test, expect } from "@playwright/test";

test("the church index links each city to its prerendered city page", async ({
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

test("a city with no churches renders the not-found page", async ({ page }) => {
  const response = await page.goto("/mass-times/no-such-town-zz/");
  expect(response?.status()).toBe(404);
  await expect(
    page.getByRole("heading", { name: "City not found" }),
  ).toBeVisible({ timeout: 15_000 });
});

const EAST_AURORA = "/mass-times/east-aurora-ny/";

test("a city page's map is live in the page, and opens to the full map view", async ({
  page,
}) => {
  await page.goto(EAST_AURORA);
  const map = page.locator(".city-map");
  await expect(map.locator(".leaflet-container")).toBeVisible({ timeout: 15_000 });
  await expect(map.locator(".church-map-marker").first()).toBeVisible();
  await expect(map.getByRole("button", { name: "Zoom in" })).toBeVisible();

  await page.getByRole("button", { name: "Expand map" }).click();
  await expect(page).toHaveURL(/#map$/);
  const dialog = page.getByRole("dialog", { name: /^Map of churches around / });
  await expect(dialog).toBeVisible();
  await expect(page.getByRole("button", { name: "Close" })).toBeFocused();
  // The home map's view: search, filters, zoom and locate.
  await expect(dialog.getByPlaceholder(/Search for a city/)).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Confession" })).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Zoom in" })).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Go to my exact location" })).toBeVisible();

  // Back closes it, leaving the city page as it was.
  await page.goBack();
  await expect(page).toHaveURL(new RegExp(`${EAST_AURORA}$`));
  await expect(dialog).toHaveCount(0);
  await expect(map.locator(".leaflet-container")).toBeVisible();

  await page.getByRole("button", { name: "Expand map" }).click();
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Expand map" })).toBeFocused();
});

test.describe("on a phone", () => {
  test.use({ viewport: { width: 390, height: 844 }, hasTouch: true });

  test("the map is live in the page and opens with filters and zoom", async ({
    page,
  }) => {
    await page.goto(EAST_AURORA);
    await expect(page.locator(".city-map .leaflet-container")).toBeVisible({
      timeout: 15_000,
    });

    await page.getByRole("button", { name: "Expand map" }).tap();
    await expect(page).toHaveURL(/#map$/);
    const dialog = page.getByRole("dialog", { name: /^Map of churches around / });
    await expect(dialog.getByRole("button", { name: "Zoom in" })).toBeVisible();

    await dialog.getByRole("button", { name: /^Filters/ }).tap();
    await expect(page.getByRole("button", { name: /^Show \d+ churches?$/ })).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(dialog).toBeVisible();

    await page.getByRole("button", { name: "Close" }).tap();
    await expect(dialog).toHaveCount(0);
    await expect(page).toHaveURL(new RegExp(`${EAST_AURORA}$`));
  });
});

test.describe("without JavaScript", () => {
  test.use({ javaScriptEnabled: false });

  test("the map preview links to the home map on the city", async ({ page }) => {
    await page.goto(EAST_AURORA);
    const preview = page.getByRole("link", {
      name: /^Open the map of churches around /,
    });
    await expect(preview).toHaveAttribute(
      "href",
      /^\/\?lat=-?[\d.]+&lng=-?[\d.]+&z=\d+$/,
    );
  });
});
