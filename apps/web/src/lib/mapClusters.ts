/**
 * Group churches that would pile up on the current zoom into one numbered pin.
 *
 * The grouping happens in Web Mercator pixels — the same projection Leaflet
 * draws with — so a cluster means "these pins would overlap on screen," not
 * "these churches share a city." The radius is deliberately small once the
 * map is at a city zoom: only churches that still sit on top of each other
 * collapse, and by zoom 14 every church is its own pin. Zoomed-out views use
 * a modestly larger radius so a downtown reads as a count instead of a
 * hundred markers.
 *
 * Each group is a ball around a seed church, not a chain. Linking every pair
 * within the radius would swallow the whole diocese at a regional zoom,
 * because parishes form a continuous corridor. A ball keeps every member
 * within one radius of the seed, so the numbered pin stays near the churches
 * it stands for. Seeds are visited north-to-south so the grouping depends on
 * geography rather than on the order churches were inserted.
 */

export interface Clusterable {
  id: number;
  latitude: number;
  longitude: number;
}

export type ChurchPin<T extends Clusterable> = {
  kind: "church";
  church: T;
};

export type ClusterPin<T extends Clusterable> = {
  kind: "cluster";
  /** Stable for a given membership, so React can keep the marker mounted while panning. */
  key: string;
  latitude: number;
  longitude: number;
  count: number;
  churches: T[];
};

export type MapPin<T extends Clusterable> = ChurchPin<T> | ClusterPin<T>;

/**
 * At this zoom and above, every church is drawn on its own — including the
 * rare pair that shares one geocode. Past here the pins no longer overlap
 * unless they are the same point, and a same-point pair is still two churches.
 */
export const INDIVIDUAL_ZOOM = 14;

/**
 * Screen-pixel radius of a cluster ball, indexed by zoom. Zooms below 8 share
 * zoom 8's pixel radius, so each step outward still covers twice the ground
 * (the map scale doubles) without a special case. Null is "don't cluster."
 */
const RADIUS_PX_BY_ZOOM: readonly (number | null)[] = [
  52, 52, 52, 52, 52, 52, 52, 52, // 0–7
  52, // 8  ~23 km — a city and its inner suburbs
  42, // 9  ~9 km  — the city holds; nearby towns peel off
  36, // 10 ~4 km  — neighborhoods
  32, // 11 ~1.8 km — the default view; only tight groups
  28, // 12 ~0.8 km
  26, // 13 ~0.4 km — pins that would still overlap
  null, // 14+ every church on its own
];

/** Pixel radius for this zoom, or null when churches are drawn individually. */
export function clusterRadiusPx(zoom: number): number | null {
  const z = Math.round(zoom);
  if (z >= INDIVIDUAL_ZOOM) return null;
  if (z < 0) return RADIUS_PX_BY_ZOOM[0];
  return RADIUS_PX_BY_ZOOM[z] ?? null;
}

/** Leaflet's EPSG:3857 pixel coordinates at an integer zoom. */
function project(latitude: number, longitude: number, zoom: number): [number, number] {
  const world = 256 * 2 ** zoom;
  const x = ((longitude + 180) / 360) * world;
  const lat = Math.max(Math.min(latitude, 85), -85);
  const latRad = (lat * Math.PI) / 180;
  const y =
    (1 - Math.log(Math.tan(latRad) + 1 / Math.cos(latRad)) / Math.PI) / 2 * world;
  return [x, y];
}

function cellKey(x: number, y: number, cell: number): string {
  return `${Math.floor(x / cell)}:${Math.floor(y / cell)}`;
}

/**
 * One pin per church, or one numbered pin per group that would overlap at
 * this zoom. Input order does not matter.
 */
export function clusterChurches<T extends Clusterable>(
  churches: readonly T[],
  zoom: number,
): MapPin<T>[] {
  const radius = clusterRadiusPx(zoom);
  if (radius == null || churches.length <= 1) {
    return churches.map((church) => ({ kind: "church", church }));
  }

  const z = Math.round(zoom);
  const coords = churches.map((church) => project(church.latitude, church.longitude, z));
  const grid = new Map<string, number[]>();
  for (let i = 0; i < churches.length; i++) {
    const [x, y] = coords[i];
    const key = cellKey(x, y, radius);
    const bucket = grid.get(key);
    if (bucket) bucket.push(i);
    else grid.set(key, [i]);
  }

  const used = new Uint8Array(churches.length);
  const order = churches
    .map((_, index) => index)
    .sort((a, b) => {
      const north = churches[b].latitude - churches[a].latitude;
      if (north !== 0) return north;
      const east = churches[a].longitude - churches[b].longitude;
      if (east !== 0) return east;
      return churches[a].id - churches[b].id;
    });

  const radiusSq = radius * radius;
  const pins: MapPin<T>[] = [];

  for (const seed of order) {
    if (used[seed]) continue;
    const [x, y] = coords[seed];
    const cx = Math.floor(x / radius);
    const cy = Math.floor(y / radius);
    const members: number[] = [];
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        const bucket = grid.get(`${cx + dx}:${cy + dy}`);
        if (!bucket) continue;
        for (const index of bucket) {
          if (used[index]) continue;
          const [x2, y2] = coords[index];
          const ddx = x2 - x;
          const ddy = y2 - y;
          if (ddx * ddx + ddy * ddy <= radiusSq) members.push(index);
        }
      }
    }
    for (const index of members) used[index] = 1;

    if (members.length === 1) {
      pins.push({ kind: "church", church: churches[members[0]] });
      continue;
    }

    const grouped = members
      .map((index) => churches[index])
      .sort((a, b) => a.id - b.id);
    let latitude = 0;
    let longitude = 0;
    for (const church of grouped) {
      latitude += church.latitude;
      longitude += church.longitude;
    }
    pins.push({
      kind: "cluster",
      key: grouped.map((church) => church.id).join("-"),
      latitude: latitude / grouped.length,
      longitude: longitude / grouped.length,
      count: grouped.length,
      churches: grouped,
    });
  }

  return pins;
}

/**
 * The nearest zoom at or above `zoom` where `churchId` is drawn as its own
 * pin. Searching for a church that currently sits inside a count flies here
 * so the popup has a pin to open. Grouping only ever splits as you zoom in,
 * so the scan stops at the first zoom that separates it.
 */
export function zoomToRevealChurch<T extends Clusterable>(
  churches: readonly T[],
  churchId: number,
  zoom: number,
): number {
  const start = Math.max(0, Math.round(zoom));
  if (start >= INDIVIDUAL_ZOOM) return Math.min(start, 19);
  if (!churches.some((church) => church.id === churchId)) return start;

  for (let z = start; z < INDIVIDUAL_ZOOM; z++) {
    const alone = clusterChurches(churches, z).some(
      (pin) => pin.kind === "church" && pin.church.id === churchId,
    );
    if (alone) return z;
  }
  return INDIVIDUAL_ZOOM;
}
