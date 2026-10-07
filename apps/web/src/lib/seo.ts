/**
 * Shared SEO/sharing metadata helpers: site constants, absolute-URL helpers,
 * and JSON-LD (schema.org) builders used by the prerendered church pages and
 * (in a later phase) the client-rendered routes.
 */
import type { ChurchBase, ChurchDetail } from "../types";
import { cityPath, type City, type CityLink } from "./cities";
import { ALL_CHURCHES, SOURCE_PHRASE, UNNAMED_CHURCH } from "../copy";

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
export const HOME_DESCRIPTION = `Find Mass, Confession, and Adoration times at Catholic churches on an interactive map. Times come ${SOURCE_PHRASE}.`;

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
 * Church page title, e.g. "St. Mary, East Aurora — Mass & Confession Times".
 * The church's name and town lead, since search results cut titles off at
 * about 60 characters and those are what tell one St. Mary from another; the
 * services people search for follow, and the description names all three.
 */
export function buildChurchTitle(church: ChurchDetail): string {
  const name = church.name?.trim() || UNNAMED_CHURCH;
  const place = church.city?.trim() || church.state?.trim();
  return `${place ? `${name}, ${place}` : name} — Mass & Confession Times`;
}

/** SERP-snippet description for a church page (kept under ~155 chars). */
export function buildChurchDescription(church: ChurchDetail): string {
  const name = church.name?.trim() || "this church";
  const loc = churchLocation(church);
  const where = loc ? ` in ${loc}` : "";
  return `Mass, Confession, and Adoration times for ${name}${where}, from the parish’s weekly bulletin.`;
}

/** Canonical path of the prerendered all-churches index page. */
export const CHURCH_INDEX_PATH = "/churches/";

/** Canonical path of a church page. */
export function churchPath(slug: string): string {
  return `${CHURCH_INDEX_PATH}${encodeURIComponent(slug)}/`;
}

export const CHURCH_INDEX_TITLE = `Browse Catholic Churches — Mass, Confession & Adoration Times · ${SITE_NAME}`;

export function buildChurchIndexDescription(churchCount: number): string {
  return `Browse all ${churchCount} Catholic churches on ${SITE_NAME} and find Mass, Confession, and Adoration times ${SOURCE_PHRASE}.`;
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
 * `Church` (PlaceOfWorship) structured data for a church page.
 *
 * Recurring service times intentionally remain visible page content instead
 * of `Event` nodes. Google requires each structured Event to describe one
 * concrete event on a unique leaf page, while church pages list many recurring
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
    name: church.name ?? UNNAMED_CHURCH,
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

/**
 * BreadcrumbList: Home → All churches → {City} → {Church}, without the city level
 * when the church's address has none.
 */
export function churchBreadcrumbJsonLd(
  church: ChurchDetail,
  city: CityLink | null,
  canonicalUrl: string,
): Record<string, unknown> {
  const origin = new URL(canonicalUrl).origin;
  const crumbs: { name: string; item: string }[] = [
    { name: SITE_NAME, item: absoluteUrl(origin, "/") },
    { name: ALL_CHURCHES, item: absoluteUrl(origin, CHURCH_INDEX_PATH) },
  ];
  if (city) {
    crumbs.push({ name: city.label, item: absoluteUrl(origin, cityPath(city.slug)) });
  }
  crumbs.push({ name: church.name ?? UNNAMED_CHURCH, item: canonicalUrl });
  return breadcrumbList(crumbs);
}

function breadcrumbList(
  crumbs: { name: string; item: string }[],
): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: crumbs.map((crumb, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: crumb.name,
      item: crumb.item,
    })),
  };
}

/** City page title, e.g. "Catholic Mass Times in East Aurora, NY — Confession & Adoration · Project Carlo". */
export function buildCityTitle(city: Pick<City, "label">): string {
  return `Catholic Mass Times in ${city.label} — Confession & Adoration · ${SITE_NAME}`;
}

/** SERP-snippet description for a city page. */
export function buildCityDescription(
  city: Pick<City, "label" | "churches">,
): string {
  const count = city.churches.length;
  const churches =
    count === 1
      ? `${city.churches[0].name?.trim() || "the Catholic church"}`
      : `the ${count} Catholic churches`;
  return `Mass, Confession, and Adoration times at ${churches} in ${city.label} and nearby churches, ${SOURCE_PHRASE}.`;
}

/**
 * Structured data for a city page: the page as a CollectionPage of its
 * churches' pages, and its breadcrumbs (Home → All churches → {City}).
 */
export function cityJsonLd(
  city: Pick<City, "label" | "churches">,
  canonicalUrl: string,
): Record<string, unknown>[] {
  const origin = new URL(canonicalUrl).origin;
  const churchUrl = (church: ChurchBase) => absoluteUrl(origin, churchPath(church.slug));
  return [
    {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "@id": `${canonicalUrl}#webpage`,
      url: canonicalUrl,
      name: buildCityTitle(city),
      description: buildCityDescription(city),
      inLanguage: "en-US",
      mainEntity: {
        "@type": "ItemList",
        itemListElement: city.churches.map((church, i) => ({
          "@type": "ListItem",
          position: i + 1,
          name: church.name ?? UNNAMED_CHURCH,
          url: churchUrl(church),
        })),
      },
    },
    breadcrumbList([
      { name: SITE_NAME, item: absoluteUrl(origin, "/") },
      { name: ALL_CHURCHES, item: absoluteUrl(origin, CHURCH_INDEX_PATH) },
      { name: city.label, item: canonicalUrl },
    ]),
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
