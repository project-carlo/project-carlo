import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import type { ChurchSearchResult } from "../api";
import { FilterPanel } from "./FilterPanel";
import { FilterPills } from "./FilterPills";
import { Masthead } from "./Masthead";
import { ListIcon, SlidersHorizontalIcon } from "./icons";
import { SearchTypeahead } from "./SearchTypeahead";
import type { FilterState } from "./filterState";
import { useDocumentLinks } from "../lib/documentLinks";
import { isAboutPageEnabled } from "../lib/featureFlags";
import { CHURCH_INDEX_PATH } from "../lib/seo";
import { CHURCH_LIST } from "../copy";
import { EVENT_TYPE_LABELS } from "../constants/eventTypes";
import type { PlaceSearchResult } from "../placeSearch";

const aboutPageEnabled = isAboutPageEnabled();

interface MapOverlayProps {
  isDesktop: boolean;
  /** The filter panel's selection, as it's being changed. */
  filters: FilterState;
  /** The selection the map shows, summarized under the search box. */
  appliedFilters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  resultCount?: number;
  filterPanelOpen: boolean;
  onFilterPanelOpenChange: (open: boolean) => void;
  onChurchSelect: (church: ChurchSearchResult) => void;
  onPlaceSelect: (place: PlaceSearchResult) => void;
  pinnedPlaceTitle?: string;
  onClearPlace: () => void;
  /** Lines under the search box, above a pinned place's. */
  children?: ReactNode;
}

/**
 * What floats over a full-window map: the card with the masthead, search and
 * filter summary, and the filter panel (a column under it on desktop, a sheet
 * on a phone). The home map and the city page's open map share it.
 *
 * The parts that cover the map carry `data-map-overlay`, so the map can
 * centre what it zooms to in the ground they leave clear; the phone's filter
 * sheet blocks the map while it's open, so it isn't marked.
 *
 * On a phone the card is kept short for the map's sake: the wordmark and the
 * links share one line, and the filter button names what the map shows.
 */
export function MapOverlay({
  isDesktop,
  filters,
  appliedFilters,
  onFiltersChange,
  resultCount,
  filterPanelOpen,
  onFilterPanelOpenChange,
  onChurchSelect,
  onPlaceSelect,
  pinnedPlaceTitle,
  onClearPlace,
  children,
}: MapOverlayProps) {
  const documentLinks = useDocumentLinks();
  const eventLabel = EVENT_TYPE_LABELS[appliedFilters.eventType];
  return (
    <div className="pointer-events-none absolute inset-x-0 top-0 bottom-0 z-[900] flex justify-center px-4 pt-[calc(1rem+var(--safe-area-inset-top))] pb-[calc(1rem+var(--safe-area-inset-bottom))] md:justify-start md:px-6 md:pt-6 md:pb-6">
      <div className="pointer-events-none flex w-full max-w-[28rem] flex-col gap-4">
        <div
          data-map-overlay
          className="pointer-events-auto rise-in shrink-0 border border-rule-strong bg-paper/96 px-4 pt-3 pb-3 shadow-missal-floating backdrop-blur-sm md:px-6 md:pt-5 md:pb-4"
        >
          <Masthead
            aside={
              // Beside the wordmark only, so the tagline keeps one line. The
              // index is also the homepage's one crawlable path into the
              // church and city pages. On a phone the links sit in a row,
              // level with the wordmark, so the card stays one line deep.
              <div className="flex shrink-0 items-center gap-3 md:mt-1 md:flex-col md:items-end md:gap-1">
                <Link
                  to={CHURCH_INDEX_PATH}
                  reloadDocument={documentLinks}
                  className="rubric-link font-serif text-[0.9375rem]"
                >
                  <ListIcon aria-hidden className="size-3.5 self-center md:hidden" />
                  {CHURCH_LIST}
                </Link>
                {aboutPageEnabled ? (
                  <Link
                    to="/about"
                    reloadDocument={documentLinks}
                    className="rubric-link font-serif text-[0.9375rem]"
                  >
                    About
                  </Link>
                ) : null}
              </div>
            }
          />
          <div className="mt-3 md:mt-5">
            <SearchTypeahead
              hideModeToggle
              placePlaceholder={
                isDesktop ? undefined : "City, ZIP, or address…"
              }
              onChurchSelect={onChurchSelect}
              onPlaceSelect={onPlaceSelect}
              filterButton={
                // A button, not a link, and named for what the map shows, so
                // it's plain both that it's a control and what it controls.
                // No chevron: it opens a sheet, not a menu under it.
                <button
                  type="button"
                  onClick={() => onFilterPanelOpenChange(true)}
                  aria-label={`Filters: ${eventLabel}`}
                  className="missal-focus ml-1 inline-flex h-8 items-center gap-1.5 border border-rule-strong bg-paper px-2.5 whitespace-nowrap font-serif text-[0.9375rem] text-rubric transition-colors hover:text-rubric-deep md:hidden"
                >
                  <SlidersHorizontalIcon aria-hidden className="size-3.5" />
                  {eventLabel}
                </button>
              }
            />
          </div>
          {children}
          {pinnedPlaceTitle ? (
            <div className="mt-3 flex items-center justify-between gap-3 font-serif text-[0.9375rem]">
              <span className="min-w-0 truncate text-ink-soft">
                Pinned: <span className="text-ink">{pinnedPlaceTitle}</span>
              </span>
              <button
                type="button"
                onClick={onClearPlace}
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
            onClose={() => onFilterPanelOpenChange(false)}
            filters={filters}
            onChange={onFiltersChange}
            resultCount={resultCount}
          />
        </div>
      </div>
    </div>
  );
}
