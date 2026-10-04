import { test, expect } from "@playwright/test";

test("diocese index lists dioceses and links to a diocese page", async ({ page }) => {
  const response = await page.goto("/dioceses/");
  expect(response?.status()).toBe(200);
  await expect(page.getByRole("heading", { level: 1, name: "Dioceses" })).toBeVisible();
  await expect(page).toHaveTitle(/Dioceses/);
  await page.getByRole("link", { name: /Diocese of Rochester/ }).first().click();
  await expect(page).toHaveURL(/\/dioceses\/rochester\/$/);
  await expect(
    page.getByRole("heading", { level: 1, name: "Diocese of Rochester" }),
  ).toBeVisible();
});

test("state hub lists cities and an A-Z of every town", async ({ page }) => {
  await page.goto("/mass-times/ny/");
  await expect(
    page.getByRole("heading", { level: 1, name: /Mass Times in New York/ }),
  ).toBeVisible();
  await expect(
    page.getByRole("region", { name: "Cities" }).getByRole("link", { name: "Buffalo", exact: true }),
  ).toHaveAttribute(
    "href",
    "/mass-times/ny/buffalo/",
  );
  await expect(page.locator("#towns")).toBeVisible();
});

test("city page has the data sections, JSON-LD and a nearby list", async ({ page }) => {
  await page.goto("/mass-times/ny/buffalo/");
  await expect(page).toHaveTitle(
    /Mass & Confession Times in Buffalo, NY · \d+ Catholic Churches \| Project Carlo/,
  );
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Buffalo");
  for (const id of ["mass", "confession", "adoration", "churches", "nearby"]) {
    await expect(page.locator(`#${id}`)).toBeVisible();
  }
  await expect(page.getByText("Earliest Sunday Mass")).toBeVisible();

  const canonical = await page.locator('link[rel="canonical"]').getAttribute("href");
  expect(canonical).toBe("https://projectcarlo.com/mass-times/ny/buffalo/");
  const ld = JSON.parse(
    (await page.locator('script[type="application/ld+json"]').first().textContent()) ?? "[]",
  ) as { "@type": string }[];
  expect(ld.map((n) => n["@type"])).toEqual([
    "CollectionPage",
    "ItemList",
    "BreadcrumbList",
  ]);
});

test("church page shows breadcrumbs, diocese, map link and nearby churches", async ({ page }) => {
  await page.goto("/churches/st-joseph-cathedral-buffalo/");
  const crumbs = page.getByRole("navigation", { name: "Breadcrumb" });
  await expect(crumbs.getByRole("link", { name: "New York" })).toHaveAttribute(
    "href",
    "/mass-times/ny/",
  );
  await expect(crumbs.getByRole("link", { name: "Buffalo" })).toHaveAttribute(
    "href",
    "/mass-times/ny/buffalo/",
  );
  await expect(page.getByRole("link", { name: "Diocese of Buffalo" }).first()).toHaveAttribute(
    "href",
    "/dioceses/buffalo/",
  );
  await expect(page.getByRole("link", { name: "View on map" })).toHaveAttribute(
    "href",
    /^\/map\?lat=[\d.-]+&lng=[\d.-]+&z=15$/,
  );
  const nearby = page.getByRole("region", { name: "Nearby churches" });
  await expect(nearby.getByRole("listitem")).toHaveCount(5);
  await expect(nearby.getByText(/\d\.\d mi/).first()).toBeVisible();
});

test("client navigation: Dioceses link on the home page renders the SPA route", async ({ page }) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await page
    .getByRole("navigation", { name: "Site" })
    .getByRole("link", { name: "Dioceses" })
    .click();
  await expect(page).toHaveURL(/\/dioceses\/$/);
  await expect(page.getByRole("heading", { level: 1, name: "Dioceses" })).toBeVisible();
  await expect(page).toHaveTitle(/Catholic Dioceses in New York State/);

  await page.getByRole("link", { name: /Diocese of Buffalo/ }).first().click();
  await expect(page).toHaveURL(/\/dioceses\/buffalo\/$/);
  await page.getByRole("link", { name: "Buffalo", exact: true }).first().click();
  await expect(page).toHaveURL(/\/mass-times\/ny\/buffalo\/$/);
  await expect(page.locator("#mass")).toBeVisible();
  expect(errors, errors.join("\n")).toEqual([]);
});

test("unknown city and diocese are not found", async ({ page }) => {
  await page.goto("/mass-times/ny/not-a-town/");
  await expect(page.getByRole("heading", { name: "Page not found" })).toBeVisible();
  await page.goto("/dioceses/atlantis/");
  await expect(page.getByRole("heading", { name: "Page not found" })).toBeVisible();
});
