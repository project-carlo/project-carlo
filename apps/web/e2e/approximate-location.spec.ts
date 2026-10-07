import { test, expect, type Page } from "@playwright/test";

/** The zoom levels of the map tiles on screen, from their URLs. */
async function tileZooms(page: Page): Promise<number[]> {
  const srcs = await page
    .locator(".leaflet-tile")
    .evaluateAll((tiles) => tiles.map((tile) => tile.getAttribute("src")));
  return [
    ...new Set(
      srcs.map((src) => Number(/tile\.openstreetmap\.org\/(\d+)\//.exec(src ?? "")?.[1])),
    ),
  ];
}

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
  await expect(page.getByText("· approximate")).toBeVisible();
  // Offered twice: as text beside the estimate, and as the map's corner
  // control (an icon, named by its label and tooltip).
  await expect(
    page.getByRole("button", { name: "Use my location" }),
  ).toHaveCount(2);
  await expect(
    page.getByRole("button").getByText("Use my location", { exact: true }),
  ).toBeVisible();
  await expect(page.getByTitle("Use my location")).toBeVisible();
  // Zoomed out to a region (desktop viewport).
  await expect(
    page.locator('.leaflet-tile[src*="tile.openstreetmap.org/9/"]').first(),
  ).toBeAttached();
  expect(await tileZooms(page)).toEqual([9]);
  // A start chosen for the visitor isn't written into the URL: a link they
  // copy shouldn't carry where their IP address puts them.
  await page.waitForTimeout(1000);
  expect(new URL(page.url()).searchParams.has("lat")).toBe(false);
});

test("a phone shows the area without the approximate note", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.route("**/api/approximate-location", (route) =>
    route.fulfill({
      json: { lat: 42.8864, lng: -78.8784, city: "Buffalo", regionCode: "NY" },
    }),
  );
  await page.goto("/");
  await expect(page.getByText("Near Buffalo, NY")).toBeVisible({
    timeout: 15_000,
  });
  await expect(page.getByText("· approximate")).toBeHidden();
  await expect(
    page.getByRole("button").getByText("Use my location", { exact: true }),
  ).toBeVisible();
});

test("a filtered link still starts near the estimate", async ({ page }) => {
  await page.route("**/api/approximate-location", (route) =>
    route.fulfill({
      json: { lat: 42.8864, lng: -78.8784, city: "Buffalo", regionCode: "NY" },
    }),
  );
  // Filters no church nearby (likely none anywhere) matches: the start
  // goes by every church, not the ones the filters leave.
  await page.goto("/?type=confession&days=mon&from=0300&to=0330");
  await expect(page.getByText("Near Buffalo, NY")).toBeVisible({
    timeout: 15_000,
  });
});

for (const [name, json] of [
  [
    "an estimate far from every church",
    { lat: 39.1, lng: -94.58, city: "Kansas City", regionCode: "MO" },
  ],
  ["no estimate", {}],
] as const) {
  test(`${name} shows the whole covered area`, async ({ page }) => {
    await page.route("**/api/approximate-location", (route) =>
      route.fulfill({ json }),
    );
    await page.goto("/");
    await expect(page.locator(".leaflet-tile").first()).toBeAttached({
      timeout: 15_000,
    });
    await expect(page.getByText("approximate")).toHaveCount(0);
    // Further out than a start near the visitor (zoom 9).
    const zooms = await tileZooms(page);
    expect(zooms).toHaveLength(1);
    expect(zooms[0]).toBeLessThan(9);
  });
}

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
  await page
    .getByRole("button")
    .getByText("Use my location", { exact: true })
    .click();
  await expect(page.getByText("Pinned:")).toContainText("Your location");
  await expect(page.getByText("Near Buffalo, NY")).toHaveCount(0);
  // The pin's popup stays closed until the pin is clicked.
  const pin = page.locator(".searched-place-marker");
  await expect(pin).toBeVisible();
  await expect(page.locator(".leaflet-popup")).toHaveCount(0);
  await pin.click();
  await expect(page.locator(".leaflet-popup")).toContainText("Your location");
});
