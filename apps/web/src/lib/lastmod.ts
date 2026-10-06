/**
 * Sitemap `<lastmod>` dates that change only when a page's content does.
 *
 * Google trusts `<lastmod>` only while it stays accurate, so stamping every
 * page with the build date teaches it to ignore the field. Instead each build
 * hashes every prerendered page and publishes the hashes with their dates in
 * `lastmod.json`; the next build fetches that file from the live site and keeps
 * a page's previous date when its hash hasn't changed.
 */

export const LASTMOD_FILE = "lastmod.json";

/** Rendered in place of a page's own modification date (its JSON-LD
 *  `dateModified`) until the date is known, so the date never feeds the hash
 *  it is derived from. */
export const LASTMOD_PLACEHOLDER = "__LASTMOD__";

export interface LastmodEntry {
  hash: string;
  /** YYYY-MM-DD */
  lastmod: string;
}

/** Keyed by site path, e.g. `/churches/all-saints-albany/`. */
export interface LastmodManifest {
  version: 1;
  pages: Record<string, LastmodEntry>;
}

const DATE = /^\d{4}-\d{2}-\d{2}$/;

/** The previous build's manifest, or null when it is missing or malformed —
 *  which only costs the dates, never the build. */
export function parseLastmodManifest(text: string): LastmodManifest | null {
  let data: unknown;
  try {
    data = JSON.parse(text);
  } catch {
    return null;
  }
  if (typeof data !== "object" || data === null) return null;
  const { version, pages } = data as Partial<LastmodManifest>;
  if (version !== 1 || typeof pages !== "object" || pages === null) return null;
  const valid: Record<string, LastmodEntry> = {};
  for (const [path, entry] of Object.entries(pages)) {
    if (
      typeof entry?.hash === "string" &&
      typeof entry.lastmod === "string" &&
      DATE.test(entry.lastmod)
    ) {
      valid[path] = { hash: entry.hash, lastmod: entry.lastmod };
    }
  }
  return { version: 1, pages: valid };
}

/** A page's HTML with what changes on every build removed: the hashed asset
 *  filenames (a style change isn't a content change) and the date placeholder. */
export function contentForHash(html: string, assetPaths: readonly string[]): string {
  let content = html.split(LASTMOD_PLACEHOLDER).join("");
  for (const path of assetPaths) content = content.split(path).join("");
  return content;
}

/** The previous date while the content is unchanged, otherwise the build date. */
export function resolveLastmod(
  previous: LastmodEntry | undefined,
  hash: string,
  buildDate: string,
): string {
  return previous?.hash === hash ? previous.lastmod : buildDate;
}

/** The latest of some YYYY-MM-DD dates (they sort as strings). */
export function latestDate(dates: Iterable<string>, fallback: string): string {
  let latest: string | null = null;
  for (const date of dates) if (latest === null || date > latest) latest = date;
  return latest ?? fallback;
}
