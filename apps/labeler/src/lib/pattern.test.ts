import { describe, expect, it } from "vitest";
import type { Season } from "../types";
import {
  allBut,
  allButWeek,
  describeSeason,
  describeWeeks,
  inSeason,
  parseSeason,
  seasonProblems,
  toggleWeek,
} from "./pattern";

describe("weeks of the month", () => {
  it("toggles weeks in canonical order", () => {
    expect(toggleWeek([], "third")).toEqual(["third"]);
    expect(toggleWeek(["third"], "first")).toEqual(["first", "third"]);
    expect(toggleWeek(["first", "third"], "third")).toEqual(["first"]);
    expect(toggleWeek(["first"], "last")).toEqual(["first", "last"]);
  });

  it("keeps last distinct from fourth", () => {
    expect(toggleWeek(["fourth"], "last")).toEqual(["fourth", "last"]);
    expect(describeWeeks(["last"])).toBe("Last");
    expect(describeWeeks(["fourth"])).toBe("4th");
  });

  it("collapses all five numbered weeks to every week", () => {
    expect(toggleWeek(["first", "second", "third", "fourth"], "fifth")).toEqual([]);
    expect(toggleWeek(["first", "second", "third", "fifth", "last"], "fourth")).toEqual([]);
  });

  it("saves all-but as the remaining numbered weeks", () => {
    expect(allBut("second")).toEqual(["first", "third", "fourth", "fifth"]);
    expect(allBut("fifth")).toEqual(["first", "second", "third", "fourth"]);
    expect(allBut("last")).toBeNull();
  });

  it("recognises an all-but list", () => {
    expect(allButWeek(["first", "third", "fourth", "fifth"])).toBe("second");
    expect(allButWeek(["first", "third", "fourth", "last"])).toBeNull();
    expect(allButWeek(["first", "third"])).toBeNull();
  });

  it("describes weeks", () => {
    expect(describeWeeks([])).toBe("Every week");
    expect(describeWeeks(["first", "third"])).toBe("1st & 3rd");
    expect(describeWeeks(["first", "third", "fourth", "fifth"])).toBe("All but 2nd");
  });
});

describe("seasons", () => {
  const schoolYear: Season = { start_month: 9, start_day: null, end_month: 5, end_day: null };
  const summer: Season = { start_month: 6, start_day: 4, end_month: 9, end_day: 10 };

  it("parses month ranges, wrapping past New Year", () => {
    expect(parseSeason("Sep-May")).toEqual({ season: schoolYear });
    expect(parseSeason("9-5")).toEqual({ season: schoolYear });
    expect(parseSeason("September through May")).toEqual({ season: schoolYear });
    expect(parseSeason("sept to may")).toEqual({ season: schoolYear });
  });

  it("parses day-level boundaries", () => {
    expect(parseSeason("Jun 4 - Sep 10")).toEqual({ season: summer });
    expect(parseSeason("June 4th – September 10th")).toEqual({ season: summer });
    expect(parseSeason("6/4-9/10")).toEqual({ season: summer });
    expect(parseSeason("4 Jun - 10 Sep")).toEqual({ season: summer });
  });

  it("treats empty input as all year and rejects nonsense", () => {
    expect(parseSeason("")).toEqual({ season: null });
    expect(parseSeason("all year")).toEqual({ season: null });
    expect(parseSeason("Lent")).toBeNull();
    expect(parseSeason("13-5")).toBeNull();
    expect(parseSeason("Feb 30 - Mar 3")).toBeNull();
    expect(parseSeason("Sep")).toBeNull();
  });

  it("allows February 29", () => {
    expect(parseSeason("Dec 1 - Feb 29")?.season?.end_day).toBe(29);
    expect(seasonProblems({ start_month: 2, start_day: 30, end_month: 3, end_day: null })).toEqual([
      "start day 30 is not in February",
    ]);
  });

  it("checks membership, including wrapping seasons", () => {
    expect(inSeason(schoolYear, 9, 1)).toBe(true);
    expect(inSeason(schoolYear, 12, 25)).toBe(true);
    expect(inSeason(schoolYear, 1, 1)).toBe(true);
    expect(inSeason(schoolYear, 5, 31)).toBe(true);
    expect(inSeason(schoolYear, 6, 1)).toBe(false);
    expect(inSeason(schoolYear, 8, 31)).toBe(false);
    expect(inSeason(summer, 6, 3)).toBe(false);
    expect(inSeason(summer, 6, 4)).toBe(true);
    expect(inSeason(summer, 9, 10)).toBe(true);
    expect(inSeason(summer, 9, 11)).toBe(false);
  });

  it("describes seasons at the grain they were given", () => {
    expect(describeSeason(null)).toBe("All year");
    expect(describeSeason(schoolYear)).toBe("Sep – May");
    expect(describeSeason(summer)).toBe("Jun 4 – Sep 10");
  });
});
