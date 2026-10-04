/**
 * `GET /api/geo`: an approximate location for the visitor, taken from
 * Cloudflare's IP geolocation (`request.cf`). No browser permission prompt, no
 * third-party call, no storage. The client (src/lib/approxLocation.ts) treats
 * it as a guess: city-level at best, and wrong for VPN users.
 *
 * Pure functions only (no Worker globals beyond Request/Response), so it is
 * unit-testable under Node.
 */

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

/** Fixed places for local testing: `/api/geo?mock=rochester`, or the
 *  `GEO_MOCK` var. Only honoured on localhost (see `isLocalHost`). */
export const GEO_MOCKS: Record<string, GeoGuess> = {
  rochester: {
    city: "Rochester",
    region: "New York",
    regionCode: "NY",
    country: "US",
    postalCode: "14604",
    lat: 43.1566,
    lng: -77.6088,
    timezone: "America/New_York",
    source: "ip",
  },
  // Outside the covered dioceses.
  columbus: {
    city: "Columbus",
    region: "Ohio",
    regionCode: "OH",
    country: "US",
    postalCode: "43215",
    lat: 39.9612,
    lng: -82.9988,
    timezone: "America/New_York",
    source: "ip",
  },
  // In the covered area, but nowhere near a church.
  adirondacks: {
    city: "Newcomb",
    region: "New York",
    regionCode: "NY",
    country: "US",
    postalCode: "12852",
    lat: 43.97,
    lng: -74.17,
    timezone: "America/New_York",
    source: "ip",
  },
  // IP geolocation with nothing usable (e.g. Tor).
  unknown: {
    city: null,
    region: null,
    regionCode: null,
    country: null,
    postalCode: null,
    lat: null,
    lng: null,
    timezone: null,
    source: "ip",
  },
};

/** Cloudflare sends coordinates as strings; anything non-numeric becomes null. */
function toNumber(value: string | number | undefined): number | null {
  if (value == null || value === "") return null;
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : null;
}

function toText(value: string | undefined): string | null {
  return value ? value : null;
}

export function geoFromCf(cf: IncomingRequestCfProperties | undefined): GeoGuess {
  return {
    city: toText(cf?.city),
    region: toText(cf?.region),
    regionCode: toText(cf?.regionCode),
    country: toText(cf?.country),
    postalCode: toText(cf?.postalCode),
    lat: toNumber(cf?.latitude),
    lng: toNumber(cf?.longitude),
    timezone: toText(cf?.timezone),
    source: "ip",
  };
}

/** True for a request made to a local dev server, where mocks are allowed. */
export function isLocalHost(hostname: string): boolean {
  return (
    hostname === "localhost" ||
    hostname === "127.0.0.1" ||
    hostname === "[::1]" ||
    hostname.endsWith(".localhost")
  );
}

/** The mock named by `?mock=` (first) or `GEO_MOCK`, on localhost only. */
export function pickMock(url: URL, env: Pick<Env, "GEO_MOCK">): GeoGuess | null {
  if (!isLocalHost(url.hostname)) return null;
  const name = (url.searchParams.get("mock") ?? env.GEO_MOCK ?? "")
    .trim()
    .toLowerCase();
  return Object.hasOwn(GEO_MOCKS, name) ? GEO_MOCKS[name] : null;
}

export function handleGeo(request: WorkerRequest, env: Env): Response {
  const url = new URL(request.url);
  const guess = pickMock(url, env) ?? geoFromCf(request.cf);
  return Response.json(guess, {
    headers: {
      // Per-visitor, so it must never sit in a shared cache.
      "Cache-Control": "private, no-store",
    },
  });
}
