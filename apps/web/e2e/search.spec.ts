import { test, expect, type Page } from "@playwright/test";

const GEOAPIFY = "https://api.geoapify.com/v1/geocode/autocomplete**";

/** Answers place searches with `results`, and records each request's URL. */
async function mockPlaceSearch(page: Page, results: object[]): Promise<URL[]> {
  const requests: URL[] = [];
  await page.route(GEOAPIFY, (route) => {
    requests.push(new URL(route.request().url()));
    return route.fulfill({ json: { results } });
  });
  return requests;
}

function mockIpLocation(page: Page) {
  return page.route("**/api/approximate-location", (route) =>
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
}

async function openMap(page: Page) {
  await page.goto("/?lat=42.7&lng=-73.8&z=10");
  const input = page.getByRole("combobox");
  await expect(input).toBeVisible({ timeout: 15_000 });
  return input;
}

const option = (page: Page, name: RegExp) => page.getByRole("option", { name });

test("a city Carlo serves is offered first and can be picked", async ({
  page,
}) => {
  await mockPlaceSearch(page, [
    {
      address_line1: "Rochester, MN",
      address_line2: "United States of America",
      name: "Rochester",
      state_code: "MN",
      result_type: "city",
      lat: 44.02,
      lon: -92.47,
    },
  ]);
  const input = await openMap(page);
  await input.pressSequentially("Rochester");

  const results = page.getByRole("option");
  await expect(results.first()).toContainText("Rochester, NY");
  await expect(results.first()).toContainText(/\d+ church/);
  await expect(option(page, /Rochester, MN/)).toBeVisible();

  await results.first().click();
  await expect(page.getByText("Pinned:")).toContainText("Rochester, NY");
});

test("a misspelled city still finds the city", async ({ page }) => {
  await mockPlaceSearch(page, []);
  const input = await openMap(page);
  await input.pressSequentially("Rochestor");
  await expect(page.getByRole("option").first()).toContainText("Rochester, NY");
});

test("results rank around the map, ahead of the IP location", async ({
  page,
}) => {
  await mockIpLocation(page);
  const requests = await mockPlaceSearch(page, []);
  const input = await openMap(page);
  await input.pressSequentially("Oakland");

  await expect
    .poll(() => requests.at(-1)?.searchParams.get("bias"))
    .toBe("proximity:-73.8,42.7");
});

test("the landing page ranks around the IP location", async ({ page }) => {
  await mockIpLocation(page);
  const requests = await mockPlaceSearch(page, []);
  await page.goto("/landing");
  const input = page.getByRole("combobox");
  await expect(input).toBeVisible({ timeout: 15_000 });
  await input.pressSequentially("Oakland");

  await expect
    .poll(() => requests.at(-1)?.searchParams.get("bias"))
    .toBe("proximity:-78.9,42.9");
});

test("a church can be found by name and opened", async ({ page }) => {
  await mockPlaceSearch(page, []);
  const input = await openMap(page);
  await input.pressSequentially("Sacred Heart Rochester");

  const church = option(page, /Sacred Heart Cathedral/);
  await expect(church).toBeVisible();
  await church.click();
  await expect(input).toHaveValue("");
  await expect(page.getByRole("option")).toHaveCount(0);
});

test("a named building the provider finds is listed", async ({ page }) => {
  await mockPlaceSearch(page, [
    {
      address_line1: "Strong Memorial Hospital",
      address_line2: "601 Elmwood Avenue, Rochester, NY 14642",
      state_code: "NY",
      result_type: "amenity",
      lat: 43.12,
      lon: -77.62,
    },
  ]);
  const input = await openMap(page);
  await input.pressSequentially("Strong Memorial Hospital");
  await expect(option(page, /Strong Memorial Hospital/)).toBeVisible();
});

test("served cities still answer when place search fails", async ({ page }) => {
  await page.route(GEOAPIFY, (route) => route.fulfill({ status: 500 }));
  const input = await openMap(page);

  await input.pressSequentially("Rochester");
  await expect(page.getByRole("option").first()).toContainText("Rochester, NY");
  await expect(page.getByText("Couldn’t search places")).toHaveCount(0);

  await input.fill("zzqqxx");
  await expect(page.getByText("Couldn’t search places")).toBeVisible();
});

test("says nothing matches only once the search has answered", async ({
  page,
}) => {
  await page.route(GEOAPIFY, async (route) => {
    const text = new URL(route.request().url()).searchParams.get("text");
    if (text === "zzqq") return route.fulfill({ json: { results: [] } });
    await new Promise((done) => setTimeout(done, 800));
    await route.fulfill({ json: { results: [] } });
  });
  const input = await openMap(page);
  await input.pressSequentially("zzqq");
  await expect(page.getByText("Nothing matches “zzqq”")).toBeVisible();

  await input.pressSequentially("x");
  await expect(page.getByText("Searching places…")).toBeVisible();
  await expect(page.getByText("Nothing matches “zzqqx”")).toBeVisible();
});

test("typing on keeps the list up while more results load", async ({ page }) => {
  await page.route(GEOAPIFY, async (route) => {
    const text = new URL(route.request().url()).searchParams.get("text");
    if (text !== "Main") await new Promise((done) => setTimeout(done, 800));
    await route.fulfill({
      json: {
        results: [
          {
            address_line1: "Main Street",
            address_line2: "Rochester, NY",
            state_code: "NY",
            result_type: "street",
            lat: 43.15,
            lon: -77.6,
          },
        ],
      },
    });
  });
  const input = await openMap(page);
  await input.pressSequentially("Main");
  const street = option(page, /Main Street/);
  await expect(street).toBeVisible();

  await input.pressSequentially(" St");
  await page.waitForTimeout(450);
  await expect(street).toBeVisible();
  await expect(page.getByText("Searching places…")).toHaveCount(0);
});
