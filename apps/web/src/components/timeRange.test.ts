import { describe, expect, it } from "vitest";
import { minutesFromPointerDelta, shiftTimeRange } from "./timeRange";

const MIN = 0;
const MAX = 24 * 60;
const STEP = 15;
const FOUR_HOURS = 4 * 60;

describe("shiftTimeRange", () => {
  it("returns the same window when delta is 0", () => {
    expect(shiftTimeRange(480, 720, 0, MIN, MAX, STEP)).toEqual([480, 720]);
  });

  it("slides a 4-hour window later while keeping its width", () => {
    expect(shiftTimeRange(480, 720, 120, MIN, MAX, STEP)).toEqual([600, 840]);
  });

  it("slides a 4-hour window earlier while keeping its width", () => {
    expect(shiftTimeRange(480, 720, -60, MIN, MAX, STEP)).toEqual([420, 660]);
  });

  it("clamps against the end of the day without shrinking", () => {
    // 6pm–10pm dragged far right becomes 8pm–midnight, still 4 hours wide.
    expect(shiftTimeRange(18 * 60, 22 * 60, 10_000, MIN, MAX, STEP)).toEqual([
      MAX - FOUR_HOURS,
      MAX,
    ]);
  });

  it("clamps against midnight without shrinking", () => {
    expect(shiftTimeRange(480, 720, -10_000, MIN, MAX, STEP)).toEqual([
      0,
      FOUR_HOURS,
    ]);
  });

  it("snaps delta to the step grid", () => {
    expect(shiftTimeRange(480, 720, 7, MIN, MAX, STEP)).toEqual([480, 720]);
    expect(shiftTimeRange(480, 720, 8, MIN, MAX, STEP)).toEqual([495, 735]);
    expect(shiftTimeRange(480, 720, -8, MIN, MAX, STEP)).toEqual([465, 705]);
  });

  it("is a no-op when the window already fills the whole day", () => {
    expect(shiftTimeRange(MIN, MAX, 180, MIN, MAX, STEP)).toEqual([MIN, MAX]);
  });

  it("returns the input unchanged when the span is inverted", () => {
    expect(shiftTimeRange(720, 480, 60, MIN, MAX, STEP)).toEqual([720, 480]);
  });
});

describe("minutesFromPointerDelta", () => {
  it("maps a full-track drag to the full day", () => {
    expect(minutesFromPointerDelta(200, 200, MIN, MAX)).toBe(MAX);
  });

  it("maps a half-track drag to 12 hours", () => {
    expect(minutesFromPointerDelta(100, 200, MIN, MAX)).toBe(MAX / 2);
  });

  it("returns 0 for an empty track", () => {
    expect(minutesFromPointerDelta(50, 0, MIN, MAX)).toBe(0);
  });
});
