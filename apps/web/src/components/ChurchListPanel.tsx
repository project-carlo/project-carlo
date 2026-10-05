import {
  useCallback,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent,
  type ReactNode,
} from "react";
import type { ChurchMapItem } from "../types";
import { useNow } from "../hooks/useNow";
import type { MobileView } from "../hooks/useListUrlState";
import {
  boundsCenter,
  boundsMoved,
  buildRows,
  nearestRow,
  sortRows,
  type GeoBounds,
  type ListSort,
} from "../lib/churchList";
import { ChurchList } from "./ChurchList";
import { MapListToggle } from "./MapListToggle";
import {
  DEFAULT_FILTER_STATE,
  type FilterState,
} from "./filterState";

export interface MapResultsProps {
  /** Churches matching the filters (what the map draws); undefined while loading. */
  churches: ChurchMapItem[] | undefined;
  /** Mapped churches matching the filters, anywhere. */
  totalCount: number | undefined;
  /** The ground the map shows clear of the floating UI; null until the map is up. */
  bounds: GeoBounds | null;
  /** The searched-place pin, which distances are measured from when there is one. */
  pin: { lat: number; lng: number; title: string } | null;
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  isDesktop: boolean;
  mobileView: MobileView;
  onMobileViewChange: (view: MobileView) => void;
  sort: ListSort;
  onSortChange: (sort: ListSort) => void;
  highlightedId: number | null;
  onHover: (churchId: number | null) => void;
  /** Centre the map on a church and open its popup. */
  onShowOnMap: (church: ChurchMapItem) => void;
  onZoomOut: () => void;
  /** The filter panel — a tab beside the results on desktop, a sheet on phones. */
  filterPanel: ReactNode;
}

type DesktopTab = "results" | "filters";

const TAB_IDS: Record<DesktopTab, { tab: string; panel: string }> = {
  results: { tab: "map-tab-results", panel: "map-panel-results" },
  filters: { tab: "map-tab-filters", panel: "map-panel-filters" },
};

/**
 * Everything the map page adds around its results list, in one place:
 *
 *  - desktop: a panel under the search card with "Results" / "Filters" tabs,
 *    plus "Search as I move the map";
 *  - phone: a full-screen list over the (still mounted) map, and the
 *    floating List / Map pill.
 *
 * The map page owns the camera, so this only reads the area (`bounds`) and
 * asks it to move (`onShowOnMap`, `onZoomOut`).
 */
export function MapResults({
  churches,
  totalCount,
  bounds,
  pin,
  filters,
  onFiltersChange,
  isDesktop,
  mobileView,
  onMobileViewChange,
  sort,
  onSortChange,
  highlightedId,
  onHover,
  onShowOnMap,
  onZoomOut,
  filterPanel,
}: MapResultsProps) {
  const now = useNow();
  const [tab, setTab] = useState<DesktopTab>("results");
  const [autoSearch, setAutoSearch] = useState(true);
  // With "search as I move" off, the area the list was last run for.
  const [frozen, setFrozen] = useState<GeoBounds | null>(null);

  // Phones have no side-by-side map, so their list always follows the camera.
  const following = !isDesktop || autoSearch || frozen == null;
  const area = following ? bounds : frozen;
  const mapMoved =
    isDesktop && !autoSearch && frozen != null && bounds != null
      ? boundsMoved(frozen, bounds)
      : false;

  const pinLat = pin?.lat;
  const pinLng = pin?.lng;
  const ref = useMemo(() => {
    if (pinLat != null && pinLng != null) return { lat: pinLat, lng: pinLng };
    return area ? boundsCenter(area) : null;
  }, [pinLat, pinLng, area]);

  const rows = useMemo(
    () =>
      churches && area
        ? sortRows(buildRows(churches, area, ref, now), sort)
        : [],
    [churches, area, ref, now, sort],
  );

  const nearestOutside = useMemo(
    () =>
      churches && ref && rows.length === 0 && churches.length > 0
        ? nearestRow(churches, ref, now)
        : null,
    [churches, ref, rows.length, now],
  );

  const handleAutoSearchChange = useCallback(
    (next: boolean) => {
      setAutoSearch(next);
      setFrozen(next ? null : bounds);
    },
    [bounds],
  );

  const handleClearTime = useCallback(
    () =>
      onFiltersChange({
        ...filters,
        timeFrom: DEFAULT_FILTER_STATE.timeFrom,
        timeTo: DEFAULT_FILTER_STATE.timeTo,
      }),
    [filters, onFiltersChange],
  );
  const handleClearDays = useCallback(
    () => onFiltersChange({ ...filters, daysOfWeek: [] }),
    [filters, onFiltersChange],
  );

  const handleShowOnMap = useCallback(
    (church: ChurchMapItem) => {
      // On a phone the list covers the map, so reveal it first. A push, so
      // Back returns to the list the person came from.
      if (!isDesktop) onMobileViewChange("map");
      onHover(null);
      onShowOnMap(church);
    },
    [isDesktop, onHover, onMobileViewChange, onShowOnMap],
  );

  const loading = churches === undefined || area === null;
  const distanceFrom = pin ? pin.title : "the map centre";

  const listProps = {
    rows,
    loading,
    totalCount,
    filters,
    sort,
    onSortChange,
    now,
    distanceFrom,
    highlightedId,
    onHover,
    onShowOnMap: handleShowOnMap,
    onZoomOut,
    onClearTime: handleClearTime,
    onClearDays: handleClearDays,
    nearestOutside,
  };

  // ------------------------------------------------------------- phone
  if (!isDesktop) {
    const listOpen = mobileView === "list";
    return (
      <>
        {listOpen ? (
          <>
            {/* Covers the map (which stays mounted beneath, keeping its
                camera) and sits under the search card. */}
            <div
              aria-hidden
              className="pointer-events-auto absolute inset-0 -z-10 bg-paper"
            />
            <section
              aria-label="Search results"
              className="pointer-events-auto -mx-4 flex min-h-0 flex-1 flex-col border-t border-rule-strong bg-paper"
            >
              <ChurchList {...listProps} bottomInset />
            </section>
          </>
        ) : null}
        <MapListToggle
          view={mobileView}
          onChange={onMobileViewChange}
          count={loading ? undefined : rows.length}
        />
        {filterPanel}
      </>
    );
  }

  // ----------------------------------------------------------- desktop
  const activeFilterCount =
    (filters.eventType !== DEFAULT_FILTER_STATE.eventType ? 1 : 0) +
    (filters.daysOfWeek.length > 0 ? 1 : 0) +
    (filters.timeFrom !== DEFAULT_FILTER_STATE.timeFrom ||
    filters.timeTo !== DEFAULT_FILTER_STATE.timeTo
      ? 1
      : 0);

  return (
    <div data-map-overlay className="pointer-events-auto flex min-h-0 w-full flex-col">
      <section className="rise-in flex min-h-0 flex-col overflow-hidden border border-rule-strong bg-paper/96 shadow-missal-panel backdrop-blur-sm">
        <DesktopTabs
          tab={tab}
          onTabChange={setTab}
          resultCount={loading ? undefined : rows.length}
          activeFilterCount={activeFilterCount}
        />
        {tab === "results" ? (
          <div
            role="tabpanel"
            id={TAB_IDS.results.panel}
            aria-labelledby={TAB_IDS.results.tab}
            className="flex min-h-0 max-h-full flex-1 flex-col"
          >
            <ChurchList
              {...listProps}
              onEditFilters={() => setTab("filters")}
              extras={
                <SearchAreaControls
                  autoSearch={autoSearch}
                  onAutoSearchChange={handleAutoSearchChange}
                  showSearchButton={mapMoved}
                  onSearchArea={() => setFrozen(bounds)}
                />
              }
            />
          </div>
        ) : (
          <div
            role="tabpanel"
            id={TAB_IDS.filters.panel}
            aria-labelledby={TAB_IDS.filters.tab}
            // The filter panel brings its own frame; inside a tab it only needs the content.
            className="min-h-0 flex-1 overflow-y-auto [&>section]:border-0 [&>section]:bg-transparent [&>section]:shadow-none"
          >
            {filterPanel}
          </div>
        )}
      </section>
    </div>
  );
}

// ------------------------------------------------------------ desktop bits

function DesktopTabs({
  tab,
  onTabChange,
  resultCount,
  activeFilterCount,
}: {
  tab: DesktopTab;
  onTabChange: (tab: DesktopTab) => void;
  resultCount: number | undefined;
  activeFilterCount: number;
}) {
  const refs = useRef<Record<DesktopTab, HTMLButtonElement | null>>({
    results: null,
    filters: null,
  });
  const order: DesktopTab[] = ["results", "filters"];

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
    event.preventDefault();
    const next = order[(order.indexOf(tab) + 1) % order.length];
    onTabChange(next);
    refs.current[next]?.focus();
  };

  return (
    <div
      role="tablist"
      aria-label="Results and filters"
      onKeyDown={handleKeyDown}
      className="flex shrink-0 border-b border-rule-strong"
    >
      {order.map((id) => {
        const selected = tab === id;
        return (
          <button
            key={id}
            ref={(node) => {
              refs.current[id] = node;
            }}
            type="button"
            role="tab"
            id={TAB_IDS[id].tab}
            aria-selected={selected}
            aria-controls={TAB_IDS[id].panel}
            tabIndex={selected ? 0 : -1}
            onClick={() => onTabChange(id)}
            className={`missal-focus relative flex-1 px-4 py-3 text-center font-display text-[1.05rem] transition-colors ${
              selected
                ? "text-rubric"
                : "text-ink-soft hover:bg-paper-deep/40 hover:text-ink"
            }`}
          >
            {id === "results" ? "Results" : "Filters"}
            {id === "results" && resultCount != null ? (
              <span className="ml-2 font-serif text-[0.875rem] tabular-nums text-ink-faint">
                {resultCount}
              </span>
            ) : null}
            {id === "filters" && activeFilterCount > 0 ? (
              <span className="ml-2 font-serif text-[0.875rem] tabular-nums text-ink-faint">
                {activeFilterCount}
              </span>
            ) : null}
            <span
              aria-hidden
              className={`absolute inset-x-0 -bottom-px h-[2px] bg-rubric transition-opacity ${
                selected ? "opacity-100" : "opacity-0"
              }`}
            />
          </button>
        );
      })}
    </div>
  );
}

function SearchAreaControls({
  autoSearch,
  onAutoSearchChange,
  showSearchButton,
  onSearchArea,
}: {
  autoSearch: boolean;
  onAutoSearchChange: (next: boolean) => void;
  showSearchButton: boolean;
  onSearchArea: () => void;
}) {
  return (
    <div className="mt-3 flex min-h-[2rem] flex-wrap items-center justify-between gap-x-4 gap-y-2">
      <label className="flex cursor-pointer items-center gap-2 font-serif text-[0.9375rem] text-ink-soft">
        <input
          type="checkbox"
          checked={autoSearch}
          onChange={(event) => onAutoSearchChange(event.target.checked)}
          className="missal-focus h-4 w-4 cursor-pointer accent-[var(--rubric)]"
        />
        Search as I move the map
      </label>
      {showSearchButton ? (
        <button
          type="button"
          onClick={onSearchArea}
          className="missal-focus bg-rubric px-3 py-1.5 font-display text-[0.95rem] leading-none text-paper transition-colors hover:bg-rubric-deep"
        >
          Search this area
        </button>
      ) : null}
    </div>
  );
}
