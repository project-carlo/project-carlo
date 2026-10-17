/**
 * The contract between the site's Worker (worker/index.ts) and the browser
 * code that reads its IP-location answer (approximateLocation.ts). Both
 * TypeScript projects include this file, so renaming the route or a field on
 * one side fails to compile on the other instead of quietly switching the
 * feature off. Types and constants only: the Worker bundle pulls in nothing
 * else.
 */

/** The Worker route that answers with the visitor's IP-derived location. */
export const APPROXIMATE_LOCATION_PATH = "/api/approximate-location";

/** The Worker's answer. A field Cloudflare couldn't resolve is null. */
export interface ApproximateLocationResponse {
  lat: number | null;
  lng: number | null;
  city: string | null;
  region: string | null;
  regionCode: string | null;
  country: string | null;
}
