import { useCallback, useRef, useState } from "react";
import type { ChurchSearchResult } from "../api";
import { PLACE_SEARCH_ZOOM, type PlaceSearchResult } from "../placeSearch";

/** Where a map is asked to go: a church (its popup opened) or a pinned place. */
export interface MapCenterRequest {
  lat: number;
  lng: number;
  churchId?: number;
  placeTitle?: string;
  placeSubtitle?: string | null;
  openPlacePopup?: boolean;
  zoom?: number;
  /**
   * Bumped on every request, so asking for the same church again still
   * produces a distinct value, which the map uses to re-pan and re-open its
   * popup without a timer-based reset.
   */
  requestId: number;
}

/**
 * A map's search selection, shared by the home map and the city page's: the
 * church or place to fly to, and the pinned place until it's removed.
 * `onSelect` runs as the visitor picks one.
 */
export function useMapSelection(onSelect?: () => void) {
  const [centerOn, setCenterOn] = useState<MapCenterRequest | null>(null);
  const requestIdRef = useRef(0);
  const onSelectRef = useRef(onSelect);
  onSelectRef.current = onSelect;

  const center = useCallback((target: Omit<MapCenterRequest, "requestId">) => {
    requestIdRef.current += 1;
    setCenterOn({ ...target, requestId: requestIdRef.current });
  }, []);

  const selectChurch = useCallback(
    (church: ChurchSearchResult) => {
      if (church.latitude == null || church.longitude == null) return;
      onSelectRef.current?.();
      center({ lat: church.latitude, lng: church.longitude, churchId: church.id });
    },
    [center],
  );

  const selectPlace = useCallback(
    (place: PlaceSearchResult) => {
      onSelectRef.current?.();
      center({
        lat: place.lat,
        lng: place.lng,
        placeTitle: place.title,
        placeSubtitle: place.subtitle,
        // The visitor's own position is pinned quietly; its popup opens on a click.
        openPlacePopup: !place.isCurrentLocation,
        zoom: PLACE_SEARCH_ZOOM,
      });
    },
    [center],
  );

  // Removes the searched-place pin. A selected church shares `centerOn` but
  // isn't a pin, so it's left alone.
  const clearPlace = useCallback(() => {
    setCenterOn((current) => (current?.placeTitle ? null : current));
  }, []);

  return { centerOn, center, selectChurch, selectPlace, clearPlace };
}
