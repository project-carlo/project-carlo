import { describe, expect, it } from "vitest";
import { rollUpEventsByDay } from "./eventRollup";
import type { EventSummary } from "../types";

let nextId = 1;

function weekly(day: string, startTime: number): EventSummary {
  return event({ kind: "weekly", day_of_week: day, start_time: startTime });
}

function onDate(date: string, startTime: number): EventSummary {
  return event({ kind: "specific_date", date, start_time: startTime });
}

function event(overrides: Partial<EventSummary>): EventSummary {
  return {
    id: nextId++,
    type: "mass",
    kind: "weekly",
    day_of_week: null,
    date: null,
    start_time: 0,
    end_time: null,
    cancelled: false,
    next_occurrence: null,
    page_number: null,
    note: null,
    ...overrides,
  };
}

describe("rollUpEventsByDay", () => {
  it("collapses several times on one weekday into a single row", () => {
    const rows = rollUpEventsByDay([
      weekly("sunday", 7 * 60 + 30),
      weekly("sunday", 9 * 60),
      weekly("sunday", 11 * 60),
    ]);

    expect(rows).toHaveLength(1);
    expect(rows[0].label).toBe("Sundays");
    expect(rows[0].times).toEqual(["7:30", "9", "11 a.m."]);
  });

  it("keeps distinct days on their own rows, in input order", () => {
    const rows = rollUpEventsByDay([
      weekly("sunday", 9 * 60),
      weekly("saturday", 16 * 60),
      weekly("monday", 8 * 60),
      weekly("saturday", 8 * 60),
    ]);

    expect(rows.map((row) => row.label)).toEqual([
      "Sundays",
      "Saturdays",
      "Mondays",
    ]);
  });

  it("sorts a day's times earliest-first regardless of input order", () => {
    const rows = rollUpEventsByDay([
      weekly("saturday", 16 * 60),
      weekly("saturday", 8 * 60),
    ]);

    expect(rows[0].times).toEqual(["8 a.m.", "4 p.m."]);
  });

  it("keeps every meridiem when a day straddles noon", () => {
    const rows = rollUpEventsByDay([
      weekly("sunday", 9 * 60),
      weekly("sunday", 17 * 60),
    ]);

    expect(rows[0].times).toEqual(["9 a.m.", "5 p.m."]);
  });

  it("lists a shared start time once", () => {
    const rows = rollUpEventsByDay([
      weekly("saturday", 16 * 60),
      event({
        kind: "weekly",
        day_of_week: "saturday",
        start_time: 16 * 60,
        type: "confession",
      }),
    ]);

    expect(rows[0].times).toEqual(["4 p.m."]);
  });

  it("groups specific-date events by their date", () => {
    const rows = rollUpEventsByDay([
      onDate("2026-03-17", 8 * 60),
      onDate("2026-03-17", 19 * 60),
      onDate("2026-03-18", 8 * 60),
    ]);

    expect(rows).toHaveLength(2);
    expect(rows[0].label).toBe("Tue, Mar 17");
    expect(rows[0].times).toEqual(["8 a.m.", "7 p.m."]);
    expect(rows[1].label).toBe("Wed, Mar 18");
  });

  it("gives an event with neither weekday nor date a row of its own", () => {
    const rows = rollUpEventsByDay([
      event({ kind: "weekly", start_time: 8 * 60 }),
      event({ kind: "weekly", start_time: 9 * 60 }),
    ]);

    expect(rows).toHaveLength(2);
    expect(rows.map((row) => row.label)).toEqual(["", ""]);
  });

  it("returns no rows for an empty schedule", () => {
    expect(rollUpEventsByDay([])).toEqual([]);
  });
});
