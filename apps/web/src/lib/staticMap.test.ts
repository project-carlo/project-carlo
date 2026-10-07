import { describe, expect, it } from "vitest";
import {
  fitZoom,
  staticMapPosition,
  staticMapTiles,
  TILE_SIZE,
  worldPixel,
} from "./staticMap";

const ROCHESTER = { lat: 43.1566, lng: -77.6088 };

describe("worldPixel", () => {
  it("puts the null island at the middle of the world", () => {
    expect(worldPixel({ lat: 0, lng: 0 }, 0)).toEqual({ x: 128, y: 128 });
    expect(worldPixel({ lat: 0, lng: 0 }, 3)).toEqual({ x: 1024, y: 1024 });
  });

  it("matches the OSM tile a known point falls in", () => {
    // Rochester, NY sits in tile 12/1164/1502.
    const p = worldPixel(ROCHESTER, 12);
    expect(Math.floor(p.x / TILE_SIZE)).toBe(1164);
    expect(Math.floor(p.y / TILE_SIZE)).toBe(1502);
  });
});

describe("fitZoom", () => {
  it("zooms all the way in on a lone point at the center", () => {
    expect(fitZoom(ROCHESTER, [ROCHESTER], 130, 72, 9, 14)).toBe(14);
  });

  it("zooms out until every point fits", () => {
    // ~5 miles east: about 146px out at zoom 11, 73px at zoom 10.
    const east = { lat: ROCHESTER.lat, lng: ROCHESTER.lng + 0.1 };
    const zoom = fitZoom(ROCHESTER, [east], 130, 72, 9, 14);
    expect(zoom).toBe(10);
    const c = worldPixel(ROCHESTER, zoom);
    expect(worldPixel(east, zoom).x - c.x).toBeLessThanOrEqual(130);
    expect(worldPixel(east, zoom + 1).x - worldPixel(ROCHESTER, zoom + 1).x).toBeGreaterThan(130);
  });

  it("stops at the minimum zoom when nothing fits", () => {
    expect(fitZoom(ROCHESTER, [{ lat: 0, lng: 0 }], 130, 72, 9, 14)).toBe(9);
  });
});

describe("staticMapTiles", () => {
  const size = { width: 800, height: 320 };

  it("covers the whole canvas with whole-pixel tiles", () => {
    const tiles = staticMapTiles(ROCHESTER, 13, size);
    for (const tile of tiles) {
      expect(Number.isInteger(tile.left)).toBe(true);
      expect(Number.isInteger(tile.top)).toBe(true);
    }
    const left = Math.min(...tiles.map((t) => t.left));
    const top = Math.min(...tiles.map((t) => t.top));
    const right = Math.max(...tiles.map((t) => t.left + TILE_SIZE));
    const bottom = Math.max(...tiles.map((t) => t.top + TILE_SIZE));
    expect(left).toBeLessThanOrEqual(0);
    expect(top).toBeLessThanOrEqual(0);
    expect(right).toBeGreaterThanOrEqual(size.width);
    expect(bottom).toBeGreaterThanOrEqual(size.height);
    // No tile lies wholly off the canvas.
    for (const tile of tiles) {
      expect(tile.left).toBeGreaterThan(-TILE_SIZE);
      expect(tile.top).toBeGreaterThan(-TILE_SIZE);
      expect(tile.left).toBeLessThan(size.width);
      expect(tile.top).toBeLessThan(size.height);
    }
  });

  it("names OSM tile URLs by zoom, column and row", () => {
    const tiles = staticMapTiles(ROCHESTER, 12, size);
    expect(tiles.map((t) => t.url)).toContain(
      "https://tile.openstreetmap.org/12/1164/1502.png",
    );
  });

  it("wraps columns across the antimeridian", () => {
    const tiles = staticMapTiles({ lat: 0, lng: 179.99 }, 2, size);
    const columns = tiles.map((t) => Number(t.url.split("/").at(-2)));
    expect(columns).toContain(0);
    expect(columns).toContain(3);
    expect(columns.every((c) => c >= 0 && c < 4)).toBe(true);
  });

  it("leaves out rows beyond the poles", () => {
    const tiles = staticMapTiles({ lat: 85, lng: 0 }, 1, size);
    const rows = tiles.map((t) => Number(t.url.split("/").at(-1)!.replace(".png", "")));
    expect(rows.every((r) => r >= 0 && r < 2)).toBe(true);
  });
});

describe("staticMapPosition", () => {
  it("puts the center in the middle of the canvas", () => {
    const pos = staticMapPosition(ROCHESTER, 13, { width: 800, height: 320 }, ROCHESTER);
    expect(Math.abs(pos.left - 400)).toBeLessThanOrEqual(0.5);
    expect(Math.abs(pos.top - 160)).toBeLessThanOrEqual(0.5);
  });

  it("lines a point up with the tile under it", () => {
    const size = { width: 800, height: 320 };
    const point = { lat: 43.17, lng: -77.58 };
    const pos = staticMapPosition(ROCHESTER, 13, size, point);
    const world = worldPixel(point, 13);
    const tile = staticMapTiles(ROCHESTER, 13, size).find(
      (t) =>
        t.url ===
        `https://tile.openstreetmap.org/13/${Math.floor(world.x / TILE_SIZE)}/${Math.floor(world.y / TILE_SIZE)}.png`,
    )!;
    expect(pos.left - tile.left).toBeCloseTo(world.x % TILE_SIZE, 6);
    expect(pos.top - tile.top).toBeCloseTo(world.y % TILE_SIZE, 6);
  });
});
