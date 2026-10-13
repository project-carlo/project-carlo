import {
  startTransition,
  useEffect,
  useMemo,
  useRef,
  useState,
  useCallback,
} from "react";
import { useLocation, useNavigation, useSearchParams } from "react-router-dom";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import type { Map as LeafletMap } from "leaflet";
import { fetchAllChurchesForSearch, fetchChurches } from "../api";
import { ChurchMap } from "../components/ChurchMap";
import {
  FULL_WINDOW_CORNER_CLASS,
  MapCornerControls,
} from "../components/MapCornerControls";
import { MapOverlay } from "../components/MapOverlay";
import {
  churchFiltersFor,
  filtersEqual,
  type FilterState,
} from "../components/filterState";
import { InlineQueryError } from "../components/InlineQueryError";
import { DESKTOP_MIN_WIDTH, useMinWidth } from "../hooks/useMinWidth";
import { useFilterUrlState } from "../hooks/useFilterUrlState";
import { useDocumentMeta } from "../hooks/useDocumentMeta";
import { rememberHomeSearch } from "../hooks/useHomeHref";
import {
  decodeMapViewFromParams,
  encodeMapViewToParams,
  type MapView,
} from "../lib/mapView";
import { fetchApproximateLocation } from "../lib/approximateLocation";
import { firstVisitStart, type MapStart } from "../lib/mapStart";
import { useBrowserLocation } from "../hooks/useBrowserLocation";
import { useMapSelection } from "../hooks/useMapSelection";
import { useChurchesInView } from "../hooks/useChurchesInView";
import { currentLocationPlace } from "../placeSearch";
import { FINDING_YOUR_LOCATION, USE_MY_LOCATION } from "../copy";
import { HOME_DESCRIPTION, HOME_TITLE, canonicalForPath } from "../lib/seo";

/** Map-centering payload accepted on navigation (e.g. via router state from the landing page). */
export interface HomeMapCenter {
  lat: number;
  lng: number;
  churchId?: number;
  placeTitle?: string;
  placeSubtitle?: string | null;
  openPlacePopup?: boolean;
  zoom?: number;
}

interface HomeNavState {
  centerOn?: HomeMapCenter;
}

/** A query string with the map's camera put in, when there is one to put. */
function withMapView(search: string, view: MapView | null): string {
  if (!view) return search;
  return `?${encodeMapViewToParams(view, new URLSearchParams(search))}`;
}

/**
 * Puts the camera into the map's history entry without telling the router,
 * for when a router navigation is under way: a second one would cancel it.
 * Does nothing once the next page's entry has replaced the map's.
 */
function writeViewToHistoryEntry(view: MapView): void {
  const { pathname, search, hash } = window.location;
  if (pathname !== "/") return;
  window.history.replaceState(
    window.history.state,
    "",
    pathname + withMapView(search, view) + hash,
  );
}

export function HomePage() {
  useDocumentMeta({
    title: HOME_TITLE,
    description: HOME_DESCRIPTION,
    canonicalUrl: canonicalForPath("/"),
  });

  const [urlFilters, setUrlFilters] = useFilterUrlState();
  const [appliedFilters, setAppliedFilters] = useState<FilterState>(
    () => urlFilters,
  );
  const [filters, setFilters] = useState<FilterState>(() => urlFilters);

  // Track the last value we wrote into (or read from) the URL so we can
  // distinguish our own echoed URL updates from genuine external ones
  // (back/forward, hand-edited URL). This avoids a render whip-back when
  // our own debounced write returns through useSearchParams.
  const lastSyncedRef = useRef<FilterState>(urlFilters);
  const appliedFiltersRef = useRef<FilterState>(appliedFilters);
  appliedFiltersRef.current = appliedFilters;

  // External URL changes → in-memory state.
  useEffect(() => {
    if (
      filtersEqual(urlFilters, lastSyncedRef.current) &&
      filtersEqual(appliedFiltersRef.current, lastSyncedRef.current)
    ) {
      return;
    }
    lastSyncedRef.current = urlFilters;
    setAppliedFilters(urlFilters);
    setFilters(urlFilters);
  }, [urlFilters]);

  // In-memory changes → URL after a long quiet period. The URL is for
  // refresh/share durability, not realtime sync, so a generous debounce
  // keeps history.replaceState (and any browser-side side effects like
  // favicon refetches) from running during continuous interaction.
  useEffect(() => {
    if (filtersEqual(appliedFilters, lastSyncedRef.current)) return;
    const id = window.setTimeout(() => {
      lastSyncedRef.current = appliedFilters;
      setUrlFilters(appliedFilters);
    }, 800);
    return () => window.clearTimeout(id);
  }, [appliedFilters, setUrlFilters]);

  // Map camera persistence. The map mounts at the view encoded in the URL (if
  // any) and writes the view back as the user pans/zooms, so it survives a trip
  // to a church page and back. Captured once on mount — MapContainer only reads
  // its initial center/zoom, so later URL edits shouldn't yank a live map.
  const [, setSearchParams] = useSearchParams();
  const location = useLocation();
  const [urlMapView] = useState<MapView | null>(() =>
    decodeMapViewFromParams(new URLSearchParams(window.location.search)),
  );

  // A first visit (no view in the URL, nothing to fly to from the landing
  // page) starts near where the visitor's IP address puts them, zoomed out
  // because the estimate can be well off, or else on the whole area the site
  // covers. The map waits for the estimate, which is capped at a short
  // timeout, rather than jump once it arrives.
  const [wantsFirstVisitStart] = useState(
    () =>
      urlMapView == null &&
      !(location.state as HomeNavState | null)?.centerOn,
  );
  const { data: approximateLocation, isPending: approximatePending } =
    useQuery({
      queryKey: ["approximate-location"],
      queryFn: ({ signal }) => fetchApproximateLocation(signal),
      enabled: wantsFirstVisitStart,
      staleTime: Infinity,
      retry: false,
    });
  const approximateSettled = !wantsFirstVisitStart || !approximatePending;
  // Every church, not just the ones the filters leave: the start mustn't
  // depend on the filters in a link. The search box shares this query.
  const { data: allChurches } = useQuery({
    queryKey: ["church-search-index"],
    queryFn: fetchAllChurchesForSearch,
    staleTime: 5 * 60 * 1000,
    enabled: wantsFirstVisitStart,
  });
  const mapViewTimerRef = useRef<number | null>(null);
  // The camera as of the last pan/zoom. The URL only catches up after the
  // debounce below, so anything that needs the view now reads it from here.
  const latestMapViewRef = useRef<MapView | null>(null);
  // Set while the router is on its way to another page; see below.
  const leavingRef = useRef(false);
  const handleMapViewChange = useCallback(
    (view: MapView) => {
      latestMapViewRef.current = view;
      rememberHomeSearch(withMapView(window.location.search, view));
      if (mapViewTimerRef.current != null) {
        window.clearTimeout(mapViewTimerRef.current);
      }
      // Short debounce: moveend already fires once movement settles, so this
      // just coalesces a flurry of zoom steps into one history.replaceState.
      mapViewTimerRef.current = window.setTimeout(() => {
        mapViewTimerRef.current = null;
        if (leavingRef.current) {
          writeViewToHistoryEntry(view);
        } else {
          setSearchParams((prev) => encodeMapViewToParams(view, prev), {
            replace: true,
          });
        }
      }, 400);
    },
    [setSearchParams],
  );
  useEffect(
    () => () => {
      if (mapViewTimerRef.current != null) {
        window.clearTimeout(mapViewTimerRef.current);
      }
    },
    [],
  );

  // On the way to another page (a link from the map, say "Church list"), a
  // view still waiting on the debounce goes into this page's history entry
  // at once, around the router: through it, it would cancel the page change.
  // Back then returns to the map as it was left.
  const navigation = useNavigation();
  const leaving =
    navigation.state !== "idle" &&
    navigation.location.pathname !== location.pathname;
  useEffect(() => {
    leavingRef.current = leaving;
    if (!leaving || mapViewTimerRef.current == null) return;
    window.clearTimeout(mapViewTimerRef.current);
    mapViewTimerRef.current = null;
    if (latestMapViewRef.current) {
      writeViewToHistoryEntry(latestMapViewRef.current);
    }
  }, [leaving]);

  // Mirror the query string, with the latest view, into sessionStorage so
  // in-app "Map" links (plain pushes to "/") can restore the current filters
  // + view, even when the page is left before the view reaches the URL.
  useEffect(() => {
    rememberHomeSearch(withMapView(location.search, latestMapViewRef.current));
  }, [location.search]);

  const [filterPanelOpen, setFilterPanelOpen] = useState(false);
  const isDesktop = useMinWidth(DESKTOP_MIN_WIDTH);
  const [map, setMap] = useState<LeafletMap | null>(null);
  // The place the IP estimate named, shown in the card with the offer of an
  // exact location until the visitor picks somewhere themselves.
  const [approximateArea, setApproximateArea] = useState<string | null>(null);
  const {
    centerOn,
    center,
    selectChurch: handleChurchSelect,
    selectPlace: handlePlaceSelect,
    clearPlace: handleClearPlace,
  } = useMapSelection(useCallback(() => setApproximateArea(null), []));

  // Hydrate initial centering from router state (e.g. landing page navigation),
  // then clear the state via history.replaceState so a hard refresh
  // doesn't re-apply stale centering.
  const hydratedFromStateRef = useRef(false);
  useEffect(() => {
    if (hydratedFromStateRef.current) return;
    hydratedFromStateRef.current = true;
    const incoming = (location.state as HomeNavState | null)?.centerOn;
    if (!incoming) return;
    center(incoming);
    window.history.replaceState(
      null,
      "",
      location.pathname + location.search,
    );
  }, [location.pathname, location.search, location.state, center]);

  const apiFilters = useMemo(
    () => churchFiltersFor(appliedFilters),
    [appliedFilters],
  );

  const { data, error, refetch } = useQuery({
    queryKey: ["churches", apiFilters],
    queryFn: () => fetchChurches(apiFilters),
    placeholderData: keepPreviousData,
  });

  // Where the map mounts, settled once (on a first visit) every church and
  // the IP estimate are in, then left alone: MapContainer reads it only once.
  // `undefined` is still settling; null is the map's built-in default, which
  // a fly-to from the landing page leaves at once. An estimate with no church
  // anywhere near it gives way to the whole covered area rather than open
  // on an empty map.
  const [mapStart, setMapStart] = useState<MapStart | null | undefined>(() => {
    if (wantsFirstVisitStart) return undefined;
    return urlMapView ? { kind: "view", view: urlMapView } : null;
  });
  useEffect(() => {
    if (mapStart !== undefined || !allChurches || !approximateSettled) return;
    const start = firstVisitStart(
      approximateLocation ?? null,
      allChurches,
      isDesktop,
    );
    setMapStart(start);
    if (start?.kind === "near" && approximateLocation) {
      setApproximateArea(approximateLocation.label);
    }
  }, [mapStart, allChurches, approximateSettled, approximateLocation, isDesktop]);

  // Filters apply as they change on every viewport, so the panel never shows
  // a selection the map isn't using.
  const handleFiltersChange = useCallback((next: FilterState) => {
    // Slider thumb / button highlight stays urgent so the input feels
    // pinned to the cursor; the downstream query + map rerender is a
    // transition, which lets newer drag values pre-empt in-flight work.
    setFilters(next);
    startTransition(() => setAppliedFilters(next));
  }, []);

  // "Use my location": the browser's position, pinned and flown to
  // like a searched place.
  const {
    status: locateStatus,
    error: locateError,
    request: handleLocate,
  } = useBrowserLocation(
    useCallback(
      ({ lat, lng }) => handlePlaceSelect(currentLocationPlace(lat, lng)),
      [handlePlaceSelect],
    ),
  );

  // The phone's filter sheet counts only the churches it will show.
  const churchesInView = useChurchesInView(
    map,
    data,
    filterPanelOpen && !isDesktop,
  );

  const pinnedPlaceTitle = centerOn?.placeTitle;
  const mapReady = data != null && mapStart !== undefined;

  return (
    <main
      className="fixed inset-x-0 top-0 flex h-dvh flex-col overflow-hidden bg-paper"
    >
      {/* The page is `fixed` so it adds nothing to the document's scrollable
       *  overflow: the document can't scroll under the phone browser bar, yet
       *  stays a normal root scroller, which Chrome needs for pull-to-refresh
       *  (overflow: hidden or overscroll-behavior: none on html/body kill it).
       *  Only the floating card can start a refresh; the map owns its touches. */}
      {/* Full-bleed map — no z-index so it doesn't create a stacking context;
       *  the elevated popup pane inside can then layer above the header. */}
      <div className="absolute inset-0">
        {mapReady ? (
          <ChurchMap
            churches={data}
            centerOn={centerOn}
            start={mapStart}
            onViewChange={handleMapViewChange}
            onClearPlace={handleClearPlace}
            mapRef={setMap}
          />
        ) : null}
      </div>

      {/* Initial load only — filter changes keep the map mounted via placeholderData */}
      {!mapReady && !error ? (
        <div className="pointer-events-none absolute inset-0 z-[800] flex items-center justify-center">
          <div className="pointer-events-auto flex items-center gap-3 border border-rule-strong bg-paper/95 px-5 py-3 shadow-missal-loading">
            <span
              className="h-2 w-2 animate-pulse rounded-full bg-rubric"
              aria-hidden
            />
            <span className="font-serif text-sm text-ink-soft">
              Loading map…
            </span>
          </div>
        </div>
      ) : null}
      {error ? (
        <div className="pointer-events-none absolute inset-0 z-[800] flex items-center justify-center p-4">
          <div className="pointer-events-auto max-w-sm border border-rule-strong bg-paper/95 px-6 py-5 shadow-missal-overlay">
            <InlineQueryError
              title="Couldn’t load churches"
              message="Check your connection and try again."
              onRetry={() => refetch()}
              centered
            />
          </div>
        </div>
      ) : null}

      {/* Floating card — masthead, search, filter pills; filter panel is only as tall
       *  as its content on md+ (capped + scroll inside when needed). */}
      <MapOverlay
        isDesktop={isDesktop}
        filters={filters}
        appliedFilters={appliedFilters}
        onFiltersChange={handleFiltersChange}
        resultCount={churchesInView}
        filterPanelOpen={filterPanelOpen}
        onFilterPanelOpenChange={setFilterPanelOpen}
        onChurchSelect={handleChurchSelect}
        onPlaceSelect={handlePlaceSelect}
        pinnedPlaceTitle={pinnedPlaceTitle}
        onClearPlace={handleClearPlace}
      >
        {approximateArea && !pinnedPlaceTitle ? (
          <div className="mt-3 flex items-baseline justify-between gap-3 font-serif text-[0.9375rem]">
            {/* An error wraps rather than truncate: it says what to do. */}
            <span
              className={`min-w-0 text-ink-soft ${locateError ? "" : "truncate"}`}
            >
              {locateError ? (
                locateError
              ) : (
                <>
                  Near <span className="text-ink">{approximateArea}</span>
                  {/* Phones haven't the width: it would only be cut off. */}
                  <span className="hidden italic md:inline">
                    {" "}
                    · approximate
                  </span>
                </>
              )}
            </span>
            <button
              type="button"
              onClick={handleLocate}
              disabled={locateStatus === "requesting"}
              className="rubric-link missal-focus shrink-0 disabled:cursor-wait"
            >
              {locateStatus === "requesting"
                ? FINDING_YOUR_LOCATION
                : USE_MY_LOCATION}
            </button>
          </div>
        ) : null}
      </MapOverlay>

      {/* The corner controls, bottom right above the map attribution: zoom on
       *  desktop (a phone pinches), and the locate button. Not a
       *  `data-map-overlay`: they're corner buttons, not a panel the map
       *  should centre around. */}
      {mapReady ? (
        <MapCornerControls
          map={map}
          zoom={isDesktop}
          locate={{
            status: locateStatus,
            // The card's line already says why, when it's showing.
            error: approximateArea && !pinnedPlaceTitle ? null : locateError,
            onLocate: handleLocate,
          }}
          className={FULL_WINDOW_CORNER_CLASS}
        />
      ) : null}
    </main>
  );
}
