import { test, expect } from "@playwright/test";

test("home page mounts and renders cleanly", async ({ page, baseURL }) => {
  const pageErrors: string[] = [];
  const consoleErrors: string[] = [];
  const failedRequests: string[] = [];

  page.on("pageerror", (e) => pageErrors.push(e.message));
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(msg.text());
  });
  page.on("response", (response) => {
    const url = response.url();
    if (baseURL && url.startsWith(baseURL) && response.status() >= 400) {
      failedRequests.push(`${response.status()} ${url}`);
    }
  });

  const response = await page.goto("/");
  expect(response?.status()).toBe(200);

  await expect(page.locator("#root")).not.toBeEmpty();

  // Leaflet container mounts (HomePage is lazy-loaded behind Suspense)
  await expect(page.locator(".leaflet-container")).toBeVisible({
    timeout: 15_000,
  });

  // The data snapshot downloaded and decoded: churches are on the map.
  await expect(page.locator(".leaflet-marker-icon").first()).toBeVisible({
    timeout: 15_000,
  });

  await page.waitForLoadState("networkidle");

  expect(pageErrors, pageErrors.join("\n")).toEqual([]);
  expect(consoleErrors, consoleErrors.join("\n")).toEqual([]);
  expect(failedRequests, failedRequests.join("\n")).toEqual([]);
});

test("the home map has zoom buttons on a desktop, not on a phone", async ({
  page,
}) => {
  await page.goto("/?lat=43.15&lng=-77.6&z=10");
  const zoomIn = page.getByRole("button", { name: "Zoom in" });
  await expect(zoomIn).toBeVisible({ timeout: 15_000 });
  await zoomIn.click();
  await expect(page).toHaveURL(/[?&]z=11(&|$)/);

  await page.setViewportSize({ width: 390, height: 844 });
  await expect(zoomIn).toHaveCount(0);
  await expect(
    page.getByRole("button", { name: "Use my location", exact: true }),
  ).toBeVisible();
});

test("the search box only claims a list while its dropdown is open", async ({
  page,
}) => {
  await page.goto("/?lat=43.15&lng=-77.6&z=10");
  const input = page.getByRole("combobox");
  await expect(input).toBeVisible({ timeout: 15_000 });
  await expect(input).toHaveAccessibleName(
    "Search for a city, ZIP code, or address",
  );

  // Closed: not expanded, and no pointers at a list or item that isn't there.
  await expect(input).toHaveAttribute("aria-expanded", "false");
  await expect(input).not.toHaveAttribute("aria-controls");
  await expect(input).not.toHaveAttribute("aria-activedescendant");

  // Open (place mode offers "Use my location" straight away): every pointer
  // names an element on the page. cmdk only sets the active item once there
  // is a selection to move, so that one may be absent.
  await input.focus();
  await expect(input).toHaveAttribute("aria-expanded", "true");
  const listId = await input.getAttribute("aria-controls");
  expect(listId).toBeTruthy();
  await expect(page.locator(`[id="${listId}"]`)).toHaveRole("listbox");
  const activeId = await input.getAttribute("aria-activedescendant");
  if (activeId) {
    await expect(page.locator(`[id="${activeId}"]`)).toHaveRole("option");
  }

  // Escape on an empty field closes it, and the pointers go with the list.
  await input.press("Escape");
  await expect(page.getByRole("listbox")).toHaveCount(0);
  await expect(input).toHaveAttribute("aria-expanded", "false");
  await expect(input).not.toHaveAttribute("aria-controls");
  await expect(input).not.toHaveAttribute("aria-activedescendant");
});
