/**
 * Minimal Cloudflare Workers types for worker/index.ts.
 *
 * `@cloudflare/workers-types` isn't a dependency (and the sandbox can't fetch
 * it), and the Worker only touches a sliver of the runtime API, so this
 * declares just that. Swap it for the real package (or `wrangler types`) if the
 * Worker grows.
 */

/** The subset of `request.cf` the Worker reads. Every field can be absent
 *  (local dev, some networks, Tor, etc.), and the coordinates arrive as
 *  strings. */
interface IncomingRequestCfProperties {
  city?: string;
  region?: string;
  regionCode?: string;
  country?: string;
  postalCode?: string;
  latitude?: string;
  longitude?: string;
  timezone?: string;
}

/** A standard Request, plus the Cloudflare-specific `cf` object. */
type WorkerRequest = Request & { cf?: IncomingRequestCfProperties };

/** A service binding such as the static-assets binding. */
interface Fetcher {
  fetch(request: Request): Promise<Response>;
}

/** Bindings declared in wrangler.jsonc (`assets.binding`) and optional vars. */
interface Env {
  ASSETS: Fetcher;
  /** Dev-only: force /api/geo to a fixed place (see worker/geo.ts MOCKS). */
  GEO_MOCK?: string;
}
