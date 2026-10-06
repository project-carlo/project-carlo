import { describe, expect, it } from "vitest";
import type { ChurchBase } from "../types";
import {
  buildCityIndex,
  cityPath,
  citySlugFor,
  distanceMiles,
  formatMiles,
  nearbyChurches,
} from "./cities";

function church(overrides: Partial<ChurchBase> & { id: number }): ChurchBase {
  return {
    parish_id: 1,
    slug: `church-${overrides.id}`,
    name: `Church ${overrides.id}`,
    address_line1: null,
    address_line2: null,
    city: null,
    state: "NY",
    postal_code: null,
    latitude: null,
    longitude: null,
    ...overrides,
  };
}

describe("citySlugFor", () => {
  it("joins city and state into a URL slug", () => {
    expect(citySlugFor({ city: "East Aurora", state: "NY" })).toBe("east-aurora-ny");
    expect(citySlugFor({ city: " St. Johnsville ", state: "NY" })).toBe("st-johnsville-ny");
    expect(citySlugFor({ city: "Coeur d'Alène", state: "ID" })).toBe("coeur-dalene-id");
  });

  it("leaves the state off when it's unknown, and returns null without a city", () => {
    expect(citySlugFor({ city: "Buffalo", state: null })).toBe("buffalo");
    expect(citySlugFor({ city: "  ", state: "NY" })).toBeNull();
    expect(citySlugFor({ city: null, state: "NY" })).toBeNull();
  });

  it("builds the page path", () => {
    expect(cityPath("east-aurora-ny")).toBe("/mass-times/east-aurora-ny/");
  });
});

describe("buildCityIndex", () => {
  const churches = [
    church({ id: 1, name: "St. Mary", city: "Buffalo", latitude: 42.9, longitude: -78.9 }),
    church({ id: 2, name: "Holy Cross", city: "Buffalo", latitude: 42.8, longitude: -78.7 }),
    church({ id: 3, name: "St. Joseph", city: "buffalo" }),
    church({ id: 4, name: "Immaculate Conception", city: "East Aurora" }),
    church({ id: 5, name: "Nowhere" }),
  ];
  const index = buildCityIndex(churches);

  it("groups churches by city slug, sorted by label, skipping churches without a city", () => {
    expect(index.cities.map((c) => c.slug)).toEqual(["buffalo-ny", "east-aurora-ny"]);
    expect(index.bySlug.get("buffalo-ny")!.churches.map((c) => c.id)).toEqual([2, 3, 1]);
  });

  it("names the city by its commonest spelling", () => {
    expect(index.bySlug.get("buffalo-ny")).toMatchObject({
      name: "Buffalo",
      state: "NY",
      label: "Buffalo, NY",
    });
  });

  it("centers the city on its geocoded churches", () => {
    const center = index.bySlug.get("buffalo-ny")!.center!;
    expect(center.lat).toBeCloseTo(42.85);
    expect(center.lng).toBeCloseTo(-78.8);
    expect(index.bySlug.get("east-aurora-ny")!.center).toBeNull();
  });
});

describe("nearbyChurches", () => {
  const home = church({ id: 1, city: "East Aurora", latitude: 42.77, longitude: -78.61 });
  const near = church({ id: 2, city: "Elma", latitude: 42.83, longitude: -78.64 });
  const nearer = church({ id: 3, city: "West Falls", latitude: 42.71, longitude: -78.67 });
  const far = church({ id: 4, city: "Rochester", latitude: 43.16, longitude: -77.61 });
  const unplaced = church({ id: 5, city: "Aurora" });
  const all = [home, near, nearer, far, unplaced];
  const city = buildCityIndex(all).bySlug.get("east-aurora-ny")!;

  it("lists geocoded churches outside the city, nearest first, within the limit and range", () => {
    const nearby = nearbyChurches(city, all);
    expect(nearby.map((n) => n.church.id)).toEqual([2, 3]);
    expect(nearby[0].distanceMiles).toBeLessThan(nearby[1].distanceMiles);
    expect(nearbyChurches(city, all, 1).map((n) => n.church.id)).toEqual([2]);
    expect(nearbyChurches(city, all, 10, 1000).map((n) => n.church.id)).toEqual([2, 3, 4]);
  });

  it("returns none for a city with no geocoded church", () => {
    const placeless = buildCityIndex([unplaced]).cities[0];
    expect(nearbyChurches(placeless, all)).toEqual([]);
  });
});

describe("distanceMiles / formatMiles", () => {
  it("measures great-circle miles", () => {
    // Buffalo City Hall to Rochester City Hall is about 67 miles as the crow flies.
    const miles = distanceMiles(
      { lat: 42.8865, lng: -78.8784 },
      { lat: 43.1566, lng: -77.6088 },
    );
    expect(miles).toBeGreaterThan(65);
    expect(miles).toBeLessThan(69);
  });

  it("keeps a decimal under ten miles", () => {
    expect(formatMiles(0.42)).toBe("0.4 mi");
    expect(formatMiles(9.94)).toBe("9.9 mi");
    expect(formatMiles(12.4)).toBe("12 mi");
  });
});
