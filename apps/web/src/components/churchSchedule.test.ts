import { describe, expect, it } from "vitest";
import type { EventSummary, WeekOfMonth } from "@carlo/core";
import { collectSectionEvents, partitionEventsByType } from "./churchSchedule";

let nextId = 1;
function weekly(
  day: string,
  start: number,
  extra: Partial<EventSummary> = {},
): EventSummary {
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
    ...extra,
  };
}

function onWeeks(weeks: WeekOfMonth[], extra: Partial<EventSummary> = {}) {
  return { weeks_of_month: weeks, ...extra };
}

describe("partitionEventsByType", () => {
  it("gives a 4th-Sunday Mass a row of its own, not a Sunday time", () => {
    // The Our Lady of Fatima Shrine's Sunday, where the 4th-Sunday Tagalog
    // Mass at 1:30 once sat between the every-week 12 and 5.
    const { mass } = partitionEventsByType([
      weekly("sunday", 17 * 60),
      weekly("sunday", 13.5 * 60, onWeeks(["fourth"], { note: "Tagalog" })),
      weekly("sunday", 9 * 60),
      weekly("sunday", 12 * 60),
    ]);
    expect(mass.weeklyByDay.sunday.map((e) => e.start_time)).toEqual([
      9 * 60,
      12 * 60,
      17 * 60,
    ]);
    expect(mass.patterned).toHaveLength(1);
    expect(mass.patterned[0]).toMatchObject({
      label: "4th Sunday",
      qualifier: null,
    });
    expect(mass.patterned[0].events.map((e) => e.note)).toEqual(["Tagalog"]);
  });

  it("puts slots with one schedule on one row, and keeps the sections apart", () => {
    const sections = partitionEventsByType([
      weekly("saturday", 10 * 60, onWeeks(["first"], { type: "adoration" })),
      weekly("saturday", 8 * 60, onWeeks(["first"], { type: "adoration" })),
      weekly("saturday", 9 * 60, onWeeks(["first"], { type: "confession" })),
    ]);
    expect(sections.adoration.patterned).toHaveLength(1);
    expect(
      sections.adoration.patterned[0].events.map((e) => e.start_time),
    ).toEqual([8 * 60, 10 * 60]);
    expect(sections.confession.patterned).toHaveLength(1);
    expect(sections.mass.patterned).toEqual([]);
  });

  it("orders rows by weekday, then the ones that run most weeks first", () => {
    const season = { start_month: 10, start_day: null, end_month: 6, end_day: null };
    const { mass } = partitionEventsByType([
      weekly("tuesday", 18 * 60, { season }),
      weekly("sunday", 8 * 60, onWeeks(["fourth"])),
      weekly("sunday", 11 * 60, onWeeks(["last"], { exclude_weeks: true })),
      weekly("sunday", 15 * 60, onWeeks(["first"])),
    ]);
    expect(mass.patterned.map((row) => [row.label, row.qualifier])).toEqual([
      ["Sunday", "Every Sunday except the last"],
      ["1st Sunday", null],
      ["4th Sunday", null],
      ["Tuesday", "October through June"],
    ]);
  });

  it("counts every row's slots for the section", () => {
    const sections = partitionEventsByType([
      weekly("sunday", 9 * 60),
      weekly("sunday", 13.5 * 60, onWeeks(["fourth"])),
      { ...weekly("", 19 * 60), kind: "specific_date", day_of_week: null, date: "2026-12-24" },
    ]);
    expect(
      collectSectionEvents(sections.mass).map((e) => e.start_time),
    ).toEqual([9 * 60, 13.5 * 60, 19 * 60]);
  });
});
