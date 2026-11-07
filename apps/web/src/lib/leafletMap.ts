import {
  createContext,
  useContext,
  useEffect,
  useLayoutEffect,
  useRef,
} from "react";
import type {
  LeafletEvent,
  LeafletEventHandlerFnMap,
  Map as LeafletMap,
} from "leaflet";

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
 * Listens to the map's events while mounted, calling the latest render's
 * handlers. The listeners stay bound from one render to the next: bound
 * again on each, they would be off the map while React swaps them, and an
 * event fired then, such as the moveend of a long jump another component's
 * effect makes, would be lost.
 */
export function useMapEvents(handlers: LeafletEventHandlerFnMap): LeafletMap {
  const map = useMap();
  const handlersRef = useRef(handlers);
  // Before any effect runs, so one that moves the map reaches these handlers.
  useLayoutEffect(() => {
    handlersRef.current = handlers;
  });
  const types = Object.keys(handlers).sort().join(" ");
  useEffect(() => {
    const listeners: Record<string, (event: LeafletEvent) => void> = {};
    for (const type of types.split(" ").filter(Boolean)) {
      listeners[type] = (event) => {
        const latest = handlersRef.current as Record<
          string,
          ((event: LeafletEvent) => void) | undefined
        >;
        latest[type]?.(event);
      };
    }
    map.on(listeners);
    return () => {
      map.off(listeners);
    };
  }, [map, types]);
  return map;
}
