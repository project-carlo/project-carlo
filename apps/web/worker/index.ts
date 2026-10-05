/**
 * The site's Worker. Static assets (and the SPA fallback) are served by
 * Cloudflare before this runs; only `/api/*` reaches it first (see
 * `run_worker_first` in wrangler.jsonc).
 */

import {
  APPROXIMATE_LOCATION_PATH,
  type ApproximateLocationResponse,
} from "../src/lib/approximateLocationApi";

interface Env {
  ASSETS: { fetch(request: Request): Promise<Response> };
}

/** The slice of Cloudflare's `request.cf` geolocation this Worker reads. */
interface CfGeo {
  latitude?: string;
  longitude?: string;
  city?: string;
  region?: string;
  regionCode?: string;
  country?: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.pathname === APPROXIMATE_LOCATION_PATH) {
      return approximateLocation(request);
    }
    return env.ASSETS.fetch(request);
  },
};

/**
 * Where the visitor's IP address places them, from the geolocation Cloudflare
 * attaches to every request — no third-party lookup, and the address itself
 * never leaves Cloudflare. It's city-level at best, so the map treats it as a
 * rough starting point, not a position. Fields Cloudflare couldn't resolve
 * come back null.
 */
function approximateLocation(request: Request): Response {
  const cf = (request as Request & { cf?: CfGeo }).cf;
  const lat = parseCoordinate(cf?.latitude, 90);
  const lng = parseCoordinate(cf?.longitude, 180);
  const located = lat != null && lng != null;
  const body: ApproximateLocationResponse = {
    lat: located ? lat : null,
    lng: located ? lng : null,
    city: cf?.city || null,
    region: cf?.region || null,
    regionCode: cf?.regionCode || null,
    country: cf?.country || null,
  };
  return Response.json(body, {
    // Per visitor, so no shared cache may keep it.
    headers: { "Cache-Control": "private, no-store" },
  });
}

function parseCoordinate(raw: string | undefined, limit: number): number | null {
  if (raw == null || raw === "") return null;
  const value = Number(raw);
  return Number.isFinite(value) && Math.abs(value) <= limit ? value : null;
}
