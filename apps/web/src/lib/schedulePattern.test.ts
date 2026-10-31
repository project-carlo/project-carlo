import { describe, expect, it } from "vitest";
import type { WeekOfMonth } from "../types";
import {
  dateMatchesPattern,
  dateMatchesWeeks,
  dateInSeason,
  describeSchedulePattern,
  patternKey,
  type SchedulePattern,
} from "./schedulePattern";

/** The qualifiers as the snapshot's flat columns, for writing cases briefly. */
interface FlatPattern {
  weeks_of_month?: WeekOfMonth[];
  exclude_weeks?: boolean;
  season_start_month?: number;
  season_start_day?: number;
  season_end_month?: number;
  season_end_day?: number;
}

function pattern(flat: FlatPattern = {}): SchedulePattern {
  const { season_start_month: start, season_end_month: end } = flat;
  return {
    weeks_of_month: flat.weeks_of_month ?? [],
    exclude_weeks: flat.exclude_weeks,
    season:
      start == null || end == null
        ? null
        : {
            start_month: start,
            start_day: flat.season_start_day ?? null,
            end_month: end,
            end_day: flat.season_end_day ?? null,
          },
  };
}

describe("dateInSeason", () => {
  const on = (month: number, day: number, flat: FlatPattern) =>
    dateInSeason(new Date(2026, month - 1, day), pattern(flat).season);

  it("covers the turn of the year when the range wraps", () => {
    // October through June: the school-year shape a parish schedule takes.
    const schoolYear = { season_start_month: 10, season_end_month: 6 };
    expect(on(9, 30, schoolYear)).toBe(false);
    expect(on(10, 1, schoolYear)).toBe(true);
    expect(on(1, 15, schoolYear)).toBe(true);
    expect(on(6, 30, schoolYear)).toBe(true);
    expect(on(7, 1, schoolYear)).toBe(false);
  });

  it("reads a range inside one year as written", () => {
    const summer = { season_start_month: 6, season_end_month: 8 };
    expect(on(5, 31, summer)).toBe(false);
    expect(on(7, 4, summer)).toBe(true);
  });

  it("holds a dated range to the day at both ends", () => {
    // "June 4 - September 10": the first days of June are not in it.
    const dated = {
      season_start_month: 6,
      season_start_day: 4,
      season_end_month: 9,
      season_end_day: 10,
    };
    expect(on(6, 3, dated)).toBe(false);
    expect(on(6, 4, dated)).toBe(true);
    expect(on(9, 10, dated)).toBe(true);
    expect(on(9, 11, dated)).toBe(false);
  });

  it("runs a dated range that wraps the new year to the day", () => {
    const dated = {
      season_start_month: 10,
      season_start_day: 15,
      season_end_month: 4,
      season_end_day: 20,
    };
    expect(on(10, 14, dated)).toBe(false);
    expect(on(10, 15, dated)).toBe(true);
    expect(on(12, 31, dated)).toBe(true);
    expect(on(4, 20, dated)).toBe(true);
    expect(on(4, 21, dated)).toBe(false);
  });

  it("stretches an undated boundary across its whole month", () => {
    const months = { season_start_month: 1, season_end_month: 4 };
    expect(on(1, 1, months)).toBe(true);
    expect(on(4, 30, months)).toBe(true);
    expect(on(5, 1, months)).toBe(false);
  });

  it("treats a slot with no range as running all year", () => {
    expect(on(2, 14, {})).toBe(true);
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

  it("skips the excluded weeks and keeps the rest", () => {
    expect(fridays.map((d) => dateMatchesWeeks(d, ["last"], true))).toEqual([
      true,
      true,
      true,
      false,
    ]);
    // October 2026 has five Fridays: the fourth (23rd) is kept, the last
    // (30th) skipped, which no list of kept weeks could say for every month.
    expect(dateMatchesWeeks(new Date(2026, 9, 23), ["last"], true)).toBe(true);
    expect(dateMatchesWeeks(new Date(2026, 9, 30), ["last"], true)).toBe(false);
    expect(
      fridays.map((d) => dateMatchesWeeks(d, ["first", "last"], true)),
    ).toEqual([false, true, true, false]);
  });

  it("keeps every week when an exclusion names none", () => {
    expect(fridays.every((d) => dateMatchesWeeks(d, [], true))).toBe(true);
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

  it("separates the weeks kept from the same weeks skipped", () => {
    expect(
      patternKey(pattern({ weeks_of_month: ["last"], exclude_weeks: true })),
    ).not.toBe(patternKey(pattern({ weeks_of_month: ["last"] })));
  });

  it("ignores the order the weeks are listed in", () => {
    expect(patternKey(pattern({ weeks_of_month: ["third", "first"] }))).toBe(
      patternKey(pattern({ weeks_of_month: ["first", "third"] })),
    );
  });

  it("separates seasons that share their months but not their days", () => {
    const june = { season_start_month: 6, season_end_month: 9 };
    expect(patternKey(pattern({ ...june, season_start_day: 4 }))).not.toBe(
      patternKey(pattern(june)),
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

  it("words an exclusion as the weeks skipped", () => {
    expect(
      describeSchedulePattern(
        pattern({ weeks_of_month: ["last"], exclude_weeks: true }),
        "sunday",
      ),
    ).toBe("Every Sunday except the last");
    expect(
      describeSchedulePattern(
        pattern({ weeks_of_month: ["last", "first"], exclude_weeks: true }),
        null,
      ),
    ).toBe("Every week except the first and last");
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

  it("dates the range when the bulletin dated it", () => {
    expect(
      describeSchedulePattern(
        pattern({
          season_start_month: 6,
          season_start_day: 4,
          season_end_month: 9,
          season_end_day: 10,
        }),
        "Thursday",
      ),
    ).toBe("June 4 through September 10");
  });

  it("keeps a range stated in whole months in whole months", () => {
    // A parish that wrote "January to April" never said the 30th of April, and
    // the null days are what keep it from being read back one.
    expect(
      describeSchedulePattern(
        pattern({ season_start_month: 1, season_end_month: 4 }),
        "Wednesday",
      ),
    ).toBe("January through April");
  });

  it("dates only the end the bulletin dated", () => {
    expect(
      describeSchedulePattern(
        pattern({
          season_start_month: 9,
          season_start_day: 8,
          season_end_month: 5,
        }),
        "Sunday",
      ),
    ).toBe("September 8 through May");
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
