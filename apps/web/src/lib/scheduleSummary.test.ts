import { describe, expect, it } from "vitest";
import type { EventSummary } from "../types";
import { weeklyScheduleRows } from "./scheduleSummary";

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
    weeks_of_month: [],
    exclude_weeks: false,
    season: null,
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
      ["Sunday", ["8 a.m.", "10:30 a.m."]],
      ["Mon – Fri", ["8 a.m."]],
      ["Saturday", ["4 p.m."]],
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
      ["Thursday", ["8 a.m."]],
    ]);
  });

  it("reads day names as the church page does, whatever their case or spacing", () => {
    const rows = weeklyScheduleRows([weekly(" Sunday ", 9 * 60), weekly("someday", 480)]);
    expect(rows.map((r) => [r.label, r.times])).toEqual([["Sunday", ["9 a.m."]]]);
  });

  it("gives slots that aren't every week rows of their own, with their qualifier", () => {
    const rows = weeklyScheduleRows([
      { ...weekly("sunday", 8 * 60), weeks_of_month: ["first"] },
      { ...weekly("monday", 8 * 60), weeks_of_month: ["first"] },
      weekly("sunday", 10 * 60),
      weekly("tuesday", 8 * 60),
    ]);
    expect(rows.map((r) => [r.label, r.times, r.note])).toEqual([
      ["Sunday", ["10 a.m."], null],
      ["Sunday", ["8 a.m."], "First Sunday of the month"],
      // Weeks of the month count each weekday's occurrences, so the first
      // Sunday and first Monday are not folded into one row.
      ["Monday", ["8 a.m."], "First Monday of the month"],
      ["Tuesday", ["8 a.m."], null],
    ]);
  });

  it("folds a run of days that keep the same season", () => {
    const summer = { start_month: 6, start_day: null, end_month: 8, end_day: null };
    const rows = weeklyScheduleRows(
      ["monday", "tuesday", "wednesday"].map((day) => ({
        ...weekly(day, 7 * 60),
        season: summer,
      })),
    );
    expect(rows.map((r) => [r.label, r.times, r.note])).toEqual([
      ["Mon – Wed", ["7 a.m."], "June through August"],
    ]);
  });

  it("leaves out dated services", () => {
    expect(weeklyScheduleRows([dated("2026-12-24", 16 * 60)])).toEqual([]);
  });
});
