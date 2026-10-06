import { describe, expect, it } from "vitest";
import type { EventSummary } from "../types";
import { compactScheduleRows, weeklyScheduleRows } from "./scheduleSummary";

let nextId = 1;
function weekly(day: string, start: number): EventSummary {
  return {
    id: nextId++,
    type: "mass",
    kind: "weekly",
    day_of_week: day,
    date: null,
    start_time: start,
    end_time: null,
    cancelled: false,
    next_occurrence: null,
    page_number: null,
    note: null,
  };
}

function dated(date: string, start: number): EventSummary {
  return { ...weekly("", start), kind: "specific_date", day_of_week: null, date };
}

describe("weeklyScheduleRows", () => {
  it("folds runs of adjacent days with the same times into one row", () => {
    const rows = weeklyScheduleRows([
      weekly("Saturday", 16 * 60),
      weekly("Sunday", 10 * 60 + 30),
      weekly("Sunday", 8 * 60),
      ...["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].map((d) =>
        weekly(d, 8 * 60),
      ),
    ]);
    expect(rows.map((r) => [r.label, r.times])).toEqual([
      ["Sundays", ["8 a.m.", "10:30 a.m."]],
      ["Mon – Fri", ["8 a.m."]],
      ["Saturdays", ["4 p.m."]],
    ]);
  });

  it("doesn't fold days across a gap, and pairs two adjacent days", () => {
    const rows = weeklyScheduleRows([
      weekly("monday", 480),
      weekly("tuesday", 480),
      weekly("thursday", 480),
      weekly("thursday", 480),
    ]);
    expect(rows.map((r) => [r.label, r.times])).toEqual([
      ["Mon & Tue", ["8 a.m."]],
      ["Thursdays", ["8 a.m."]],
    ]);
  });
});

describe("compactScheduleRows", () => {
  it("adds the soonest dated services after the weekly rows", () => {
    const rows = compactScheduleRows(
      [
        dated("2026-12-25", 0),
        weekly("Sunday", 600),
        dated("2026-12-24", 16 * 60),
        dated("2026-12-24", 22 * 60),
        dated("2027-01-01", 600),
      ],
      2,
    );
    expect(rows.map((r) => [r.label, r.times])).toEqual([
      ["Sundays", ["10 a.m."]],
      ["Thu, Dec 24", ["4 p.m.", "10 p.m."]],
      ["Fri, Dec 25", ["12 a.m."]],
    ]);
  });
});
