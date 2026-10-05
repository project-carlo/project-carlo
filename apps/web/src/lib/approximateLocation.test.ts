import { afterEach, describe, expect, it, vi } from "vitest";
import {
  distanceKm,
  fetchApproximateLocation,
  isNearAnyChurch,
  parseApproximateLocation,
} from "./approximateLocation";

const ROCHESTER = { lat: 43.1566, lng: -77.6088 };
const BUFFALO = { lat: 42.8864, lng: -78.8784 };

describe("parseApproximateLocation", () => {
  it("reads a located response, labelled with the region code", () => {
    expect(
      parseApproximateLocation({
        lat: 43.15,
        lng: -77.61,
        city: "Rochester",
        region: "New York",
        regionCode: "NY",
        country: "US",
      }),
    ).toEqual({ lat: 43.15, lng: -77.61, label: "Rochester, NY" });
  });

  it("falls back to the region name, then the city alone", () => {
    expect(
      parseApproximateLocation({
        lat: 51.5,
        lng: -0.12,
        city: "London",
        region: "England",
        regionCode: null,
      })?.label,
    ).toBe("London, England");
    expect(
      parseApproximateLocation({ lat: 1.29, lng: 103.85, city: "Singapore" })
        ?.label,
    ).toBe("Singapore");
  });

  it("ignores a country-level centroid with no city", () => {
    expect(
      parseApproximateLocation({
        lat: 37.751,
        lng: -97.822,
        city: null,
        country: "US",
      }),
    ).toBeNull();
  });

  it("rejects missing or out-of-range coordinates and non-objects", () => {
    expect(parseApproximateLocation({ lat: null, lng: null, city: "X" })).toBeNull();
    expect(parseApproximateLocation({ lat: 91, lng: 0, city: "X" })).toBeNull();
    expect(parseApproximateLocation({ lat: "43", lng: "-77", city: "X" })).toBeNull();
    expect(parseApproximateLocation(null)).toBeNull();
    expect(parseApproximateLocation("<!doctype html>")).toBeNull();
  });
});

describe("distanceKm", () => {
  it("measures Rochester to Buffalo at about 108 km", () => {
    expect(distanceKm(ROCHESTER, BUFFALO)).toBeCloseTo(108, -1);
  });

  it("is zero for the same point", () => {
    expect(distanceKm(ROCHESTER, ROCHESTER)).toBe(0);
  });
});

describe("isNearAnyChurch", () => {
  const churches = [
    { latitude: null, longitude: null },
    { latitude: BUFFALO.lat, longitude: BUFFALO.lng },
  ];

  it("finds a church within range", () => {
    expect(isNearAnyChurch(ROCHESTER, churches, 150)).toBe(true);
  });

  it("is false when every church is out of range", () => {
    expect(isNearAnyChurch(ROCHESTER, churches, 50)).toBe(false);
    // Kansas City, far from any church in a New York-only dataset.
    expect(isNearAnyChurch({ lat: 39.1, lng: -94.58 }, churches)).toBe(false);
  });

  it("is false with no mapped churches", () => {
    expect(isNearAnyChurch(ROCHESTER, [{ latitude: null, longitude: null }])).toBe(
      false,
    );
  });
});

describe("fetchApproximateLocation", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.useRealTimers();
  });

  it("returns the parsed location", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () =>
        Response.json({ lat: 43.15, lng: -77.61, city: "Rochester", regionCode: "NY" }),
      ),
    );
    await expect(fetchApproximateLocation()).resolves.toEqual({
      lat: 43.15,
      lng: -77.61,
      label: "Rochester, NY",
    });
  });

  it("resolves null on an error status or a network failure", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response("", { status: 404 })));
    await expect(fetchApproximateLocation()).resolves.toBeNull();
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => {
        throw new TypeError("Failed to fetch");
      }),
    );
    await expect(fetchApproximateLocation()).resolves.toBeNull();
  });

  it("gives up after its timeout rather than hold the map back", async () => {
    vi.useFakeTimers();
    vi.stubGlobal(
      "fetch",
      vi.fn(
        (_url: string, init: RequestInit) =>
          new Promise((_, reject) => {
            init.signal?.addEventListener("abort", () =>
              reject(new DOMException("Aborted", "AbortError")),
            );
          }),
      ),
    );
    const pending = fetchApproximateLocation();
    await vi.advanceTimersByTimeAsync(5000);
    await expect(pending).resolves.toBeNull();
  });
});
