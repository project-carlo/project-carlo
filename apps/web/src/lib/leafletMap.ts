import { createContext, useContext, useEffect } from "react";
import type { LeafletEventHandlerFnMap, Map as LeafletMap } from "leaflet";

/**
 * The Leaflet map a `MapContainer` (components/Leaflet.tsx) has created,
 * for the layers and behaviors rendered inside it. Null outside one: the
 * container renders its children only once its map exists.
 */
export const LeafletMapContext = createContext<LeafletMap | null>(null);

/** The map this component is rendered inside. */
export function useMap(): LeafletMap {
  const map = useContext(LeafletMapContext);
  if (!map) throw new Error("useMap must be called inside a MapContainer");
  return map;
}

/**
 * Listens to the map's events while mounted. The handlers are bound again
 * whenever the object changes, so one written inline sees the latest render's
 * props and state; memoize it to keep the same listeners across renders.
 */
export function useMapEvents(handlers: LeafletEventHandlerFnMap): LeafletMap {
  const map = useMap();
  useEffect(() => {
    map.on(handlers);
    return () => {
      map.off(handlers);
    };
  }, [map, handlers]);
  return map;
}
