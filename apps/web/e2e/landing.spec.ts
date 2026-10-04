import { test, expect } from "@playwright/test";

test("home (landing) page mounts cleanly, with browse links and no map", async ({
  page,
}) => {
  const pageErrors: string[] = [];
  const consoleErrors: string[] = [];
  const requests: string[] = [];

  page.on("pageerror", (e) => pageErrors.push(e.message));
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("request", (req) => requests.push(req.url()));

  const response = await page.goto("/");
  expect(response?.status()).toBe(200);

  await expect(
    page.getByRole("heading", { name: /Project Carlo/i }),
  ).toBeVisible();

  // Browse section: dioceses, cities, A-Z directory.
  const browse = page.getByRole("region", { name: "Browse parishes" });
  await expect(browse.getByRole("link", { name: /Diocese of Rochester/ })).toHaveAttribute(
    "href",
    "/dioceses/rochester/",
  );
  await expect(browse.getByRole("link", { name: /All parishes A–Z/ })).toHaveAttribute(
    "href",
    "/churches/",
  );

  await page.waitForLoadState("networkidle");
  // Leaflet stays out of the landing page's load.
  expect(requests.filter((u) => /\/assets\/map-/.test(u))).toEqual([]);

  expect(pageErrors, pageErrors.join("\n")).toEqual([]);
  expect(consoleErrors, consoleErrors.join("\n")).toEqual([]);
});

test("/landing redirects to /", async ({ page }) => {
  await page.goto("/landing");
  await expect(page).toHaveURL(/\/$/);
  await expect(
    page.getByRole("heading", { name: /Project Carlo/i }),
  ).toBeVisible();
});

test("the Map link in the header goes to /map", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("navigation", { name: "Site" }).getByRole("link", { name: "Map" }).click();
  await expect(page).toHaveURL(/\/map$/);
  await expect(page.locator(".leaflet-container")).toBeVisible({
    timeout: 15_000,
  });
});
