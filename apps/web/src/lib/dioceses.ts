import type { ChurchBase } from "../types";
import { citySlugFor, type City } from "./cities";

/**
 * Diocese pages: one per diocese the site covers in full, linking the pages
 * of its cities. Pure; shared by the SPA (api.ts) and the prerenderer, so
 * both put churches and cities in the same dioceses.
 *
 * Which churches a diocese has comes from src/data/dioceses.json, written by
 * `pnpm diocese site-index` (and `promote`) from data/dioceses/ and
 * data/churches.csv, not from the data snapshot, which knows no dioceses. A
 * church the file lists and the snapshot doesn't have is left out; one the
 * snapshot has and the file doesn't list is put in its city's diocese (see
 * buildDioceseIndex).
 */

/** Path of the list of dioceses. */
export const DIOCESE_INDEX_PATH = "/dioceses/";

/** A diocese as src/data/dioceses.json records it, under its slug. */
export interface DioceseRecord {
  /** As the diocese names itself, e.g. "Roman Catholic Diocese of Buffalo". */
  name: string;
  state: string | null;
  /** The diocese's own website. */
  website: string | null;
  /**
   * Whether the site covers the whole diocese (`coverage: complete` in its
   * diocese.md): only then does it get pages and breadcrumbs of its own.
   */
  covered: boolean;
  /** Slugs of its churches. */
  churches: string[];
}

export type DioceseRecords = Record<string, DioceseRecord>;

/** One of a diocese's cities, and how many of the city's churches are in it. */
export interface DioceseCity {
  city: City;
  /** All of the city's churches, unless the city is split between dioceses. */
  churchCount: number;
}

export interface Diocese {
  /** URL slug: the diocese's folder under data/dioceses/, e.g. `buffalo`. */
  slug: string;
  name: string;
  /** "Diocese of Buffalo": the name without "Roman Catholic". */
  label: string;
  state: string | null;
  website: string | null;
  covered: boolean;
  /** Its churches on the site, in snapshot order (by name). */
  churches: ChurchBase[];
  /** Its cities, by label. */
  cities: DioceseCity[];
}

/** What a link to a diocese page needs. */
export type DioceseLink = Pick<Diocese, "slug" | "label">;

export interface DioceseIndex {
  /** Every diocese with a church on the site, by place (Albany, Buffalo, New York…). */
  dioceses: Diocese[];
  bySlug: Map<string, Diocese>;
  /** Each church's diocese, by church slug. */
  byChurch: Map<string, Diocese>;
  /** Each city's diocese, by city slug; a city split between dioceses has none. */
  byCity: Map<string, Diocese>;
}

/** "Diocese of Buffalo" for "Roman Catholic Diocese of Buffalo". */
export function dioceseLabel(name: string): string {
  return name.trim().replace(/^(?:the\s+)?(?:roman\s+)?catholic\s+/i, "");
}

/** "Buffalo" for "Diocese of Buffalo": what dioceses sort by, so an archdiocese doesn't lead. */
export function diocesePlace(label: string): string {
  return label.replace(/^(?:arch)?diocese\s+of\s+/i, "");
}

/** Site-relative path of a diocese page. */
export function diocesePath(slug: string): string {
  return `${DIOCESE_INDEX_PATH}${encodeURIComponent(slug)}/`;
}

/** The link to a diocese's page, or null when it has none (it isn't covered). */
export function dioceseLinkFor(diocese: Diocese | undefined): DioceseLink | null {
  return diocese?.covered ? { slug: diocese.slug, label: diocese.label } : null;
}

/**
 * Put `churches` (the site's) into the dioceses `records` lists them under,
 * and each diocese's cities from `cities` (buildCityIndex's). Dioceses with
 * no church on the site are left out.
 *
 * A church `records` doesn't list is in its city's diocese, when the city's
 * other churches are all in one. That covers the churches a promotion took
 * out of data/churches.csv, which the published data keeps until a reviewed
 * weekly run removes them.
 */
export function buildDioceseIndex(
  churches: ChurchBase[],
  cities: City[],
  records: DioceseRecords,
): DioceseIndex {
  const listed = new Map<string, string>();
  for (const [slug, record] of Object.entries(records)) {
    for (const church of record.churches) listed.set(church, slug);
  }

  // The one diocese each city's listed churches are in; null when several.
  const cityDiocese = new Map<string, string | null>();
  for (const city of cities) {
    for (const church of city.churches) {
      const slug = listed.get(church.slug);
      if (!slug) continue;
      const seen = cityDiocese.get(city.slug);
      cityDiocese.set(city.slug, seen === undefined || seen === slug ? slug : null);
    }
  }

  const members = new Map<string, ChurchBase[]>();
  for (const church of churches) {
    const citySlug = citySlugFor(church);
    const slug =
      listed.get(church.slug) ?? (citySlug ? cityDiocese.get(citySlug) : undefined);
    if (!slug) continue;
    const list = members.get(slug);
    if (list) list.push(church);
    else members.set(slug, [church]);
  }

  const dioceses: Diocese[] = [];
  for (const [slug, list] of members) {
    const record = records[slug];
    dioceses.push({
      slug,
      name: record.name,
      label: dioceseLabel(record.name),
      state: record.state,
      website: record.website,
      covered: record.covered,
      churches: list,
      cities: [],
    });
  }
  dioceses.sort(
    (a, b) =>
      diocesePlace(a.label).localeCompare(diocesePlace(b.label)) ||
      a.slug.localeCompare(b.slug),
  );
  const bySlug = new Map(dioceses.map((d) => [d.slug, d]));
  const byChurch = new Map<string, Diocese>();
  for (const diocese of dioceses) {
    for (const church of diocese.churches) byChurch.set(church.slug, diocese);
  }

  // `cities` is by label, so each diocese's cities are too.
  const byCity = new Map<string, Diocese>();
  for (const city of cities) {
    const counts = new Map<Diocese, number>();
    for (const church of city.churches) {
      const diocese = byChurch.get(church.slug);
      if (diocese) counts.set(diocese, (counts.get(diocese) ?? 0) + 1);
    }
    for (const [diocese, churchCount] of counts) {
      diocese.cities.push({ city, churchCount });
    }
    if (counts.size === 1) byCity.set(city.slug, [...counts.keys()][0]);
  }

  return { dioceses, bySlug, byChurch, byCity };
}

/** "1 church", "145 churches". */
export function countChurches(count: number): string {
  return `${count} ${count === 1 ? "church" : "churches"}`;
}

/** "1 city or town", "52 cities and towns". */
export function countCities(count: number): string {
  return count === 1 ? "1 city or town" : `${count} cities and towns`;
}

/** "145 churches in 52 cities and towns": how much of the diocese the site lists. */
export function dioceseCoverage(diocese: Pick<Diocese, "churches" | "cities">): string {
  return `${countChurches(diocese.churches.length)} in ${countCities(diocese.cities.length)}`;
}
