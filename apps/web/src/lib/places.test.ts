import { describe, expect, it } from "vitest";
import {
  CITY_PAGE_MIN_CHURCHES,
  churchPath,
  cityHasPage,
  cityPath,
  citySlug,
  citiesWithAtLeast,
  dioceseChurchCounts,
  dioceseKeyForChurch,
  diocesePath,
  dioceses,
  groupChurchesByCity,
  haversineMiles,
  nearestChurches,
  placesCities,
  statePath,
} from "./places";

type TestChurch = {
  id: number;
  slug: string;
  city: string | null;
  state: string | null;
  latitude: number | null;
  longitude: number | null;
};

function church(
  id: number,
  city: string | null,
  lat: number | null = null,
  lng: number | null = null,
  state: string | null = "NY",
): TestChurch {
  return { id, slug: `c${id}`, city, state, latitude: lat, longitude: lng };
}

describe("citySlug and paths", () => {
  it("slugifies city names", () => {
    expect(citySlug("Niagara Falls")).toBe("niagara-falls");
    expect(citySlug("St. Johnsville")).toBe("st-johnsville");
    expect(citySlug("  O'Brien   Heights ")).toBe("obrien-heights");
    expect(citySlug("Cañon")).toBe("canon");
  });

  it("builds site paths", () => {
    expect(statePath("NY")).toBe("/mass-times/ny/");
    expect(cityPath("NY", "Niagara Falls")).toBe("/mass-times/ny/niagara-falls/");
    expect(diocesePath("rochester")).toBe("/dioceses/rochester/");
    expect(churchPath("st-marys-corning")).toBe("/churches/st-marys-corning/");
  });
});

describe("diocese data", () => {
  it("lists dioceses with names and descriptions", () => {
    const list = dioceses();
    const rochester = list.find((d) => d.key === "rochester");
    expect(rochester?.shortName).toBe("Diocese of Rochester");
    expect(rochester?.state).toBe("NY");
    expect(list.find((d) => d.key === "new-york")?.shortName).toBe(
      "Archdiocese of New York",
    );
    expect(list.every((d) => d.name && d.shortName)).toBe(true);
  });

  it("maps churches to dioceses", () => {
    expect(dioceseKeyForChurch("st-marys-corning")).toBe("rochester");
    expect(dioceseKeyForChurch("no-such-church")).toBeNull();
  });

  it("counts churches per diocese", () => {
    const counts = dioceseChurchCounts();
    expect(counts.rochester).toBeGreaterThan(0);
  });

  it("exposes multi-church cities from the generated data", () => {
    const cities = placesCities(3);
    expect(cities.length).toBeGreaterThan(0);
    expect(cities.every((c) => c.count >= 3)).toBe(true);
    expect(placesCities().length).toBeGreaterThanOrEqual(cities.length);
  });
});

describe("city grouping", () => {
  const churches = [
    church(1, "Niagara Falls"),
    church(2, "niagara falls"),
    church(3, "Niagara Falls"),
    church(4, "Lockport"),
    church(5, "Lockport"),
    church(6, "Albion"),
    church(7, null),
    church(8, "Albion", null, null, null),
  ];

  it("groups by city, merging spelling variants and skipping unknowns", () => {
    const groups = groupChurchesByCity(churches);
    expect(groups.map((g) => g.city)).toEqual([
      "Lockport",
      "Niagara Falls",
      "Albion",
    ].sort());
    const niagara = groups.find((g) => g.slug === "niagara-falls")!;
    expect(niagara.churches).toHaveLength(3);
    expect(niagara.city).toBe("Niagara Falls");
    expect(niagara.path).toBe("/mass-times/ny/niagara-falls/");
    expect(groups.find((g) => g.slug === "albion")!.churches).toHaveLength(1);
  });

  it("filters to cities with enough churches, largest first", () => {
    expect(citiesWithAtLeast(churches, 2).map((g) => g.slug)).toEqual([
      "niagara-falls",
      "lockport",
    ]);
    expect(citiesWithAtLeast(churches, 3).map((g) => g.slug)).toEqual([
      "niagara-falls",
    ]);
  });

  it("knows which cities get a page", () => {
    expect(CITY_PAGE_MIN_CHURCHES).toBe(2);
    expect(cityHasPage(churches, "NY", "Niagara Falls")).toBe(true);
    expect(cityHasPage(churches, "ny", "lockport")).toBe(true);
    expect(cityHasPage(churches, "NY", "Albion")).toBe(false);
    expect(cityHasPage(churches, "NY", "Nowhere")).toBe(false);
  });
});

describe("distance", () => {
  const rochester = { lat: 43.1566, lng: -77.6088 };
  const buffalo = { lat: 42.8864, lng: -78.8784 };

  it("computes great-circle miles", () => {
    expect(haversineMiles(rochester, rochester)).toBe(0);
    expect(haversineMiles(rochester, buffalo)).toBeGreaterThan(65);
    expect(haversineMiles(rochester, buffalo)).toBeLessThan(69);
    expect(haversineMiles(rochester, buffalo)).toBeCloseTo(
      haversineMiles(buffalo, rochester),
      6,
    );
  });

  it("finds the nearest geocoded churches, nearest first", () => {
    const list = [
      church(1, "A", 43.16, -77.61),
      church(2, "B", 42.89, -78.88),
      church(3, "C", 43.2, -77.5),
      church(4, "D", null, null),
      church(5, "E", 43.15, -77.6),
    ];
    const near = nearestChurches(list, rochester, 3);
    expect(near.map((n) => n.church.id)).toEqual([1, 5, 3]);
    expect(near[0].distanceMiles).toBeLessThan(near[1].distanceMiles);
    expect(nearestChurches(list, rochester, 2, 5).map((n) => n.church.id)).toEqual([
      1, 3,
    ]);
    expect(nearestChurches(list, rochester, 0)).toEqual([]);
  });
});
