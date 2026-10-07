import { useCallback, useEffect, useRef, useState } from "react";
import type { Map as LeafletMap } from "leaflet";
import { FilterPanel } from "./FilterPanel";
import { FULL_WINDOW_CORNER_CLASS, MapCornerControls } from "./MapCornerControls";
import { MapOverlay } from "./MapOverlay";
import { filtersEqual, DEFAULT_FILTER_STATE, type FilterState } from "./filterState";
import { SlidersHorizontalIcon, XIcon } from "@/components/icons";
import { useBrowserLocation } from "@/hooks/useBrowserLocation";
import type { useMapSelection } from "@/hooks/useMapSelection";
import { CITY_MAP_CHIP_CLASS } from "@/lib/cityMap";
import { currentLocationPlace } from "../placeSearch";

const noop = () => {};

/**
 * The city page's map, open over the whole window. On a desktop it's the
 * home map's view (search, filters, zoom and locate) with a Close button; on
 * a phone, a Filters button that opens the home map's filter sheet, Close,
 * and zoom buttons where the home map keeps its locate button.
 */
export default function CityMapOpenControls({
  isDesktop,
  map,
  filters,
  appliedFilters,
  onFiltersChange,
  resultCount,
  selection,
  onClose,
}: {
  isDesktop: boolean;
  map: LeafletMap | null;
  filters: FilterState;
  appliedFilters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  resultCount?: number;
  selection: ReturnType<typeof useMapSelection>;
  onClose: () => void;
}) {
  const [filterPanelOpen, setFilterPanelOpen] = useState(false);
  const { selectChurch, selectPlace, clearPlace, centerOn } = selection;
  const {
    status: locateStatus,
    error: locateError,
    request: handleLocate,
  } = useBrowserLocation(
    useCallback(
      ({ lat, lng }) => selectPlace(currentLocationPlace(lat, lng)),
      [selectPlace],
    ),
  );

  // Focus starts on Close, as the map opens.
  const closeRef = useRef<HTMLButtonElement>(null);
  useEffect(() => closeRef.current?.focus(), []);

  const closeButton = (
    <button
      ref={closeRef}
      type="button"
      onClick={onClose}
      className={`${CITY_MAP_CHIP_CLASS} pointer-events-auto shrink-0 py-2`}
    >
      <XIcon className="size-4" />
      Close
    </button>
  );

  if (isDesktop) {
    return (
      <>
        <MapOverlay
          isDesktop
          filters={filters}
          appliedFilters={appliedFilters}
          onFiltersChange={onFiltersChange}
          resultCount={resultCount}
          filterPanelOpen={false}
          onFilterPanelOpenChange={noop}
          onChurchSelect={selectChurch}
          onPlaceSelect={selectPlace}
          pinnedPlaceTitle={centerOn?.placeTitle}
          onClearPlace={clearPlace}
        />
        <div className="absolute top-6 right-6 z-[950]">{closeButton}</div>
        <MapCornerControls
          map={map}
          zoom
          locate={{
            status: locateStatus,
            error: locateError,
            onLocate: handleLocate,
          }}
          className={FULL_WINDOW_CORNER_CLASS}
        />
      </>
    );
  }

  const filtered = !filtersEqual(appliedFilters, DEFAULT_FILTER_STATE);
  return (
    <>
      <div className="pointer-events-none absolute inset-x-0 top-0 z-[950] flex items-start justify-between gap-3 px-4 pt-[calc(1rem+var(--safe-area-inset-top))]">
        <button
          type="button"
          onClick={() => setFilterPanelOpen(true)}
          aria-label={filtered ? "Filters (some applied)" : "Filters"}
          className={`${CITY_MAP_CHIP_CLASS} pointer-events-auto py-2`}
        >
          <SlidersHorizontalIcon className="size-4" />
          Filters
          {filtered ? (
            <span aria-hidden="true" className="size-1.5 rounded-full bg-rubric" />
          ) : null}
        </button>
        {closeButton}
      </div>
      <MapCornerControls map={map} zoom className={FULL_WINDOW_CORNER_CLASS} />
      <FilterPanel
        isOpen={filterPanelOpen}
        isDesktop={false}
        onClose={() => setFilterPanelOpen(false)}
        filters={filters}
        onChange={onFiltersChange}
        resultCount={resultCount}
      />
    </>
  );
}
