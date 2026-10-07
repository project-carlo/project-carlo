import { test, expect } from "@playwright/test";

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
