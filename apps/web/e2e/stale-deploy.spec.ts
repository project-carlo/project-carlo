import { test, expect, type Page } from "@playwright/test";

// A deploy removes the previous build's hashed chunks, so a page loaded
// before it gets 404.html for a lazy chunk. These stand in for that by
// answering HomePage's chunk the way the live site answers a missing one.
async function removeHomePageChunk(page: Page, times?: number) {
  await page.route(
    "**/assets/HomePage-*.js",
    (route) =>
      route.fulfill({
        status: 404,
        contentType: "text/html",
        body: "<!doctype html><title>Not found</title>",
      }),
    { times },
  );
}

/** Counts the page's document loads, the first one included. */
function countLoads(page: Page): () => number {
  let loads = 0;
  page.on("load", () => loads++);
  return () => loads;
}

test("a page left over from an earlier deploy reloads into the new one", async ({
  page,
}) => {
  await removeHomePageChunk(page, 1);
  const loads = countLoads(page);

  await page.goto("/");

  await expect(page.locator(".leaflet-container")).toBeVisible({
    timeout: 15_000,
  });
  expect(loads()).toBe(2);
  await expect(
    page.getByRole("heading", { name: "Something went wrong" }),
  ).toHaveCount(0);
});

test("a chunk missing from the live site too shows an error, not a reload loop", async ({
  page,
}) => {
  await removeHomePageChunk(page);
  const loads = countLoads(page);

  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "Something went wrong" }),
  ).toBeVisible({ timeout: 15_000 });
  await expect(page.getByRole("button", { name: "Reload" })).toBeVisible();
  // One reload to look for a new version, then it stops.
  expect(loads()).toBe(2);
  await expect(page.getByText("Unexpected Application Error")).toHaveCount(0);
});
