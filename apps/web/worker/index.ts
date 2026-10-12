/**
 * The site's Worker. Static assets are served by Cloudflare before this runs;
 * only `/api/*` reaches it first (see `run_worker_first` in wrangler.jsonc).
 * Requests no file matches arrive here too and go back to the assets, which
 * answer with 404.html.
 */

import { ACCESS_JWT_HEADER, verifyAccessJwt } from "../src/lib/accessAuth";
import {
  APPROXIMATE_LOCATION_PATH,
  type ApproximateLocationResponse,
} from "../src/lib/approximateLocationApi";
import {
  ANALYTICS_PATH,
  MAX_BATCH_BYTES,
  analyticsDataPoint,
  isBotUserAgent,
  parseAnalyticsBatch,
  type AnalyticsDataPoint,
} from "../src/lib/analyticsApi";
import {
  ANALYTICS_DASHBOARD_API_PATH,
  loadAnalyticsDashboard,
  parseReportOptions,
} from "../src/lib/analyticsReports";

interface Env {
  ASSETS: { fetch(request: Request): Promise<Response> };
  /** Workers Analytics Engine (wrangler.jsonc). Optional, so a Worker
   *  deployed without the binding still serves the site. */
  ANALYTICS?: { writeDataPoint(point: AnalyticsDataPoint): void };
  /** The analytics dashboard's settings, all secrets (docs/analytics.md).
   *  Without them the dashboard endpoint answers 503. */
  CLOUDFLARE_ACCOUNT_ID?: string;
  /** Account → Account Analytics → Read; not the deploy token. */
  ANALYTICS_API_TOKEN?: string;
  /** The Zero Trust team domain, `<team>.cloudflareaccess.com`. */
  ACCESS_TEAM_DOMAIN?: string;
  /** The Access application's Application Audience (AUD) tag. */
  ACCESS_AUD?: string;
  /** "1" in .dev.vars lets `wrangler dev` on localhost skip Access. */
  ANALYTICS_DASHBOARD_LOCAL?: string;
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
    if (url.pathname === ANALYTICS_PATH) {
      return recordEvents(request, url, env);
    }
    if (url.pathname === ANALYTICS_DASHBOARD_API_PATH) {
      return analyticsDashboard(request, url, env);
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

/**
 * Writes a batch of the browser's events (src/lib/analytics.ts) to Analytics
 * Engine, one data point each. The country is Cloudflare's, from the request;
 * the address itself is never recorded. Crawlers' batches are dropped.
 * Anything that isn't a batch gets a 400, and the browser never reads the
 * answer, so a 204 says only that the batch was accepted.
 */
async function recordEvents(request: Request, url: URL, env: Env): Promise<Response> {
  if (request.method !== "POST") {
    return new Response(null, { status: 405, headers: { Allow: "POST" } });
  }
  const length = Number(request.headers.get("Content-Length") ?? 0);
  if (!(length <= MAX_BATCH_BYTES)) return new Response(null, { status: 413 });
  let body: unknown;
  try {
    const raw = await request.text();
    if (raw.length > MAX_BATCH_BYTES) return new Response(null, { status: 413 });
    body = JSON.parse(raw);
  } catch {
    return new Response(null, { status: 400 });
  }
  const batch = parseAnalyticsBatch(body);
  if (!batch) return new Response(null, { status: 400 });
  if (env.ANALYTICS && !isBotUserAgent(request.headers.get("User-Agent"))) {
    const cf = (request as Request & { cf?: CfGeo }).cf;
    const context = { host: url.hostname, country: cf?.country ?? "" };
    for (const event of batch.events) {
      env.ANALYTICS.writeDataPoint(analyticsDataPoint(batch, event, context));
    }
  }
  return new Response(null, { status: 204 });
}

/** Hosts `wrangler dev` serves on, which no request to Cloudflare can carry. */
const LOCAL_HOSTS = new Set(["localhost", "127.0.0.1"]);

/**
 * The analytics dashboard's data (src/views/AnalyticsDashboardPage.tsx): every
 * report `pnpm analytics` prints, as JSON, for whoever Cloudflare Access has
 * signed in. The Worker checks Access's token itself, so the workers.dev and
 * preview URLs, which the Access application on projectcarlo.com doesn't
 * cover, refuse too. Unconfigured, it answers 503, never the data.
 */
async function analyticsDashboard(request: Request, url: URL, env: Env): Promise<Response> {
  const headers = { "Cache-Control": "private, no-store" };
  const fail = (status: number, error: string) => Response.json({ error }, { status, headers });
  if (request.method !== "GET") {
    return new Response(null, { status: 405, headers: { Allow: "GET" } });
  }

  const local = env.ANALYTICS_DASHBOARD_LOCAL === "1" && LOCAL_HOSTS.has(url.hostname);
  if (!local) {
    if (!env.ACCESS_TEAM_DOMAIN || !env.ACCESS_AUD) {
      return fail(503, "Cloudflare Access isn't set up for the dashboard (docs/analytics.md).");
    }
    let identity;
    try {
      identity = await verifyAccessJwt(request.headers.get(ACCESS_JWT_HEADER), {
        teamDomain: env.ACCESS_TEAM_DOMAIN,
        audience: env.ACCESS_AUD,
      });
    } catch {
      return fail(502, "Couldn't fetch Cloudflare Access's signing keys.");
    }
    if (!identity) return fail(403, "Sign in through Cloudflare Access to see the dashboard.");
  }

  if (!env.CLOUDFLARE_ACCOUNT_ID || !env.ANALYTICS_API_TOKEN) {
    return fail(503, "The dashboard's Analytics Engine token isn't set (docs/analytics.md).");
  }
  const options = parseReportOptions({
    days: url.searchParams.get("days"),
    host: url.searchParams.get("host"),
    // The site the dashboard is opened on: projectcarlo.com, or a preview.
    defaultHost: url.hostname,
  });
  if ("error" in options) return fail(400, options.error);
  try {
    const data = await loadAnalyticsDashboard(options, {
      accountId: env.CLOUDFLARE_ACCOUNT_ID,
      apiToken: env.ANALYTICS_API_TOKEN,
    });
    return Response.json(data, { headers });
  } catch (error) {
    return fail(502, error instanceof Error ? error.message : String(error));
  }
}

function parseCoordinate(raw: string | undefined, limit: number): number | null {
  if (raw == null || raw === "") return null;
  const value = Number(raw);
  return Number.isFinite(value) && Math.abs(value) <= limit ? value : null;
}
