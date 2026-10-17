import { test, expect, type Page, type Request } from "@playwright/test";

/** A church whose page links its bulletin. */
const ST_ANTHONY = "/churches/st-anthony-of-padua-buffalo/";

interface SentBatch {
  session: string;
  device: string;
  events: { name: string; path: string; kind?: string; target?: string; entry?: boolean }[];
}

/**
 * Analytics stays off in automated browsers (navigator.webdriver), so these
 * tests turn it on as a visitor's browser would have it.
 */
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(Navigator.prototype, "webdriver", { get: () => false });
  });
});

/** Leaves the page as far as analytics can tell, and returns what it sent. */
async function leave(page: Page): Promise<{ request: Request; batch: SentBatch }> {
  const sent = page.waitForRequest("**/api/events");
  await page.evaluate(() => window.dispatchEvent(new Event("pagehide")));
  const request = await sent;
  return { request, batch: JSON.parse(request.postData() ?? "null") as SentBatch };
}

test("a prerendered page sends its pageview and outbound clicks in one batch", async ({
  page,
  context,
}) => {
  await page.goto(ST_ANTHONY);
  // The bulletin opens in a new tab; only that it was followed matters.
  await context.route(/^https?:\/\/(?!127\.0\.0\.1)/, (route) => route.abort());
  await page.locator('a[data-track="bulletin"]').click();

  const { request, batch } = await leave(page);
  expect(batch.session).toMatch(/^[a-z0-9]{16}$/);
  expect(batch.device).toBe("desktop");
  expect(batch.events).toEqual([
    expect.objectContaining({ name: "pageview", path: ST_ANTHONY, entry: true }),
    expect.objectContaining({ name: "outbound", path: ST_ANTHONY, kind: "bulletin" }),
  ]);
  const response = await request.response();
  expect(response?.status()).toBe(204);
});

test("the app sends a pageview per page, in the same visit as the one before", async ({
  page,
}) => {
  await page.goto(ST_ANTHONY);
  const first = await leave(page);

  await page.goto("/");
  await expect(page.locator(".leaflet-container")).toBeVisible();
  const second = await leave(page);
  expect(second.batch.session).toBe(first.batch.session);
  expect(second.batch.events).toEqual([
    expect.objectContaining({ name: "pageview", path: "/", entry: false }),
  ]);
});

test("the Worker refuses what isn't a batch", async ({ request }) => {
  expect((await request.get("/api/events")).status()).toBe(405);
  expect((await request.post("/api/events", { data: "nonsense" })).status()).toBe(400);
  expect(
    (
      await request.post("/api/events", {
        data: { session: "0123456789abcdef", events: [{ name: "pageview", path: "/" }] },
      })
    ).status(),
  ).toBe(204);
});
