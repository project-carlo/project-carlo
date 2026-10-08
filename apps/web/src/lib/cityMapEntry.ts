/**
 * The script that makes a prerendered city page's map live (see
 * src/lib/cityMap.ts): a build entry of its own beside index.html
 * (vite.config.ts), which scripts/prerender.ts finds in Vite's manifest.
 * Kept apart from cityMap.ts, which uses the DOM, so the build config can
 * import it.
 */
export const CITY_MAP_ENTRY = "src/islands/cityMap.ts";

/** The all-churches index's search script (src/islands/churchIndex.ts), the
 *  same way. */
export const CHURCH_INDEX_ENTRY = "src/islands/churchIndex.ts";
