import { test, expect, type Page } from "@playwright/test";

const DASHBOARD = "/admin/analytics";
const API = "**/api/admin/analytics?*";

/** A dashboard answer as the Worker gives it, with today's date in it. */
function dashboardData(days: number) {
  const today = new Date().toISOString().slice(0, 10);
  return {
    host: "projectcarlo.com",
    days,
    hosts: ["projectcarlo.com", "preview.example.workers.dev"],
    reports: [
      {
        key: "daily",
        title: "Visits and pageviews by day (UTC)",
        rows: [{ day: `${today} 00:00:00`, visits: 12, pageviews: 30 }],
      },
      { key: "pages", title: "Top pages", rows: [{ page: "/churches/st-anne/", count: 18 }] },
      { key: "countries", title: "Countries", rows: [{ country: "US", count: 30 }] },
      { key: "referrers", title: "Referring sites", rows: [] },
    ],
  };
}

/** Answers the dashboard's requests with `dashboardData`, recording each. */
async function serveDashboard(page: Page): Promise<URL[]> {
  const requests: URL[] = [];
  await page.route(API, (route) => {
    const url = new URL(route.request().url());
    requests.push(url);
    return route.fulfill({ json: dashboardData(Number(url.searchParams.get("days"))) });
  });
  return requests;
}

test("the endpoint refuses everyone while Access isn't set up", async ({ request }) => {
  const res = await request.get("/api/admin/analytics");
  expect(res.status()).toBe(503);
  expect(await res.json()).toEqual({ error: expect.stringContaining("Cloudflare Access") });
  expect(res.headers()["cache-control"]).toBe("private, no-store");

  const forged = await request.get("/api/admin/analytics", {
    headers: { "Cf-Access-Jwt-Assertion": "a.b.c" },
  });
  expect(forged.status()).toBe(503);

  const post = await request.post("/api/admin/analytics");
  expect(post.status()).toBe(405);
});

test("the page is served noindex", async ({ request }) => {
  const res = await request.get(DASHBOARD);
  expect(res.status()).toBe(200);
  expect(await res.text()).toContain('<meta name="robots" content="noindex" />');
});

test("draws the reports and refetches for another period", async ({ page }) => {
  const requests = await serveDashboard(page);
  await page.goto(DASHBOARD);

  await expect(page.getByRole("heading", { name: "Visitor analytics" })).toBeVisible();
  await expect(page.getByText("projectcarlo.com, last 7 days")).toBeVisible();
  await expect(page.locator("dd").first()).toHaveText("12");
  await expect(page.getByText("/churches/st-anne/")).toBeVisible();
  await expect(page.getByText("United States")).toBeVisible();
  await expect(page.getByText("Nothing yet.")).toBeVisible();
  // Eight days: today and the seven before it.
  await expect(page.getByRole("button", { name: /visits, \d+ pageviews/ })).toHaveCount(8);

  await page.getByRole("button", { name: "30 days" }).click();
  await expect(page.getByText("projectcarlo.com, last 30 days")).toBeVisible();
  await expect(page).toHaveURL(/days=30/);
  expect(requests.map((url) => url.searchParams.get("days"))).toEqual(["7", "30"]);

  await page.getByRole("combobox", { name: "Site" }).selectOption("preview.example.workers.dev");
  await expect.poll(() => requests.at(-1)?.searchParams.get("host")).toBe(
    "preview.example.workers.dev",
  );
});

test("fits a phone without scrolling sideways", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 740 });
  await serveDashboard(page);
  await page.goto(`${DASHBOARD}?days=90`);
  await expect(page.getByRole("button", { name: /visits, \d+ pageviews/ })).toHaveCount(91);
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  );
  expect(overflow).toBe(0);
});

test("asks to sign in again when Access refuses", async ({ page }) => {
  await page.route(API, (route) =>
    route.fulfill({
      status: 403,
      json: { error: "Sign in through Cloudflare Access to see the dashboard." },
    }),
  );
  await page.goto(DASHBOARD);
  await expect(page.getByRole("alert")).toContainText("Sign in through Cloudflare Access");
  await expect(page.getByRole("button", { name: "Sign in again" })).toBeVisible();
});

test("doesn't count itself as a pageview", async ({ page }) => {
  // Analytics is off in automated browsers; turn it on as a visitor's would be.
  await page.addInitScript(() => {
    Object.defineProperty(Navigator.prototype, "webdriver", { get: () => false });
  });
  await serveDashboard(page);
  const sent: string[] = [];
  page.on("request", (request) => {
    if (request.url().includes("/api/events")) sent.push(request.postData() ?? "");
  });
  await page.goto(DASHBOARD);
  await expect(page.getByRole("heading", { name: "Visitor analytics" })).toBeVisible();
  await page.evaluate(() => window.dispatchEvent(new Event("pagehide")));
  await page.waitForTimeout(500);
  expect(sent).toEqual([]);
});
