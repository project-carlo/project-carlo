import { test, expect } from "@playwright/test";

test("unknown route is a real 404 that renders NotFoundPage", async ({
  page,
}) => {
  const response = await page.goto("/this-route-does-not-exist-xyz");
  // 404.html is the SPA shell served with a 404 status; React Router renders
  // the * route.
  expect(response?.status()).toBe(404);
  await expect(
    page.getByRole("heading", { name: "Page not found" }),
  ).toBeVisible();
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute(
    "content",
    "noindex",
  );
});

test("unknown church slug is a real 404", async ({ page }) => {
  const response = await page.goto("/churches/no-such-church-xyz/");
  expect(response?.status()).toBe(404);
  await expect(
    page.getByRole("heading", { name: "Church not found" }),
  ).toBeVisible();
});

test("NotFoundPage 'Map' link navigates to home", async ({ page }) => {
  await page.goto("/this-route-does-not-exist-xyz");
  await page.getByRole("link", { name: "Map", exact: true }).click();
  await expect(page).toHaveURL("/");
});
