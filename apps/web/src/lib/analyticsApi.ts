/**
 * The contract between the browser's analytics (analytics.ts) and the Worker
 * route that records it (worker/index.ts) in Workers Analytics Engine. Both
 * TypeScript projects include this file, as with approximateLocationApi.ts.
 * No DOM and no imports: the Worker bundle pulls in nothing else.
 *
 * What's recorded, and how to query it, is in docs/analytics.md.
 */

/** The Worker route the browser posts its batches of events to. */
export const ANALYTICS_PATH = "/api/events";

/** Events past this many in one batch are dropped. The browser sends a batch
 *  once it reaches this size; the Worker writes one data point per event. */
export const MAX_EVENTS_PER_BATCH = 25;

/** A request body past this many bytes is refused unread. */
export const MAX_BATCH_BYTES = 16_384;

/**
 * Every event the site records. A name not listed here is dropped, so a typo
 * can't start a series of its own.
 *
 * - pageview: a page was shown (`referrer`, `campaign` and `entry` set only here)
 * - search_select: a search result was picked (`kind` church or place;
 *   `target` the church's slug)
 * - locate: "Use my location" (`kind` located, denied, unavailable or unsupported)
 * - filter: the map's filters changed (`kind` event_type, days or clear;
 *   `detail` the event type)
 * - map_open: a city or church page's map was opened full screen
 * - feedback_open: the feedback form was opened (`target` the church's slug)
 * - outbound: a link off the site was followed (`kind` from the link's
 *   data-track attribute, else "link"; `target` the host)
 */
export const ANALYTICS_EVENT_NAMES = [
  "pageview",
  "search_select",
  "locate",
  "filter",
  "map_open",
  "feedback_open",
  "outbound",
] as const;

export type AnalyticsEventName = (typeof ANALYTICS_EVENT_NAMES)[number];

/** The visitor's screen, by the viewport's width when the batch was sent. */
export const ANALYTICS_DEVICES = ["mobile", "tablet", "desktop"] as const;

export type AnalyticsDevice = (typeof ANALYTICS_DEVICES)[number];

/** One thing a visitor did. Free text never goes in: no search queries, no
 *  place names, nothing that could say who or where someone is. */
export interface AnalyticsEvent {
  name: AnalyticsEventName;
  /** The page it happened on, without the query string. */
  path: string;
  kind?: string;
  target?: string;
  detail?: string;
  /** The host of the site that linked here, when it isn't this one. */
  referrer?: string;
  /** The link's utm_source (or ref) parameter. */
  campaign?: string;
  /** Whether this pageview began the visit. */
  entry?: boolean;
}

/** What the browser posts to ANALYTICS_PATH. */
export interface AnalyticsBatch {
  /**
   * A random id for the visit, kept in the tab's sessionStorage until it has
   * been idle half an hour: it counts visits and ties a visit's events
   * together, and outlives neither the tab nor the visit.
   */
  session: string;
  device: AnalyticsDevice;
  events: AnalyticsEvent[];
}

/**
 * One Analytics Engine data point. The positions are the dataset's columns,
 * which queries name (see docs/analytics.md), so never reorder them:
 *
 * - index1: session
 * - blob1 name, blob2 path, blob3 host (the site's, to tell previews from
 *   production), blob4 country, blob5 device, blob6 kind, blob7 target,
 *   blob8 detail, blob9 referrer, blob10 campaign
 * - double1: 1 for a pageview that began the visit, else 0
 */
export interface AnalyticsDataPoint {
  indexes: [string];
  blobs: string[];
  doubles: number[];
}

/** What the Worker knows of the request: never the visitor's address. */
export interface AnalyticsRequestContext {
  /** The hostname the page was served from. */
  host: string;
  /** Cloudflare's two-letter country code for the request, or "". */
  country: string;
}

const SESSION_PATTERN = /^[a-z0-9]{8,32}$/;
const MAX_PATH_LENGTH = 200;
const MAX_FIELD_LENGTH = 100;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isEventName(value: unknown): value is AnalyticsEventName {
  return (ANALYTICS_EVENT_NAMES as readonly unknown[]).includes(value);
}

function isDevice(value: unknown): value is AnalyticsDevice {
  return (ANALYTICS_DEVICES as readonly unknown[]).includes(value);
}

/** A string field cut to `max` characters, or undefined if it isn't one. */
function text(value: unknown, max = MAX_FIELD_LENGTH): string | undefined {
  if (typeof value !== "string") return undefined;
  const trimmed = value.trim();
  return trimmed ? trimmed.slice(0, max) : undefined;
}

function parseEvent(value: unknown): AnalyticsEvent | null {
  if (!isRecord(value) || !isEventName(value.name)) return null;
  const path = text(value.path, MAX_PATH_LENGTH);
  if (!path?.startsWith("/")) return null;
  return {
    name: value.name,
    path,
    kind: text(value.kind),
    target: text(value.target),
    detail: text(value.detail),
    referrer: text(value.referrer),
    campaign: text(value.campaign),
    entry: value.entry === true,
  };
}

/**
 * The batch a request body holds, with each field checked and cut to size and
 * any event that isn't one of ANALYTICS_EVENT_NAMES dropped; null if the body
 * isn't a batch at all. The body comes from anyone, so nothing is trusted.
 */
export function parseAnalyticsBatch(body: unknown): AnalyticsBatch | null {
  if (!isRecord(body)) return null;
  const session = body.session;
  if (typeof session !== "string" || !SESSION_PATTERN.test(session)) return null;
  if (!Array.isArray(body.events)) return null;
  const events = body.events
    .slice(0, MAX_EVENTS_PER_BATCH)
    .map(parseEvent)
    .filter((event): event is AnalyticsEvent => event !== null);
  if (events.length === 0) return null;
  return {
    session,
    device: isDevice(body.device) ? body.device : "desktop",
    events,
  };
}

/** The data point an event is written as; see AnalyticsDataPoint. */
export function analyticsDataPoint(
  batch: AnalyticsBatch,
  event: AnalyticsEvent,
  context: AnalyticsRequestContext,
): AnalyticsDataPoint {
  return {
    indexes: [batch.session],
    blobs: [
      event.name,
      event.path,
      context.host,
      context.country,
      batch.device,
      event.kind ?? "",
      event.target ?? "",
      event.detail ?? "",
      event.referrer ?? "",
      event.campaign ?? "",
    ],
    doubles: [event.entry ? 1 : 0],
  };
}

/** Whether a User-Agent is a crawler or a script rather than a person's browser. */
export function isBotUserAgent(userAgent: string | null): boolean {
  if (!userAgent) return true;
  return /bot|crawl|spider|slurp|headless|lighthouse|preview|python|curl|wget|httpclient/i.test(
    userAgent,
  );
}
