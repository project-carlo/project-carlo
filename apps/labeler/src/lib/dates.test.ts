import { describe, expect, it } from "vitest";
import { dateForWeekday, dayOfDate, describeDays, formatDate, parseDates, parseDays, parseLooseDate } from "./dates";
import { DAYS } from "../types";

describe("parseDays", () => {
  it.each([
    ["Sun", ["Sunday"]],
    ["sunday", ["Sunday"]],
    ["Sundays", ["Sunday"]],
    ["Mon-Fri", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]],
    ["mon – fri", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]],
    ["M-F", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]],
    ["sat, sun", ["Saturday", "Sunday"]],
    ["Tue & Thu", ["Tuesday", "Thursday"]],
    ["tues and thurs", ["Tuesday", "Thursday"]],
    ["tu/th", ["Tuesday", "Thursday"]],
    ["weekdays", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]],
    ["weekends", ["Saturday", "Sunday"]],
    ["fri-mon", ["Monday", "Friday", "Saturday", "Sunday"]],
    ["daily", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]],
    ["m w f", ["Monday", "Wednesday", "Friday"]],
  ])("reads %s", (input, expected) => {
    expect(parseDays(input)).toEqual(expected);
  });

  it.each(["", "t", "s", "tomorrow", "mon-xyz", "funday"])("rejects %j", (input) => {
    expect(parseDays(input)).toBeNull();
  });
});

describe("parseLooseDate", () => {
  const ref = "2026-09-27";

  it.each([
    ["2026-10-05", "2026-10-05"],
    ["10/5", "2026-10-05"],
    ["10/5/26", "2026-10-05"],
    ["10/5/2027", "2027-10-05"],
    ["Oct 5", "2026-10-05"],
    ["October 5th", "2026-10-05"],
    ["5 October", "2026-10-05"],
    ["Mon Oct 5", "2026-10-05"],
    ["Monday, October 5, 2026", "2026-10-05"],
    ["Sept 30", "2026-09-30"],
  ])("reads %s", (input, expected) => {
    expect(parseLooseDate(input, ref)).toBe(expected);
  });

  it("takes the year nearest the bulletin date", () => {
    expect(parseLooseDate("1/3", "2026-12-20")).toBe("2027-01-03");
    expect(parseLooseDate("12/28", "2027-01-03")).toBe("2026-12-28");
  });

  it.each(["", "Octember 5", "2/30", "13/1", "someday"])("rejects %j", (input) => {
    expect(parseLooseDate(input, ref)).toBeNull();
  });

  it("splits several dates", () => {
    expect(parseDates("10/2; 10/9", ref)).toEqual(["2026-10-02", "2026-10-09"]);
    expect(parseDates("Oct 2, Oct 9", ref)).toEqual(["2026-10-02", "2026-10-09"]);
    expect(parseDates("October 5, 2026", ref)).toEqual(["2026-10-05"]);
    expect(parseDates("10/2, nope", ref)).toBeNull();
  });

  it("formats dates with their weekday", () => {
    expect(formatDate("2026-10-05")).toBe("Mon Oct 5");
    expect(formatDate(null)).toBe("");
  });

  it("reads back a formatted list of dates", () => {
    const dates = ["2026-10-02", "2026-10-09"];
    expect(parseDates(dates.map(formatDate).join("; "), ref)).toEqual(dates);
  });
});

describe("dateForWeekday", () => {
  // 2026-09-27 is a Sunday, so the bulletin week runs through Saturday 2026-10-03.
  it("places each weekday on or after a Sunday bulletin date", () => {
    expect(DAYS.map((day) => dateForWeekday("2026-09-27", day))).toEqual([
      "2026-09-28",
      "2026-09-29",
      "2026-09-30",
      "2026-10-01",
      "2026-10-02",
      "2026-10-03",
      "2026-09-27",
    ]);
  });

  it("uses the same weekday when the bulletin falls on it, and the next week otherwise", () => {
    expect(dateForWeekday("2026-09-30", "Wednesday")).toBe("2026-09-30");
    expect(dateForWeekday("2026-09-30", "Tuesday")).toBe("2026-10-06");
  });

  it("rejects a bulletin date that is not a day", () => {
    expect(dateForWeekday("nope", "Sunday")).toBeNull();
  });
});

describe("dayOfDate", () => {
  it("reads the weekday of an ISO date", () => {
    expect(dayOfDate("2026-10-02")).toBe("Friday");
    expect(dayOfDate("2026-10-03")).toBe("Saturday");
    expect(dayOfDate("2026-09-27")).toBe("Sunday");
    expect(dayOfDate("nope")).toBeNull();
  });
});

describe("describeDays", () => {
  it.each([
    ["Mon-Fri", "Mon–Fri"],
    ["sat, sun", "Sat, Sun"],
    ["m w f", "Mon, Wed, Fri"],
    ["daily", "Mon–Sun"],
    ["fri-mon", "Mon, Fri, Sat, Sun"],
  ])("describes %s as %s, which reads back the same", (input, expected) => {
    const days = parseDays(input)!;
    expect(describeDays(days)).toBe(expected);
    expect(parseDays(describeDays(days))).toEqual(days);
  });
});
