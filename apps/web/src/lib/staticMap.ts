import type { LatLng } from "./cities";

/**
 * A map drawn without a map library: OpenStreetMap tiles laid out as plain
 * images, with points placed on them in pixels. Pure, so a city page's map
 * preview is laid out when the page is rendered (prerendered too) and shows
 * before any script runs.
 *
 * Pixels are rounded the way Leaflet rounds them, so a live map opened on the
 * same view draws every tile and marker on the very same pixels.
 */

/** Edge of an OpenStreetMap tile, in pixels. */
export const TILE_SIZE = 256;

/** OpenStreetMap's tiles, as Leaflet's tile layer takes them (ChurchMap's too). */
export const OSM_TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png";

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

/** The point at Web Mercator pixel coordinates `x`, `y` at `zoom`. */
export function latLngAt(x: number, y: number, zoom: number): LatLng {
  const scale = TILE_SIZE * 2 ** zoom;
  const n = Math.PI * (1 - (2 * y) / scale);
  return {
    lat: (Math.atan(Math.sinh(n)) * 180) / Math.PI,
    lng: (x / scale) * 360 - 180,
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
 * whole pixel and no hairline seams show between them (Leaflet's "pixel
 * origin", rounded the same way).
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
        url: OSM_TILE_URL.replace("{z}", String(zoom))
          .replace("{x}", String(x))
          .replace("{y}", String(row)),
        left: column * TILE_SIZE - o.x,
        top: row * TILE_SIZE - o.y,
      });
    }
  }
  return tiles;
}

/**
 * Where `point` falls on a map of `size` centered on `center`, on the whole
 * pixel Leaflet would put a marker for it.
 */
export function staticMapPosition(
  center: LatLng,
  zoom: number,
  size: StaticMapSize,
  point: LatLng,
): StaticMapPosition {
  const o = origin(center, zoom, size);
  const p = worldPixel(point, zoom);
  return { left: Math.round(p.x) - o.x, top: Math.round(p.y) - o.y };
}

/** The `[west, south, east, north]` box a map of `size` centered on `center` shows. */
export function staticMapBounds(
  center: LatLng,
  zoom: number,
  size: StaticMapSize,
): [number, number, number, number] {
  const o = origin(center, zoom, size);
  const northWest = latLngAt(o.x, o.y, zoom);
  const southEast = latLngAt(o.x + size.width, o.y + size.height, zoom);
  return [northWest.lng, southEast.lat, southEast.lng, northWest.lat];
}

/**
 * Where to put a map of `size` (CSS `left` and `top`) so that, inside a box
 * of any size, centered on the same `center`, it lines up pixel for pixel
 * with a Leaflet map filling that box.
 *
 * Leaflet puts the box's corner at round(c − box / 2) in world pixels, and
 * this map's corner is at round(c − size / 2), so the map sits at the
 * difference. That depends on the box's size, which only CSS knows; with
 * c = n + f, n whole, it's round(f) − size / 2 − round(f − box / 2), for CSS's
 * round(), which rounds halves up as Math.round does. Browsers without it
 * drop the declaration for a plain centering, off by at most half a pixel.
 */
export function staticMapPlacement(
  center: LatLng,
  zoom: number,
  size: StaticMapSize,
): { left: string; top: string } {
  const c = worldPixel(center, zoom);
  const axis = (value: number, extent: number) => {
    const f = value - Math.floor(value);
    return `calc(${Math.round(f) - extent / 2}px - round(nearest, calc(${f}px - 50%), 1px))`;
  };
  return { left: axis(c.x, size.width), top: axis(c.y, size.height) };
}
