import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
  type RefObject,
} from "react";
import { Command as CommandPrimitive, useCommandState } from "cmdk";
import { useQuery } from "@tanstack/react-query";
import type { ChurchSearchResult } from "../api";
import {
  approximateLocationQuery,
  churchSearchIndexQuery,
} from "../lib/homeStartQueries";
import { formatAddress } from "@carlo/core";
import type { LatLng } from "../lib/cities";
import { wantsCurrentLocation } from "../lib/currentLocationQuery";
import {
  buildLocalSearchIndex,
  chooseSearchCenter,
  rankPlaces,
  searchChurches,
} from "../lib/localSearch";
import { useBrowserLocation } from "../hooks/useBrowserLocation";
import { track } from "../lib/analytics";
import {
  canSearchPlaces,
  currentLocationPlace,
  PlaceSearchConfigurationError,
  roundToBiasPrecision,
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

/** Most people type slower than this between letters, so a shorter pause
 *  would search on nearly every one of them. */
const DEBOUNCE_MS = 300;
const PLACE_RESULT_CACHE_MS = 10 * 60 * 1000;

const RESULT_ITEM_CLASS =
  "group relative cursor-pointer gap-0 rounded-none border-l-2 border-transparent px-3 py-2.5 font-serif text-base text-ink data-[selected=true]:border-rubric data-[selected=true]:bg-paper-deep/60 data-[selected=true]:text-ink";
const RESULT_GROUP_CLASS =
  "**:[[cmdk-group-heading]]:px-2 **:[[cmdk-group-heading]]:pt-0 **:[[cmdk-group-heading]]:pb-1 **:[[cmdk-group-heading]]:text-[0.8125rem] **:[[cmdk-group-heading]]:font-normal **:[[cmdk-group-heading]]:text-ink-soft";
const STATUS_CLASS =
  "px-3 py-4 text-center font-serif text-sm text-ink-soft";

interface SearchTypeaheadProps {
  onChurchSelect: (church: ChurchSearchResult) => void;
  onPlaceSelect: (place: PlaceSearchResult) => void;
  filterButton: ReactNode;
  /** Input/icon sizing variant. `md` (default) matches the map header; `lg` renders the hero size used on the landing page. */
  size?: "md" | "lg";
  /** The search's placeholder, where the default won't fit. */
  placeholder?: string;
  /**
   * What the visitor is looking at, to rank results around: the middle of the
   * map, when there's one. Without it, or if it's somewhere Carlo doesn't
   * cover, results rank around their IP location.
   */
  getSearchCenter?: () => LatLng | null;
}

export function SearchTypeahead({
  onChurchSelect,
  onPlaceSelect,
  filterButton,
  size = "md",
  placeholder = "Search for a city, ZIP, address, or church…",
  getSearchCenter,
}: SearchTypeaheadProps) {
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const searchAnchorRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const t = setTimeout(() => setDebouncedQuery(query), DEBOUNCE_MS);
    return () => clearTimeout(t);
  }, [query]);

  const { data: allChurches = [], isLoading: churchesLoading } = useQuery(
    churchSearchIndexQuery,
  );
  const localIndex = useMemo(
    () => buildLocalSearchIndex(allChurches),
    [allChurches],
  );
  // Asked for once the box is opened: most page views never search.
  const { data: approximateLocation } = useQuery({
    ...approximateLocationQuery,
    enabled: isOpen,
  });
  const searchCenter = chooseSearchCenter(
    [getSearchCenter?.(), approximateLocation],
    allChurches,
  );
  // Rounded, so a small move of the map neither reranks nor searches again.
  const biasLat = searchCenter ? roundToBiasPrecision(searchCenter).lat : null;
  const biasLng = searchCenter ? roundToBiasPrecision(searchCenter).lng : null;
  const near = useMemo(
    () =>
      biasLat !== null && biasLng !== null
        ? { lat: biasLat, lng: biasLng }
        : null,
    [biasLat, biasLng],
  );

  const trimmedQuery = query.trim();
  const trimmedDebouncedQuery = debouncedQuery.trim();
  const shouldSearchPlaces = canSearchPlaces(trimmedDebouncedQuery);
  const {
    data: providerPlaces = [],
    isLoading: placesLoading,
    isPlaceholderData: placesPending,
    error: placeError,
  } = useQuery({
    queryKey: ["place-search", trimmedDebouncedQuery, biasLat, biasLng],
    queryFn: ({ signal }) =>
      searchPlaces(trimmedDebouncedQuery, { near, signal }),
    enabled: shouldSearchPlaces,
    staleTime: PLACE_RESULT_CACHE_MS,
    gcTime: PLACE_RESULT_CACHE_MS,
    retry: false,
    // Typing on keeps the list up while its next results load, rather than
    // blanking it; a different search doesn't show the last one's.
    placeholderData: (previous, previousQuery) => {
      const previousText = previousQuery?.queryKey[1];
      return typeof previousText === "string" &&
        trimmedDebouncedQuery.startsWith(previousText)
        ? previous
        : undefined;
    },
  });

  // What the debounce last let through still belongs in the list if the box
  // only added to it or took from it, but not if it now holds something else.
  const showsDebouncedSearch =
    trimmedQuery !== "" &&
    (trimmedQuery.startsWith(trimmedDebouncedQuery) ||
      trimmedDebouncedQuery.startsWith(trimmedQuery));

  // Cities answer on every keystroke. The rest waits for the pause in typing.
  const placeResults = useMemo(
    () =>
      canSearchPlaces(trimmedQuery)
        ? rankPlaces(
            trimmedQuery,
            localIndex,
            shouldSearchPlaces && showsDebouncedSearch ? providerPlaces : [],
            near,
          )
        : [],
    [
      trimmedQuery,
      localIndex,
      shouldSearchPlaces,
      showsDebouncedSearch,
      providerPlaces,
      near,
    ],
  );
  const churchResults = useMemo(
    () =>
      showsDebouncedSearch
        ? searchChurches(trimmedDebouncedQuery, localIndex, near)
        : [],
    [showsDebouncedSearch, trimmedDebouncedQuery, localIndex, near],
  );

  const hasTypedQuery = trimmedQuery.length > 0;
  // Offered on an empty field, and after that only when the query is asking
  // for it, so it doesn't top every list of place results.
  const showCurrentLocationOption = wantsCurrentLocation(query);
  // Opens immediately so the current-location suggestion is the default.
  const showDropdown =
    isOpen && (showCurrentLocationOption || trimmedQuery.length >= 2);
  const hasResults = placeResults.length > 0 || churchResults.length > 0;
  // "No results" only once a search has run on what's in the box: not while
  // the debounce lags the typing, and not for a query too short to search,
  // which would otherwise read as a search that found nothing.
  const searchSettled = debouncedQuery === query;
  // Results kept up from the last search aren't an answer to this one, so
  // while they're showing an empty list only means it hasn't come back yet.
  // Nor has one that waits on the debounce, which would otherwise leave the
  // dropdown blank, as it was after correcting "biston ma" to "boston ma".
  const isLoading =
    placesLoading ||
    placesPending ||
    churchesLoading ||
    (!searchSettled && canSearchPlaces(trimmedQuery));
  // Echo what was searched, so a typo is easy to spot, and say what to try.
  const emptyMessage = !searchSettled
    ? null
    : !shouldSearchPlaces
      ? "Keep typing a town, ZIP code, address, or church."
      : `Nothing matches “${trimmedDebouncedQuery}”. Try a town name or ZIP code.`;
  const placeSearchNotConfigured =
    placeError instanceof PlaceSearchConfigurationError;
  // A church named outright comes first. A city Carlo serves still leads,
  // since its name may only be part of a church's.
  const churchesFirst =
    churchResults.length > 0 &&
    !placeResults.some((place) => place.isServedCity);

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
      track("search_select", { kind: place.isServedCity ? "city" : "place" });
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

  const inputRef = useRef<HTMLInputElement | null>(null);

  const placeGroup =
    placeResults.length > 0 ? (
      <CommandGroup
        heading={<span className="smallcaps">Places</span>}
        className={RESULT_GROUP_CLASS}
      >
        {placeResults.map((place) => (
          <CommandItem
            key={place.id}
            value={`${place.title} ${place.subtitle ?? ""}`}
            onSelect={() => handlePlaceSelect(place)}
            className={RESULT_ITEM_CLASS}
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
        ))}
      </CommandGroup>
    ) : null;

  const churchGroup =
    churchResults.length > 0 ? (
      <CommandGroup
        heading={<span className="smallcaps">Churches</span>}
        className={RESULT_GROUP_CLASS}
      >
        {churchResults.map((church) => {
          const locationText = getChurchLocationText(church);
          return (
            <CommandItem
              key={church.id}
              value={`${church.name ?? `church-${church.id}`} ${locationText}`}
              onSelect={() => handleChurchSelect(church)}
              className={RESULT_ITEM_CLASS}
            >
              <div className="min-w-0">
                <div className="truncate">{church.name ?? UNNAMED_CHURCH}</div>
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
    ) : null;

  return (
    <Command
      shouldFilter={false}
      // cmdk names its input by a hidden label of its own (aria-labelledby),
      // which outranks aria-label, so the name has to go here.
      label="Search for a city, ZIP code, address, or church"
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
              <div className="shrink-0">{filterButton}</div>
            </div>
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
          <CommandList className="max-h-80 px-2 py-2">
            {showCurrentLocationOption ? (
              <CommandGroup className="[&_[cmdk-group-heading]]:hidden">
                <CommandItem
                  value={USE_MY_LOCATION}
                  onSelect={handleCurrentLocationSelect}
                  disabled={locationStatus === "requesting"}
                  className={`${RESULT_ITEM_CLASS} data-[disabled=true]:pointer-events-none`}
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
            {churchesFirst ? churchGroup : placeGroup}
            {churchesFirst ? placeGroup : churchGroup}
            {!hasTypedQuery || hasResults ? null : isLoading ? (
              <div className="px-3 py-4 font-serif text-sm text-ink-soft">
                Searching places…
              </div>
            ) : placeSearchNotConfigured ? (
              // A setup problem: name it for a developer; a visitor can
              // only be told it won't work, since trying again won't help.
              <CommandEmpty className={STATUS_CLASS}>
                {import.meta.env.DEV
                  ? "Place search needs a Geoapify API key."
                  : "Place search isn’t available right now."}
              </CommandEmpty>
            ) : placeError ? (
              <CommandEmpty className={STATUS_CLASS}>
                Couldn’t search places just now. Try again in a moment.
              </CommandEmpty>
            ) : emptyMessage ? (
              <CommandEmpty className={STATUS_CLASS}>
                {emptyMessage}
              </CommandEmpty>
            ) : null}
          </CommandList>
          <div className="border-t border-rule-strong px-4 py-2 text-right font-serif text-xs text-ink-soft">
            Powered by Geoapify
          </div>
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
