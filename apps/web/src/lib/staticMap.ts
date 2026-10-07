import type { LatLng } from "./cities";

/**
 * A map drawn without a map library: OpenStreetMap tiles laid out as plain
 * images, with points placed on them in pixels. Pure, so the prerendered city
 * pages, which ship no JavaScript, can show the same map preview the app does.
 */

/** Edge of an OpenStreetMap tile, in pixels. */
export const TILE_SIZE = 256;

/** The tile server the home map's Leaflet layer uses too. */
const TILE_URL = "https://tile.openstreetmap.org";

export interface StaticMapSize {
  width: number;
  height: number;
}

/** A tile image, placed from the map's top-left corner. */
export interface StaticMapTile {
  key: string;
  url: string;
  left: number;
  top: number;
}

/** A point's position from the map's top-left corner, in pixels. */
export interface StaticMapPosition {
  left: number;
  top: number;
}

/** Web Mercator pixel coordinates of a point on the whole world at `zoom`. */
export function worldPixel(point: LatLng, zoom: number): { x: number; y: number } {
  const scale = TILE_SIZE * 2 ** zoom;
  // Clamped short of the poles, where Mercator runs off to infinity.
  const sin = Math.min(Math.max(Math.sin((point.lat * Math.PI) / 180), -0.9999), 0.9999);
  return {
    x: ((point.lng + 180) / 360) * scale,
    y: (0.5 - Math.log((1 + sin) / (1 - sin)) / (4 * Math.PI)) * scale,
  };
}

/**
 * The closest zoom, from `maxZoom` down to `minZoom`, at which every point
 * lies within `halfWidth` and `halfHeight` pixels of `center`; `minZoom` when
 * none fits.
 */
export function fitZoom(
  center: LatLng,
  points: ReadonlyArray<LatLng>,
  halfWidth: number,
  halfHeight: number,
  minZoom: number,
  maxZoom: number,
): number {
  for (let zoom = maxZoom; zoom > minZoom; zoom--) {
    const c = worldPixel(center, zoom);
    const fits = points.every((point) => {
      const p = worldPixel(point, zoom);
      return Math.abs(p.x - c.x) <= halfWidth && Math.abs(p.y - c.y) <= halfHeight;
    });
    if (fits) return zoom;
  }
  return minZoom;
}

/**
 * The map's top-left corner in world pixels, whole so every tile lands on a
 * whole pixel and no hairline seams show between them.
 */
function origin(center: LatLng, zoom: number, size: StaticMapSize) {
  const c = worldPixel(center, zoom);
  return {
    x: Math.round(c.x - size.width / 2),
    y: Math.round(c.y - size.height / 2),
  };
}

/** The tiles that cover a map of `size` centered on `center`. */
export function staticMapTiles(
  center: LatLng,
  zoom: number,
  size: StaticMapSize,
): StaticMapTile[] {
  const o = origin(center, zoom, size);
  const count = 2 ** zoom;
  const tiles: StaticMapTile[] = [];
  const firstRow = Math.floor(o.y / TILE_SIZE);
  const lastRow = Math.floor((o.y + size.height - 1) / TILE_SIZE);
  const firstColumn = Math.floor(o.x / TILE_SIZE);
  const lastColumn = Math.floor((o.x + size.width - 1) / TILE_SIZE);
  for (let row = firstRow; row <= lastRow; row++) {
    if (row < 0 || row >= count) continue;
    for (let column = firstColumn; column <= lastColumn; column++) {
      // Columns wrap around the antimeridian; rows don't wrap past the poles.
      const x = ((column % count) + count) % count;
      tiles.push({
        key: `${zoom}/${column}/${row}`,
        url: `${TILE_URL}/${zoom}/${x}/${row}.png`,
        left: column * TILE_SIZE - o.x,
        top: row * TILE_SIZE - o.y,
      });
    }
  }
  return tiles;
}

/** Where `point` falls on a map of `size` centered on `center`. */
export function staticMapPosition(
  center: LatLng,
  zoom: number,
  size: StaticMapSize,
  point: LatLng,
): StaticMapPosition {
  const o = origin(center, zoom, size);
  const p = worldPixel(point, zoom);
  return { left: p.x - o.x, top: p.y - o.y };
}
