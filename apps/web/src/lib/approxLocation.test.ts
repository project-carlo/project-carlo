import { describe, expect, it } from "vitest";
import {
  COVERAGE_RADIUS_MILES,
  IP_GUESS_KEY,
  LAST_PLACE_KEY,
  cacheGuess,
  geoEndpoint,
  inCoverageBox,
  isInCoverage,
  labelForGuess,
  locationFromGuess,
  parseGeoGuess,
  parseLastPlace,
  readCachedGuess,
  readLastPlace,
  rememberPlace,
  resolveApproxLocation,
  saveLastPlace,
  type GeoGuess,
} from "./approxLocation";

class MemoryStorage implements Storage {
  private map = new Map<string, string>();
  get length() {
    return this.map.size;
  }
  clear() {
    this.map.clear();
  }
  getItem(key: string) {
    return this.map.get(key) ?? null;
  }
  key(index: number) {
    return [...this.map.keys()][index] ?? null;
  }
  removeItem(key: string) {
    this.map.delete(key);
  }
  setItem(key: string, value: string) {
    this.map.set(key, value);
  }
}

const throwingStorage = {
  getItem() {
    throw new Error("blocked");
  },
  setItem() {
    throw new Error("blocked");
  },
} as unknown as Storage;

const ROCHESTER = { lat: 43.1566, lng: -77.6088 };
const COLUMBUS = { lat: 39.9612, lng: -82.9988 };

function guess(overrides: Partial<GeoGuess> = {}): GeoGuess {
  return {
    city: "Rochester",
    region: "New York",
    regionCode: "NY",
    country: "US",
    postalCode: "14604",
    lat: ROCHESTER.lat,
    lng: ROCHESTER.lng,
    timezone: "America/New_York",
    source: "ip",
    ...overrides,
  };
}

describe("last place", () => {
  it("round-trips through storage", () => {
    const storage = new MemoryStorage();
    expect(readLastPlace(storage)).toBeNull();
    saveLastPlace(
      { ...ROCHESTER, label: "Rochester", source: "search" },
      storage,
      1234,
    );
    expect(JSON.parse(storage.getItem(LAST_PLACE_KEY)!)).toEqual({
      lat: 43.1566,
      lng: -77.6088,
      label: "Rochester",
      source: "search",
      savedAt: 1234,
    });
    expect(readLastPlace(storage)).toMatchObject({
      label: "Rochester",
      source: "search",
      savedAt: 1234,
    });
  });

  it("rejects malformed values", () => {
    expect(parseLastPlace(null)).toBeNull();
    expect(parseLastPlace("x")).toBeNull();
    expect(
      parseLastPlace({ lat: 91, lng: 0, label: "x", source: "search" }),
    ).toBeNull();
    expect(
      parseLastPlace({ lat: 1, lng: 1, label: "", source: "search" }),
    ).toBeNull();
    expect(
      parseLastPlace({ lat: 1, lng: 1, label: "x", source: "ip" }),
    ).toBeNull();
    const storage = new MemoryStorage();
    storage.setItem(LAST_PLACE_KEY, "{not json");
    expect(readLastPlace(storage)).toBeNull();
  });

  it("never throws when storage is unavailable", () => {
    expect(readLastPlace(throwingStorage)).toBeNull();
    expect(() =>
      saveLastPlace({ ...ROCHESTER, label: "x", source: "device" }, throwingStorage),
    ).not.toThrow();
    expect(readLastPlace(null)).toBeNull();
    expect(() =>
      saveLastPlace({ ...ROCHESTER, label: "x", source: "device" }, null),
    ).not.toThrow();
  });

  it("rememberPlace is safe without a browser", () => {
    expect(() =>
      rememberPlace({ id: "p1", title: "Corning", lat: 42.14, lng: -77.05 }),
    ).not.toThrow();
  });
});

describe("IP guess", () => {
  it("labels with city and state, falling back gracefully", () => {
    expect(labelForGuess(guess())).toBe("Rochester, NY");
    expect(labelForGuess(guess({ regionCode: null }))).toBe("Rochester, New York");
    expect(labelForGuess(guess({ city: null }))).toBe("New York");
    expect(labelForGuess(guess({ city: null, region: null }))).toBe("your area");
    expect(labelForGuess(guess({ regionCode: null, region: null }))).toBe(
      "Rochester",
    );
  });

  it("needs coordinates to count as a location", () => {
    expect(locationFromGuess(null)).toBeNull();
    expect(locationFromGuess(guess({ lat: null }))).toBeNull();
    expect(locationFromGuess(guess())).toEqual({
      ...ROCHESTER,
      label: "Rochester, NY",
      source: "ip",
    });
  });

  it("parses the Worker's JSON defensively", () => {
    expect(parseGeoGuess(undefined)).toBeNull();
    expect(parseGeoGuess({ city: 5, lat: "43", lng: NaN })).toMatchObject({
      city: null,
      lat: null,
      lng: null,
    });
  });

  it("caches positive and negative results for the session", () => {
    const storage = new MemoryStorage();
    expect(readCachedGuess(storage)).toBeNull();
    cacheGuess(null, storage);
    expect(readCachedGuess(storage)).toEqual({ guess: null });
    cacheGuess(guess(), storage);
    expect(readCachedGuess(storage)?.guess?.city).toBe("Rochester");
    storage.setItem(IP_GUESS_KEY, "garbage");
    expect(readCachedGuess(storage)).toBeNull();
    expect(readCachedGuess(throwingStorage)).toBeNull();
  });

  it("passes ?geo= through as ?mock= on localhost only", () => {
    expect(geoEndpoint({ hostname: "localhost", search: "?geo=rochester" })).toBe(
      "/api/geo?mock=rochester",
    );
    expect(geoEndpoint({ hostname: "127.0.0.1", search: "?geo=columbus" })).toBe(
      "/api/geo?mock=columbus",
    );
    expect(geoEndpoint({ hostname: "localhost", search: "" })).toBe("/api/geo");
    expect(
      geoEndpoint({ hostname: "projectcarlo.org", search: "?geo=rochester" }),
    ).toBe("/api/geo");
    expect(geoEndpoint(null)).toBe("/api/geo");
  });
});

describe("resolveApproxLocation", () => {
  const last = {
    lat: 42.14,
    lng: -77.05,
    label: "Corning",
    source: "search" as const,
    savedAt: 1,
  };

  it("prefers the last chosen place over the IP guess", () => {
    expect(resolveApproxLocation(last, guess())).toEqual({
      lat: 42.14,
      lng: -77.05,
      label: "Corning",
      source: "search",
    });
  });

  it("falls back to the IP guess, then to nothing", () => {
    expect(resolveApproxLocation(null, guess())?.source).toBe("ip");
    expect(resolveApproxLocation(null, null)).toBeNull();
    expect(resolveApproxLocation(null, guess({ lat: null, lng: null }))).toBeNull();
  });
});

describe("coverage", () => {
  const churches = [
    { id: 1, latitude: 43.16, longitude: -77.61 },
    { id: 2, latitude: 42.89, longitude: -78.88 },
    { id: 3, latitude: null, longitude: null },
  ];

  it("rules out far places with the coarse box", () => {
    expect(inCoverageBox(ROCHESTER)).toBe(true);
    expect(inCoverageBox(COLUMBUS)).toBe(false);
    expect(isInCoverage(COLUMBUS)).toBe(false);
    expect(isInCoverage(ROCHESTER)).toBe(true);
  });

  it("uses the nearest church when the snapshot is loaded", () => {
    expect(isInCoverage(ROCHESTER, churches)).toBe(true);
    // Inside the box, but 40+ miles from every church.
    const remote = { lat: 43.97, lng: -74.17 };
    expect(inCoverageBox(remote)).toBe(true);
    expect(isInCoverage(remote, churches)).toBe(false);
    expect(isInCoverage(remote, churches, 400)).toBe(true);
    expect(COVERAGE_RADIUS_MILES).toBe(40);
  });

  it("ignores churches without coordinates", () => {
    expect(isInCoverage(ROCHESTER, [churches[2]])).toBe(false);
  });
});
