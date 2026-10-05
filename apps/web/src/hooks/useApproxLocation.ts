import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchAllChurchesForSearch } from "../api";
import {
  LAST_PLACE_EVENT,
  LAST_PLACE_KEY,
  fetchIpGuess,
  inCoverageBox,
  isInCoverage,
  readLastPlace,
  resolveApproxLocation,
  type ApproxLocation,
  type LastPlace,
} from "../lib/approxLocation";

export interface ApproxLocationState {
  /** `loading` until the guess (and, near the covered area, the snapshot that
   *  refines the coverage test) has settled; `ready` after, even when empty. */
  status: "loading" | "ready";
  /** The best place we have for the visitor, or null (then: "fit coverage"). */
  location: ApproxLocation | null;
  /** True when the location is within ~40 miles of a church. False while
   *  loading and when there is no location. */
  inCoverage: boolean;
}

/**
 * Where the visitor probably is, with no browser permission prompt: the last
 * place they chose, else the Worker's IP-based guess (see
 * src/lib/approxLocation.ts). Safe to render outside a browser (the prerender):
 * it just reports `loading`.
 */
export function useApproxLocation(
  options: { enabled?: boolean } = {},
): ApproxLocationState {
  const { enabled = true } = options;
  const [lastPlace, setLastPlace] = useState<LastPlace | null>(() =>
    readLastPlace(),
  );

  // Follow changes: same tab (saveLastPlace's event) and other tabs (storage).
  useEffect(() => {
    const sync = () => setLastPlace(readLastPlace());
    const onStorage = (event: StorageEvent) => {
      if (event.key === null || event.key === LAST_PLACE_KEY) sync();
    };
    window.addEventListener(LAST_PLACE_EVENT, sync);
    window.addEventListener("storage", onStorage);
    return () => {
      window.removeEventListener(LAST_PLACE_EVENT, sync);
      window.removeEventListener("storage", onStorage);
    };
  }, []);

  // The guess is only worth a request when the visitor hasn't chosen a place.
  const guess = useQuery({
    queryKey: ["ip-geo"],
    queryFn: ({ signal }) => fetchIpGuess({ signal }),
    enabled: enabled && lastPlace === null,
    staleTime: Infinity,
    gcTime: Infinity,
    retry: false,
  });

  const location = useMemo(
    () => resolveApproxLocation(lastPlace, guess.data ?? null),
    [lastPlace, guess.data],
  );

  // The same query the search typeahead runs, so this costs no extra download.
  // It only refines the coarse bounding-box test, so a failure isn't fatal.
  const churches = useQuery({
    queryKey: ["church-search-index"],
    queryFn: fetchAllChurchesForSearch,
    staleTime: 5 * 60 * 1000,
    enabled: enabled && location !== null && inCoverageBox(location),
  });

  return useMemo<ApproxLocationState>(() => {
    if (lastPlace === null && guess.isPending) {
      return { status: "loading", location: null, inCoverage: false };
    }
    if (!location) {
      return { status: "ready", location: null, inCoverage: false };
    }
    if (!inCoverageBox(location)) {
      return { status: "ready", location, inCoverage: false };
    }
    if (churches.isPending) {
      return { status: "loading", location, inCoverage: false };
    }
    return {
      status: "ready",
      location,
      inCoverage: isInCoverage(location, churches.data),
    };
  }, [lastPlace, guess.isPending, location, churches.isPending, churches.data]);
}
