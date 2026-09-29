/**
 * Pin clustering for the church map.
 *
 * Whether the map clusters at all is decided by the zoom alone. At
 * `CLUSTER_MAX_ZOOM` and every zoom further out, every church is drawn inside
 * a numbered roundel — a church with no neighbours near it gets a roundel of
 * its own, marked 1 — and from `PIN_ZOOM` in every church has its own pin.
 * One rule for the whole map reads better than pins and roundels mixed by
 * how crowded each patch of it happens to be.
 *
 * Which churches share a roundel is decided by how close they are. The
 * algorithm is the one supercluster uses — greedy, hierarchical, built once
 * from the closest zoom outwards — with one change: the merge radius depends
 * on the zoom.
 *
 * - Greedy: at each zoom, take the biggest group not yet placed and absorb
 *   every other group within the radius of it.
 * - Hierarchical: each zoom clusters the groups of the zoom one step closer
 *   in, so a roundel at zoom z is always a union of what's drawn at z + 1.
 *   Zooming in only ever splits a roundel; it never regroups its churches
 *   with others.
 * - Radius by zoom: a little over one roundel wide at the cutoff, so only
 *   roundels that would overlap are merged, and wider in a state-sized view,
 *   where small roundels would otherwise pile up on each other.
 */

/**
 * The last zoom that clusters: here and further out, every church is in a
 * roundel. Zoom 10 takes in a few counties. The default view (zoom 11) and a
 * place search (zoom 12) are closer in, so they open on pins.
 */
export const CLUSTER_MAX_ZOOM = 10;

/** The first zoom at which every church has a pin of its own. */
export const PIN_ZOOM = CLUSTER_MAX_ZOOM + 1;

/**
 * How close, in screen pixels, two groups must be at `zoom` to share a
 * roundel. A small roundel is 28–32 px across, so at the cutoff the radius
 * leaves a few pixels between the ones it keeps apart. Each step out adds a
 * few more.
 */
export function clusterRadiusPx(zoom: number): number {
  return Math.min(60, 40 + (CLUSTER_MAX_ZOOM - zoom) * 6);
}

/** Leaflet's tile size: a zoom-z world is `TILE_SIZE * 2^z` pixels wide. */
const TILE_SIZE = 256;

/** `[west, south, east, north]`, in degrees. */
export type BBox = [number, number, number, number];

export interface ClusterablePoint {
  id: number;
  latitude: number;
  longitude: number;
}

export interface MapPoint<T> {
  kind: "point";
  item: T;
}

export interface MapCluster {
  kind: "cluster";
  /** Unique within one index, and the same at every zoom the roundel spans. */
  id: number;
  lat: number;
  lng: number;
  count: number;
}

export type MapEntry<T> = MapPoint<T> | MapCluster;

export interface ClusterIndex<T extends ClusterablePoint> {
  /**
   * What to draw in `bbox` at `zoom`: only roundels up to `CLUSTER_MAX_ZOOM`,
   * only churches from `PIN_ZOOM`.
   */
  entries(bbox: BBox, zoom: number): MapEntry<T>[];
  /** Every church inside a roundel. */
  leaves(clusterId: number): T[];
  /**
   * The zoom at which a roundel splits, or, for a roundel of one, becomes a
   * pin.
   */
  expansionZoom(clusterId: number): number;
  /**
   * The lowest zoom at which this church has a pin of its own (`PIN_ZOOM`),
   * or `null` if it isn't in the index (filtered out, or without
   * coordinates).
   */
  soloZoom(itemId: number): number | null;
}

/** One church, or a roundel of them, at some zoom. */
interface Group<T> {
  /** Web Mercator, in world fractions: [0, 1] west→east and north→south. */
  x: number;
  y: number;
  count: number;
  /** The church, at `PIN_ZOOM`, where every group is one pin. */
  item: T | null;
  /** A roundel's entry, at every zoom that clusters; its `id` keys its React
   *  marker. */
  cluster: MapCluster | null;
  /** The groups one zoom closer in that merged into this roundel. */
  children: Group<T>[];
  /** Where the input put this group, to break ties the same way each time. */
  order: number;
}

export function buildClusterIndex<T extends ClusterablePoint>(
  items: readonly T[],
): ClusterIndex<T> {
  const clusters = new Map<number, { group: Group<T>; zoom: number }>();
  const ids = new Set(items.map((item) => item.id));

  // levels[z] is what is drawn at zoom z.
  const levels: Group<T>[][] = [];
  let level: Group<T>[] = items.map((item, order) => ({
    x: lngToX(item.longitude),
    y: latToY(item.latitude),
    count: 1,
    item,
    cluster: null,
    children: [],
    order,
  }));
  levels[PIN_ZOOM] = level;

  for (let zoom = CLUSTER_MAX_ZOOM; zoom >= 0; zoom--) {
    level = mergeLevel(level, zoom, (group) => {
      clusters.set(group.cluster!.id, { group, zoom });
    });
    levels[zoom] = level;
  }

  return {
    entries(bbox, zoom) {
      const z = Math.min(Math.max(Math.floor(zoom), 0), PIN_ZOOM);
      const [west, south, east, north] = bbox;
      const allLngs = east - west >= 360;
      const entries: MapEntry<T>[] = [];
      for (const group of levels[z]) {
        const lat = group.cluster ? group.cluster.lat : group.item!.latitude;
        const lng = group.cluster ? group.cluster.lng : group.item!.longitude;
        if (lat < south || lat > north) continue;
        if (!allLngs && (lng < west || lng > east)) continue;
        entries.push(group.cluster ?? { kind: "point", item: group.item! });
      }
      return entries;
    },

    leaves(clusterId) {
      const found = clusters.get(clusterId);
      const out: T[] = [];
      const collect = (group: Group<T>) => {
        if (group.item) out.push(group.item);
        else group.children.forEach(collect);
      };
      if (found) collect(found.group);
      return out;
    },

    expansionZoom(clusterId) {
      const found = clusters.get(clusterId);
      return found ? found.zoom + 1 : PIN_ZOOM;
    },

    soloZoom(itemId) {
      return ids.has(itemId) ? PIN_ZOOM : null;
    },
  };
}

// Ids only need to be unique within an index, but a module-wide counter
// also keeps a rebuilt index (after a filter change) from reusing a React
// key for a roundel with different churches in it.
let nextClusterId = 1;

/**
 * Cluster one zoom's groups into the next zoom out. Groups are bucketed into
 * a grid of radius-sized cells, so each one only checks the 3 × 3 cells
 * around it. Every group that comes out is a roundel: at the cutoff, a
 * church with nothing near it becomes a roundel of one.
 */
function mergeLevel<T>(
  groups: readonly Group<T>[],
  zoom: number,
  onCreate: (group: Group<T>) => void,
): Group<T>[] {
  const radius = clusterRadiusPx(zoom) / (TILE_SIZE * 2 ** zoom);
  const radiusSq = radius * radius;
  // A world is under 2^24 cells across at any zoom this runs at, so a cell's
  // column and row pack losslessly into one number.
  const columns = 2 ** 24;
  const cellOf = (value: number) => Math.floor(value / radius);
  const grid = new Map<number, number[]>();
  groups.forEach((group, i) => {
    const key = cellOf(group.x) * columns + cellOf(group.y);
    const cell = grid.get(key);
    if (cell) cell.push(i);
    else grid.set(key, [i]);
  });

  // Biggest first, so a city's roundel draws in its outlying churches
  // rather than a suburb's pair drawing in part of the city.
  const seeds = groups
    .map((_, i) => i)
    .sort(
      (a, b) =>
        groups[b].count - groups[a].count || groups[a].order - groups[b].order,
    );
  const placed = new Uint8Array(groups.length);
  const out: Group<T>[] = [];
  for (const s of seeds) {
    if (placed[s]) continue;
    placed[s] = 1;
    const seed = groups[s];
    const members = [seed];
    const cx = cellOf(seed.x);
    const cy = cellOf(seed.y);
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        const cell = grid.get((cx + dx) * columns + (cy + dy));
        if (!cell) continue;
        for (const o of cell) {
          if (placed[o]) continue;
          const other = groups[o];
          const ddx = other.x - seed.x;
          const ddy = other.y - seed.y;
          if (ddx * ddx + ddy * ddy > radiusSq) continue;
          placed[o] = 1;
          members.push(other);
        }
      }
    }
    // A roundel that absorbed nothing is the same roundel one zoom out, so
    // it keeps its id (and its marker) and splits at the same zoom.
    if (members.length === 1 && seed.cluster) {
      out.push(seed);
      continue;
    }

    let count = 0;
    let x = 0;
    let y = 0;
    for (const member of members) {
      count += member.count;
      x += member.x * member.count;
      y += member.y * member.count;
    }
    x /= count;
    y /= count;
    const group: Group<T> = {
      x,
      y,
      count,
      item: null,
      cluster: {
        kind: "cluster",
        id: nextClusterId++,
        lat: yToLat(y),
        lng: xToLng(x),
        count,
      },
      children: members,
      order: Math.min(...members.map((member) => member.order)),
    };
    onCreate(group);
    out.push(group);
  }
  return out;
}

function lngToX(lng: number): number {
  return lng / 360 + 0.5;
}

function xToLng(x: number): number {
  return (x - 0.5) * 360;
}

function latToY(lat: number): number {
  const sin = Math.sin((Math.max(-85, Math.min(85, lat)) * Math.PI) / 180);
  return 0.5 - Math.log((1 + sin) / (1 - sin)) / (4 * Math.PI);
}

function yToLat(y: number): number {
  const n = (0.5 - y) * 2 * Math.PI;
  return (Math.atan(Math.sinh(n)) * 180) / Math.PI;
}

/**
 * The convex hull of some `[lat, lng]` points, counter-clockwise (Andrew's
 * monotone chain). Drawn under a hovered roundel to show the ground it
 * covers; flat lat/lng is fine at the scale of a cluster.
 */
export function convexHull(
  points: readonly [number, number][],
): [number, number][] {
  const sorted = [...points].sort((a, b) => a[1] - b[1] || a[0] - b[0]);
  if (sorted.length <= 2) return sorted;
  const cross = (
    o: [number, number],
    a: [number, number],
    b: [number, number],
  ) => (a[1] - o[1]) * (b[0] - o[0]) - (a[0] - o[0]) * (b[1] - o[1]);
  const half = (pts: [number, number][]) => {
    const hull: [number, number][] = [];
    for (const p of pts) {
      while (
        hull.length >= 2 &&
        cross(hull[hull.length - 2], hull[hull.length - 1], p) <= 0
      ) {
        hull.pop();
      }
      hull.push(p);
    }
    hull.pop();
    return hull;
  };
  const lower = half(sorted);
  const upper = half([...sorted].reverse());
  return [...lower, ...upper];
}
