import type { MapView } from "./mapView";

/**
 * The city page's map: a still preview the page is rendered with, made live
 * by CityMapLive, which also opens it over the whole window. Open is a URL
 * hash, so the browser's back button (or swipe) closes it, a link can open
 * it, and coming back from a church page finds it as it was left.
 */

/** What the live map needs from the page, read off the preview. */
export interface CityMapConfig {
  /** "East Aurora, NY". */
  label: string;
  /** The preview's view, which the live map opens on. */
  view: MapView;
}

/** Marks the preview; its value is the JSON of a CityMapConfig. */
export const CITY_MAP_ATTRIBUTE = "data-city-map";
/** Marks the element the live map is mounted into, inside the preview. */
export const CITY_MAP_SLOT_ATTRIBUTE = "data-city-map-slot";

/** The hash of a city page with its map open. */
const CITY_MAP_HASH = "#map";

export function isCityMapOpen(): boolean {
  return window.location.hash === CITY_MAP_HASH;
}

/**
 * Tells whoever follows the URL (useCityMapOpen, and the app's router) that
 * it changed: pushState and replaceState don't, as the back button does.
 */
function announceUrlChange(): void {
  window.dispatchEvent(new PopStateEvent("popstate", { state: window.history.state }));
}

/**
 * Opens the map, adding a history entry for the back button to close it.
 * The entry keeps the current one's state, which the app's router keeps its
 * place in history in; setting `location.hash` would leave it empty.
 */
export function openCityMap(): void {
  const { pathname, search } = window.location;
  window.history.pushState(window.history.state, "", pathname + search + CITY_MAP_HASH);
  announceUrlChange();
}

/** Closes the map in place, for an open map this page added no entry for. */
export function closeCityMapInPlace(): void {
  const { pathname, search } = window.location;
  window.history.replaceState(window.history.state, "", pathname + search);
  announceUrlChange();
}

/** Parses a preview's config, or null if it isn't one. */
export function parseCityMapConfig(json: string | undefined): CityMapConfig | null {
  if (!json) return null;
  try {
    const value = JSON.parse(json) as Partial<CityMapConfig>;
    const view = value.view;
    if (
      typeof value.label !== "string" ||
      !view ||
      !Number.isFinite(view.lat) ||
      !Number.isFinite(view.lng) ||
      !Number.isFinite(view.zoom)
    ) {
      return null;
    }
    return { label: value.label, view };
  } catch {
    return null;
  }
}

/**
 * Where the map in the page keeps its zoom buttons, above the attribution;
 * the still preview's inert copy sits on the same pixels.
 */
export const CITY_MAP_ZOOM_CORNER_CLASS = "right-3 bottom-7";

/** The city map's buttons over the map (Expand, Close, Filters): small cards. */
export const CITY_MAP_CHIP_CLASS =
  "missal-focus inline-flex items-center gap-2 border border-rule-strong bg-paper/95 px-3 py-1.5 font-serif text-[0.9375rem] text-rubric shadow-missal-floating backdrop-blur-sm transition-colors hover:text-rubric-deep";
