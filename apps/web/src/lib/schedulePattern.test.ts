import { describe, expect, it } from "vitest";
import {
  dateMatchesPattern,
  dateMatchesWeeks,
  dateInSeason,
  describeSchedulePattern,
  parseSeasonDay,
  parseSeasonMonth,
  parseSeasonNote,
  parseWeeksOfMonth,
  patternKey,
  type SchedulePattern,
} from "./schedulePattern";

function pattern(overrides: Partial<SchedulePattern> = {}): SchedulePattern {
  return {
    weeks_of_month: [],
    season_start_month: null,
    season_start_day: null,
    season_end_month: null,
    season_end_day: null,
    season_note: null,
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

describe("parseSeasonDay", () => {
  it("keeps a day the month can actually hold", () => {
    expect(parseSeasonDay(10, 9)).toBe(10);
    expect(parseSeasonDay("4", 6)).toBe(4);
  });

  it("drops a day that cannot fall in its month, leaving the whole month", () => {
    expect(parseSeasonDay(31, 9)).toBeNull();
    expect(parseSeasonDay(30, 2)).toBeNull();
    expect(parseSeasonDay(0, 6)).toBeNull();
  });

  it("has nothing to refine without a month", () => {
    expect(parseSeasonDay(10, null)).toBeNull();
  });
});

describe("parseSeasonNote", () => {
  it("keeps the bulletin's wording, tidied to one line", () => {
    expect(parseSeasonNote("October\n through  June")).toBe("October through June");
  });

  it("treats blank text as no note", () => {
    expect(parseSeasonNote("   ")).toBeNull();
    expect(parseSeasonNote(null)).toBeNull();
  });
});

describe("dateInSeason", () => {
  const on = (month: number, day: number, overrides: Partial<SchedulePattern>) =>
    dateInSeason(new Date(2026, month - 1, day), pattern(overrides));

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

  it("quotes the bulletin rather than the exact days behind it", () => {
    // The days are what filtering reads; "January 1 through April 30" is not
    // what the parish printed, so it is not what the reader is shown.
    expect(
      describeSchedulePattern(
        pattern({
          season_start_month: 1,
          season_start_day: 1,
          season_end_month: 4,
          season_end_day: 30,
          season_note: "January to April",
        }),
        "Wednesday",
      ),
    ).toBe("January to April");
  });

  it("still derives the weeks of the month beside a quoted season", () => {
    expect(
      describeSchedulePattern(
        pattern({
          weeks_of_month: ["first"],
          season_start_month: 10,
          season_end_month: 6,
          season_note: "during the school year",
        }),
        "Friday",
      ),
    ).toBe("First Friday of the month, during the school year");
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
