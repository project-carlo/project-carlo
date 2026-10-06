import {
  startTransition,
  useEffect,
  useMemo,
  useRef,
  useState,
  useCallback,
} from "react";
import { Link, useLocation, useSearchParams } from "react-router-dom";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import {
  fetchAllChurchesForSearch,
  fetchChurches,
  type ChurchSearchResult,
} from "../api";
import { ChurchMap } from "../components/ChurchMap";
import { FilterPanel } from "../components/FilterPanel";
import { FilterPills } from "../components/FilterPills";
import { SearchTypeahead } from "../components/SearchTypeahead";
import { Masthead } from "../components/Masthead";
import {
  filtersEqual,
  getTimeRange,
  type FilterState,
} from "../components/filterState";
import { InlineQueryError } from "../components/InlineQueryError";
import { useMinWidth } from "../hooks/useMinWidth";
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
import { LocateButton } from "../components/LocateButton";
import {
  currentLocationPlace,
  PLACE_SEARCH_ZOOM,
  type PlaceSearchResult,
} from "../placeSearch";
import { isAboutPageEnabled } from "../lib/featureFlags";
import {
  CHURCH_INDEX_PATH,
  HOME_DESCRIPTION,
  HOME_TITLE,
  canonicalForPath,
} from "../lib/seo";

const aboutPageEnabled = isAboutPageEnabled();

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
  const handleMapViewChange = useCallback(
    (view: MapView) => {
      if (mapViewTimerRef.current != null) {
        window.clearTimeout(mapViewTimerRef.current);
      }
      // Short debounce: moveend already fires once movement settles, so this
      // just coalesces a flurry of zoom steps into one history.replaceState.
      mapViewTimerRef.current = window.setTimeout(() => {
        setSearchParams((prev) => encodeMapViewToParams(view, prev), {
          replace: true,
        });
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

  // Mirror the live query string into sessionStorage so in-app "Back to map"
  // links (plain pushes to "/") can restore the current filters + view.
  useEffect(() => {
    rememberHomeSearch(location.search);
  }, [location.search]);

  const [filterPanelOpen, setFilterPanelOpen] = useState(false);
  const isDesktop = useMinWidth(768);
  const [centerOn, setCenterOn] = useState<{
    lat: number;
    lng: number;
    churchId?: number;
    placeTitle?: string;
    placeSubtitle?: string | null;
    openPlacePopup?: boolean;
    zoom?: number;
    requestId: number;
  } | null>(null);
  // Monotonic id bumped on every church selection so that re-selecting the
  // same church still produces a distinct `centerOn` value, which the map
  // uses to re-pan and re-open the popup without a timer-based reset.
  const centerRequestIdRef = useRef(0);

  // Hydrate initial centering from router state (e.g. landing page navigation),
  // then clear the state via history.replaceState so a hard refresh
  // doesn't re-apply stale centering.
  const hydratedFromStateRef = useRef(false);
  useEffect(() => {
    if (hydratedFromStateRef.current) return;
    hydratedFromStateRef.current = true;
    const incoming = (location.state as HomeNavState | null)?.centerOn;
    if (!incoming) return;
    centerRequestIdRef.current += 1;
    setCenterOn({ ...incoming, requestId: centerRequestIdRef.current });
    window.history.replaceState(
      null,
      "",
      location.pathname + location.search,
    );
  }, [location.pathname, location.search, location.state]);

  const apiFilters = useMemo(() => {
    const { from, to } = getTimeRange(appliedFilters);
    return {
      types: [appliedFilters.eventType],
      daysOfWeek:
        appliedFilters.daysOfWeek.length > 0
          ? appliedFilters.daysOfWeek
          : undefined,
      timeFrom: from,
      timeTo: to,
    };
  }, [appliedFilters]);

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
  // The place the IP estimate named, shown in the card with the offer of an
  // exact location until the visitor picks somewhere themselves.
  const [approximateArea, setApproximateArea] = useState<string | null>(null);
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

  // Churches without coordinates aren't on the map, so they don't count.
  const mappedChurchCount = useMemo(
    () =>
      data?.filter(
        (church) => church.latitude !== null && church.longitude !== null,
      ).length,
    [data],
  );

  // Filters apply as they change on every viewport, so the panel never shows
  // a selection the map isn't using.
  const handleFiltersChange = useCallback((next: FilterState) => {
    // Slider thumb / button highlight stays urgent so the input feels
    // pinned to the cursor; the downstream query + map rerender is a
    // transition, which lets newer drag values pre-empt in-flight work.
    setFilters(next);
    startTransition(() => setAppliedFilters(next));
  }, []);

  const handleChurchSelect = useCallback((church: ChurchSearchResult) => {
    if (church.latitude != null && church.longitude != null) {
      setApproximateArea(null);
      centerRequestIdRef.current += 1;
      setCenterOn({
        lat: church.latitude,
        lng: church.longitude,
        churchId: church.id,
        requestId: centerRequestIdRef.current,
      });
    }
  }, []);

  const handlePlaceSelect = useCallback((place: PlaceSearchResult) => {
    setApproximateArea(null);
    centerRequestIdRef.current += 1;
    setCenterOn({
      lat: place.lat,
      lng: place.lng,
      placeTitle: place.title,
      placeSubtitle: place.subtitle,
      // The visitor's own position is pinned quietly; its popup opens on a click.
      openPlacePopup: !place.isCurrentLocation,
      zoom: PLACE_SEARCH_ZOOM,
      requestId: centerRequestIdRef.current,
    });
  }, []);

  // Removes the searched-place pin. A selected church shares `centerOn` but
  // isn't a pin, so it's left alone.
  const handleClearPlace = useCallback(() => {
    setCenterOn((current) => (current?.placeTitle ? null : current));
  }, []);

  // "Go to my exact location": the browser's position, pinned and flown to
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
              title={"Couldn't load data"}
              message="Check your connection and try again."
              onRetry={() => refetch()}
              centered
            />
          </div>
        </div>
      ) : null}

      {/* Floating card — masthead, search, filter pills; filter panel is only as tall
       *  as its content on md+ (capped + scroll inside when needed). The parts
       *  that cover the map carry `data-map-overlay`, so the map can centre
       *  what it zooms to in the ground they leave clear; the phone's filter
       *  sheet blocks the map while it's open, so it isn't marked. */}
      <div className="pointer-events-none absolute inset-x-0 top-0 bottom-0 z-[900] flex justify-center px-4 pt-[calc(1rem+var(--safe-area-inset-top))] pb-[calc(1rem+var(--safe-area-inset-bottom))] md:justify-start md:px-6 md:pt-6 md:pb-6">
        <div className="pointer-events-none flex w-full max-w-[28rem] flex-col gap-4">
          <div
            data-map-overlay
            className="pointer-events-auto rise-in shrink-0 border border-rule-strong bg-paper/96 px-6 pt-5 pb-4 shadow-missal-floating backdrop-blur-sm"
          >
            <Masthead
              aside={
                // Beside the wordmark only, so the tagline keeps one line.
                // A plain link, not a router Link: /churches/ is a prerendered
                // page with no SPA route. It's also the homepage's one
                // crawlable path into the church and city pages.
                <div className="mt-1 flex shrink-0 flex-col items-end gap-1">
                  <a
                    href={CHURCH_INDEX_PATH}
                    className="rubric-link font-serif text-[0.9375rem]"
                  >
                    All churches
                  </a>
                  {aboutPageEnabled ? (
                    <Link
                      to="/about"
                      className="rubric-link font-serif text-[0.9375rem]"
                    >
                      About
                    </Link>
                  ) : null}
                </div>
              }
            />
            <div className="mt-5">
              <SearchTypeahead
                hideModeToggle
                onChurchSelect={handleChurchSelect}
                onPlaceSelect={handlePlaceSelect}
                filterButton={
                  <button
                    type="button"
                    onClick={() => setFilterPanelOpen(true)}
                    aria-label="Open filters"
                    data-active={filterPanelOpen}
                    className="rubric-link ml-1 whitespace-nowrap font-serif text-[0.9375rem] md:hidden"
                  >
                    Filters
                  </button>
                }
              />
            </div>
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
                    ? "Locating…"
                    : "Use exact location"}
                </button>
              </div>
            ) : null}
            {pinnedPlaceTitle ? (
              <div className="mt-3 flex items-center justify-between gap-3 font-serif text-[0.9375rem]">
                <span className="min-w-0 truncate text-ink-soft">
                  Pinned: <span className="text-ink">{pinnedPlaceTitle}</span>
                </span>
                <button
                  type="button"
                  onClick={handleClearPlace}
                  aria-label={`Remove pin for ${pinnedPlaceTitle}`}
                  className="rubric-link missal-focus shrink-0"
                >
                  Remove pin
                </button>
              </div>
            ) : null}
            <FilterPills filters={appliedFilters} />
          </div>

          <div
            data-map-overlay={isDesktop ? true : undefined}
            className={`w-full md:min-h-0 ${
              !isDesktop && !filterPanelOpen
                ? "pointer-events-none"
                : "pointer-events-auto"
            }`}
          >
            <FilterPanel
              isOpen={!isDesktop && filterPanelOpen}
              isDesktop={isDesktop}
              onClose={() => setFilterPanelOpen(false)}
              filters={filters}
              onChange={handleFiltersChange}
              resultCount={mappedChurchCount}
            />
          </div>
        </div>
      </div>

      {/* The locate control, bottom right above the map attribution. Not a
       *  `data-map-overlay`: it's a corner button, not a panel the map
       *  should centre around. */}
      {mapReady ? (
        <div className="pointer-events-none absolute right-4 bottom-[calc(2.25rem+var(--safe-area-inset-bottom))] left-4 z-[900] md:right-6">
          <div className="pointer-events-auto ml-auto w-fit">
            <LocateButton
              status={locateStatus}
              // The card's line already says why, when it's showing.
              error={approximateArea && !pinnedPlaceTitle ? null : locateError}
              onLocate={handleLocate}
            />
          </div>
        </div>
      ) : null}
    </main>
  );
}
