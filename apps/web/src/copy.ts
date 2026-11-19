/**
 * Visitor-facing strings that appear in more than one place, or that name one
 * of the site's fixed terms (an action, a filter, a fallback), so a wording
 * change is a one-line edit. Other one-off strings stay beside their markup.
 *
 * Apostrophes are typographic (’), as they are everywhere on the site.
 * docs/ui-copy-audit.md has the terminology these follow.
 */

import type { ChurchDetail, ScheduleSource } from "@carlo/core";

/**
 * Where the times come from, as the end of a sentence: "…times, from each
 * parish’s bulletin or website." Most come from the weekly bulletin; a parish
 * with none posts them on its own website or Facebook page.
 */
export const SOURCE_PHRASE = "from each parish’s bulletin or website";

/** The accuracy note at the foot of city pages, whose churches' sources vary. */
export const DISCLAIMER =
  "Times are read from each parish’s bulletin or website by AI and can contain mistakes. Please check with the parish before you go.";

/** A parish's page its times are read from, when it has no bulletin. */
export const SOURCE_NAMES: Record<ScheduleSource, string> = {
  website: "the parish website",
  facebook: "the parish’s Facebook page",
};

/**
 * The accuracy note at the foot of a church page, naming that church's source.
 * A bulletin church's is the wording every church page has always had, so its
 * page (and sitemap date) doesn't change.
 */
export function churchDisclaimer(church: ChurchDetail): string {
  if (church.schedule_source) {
    return `Times are read from ${SOURCE_NAMES[church.schedule_source]} by AI and can contain mistakes, and the parish may have changed them since. Please check with the parish before you go.`;
  }
  return "Times are read from each parish’s bulletin by AI and can contain mistakes. Please check with the parish before you go.";
}

/** The name shown for a church the data has no name for. */
export const UNNAMED_CHURCH = "Unnamed church";

/**
 * The link to the map from pages a visitor can land on straight from a search
 * engine, where "Back to map" would point at a page they never saw.
 */
export const MAP_LINK = "Map";

/** The all-churches index, as links and breadcrumbs name it. */
export const CHURCH_LIST = "Church list";

/** Asking the browser for the visitor's position, and the wait for it. */
export const USE_MY_LOCATION = "Use my location";
export const FINDING_YOUR_LOCATION = "Finding your location…";
/** The visitor's own position, once found: the pin's name. */
export const YOUR_LOCATION = "Your location";
/** The way forward when the browser can't give a position. */
export const LOCATION_FALLBACK = "Try searching for your town instead.";

/** Filter section headings, shared by the map's panel and the landing page. */
export const FILTER_SERVICE_HEADING = "Looking for";
export const FILTER_DAY_HEADING = "Day of week";
/** The time filter matches a service's start time, not any time it runs. */
export const FILTER_TIME_HEADING = "Starting";
/** Each section's clear button names the state it returns to. */
export const ANY_DAY = "Any day";
export const ANY_TIME = "Any time";
export const CLEAR_FILTERS = "Clear filters";
