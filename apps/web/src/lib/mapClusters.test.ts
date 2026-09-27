import { describe, expect, it } from "vitest";
import {
  buildClusterIndex,
  CLUSTER_MAX_ZOOM,
  clusterRadiusPx,
  convexHull,
  PIN_ZOOM,
  type BBox,
  type ClusterablePoint,
  type MapEntry,
} from "./mapClusters";

const WORLD: BBox = [-180, -90, 180, 90];

/** A deterministic scatter over upstate New York, dense in two "cities". */
function scatter(count: number): ClusterablePoint[] {
  let seed = 7;
  const random = () => {
    seed = (seed * 16807) % 2147483647;
    return seed / 2147483647;
  };
  return Array.from({ length: count }, (_, id) => {
    const city = id % 3;
    if (city === 0) {
      return {
        id,
        latitude: 42 + random() * 1.3,
        longitude: -79.5 + random() * 4,
      };
    }
    const [lat, lng] = city === 1 ? [43.16, -77.61] : [42.89, -78.85];
    return {
      id,
      latitude: lat + (random() - 0.5) * 0.12,
      longitude: lng + (random() - 0.5) * 0.16,
    };
  });
}

function leafIds(
  index: ReturnType<typeof buildClusterIndex<ClusterablePoint>>,
  entry: MapEntry<ClusterablePoint>,
): number[] {
  return entry.kind === "point"
    ? [entry.item.id]
    : index.leaves(entry.id).map((item) => item.id);
}

describe("buildClusterIndex", () => {
  const points = scatter(300);
  const index = buildClusterIndex(points);

  it("accounts for every church exactly once at every zoom", () => {
    for (let zoom = 0; zoom <= PIN_ZOOM + 2; zoom++) {
      const ids = index
        .entries(WORLD, zoom)
        .flatMap((entry) => leafIds(index, entry))
        .sort((a, b) => a - b);
      expect(ids).toEqual(points.map((point) => point.id));
    }
  });

  it("gives every church its own pin from the pin zoom in", () => {
    for (const zoom of [PIN_ZOOM, PIN_ZOOM + 3]) {
      const entries = index.entries(WORLD, zoom);
      expect(entries).toHaveLength(points.length);
      expect(entries.every((entry) => entry.kind === "point")).toBe(true);
    }
  });

  it("puts every church in a roundel at the cutoff and further out", () => {
    for (let zoom = 0; zoom <= CLUSTER_MAX_ZOOM; zoom++) {
      const entries = index.entries(WORLD, zoom);
      expect(entries.every((entry) => entry.kind === "cluster")).toBe(true);
    }
    // Some of the countryside churches have no neighbour that close.
    const ones = index
      .entries(WORLD, CLUSTER_MAX_ZOOM)
      .filter((entry) => entry.kind === "cluster" && entry.count === 1);
    expect(ones.length).toBeGreaterThan(0);
  });

  it("clusters more the further out the map is", () => {
    const counts = [];
    for (let zoom = 0; zoom <= PIN_ZOOM; zoom++) {
      counts.push(index.entries(WORLD, zoom).length);
    }
    for (let i = 1; i < counts.length; i++) {
      expect(counts[i]).toBeGreaterThanOrEqual(counts[i - 1]);
    }
    expect(counts[0]).toBeLessThan(10);
  });

  it("only ever splits a roundel when zooming in", () => {
    for (let zoom = 0; zoom <= CLUSTER_MAX_ZOOM; zoom++) {
      const groupOf = new Map<number, number>();
      index.entries(WORLD, zoom).forEach((entry, group) => {
        for (const id of leafIds(index, entry)) groupOf.set(id, group);
      });
      for (const entry of index.entries(WORLD, zoom + 1)) {
        const groups = new Set(
          leafIds(index, entry).map((id) => groupOf.get(id)),
        );
        expect(groups.size).toBe(1);
      }
    }
  });

  it("splits a roundel at its expansion zoom", () => {
    for (let zoom = 0; zoom <= CLUSTER_MAX_ZOOM; zoom++) {
      for (const entry of index.entries(WORLD, zoom)) {
        if (entry.kind !== "cluster") continue;
        const expansion = index.expansionZoom(entry.id);
        expect(expansion).toBeGreaterThan(zoom);
        const leaves = new Set(leafIds(index, entry));
        const pieces = index
          .entries(WORLD, expansion)
          .filter((piece) => leaves.has(leafIds(index, piece)[0]));
        if (entry.count === 1) {
          // A roundel of one can't split; it becomes its church's pin.
          expect(expansion).toBe(PIN_ZOOM);
          expect(pieces.map((piece) => piece.kind)).toEqual(["point"]);
        } else {
          expect(pieces.length).toBeGreaterThan(1);
        }
        // …and it is the same roundel at every zoom until then.
        for (let z = zoom; z < expansion; z++) {
          expect(
            index
              .entries(WORLD, z)
              .some((other) => other.kind === "cluster" && other.id === entry.id),
          ).toBe(true);
        }
      }
    }
  });

  it("reports the pin zoom as the first at which each church stands alone", () => {
    for (const point of points) {
      expect(index.soloZoom(point.id)).toBe(PIN_ZOOM);
      const standsAlone = (zoom: number) =>
        index
          .entries(WORLD, zoom)
          .some((entry) => entry.kind === "point" && entry.item.id === point.id);
      expect(standsAlone(PIN_ZOOM)).toBe(true);
      expect(standsAlone(CLUSTER_MAX_ZOOM)).toBe(false);
    }
    expect(index.soloZoom(-1)).toBeNull();
  });

  it("never merges churches further apart than the radius", () => {
    const far = buildClusterIndex([
      { id: 1, latitude: 43, longitude: -77 },
      { id: 2, latitude: 43, longitude: -76.8 },
    ]);
    // 0.2° of longitude is ~73 px at zoom 9 (256 · 2^9 · 0.2 / 360) and
    // ~36 px at zoom 8.
    expect(clusterRadiusPx(9)).toBeLessThan(73);
    expect(
      far
        .entries(WORLD, 9)
        .map((entry) => (entry.kind === "cluster" ? entry.count : 0)),
    ).toEqual([1, 1]);
    expect(clusterRadiusPx(8)).toBeGreaterThan(36);
    expect(far.entries(WORLD, 8)).toHaveLength(1);
  });

  it("keeps two churches on one corner together until the last zoom", () => {
    const sameCorner = buildClusterIndex([
      { id: 1, latitude: 43.15, longitude: -77.6 },
      { id: 2, latitude: 43.1502, longitude: -77.6001 },
    ]);
    expect(sameCorner.entries(WORLD, CLUSTER_MAX_ZOOM)).toHaveLength(1);
    expect(sameCorner.entries(WORLD, PIN_ZOOM)).toHaveLength(2);
  });

  it("gives a church on its own a roundel of one, the same at every zoom out", () => {
    const lone = buildClusterIndex([{ id: 1, latitude: 43, longitude: -77 }]);
    const [entry] = lone.entries(WORLD, CLUSTER_MAX_ZOOM);
    if (entry.kind !== "cluster") throw new Error("expected a roundel");
    expect(entry.count).toBe(1);
    expect(entry.lat).toBeCloseTo(43, 6);
    expect(entry.lng).toBeCloseTo(-77, 6);
    expect(lone.leaves(entry.id).map((item) => item.id)).toEqual([1]);
    expect(lone.expansionZoom(entry.id)).toBe(PIN_ZOOM);
    expect(lone.entries(WORLD, 0)).toEqual([entry]);
    expect(lone.entries(WORLD, PIN_ZOOM).map((e) => e.kind)).toEqual([
      "point",
    ]);
  });

  it("returns only what falls inside the box", () => {
    const rochester: BBox = [-77.8, 43, -77.4, 43.3];
    const inside = index.entries(rochester, PIN_ZOOM);
    expect(inside.length).toBeGreaterThan(0);
    for (const entry of inside) {
      if (entry.kind !== "point") throw new Error("expected pins only");
      expect(entry.item.longitude).toBeGreaterThanOrEqual(-77.8);
      expect(entry.item.longitude).toBeLessThanOrEqual(-77.4);
      expect(entry.item.latitude).toBeGreaterThanOrEqual(43);
      expect(entry.item.latitude).toBeLessThanOrEqual(43.3);
    }
  });

  it("places a roundel at its churches' centroid", () => {
    const pair = buildClusterIndex([
      { id: 1, latitude: 43, longitude: -77 },
      { id: 2, latitude: 43.002, longitude: -77.002 },
    ]);
    const [entry] = pair.entries(WORLD, 8);
    if (entry.kind !== "cluster") throw new Error("expected a roundel");
    expect(entry.count).toBe(2);
    expect(entry.lat).toBeCloseTo(43.001, 4);
    expect(entry.lng).toBeCloseTo(-77.001, 4);
  });

  it("handles an empty map", () => {
    const empty = buildClusterIndex([]);
    expect(empty.entries(WORLD, 5)).toEqual([]);
  });
});

describe("clusterRadiusPx", () => {
  it("is a little over a roundel wide at the cutoff and wider further out", () => {
    expect(clusterRadiusPx(CLUSTER_MAX_ZOOM)).toBe(40);
    expect(clusterRadiusPx(7)).toBeGreaterThan(clusterRadiusPx(CLUSTER_MAX_ZOOM));
    expect(clusterRadiusPx(0)).toBe(60);
  });
});

describe("convexHull", () => {
  it("drops interior points", () => {
    const hull = convexHull([
      [0, 0],
      [0, 2],
      [2, 2],
      [2, 0],
      [1, 1],
    ]);
    expect(hull).toHaveLength(4);
    expect(hull).not.toContainEqual([1, 1]);
  });

  it("passes one or two points through", () => {
    expect(convexHull([[1, 1]])).toEqual([[1, 1]]);
    expect(convexHull([
      [1, 1],
      [2, 2],
    ])).toHaveLength(2);
  });
});
