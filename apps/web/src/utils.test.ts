import { describe, expect, it } from "vitest";
import type { Season, WeekOfMonth } from "./types";
import { formatQualifiedTime, formatSlotQualifier } from "./utils";

function qualifier(weeks: WeekOfMonth[], season: Season | null = null) {
  return formatSlotQualifier({ weeks_of_month: weeks, season });
}

describe("formatSlotQualifier", () => {
  it("is null for a slot held every week, all year", () => {
    expect(qualifier([])).toBeNull();
  });

  it("lists the weeks of the month in calendar order", () => {
    expect(qualifier(["first"])).toBe("1st");
    expect(qualifier(["third", "first"])).toBe("1st & 3rd");
    expect(qualifier(["last", "second", "fourth"])).toBe("2nd, 4th & last");
    expect(qualifier(["fifth"])).toBe("5th");
  });

  it("names a season by its months, and its days when it has them", () => {
    const season = (
      start_month: number,
      start_day: number | null,
      end_month: number,
      end_day: number | null,
    ): Season => ({ start_month, start_day, end_month, end_day });
    expect(qualifier([], season(5, null, 10, null))).toBe("May–Oct");
    expect(qualifier([], season(10, null, 6, 15))).toBe("Oct–Jun 15");
    expect(qualifier([], season(7, null, 7, null))).toBe("Jul");
    expect(qualifier(["first", "third"], season(6, 15, 9, 7))).toBe(
      "1st & 3rd, Jun 15–Sep 7",
    );
  });
});

describe("formatQualifiedTime", () => {
  it("adds a qualifier in parentheses", () => {
    expect(formatQualifiedTime("10 a.m.", "1st & 3rd")).toBe("10 a.m. (1st & 3rd)");
    expect(formatQualifiedTime("10 a.m.", null)).toBe("10 a.m.");
  });
});
