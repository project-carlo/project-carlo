/**
 * Visitor-facing strings that appear in more than one place, or that name one
 * of the site's fixed terms (an action, a filter, a fallback), so a wording
 * change is a one-line edit. Other one-off strings stay beside their markup.
 *
 * Apostrophes are typographic (’), as they are everywhere on the site.
 * docs/ui-copy-audit.md has the terminology these follow.
 */

/** Where the times come from, as the end of a sentence: "…times, from each parish’s weekly bulletin." */
export const SOURCE_PHRASE = "from each parish’s weekly bulletin";

/** The accuracy note at the foot of church and city pages. */
export const DISCLAIMER =
  "Times are read from each parish’s bulletin by AI and can contain mistakes. Please check with the parish before you go.";

/** The name shown for a church the data has no name for. */
export const UNNAMED_CHURCH = "Unnamed church";

/**
 * The link to the map from pages a visitor can land on straight from a search
 * engine, where "Back to map" would point at a page they never saw.
 */
export const MAP_LINK = "Map";

/** The all-churches index, as links and breadcrumbs name it. */
export const ALL_CHURCHES = "All churches";

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
