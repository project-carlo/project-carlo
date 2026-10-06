import type { ChurchBase } from "../types";

/**
 * City (and town) pages: one per city that has at least one church, listing
 * its churches and the closest ones outside it. Pure; shared by the SPA
 * (api.ts) and the prerenderer, so both group churches and measure distances
 * the same way.
 */

/** Path prefix of a city page, e.g. `/mass-times/east-aurora-ny/`. */
export const CITY_PATH_PREFIX = "/mass-times/";

/** How many churches outside the city its page lists as nearby. */
export const NEARBY_CHURCH_LIMIT = 6;

/** Churches farther than this from the city aren't "nearby", however few are closer. */
export const NEARBY_MAX_MILES = 40;

export interface LatLng {
  lat: number;
  lng: number;
}

/**
 * Where a city is, by slug, as scripts/geocode-cities.ts records it in
 * src/data/cityCenters.json: the town's own coordinates from OpenStreetMap.
 */
export type CityCenters = Record<string, LatLng>;

export interface City {
  /** URL slug: city and state, e.g. `east-aurora-ny`. */
  slug: string;
  /** City name as the addresses spell it, e.g. "East Aurora". */
  name: string;
  state: string | null;
  /** "East Aurora, NY". */
  label: string;
  /** The city's churches, by name. */
  churches: ChurchBase[];
  /**
   * Where the city is: its geocoded center when cityCenters.json has one,
   * else the mean position of its geocoded churches; null when neither is known.
   */
  center: LatLng | null;
  /** Whether `center` is the town's own geocoded center, not its churches' mean. */
  geocodedCenter: boolean;
}

export interface CityIndex {
  /** Every city, by label. */
  cities: City[];
  bySlug: Map<string, City>;
}

/** Lowercase, accent-free, hyphen-separated slug of free text. */
function slugify(text: string): string {
  return text
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/&/g, " and ")
    .replace(/['’]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function clean(value: string | null): string | null {
  const trimmed = value?.trim();
  return trimmed ? trimmed : null;
}

/** "East Aurora, NY" for a city and state, or the city alone without a state. */
export function cityLabel(name: string, state: string | null): string {
  return state ? `${name}, ${state}` : name;
}

/** The slug of a church's city page, or null when its address has no city. */
export function citySlugFor(church: Pick<ChurchBase, "city" | "state">): string | null {
  const city = clean(church.city);
  if (!city) return null;
  const slug = slugify([city, clean(church.state)].filter(Boolean).join(" "));
  return slug || null;
}

/** Site-relative path of a city page. */
export function cityPath(slug: string): string {
  return `${CITY_PATH_PREFIX}${encodeURIComponent(slug)}/`;
}

function compareNames(a: ChurchBase, b: ChurchBase): number {
  return (a.name ?? "").localeCompare(b.name ?? "") || a.id - b.id;
}

/** The commonest spelling, so one stray "east aurora" doesn't rename the page. */
function commonest(values: string[]): string {
  const counts = new Map<string, number>();
  let best = values[0];
  for (const value of values) {
    const count = (counts.get(value) ?? 0) + 1;
    counts.set(value, count);
    if (count > (counts.get(best) ?? 0)) best = value;
  }
  return best;
}

/**
 * Group churches into cities by their address's city and state. Churches
 * whose address has no city belong to none. Each city is centered on its
 * entry in `centers`, when there is one.
 */
export function buildCityIndex(
  churches: ChurchBase[],
  centers: CityCenters = {},
): CityIndex {
  const groups = new Map<string, ChurchBase[]>();
  for (const church of churches) {
    const slug = citySlugFor(church);
    if (!slug) continue;
    const group = groups.get(slug);
    if (group) group.push(church);
    else groups.set(slug, [church]);
  }

  const cities: City[] = [];
  for (const [slug, members] of groups) {
    const name = commonest(members.map((c) => clean(c.city)!));
    const states = members.map((c) => clean(c.state)).filter((s) => s !== null);
    const state = states.length > 0 ? commonest(states) : null;
    const geocoded = Object.hasOwn(centers, slug) ? centers[slug] : null;
    cities.push({
      slug,
      name,
      state,
      label: cityLabel(name, state),
      churches: [...members].sort(compareNames),
      center: geocoded
        ? { lat: geocoded.lat, lng: geocoded.lng }
        : centroid(members),
      geocodedCenter: geocoded !== null,
    });
  }
  cities.sort((a, b) => a.label.localeCompare(b.label) || a.slug.localeCompare(b.slug));
  return { cities, bySlug: new Map(cities.map((city) => [city.slug, city])) };
}

function centroid(churches: ChurchBase[]): LatLng | null {
  let lat = 0;
  let lng = 0;
  let count = 0;
  for (const church of churches) {
    if (church.latitude == null || church.longitude == null) continue;
    lat += church.latitude;
    lng += church.longitude;
    count++;
  }
  return count > 0 ? { lat: lat / count, lng: lng / count } : null;
}

const EARTH_RADIUS_MILES = 3958.8;

/** Great-circle distance in miles. */
export function distanceMiles(a: LatLng, b: LatLng): number {
  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const dLat = toRad(b.lat - a.lat);
  const dLng = toRad(b.lng - a.lng);
  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 2 * EARTH_RADIUS_MILES * Math.asin(Math.min(1, Math.sqrt(h)));
}

export interface NearbyChurch {
  church: ChurchBase;
  /** Miles from the city's center. */
  distanceMiles: number;
}

/**
 * The geocoded churches outside `city` closest to its center, nearest first,
 * at most `limit` of them and none farther than `maxMiles`.
 */
export function nearbyChurches(
  city: City,
  churches: ChurchBase[],
  limit: number = NEARBY_CHURCH_LIMIT,
  maxMiles: number = NEARBY_MAX_MILES,
): NearbyChurch[] {
  const center = city.center;
  if (!center) return [];
  const inCity = new Set(city.churches.map((c) => c.id));
  const nearby: NearbyChurch[] = [];
  for (const church of churches) {
    if (inCity.has(church.id)) continue;
    if (church.latitude == null || church.longitude == null) continue;
    const miles = distanceMiles(center, {
      lat: church.latitude,
      lng: church.longitude,
    });
    if (miles <= maxMiles) nearby.push({ church, distanceMiles: miles });
  }
  return nearby
    .sort((a, b) => a.distanceMiles - b.distanceMiles || a.church.id - b.church.id)
    .slice(0, limit);
}

/** "0.4 mi", "3.2 mi", "12 mi". */
export function formatMiles(miles: number): string {
  return miles < 10 ? `${miles.toFixed(1)} mi` : `${Math.round(miles)} mi`;
}
