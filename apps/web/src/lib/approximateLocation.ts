import {
  APPROXIMATE_LOCATION_PATH,
  type ApproximateLocationResponse,
} from "./approximateLocationApi";

/**
 * The visitor's rough whereabouts from their IP address, served by the site's
 * Worker (worker/index.ts) from Cloudflare's request geolocation. It's often
 * tens of kilometres off — the IP may belong to an ISP hub in another town —
 * so the map only uses it to pick a zoomed-out starting view.
 */
export interface ApproximateLocation {
  lat: number;
  lng: number;
  /** The city it's in, e.g. "Rochester, NY". */
  label: string;
}

/** Zoom for a map started from an IP estimate: a region rather than a town,
 *  so the visitor is still on screen when the estimate is a county or two
 *  out. A phone shows a third as much ground at the same zoom, so it starts
 *  a level further out to cover a similar distance. */
export function approximateLocationZoom(isDesktop: boolean): number {
  return isDesktop ? 9 : 8;
}

/** Starting the map somewhere with no churches on it helps no one, so an
 *  estimate further than this from every church is ignored. */
export const MAX_KM_FROM_NEAREST_CHURCH = 150;

/** How long the map waits for the estimate before starting on the whole
 *  covered area instead. */
const LOOKUP_TIMEOUT_MS = 1500;

/**
 * Reads the Worker's response. Without a city the coordinates are a country
 * or region centroid (the US one is in rural Kansas), which is no use as a
 * starting point, so those come back null too.
 */
export function parseApproximateLocation(
  body: unknown,
): ApproximateLocation | null {
  if (typeof body !== "object" || body === null) return null;
  // Typed as the Worker's answer, but checked field by field: whatever
  // answered (a stale Worker, a proxy's error page) may not be it.
  const { lat, lng, city, region, regionCode } = body as Partial<
    Record<keyof ApproximateLocationResponse, unknown>
  >;
  if (typeof lat !== "number" || !Number.isFinite(lat)) return null;
  if (typeof lng !== "number" || !Number.isFinite(lng)) return null;
  if (Math.abs(lat) > 90 || Math.abs(lng) > 180) return null;
  if (typeof city !== "string" || city.trim() === "") return null;
  const area = [regionCode, region].find(
    (value): value is string => typeof value === "string" && value !== "",
  );
  return {
    lat,
    lng,
    label: area ? `${city.trim()}, ${area}` : city.trim(),
  };
}

/**
 * Fetches the estimate, resolving null rather than throwing when there isn't
 * one (no Worker in front of the build, a slow network, an unplaceable IP):
 * the map then starts on the whole area the site covers.
 */
export async function fetchApproximateLocation(
  signal?: AbortSignal,
): Promise<ApproximateLocation | null> {
  const controller = new AbortController();
  const abort = () => controller.abort();
  signal?.addEventListener("abort", abort);
  const timer = setTimeout(abort, LOOKUP_TIMEOUT_MS);
  try {
    const response = await fetch(APPROXIMATE_LOCATION_PATH, {
      signal: controller.signal,
      headers: { Accept: "application/json" },
    });
    if (!response.ok) return null;
    return parseApproximateLocation(await response.json());
  } catch {
    return null;
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener("abort", abort);
  }
}

const EARTH_RADIUS_KM = 6371;

function toRadians(degrees: number): number {
  return (degrees * Math.PI) / 180;
}

/** Great-circle distance between two points, in kilometres. */
export function distanceKm(
  a: { lat: number; lng: number },
  b: { lat: number; lng: number },
): number {
  const dLat = toRadians(b.lat - a.lat);
  const dLng = toRadians(b.lng - a.lng);
  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRadians(a.lat)) *
      Math.cos(toRadians(b.lat)) *
      Math.sin(dLng / 2) ** 2;
  return 2 * EARTH_RADIUS_KM * Math.asin(Math.min(1, Math.sqrt(h)));
}

/** Whether any church with coordinates lies within `maxKm` of `point`. */
export function isNearAnyChurch(
  point: { lat: number; lng: number },
  churches: ReadonlyArray<{ latitude: number | null; longitude: number | null }>,
  maxKm: number = MAX_KM_FROM_NEAREST_CHURCH,
): boolean {
  return churches.some(
    (church) =>
      church.latitude != null &&
      church.longitude != null &&
      distanceKm(point, { lat: church.latitude, lng: church.longitude }) <=
        maxKm,
  );
}
