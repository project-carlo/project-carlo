import { test, expect } from "@playwright/test";

const ST_ANTHONY = "/churches/st-anthony-of-padua-buffalo/";

test("a church page links its times as a calendar file to download", async ({ page, request }) => {
  await page.goto(ST_ANTHONY);
  const link = page.getByRole("link", { name: "Add to your calendar" });
  await expect(link).toHaveAttribute("href", `${ST_ANTHONY}schedule.ics`);

  const download = page.waitForEvent("download");
  await link.click();
  expect((await download).suggestedFilename()).toBe("st-anthony-of-padua-buffalo.ics");

  const response = await request.get(`${ST_ANTHONY}schedule.ics`);
  expect(response.ok()).toBe(true);
  expect(response.headers()["content-type"]).toBe("text/calendar; charset=utf-8");
  const body = await response.text();
  expect(body.startsWith("BEGIN:VCALENDAR\r\n")).toBe(true);
  expect(body).toContain("SUMMARY:Mass at St. Anthony of Padua Church");
});
