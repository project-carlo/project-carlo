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

/** The parameters a visit is credited to a campaign by (src/lib/analytics.ts). */
const CAMPAIGN_PARAMS = ["utm_source", "ref"] as const;

/**
 * Where a link in the embed opens, in a new tab: its own URL, plus the
 * embed's campaign when it's a page of this site and carries none of its own.
 * The new tab's first pageview reads the campaign from its URL, and its
 * referrer is the embed (this site), which analytics doesn't count, so
 * without it the visit would look direct.
 */
export function embedLinkHref(href: string, embedHref: string): string {
  const embed = new URL(embedHref);
  const url = new URL(href, embed);
  if (url.origin !== embed.origin || CAMPAIGN_PARAMS.some((p) => url.searchParams.has(p))) {
    return url.href;
  }
  for (const param of CAMPAIGN_PARAMS) {
    const value = embed.searchParams.get(param);
    if (value) url.searchParams.set(param, value);
  }
  return url.href;
}
