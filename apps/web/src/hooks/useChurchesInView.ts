import { useLayoutEffect, useMemo, useState } from "react";
import type { LatLngBounds, Map as LeafletMap } from "leaflet";
import type { ChurchMapItem } from "../types";

/**
 * How many of `churches` have a pin inside the map's visible bounds: the
 * ones the phone's filter sheet will show once it closes. Kept up to date as
 * the map moves or resizes, but only while `enabled`, so a map nobody is
 * counting doesn't re-render its page on every pan. Undefined until there are
 * a map and churches to count.
 */
export function useChurchesInView(
  map: LeafletMap | null,
  churches: readonly ChurchMapItem[] | undefined,
  enabled: boolean,
): number | undefined {
  const [bounds, setBounds] = useState<LatLngBounds | null>(null);
  // Before paint, so the sheet never opens on a count from the last time.
  useLayoutEffect(() => {
    if (!map || !enabled) return;
    const update = () => setBounds(map.getBounds());
    update();
    map.on("moveend resize", update);
    return () => {
      map.off("moveend resize", update);
    };
  }, [map, enabled]);

  return useMemo(() => {
    if (!bounds || !churches) return undefined;
    let count = 0;
    for (const church of churches) {
      if (church.latitude === null || church.longitude === null) continue;
      if (bounds.contains([church.latitude, church.longitude])) count += 1;
    }
    return count;
  }, [bounds, churches]);
}
