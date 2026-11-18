import { test, expect, type Page } from "@playwright/test";

const GEOAPIFY = "https://api.geoapify.com/v1/geocode/autocomplete**";

/** Place searches find nothing, so only the site's own churches are offered. */
function mockNoPlaces(page: Page) {
  return page.route(GEOAPIFY, (route) => route.fulfill({ json: { results: [] } }));
}

/** The embed for the Diocese of Syracuse, as a diocese's snippet loads it. */
const SYRACUSE_EMBED = "/embed?diocese=syracuse&ref=diocese-syracuse";

async function openEmbed(page: Page, url = SYRACUSE_EMBED) {
  const response = await page.goto(url);
  expect(response?.status()).toBe(200);
  await expect(page.locator(".leaflet-container")).toBeVisible({ timeout: 15_000 });
  await expect(page.locator(".church-map-marker, .church-map-cluster").first()).toBeVisible({
    timeout: 15_000,
  });
}

test("the embed shows the map without the site's masthead, crediting the full site", async ({
  page,
}) => {
  await openEmbed(page);

  await expect(page.getByRole("link", { name: "Project Carlo — home" })).toHaveCount(0);
  await expect(page.getByRole("link", { name: "Church list" })).toHaveCount(0);
  const credit = page.getByRole("link", { name: /Powered by Project Carlo/ });
  await expect(credit).toHaveAttribute("target", "_blank");
  // The full site at the same campaign, without the embed's diocese.
  await expect(credit).toHaveAttribute("href", /^\/\?(.*&)?ref=diocese-syracuse/);
  await expect(credit).not.toHaveAttribute("href", /diocese=/);
  // Not a page for search engines: it repeats the homepage.
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute("content", "noindex");
});

test("the embed opens on its diocese's churches", async ({ page }) => {
  await openEmbed(page);

  // Framed on the diocese of Syracuse, not the IP estimate or every church.
  // The view reaches the URL once the map moves; zooming keeps its centre.
  await page.getByRole("button", { name: "Zoom in" }).click();
  await expect
    .poll(() => new URL(page.url()).searchParams.get("lat"), { timeout: 5_000 })
    .not.toBeNull();
  const params = new URL(page.url()).searchParams;
  expect(Number(params.get("lat"))).toBeGreaterThan(42);
  expect(Number(params.get("lat"))).toBeLessThan(44.5);
  expect(Number(params.get("lng"))).toBeGreaterThan(-77.5);
  expect(Number(params.get("lng"))).toBeLessThan(-75);
  expect(params.get("diocese")).toBe("syracuse");
});

test("the embed's search offers only its diocese's churches", async ({ page }) => {
  await mockNoPlaces(page);
  await openEmbed(page);
  const input = page.getByRole("combobox");

  await input.pressSequentially("St. Joseph Cathedral");
  await expect(page.getByRole("option", { name: /St\. Joseph Cathedral/ })).toHaveCount(0);

  await input.fill("");
  await input.pressSequentially("Cathedral of the Immaculate");
  await expect(
    page.getByRole("option", { name: /Cathedral of the Immaculate Conception/ }),
  ).toHaveCount(1);
});

test("the embed opens church pages in a new tab and adds nothing to the host's history", async ({
  page,
}) => {
  await mockNoPlaces(page);
  await openEmbed(page);
  const historyLength = await page.evaluate(() => history.length);

  const input = page.getByRole("combobox");
  await input.pressSequentially("Cathedral of the Immaculate");
  await page.getByRole("option", { name: /Cathedral of the Immaculate Conception/ }).click();
  const link = page.locator(".leaflet-popup").getByRole("link", { name: /Full schedule/ });

  // In a new tab, credited to the embed's campaign.
  const [tab] = await Promise.all([page.context().waitForEvent("page"), link.click()]);
  await expect(tab).toHaveURL(
    /\/churches\/cathedral-immaculate-conception-syracuse\/\?ref=diocese-syracuse$/,
  );
  await tab.close();

  // The map's attribution too, though Leaflet writes its links itself.
  await page.context().route("https://www.openstreetmap.org/**", (route) =>
    route.fulfill({ body: "" }),
  );
  const [osm] = await Promise.all([
    page.context().waitForEvent("page"),
    page.locator(".leaflet-control-attribution").getByRole("link", { name: "OpenStreetMap" }).click(),
  ]);
  await expect(osm).toHaveURL("https://www.openstreetmap.org/copyright");
  await osm.close();

  // Still the embed, with the map's moves kept in its own entry.
  await expect(page).toHaveURL(/\/embed\?/);
  expect(await page.evaluate(() => history.length)).toBe(historyLength);

  // The popup's close button is a link to "#close", and only closes it.
  await page.locator(".leaflet-popup-close-button").click();
  await expect(page.locator(".leaflet-popup")).toHaveCount(0);
  expect(page.context().pages()).toHaveLength(1);
});

test("an embed with a view in its URL still says a diocese isn't covered, with no map first", async ({
  page,
}) => {
  await page.goto("/embed?diocese=not-a-diocese&lat=43&lng=-76&z=10");

  await expect(page.getByRole("heading", { name: "This diocese isn’t supported yet" })).toBeVisible({
    timeout: 15_000,
  });
  await expect(page.locator(".leaflet-container")).toHaveCount(0);
});

test("the embed leaves nothing for the full site's map links to restore", async ({ page }) => {
  await openEmbed(page);
  await page.getByRole("button", { name: "Zoom in" }).click();
  await expect
    .poll(() => new URL(page.url()).searchParams.get("lat"), { timeout: 5_000 })
    .not.toBeNull();

  expect(await page.evaluate(() => sessionStorage.getItem("carlo:home-search"))).toBeNull();
});

test("an embed for a diocese the site doesn't cover says so", async ({ page }) => {
  const response = await page.goto("/embed?diocese=not-a-diocese");
  expect(response?.status()).toBe(200);

  await expect(page.getByRole("heading", { name: "This diocese isn’t supported yet" })).toBeVisible({
    timeout: 15_000,
  });
  await expect(page.getByText("“not-a-diocese”")).toBeVisible();
  await expect(page.locator(".leaflet-container")).toHaveCount(0);
});

test("an embed without a diocese shows every church", async ({ page }) => {
  await openEmbed(page, "/embed");
  await expect(page.getByRole("link", { name: /Powered by Project Carlo/ })).toBeVisible();
});

test("the embed's map leaves the wheel to the host page until it's clicked", async ({ page }) => {
  await openEmbed(page);
  const box = (await page.locator(".leaflet-container").boundingBox())!;
  const view = () => new URL(page.url()).searchParams.get("z");

  await page.mouse.move(box.x + box.width * 0.75, box.y + box.height * 0.75);
  await page.mouse.wheel(0, -600);
  await page.waitForTimeout(1_000);
  expect(view()).toBeNull();

  await page.mouse.down();
  await page.mouse.up();
  await page.waitForTimeout(1_000);
  const before = view();
  await page.mouse.wheel(0, -600);
  await expect.poll(view, { timeout: 5_000 }).not.toBe(before);
});
