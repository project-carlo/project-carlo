import { describe, expect, it } from "vitest";
import { wantsCurrentLocation } from "./currentLocationQuery";

describe("wantsCurrentLocation", () => {
  it("is the default on an empty field", () => {
    expect(wantsCurrentLocation("")).toBe(true);
    expect(wantsCurrentLocation("   ")).toBe(true);
  });

  it("drops out once the user types an ordinary place", () => {
    expect(wantsCurrentLocation("r")).toBe(false);
    expect(wantsCurrentLocation("ro")).toBe(false);
    expect(wantsCurrentLocation("Rochester")).toBe(false);
    expect(wantsCurrentLocation("14607")).toBe(false);
    expect(wantsCurrentLocation("Locust St")).toBe(false);
  });

  it("stays for queries that are asking for the user's location", () => {
    expect(wantsCurrentLocation("cur")).toBe(true);
    expect(wantsCurrentLocation("Current Loc")).toBe(true);
    expect(wantsCurrentLocation("near me")).toBe(true);
    expect(wantsCurrentLocation("my  loc")).toBe(true);
    expect(wantsCurrentLocation("nearby")).toBe(true);
  });
});
