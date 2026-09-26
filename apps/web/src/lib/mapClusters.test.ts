import { describe, expect, it } from "vitest";
import {
  INDIVIDUAL_ZOOM,
  clusterChurches,
  clusterRadiusPx,
  zoomToRevealChurch,
  type Clusterable,
  type MapPin,
} from "./mapClusters";

function church(id: number, latitude: number, longitude: number): Clusterable {
  return { id, latitude, longitude };
}

function summary(pins: MapPin<Clusterable>[]): string[] {
  return pins
    .map((pin) =>
      pin.kind === "church" ? `church:${pin.church.id}` : `cluster:${pin.key}`,
    )
    .sort();
}

describe("clusterRadiusPx", () => {
  it("stops clustering once pins would no longer overlap", () => {
    expect(clusterRadiusPx(INDIVIDUAL_ZOOM)).toBeNull();
    expect(clusterRadiusPx(INDIVIDUAL_ZOOM + 2)).toBeNull();
    expect(clusterRadiusPx(13)).toBe(26);
    expect(clusterRadiusPx(11)).toBe(32);
    expect(clusterRadiusPx(8)).toBe(52);
  });

  it("rounds a fractional zoom and keeps low zooms on the regional radius", () => {
    expect(clusterRadiusPx(10.6)).toBe(clusterRadiusPx(11));
    expect(clusterRadiusPx(4)).toBe(clusterRadiusPx(8));
  });
});

describe("clusterChurches", () => {
  const downtown = church(1, 43.15, -77.6);
  // ~1.3 km north of downtown: inside the default-zoom ball, outside the
  // zoom-12 ball (~0.8 km).
  const neighbor = church(2, 43.162, -77.6);
  // A different city, far outside even the regional ball.
  const elsewhere = church(3, 42.89, -78.88);

  it("leaves a single church alone at every zoom", () => {
    expect(clusterChurches([downtown], 8)).toEqual([
      { kind: "church", church: downtown },
    ]);
    expect(clusterChurches([], 11)).toEqual([]);
  });

  it("draws every church on its own at the individual zoom, even coincident ones", () => {
    const twin = church(4, downtown.latitude, downtown.longitude);
    const pins = clusterChurches([downtown, twin], INDIVIDUAL_ZOOM);
    expect(pins.every((pin) => pin.kind === "church")).toBe(true);
    expect(pins).toHaveLength(2);
  });

  it("collapses nearby churches at a city zoom and splits them once they have room", () => {
    const atCity = clusterChurches([downtown, neighbor, elsewhere], 11);
    const cluster = atCity.find((pin) => pin.kind === "cluster");
    expect(cluster).toMatchObject({
      kind: "cluster",
      count: 2,
      key: "1-2",
    });
    expect(atCity.some((pin) => pin.kind === "church" && pin.church.id === 3)).toBe(
      true,
    );

    const closer = clusterChurches([downtown, neighbor], 12);
    expect(closer.every((pin) => pin.kind === "church")).toBe(true);
  });

  it("places a cluster at the average of its churches", () => {
    const pins = clusterChurches([downtown, neighbor], 11);
    const cluster = pins.find((pin) => pin.kind === "cluster");
    expect(cluster).toMatchObject({
      kind: "cluster",
      latitude: (downtown.latitude + neighbor.latitude) / 2,
      longitude: downtown.longitude,
    });
  });

  it("does not chain a corridor of parishes into one diocese-wide pin", () => {
    // Each step is ~1.3 km, inside the zoom-11 radius of its neighbor and
    // outside the radius of the church two steps away.
    const line = Array.from({ length: 6 }, (_, index) =>
      church(index + 1, 43 + index * 0.012, -77.6),
    );
    const pins = clusterChurches(line, 11);
    const clusters = pins.filter((pin) => pin.kind === "cluster");
    expect(clusters).toHaveLength(3);
    expect(clusters.every((pin) => pin.kind === "cluster" && pin.count === 2)).toBe(
      true,
    );
    expect(pins).toHaveLength(3);
  });

  it("is independent of input order", () => {
    const points = [elsewhere, neighbor, downtown];
    expect(summary(clusterChurches(points, 10))).toEqual(
      summary(clusterChurches([...points].reverse(), 10)),
    );
  });

  it("uses fewer markers as the map zooms out over a tight group", () => {
    const block = [
      church(1, 43.15, -77.6),
      church(2, 43.152, -77.602),
      church(3, 43.148, -77.598),
      church(4, 43.151, -77.605),
    ];
    expect(clusterChurches(block, 11)).toHaveLength(1);
    expect(clusterChurches(block, INDIVIDUAL_ZOOM)).toHaveLength(4);
  });
});

describe("zoomToRevealChurch", () => {
  const downtown = church(1, 43.15, -77.6);
  const neighbor = church(2, 43.162, -77.6);

  it("stays put when the church is already its own pin", () => {
    expect(zoomToRevealChurch([downtown, neighbor], downtown.id, 12)).toBe(12);
  });

  it("returns the first zoom that pulls the church out of a cluster", () => {
    const zoom = zoomToRevealChurch([downtown, neighbor], neighbor.id, 9);
    expect(zoom).toBeGreaterThan(9);
    expect(zoom).toBeLessThanOrEqual(INDIVIDUAL_ZOOM);
    expect(
      clusterChurches([downtown, neighbor], zoom).some(
        (pin) => pin.kind === "church" && pin.church.id === neighbor.id,
      ),
    ).toBe(true);
    expect(
      clusterChurches([downtown, neighbor], zoom - 1).some(
        (pin) => pin.kind === "cluster" && pin.churches.some((c) => c.id === neighbor.id),
      ),
    ).toBe(true);
  });

  it("caps a same-point pair at the individual zoom", () => {
    const twin = church(3, downtown.latitude, downtown.longitude);
    expect(zoomToRevealChurch([downtown, twin], twin.id, 11)).toBe(INDIVIDUAL_ZOOM);
  });

  it("ignores an unknown church", () => {
    expect(zoomToRevealChurch([downtown], 99, 10)).toBe(10);
  });
});
