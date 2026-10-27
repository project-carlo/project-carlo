import type { QueryClient } from "@tanstack/react-query";
import { fetchAllChurchesForSearch } from "../api";
import { fetchApproximateLocation } from "./approximateLocation";
import { decodeMapViewFromParams } from "./mapView";

/**
 * The two queries the home map waits on before it mounts on a first visit:
 * every church, and the IP-location estimate. HomePage reads them with these
 * same options; main.tsx starts them before the HomePage chunk has loaded.
 */
export const churchSearchIndexQuery = {
  queryKey: ["church-search-index"],
  queryFn: fetchAllChurchesForSearch,
  staleTime: 5 * 60 * 1000,
} as const;

export const approximateLocationQuery = {
  queryKey: ["approximate-location"],
  queryFn: ({ signal }: { signal: AbortSignal }) =>
    fetchApproximateLocation(signal),
  staleTime: Infinity,
  retry: false,
} as const;

/**
 * Whether the home map opens on a first visit: no view in the URL and no
 * church handed over by the landing page to fly to. Only then does it wait on
 * the queries above before mounting. HomePage and the prefetch below both ask
 * this, so they always agree on which fetches to make.
 */
export function isFirstVisitStart(search: string, navState: unknown): boolean {
  if (decodeMapViewFromParams(new URLSearchParams(search)) != null) {
    return false;
  }
  const centerOn =
    typeof navState === "object" && navState !== null && "centerOn" in navState
      ? navState.centerOn
      : undefined;
  return !centerOn;
}

/**
 * Starts the home map's startup fetches when the page loads straight onto the
 * map, instead of after the router has fetched the HomePage chunk. That saves
 * a round of requests before the first map tiles can load. Only a first visit
 * waits on these, so a return visit (a view in the URL) fetches nothing early.
 */
export function prefetchHomeStart(queryClient: QueryClient): void {
  const { pathname, search } = window.location;
  let firstVisit: boolean;
  if (pathname === "/") {
    // React Router keeps navigation state under `usr` in history.state.
    const navState = (window.history.state as { usr?: unknown } | null)?.usr;
    firstVisit = isFirstVisitStart(search, navState);
  } else if (pathname === "/map") {
    // The old map path redirects to a bare "/", dropping any query or state.
    firstVisit = true;
  } else {
    return;
  }
  if (!firstVisit) return;
  void queryClient.prefetchQuery(churchSearchIndexQuery);
  void queryClient.prefetchQuery(approximateLocationQuery);
}
