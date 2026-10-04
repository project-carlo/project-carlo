import { test, expect } from "@playwright/test";

test("map page mounts and renders cleanly", async ({ page, baseURL }) => {
  const pageErrors: string[] = [];
  const consoleErrors: string[] = [];
  const failedRequests: string[] = [];

  page.on("pageerror", (e) => pageErrors.push(e.message));
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("response", (response) => {
    const url = response.url();
    if (baseURL && url.startsWith(baseURL) && response.status() >= 400) {
      failedRequests.push(`${response.status()} ${url}`);
    }
  });

  const response = await page.goto("/map");
  expect(response?.status()).toBe(200);

  await expect(page.locator("#root")).not.toBeEmpty();

  // Leaflet container mounts (MapPage is lazy-loaded behind Suspense)
  await expect(page.locator(".leaflet-container")).toBeVisible({
    timeout: 15_000,
  });

  // The data snapshot downloaded and decoded: churches are on the map.
  await expect(page.locator(".leaflet-marker-icon").first()).toBeVisible({
    timeout: 15_000,
  });

  await page.waitForLoadState("networkidle");

  expect(pageErrors, pageErrors.join("\n")).toEqual([]);
  expect(consoleErrors, consoleErrors.join("\n")).toEqual([]);
  expect(failedRequests, failedRequests.join("\n")).toEqual([]);
});

test("old map links at /?lat=..&lng=..&z=.. redirect to /map with the query", async ({
  page,
}) => {
  await page.goto("/?lat=43.1&lng=-77.6&z=11&type=adoration");
  await expect(page).toHaveURL(/\/map\?/);
  const url = new URL(page.url());
  expect(url.pathname).toBe("/map");
  expect(url.searchParams.get("lat")).toBe("43.1");
  expect(url.searchParams.get("type")).toBe("adoration");
  await expect(page.locator(".leaflet-container")).toBeVisible({
    timeout: 15_000,
  });
});
