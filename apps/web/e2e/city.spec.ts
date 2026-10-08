import { test, expect, type Browser, type Page } from "@playwright/test";

test("the church index links each city to its prerendered city page", async ({
  page,
}) => {
  await page.goto("/churches/");
  const cityLink = page.locator('h2 a[href^="/mass-times/"]').first();
  const label = (await cityLink.textContent())!.trim();
  await cityLink.click();

  await expect(page).toHaveURL(/\/mass-times\/[a-z0-9-]+\/$/);
  await expect(
    page.getByRole("heading", { level: 1, name: `Mass Times in ${label}` }),
  ).toBeVisible();
  await expect(
    page.getByRole("navigation", { name: "Breadcrumb" }),
  ).toContainText(label);
});

test("a church page's breadcrumb leads back to its city page", async ({
  page,
}) => {
  await page.goto("/churches/");
  const cityLink = page.locator('h2 a[href^="/mass-times/"]').first();
  const cityHref = (await cityLink.getAttribute("href"))!;
  await cityLink.click();

  await page.getByRole("link", { name: "Full schedule" }).first().click();
  await expect(page).toHaveURL(/\/churches\/[^/]+\/$/);

  const breadcrumb = page.getByRole("navigation", { name: "Breadcrumb" });
  await breadcrumb.locator(`a[href="${cityHref}"]`).click();
  await expect(page).toHaveURL(cityHref);
});

test("a city with no churches renders the not-found page", async ({ page }) => {
  const response = await page.goto("/mass-times/no-such-town-zz/");
  expect(response?.status()).toBe(404);
  await expect(
    page.getByRole("heading", { name: "City not found" }),
  ).toBeVisible({ timeout: 15_000 });
});

const EAST_AURORA = "/mass-times/east-aurora-ny/";

test("a city page's map is live in the page, and opens to the full map view", async ({
  page,
}) => {
  await page.goto(EAST_AURORA);
  const map = page.locator(".city-map");
  await expect(map.locator(".leaflet-container")).toBeVisible({ timeout: 15_000 });
  await expect(
    map.locator(".leaflet-container .church-map-marker").first(),
  ).toBeVisible();
  await expect(map.getByRole("button", { name: "Zoom in" })).toBeVisible();
  // The no-JavaScript link to the home map is gone, for the keyboard too.
  await expect(
    page.getByRole("link", { name: /^Open the map of churches around / }),
  ).toHaveCount(0);

  await page.getByRole("button", { name: "Expand map" }).click();
  await expect(page).toHaveURL(/#map$/);
  const dialog = page.getByRole("dialog", { name: /^Map of churches around / });
  await expect(dialog).toBeVisible();
  await expect(page.getByRole("button", { name: "Close map" })).toBeFocused();
  // The home map's view: search, filters, zoom and locate.
  await expect(dialog.getByPlaceholder(/Search for a city/)).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Confession" })).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Zoom in" })).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Use my location", exact: true })).toBeVisible();
  // The search's suggestions open over the map, not under it.
  await dialog.getByPlaceholder(/Search for a city/).fill("Buffalo");
  await page
    .locator("[data-slot=popover-content]")
    .click({ trial: true, timeout: 5_000 });

  // Back closes it, leaving the city page as it was.
  await page.goBack();
  await expect(page).toHaveURL(new RegExp(`${EAST_AURORA}$`));
  await expect(dialog).toHaveCount(0);
  await expect(map.locator(".leaflet-container")).toBeVisible();

  await page.getByRole("button", { name: "Expand map" }).click();
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  await expect(page.getByRole("button", { name: "Expand map" })).toBeFocused();
});

test("the open map keeps focus in itself, and Escape closes a popup before the map", async ({
  page,
}) => {
  await page.goto(EAST_AURORA);
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  await page.getByRole("button", { name: "Expand map" }).click();
  const dialog = page.getByRole("dialog", { name: /^Map of churches around / });
  await expect(dialog).toBeVisible();

  // Tab never reaches the page behind the map.
  for (let i = 0; i < 40; i++) {
    await page.keyboard.press("Tab");
    const outside = await page.evaluate(() => {
      const el = document.activeElement;
      return el != null && el !== document.body && el.closest("main") != null;
    });
    expect(outside, `focus left the map after ${i + 1} Tabs`).toBe(false);
  }

  await dialog.locator(".church-map-marker").first().click();
  await expect(dialog.locator(".leaflet-popup")).toBeVisible();
  // With focus on a control, not the map, as Leaflet's own Escape needs.
  await page.getByRole("button", { name: "Close map", exact: true }).focus();
  await page.keyboard.press("Escape");
  await expect(dialog.locator(".leaflet-popup")).toHaveCount(0);
  await expect(dialog).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(dialog).toHaveCount(0);
  // The page behind is back in play.
  await expect(page.locator("main")).not.toHaveAttribute("inert");
});

/** Drags the page's map a little way, so its pins are off the middle. */
async function nudgeCityMap(page: Page, dx: number, dy: number) {
  const box = (await page.locator(".city-map").boundingBox())!;
  const [x, y] = [box.x + box.width / 2, box.y + box.height / 2];
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x + dx, y + dy, { steps: 5 });
  await page.mouse.up();
}

/**
 * Expands the page's map, its pin's popup open, and checks the pin comes to
 * the middle of the map below the buttons along its top, its card clear of
 * them.
 */
async function expectExpandedPinCentered(page: Page) {
  await page.getByRole("button", { name: "Expand map" }).click();
  const dialog = page.getByRole("dialog", { name: /^Map of churches around / });
  await expect(dialog.getByText("Full schedule")).toBeVisible();
  const buttons = dialog.locator("[data-map-overlay]");
  await expect(buttons).toBeVisible();
  const top = await buttons.evaluate((el) => el.getBoundingClientRect().bottom);
  // How far the point the pin stands on is from there, across and down.
  await expect
    .poll(async () => {
      const pin = (await dialog.locator(".church-map-marker.is-selected").boundingBox())!;
      return [
        Math.round(Math.abs(pin.x + 17 - 390 / 2) / 4),
        Math.round(Math.abs(pin.y + 40 - (top + 844) / 2) / 4),
      ];
    })
    .toEqual([0, 0]);
  expect((await dialog.locator(".leaflet-popup").boundingBox())!.y).toBeGreaterThan(top);
  return dialog;
}

test("a pin's popup in the page is only the church's name, and the full card in the middle once the map is open", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(EAST_AURORA);
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  const map = page.locator(".city-map");
  await nudgeCityMap(page, 100, 40);
  await map.locator(".leaflet-container .church-map-marker").first().click();
  const popup = map.locator(".leaflet-popup");
  await expect(popup.locator(".map-popup-compact")).toBeVisible();
  await expect(popup.getByRole("link")).toHaveAttribute("href", /^\/churches\//);
  await expect(popup.getByText("Full schedule")).toHaveCount(0);
  await expect(popup.locator(".leaflet-popup-close-button")).toBeHidden();
  const compactWidth = (await popup.boundingBox())!.width;
  expect(compactWidth).toBeLessThanOrEqual(250);

  // Opening the map keeps the popup, now the full card, with its pin in the
  // middle.
  const dialog = await expectExpandedPinCentered(page);
  expect((await dialog.locator(".leaflet-popup").boundingBox())!.width).toBeGreaterThan(
    compactWidth,
  );

  // And again, once the open map's controls are already loaded (they then
  // mount as the map resizes, not after). Closing the map leaves the popup
  // open, back to the name.
  await dialog.getByRole("button", { name: "Close", exact: true }).click();
  await expect(dialog).toHaveCount(0);
  await expect(popup.locator(".map-popup-compact")).toBeVisible();
  await nudgeCityMap(page, -60, -30);
  await expectExpandedPinCentered(page);
});

/** Each marker's box in the map, from left to right. */
async function markerBoxes(page: Page, selector: string): Promise<string[]> {
  return page.locator(".city-map").evaluate((map, sel) => {
    const frame = map.getBoundingClientRect();
    return [...map.querySelectorAll(sel)]
      .map((el) => el.getBoundingClientRect())
      .filter((r) => r.right > frame.left && r.left < frame.right && r.bottom > frame.top && r.top < frame.bottom)
      .map((r) => `${Math.round(r.left - frame.left)},${Math.round(r.top - frame.top)},${Math.round(r.width)}`)
      .sort();
  }, selector);
}

const MARKERS = ".church-map-marker, .church-map-cluster";

/** The markers the still preview draws for a city, with JavaScript off. */
async function stillMarkerBoxes(browser: Browser, path: string): Promise<string[]> {
  const still = await browser.newPage({ javaScriptEnabled: false });
  await still.goto(path);
  const boxes = await markerBoxes(still, MARKERS);
  await still.close();
  expect(boxes.length).toBeGreaterThan(0);
  return boxes;
}

test("the live map takes over the preview with its markers where they were", async ({
  browser,
  page,
}) => {
  const stillBoxes = await stillMarkerBoxes(browser, "/mass-times/buffalo-ny/");

  await page.goto("/mass-times/buffalo-ny/");
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  await expect(page.locator(".city-map-static-pins")).toBeHidden();
  expect(await markerBoxes(page, `.leaflet-container :is(${MARKERS})`)).toEqual(
    stillBoxes,
  );
});

test("the markers a pan drags into the page's map are there before it stops", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/mass-times/rochester-ny/");
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  const live = `.leaflet-container :is(${MARKERS})`;
  const before = await markerBoxes(page, live);

  // Further than the markers drawn around the small map reach (half its size
  // past each edge), and held there. Up and left, to bring in the towns
  // south-east of the city rather than the lake.
  const box = (await page.locator(".city-map").boundingBox())!;
  const [x, y] = [box.x + box.width / 2, box.y + box.height / 2];
  await page.mouse.move(x, y);
  await page.mouse.down();
  await page.mouse.move(x - box.width, y - box.height, { steps: 30 });
  // Held still past Leaflet's inertia window, so letting go doesn't fling it.
  await page.waitForTimeout(200);
  const dragging = await markerBoxes(page, live);
  await page.mouse.up();
  await page.waitForTimeout(300);

  expect(dragging).not.toEqual(before);
  expect(dragging.length).toBeGreaterThan(0);
  expect(await markerBoxes(page, live)).toEqual(dragging);
});

test("the still tiles go once the live map moves off their view", async ({
  page,
}) => {
  await page.goto("/mass-times/buffalo-ny/");
  await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
    timeout: 15_000,
  });
  // Under the live map until it moves: they show through while its tiles load.
  await expect(page.locator(".city-map-tiles")).toBeVisible();

  // Zoomed out, they'd show through around the live map's shrinking tiles.
  await page.locator(".city-map").getByRole("button", { name: "Zoom out" }).click();
  await expect(page.locator(".city-map-live[data-moved]")).toHaveCount(1);
  await expect(page.locator(".city-map-tiles")).toBeHidden();
});

test("in the app, each city page's live map is that city's", async ({
  browser,
  page,
}) => {
  const buffalo = "/mass-times/buffalo-ny/";
  const buffaloBoxes = await stillMarkerBoxes(browser, buffalo);

  /** Navigates in the app, as one of its links would. */
  const routeTo = (path: string) =>
    page.evaluate((to) => {
      const idx = ((window.history.state as { idx?: number } | null)?.idx ?? 0) + 1;
      window.history.pushState({ usr: null, key: `e2e-${idx}`, idx }, "", to);
      window.dispatchEvent(new PopStateEvent("popstate", { state: window.history.state }));
    }, path);
  const liveMapOf = async (label: string) => {
    await expect(
      page.getByRole("heading", { level: 1, name: `Mass Times in ${label}` }),
    ).toBeVisible({ timeout: 15_000 });
    await expect(page.locator(".city-map-live[data-ready]")).toHaveCount(1, {
      timeout: 15_000,
    });
    return markerBoxes(page, `.leaflet-container :is(${MARKERS})`);
  };

  await page.goto("/");
  await expect(page.locator(".leaflet-container")).toBeVisible({ timeout: 15_000 });
  await routeTo(buffalo);
  expect(await liveMapOf("Buffalo, NY")).toEqual(buffaloBoxes);
  await routeTo("/mass-times/rochester-ny/");
  expect(await liveMapOf("Rochester, NY")).not.toEqual(buffaloBoxes);
  // Back to a city whose data is cached: the page is reused, not the map.
  await page.goBack();
  expect(await liveMapOf("Buffalo, NY")).toEqual(buffaloBoxes);

  // Opening the map keeps the router's place in history.
  const before = await page.evaluate(() => window.history.state);
  await page.getByRole("button", { name: "Expand map" }).click();
  await expect(page).toHaveURL(/#map$/);
  expect(await page.evaluate(() => window.history.state)).toEqual(before);
  await page.goBack();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page).toHaveURL(new RegExp(`${buffalo}$`));
});

test("in the app, a church page's breadcrumb goes to its city with no loading screen", async ({
  page,
}) => {
  await page.goto("/churches/");
  const cityLink = page.locator('h2 a[href^="/mass-times/"]').first();
  const cityHref = (await cityLink.getAttribute("href"))!;
  const cityLabel = (await cityLink.textContent())!.trim();
  const churchHref = (await page
    .locator("[data-city-group]")
    .first()
    .locator('li a[href^="/churches/"]')
    .first()
    .getAttribute("href"))!;

  await page.goto("/");
  await expect(page.locator(".leaflet-container")).toBeVisible({ timeout: 15_000 });
  // Navigates in the app, as a link in a map pin's popup would.
  await page.evaluate((to) => {
    const idx = ((window.history.state as { idx?: number } | null)?.idx ?? 0) + 1;
    window.history.pushState({ usr: null, key: `e2e-${idx}`, idx }, "", to);
    window.dispatchEvent(new PopStateEvent("popstate", { state: window.history.state }));
  }, churchHref);
  const breadcrumb = page.getByRole("navigation", { name: "Breadcrumb" });
  await expect(breadcrumb).toBeVisible({ timeout: 15_000 });

  // Note any "Loading…" the page shows from here on.
  await page.evaluate(() => {
    const w = window as typeof window & { sawLoading?: boolean };
    w.sawLoading = false;
    new MutationObserver(() => {
      if (/Loading/.test(document.body.innerText)) w.sawLoading = true;
    }).observe(document.body, { childList: true, subtree: true, characterData: true });
  });
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

  await breadcrumb.locator(`a[href="${cityHref}"]`).click();
  await expect(
    page.getByRole("heading", { level: 1, name: `Mass Times in ${cityLabel}` }),
  ).toBeVisible();
  expect(
    await page.evaluate(() => (window as typeof window & { sawLoading?: boolean }).sawLoading),
  ).toBe(false);
  // The city page opens at its top, as a page load would.
  expect(await page.evaluate(() => window.scrollY)).toBe(0);
});

test.describe("on a phone", () => {
  test.use({ viewport: { width: 390, height: 844 }, hasTouch: true });

  test("the map is live in the page and opens with filters and zoom", async ({
    page,
  }) => {
    await page.goto(EAST_AURORA);
    await expect(page.locator(".city-map .leaflet-container")).toBeVisible({
      timeout: 15_000,
    });

    await page.getByRole("button", { name: "Expand map" }).tap();
    await expect(page).toHaveURL(/#map$/);
    const dialog = page.getByRole("dialog", { name: /^Map of churches around / });
    await expect(dialog.getByRole("button", { name: "Zoom in" })).toBeVisible();

    await dialog.getByRole("button", { name: /^Filters/ }).tap();
    await expect(page.getByRole("button", { name: /^Show \d+ churches?$/ })).toBeVisible();
    await page.keyboard.press("Escape");
    await expect(dialog).toBeVisible();

    await page.getByRole("button", { name: "Close" }).tap();
    await expect(dialog).toHaveCount(0);
    await expect(page).toHaveURL(new RegExp(`${EAST_AURORA}$`));
  });
});

test.describe("without JavaScript", () => {
  test.use({ javaScriptEnabled: false });

  test("the map preview links to the home map on the city", async ({ page }) => {
    await page.goto(EAST_AURORA);
    const preview = page.getByRole("link", {
      name: /^Open the map of churches around /,
    });
    await expect(preview).toHaveAttribute(
      "href",
      /^\/\?lat=-?[\d.]+&lng=-?[\d.]+&z=\d+$/,
    );
  });
});
