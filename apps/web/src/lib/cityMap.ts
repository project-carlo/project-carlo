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
/** Marks the preview's link, which a phone's first tap turns into "open". */
export const CITY_MAP_OPEN_ATTRIBUTE = "data-city-map-open";

/** The hash of a city page with its map open. */
export const CITY_MAP_HASH = "#map";

/**
 * Where the map is live in the page itself. Narrower screens keep the still
 * preview, which opens the live map over the whole window when tapped: a live
 * map in a phone's page catches the swipes meant to scroll it.
 */
export const INLINE_MAP_MIN_WIDTH = 768;

export function isCityMapOpen(): boolean {
  return window.location.hash === CITY_MAP_HASH;
}

/** Opens the map, adding a history entry for the back button to close it. */
export function openCityMap(): void {
  window.location.hash = CITY_MAP_HASH;
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
