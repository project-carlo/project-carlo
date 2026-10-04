import { test, expect } from "@playwright/test";

// The dev/preview server runs on localhost, where /api/geo honours ?mock= and
// the pages pass ?geo= through to it (see src/lib/approxLocation.ts).

test.describe("/api/geo", () => {
  test("returns a no-store JSON guess; mocks work on localhost", async ({
    request,
  }) => {
    const res = await request.get("/api/geo?mock=rochester");
    expect(res.status()).toBe(200);
    expect(res.headers()["cache-control"]).toBe("private, no-store");
    expect(res.headers()["content-type"]).toContain("application/json");
    expect(await res.json()).toMatchObject({
      city: "Rochester",
      regionCode: "NY",
      lat: 43.1566,
      lng: -77.6088,
      source: "ip",
    });
  });

  test("answers without a mock, with the documented fields", async ({
    request,
  }) => {
    const body = await (await request.get("/api/geo")).json();
    for (const key of [
      "city",
      "region",
      "regionCode",
      "country",
      "postalCode",
      "lat",
      "lng",
      "timezone",
    ]) {
      expect(body).toHaveProperty(key);
    }
    expect(body.source).toBe("ip");
  });

  test("unknown /api/* paths are a JSON 404, not the SPA", async ({
    request,
  }) => {
    const res = await request.get("/api/nope");
    expect(res.status()).toBe(404);
    expect(res.headers()["content-type"]).toContain("application/json");
  });

  test("static routing still works around the Worker", async ({ request }) => {
    const landing = await request.get("/landing", { maxRedirects: 0 });
    expect(landing.status()).toBe(301);
    expect(landing.headers().location).toBe("/");
    const churches = await request.get("/churches", { maxRedirects: 0 });
    expect(churches.status()).toBe(301);
    expect(churches.headers().location).toBe("/churches/");
  });
});

test.describe("landing page near you", () => {
  test("the static HTML has no visitor-specific part", async ({ request }) => {
    const html = await (await request.get("/")).text();
    expect(html).not.toContain("id=\"nearby\"");
    expect(html).not.toContain("Next Mass near");
  });

  test("shows the nearest churches for an in-coverage visitor", async ({
    page,
  }) => {
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(e.message));

    await page.goto("/?geo=rochester");
    await expect(page.getByText("Near", { exact: false }).first()).toBeVisible();
    await expect(
      page.getByRole("button", { name: "change" }),
    ).toBeVisible({ timeout: 15_000 });
    await expect(page.getByText("(approximate)")).toBeVisible();

    const nearby = page.locator("#nearby");
    await expect(nearby.getByRole("heading", { name: "Nearby" })).toBeVisible();
    const rows = nearby.locator("ol > li");
    await expect(rows).toHaveCount(5, { timeout: 15_000 });
    await expect(rows.first().getByRole("link")).toHaveAttribute(
      "href",
      /^\/churches\/[^/]+\/$/,
    );

    // The Mass/Confession/Adoration switch re-ranks the list.
    await nearby.getByRole("button", { name: "Confession" }).click();
    await expect(nearby.getByText(/Next Confession near/)).toBeVisible();

    // "See all on the map" opens the map on that spot, at the same service.
    await nearby.getByRole("link", { name: /See all on the map/ }).click();
    await expect(page).toHaveURL(/\/map\?.*lat=43\.1566.*lng=-77\.6088/);
    await expect(page).toHaveURL(/type=confession/);
    expect(errors, errors.join("\n")).toEqual([]);
  });

  test("'change' focuses the search field", async ({ page }) => {
    await page.goto("/?geo=rochester");
    await page.getByRole("button", { name: "change" }).click();
    await expect(
      page.getByRole("combobox", { name: /Search for a city/ }),
    ).toBeFocused();
  });

  test("an out-of-coverage visitor gets the coverage note, not a list", async ({
    page,
  }) => {
    await page.goto("/?geo=columbus");
    const note = page.getByRole("region", { name: "Coverage" });
    await expect(note).toBeVisible({ timeout: 15_000 });
    await expect(note.getByRole("link", { name: "Rochester" })).toHaveAttribute(
      "href",
      "/dioceses/rochester/",
    );
    await expect(page.locator("#nearby ol")).toHaveCount(0);
  });

  test("a remembered place wins over the IP guess", async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem(
        "carlo:last-place",
        JSON.stringify({
          lat: 42.9,
          lng: -78.87,
          label: "Buffalo",
          source: "search",
          savedAt: Date.now(),
        }),
      );
    });
    await page.goto("/?geo=columbus");
    await expect(page.getByText("Buffalo", { exact: true }).first()).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.locator("#nearby ol > li")).toHaveCount(5, {
      timeout: 15_000,
    });
  });
});

test.describe("map default camera", () => {
  test("opens near the visitor and explains why, dismissibly", async ({
    page,
  }) => {
    await page.goto("/map?geo=rochester");
    await expect(page.locator(".leaflet-container")).toBeVisible({
      timeout: 15_000,
    });
    const notice = page.getByRole("status").filter({
      hasText: "Showing the area near",
    });
    await expect(notice).toContainText("Rochester, NY");
    await expect(notice).toContainText("approximate");
    await expect(
      notice.getByRole("button", { name: "Use precise location" }),
    ).toBeVisible();
    await notice.getByRole("button", { name: "Dismiss location notice" }).click();
    await expect(notice).toHaveCount(0);
  });

  test("an explicit camera in the URL wins and shows no notice", async ({
    page,
  }) => {
    await page.goto("/map?geo=rochester&lat=42.9&lng=-78.87&z=12");
    await expect(page.locator(".leaflet-container")).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByText("Showing the area near")).toHaveCount(0);
  });

  test("outside coverage keeps the default view with no notice", async ({
    page,
  }) => {
    await page.goto("/map?geo=columbus");
    await expect(page.locator(".leaflet-container")).toBeVisible({
      timeout: 15_000,
    });
    await expect(page.getByText("Showing the area near")).toHaveCount(0);
  });
});
