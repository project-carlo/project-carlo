/**
 * The script that makes a prerendered city page's map live (see
 * src/lib/cityMap.ts): a build entry of its own beside index.html
 * (vite.config.ts), which scripts/prerender.ts finds in Vite's manifest.
 * Apart from cityMap.ts, which needs the DOM, so the build config can read it.
 */
export const CITY_MAP_ENTRY = "src/islands/cityMap.ts";
