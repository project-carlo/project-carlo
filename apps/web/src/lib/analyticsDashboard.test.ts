import { describe, expect, it } from "vitest";
import { fillDays, niceMax, rowCount, rowLabel } from "./analyticsDashboard";

describe("fillDays", () => {
  const now = Date.UTC(2026, 9, 12, 15);

  it("fills the days nothing happened with zeros", () => {
    const days = fillDays(
      [
        { day: "2026-10-10 00:00:00", visits: 3, pageviews: 7 },
        { day: "2026-10-12 00:00:00", visits: "1", pageviews: "2" },
      ],
      3,
      now,
    );
    expect(days).toEqual([
      { date: "2026-10-09", visits: 0, pageviews: 0 },
      { date: "2026-10-10", visits: 3, pageviews: 7 },
      { date: "2026-10-11", visits: 0, pageviews: 0 },
      { date: "2026-10-12", visits: 1, pageviews: 2 },
    ]);
  });
});

describe("niceMax", () => {
  it("rounds up to 1, 2 or 5 of a power of ten", () => {
    expect(niceMax(0)).toBe(1);
    expect(niceMax(1)).toBe(1);
    expect(niceMax(3)).toBe(5);
    expect(niceMax(7)).toBe(10);
    expect(niceMax(12)).toBe(20);
    expect(niceMax(200)).toBe(200);
    expect(niceMax(201)).toBe(500);
  });
});

describe("rowLabel and rowCount", () => {
  it("labels by every column before the count", () => {
    const row = { event: "search_select", kind: "church", count: 4 };
    expect(rowLabel(row)).toBe("search_select · church");
    expect(rowCount(row)).toBe(4);
  });

  it("skips empty labels", () => {
    expect(rowLabel({ event: "map_open", kind: "", count: 2 })).toBe("map_open");
    expect(rowLabel({ page: "", count: 2 })).toBe("(none)");
  });
});
