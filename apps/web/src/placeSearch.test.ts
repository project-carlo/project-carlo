import { describe, expect, it } from "vitest";
import {
  canSearchPlaces,
  parsePlaceResults,
  placeSearchParams,
  roundToBiasPrecision,
  type GeoapifyResult,
} from "./placeSearch";

function result(overrides: GeoapifyResult): GeoapifyResult {
  return { lat: 43, lon: -77, result_type: "city", ...overrides };
}

describe("placeSearchParams", () => {
  it("biases toward the point it's given", () => {
    const params = placeSearchParams("Erie", { lat: 40.4, lng: -80 });
    expect(params.get("bias")).toBe("proximity:-80,40.4");
  });

  it("asks for no bias without a point", () => {
    expect(placeSearchParams("Erie", null).has("bias")).toBe(false);
  });

  it("stays in the US", () => {
    expect(placeSearchParams("Erie", null).get("filter")).toBe("countrycode:us");
  });

  it("asks for more than the dropdown lists", () => {
    expect(Number(placeSearchParams("Erie", null).get("limit"))).toBeGreaterThan(5);
  });

  it("looks only for postcodes when given a ZIP", () => {
    expect(placeSearchParams("14620", null).get("type")).toBe("postcode");
    expect(placeSearchParams("Erie", null).has("type")).toBe(false);
  });

  it("trims the query", () => {
    expect(placeSearchParams("  Erie ", null).get("text")).toBe("Erie");
  });
});

describe("parsePlaceResults", () => {
  it("keeps a named building, hospital or cathedral", () => {
    const [place] = parsePlaceResults({
      results: [
        result({
          result_type: "amenity",
          address_line1: "Sacred Heart Cathedral",
          address_line2: "296 Flower City Park, Rochester, NY 14615",
        }),
      ],
    });
    expect(place.title).toBe("Sacred Heart Cathedral");
    expect(place.subtitle).toBe("296 Flower City Park, Rochester, NY 14615");
  });

  it("drops what the map can't go to", () => {
    expect(
      parsePlaceResults({
        results: [
          result({ result_type: "country", address_line1: "United States" }),
          result({ address_line1: "No position", lat: undefined }),
        ],
      }),
    ).toEqual([]);
  });

  it("lists a repeated result once", () => {
    const repeated = result({
      address_line1: "Philadelphia",
      address_line2: "NY 13673",
    });
    expect(
      parsePlaceResults({ results: [repeated, { ...repeated, lat: 44 }] }),
    ).toHaveLength(1);
  });

  it("records the bare name and the state's code", () => {
    const [place] = parsePlaceResults({
      results: [
        result({
          name: "City of Lackawanna",
          address_line1: "City of Lackawanna",
          state_code: "ny",
        }),
      ],
    });
    expect(place.placeName).toBe("lackawanna");
    expect(place.stateCode).toBe("NY");
  });

  it("treats a response with no results as none", () => {
    expect(parsePlaceResults({})).toEqual([]);
  });
});

describe("roundToBiasPrecision", () => {
  it("rounds to a tenth of a degree", () => {
    expect(roundToBiasPrecision({ lat: 43.1566, lng: -77.6088 })).toEqual({
      lat: 43.2,
      lng: -77.6,
    });
  });
});

describe("canSearchPlaces", () => {
  it("waits for three letters, or two digits of a ZIP", () => {
    expect(canSearchPlaces("Ro")).toBe(false);
    expect(canSearchPlaces("Roc")).toBe(true);
    expect(canSearchPlaces("14")).toBe(true);
  });
});
