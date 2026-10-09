/**
 * The site's own visitor analytics: what pages are seen and what people do on
 * them, recorded by the Worker in Workers Analytics Engine (worker/index.ts).
 * No third party, no cookies, no free text, and nothing that outlives the
 * visit; see docs/analytics.md for what's recorded and how to query it.
 *
 * Events wait in memory and go in one request when the page is hidden or
 * left (or the batch fills), so a page costs one Worker invocation however
 * much is done on it. Nothing is sent from automated browsers, or when the
 * visitor asks not to be tracked (Global Privacy Control, Do Not Track).
 */
import {
  ANALYTICS_PATH,
  MAX_EVENTS_PER_BATCH,
  type AnalyticsBatch,
  type AnalyticsDevice,
  type AnalyticsEvent,
  type AnalyticsEventName,
} from "./analyticsApi";

const SESSION_KEY = "project-carlo:analytics-session";

/** A visit ends after this long without an event, as in most analytics. */
const SESSION_IDLE_MS = 30 * 60 * 1000;

/** What an event says beyond its name and page. */
export type AnalyticsProps = Pick<AnalyticsEvent, "kind" | "target" | "detail">;

interface Session {
  id: string;
  /** Whether this page load began the visit. */
  isNew: boolean;
}

const queue: AnalyticsEvent[] = [];
let session: Session | null = null;
let lastPageviewPath: string | null = null;
let started = false;

function isEnabled(): boolean {
  if (typeof window === "undefined") return false;
  const nav = navigator as Navigator & { globalPrivacyControl?: boolean };
  if (nav.webdriver || nav.globalPrivacyControl || nav.doNotTrack === "1") {
    return false;
  }
  return true;
}

function randomId(): string {
  const bytes = crypto.getRandomValues(new Uint8Array(8));
  return Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");
}

/**
 * The visit this page load belongs to: the tab's, unless it has been idle
 * past SESSION_IDLE_MS. Without sessionStorage each page load is a visit.
 */
function currentSession(): Session {
  const now = Date.now();
  if (!session) {
    let stored: { id?: unknown; last?: unknown } | null = null;
    try {
      stored = JSON.parse(sessionStorage.getItem(SESSION_KEY) ?? "null");
    } catch {
      stored = null;
    }
    const fresh =
      typeof stored?.id === "string" &&
      typeof stored.last === "number" &&
      now - stored.last < SESSION_IDLE_MS;
    session = fresh
      ? { id: stored!.id as string, isNew: false }
      : { id: randomId(), isNew: true };
  }
  try {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify({ id: session.id, last: now }));
  } catch {
    // Private mode or storage blocked: the visit lasts this page.
  }
  return session;
}

export function deviceForWidth(width: number): AnalyticsDevice {
  if (width < 640) return "mobile";
  if (width < 1024) return "tablet";
  return "desktop";
}

function enqueue(event: AnalyticsEvent): void {
  queue.push(event);
  if (queue.length >= MAX_EVENTS_PER_BATCH) flush();
}

/** Records something the visitor did on the current page. */
export function track(name: AnalyticsEventName, props: AnalyticsProps = {}): void {
  if (!isEnabled()) return;
  currentSession();
  enqueue({ name, path: window.location.pathname, ...props });
}

/**
 * Records the current page as seen, once per path in a row (React's
 * development double-render, or a query-string change, doesn't count twice).
 * The first pageview of the page load carries the referring site and the
 * campaign it came from.
 */
export function trackPageview(): void {
  if (!isEnabled()) return;
  const path = window.location.pathname;
  if (path === lastPageviewPath) return;
  const first = lastPageviewPath === null;
  lastPageviewPath = path;
  const visit = currentSession();
  const event: AnalyticsEvent = { name: "pageview", path };
  if (first) {
    event.referrer = externalReferrer();
    const params = new URLSearchParams(window.location.search);
    event.campaign = params.get("utm_source") ?? params.get("ref") ?? undefined;
    event.entry = visit.isNew;
  }
  enqueue(event);
}

function externalReferrer(): string | undefined {
  try {
    const host = new URL(document.referrer).hostname;
    return host && host !== window.location.hostname ? host : undefined;
  } catch {
    return undefined;
  }
}

/** Sends what's waiting, in a request that survives the page being left. */
function flush(): void {
  if (queue.length === 0 || !session) return;
  const batch: AnalyticsBatch = {
    session: session.id,
    device: deviceForWidth(window.innerWidth),
    events: queue.splice(0, MAX_EVENTS_PER_BATCH),
  };
  // Sent as text/plain, the type a beacon needs no permission for; the
  // Worker reads JSON either way.
  const body = JSON.stringify(batch);
  try {
    if (navigator.sendBeacon?.(ANALYTICS_PATH, body)) return;
    void fetch(ANALYTICS_PATH, { method: "POST", body, keepalive: true }).catch(() => {});
  } catch {
    // Analytics never gets in the visitor's way.
  }
}

/**
 * Follows links off the site: the link's `data-track` names what it was
 * (say, "bulletin"), so a page marks its links instead of wiring handlers.
 */
function trackOutboundClick(event: MouseEvent): void {
  const link = (event.target as Element | null)?.closest?.("a[href]");
  if (!(link instanceof HTMLAnchorElement)) return;
  let url: URL;
  try {
    url = new URL(link.href, window.location.href);
  } catch {
    return;
  }
  if (!url.protocol.startsWith("http") || url.hostname === window.location.hostname) return;
  track("outbound", {
    kind: link.dataset.track || "link",
    target: url.hostname,
  });
}

/**
 * Starts sending: on the page being hidden or left, which is the last moment
 * a phone reliably gives a page. Call once per page load, before tracking.
 */
export function startAnalytics(): void {
  if (started || !isEnabled()) return;
  started = true;
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") flush();
  });
  window.addEventListener("pagehide", flush);
  // Capture, so a link that stops the click's propagation still counts; the
  // middle button opens links too.
  document.addEventListener("click", trackOutboundClick, true);
  document.addEventListener("auxclick", trackOutboundClick, true);
}
