import { useEffect, useMemo } from "react";
import { useQuery } from "@tanstack/react-query";
import { useMap, ZoomControl } from "react-leaflet";
import { fetchChurches, type ChurchFilters } from "../api";
import { ChurchMap } from "./ChurchMap";
import { DEFAULT_FILTER_STATE } from "./filterState";
import type { MapStart } from "../lib/mapStart";
import type { MapView } from "../lib/mapView";
import type { ChurchMapItem } from "../types";

/** The home map's opening query, so in the app the two share one cache entry. */
const FILTERS: ChurchFilters = { types: [DEFAULT_FILTER_STATE.eventType] };

const NO_CHURCHES: ChurchMapItem[] = [];

/**
 * Fits the map to its box whenever it moves between the page and the whole
 * window. In the page, the scroll wheel scrolls the page until the map is
 * clicked, and again once the pointer leaves it; over the whole window it
 * zooms.
 */
function MapMode({ open }: { open: boolean }) {
  const map = useMap();
  useEffect(() => {
    map.invalidateSize({ animate: false });
    if (open) {
      map.scrollWheelZoom.enable();
      return;
    }
    map.scrollWheelZoom.disable();
    const enable = () => map.scrollWheelZoom.enable();
    const disable = () => map.scrollWheelZoom.disable();
    map.on("click focus", enable);
    map.on("mouseout", disable);
    return () => {
      map.off("click focus", enable);
      map.off("mouseout", disable);
    };
  }, [map, open]);
  return null;
}

/**
 * The live map behind CityMapLive: the home map's churches, pins and popups,
 * opening on the city preview's view. Loaded only when it's shown, so a phone
 * that never opens the map never downloads Leaflet.
 */
export default function CityLeafletMap({
  view,
  open,
  onReady,
  onViewChange,
}: {
  view: MapView;
  open: boolean;
  /** Called once the churches are on the map. */
  onReady: () => void;
  onViewChange: (view: MapView) => void;
}) {
  const { data } = useQuery({
    queryKey: ["churches", FILTERS],
    queryFn: () => fetchChurches(FILTERS),
  });
  useEffect(() => {
    if (data) onReady();
  }, [data, onReady]);
  // Read once, on mount, like every start.
  const start = useMemo<MapStart>(() => ({ kind: "view", view }), [view]);

  return (
    <ChurchMap
      churches={data ?? NO_CHURCHES}
      start={start}
      onViewChange={onViewChange}
    >
      <ZoomControl position="bottomright" />
      <MapMode open={open} />
    </ChurchMap>
  );
}
