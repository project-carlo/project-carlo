import { describe, expect, it } from "vitest";
import { churchBounds, firstVisitStart } from "./mapStart";

const BUFFALO = { lat: 42.8864, lng: -78.8784, label: "Buffalo, NY" };
const KANSAS_CITY = { lat: 39.1, lng: -94.58, label: "Kansas City, MO" };

const churches = [
  { latitude: null, longitude: null },
  { latitude: 42.89, longitude: -78.87 }, // Buffalo
  { latitude: 43.16, longitude: -77.61 }, // Rochester
  { latitude: 42.65, longitude: -73.75 }, // Albany
];

describe("churchBounds", () => {
  it("boxes every church with coordinates", () => {
    expect(churchBounds(churches)).toEqual([
      [42.65, -78.87],
      [43.16, -73.75],
    ]);
  });

  it("is null with no mapped church", () => {
    expect(churchBounds([{ latitude: null, longitude: null }])).toBeNull();
    expect(churchBounds([])).toBeNull();
  });
});

describe("firstVisitStart", () => {
  it("starts near an estimate with a church in reach, zoomed out", () => {
    expect(firstVisitStart(BUFFALO, churches, true)).toEqual({
      kind: "near",
      view: { lat: BUFFALO.lat, lng: BUFFALO.lng, zoom: 9 },
    });
    expect(firstVisitStart(BUFFALO, churches, false)).toMatchObject({
      view: { zoom: 8 },
    });
  });

  it("shows the whole covered area for a faraway estimate or none", () => {
    const area = {
      kind: "area",
      bounds: [
        [42.65, -78.87],
        [43.16, -73.75],
      ],
    };
    expect(firstVisitStart(KANSAS_CITY, churches, true)).toEqual(area);
    expect(firstVisitStart(null, churches, true)).toEqual(area);
  });

  it("leaves the map on its default with no mapped church", () => {
    expect(
      firstVisitStart(BUFFALO, [{ latitude: null, longitude: null }], true),
    ).toBeNull();
  });
});
