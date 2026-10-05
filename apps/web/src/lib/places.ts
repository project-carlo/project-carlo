/**
 * Shared "places" layer: diocese records, city grouping, URL paths and
 * nearest-church math. Pure (no DOM, no React, no router), so the SPA and the
 * prerenderer (scripts/prerender.ts) use exactly the same code.
 *
 * Diocese data is not in the data snapshot; it comes from
 * src/generated/places.json, written by `pnpm places:gen`
 * (scripts/generate-places.ts) from data/dioceses/** and data/churches.csv.
 *
 * Site structure these helpers build paths for:
 *   /mass-times/ny/                 state hub
 *   /mass-times/ny/{city}/          city page (only cities with 2+ churches)
 *   /dioceses/                      diocese index
 *   /dioceses/{key}/                diocese page
 *   /churches/{slug}/               church page
 */
import placesData from "../generated/places.json";
import type { ChurchBase } from "../types";
import { citySlug } from "./slug";

export { citySlug };

/** A city gets its own page only when it has at least this many churches. */
export const CITY_PAGE_MIN_CHURCHES = 2;

/** "Main cities" (footer, landing page) need at least this many churches. */
export const MAIN_CITY_MIN_CHURCHES = 3;

export const DEFAULT_STATE = "NY";
export const DIOCESE_INDEX_PATH = "/dioceses/";
export const MAP_PATH = "/map";

// ---------------------------------------------------------------- paths

/** `/mass-times/ny/` */
export function statePath(state: string = DEFAULT_STATE): string {
  return `/mass-times/${state.trim().toLowerCase()}/`;
}

/** `/mass-times/ny/niagara-falls/` */
export function cityPath(state: string, city: string): string {
  return `${statePath(state)}${citySlug(city)}/`;
}

/** `/dioceses/rochester/` */
export function diocesePath(key: string): string {
  return `/dioceses/${key}/`;
}

/** `/churches/st-marys-corning/` */
export function churchPath(slug: string): string {
  return `/churches/${encodeURIComponent(slug)}/`;
}

// ------------------------------------------------------------- dioceses

export interface Diocese {
  /** Folder name under data/dioceses, e.g. "rochester". Used in URLs. */
  key: string;
  /** Official name, e.g. "Roman Catholic Diocese of Rochester". */
  name: string;
  /** Display name, e.g. "Diocese of Rochester" / "Archdiocese of New York". */
  shortName: string;
  /** Two-letter state, e.g. "NY". */
  state: string;
  website: string | null;
  /** One-paragraph description, or null when there is none. */
  description: string | null;
}

/** A city with several churches, as stored in places.json. */
export interface CityEntry {
  state: string;
  name: string;
  slug: string;
  count: number;
}

interface PlacesData {
  dioceses: Record<string, Diocese>;
  churchDiocese: Record<string, string>;
  cities: CityEntry[];
}

const places = placesData as PlacesData;

/** Every diocese, ordered by display name. */
export function dioceses(): Diocese[] {
  return Object.values(places.dioceses).sort((a, b) =>
    a.shortName.localeCompare(b.shortName),
  );
}

export function getDiocese(key: string): Diocese | null {
  return places.dioceses[key] ?? null;
}

/** The diocese key for a church slug, or null when no diocese record covers it. */
export function dioceseKeyForChurch(slug: string): string | null {
  return places.churchDiocese[slug] ?? null;
}

export function dioceseForChurch(slug: string): Diocese | null {
  const key = dioceseKeyForChurch(slug);
  return key ? getDiocese(key) : null;
}

/** Churches (from any list with `slug`) that belong to a diocese. */
export function churchesInDiocese<T extends Pick<ChurchBase, "slug">>(
  churches: T[],
  key: string,
): T[] {
  return churches.filter((c) => dioceseKeyForChurch(c.slug) === key);
}

/** Church count per diocese key, from the committed mapping alone (no snapshot needed). */
export function dioceseChurchCounts(): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const key of Object.values(places.churchDiocese)) {
    counts[key] = (counts[key] ?? 0) + 1;
  }
  return counts;
}

/**
 * Cities with `min`+ churches from the committed places.json, ordered by
 * church count (desc) then name. Needs no snapshot, so footers and the landing
 * page render synchronously. Generated data covers cities with 2+ churches.
 */
export function placesCities(min: number = CITY_PAGE_MIN_CHURCHES): CityEntry[] {
  return places.cities.filter((c) => c.count >= min);
}

// --------------------------------------------------------------- cities

type CityChurch = Pick<ChurchBase, "city" | "state">;

export interface CityGroup<T extends CityChurch = ChurchBase> {
  state: string;
  /** Display name, e.g. "Niagara Falls". */
  city: string;
  /** URL slug, e.g. "niagara-falls". */
  slug: string;
  /** `/mass-times/ny/niagara-falls/` */
  path: string;
  churches: T[];
}

/**
 * Group churches by (state, city). Spelling/case variants of one city merge
 * (grouped on the slug); the most common spelling is the display name. Churches
 * with no city or state are left out. Ordered by city name.
 */
export function groupChurchesByCity<T extends CityChurch>(
  churches: T[],
): CityGroup<T>[] {
  const groups = new Map<
    string,
    { state: string; slug: string; names: Map<string, number>; churches: T[] }
  >();
  for (const church of churches) {
    const city = church.city?.trim();
    const state = church.state?.trim().toUpperCase();
    if (!city || !state) continue;
    const slug = citySlug(city);
    if (!slug) continue;
    const id = `${state}/${slug}`;
    let group = groups.get(id);
    if (!group) {
      group = { state, slug, names: new Map(), churches: [] };
      groups.set(id, group);
    }
    group.churches.push(church);
    group.names.set(city, (group.names.get(city) ?? 0) + 1);
  }
  return [...groups.values()]
    .map((g) => {
      const city = [...g.names.entries()].sort(
        (a, b) => b[1] - a[1] || a[0].localeCompare(b[0]),
      )[0][0];
      return {
        state: g.state,
        city,
        slug: g.slug,
        path: cityPath(g.state, city),
        churches: g.churches,
      };
    })
    .sort((a, b) => a.state.localeCompare(b.state) || a.city.localeCompare(b.city));
}

/** City groups with at least `n` churches, largest first (ties by name). */
export function citiesWithAtLeast<T extends CityChurch>(
  churches: T[],
  n: number,
): CityGroup<T>[] {
  return groupChurchesByCity(churches)
    .filter((g) => g.churches.length >= n)
    .sort((a, b) => b.churches.length - a.churches.length || a.city.localeCompare(b.city));
}

/** True when this city has enough churches to get its own page. */
export function cityHasPage<T extends CityChurch>(
  churches: T[],
  state: string,
  city: string,
  min: number = CITY_PAGE_MIN_CHURCHES,
): boolean {
  const wantedState = state.trim().toUpperCase();
  const wantedSlug = citySlug(city);
  let count = 0;
  for (const c of churches) {
    if (c.state?.trim().toUpperCase() !== wantedState) continue;
    if (!c.city || citySlug(c.city) !== wantedSlug) continue;
    if (++count >= min) return true;
  }
  return false;
}

// ------------------------------------------------------------- distance

export interface LatLng {
  lat: number;
  lng: number;
}

const EARTH_RADIUS_MILES = 3958.8;

/** Great-circle distance in miles. */
export function haversineMiles(a: LatLng, b: LatLng): number {
  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const dLat = toRad(b.lat - a.lat);
  const dLng = toRad(b.lng - a.lng);
  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 2 * EARTH_RADIUS_MILES * Math.asin(Math.min(1, Math.sqrt(h)));
}

export interface NearbyChurch<T> {
  church: T;
  distanceMiles: number;
}

/**
 * The `n` geocoded churches closest to `point`, nearest first. Churches with
 * no coordinates are skipped, as is the one whose `id` is `excludeId` (use it
 * to leave a church out of its own "nearby" list).
 */
export function nearestChurches<
  T extends Pick<ChurchBase, "id" | "latitude" | "longitude">,
>(
  churches: T[],
  point: LatLng,
  n: number,
  excludeId?: number,
): NearbyChurch<T>[] {
  const out: NearbyChurch<T>[] = [];
  for (const church of churches) {
    if (church.id === excludeId) continue;
    if (church.latitude == null || church.longitude == null) continue;
    out.push({
      church,
      distanceMiles: haversineMiles(point, {
        lat: church.latitude,
        lng: church.longitude,
      }),
    });
  }
  out.sort((a, b) => a.distanceMiles - b.distanceMiles);
  return out.slice(0, Math.max(0, n));
}
