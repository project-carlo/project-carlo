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
 * Starts the home map's startup fetches when the page loads straight onto the
 * map, instead of after the router has fetched the HomePage chunk. That saves
 * a round of requests before the first map tiles can load. Only the fetches
 * HomePage would make itself are started: the IP lookup only for a first
 * visit (no view in the URL, nothing handed over by the landing page).
 */
export function prefetchHomeStart(queryClient: QueryClient): void {
  if (window.location.pathname !== "/") return;
  void queryClient.prefetchQuery(churchSearchIndexQuery);
  const hasView =
    decodeMapViewFromParams(new URLSearchParams(window.location.search)) !=
    null;
  // React Router keeps navigation state under `usr` in history.state.
  const routerState = (window.history.state as { usr?: unknown } | null)?.usr;
  const hasCenterOn =
    typeof routerState === "object" &&
    routerState !== null &&
    "centerOn" in routerState &&
    routerState.centerOn != null;
  if (!hasView && !hasCenterOn) {
    void queryClient.prefetchQuery(approximateLocationQuery);
  }
}
