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
import { fetchChurches } from "../api";
import { ChurchMap } from "./ChurchMap";
import { MapCornerControls } from "./MapCornerControls";
import {
  churchFiltersFor,
  DEFAULT_FILTER_STATE,
  type FilterState,
} from "./filterState";
import { CityMapExpandChip } from "./CityMapExpandChip";
import { useMinWidth } from "@/hooks/useMinWidth";
import { useMapSelection } from "@/hooks/useMapSelection";
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
 * What CityMapLive shows: the home map's churches, pins and popups, opening
 * on the city preview's view. In the page it has Expand (and zoom buttons on
 * a desktop);
 * open, CityMapOpenControls adds the rest. The filters chosen there stay on
 * the map in the page. Loaded only once the page's map goes live, and the
 * open controls only once the churches are up.
 */
export default function CityMapView({
  view,
  open,
  onOpen,
  onClose,
  onReady,
}: {
  view: MapView;
  open: boolean;
  onOpen: () => void;
  onClose: () => void;
  /** Called once the churches are on the map. */
  onReady: () => void;
}) {
  const isDesktop = useMinWidth(768);
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
  const { data } = useQuery({
    queryKey: ["churches", apiFilters],
    queryFn: () => fetchChurches(apiFilters),
    placeholderData: keepPreviousData,
  });
  useEffect(() => {
    if (!data) return;
    onReady();
    void loadOpenControls();
  }, [data, onReady]);
  const mappedChurchCount = useMemo(
    () =>
      data?.filter(
        (church) => church.latitude !== null && church.longitude !== null,
      ).length,
    [data],
  );

  // Read once, on mount, like every start.
  const start = useMemo<MapStart>(() => ({ kind: "view", view }), [view]);

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
        start={start}
        centerOn={selection.centerOn}
        onClearPlace={selection.clearPlace}
        mapRef={setMap}
      >
        <MapMode open={open} />
      </ChurchMap>
      {open ? (
        <Suspense fallback={null}>
          <CityMapOpenControls
            isDesktop={isDesktop}
            map={map}
            filters={filters}
            appliedFilters={appliedFilters}
            onFiltersChange={handleFiltersChange}
            resultCount={mappedChurchCount}
            selection={selection}
            onClose={onClose}
          />
        </Suspense>
      ) : (
        <>
          <CityMapExpandChip onClick={onOpen} buttonRef={expandRef} />
          {/* A phone pinches; its small box has no room to spare. */}
          <MapCornerControls map={map} zoom={isDesktop} className="right-3 bottom-7" />
        </>
      )}
    </>
  );
}
