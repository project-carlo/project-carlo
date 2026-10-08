import { test, expect, type Page } from "@playwright/test";

/** A church downtown, with its neighbours' pins around it. */
const ST_ANTHONY = "/churches/st-anthony-of-padua-buffalo/";

const MARKERS = ".church-map-marker, .church-map-cluster";

/** Each marker's box in the map, and whether it's the page's church. */
async function markerBoxes(page: Page, selector: string): Promise<string[]> {
  return page.locator(".city-map").evaluate((map, sel) => {
    const frame = map.getBoundingClientRect();
    return [...map.querySelectorAll(sel)]
      .map((el) => ({ el, r: el.getBoundingClientRect() }))
      .filter(({ r }) => r.right > frame.left && r.left < frame.right && r.bottom > frame.top && r.top < frame.bottom)
      .map(
        ({ el, r }) =>
          `${Math.round(r.left - frame.left)},${Math.round(r.top - frame.top)},${Math.round(r.width)}` +
          (el.classList.contains("is-current") ? ",current" : ""),
      )
      .sort();
  }, selector);
}

test("a church page's map marks its church, takes over the preview in place, and opens", async ({
  browser,
  page,
}) => {
  const still = await browser.newPage({ javaScriptEnabled: false });
  await still.goto(ST_ANTHONY);
  const stillBoxes = await markerBoxes(still, MARKERS);
  await still.close();
  expect(stillBoxes.filter((box) => box.endsWith(",current"))).toHaveLength(1);
  expect(stillBoxes.length).toBeGreaterThan(1);

  await page.goto(ST_ANTHONY);
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  await expect(page.locator(".city-map-static-pins")).toBeHidden();
  expect(await markerBoxes(page, `.leaflet-container :is(${MARKERS})`)).toEqual(
    stillBoxes,
  );

  await page.getByRole("button", { name: "Expand map" }).click();
  await expect(page).toHaveURL(/#map$/);
  const dialog = page.getByRole("dialog", {
    name: "Map of churches around St. Anthony of Padua Church",
  });
  await expect(dialog).toBeVisible();
  await expect(dialog.locator(".church-map-marker.is-current")).toHaveCount(1);
  await page.goBack();
  await expect(dialog).toHaveCount(0);
  await expect(page).toHaveURL(new RegExp(`${ST_ANTHONY}$`));
});

test("the page's church stays on its map when the filters leave it out", async ({
  page,
}) => {
  await page.goto(ST_ANTHONY);
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  await page.getByRole("button", { name: "Expand map" }).click();
  const dialog = page.getByRole("dialog");
  await dialog.getByRole("button", { name: "Adoration" }).click();
  await expect(dialog.locator(".church-map-marker.is-current")).toHaveCount(1);
});

test("the page's church pin opens only its name in the page, and the full card open", async ({
  page,
}) => {
  await page.goto(ST_ANTHONY);
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  const map = page.locator(".city-map");
  await map.locator(".leaflet-container .church-map-marker.is-current").click();
  const popup = map.locator(".leaflet-popup");
  await expect(popup.locator(".map-popup-compact")).toBeVisible();
  await expect(popup.getByRole("link")).toHaveAttribute(
    "href",
    new RegExp(`${ST_ANTHONY}$`),
  );
  await expect(popup.getByText("Full schedule")).toHaveCount(0);

  await page.getByRole("button", { name: "Expand map" }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog.getByText("Full schedule")).toBeVisible();
  await expect(dialog.locator(".church-map-marker.is-current")).toHaveClass(
    /is-selected/,
  );
});

test("a church page's still tiles go once the live map moves", async ({
  page,
}) => {
  await page.goto(ST_ANTHONY);
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  await expect(page.locator(".city-map-tiles")).toBeVisible();
  await page.locator(".city-map").getByRole("button", { name: "Zoom out" }).click();
  await expect(page.locator(".city-map-live[data-moved]")).toHaveCount(1);
  await expect(page.locator(".city-map-tiles")).toBeHidden();
});
