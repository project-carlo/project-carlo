import {
  useState,
  useEffect,
  useCallback,
  useMemo,
  useLayoutEffect,
  type RefObject,
  useRef,
  type ReactNode,
} from "react";
import { Command as CommandPrimitive, useCommandState } from "cmdk";
import { useQuery } from "@tanstack/react-query";
import type FuseType from "fuse.js";
import type { ChurchSearchResult } from "../api";
import { churchSearchIndexQuery } from "../lib/homeStartQueries";
import { formatAddress } from "../utils";
import { wantsCurrentLocation } from "../lib/currentLocationQuery";
import { useBrowserLocation } from "../hooks/useBrowserLocation";
import { track } from "../lib/analytics";
import {
  canSearchPlaces,
  currentLocationPlace,
  PlaceSearchConfigurationError,
  searchPlaces,
  type PlaceSearchResult,
} from "../placeSearch";
import { SearchIcon, XIcon } from "@/components/icons";
import {
  FINDING_YOUR_LOCATION,
  UNNAMED_CHURCH,
  USE_MY_LOCATION,
} from "../copy";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverAnchor,
  PopoverContent,
} from "@/components/ui/popover";

const DEBOUNCE_MS = 200;
type SearchMode = "place" | "parish";

interface SearchTypeaheadProps {
  onChurchSelect: (church: ChurchSearchResult) => void;
  onPlaceSelect: (place: PlaceSearchResult) => void;
  filterButton: ReactNode;
  /** Hide the inline place/parish mode toggle. Defaults to false. */
  hideModeToggle?: boolean;
  /** Input/icon sizing variant. `md` (default) matches the map header; `lg` renders the hero size used on the landing page. */
  size?: "md" | "lg";
  /** The place search's placeholder, where the default won't fit. */
  placePlaceholder?: string;
}

export function SearchTypeahead({
  onChurchSelect,
  onPlaceSelect,
  filterButton,
  hideModeToggle = false,
  size = "md",
  placePlaceholder = "Search for a city, ZIP, or address…",
}: SearchTypeaheadProps) {
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [searchMode, setSearchMode] = useState<SearchMode>("place");
  const searchAnchorRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(query), DEBOUNCE_MS);
    return () => clearTimeout(t);
  }, [query]);

  const { data: allChurches = [], isLoading: churchesLoading } = useQuery(
    churchSearchIndexQuery,
  );

  const trimmedDebouncedQuery = debouncedQuery.trim();
  const shouldSearchPlaces =
    searchMode === "place" && canSearchPlaces(trimmedDebouncedQuery);
  const {
    data: placeResults = [],
    isLoading: placesLoading,
    error: placeError,
  } = useQuery({
    queryKey: ["place-search", trimmedDebouncedQuery],
    queryFn: ({ signal }) =>
      searchPlaces(trimmedDebouncedQuery, {
        signal,
      }),
    enabled: shouldSearchPlaces,
    staleTime: 10 * 60 * 1000,
    retry: false,
  });

  const FuseRef = useRef<typeof FuseType | null>(null);
  const [fuseReady, setFuseReady] = useState(false);

  useEffect(() => {
    import("fuse.js").then((m) => {
      FuseRef.current = m.default;
      setFuseReady(true);
    });
  }, []);

  const fuse = useMemo(() => {
    if (!fuseReady || !FuseRef.current) return null;
    return new FuseRef.current(
      allChurches.filter((c) => c.name),
      {
        keys: [
          { name: "name", weight: 0.62 },
          { name: "city", weight: 0.13 },
          { name: "state", weight: 0.08 },
          { name: "postal_code", weight: 0.08 },
          { name: "address_line1", weight: 0.07 },
          { name: "address_line2", weight: 0.02 },
        ],
        threshold: 0.4,
        includeScore: true,
      },
    );
  }, [fuseReady, allChurches]);

  const parishResults = useMemo(() => {
    if (searchMode !== "parish") return [];
    const trimmed = trimmedDebouncedQuery;
    if (trimmed.length < 2 || !fuse) return [];
    const matches = fuse.search(trimmed);
    return matches.slice(0, 10).map((m) => m.item);
  }, [fuse, searchMode, trimmedDebouncedQuery]);

  const isPlaceMode = searchMode === "place";
  const hasTypedQuery = query.trim().length > 0;
  // Offered on an empty field, and after that only when the query is asking
  // for it, so it doesn't top every list of place results.
  const showCurrentLocationOption = isPlaceMode && wantsCurrentLocation(query);
  // Place mode opens immediately so the current-location suggestion is the
  // default; parish mode still waits for enough text to search.
  const showDropdown =
    isOpen && (showCurrentLocationOption || query.trim().length >= 2);
  const showSearchStatus = !isPlaceMode || hasTypedQuery;
  const activeResults = isPlaceMode ? placeResults : parishResults;
  const hasResults = activeResults.length > 0;
  const isLoading = isPlaceMode ? placesLoading : churchesLoading;
  const heading = isPlaceMode ? "Places" : "Matching churches";
  const placeholder = isPlaceMode ? placePlaceholder : "Search for a church…";
  // "No results" only once a search has run on what's in the box: not while
  // the debounce lags the typing, and not for a query too short to search,
  // which would otherwise read as a search that found nothing.
  const searchSettled = debouncedQuery === query;
  const searchRan = isPlaceMode
    ? shouldSearchPlaces
    : trimmedDebouncedQuery.length >= 2 && fuse != null;
  // Echo what was searched, so a typo is easy to spot, and say what to try.
  const emptyMessage = !searchSettled
    ? null
    : !searchRan
      ? isPlaceMode
        ? "Keep typing a town, ZIP code, or address."
        : "Keep typing a church name."
      : isPlaceMode
        ? `No places match “${trimmedDebouncedQuery}”. Try a town name or ZIP code.`
        : `No churches match “${trimmedDebouncedQuery}”. Try fewer words, or part of the name.`;
  const modeButtonLabel = isPlaceMode ? "Search churches" : "Search places";
  const placeSearchNotConfigured =
    isPlaceMode && placeError instanceof PlaceSearchConfigurationError;

  const clearQuery = useCallback(() => {
    setQuery("");
    setDebouncedQuery("");
    setIsOpen(false);
  }, []);

  const handleChurchSelect = useCallback(
    (church: ChurchSearchResult) => {
      track("search_select", { kind: "church", target: church.slug });
      onChurchSelect(church);
      clearQuery();
    },
    [clearQuery, onChurchSelect],
  );

  const handlePlaceSelect = useCallback(
    (place: PlaceSearchResult) => {
      // Never the place itself: it could be where the visitor lives.
      track("search_select", { kind: "place" });
      onPlaceSelect(place);
      clearQuery();
    },
    [clearQuery, onPlaceSelect],
  );

  const {
    status: locationStatus,
    error: locationError,
    request: handleCurrentLocationSelect,
  } = useBrowserLocation(
    useCallback(
      ({ lat, lng }) => {
        onPlaceSelect(currentLocationPlace(lat, lng));
        clearQuery();
      },
      [clearQuery, onPlaceSelect],
    ),
  );

  const getChurchLocationText = useCallback((church: ChurchSearchResult) => {
    const address = formatAddress(church);
    if (address) return address;
    const stateZip = [church.state, church.postal_code].filter(Boolean).join(" ");
    return [church.city, stateZip].filter(Boolean).join(", ");
  }, []);

  const handleModeToggle = useCallback(
    () => {
      setSearchMode((current) => (current === "place" ? "parish" : "place"));
      setIsOpen(true);
    },
    [],
  );

  const inputLabel = isPlaceMode
    ? "Search for a city, ZIP code, or address"
    : "Search for a church by name";

  const inputRef = useRef<HTMLInputElement | null>(null);

  return (
    <Command
      shouldFilter={false}
      // cmdk names its input by a hidden label of its own (aria-labelledby),
      // which outranks aria-label, so the name has to go here.
      label={inputLabel}
      className="overflow-visible bg-transparent p-0"
    >
      <ComboboxAriaSync inputRef={inputRef} open={showDropdown} />
      <Popover open={showDropdown} onOpenChange={setIsOpen}>
        <PopoverAnchor asChild>
          <div ref={searchAnchorRef} className="relative w-full">
            <div
              className="missal-search-field group flex w-full items-center gap-2 rounded-sm border-b pb-1.5 transition-colors"
              style={{
                borderBottomColor: isFocused
                  ? "var(--rubric)"
                  : "var(--rule-strong)",
                borderBottomWidth: isFocused ? 1.5 : 1,
              }}
            >
              <SearchIcon
                className={`shrink-0 transition-colors ${
                  size === "lg" ? "size-[22px]" : "size-4"
                } ${isFocused ? "text-rubric" : "text-ink-soft"}`}
              />
              <CommandPrimitive.Input
                value={query}
                onValueChange={(value) => {
                  setQuery(value);
                  setIsOpen(true);
                }}
                onFocus={() => {
                  setIsFocused(true);
                  setIsOpen(true);
                }}
                onBlur={() => setIsFocused(false)}
                onKeyDown={(event) => {
                  if (event.key === "Escape") {
                    if (query.length > 0) {
                      clearQuery();
                    } else {
                      setIsOpen(false);
                    }
                  }
                }}
                placeholder={placeholder}
                ref={inputRef}
                autoComplete="off"
                className={`min-w-0 flex-1 bg-transparent font-serif text-ink outline-none placeholder:text-ink-soft placeholder:italic ${
                  size === "lg" ? "text-[1.375rem]" : "text-[1.0625rem]"
                }`}
              />
              {query.length > 0 ? (
                <button
                  type="button"
                  onClick={clearQuery}
                  aria-label="Clear search"
                  className="missal-focus flex size-6 shrink-0 items-center justify-center text-ink-soft transition-colors hover:text-rubric"
                >
                  <XIcon className="size-3.5" />
                </button>
              ) : null}
              {hideModeToggle ? null : (
                <button
                  type="button"
                  onClick={handleModeToggle}
                  className="rubric-link ml-1 hidden whitespace-nowrap font-serif text-[0.9375rem] sm:inline-flex"
                >
                  {modeButtonLabel}
                </button>
              )}
              <div className="shrink-0">{filterButton}</div>
            </div>
            {hideModeToggle ? null : (
              <button
                type="button"
                onClick={handleModeToggle}
                className="rubric-link mt-2 font-serif text-[0.9375rem] sm:hidden"
              >
                {modeButtonLabel}
              </button>
            )}
          </div>
        </PopoverAnchor>
        <PopoverContent
          align="start"
          side="bottom"
          sideOffset={10}
          avoidCollisions={false}
          // Matches the search field it drops out of. A fixed 32rem overhung
          // the 28rem masthead card on the map page and fell short of the
          // landing page's wider field.
          className="z-[950] w-(--radix-popover-trigger-width) border-rule-strong bg-paper p-0 shadow-missal-popover"
          onOpenAutoFocus={(event) => event.preventDefault()}
          onInteractOutside={(event) => {
            const target = event.target;
            if (
              target instanceof Node &&
              searchAnchorRef.current?.contains(target)
            ) {
              event.preventDefault();
            }
          }}
        >
          <div className="border-b border-rule-strong px-4 pt-3 pb-2">
            <span className="smallcaps text-[0.8125rem] text-ink-soft">
              {heading}
            </span>
          </div>
          <CommandList className="max-h-80 px-2 py-2">
            {showCurrentLocationOption ? (
              <CommandGroup className="[&_[cmdk-group-heading]]:hidden">
                <CommandItem
                  value={USE_MY_LOCATION}
                  onSelect={handleCurrentLocationSelect}
                  disabled={locationStatus === "requesting"}
                  className="group relative cursor-pointer gap-0 rounded-none border-l-2 border-transparent px-3 py-2.5 font-serif text-base text-ink data-[disabled=true]:pointer-events-none data-[selected=true]:border-rubric data-[selected=true]:bg-paper-deep/60 data-[selected=true]:text-ink"
                >
                  <div className="min-w-0">
                    <div className="truncate">
                      {locationStatus === "requesting"
                        ? FINDING_YOUR_LOCATION
                        : USE_MY_LOCATION}
                    </div>
                    <div
                      className={`mt-0.5 text-sm text-ink-soft ${locationError ? "" : "truncate"}`}
                    >
                      {locationError ?? "Show churches around you"}
                    </div>
                  </div>
                </CommandItem>
              </CommandGroup>
            ) : null}
            {showSearchStatus ? (
              isLoading ? (
                <div className="px-3 py-4 font-serif text-sm text-ink-soft">
                  {isPlaceMode ? "Searching places…" : "Loading churches…"}
                </div>
              ) : placeSearchNotConfigured ? (
                // A setup problem: name it for a developer; a visitor can
                // only be told it won't work, since trying again won't help.
                <CommandEmpty className="px-3 py-4 text-center font-serif text-sm text-ink-soft">
                  {import.meta.env.DEV
                    ? "Place search needs a Geoapify API key."
                    : "Place search isn’t available right now."}
                </CommandEmpty>
              ) : isPlaceMode && placeError ? (
                <CommandEmpty className="px-3 py-4 text-center font-serif text-sm text-ink-soft">
                  Couldn’t search places just now. Try again in a moment.
                </CommandEmpty>
              ) : hasResults ? (
                <CommandGroup className="[&_[cmdk-group-heading]]:hidden">
                  {isPlaceMode
                    ? placeResults.map((place) => (
                        <CommandItem
                          key={place.id}
                          value={`${place.title} ${place.subtitle ?? ""}`}
                          onSelect={() => handlePlaceSelect(place)}
                          className="group relative cursor-pointer gap-0 rounded-none border-l-2 border-transparent px-3 py-2.5 font-serif text-base text-ink data-[selected=true]:border-rubric data-[selected=true]:bg-paper-deep/60 data-[selected=true]:text-ink"
                        >
                          <div className="min-w-0">
                            <div className="truncate">{place.title}</div>
                            {place.subtitle ? (
                              <div className="mt-0.5 truncate text-sm text-ink-soft">
                                {place.subtitle}
                              </div>
                            ) : null}
                          </div>
                        </CommandItem>
                      ))
                    : parishResults.map((church) => {
                        const locationText = getChurchLocationText(church);
                        return (
                          <CommandItem
                            key={church.id}
                            value={`${church.name ?? `church-${church.id}`} ${locationText}`}
                            onSelect={() => handleChurchSelect(church)}
                            className="group relative cursor-pointer gap-0 rounded-none border-l-2 border-transparent px-3 py-2.5 font-serif text-base text-ink data-[selected=true]:border-rubric data-[selected=true]:bg-paper-deep/60 data-[selected=true]:text-ink"
                          >
                            <div className="min-w-0">
                              <div className="truncate">
                                {church.name ?? UNNAMED_CHURCH}
                              </div>
                              {locationText ? (
                                <div className="mt-0.5 truncate text-sm text-ink-soft">
                                  {locationText}
                                </div>
                              ) : null}
                            </div>
                          </CommandItem>
                        );
                      })}
                </CommandGroup>
              ) : emptyMessage ? (
                <CommandEmpty className="px-3 py-4 text-center font-serif text-sm text-ink-soft">
                  {emptyMessage}
                </CommandEmpty>
              ) : null
            ) : null}
          </CommandList>
          {isPlaceMode ? (
            <div className="border-t border-rule-strong px-4 py-2 text-right font-serif text-xs text-ink-soft">
              Powered by Geoapify
            </div>
          ) : null}
        </PopoverContent>
      </Popover>
    </Command>
  );
}

/**
 * cmdk's input always says it is expanded and points at its list and selected
 * item, but here the list only exists while the dropdown is open. cmdk sets
 * those attributes after the props it is given, so they can't be overridden
 * as props; this corrects them on the element after every render instead.
 * Rendered inside <Command> so it re-renders whenever the selection changes.
 * e2e/home.spec.ts checks the result, so a cmdk change that breaks it fails
 * a test.
 */
function ComboboxAriaSync({
  inputRef,
  open,
}: {
  inputRef: RefObject<HTMLInputElement | null>;
  open: boolean;
}) {
  const selectedItemId = useCommandState((state) => state.selectedItemId);
  // cmdk's list id, read from the input before it is first taken away.
  const listIdRef = useRef<string | null>(null);
  useLayoutEffect(() => {
    const input = inputRef.current;
    if (!input) return;
    listIdRef.current ??= input.getAttribute("aria-controls");
    const listId = listIdRef.current;
    input.setAttribute("aria-expanded", String(open));
    setOrRemove(input, "aria-controls", open ? listId : null);
    setOrRemove(
      input,
      "aria-activedescendant",
      open ? (selectedItemId ?? null) : null,
    );
  });
  return null;
}

function setOrRemove(el: Element, name: string, value: string | null) {
  if (value == null) el.removeAttribute(name);
  else el.setAttribute(name, value);
}
