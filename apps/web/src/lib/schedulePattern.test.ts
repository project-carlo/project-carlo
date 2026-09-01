import { describe, expect, it } from "vitest";
import {
  dateMatchesPattern,
  dateMatchesWeeks,
  describeSchedulePattern,
  monthInSeason,
  parseSeasonMonth,
  parseWeeksOfMonth,
  patternKey,
  type SchedulePattern,
} from "./schedulePattern";

function pattern(overrides: Partial<SchedulePattern> = {}): SchedulePattern {
  return {
    weeks_of_month: [],
    season_start_month: null,
    season_end_month: null,
    ...overrides,
  };
}

describe("parseWeeksOfMonth", () => {
  it("splits the stored comma-separated column", () => {
    expect(parseWeeksOfMonth("first,third")).toEqual(["first", "third"]);
  });

  it("treats an absent or empty column as every week", () => {
    expect(parseWeeksOfMonth(null)).toEqual([]);
    expect(parseWeeksOfMonth("")).toEqual([]);
    expect(parseWeeksOfMonth(undefined)).toEqual([]);
  });

  it("drops tokens outside the vocabulary rather than guessing", () => {
    expect(parseWeeksOfMonth("first,occasionally")).toEqual(["first"]);
  });
});

describe("parseSeasonMonth", () => {
  it("keeps a usable month and rejects anything else", () => {
    expect(parseSeasonMonth(10)).toBe(10);
    expect(parseSeasonMonth(0)).toBeNull();
    expect(parseSeasonMonth(13)).toBeNull();
    expect(parseSeasonMonth(null)).toBeNull();
  });
});

describe("monthInSeason", () => {
  it("covers the turn of the year when the range wraps", () => {
    // October through June: the school-year shape a parish schedule takes.
    expect(monthInSeason(9, 10, 6)).toBe(false);
    expect(monthInSeason(10, 10, 6)).toBe(true);
    expect(monthInSeason(1, 10, 6)).toBe(true);
    expect(monthInSeason(6, 10, 6)).toBe(true);
    expect(monthInSeason(7, 10, 6)).toBe(false);
  });

  it("reads a range inside one year as written", () => {
    expect(monthInSeason(5, 6, 8)).toBe(false);
    expect(monthInSeason(7, 6, 8)).toBe(true);
  });

  it("treats a slot with no range as running all year", () => {
    expect(monthInSeason(2, null, null)).toBe(true);
  });
});

describe("dateMatchesWeeks", () => {
  // September 2026: Fridays fall on the 4th, 11th, 18th and 25th.
  const fridays = [4, 11, 18, 25].map((day) => new Date(2026, 8, day));

  it("matches every date when no weeks are named", () => {
    expect(fridays.every((d) => dateMatchesWeeks(d, []))).toBe(true);
  });

  it("matches only the first occurrence of the weekday", () => {
    expect(fridays.map((d) => dateMatchesWeeks(d, ["first"]))).toEqual([
      true,
      false,
      false,
      false,
    ]);
  });

  it("counts occurrences of the weekday, not calendar weeks", () => {
    // The 4th is the first Friday even though it sits in the month's first
    // partial week; the 11th is the second.
    expect(dateMatchesWeeks(new Date(2026, 8, 11), ["second"])).toBe(true);
  });

  it("reads 'last' as the final occurrence, not the fourth", () => {
    // October 2026 has five Fridays: 2, 9, 16, 23, 30.
    expect(dateMatchesWeeks(new Date(2026, 9, 23), ["last"])).toBe(false);
    expect(dateMatchesWeeks(new Date(2026, 9, 30), ["last"])).toBe(true);
    expect(dateMatchesWeeks(new Date(2026, 9, 23), ["fourth"])).toBe(true);
  });

  it("matches any of several named weeks", () => {
    expect(fridays.map((d) => dateMatchesWeeks(d, ["second", "fourth"]))).toEqual(
      [false, true, false, true],
    );
  });
});

describe("dateMatchesPattern", () => {
  it("requires the week and the season both", () => {
    const monthlyInSeason = pattern({
      weeks_of_month: ["first"],
      season_start_month: 10,
      season_end_month: 6,
    });
    // First Friday of October, in season.
    expect(dateMatchesPattern(new Date(2026, 9, 2), monthlyInSeason)).toBe(true);
    // First Friday of September, out of season.
    expect(dateMatchesPattern(new Date(2026, 8, 4), monthlyInSeason)).toBe(
      false,
    );
    // In season, but the third Friday.
    expect(dateMatchesPattern(new Date(2026, 9, 16), monthlyInSeason)).toBe(
      false,
    );
  });
});

describe("patternKey", () => {
  it("gives every plain weekly slot the same key", () => {
    expect(patternKey(pattern())).toBe("");
  });

  it("separates slots that keep different schedules", () => {
    expect(patternKey(pattern({ weeks_of_month: ["first"] }))).not.toBe(
      patternKey(pattern()),
    );
    expect(patternKey(pattern({ weeks_of_month: ["first"] }))).not.toBe(
      patternKey(pattern({ weeks_of_month: ["second"] })),
    );
  });
});

describe("describeSchedulePattern", () => {
  it("says nothing about a plain weekly slot", () => {
    expect(describeSchedulePattern(pattern(), "Friday")).toBeNull();
  });

  it("names the week of the month against its weekday", () => {
    expect(
      describeSchedulePattern(pattern({ weeks_of_month: ["first"] }), "Friday"),
    ).toBe("First Friday of the month");
  });

  it("lists several weeks in one phrase", () => {
    expect(
      describeSchedulePattern(
        pattern({ weeks_of_month: ["second", "fourth"] }),
        "saturday",
      ),
    ).toBe("Second and fourth Saturdays of the month");
  });

  it("names the season range", () => {
    expect(
      describeSchedulePattern(
        pattern({ season_start_month: 10, season_end_month: 6 }),
        "Tuesday",
      ),
    ).toBe("October through June");
  });

  it("carries both qualifiers when a slot has both", () => {
    expect(
      describeSchedulePattern(
        pattern({
          weeks_of_month: ["first"],
          season_start_month: 10,
          season_end_month: 6,
        }),
        "Friday",
      ),
    ).toBe("First Friday of the month, October through June");
  });
});
