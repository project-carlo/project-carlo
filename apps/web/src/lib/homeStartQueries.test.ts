import { describe, expect, it } from "vitest";
import { isFirstVisitStart } from "./homeStartQueries";

describe("isFirstVisitStart", () => {
  it("is a first visit with no view and no handed-over church", () => {
    expect(isFirstVisitStart("", null)).toBe(true);
    expect(isFirstVisitStart("?day=sun", undefined)).toBe(true);
    expect(isFirstVisitStart("", {})).toBe(true);
  });

  it("is not when the URL carries a view", () => {
    expect(isFirstVisitStart("?lat=43.15&lng=-77.6&z=10", null)).toBe(false);
  });

  it("is not when the landing page hands over a church to fly to", () => {
    expect(
      isFirstVisitStart("", { centerOn: { lat: 43.15, lng: -77.6 } }),
    ).toBe(false);
  });

  it("treats an empty centerOn as nothing handed over, as HomePage did", () => {
    expect(isFirstVisitStart("", { centerOn: null })).toBe(true);
    expect(isFirstVisitStart("", { centerOn: 0 })).toBe(true);
  });
});
