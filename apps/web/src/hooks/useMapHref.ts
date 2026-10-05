import { useState } from "react";

/**
 * The map page (`/map`) keeps its full state (filters + camera) in the URL
 * query string. In-app "Back to map" links are plain pushes to "/map", though,
 * so without help they'd drop that state. We stash the last map query string
 * in sessionStorage whenever it changes and replay it here, so returning to the
 * map restores the exact filters and view the user left — regardless of how
 * they navigated away.
 */
const MAP_SEARCH_KEY = "carlo:map-search";

export function rememberMapSearch(search: string): void {
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.setItem(MAP_SEARCH_KEY, search);
  } catch {
    // Private-mode / storage-disabled: degrade to a plain "/map" link.
  }
}

function readMapSearch(): string {
  if (typeof window === "undefined") return "";
  try {
    return window.sessionStorage.getItem(MAP_SEARCH_KEY) ?? "";
  } catch {
    return "";
  }
}

/**
 * Returns the href for "Back to map" links: "/map" plus the remembered query
 * string. Read once on mount — these links live on pages that don't outlive a
 * single visit, so there's no need to react to later storage writes.
 */
export function useMapHref(): string {
  const [search] = useState(readMapSearch);
  return search ? `/map${search}` : "/map";
}
