import { describe, expect, it } from "vitest";
import { formatDuration, formatTime, minutesOf, parseLooseTime } from "./time";

describe("parseLooseTime", () => {
  it.each([
    ["530p", "17:30"],
    ["530P", "17:30"],
    ["5:30p", "17:30"],
    ["5:30 pm", "17:30"],
    ["5:30 p.m.", "17:30"],
    ["5.30pm", "17:30"],
    ["5p", "17:00"],
    ["12p", "12:00"],
    ["12:15 PM", "12:15"],
    ["12a", "00:00"],
    ["12:30am", "00:30"],
    ["7a", "07:00"],
    ["1130a", "11:30"],
    ["17:30", "17:30"],
    ["1730", "17:30"],
    ["0730", "07:30"],
    ["07:30", "07:30"],
    ["0:15", "00:15"],
    ["23:59", "23:59"],
    ["noon", "12:00"],
    ["Noon", "12:00"],
    ["midnight", "00:00"],
    ["12", "12:00"],
  ])("reads %s as %s", (input, expected) => {
    expect(parseLooseTime(input)).toBe(expected);
  });

  it("reads bare 1-6 as afternoon and 7-11 as morning", () => {
    expect(parseLooseTime("5:30")).toBe("17:30");
    expect(parseLooseTime("530")).toBe("17:30");
    expect(parseLooseTime("6")).toBe("18:00");
    expect(parseLooseTime("1:00")).toBe("13:00");
    expect(parseLooseTime("7:00")).toBe("07:00");
    expect(parseLooseTime("11:30")).toBe("11:30");
  });

  it.each(["", "  ", "abc", "13p", "0p", "5:60", "24:00", "25", "5:3", "5:300", "10 to 5"])(
    "rejects %j",
    (input) => {
      expect(parseLooseTime(input)).toBeNull();
    },
  );
});

describe("formatting", () => {
  it("formats 24-hour times for display", () => {
    expect(formatTime("17:30")).toBe("5:30 PM");
    expect(formatTime("00:05")).toBe("12:05 AM");
    expect(formatTime("12:00")).toBe("12:00 PM");
    expect(formatTime(null)).toBe("");
    expect(formatTime("")).toBe("");
  });

  it("round-trips through the parser", () => {
    for (const t of ["00:00", "07:15", "12:00", "12:45", "13:05", "23:59"]) {
      expect(parseLooseTime(formatTime(t))).toBe(t);
    }
  });

  it("counts minutes and durations", () => {
    expect(minutesOf("01:30")).toBe(90);
    expect(minutesOf("1:30")).toBeNull();
    expect(formatDuration(125)).toBe("2:05");
  });
});
