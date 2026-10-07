import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import type { ChurchSearchResult } from "../api";
import { FilterPanel } from "./FilterPanel";
import { FilterPills } from "./FilterPills";
import { Masthead } from "./Masthead";
import { SearchTypeahead } from "./SearchTypeahead";
import type { FilterState } from "./filterState";
import { useDocumentLinks } from "../lib/documentLinks";
import { isAboutPageEnabled } from "../lib/featureFlags";
import { CHURCH_INDEX_PATH } from "../lib/seo";
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
  return (
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
                    reloadDocument={documentLinks}
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
              onChurchSelect={onChurchSelect}
              onPlaceSelect={onPlaceSelect}
              filterButton={
                <button
                  type="button"
                  onClick={() => onFilterPanelOpenChange(true)}
                  aria-label="Open filters"
                  data-active={filterPanelOpen}
                  className="rubric-link ml-1 whitespace-nowrap font-serif text-[0.9375rem] md:hidden"
                >
                  Filters
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
