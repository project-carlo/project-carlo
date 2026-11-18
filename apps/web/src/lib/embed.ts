/**
 * The embed: the home map at /embed, for dioceses to frame on their own sites
 * (docs/embed.md). It drops the site's masthead and links for a "Powered by"
 * line, opens church pages in a new tab rather than inside the frame, and
 * with `diocese=<slug>` shows only that diocese's churches, framed to fit
 * them. The URL is a public contract: dioceses paste it into their pages, so
 * its parameters keep working once shipped.
 */

export const EMBED_PATH = "/embed";

/** The query parameter naming the diocese, by its folder in data/dioceses/. */
export const DIOCESE_PARAM = "diocese";

/**
 * The diocese an embed URL asks for: its `diocese=` value, trimmed and
 * lowercased, or null when there is none. A value that names no diocese the
 * site covers is still returned: the embed says it isn't supported, rather
 * than quietly show every church under a diocese's name.
 */
export function embedDiocese(search: string): string | null {
  const value = new URLSearchParams(search).get(DIOCESE_PARAM)?.trim().toLowerCase();
  return value ? value : null;
}

/**
 * The full site's map for an embed's query string: the same view, filters
 * and campaign (`ref` / `utm_source`), so a visit that follows the link is
 * still credited to the embed, without the embed's diocese.
 */
export function fullSiteMapHref(search: string): string {
  const params = new URLSearchParams(search);
  params.delete(DIOCESE_PARAM);
  const query = params.toString();
  return query ? `/?${query}` : "/";
}
