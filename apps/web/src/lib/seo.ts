/**
 * Shared SEO/sharing metadata helpers: site constants, absolute-URL helpers,
 * and JSON-LD (schema.org) builders used by the prerendered church pages and
 * (in a later phase) the client-rendered routes.
 */
import type { ChurchDetail } from "../types";

export const SITE_NAME = "Project Carlo";
export const SITE_LOCALE = "en_US";
export const SITE_ORIGIN = "https://projectcarlo.com";

export const OG_IMAGE_PATH = "/og-default.png";
export const OG_IMAGE_WIDTH = 1200;
export const OG_IMAGE_HEIGHT = 630;
export const OG_IMAGE_ALT =
  "Project Carlo — Mass, Confession & Adoration times near you";

/** Default homepage title/description — keep keyword-forward, location-agnostic. */
export const HOME_TITLE =
  "Mass, Confession & Adoration Times Near You · Project Carlo";
export const HOME_DESCRIPTION =
  "Find Mass, Confession, and Adoration times at Catholic parishes on an interactive map. Schedules are parsed from each parish's weekly bulletin.";

/** The map app at `/map`. */
export const MAP_TITLE =
  "Map of Mass, Confession & Adoration Times · Project Carlo";
export const MAP_DESCRIPTION =
  "An interactive map of Catholic parishes with Mass, Confession, and Adoration times parsed from each parish's weekly bulletin. Filter by day and time.";

/** Resolve a site-relative path against an origin into an absolute URL. */
export function absoluteUrl(origin: string, path: string): string {
  return new URL(path, `${origin}/`).href;
}

/**
 * Serialize JSON-LD for embedding in a `<script>` tag. `JSON.stringify` does
 * not escape `<`, so a value containing `</script>` would otherwise terminate
 * the tag and break (or inject into) the surrounding HTML.
 */
export function serializeJsonLd(value: unknown): string {
  return JSON.stringify(value).replace(/</g, "\\u003c");
}

/** Absolute canonical URL for a site-relative path on the production origin. */
export function canonicalForPath(path: string): string {
  return absoluteUrl(SITE_ORIGIN, path);
}

/** "City, ST" for a church, or "" when neither is known. */
export function churchLocation(church: ChurchDetail): string {
  return [church.city, church.state]
    .filter((part): part is string => Boolean(part && part.trim()))
    .join(", ");
}

/**
 * Keyword-forward church page title: leads with the parish name (branded
 * searches) followed by the services and location people actually search for.
 */
export function buildChurchTitle(church: ChurchDetail): string {
  const name = church.name?.trim() || "Catholic Parish";
  const loc = churchLocation(church);
  const base = `${name} — Mass, Confession & Adoration Times`;
  return loc ? `${base} in ${loc}` : base;
}

/** SERP-snippet description for a church page (kept under ~155 chars). */
export function buildChurchDescription(church: ChurchDetail): string {
  const name = church.name?.trim() || "this parish";
  const loc = churchLocation(church);
  const where = loc ? ` in ${loc}` : "";
  return `Mass, Confession, and Adoration times for ${name}${where}, parsed from the parish's latest weekly bulletin.`;
}

/** Canonical path of the prerendered all-parishes index page. */
export const CHURCH_INDEX_PATH = "/churches/";

export const CHURCH_INDEX_TITLE = `Browse Catholic Parishes — Mass, Confession & Adoration Times · ${SITE_NAME}`;

export function buildChurchIndexDescription(parishCount: number): string {
  return `Browse all ${parishCount} Catholic parishes on ${SITE_NAME} and find Mass, Confession, and Adoration times parsed from each parish's weekly bulletin.`;
}

/** schema.org PostalAddress for a church, or null when no address is known. */
function postalAddress(church: ChurchDetail): Record<string, unknown> | null {
  const street = [church.address_line1, church.address_line2]
    .filter((part): part is string => Boolean(part && part.trim()))
    .join(", ");
  const parts: Record<string, unknown> = { "@type": "PostalAddress" };
  if (street) parts.streetAddress = street;
  if (church.city) parts.addressLocality = church.city;
  if (church.state) parts.addressRegion = church.state;
  if (church.postal_code) parts.postalCode = church.postal_code;
  parts.addressCountry = "US";
  // Require at least one locality-level field to be meaningful.
  if (!street && !church.city && !church.state && !church.postal_code) {
    return null;
  }
  return parts;
}

/**
 * `Church` (PlaceOfWorship) structured data for a parish detail page.
 *
 * Recurring service times intentionally remain visible page content instead
 * of `Event` nodes. Google requires each structured Event to describe one
 * concrete event on a unique leaf page, while parish pages list many recurring
 * services: https://developers.google.com/search/docs/appearance/structured-data/event
 */
export function churchJsonLd(
  church: ChurchDetail,
  canonicalUrl: string,
): Record<string, unknown> {
  const origin = new URL(canonicalUrl).origin;
  const churchId = `${canonicalUrl}#church`;
  const node: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "Church",
    "@id": churchId,
    name: church.name ?? "Catholic parish",
    url: canonicalUrl,
    image: absoluteUrl(origin, OG_IMAGE_PATH),
  };

  const address = postalAddress(church);
  if (address) node.address = address;

  if (church.latitude != null && church.longitude != null) {
    node.geo = {
      "@type": "GeoCoordinates",
      latitude: church.latitude,
      longitude: church.longitude,
    };
  }

  const sameAs = [church.homepage_url].filter(
    (u): u is string => Boolean(u && u.trim()),
  );
  if (sameAs.length > 0) node.sameAs = sameAs;

  return node;
}

/**
 * `WebPage` node carrying `dateModified` (derived from the parish's latest
 * bulletin, same source as the sitemap `<lastmod>`) — freshness signal for a
 * schedules site.
 */
export function churchWebPageJsonLd(
  church: ChurchDetail,
  canonicalUrl: string,
  dateModified: string | null,
): Record<string, unknown> {
  const node: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": `${canonicalUrl}#webpage`,
    url: canonicalUrl,
    name: buildChurchTitle(church),
    description: buildChurchDescription(church),
    about: { "@id": `${canonicalUrl}#church` },
    inLanguage: "en-US",
  };
  if (dateModified) node.dateModified = dateModified;
  return node;
}

/** A level of a breadcrumb trail; `path` is site-relative. */
export interface BreadcrumbItem {
  name: string;
  path: string;
}

/**
 * BreadcrumbList for a trail like Home → New York → Buffalo → {Parish}.
 * schema.org requires every crumb to carry an `item` URL, so a level that has
 * no page of its own (a one-church town) is simply left out of the trail.
 */
export function breadcrumbJsonLd(
  origin: string,
  crumbs: BreadcrumbItem[],
): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: crumbs.map((crumb, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: crumb.name,
      item: absoluteUrl(origin, crumb.path),
    })),
  };
}

/** Breadcrumbs for a church page; see `churchCrumbs` in lib/browse.ts. */
export function churchBreadcrumbJsonLd(
  church: ChurchDetail,
  canonicalUrl: string,
  crumbs?: BreadcrumbItem[],
): Record<string, unknown> {
  const origin = new URL(canonicalUrl).origin;
  return breadcrumbJsonLd(
    origin,
    crumbs ?? [
      { name: "Home", path: "/" },
      { name: church.name ?? "Parish", path: new URL(canonicalUrl).pathname },
    ],
  );
}

/** `ItemList` of links to the pages a browse page lists, in display order. */
export function itemListJsonLd(
  origin: string,
  items: { name: string; path: string }[],
): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    numberOfItems: items.length,
    itemListElement: items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      url: absoluteUrl(origin, item.path),
      name: item.name,
    })),
  };
}

/**
 * JSON-LD for a browse page (diocese index, diocese, state hub, city): a
 * `CollectionPage` with `dateModified`, its `BreadcrumbList` and an `ItemList`
 * of the pages it links to. Recurring schedules stay visible content rather
 * than `Event` nodes (see `churchJsonLd`).
 */
export function browsePageJsonLd(opts: {
  origin: string;
  path: string;
  title: string;
  description: string;
  dateModified: string;
  crumbs: BreadcrumbItem[];
  items: { name: string; path: string }[];
}): Record<string, unknown>[] {
  const url = absoluteUrl(opts.origin, opts.path);
  return [
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "@id": `${url}#webpage`,
      url,
      name: opts.title,
      description: opts.description,
      dateModified: opts.dateModified,
      inLanguage: "en-US",
      isPartOf: { "@id": `${opts.origin}/#website` },
      mainEntity: { "@id": `${url}#list` },
    },
    { ...itemListJsonLd(opts.origin, opts.items), "@id": `${url}#list` },
    breadcrumbJsonLd(opts.origin, opts.crumbs),
  ];
}

/** Site-level WebSite + Organization graph for the homepage. */
export function websiteJsonLd(origin: string): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebSite",
        "@id": `${origin}/#website`,
        name: SITE_NAME,
        url: absoluteUrl(origin, "/"),
        description: HOME_DESCRIPTION,
        inLanguage: "en-US",
        publisher: { "@id": `${origin}/#organization` },
      },
      {
        "@type": "Organization",
        "@id": `${origin}/#organization`,
        name: SITE_NAME,
        url: absoluteUrl(origin, "/"),
        logo: absoluteUrl(origin, "/icon-512.png"),
      },
    ],
  };
}
