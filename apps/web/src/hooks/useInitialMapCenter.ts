import { useCallback, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useApproxLocation } from "./useApproxLocation";
import type { ApproxLocation } from "../lib/approxLocation";
import type { MapView } from "../lib/mapView";

/** How close the default view is to a visitor's neighbourhood. */
const APPROX_ZOOM = 11;

/** Wait this long for the location guess before showing the default view. */
const MAX_WAIT_MS = 1500;

interface Decision {
  view: MapView | null;
  /** The location `view` is centered on; null when the default view is used. */
  location: ApproxLocation | null;
}

const NO_DECISION: Decision = { view: null, location: null };

export interface InitialMapCenter {
  /** False until the starting camera is known; mount the map only after this. */
  ready: boolean;
  /** The camera to open the map at, or null for the default (fit coverage). */
  view: MapView | null;
  /** The approximate location the map opened on, to explain it. Null when the
   *  default view is used or the visitor dismissed the notice. */
  notice: ApproxLocation | null;
  dismissNotice: () => void;
}

/**
 * The map's starting camera when the URL has none and nothing asked for a
 * place (`centerOn` router state): the visitor's approximate location, if it
 * is within coverage. Decided once, then frozen, because a Leaflet map only
 * reads its initial center on mount.
 *
 * `urlView` is the camera decoded from the URL, which always wins.
 */
export function useInitialMapCenter(urlView: MapView | null): InitialMapCenter {
  const routerLocation = useLocation();
  const [skip] = useState(
    () =>
      urlView !== null ||
      Boolean((routerLocation.state as { centerOn?: unknown } | null)?.centerOn),
  );
  // A camera from the URL or router state makes the guess moot: don't ask.
  const approx = useApproxLocation({ enabled: !skip });
  const [timedOut, setTimedOut] = useState(false);
  const [dismissed, setDismissed] = useState(false);
  const [decision, setDecision] = useState<Decision | null>(
    skip ? NO_DECISION : null,
  );

  useEffect(() => {
    if (decision) return;
    const id = window.setTimeout(() => setTimedOut(true), MAX_WAIT_MS);
    return () => window.clearTimeout(id);
  }, [decision]);

  // Settle exactly once, as soon as the guess is in (or we have waited long
  // enough). Setting state during render is the supported way to derive it.
  if (!decision && (approx.status === "ready" || timedOut)) {
    const { location } = approx;
    setDecision(
      approx.status === "ready" && location && approx.inCoverage
        ? {
            view: { lat: location.lat, lng: location.lng, zoom: APPROX_ZOOM },
            location,
          }
        : NO_DECISION,
    );
  }

  const dismissNotice = useCallback(() => setDismissed(true), []);

  return {
    ready: decision !== null,
    view: decision?.view ?? null,
    notice: dismissed ? null : (decision?.location ?? null),
    dismissNotice,
  };
}
