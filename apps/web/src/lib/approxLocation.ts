/**
 * Where is this visitor, roughly, without asking the browser for permission?
 *
 * A fallback chain, best first:
 *   1. the last place they chose themselves (a search result, or "use my
 *      current location"), remembered in localStorage;
 *   2. an IP-based guess from the Worker's `GET /api/geo`, cached for the
 *      session in sessionStorage;
 *   3. nothing: callers fall back to "fit the covered area".
 *
 * This module is pure (no React, no router) and storage-safe: every storage
 * access is wrapped, so private windows, blocked storage and the prerender
 * (no `window`) just see "nothing remembered".
 */
import { nearestChurches, type LatLng } from "./places";

export const LAST_PLACE_KEY = "carlo:last-place";
export const IP_GUESS_KEY = "carlo:ip-guess";
/** Fired on `window` (same tab) whenever the remembered place changes. */
export const LAST_PLACE_EVENT = "carlo:last-place-changed";

/** How near a church a visitor has to be for the site to be useful to them. */
export const COVERAGE_RADIUS_MILES = 40;

/** Where the approximate location comes from. */
export type LocationSource = "search" | "device" | "ip";

export interface ApproxLocation {
  lat: number;
  lng: number;
  /** "Rochester, NY", a search result's title, or "Your current location". */
  label: string;
  source: LocationSource;
}

export interface LastPlace {
  lat: number;
  lng: number;
  label: string;
  source: "search" | "device";
  /** Epoch milliseconds. */
  savedAt: number;
}

/** What `GET /api/geo` returns (worker/geo.ts). Every field can be null. */
export interface GeoGuess {
  city: string | null;
  region: string | null;
  regionCode: string | null;
  country: string | null;
  postalCode: string | null;
  lat: number | null;
  lng: number | null;
  timezone: string | null;
  source: "ip";
}

// -------------------------------------------------------------- storage

type StorageKind = "localStorage" | "sessionStorage";

/** The named Web Storage, or null when it is missing or throws on access. */
function getStorage(kind: StorageKind): Storage | null {
  try {
    if (typeof window === "undefined") return null;
    return window[kind] ?? null;
  } catch {
    return null;
  }
}

function readJson(storage: Storage | null, key: string): unknown {
  try {
    const raw = storage?.getItem(key);
    return raw ? (JSON.parse(raw) as unknown) : null;
  } catch {
    return null;
  }
}

function writeJson(storage: Storage | null, key: string, value: unknown): void {
  try {
    storage?.setItem(key, JSON.stringify(value));
  } catch {
    // Quota, private mode, blocked storage: the preference just isn't kept.
  }
}

function isFiniteNumber(value: unknown): value is number {
  return typeof value === "number" && Number.isFinite(value);
}

function isValidLatLng(lat: unknown, lng: unknown): boolean {
  return (
    isFiniteNumber(lat) &&
    isFiniteNumber(lng) &&
    Math.abs(lat) <= 90 &&
    Math.abs(lng) <= 180
  );
}

// ----------------------------------------------------------- last place

export function parseLastPlace(value: unknown): LastPlace | null {
  if (!value || typeof value !== "object") return null;
  const v = value as Record<string, unknown>;
  if (!isValidLatLng(v.lat, v.lng)) return null;
  if (typeof v.label !== "string" || !v.label.trim()) return null;
  if (v.source !== "search" && v.source !== "device") return null;
  return {
    lat: v.lat as number,
    lng: v.lng as number,
    label: v.label,
    source: v.source,
    savedAt: isFiniteNumber(v.savedAt) ? v.savedAt : 0,
  };
}

export function readLastPlace(
  storage: Storage | null = getStorage("localStorage"),
): LastPlace | null {
  return parseLastPlace(readJson(storage, LAST_PLACE_KEY));
}

/** Remember a place the visitor chose. Notifies `useApproxLocation` hooks. */
export function saveLastPlace(
  place: Omit<LastPlace, "savedAt">,
  storage: Storage | null = getStorage("localStorage"),
  now: number = Date.now(),
): void {
  writeJson(storage, LAST_PLACE_KEY, { ...place, savedAt: now });
  try {
    if (typeof window !== "undefined") {
      window.dispatchEvent(new Event(LAST_PLACE_EVENT));
    }
  } catch {
    // Not in a browser.
  }
}

/** The minimal shape of a typeahead place result that `rememberPlace` reads. */
interface RememberablePlace {
  id: string;
  title: string;
  lat: number;
  lng: number;
}

/** The typeahead's "Use your current location" row builds ids with this prefix. */
const CURRENT_LOCATION_ID_PREFIX = "current-location-";

/**
 * Save a place picked in the search typeahead (or its "current location" row)
 * as the visitor's last place. Call it from every `onPlaceSelect`.
 */
export function rememberPlace(place: RememberablePlace): void {
  const device = place.id.startsWith(CURRENT_LOCATION_ID_PREFIX);
  saveLastPlace({
    lat: place.lat,
    lng: place.lng,
    label: device ? "Your current location" : place.title,
    source: device ? "device" : "search",
  });
}

// ------------------------------------------------------------ IP guess

export function parseGeoGuess(value: unknown): GeoGuess | null {
  if (!value || typeof value !== "object") return null;
  const v = value as Record<string, unknown>;
  const text = (x: unknown) => (typeof x === "string" && x ? x : null);
  const num = (x: unknown) => (isFiniteNumber(x) ? x : null);
  return {
    city: text(v.city),
    region: text(v.region),
    regionCode: text(v.regionCode),
    country: text(v.country),
    postalCode: text(v.postalCode),
    lat: num(v.lat),
    lng: num(v.lng),
    timezone: text(v.timezone),
    source: "ip",
  };
}

/** "Rochester, NY", "Ontario" or "your area": a label for an IP guess. */
export function labelForGuess(guess: GeoGuess): string {
  const place = guess.city ?? guess.region;
  if (!place) return "your area";
  const state =
    guess.city && (guess.regionCode ?? guess.region)
      ? (guess.regionCode ?? guess.region)
      : null;
  return state ? `${place}, ${state}` : place;
}

/** The IP guess as a location, or null when it has no usable coordinates. */
export function locationFromGuess(
  guess: GeoGuess | null,
): ApproxLocation | null {
  if (!guess || !isValidLatLng(guess.lat, guess.lng)) return null;
  return {
    lat: guess.lat as number,
    lng: guess.lng as number,
    label: labelForGuess(guess),
    source: "ip",
  };
}

interface CachedGuess {
  /** Null caches a failed or empty lookup so it isn't retried on every page. */
  guess: GeoGuess | null;
}

export function readCachedGuess(
  storage: Storage | null = getStorage("sessionStorage"),
): CachedGuess | null {
  const raw = readJson(storage, IP_GUESS_KEY);
  if (!raw || typeof raw !== "object" || !("guess" in raw)) return null;
  const guess = (raw as { guess: unknown }).guess;
  return { guess: guess === null ? null : parseGeoGuess(guess) };
}

export function cacheGuess(
  guess: GeoGuess | null,
  storage: Storage | null = getStorage("sessionStorage"),
): void {
  writeJson(storage, IP_GUESS_KEY, { guess });
}

/**
 * Where to ask for the guess. On localhost a `?geo=rochester` in the page URL
 * is passed through as `/api/geo?mock=rochester` so each location can be tried
 * in a browser; the Worker ignores `mock` anywhere else.
 */
export function geoEndpoint(
  pageLocation: Pick<Location, "hostname" | "search"> | null = typeof window ===
  "undefined"
    ? null
    : window.location,
): string {
  const base = "/api/geo";
  if (!pageLocation) return base;
  const local =
    pageLocation.hostname === "localhost" ||
    pageLocation.hostname === "127.0.0.1" ||
    pageLocation.hostname === "[::1]";
  const mock = new URLSearchParams(pageLocation.search).get("geo");
  return local && mock ? `${base}?mock=${encodeURIComponent(mock)}` : base;
}

const GEO_TIMEOUT_MS = 4000;

/**
 * The visitor's IP-based guess: from sessionStorage if this session has asked
 * already, else from the Worker. Never throws; a failure is just "no guess"
 * (and is cached, so a site served without the Worker doesn't re-request on
 * every navigation).
 */
export async function fetchIpGuess(
  options: { fetchImpl?: typeof fetch; signal?: AbortSignal } = {},
): Promise<GeoGuess | null> {
  const cached = readCachedGuess();
  if (cached) return cached.guess;

  const doFetch = options.fetchImpl ?? fetch;
  const timeout = new AbortController();
  const timer = setTimeout(() => timeout.abort(), GEO_TIMEOUT_MS);
  const onAbort = () => timeout.abort();
  options.signal?.addEventListener("abort", onAbort);
  try {
    const response = await doFetch(geoEndpoint(), {
      signal: timeout.signal,
      headers: { Accept: "application/json" },
    });
    const type = response.headers.get("content-type") ?? "";
    // Without the Worker (plain static hosting) the SPA fallback answers with
    // index.html: not JSON, so not a guess.
    if (!response.ok || !type.includes("json")) {
      cacheGuess(null);
      return null;
    }
    const guess = parseGeoGuess(await response.json());
    cacheGuess(guess);
    return guess;
  } catch {
    // Offline, timed out or aborted: don't cache, a later page may succeed.
    return null;
  } finally {
    clearTimeout(timer);
    options.signal?.removeEventListener("abort", onAbort);
  }
}

// ---------------------------------------------------------------- chain

/** The best location available: last chosen place, else the IP guess, else null. */
export function resolveApproxLocation(
  lastPlace: LastPlace | null,
  guess: GeoGuess | null,
): ApproxLocation | null {
  if (lastPlace) {
    return {
      lat: lastPlace.lat,
      lng: lastPlace.lng,
      label: lastPlace.label,
      source: lastPlace.source,
    };
  }
  return locationFromGuess(guess);
}

// ------------------------------------------------------------- coverage

/**
 * A coarse box around everything the snapshot covers (Albany, Buffalo,
 * Rochester and Syracuse dioceses: lat 41.4 to 43.7, lng -79.7 to -73.3),
 * padded by the coverage radius. A cheap first test, before the snapshot has
 * loaded, that already rules out most of the world. Widen it when a diocese
 * outside this box is added.
 */
export const COVERAGE_BOX = {
  south: 40.8,
  north: 44.3,
  west: -80.6,
  east: -72.4,
} as const;

export function inCoverageBox(point: LatLng): boolean {
  return (
    point.lat >= COVERAGE_BOX.south &&
    point.lat <= COVERAGE_BOX.north &&
    point.lng >= COVERAGE_BOX.west &&
    point.lng <= COVERAGE_BOX.east
  );
}

/**
 * True when the point is within `radiusMiles` of a church. With no churches
 * (snapshot not loaded yet) the coarse box decides; with them, the box is
 * only a shortcut for "obviously not".
 */
export function isInCoverage(
  point: LatLng,
  churches?: ReadonlyArray<{
    id: number;
    latitude: number | null;
    longitude: number | null;
  }> | null,
  radiusMiles: number = COVERAGE_RADIUS_MILES,
): boolean {
  if (!inCoverageBox(point)) return false;
  if (!churches || churches.length === 0) return true;
  const [nearest] = nearestChurches([...churches], point, 1);
  return nearest != null && nearest.distanceMiles <= radiusMiles;
}
