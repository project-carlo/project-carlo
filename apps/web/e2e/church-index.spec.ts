import { test, expect, type Page } from "@playwright/test";

test("the church index filters by city name", async ({ page }) => {
  await page.goto("/churches/");
  const search = page.getByRole("searchbox", { name: "Search churches and cities" });
  await expect(search).toBeVisible();

  const groups = page.locator("[data-city-group]");
  const total = await groups.count();
  const label = (await groups.first().locator("h2").textContent())!.trim();
  await search.fill(label);

  await expect(groups.first()).toBeVisible();
  const visible = groups.filter({ visible: true });
  expect(await visible.count()).toBeGreaterThan(0);
  expect(await visible.count()).toBeLessThan(total);
  await expect(page.locator("#church-search-status")).toHaveText(
    /^Showing \d+ of \d+ churches\.$/,
  );

  await search.press("Escape");
  await expect(groups.filter({ visible: true })).toHaveCount(total);
});

test("the church index filters by church name, with St. matching Saint", async ({
  page,
}) => {
  await page.goto("/churches/");
  const search = page.getByRole("searchbox", { name: "Search churches and cities" });
  const items = page.locator("[data-city-group] li");
  const total = await items.count();

  const stChurch = items.filter({ hasText: /^\s*St\. / }).first();
  const name = (await stChurch.textContent())!.trim();
  const saintQuery = name.replace(/^St\. /, "Saint ");
  await search.fill(saintQuery);

  await expect(items.filter({ hasText: name }).first()).toBeVisible();
  expect(await items.filter({ visible: true }).count()).toBeLessThan(total);
});

test("the church index says when nothing matches", async ({ page }) => {
  await page.goto("/churches/");
  await page
    .getByRole("searchbox", { name: "Search churches and cities" })
    .fill("zzzz-no-such-church");
  await expect(
    page.getByText("No churches or cities match “zzzz-no-such-church”."),
  ).toBeVisible();
  await expect(page.locator("[data-city-group]").filter({ visible: true })).toHaveCount(0);
});

/** Counts the page's document loads, the first one included. */
function countLoads(page: Page): () => number {
  let loads = 0;
  page.on("load", () => loads++);
  return () => loads;
}

/** Opens the map somewhere other than where it starts, and returns its query. */
async function moveMap(page: Page): Promise<string> {
  await page.goto("/?lat=43.15&lng=-77.6&z=10");
  const zoomIn = page.getByRole("button", { name: "Zoom in" });
  await expect(zoomIn).toBeVisible({ timeout: 15_000 });
  await zoomIn.click();
  await expect(page).toHaveURL(/[?&]z=11(&|$)/);
  return new URL(page.url()).search;
}

test("in the app, the index's Map link goes back to the map as it was, without reloading", async ({
  page,
}) => {
  await page.goto("/churches/");
  const churchHref = (await page
    .locator('[data-city-group] li a[href^="/churches/"]')
    .first()
    .getAttribute("href"))!;

  const search = await moveMap(page);
  const loads = countLoads(page);
  // Navigates in the app, as a link in a map pin's popup would.
  await page.evaluate((to) => {
    const idx = ((window.history.state as { idx?: number } | null)?.idx ?? 0) + 1;
    window.history.pushState({ usr: null, key: `e2e-${idx}`, idx }, "", to);
    window.dispatchEvent(new PopStateEvent("popstate", { state: window.history.state }));
  }, churchHref);
  const breadcrumb = page.getByRole("navigation", { name: "Breadcrumb" });
  await breadcrumb.getByRole("link", { name: "All churches" }).click();
  await expect(page).toHaveURL(/\/churches\/$/);
  await expect(page.getByRole("heading", { level: 1, name: "All churches" })).toBeVisible();

  // Its search works in the app too.
  const searchBox = page.getByRole("searchbox", { name: "Search churches and cities" });
  await searchBox.fill("zzzz-no-such-church");
  await expect(page.getByText("No churches or cities match “zzzz-no-such-church”.")).toBeVisible();

  // Note any "Loading…" the page shows from here on.
  await page.evaluate(() => {
    const w = window as typeof window & { sawLoading?: boolean };
    w.sawLoading = false;
    new MutationObserver(() => {
      if (/Loading/.test(document.body.innerText)) w.sawLoading = true;
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
  });
  await page.getByRole("link", { name: "Map", exact: true }).click();
  await expect(page.locator(".leaflet-container")).toBeVisible();
  expect(new URL(page.url()).search).toBe(search);
  expect(
    await page.evaluate(() => (window as typeof window & { sawLoading?: boolean }).sawLoading),
  ).toBe(false);
  expect(loads()).toBe(0);
});

test("the prerendered index's Map link goes back to the map as it was", async ({ page }) => {
  const search = await moveMap(page);
  await page.goto("/churches/");
  await expect(page.getByRole("link", { name: "Map", exact: true })).toHaveAttribute(
    "href",
    `/${search}`,
  );
});

test("in the app, back to the index returns to where it was left", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator(".leaflet-container")).toBeVisible({ timeout: 15_000 });
  const loads = countLoads(page);
  await page.getByRole("link", { name: "All churches" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "All churches" })).toBeVisible();

  const church = page.locator('[data-city-group] li a[href^="/churches/"]').nth(150);
  await church.scrollIntoViewIfNeeded();
  const scrollY = await page.evaluate(() => window.scrollY);
  expect(scrollY).toBeGreaterThan(1000);
  // Clicked where it is: Playwright's own click would scroll it clear of
  // the sticky header first.
  await church.evaluate((link: HTMLElement) => link.click());
  await expect(page.getByRole("navigation", { name: "Breadcrumb" })).toBeVisible();
  expect(await page.evaluate(() => window.scrollY)).toBe(0);

  await page.goBack();
  await expect(page.getByRole("heading", { level: 1, name: "All churches" })).toBeVisible();
  expect(await page.evaluate(() => window.scrollY)).toBe(scrollY);
  expect(loads()).toBe(0);
});
