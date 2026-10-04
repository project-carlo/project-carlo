import { test, expect } from "@playwright/test";

test.describe("results list, desktop", () => {
  test.use({ viewport: { width: 1280, height: 800 } });

  test("lists the churches in view beside the map, and sorts", async ({
    page,
  }) => {
    await page.goto("/map");
    const rows = page.locator("ol[aria-label='Churches in this area'] > li");
    await expect(rows.first()).toBeVisible({ timeout: 15_000 });
    await expect(page.getByRole("status")).toContainText(
      /\d+ churches? in this area · \d+ in all/,
    );

    // Each row links to its church page and shows a next time.
    await expect(rows.first().getByRole("link").first()).toHaveAttribute(
      "href",
      /^\/churches\/.+\/$/,
    );
    await expect(rows.first()).toContainText(/Next Mass/);

    await page.getByRole("button", { name: "Soonest" }).click();
    await expect(page).toHaveURL(/sort=soonest/);

    // Filters live in the second tab.
    await page.getByRole("tab", { name: /Filters/ }).click();
    await expect(page.getByText("Service type")).toBeVisible();
  });

  test("an unmatchable filter shows the empty state with a way out", async ({
    page,
  }) => {
    await page.goto("/map?type=confession&days=sun&from=0300&to=0305");
    await expect(page.getByText(/No churches with/)).toBeVisible({
      timeout: 15_000,
    });
    await page.getByRole("button", { name: "Clear time filter" }).click();
    await expect(
      page.locator("ol[aria-label='Churches in this area'] > li").first(),
    ).toBeVisible();
  });
});

test.describe("results list, phone", () => {
  test.use({ viewport: { width: 390, height: 844 }, hasTouch: true });

  test("the List / Map pill swaps views and keeps Back working", async ({
    page,
  }) => {
    await page.goto("/map");
    await expect(page.locator(".leaflet-marker-icon").first()).toBeVisible({
      timeout: 15_000,
    });

    await page.getByRole("button", { name: "Show results as a list" }).click();
    await expect(page).toHaveURL(/view=list/);
    const rows = page.locator("ol[aria-label='Churches in this area'] > li");
    await expect(rows.first()).toBeVisible();

    // "Show on map" returns to the map with that church's popup open.
    await rows.first().getByRole("button", { name: /Show .* on map/ }).click();
    await expect(page).not.toHaveURL(/view=list/);
    await expect(page.locator(".leaflet-popup")).toBeVisible({
      timeout: 10_000,
    });

    // Back goes to the list, as with any other screen.
    await page.goBack();
    await expect(page).toHaveURL(/view=list/);
    await expect(rows.first()).toBeVisible();
  });

  test("view=list opens straight into the list", async ({ page }) => {
    await page.goto("/map?view=list");
    await expect(
      page.locator("ol[aria-label='Churches in this area'] > li").first(),
    ).toBeVisible({ timeout: 15_000 });
    await page.getByRole("button", { name: "Show results on the map" }).click();
    await expect(page).not.toHaveURL(/view=list/);
  });
});
