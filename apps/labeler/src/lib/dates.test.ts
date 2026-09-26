import { describe, expect, it } from "vitest";
import { formatDate, parseDates, parseDays, parseLooseDate } from "./dates";

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
});
