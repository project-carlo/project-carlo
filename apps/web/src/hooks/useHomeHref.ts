import { useState } from "react";

/**
 * The map page keeps its full state (filters + camera) in the URL query string.
 * In-app links to the map are plain pushes to "/", though, so without help
 * they'd drop that state. We stash the last map query string in sessionStorage
 * whenever it changes and replay it here, so returning to the map restores the
 * exact filters and view the user left — regardless of how they navigated away.
 */
export const HOME_SEARCH_KEY = "carlo:home-search";

/**
 * Marks a link to the map that should carry the remembered query string. The
 * prerendered pages render it as a bare "/", and a script of theirs fills in
 * the rest (see scripts/prerender.ts).
 */
export const HOME_LINK_ATTRIBUTE = "data-home-link";

export function rememberHomeSearch(search: string): void {
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.setItem(HOME_SEARCH_KEY, search);
  } catch {
    // Private-mode / storage-disabled: degrade to a plain "/" link.
  }
}

function readHomeSearch(): string {
  if (typeof window === "undefined") return "";
  try {
    return window.sessionStorage.getItem(HOME_SEARCH_KEY) ?? "";
  } catch {
    return "";
  }
}

/**
 * Returns the href for in-app links to the map: "/" plus the remembered query
 * string. Read once on mount — these links live on pages that don't outlive a
 * single visit, so there's no need to react to later storage writes.
 */
export function useHomeHref(): string {
  const [search] = useState(readHomeSearch);
  return search ? `/${search}` : "/";
}
