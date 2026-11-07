import { describe, expect, it } from "vitest";
import {
  DAY_ORDER,
  FILTER_DAY_LABELS,
  filterDayFromJsDay,
  jsDayFor,
} from "./days";

describe("jsDayFor", () => {
  it("returns the value Date.getDay() gives for the same day", () => {
    // 2026-06-14 is a Sunday, so the week starting there walks DAY_ORDER.
    DAY_ORDER.forEach((day, index) => {
      const date = new Date(2026, 5, 14 + index);
      expect(date.getDay()).toBe(index);
      expect(jsDayFor(day)).toBe(date.getDay());
    });
  });

  it("accepts the capitalised, padded form the pipeline writes", () => {
    expect(jsDayFor("Wednesday")).toBe(3);
    expect(jsDayFor("  saturday ")).toBe(6);
  });

  it("returns -1 for anything that is not a weekday name", () => {
    expect(jsDayFor("someday")).toBe(-1);
    expect(jsDayFor("")).toBe(-1);
  });
});

describe("filterDayFromJsDay", () => {
  it("shifts Sunday-first to the filter's Monday-first indexing", () => {
    expect(filterDayFromJsDay(jsDayFor("monday"))).toBe(0);
    expect(filterDayFromJsDay(jsDayFor("sunday"))).toBe(6);
  });

  it("passes a non-weekday through as -1", () => {
    expect(filterDayFromJsDay(jsDayFor("someday"))).toBe(-1);
  });
});

describe("FILTER_DAY_LABELS", () => {
  it("is Monday-first and indexed to match FilterState.daysOfWeek", () => {
    expect(FILTER_DAY_LABELS).toEqual([
      { full: "Monday", abbr: "Mon" },
      { full: "Tuesday", abbr: "Tue" },
      { full: "Wednesday", abbr: "Wed" },
      { full: "Thursday", abbr: "Thu" },
      { full: "Friday", abbr: "Fri" },
      { full: "Saturday", abbr: "Sat" },
      { full: "Sunday", abbr: "Sun" },
    ]);
  });

  it("agrees with filterDayFromJsDay on every day", () => {
    FILTER_DAY_LABELS.forEach((label, index) => {
      expect(filterDayFromJsDay(jsDayFor(label.full))).toBe(index);
    });
  });
});
