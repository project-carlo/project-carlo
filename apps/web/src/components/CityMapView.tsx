import {
  lazy,
  startTransition,
  Suspense,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import type { Map as LeafletMap } from "leaflet";
import { useMap } from "react-leaflet";
import { fetchChurches, fetchMapChurch } from "../api";
import { ChurchMap } from "./ChurchMap";
import { MapCornerControls } from "./MapCornerControls";
import {
  churchFiltersFor,
  DEFAULT_FILTER_STATE,
  type FilterState,
} from "./filterState";
import { CityMapExpandChip } from "./CityMapExpandChip";
import { DESKTOP_MIN_WIDTH, useMinWidth } from "@/hooks/useMinWidth";
import { useMapSelection } from "@/hooks/useMapSelection";
import { CITY_MAP_ZOOM_CORNER_CLASS } from "@/lib/cityMap";
import type { MapStart } from "@/lib/mapStart";
import type { MapView } from "@/lib/mapView";
import type { ChurchMapItem } from "../types";

const loadOpenControls = () => import("./CityMapOpenControls");
const CityMapOpenControls = lazy(loadOpenControls);

const NO_CHURCHES: ChurchMapItem[] = [];

/**
 * Fits the map to its box whenever it moves between the page and the whole
 * window. In the page, the scroll wheel scrolls the page until the map is
 * clicked, and again once the pointer leaves it; over the whole window it
 * zooms. (A phone drags and pinches it either way.)
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
 * Calls `onMove` once the map starts moving: dragged, pinched, zoomed or sent
 * to a search result. (Not as it's resized: Leaflet keeps its center then,
 * as the preview's centered canvas does.)
 */
function MoveWatch({ onMove }: { onMove: () => void }) {
  const map = useMap();
  useEffect(() => {
    map.on("movestart zoomstart", onMove);
    return () => {
      map.off("movestart zoomstart", onMove);
    };
  }, [map, onMove]);
  return null;
}

/**
 * What CityMapLive shows: the home map's churches, pins and popups, opening
 * on the page preview's view. In the page it has Expand (and zoom buttons on
 * a desktop), and a pin's popup is only the church's name, since the full
 * card would cover most of the small map; open, CityMapOpenControls adds the
 * rest. The filters chosen there stay on the map in the page. Loaded only
 * once the page's map goes live, and the open controls only once the
 * churches are up.
 *
 * On a church page, the church's pin is marked as the page's, and stays on
 * the map whatever the filters leave, as the preview draws it.
 */
export default function CityMapView({
  view,
  churchId,
  open,
  onOpen,
  onClose,
  onReady,
  onMove,
}: {
  view: MapView;
  /** A church page's church. */
  churchId?: number;
  open: boolean;
  onOpen: () => void;
  onClose: () => void;
  /** Called once the churches are on the map. */
  onReady: () => void;
  /** Called as the map starts moving off the view it opened on. */
  onMove: () => void;
}) {
  const isDesktop = useMinWidth(DESKTOP_MIN_WIDTH);
  const [map, setMap] = useState<LeafletMap | null>(null);
  const selection = useMapSelection();

  const [filters, setFilters] = useState<FilterState>(DEFAULT_FILTER_STATE);
  const [appliedFilters, setAppliedFilters] =
    useState<FilterState>(DEFAULT_FILTER_STATE);
  // As on the home map: the panel follows the input at once, the map in a
  // transition that newer input can pre-empt.
  const handleFiltersChange = useCallback((next: FilterState) => {
    setFilters(next);
    startTransition(() => setAppliedFilters(next));
  }, []);
  // With the default filters, the same query (and cache entry) as the home map's.
  const apiFilters = useMemo(
    () => churchFiltersFor(appliedFilters),
    [appliedFilters],
  );
  const { data: filtered } = useQuery({
    queryKey: ["churches", apiFilters],
    queryFn: () => fetchChurches(apiFilters),
    placeholderData: keepPreviousData,
  });
  const { data: pageChurch } = useQuery({
    queryKey: ["map-church", churchId],
    queryFn: () => fetchMapChurch(churchId!),
    enabled: churchId !== undefined,
  });
  // The page's church, added when the filters leave it out.
  const data = useMemo(() => {
    if (churchId === undefined) return filtered;
    if (!filtered || pageChurch === undefined) return undefined;
    if (!pageChurch || filtered.some((church) => church.id === churchId)) {
      return filtered;
    }
    return [...filtered, pageChurch];
  }, [churchId, filtered, pageChurch]);
  useEffect(() => {
    if (!data) return;
    onReady();
    void loadOpenControls();
  }, [data, onReady]);

  // Read once, on mount, like every start.
  const start = useMemo<MapStart>(() => ({ kind: "view", view }), [view]);

  // Open, Escape closes an open popup first, and only the next one the map
  // (CityMapLive, which skips a handled Escape). Leaflet does the same only
  // while the map itself has focus, so a key pressed with focus on a pin, on
  // the page body or on a control would have closed the whole map. Captured,
  // to run before CityMapLive's listener; not when focus is somewhere the map
  // opened outside itself (the phone's filter sheet), which has its own.
  useEffect(() => {
    if (!open || !map) return;
    const container = map.getContainer();
    // The element the map moves in (CityMapLive's), which holds its controls.
    const dialog = container.parentElement;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape" || !container.querySelector(".leaflet-popup")) {
        return;
      }
      const target = event.target;
      if (
        target !== document.body &&
        !(target instanceof Node && dialog?.contains(target))
      ) {
        return;
      }
      map.closePopup();
      event.preventDefault();
    };
    window.addEventListener("keydown", onKeyDown, true);
    return () => window.removeEventListener("keydown", onKeyDown, true);
  }, [open, map]);

  // Focus goes back to Expand as the map closes.
  const expandRef = useRef<HTMLButtonElement>(null);
  const wasOpenRef = useRef(open);
  useEffect(() => {
    if (!open && wasOpenRef.current) expandRef.current?.focus();
    wasOpenRef.current = open;
  }, [open]);

  return (
    <>
      <ChurchMap
        churches={data ?? NO_CHURCHES}
        currentChurchId={churchId}
        start={start}
        centerOn={selection.centerOn}
        onClearPlace={selection.clearPlace}
        mapRef={setMap}
        compactPopups={!open}
      >
        <MapMode open={open} />
        <MoveWatch onMove={onMove} />
      </ChurchMap>
      {open ? (
        <Suspense fallback={null}>
          <CityMapOpenControls
            isDesktop={isDesktop}
            map={map}
            filters={filters}
            appliedFilters={appliedFilters}
            onFiltersChange={handleFiltersChange}
            churches={data}
            selection={selection}
            onClose={onClose}
          />
        </Suspense>
      ) : (
        <>
          <CityMapExpandChip onClick={onOpen} buttonRef={expandRef} />
          {/* A phone pinches; its small box has no room to spare. */}
          <MapCornerControls
            map={map}
            zoom={isDesktop}
            className={CITY_MAP_ZOOM_CORNER_CLASS}
          />
        </>
      )}
    </>
  );
}
