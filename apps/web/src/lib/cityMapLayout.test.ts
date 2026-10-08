import { describe, expect, it } from "vitest";
import { churchMapMarkers, churchMapView } from "./cityMapLayout";
import { parseCityMapConfig } from "./cityMap";
import { buildClusterIndex } from "./mapClusters";

const church = (id: number, latitude: number, longitude: number) => ({
  id,
  latitude,
  longitude,
});

// Two churches a few blocks apart in Rochester, and one in Buffalo.
const CATHEDRAL = church(1, 43.1566, -77.6088);
const NEIGHBOR = church(2, 43.1601, -77.6052);
const BUFFALO = church(3, 42.8864, -78.8784);

describe("churchMapView", () => {
  it("centers on the church at street level", () => {
    expect(churchMapView(CATHEDRAL)).toEqual({
      lat: CATHEDRAL.latitude,
      lng: CATHEDRAL.longitude,
      zoom: 15,
    });
  });

  it("has no view for a church with no position", () => {
    expect(churchMapView({ latitude: null, longitude: -77.6 })).toBeNull();
  });
});

describe("churchMapMarkers", () => {
  const view = churchMapView(CATHEDRAL)!;
  const at = { id: CATHEDRAL.id, lat: view.lat, lng: view.lng };

  it("marks the church's own pin, among its neighbours' pins", () => {
    const index = buildClusterIndex([CATHEDRAL, NEIGHBOR, BUFFALO]);
    const markers = churchMapMarkers(index, view, at);
    expect(markers).toHaveLength(2);
    expect(markers).toContainEqual({ kind: "pin", ...at, current: true });
    expect(markers).toContainEqual({
      kind: "pin",
      id: NEIGHBOR.id,
      lat: NEIGHBOR.latitude,
      lng: NEIGHBOR.longitude,
    });
  });

  it("adds the church's pin when the map's filters leave it out", () => {
    const index = buildClusterIndex([NEIGHBOR]);
    const markers = churchMapMarkers(index, view, at);
    expect(markers).toHaveLength(2);
    expect(markers.filter((m) => m.kind === "pin" && m.current)).toEqual([
      { kind: "pin", ...at, current: true },
    ]);
  });
});

describe("parseCityMapConfig", () => {
  const view = { lat: 43.1, lng: -77.6, zoom: 15 };

  it("keeps a church page's church", () => {
    expect(
      parseCityMapConfig(JSON.stringify({ label: "St. Mary", view, churchId: 7 })),
    ).toEqual({ label: "St. Mary", view, churchId: 7 });
  });

  it("reads a city page's config without one", () => {
    expect(parseCityMapConfig(JSON.stringify({ label: "Rochester, NY", view }))).toEqual({
      label: "Rochester, NY",
      view,
    });
  });

  it("rejects a church that isn't an id", () => {
    expect(
      parseCityMapConfig(JSON.stringify({ label: "St. Mary", view, churchId: "7" })),
    ).toBeNull();
  });
});
