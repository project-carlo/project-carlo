import { test, expect } from "@playwright/test";

test("the Worker answers the approximate-location lookup", async ({
  request,
}) => {
  const response = await request.get("/api/approximate-location");
  expect(response.status()).toBe(200);
  expect(response.headers()["content-type"]).toContain("application/json");
  expect(response.headers()["cache-control"]).toContain("no-store");
  const body = await response.json();
  // Locally there may be no geolocation at all; the shape is what's fixed.
  for (const key of ["lat", "lng", "city", "region", "regionCode", "country"]) {
    expect(body).toHaveProperty(key);
  }
});

test("a first visit starts near the IP estimate, zoomed out", async ({
  page,
}) => {
  await page.route("**/api/approximate-location", (route) =>
    route.fulfill({
      json: {
        lat: 42.8864,
        lng: -78.8784,
        city: "Buffalo",
        region: "New York",
        regionCode: "NY",
        country: "US",
      },
    }),
  );
  await page.goto("/");
  await expect(page.getByText("Near Buffalo, NY")).toBeVisible({
    timeout: 15_000,
  });
  await expect(
    page.getByRole("button", { name: "Use exact location" }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Go to my exact location" }),
  ).toBeVisible();
  // Zoomed out to a region (desktop viewport): the tiles are zoom 9's.
  await expect(
    page.locator('.leaflet-tile[src*="tile.openstreetmap.org/9/"]').first(),
  ).toBeAttached();
});

test("an estimate far from every church keeps the default view", async ({
  page,
}) => {
  await page.route("**/api/approximate-location", (route) =>
    route.fulfill({
      json: { lat: 39.1, lng: -94.58, city: "Kansas City", regionCode: "MO" },
    }),
  );
  await page.goto("/");
  await expect(page.locator(".leaflet-container")).toBeVisible({
    timeout: 15_000,
  });
  await expect(page.getByText("Kansas City")).toHaveCount(0);
});

test("a view in the URL wins over the IP estimate", async ({ page }) => {
  let looked = false;
  await page.route("**/api/approximate-location", (route) => {
    looked = true;
    return route.fulfill({ json: {} });
  });
  await page.goto("/?lat=43.1566&lng=-77.6088&z=13");
  await expect(page.locator(".leaflet-container")).toBeVisible({
    timeout: 15_000,
  });
  expect(looked).toBe(false);
});

test("exact location pins the browser's position", async ({
  page,
  context,
}) => {
  await context.grantPermissions(["geolocation"]);
  await context.setGeolocation({ latitude: 43.1566, longitude: -77.6088 });
  await page.route("**/api/approximate-location", (route) =>
    route.fulfill({
      json: { lat: 42.8864, lng: -78.8784, city: "Buffalo", regionCode: "NY" },
    }),
  );
  await page.goto("/");
  await page.getByRole("button", { name: "Use exact location" }).click();
  await expect(page.getByText("Pinned:")).toContainText(
    "Your current location",
  );
  await expect(page.getByText("Near Buffalo, NY")).toHaveCount(0);
});
