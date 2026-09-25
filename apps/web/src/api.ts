import { filterDayFromJsDay, jsDayFor } from "./constants/days";
import { EVENT_TYPE_ORDER } from "./constants/eventTypes";
import { compareSchedule, parseIsoDateLocal } from "./lib/schedule";
import { parseSnapshot, SNAPSHOT_FILE, type Snapshot } from "./lib/snapshot";
import type {
  ChurchBase,
  ChurchDetail,
  ChurchMapItem,
  EventSummary,
  EventType,
  RawEvent,
} from "./types";

export class ChurchNotFoundError extends Error {
  readonly slug: string;
  constructor(slug: string) {
    super(`Church not found: ${slug}`);
    this.name = "ChurchNotFoundError";
    this.slug = slug;
  }
}

export interface ChurchFilters {
  types: EventType[];
  daysOfWeek?: number[];
  timeFrom?: number;
  timeTo?: number;
}

// The snapshot is loaded once and never mutated, so every church and event is
// decoded into memory once and reused for every filter change. This keeps the
// slider drag → map update path JS-only after the first call.
let snapshotPromise: Promise<Snapshot> | null = null;

async function loadSnapshot(): Promise<Snapshot> {
  const response = await fetch(`/${SNAPSHOT_FILE}`, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Failed to fetch ${SNAPSHOT_FILE}: ${response.status}`);
  }
  // Served as an opaque pre-gzipped file (see public/_headers): unzip it here.
  const compressed = response.body ?? new Blob([await response.arrayBuffer()]).stream();
  const decompressed = compressed.pipeThrough(new DecompressionStream("gzip"));
  return parseSnapshot(await new Response(decompressed).text());
}

function getSnapshot(): Promise<Snapshot> {
  if (!snapshotPromise) {
    snapshotPromise = loadSnapshot().catch((error: unknown) => {
      // Don't hold on to a failed load: callers retry (react-query does so
      // automatically), and a cached rejection would make every retry fail
      // instantly without touching the network again.
      snapshotPromise = null;
      throw error;
    });
  }
  return snapshotPromise;
}

function toEventSummary(ev: RawEvent): EventSummary {
  return {
    id: ev.id,
    type: ev.event_type,
    kind: ev.event_kind,
    day_of_week: ev.day_of_week,
    date: ev.date,
    start_time: ev.start_time,
    end_time: ev.end_time,
    cancelled: ev.cancelled,
    next_occurrence: ev.occurrence,
    page_number: ev.page_number,
    note: ev.note,
  };
}

export function eventMatchesFilters(
  ev: RawEvent,
  filters: ChurchFilters,
): boolean {
  if (ev.cancelled) return false;
  if (filters.daysOfWeek && filters.daysOfWeek.length > 0) {
    if (ev.event_kind === "weekly" && ev.day_of_week) {
      const dayIdx = filterDayFromJsDay(jsDayFor(ev.day_of_week));
      if (dayIdx < 0 || !filters.daysOfWeek.includes(dayIdx)) return false;
    }
    // For specific_date, check if the date falls on a selected weekday
    if (ev.event_kind === "specific_date" && ev.date) {
      const d = parseIsoDateLocal(ev.date);
      if (!d) return false;
      if (!filters.daysOfWeek.includes(filterDayFromJsDay(d.getDay()))) {
        return false;
      }
    }
  }
  if (
    filters.timeFrom != null &&
    filters.timeTo != null &&
    (ev.start_time < filters.timeFrom || ev.start_time > filters.timeTo)
  ) {
    return false;
  }
  return true;
}

function buildMapItem(
  church: ChurchBase,
  churchEvents: RawEvent[],
): ChurchMapItem {
  const weeklyEvents = churchEvents.filter(
    (e) => e.event_kind === "weekly" && e.day_of_week && !e.cancelled,
  );
  // Dedup repeated weekly slots (same weekday + start time) that occasionally
  // appear across bulletins. Prefer weekly events for the popup; if the parish
  // has only specific-date events, fall back to the five soonest occurrences.
  const seen = new Set<string>();
  let popupSchedule = weeklyEvents
    .filter((e) => {
      const key = `${e.day_of_week!.toLowerCase()}-${e.start_time}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .map(toEventSummary)
    .sort((a, b) => compareSchedule(a, b));
  if (popupSchedule.length === 0) {
    popupSchedule = churchEvents
      .filter((e) => e.occurrence !== null)
      .sort((a, b) => a.occurrence!.localeCompare(b.occurrence!))
      .slice(0, 5)
      .map(toEventSummary);
  }
  const eventTypes = [
    ...new Set(churchEvents.map((e) => e.event_type)),
  ].sort() as EventType[];
  return {
    ...church,
    event_types: eventTypes,
    upcoming_events: popupSchedule,
  };
}

// Per-church memo of the last map item handed out, keyed by the church row and
// the ids of the events that produced the item. Dragging the time slider
// re-runs this query on every input event, and for most parishes the matching
// events don't change from one step to the next; handing back the identical
// object then lets React.memo skip the marker (and Leaflet skip re-positioning
// it) instead of re-rendering all ~130 pins. Bounded by the church count.
const mapItemCache = new Map<
  number,
  { church: ChurchBase; signature: string; item: ChurchMapItem }
>();

/**
 * Drop the memo. Only needed in tests: the app loads one immutable snapshot,
 * so an event id always denotes the same event and the memo can never go
 * stale. A test suite, though, builds fresh fixtures — and one that shares a
 * church object between cases (a hoisted fixture) while varying the event
 * data behind the same ids would otherwise be served the earlier case's item.
 */
export function resetMapItemCache(): void {
  mapItemCache.clear();
}

/**
 * Build the map items for one set of filters, reusing the previous item for
 * every church whose matching events are unchanged.
 *
 * Exported for tests; `fetchChurches` is the app-facing entry point.
 */
export function collectMapItems(
  churches: ChurchBase[],
  allEvents: RawEvent[],
  filters: ChurchFilters,
): ChurchMapItem[] {
  const types = filters.types.length > 0 ? filters.types : EVENT_TYPE_ORDER;
  const typeSet = new Set<EventType>(types);

  const grouped = new Map<number, RawEvent[]>();
  for (const ev of allEvents) {
    if (!typeSet.has(ev.event_type)) continue;
    if (!eventMatchesFilters(ev, filters)) continue;
    let list = grouped.get(ev.church_id);
    if (!list) {
      list = [];
      grouped.set(ev.church_id, list);
    }
    list.push(ev);
  }

  const items: ChurchMapItem[] = [];
  for (const church of churches) {
    const churchEvents = grouped.get(church.id);
    // No matching events means no event types, which the map never showed.
    if (!churchEvents || churchEvents.length === 0) continue;

    // Events are grouped in a stable order, so their ids fully describe the
    // item this church produces.
    let signature = "";
    for (const ev of churchEvents) signature += `${ev.id},`;

    const cached = mapItemCache.get(church.id);
    if (cached && cached.church === church && cached.signature === signature) {
      items.push(cached.item);
      continue;
    }
    const item = buildMapItem(church, churchEvents);
    mapItemCache.set(church.id, { church, signature, item });
    items.push(item);
  }
  return items;
}

export async function fetchChurches(
  filters: ChurchFilters,
): Promise<ChurchMapItem[]> {
  const { churches, events } = await getSnapshot();
  return collectMapItems(churches, events, filters);
}

/** What the typeahead gets back: the shared church row, geocoded ones only. */
export type ChurchSearchResult = ChurchBase;

export async function fetchAllChurchesForSearch(): Promise<
  ChurchSearchResult[]
> {
  const { churches } = await getSnapshot();
  return churches.filter((c) => c.latitude !== null && c.longitude !== null);
}

/** One church with its parish links; shared with the prerenderer. */
export function findChurch(snapshot: Snapshot, slug: string): ChurchDetail {
  const church = snapshot.churchDetail(slug);
  if (!church) throw new ChurchNotFoundError(slug);
  return church;
}

/**
 * A church page's schedule: its upcoming events of the given types (all types
 * when none are given), in schedule order. Cancelled events and past dates
 * have no next occurrence and are left out. Shared with the prerenderer, so a
 * static church page lists the same events as the live one.
 */
export function churchSchedule(
  snapshot: Snapshot,
  slug: string,
  types: EventType[],
): EventSummary[] {
  const typeSet = new Set(types.length > 0 ? types : EVENT_TYPE_ORDER);
  const church = findChurch(snapshot, slug);
  return snapshot
    .eventsOf(church.id)
    .filter((e) => typeSet.has(e.event_type) && e.occurrence !== null)
    .map(toEventSummary)
    .sort((a, b) => compareSchedule(a, b));
}

export async function fetchChurch(slug: string): Promise<ChurchDetail> {
  return findChurch(await getSnapshot(), slug);
}

export async function fetchChurchEvents(
  slug: string,
  types: EventType[],
): Promise<EventSummary[]> {
  return churchSchedule(await getSnapshot(), slug, types);
}
