/**
 * Project Carlo's Worker. The site is static assets (dist/); the Worker runs
 * first only for `/api/*` (`assets.run_worker_first` in wrangler.jsonc), so
 * every other request is served straight from the assets layer, with
 * public/_redirects, public/_headers and the SPA fallback intact.
 *
 * The `env.ASSETS.fetch` branch below is a safety net, not the normal path.
 */
import { handleGeo } from "./geo";

function json(body: unknown, status: number, extra?: HeadersInit): Response {
  return Response.json(body, {
    status,
    headers: { "Cache-Control": "private, no-store", ...extra },
  });
}

export default {
  async fetch(request: WorkerRequest, env: Env): Promise<Response> {
    const { pathname } = new URL(request.url);

    if (pathname === "/api/geo") {
      if (request.method !== "GET" && request.method !== "HEAD") {
        return json({ error: "Method not allowed" }, 405, { Allow: "GET, HEAD" });
      }
      return handleGeo(request, env);
    }

    if (pathname === "/api" || pathname.startsWith("/api/")) {
      return json({ error: "Not found" }, 404);
    }

    return env.ASSETS.fetch(request);
  },
};
