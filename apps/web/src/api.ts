import type { Database } from "sql.js";
import { filterDayFromJsDay, jsDayFor } from "./constants/days";
import { EVENT_TYPE_ORDER } from "./constants/eventTypes";
import { getDb } from "./db";
import {
  CHURCH_COLUMNS,
  CHURCH_DETAIL_COLUMNS,
  mapChurchDetailRow,
  mapChurchRow,
} from "./lib/churchRow";
import {
  compareSchedule,
  computeNextOccurrence,
  parseIsoDateLocal,
  patternOf,
} from "./lib/schedule";
import {
  dateInSeason,
  parseSeasonDay,
  parseSeasonMonth,
  parseWeeksOfMonth,
  patternKey,
  type WeekOfMonth,
} from "./lib/schedulePattern";
import { num, str } from "./lib/sqlRow";
import type {
  ChurchBase,
  ChurchDetail,
  ChurchMapItem,
  EventSummary,
  EventType,
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

export interface RawEvent {
  id: number;
  church_id: number;
  event_type: EventType;
  event_kind: "weekly" | "specific_date";
  day_of_week: string | null;
  date: string | null;
  start_time: number;
  end_time: number | null;
  cancelled: boolean;
  occurrence: string | null;
  page_number: number | null;
  note: string | null;
  weeks_of_month: WeekOfMonth[];
  season_start_month: number | null;
  season_start_day: number | null;
  season_end_month: number | null;
  season_end_day: number | null;
}

// frontend.snapshot is loaded once and never mutated, so the church and event
// tables can be read into memory once and reused for every filter change.
// This keeps the slider drag → map update path JS-only after the first call.
let allChurchesPromise: Promise<ChurchBase[]> | null = null;
let allEventsPromise: Promise<RawEvent[]> | null = null;

function mapEventRow(row: Record<string, unknown>): RawEvent {
  const startMonth = parseSeasonMonth(row["season_start_month"]);
  const endMonth = parseSeasonMonth(row["season_end_month"]);
  const ev: RawEvent = {
    id: row["id"] as number,
    church_id: row["church_id"] as number,
    event_type: row["event_type"] as EventType,
    event_kind: row["event_kind"] as "weekly" | "specific_date",
    day_of_week: str(row["day_of_week"]),
    date: str(row["date"]),
    start_time: row["start_time"] as number,
    end_time: num(row["end_time"]),
    cancelled: Boolean(row["cancelled"]),
    occurrence: null,
    page_number: num(row["page_number"]),
    note: str(row["note"]),
    weeks_of_month: parseWeeksOfMonth(row["weeks_of_month"]),
    season_start_month: startMonth,
    season_start_day: parseSeasonDay(row["season_start_day"], startMonth),
    season_end_month: endMonth,
    season_end_day: parseSeasonDay(row["season_end_day"], endMonth),
  };
  ev.occurrence = computeNextOccurrence(ev);
  return ev;
}

async function loadCaches(
  db: Database,
): Promise<{ churches: ChurchBase[]; events: RawEvent[] }> {
  const churches = await (allChurchesPromise ??= Promise.resolve(
    loadAllChurches(db),
  ));
  const events = await (allEventsPromise ??= Promise.resolve(
    loadAllEvents(db),
  ));
  return { churches, events };
}

function loadAllChurches(db: Database): ChurchBase[] {
  const stmt = db.prepare(`SELECT ${CHURCH_COLUMNS} FROM church ORDER BY name`);
  const churches: ChurchBase[] = [];
  try {
    while (stmt.step()) {
      churches.push(mapChurchRow(stmt.getAsObject()));
    }
  } finally {
    stmt.free();
  }
  return churches;
}

function loadAllEvents(db: Database): RawEvent[] {
  const stmt = db.prepare(
    `SELECT id, church_id, event_type, event_kind,
            day_of_week, date, start_time, end_time, cancelled,
            page_number, note, weeks_of_month,
            season_start_month, season_start_day,
            season_end_month, season_end_day
     FROM event`,
  );
  const results: RawEvent[] = [];
  try {
    while (stmt.step()) {
      results.push(mapEventRow(stmt.getAsObject()));
    }
  } finally {
    stmt.free();
  }
  return results;
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
    weeks_of_month: ev.weeks_of_month,
    season_start_month: ev.season_start_month,
    season_start_day: ev.season_start_day,
    season_end_month: ev.season_end_month,
    season_end_day: ev.season_end_day,
  };
}

export function eventMatchesFilters(
  ev: RawEvent,
  filters: ChurchFilters,
  today: Date = new Date(),
): boolean {
  if (ev.cancelled) return false;
  // The map answers "where can I go this week", so a slot that does not resume
  // until October is not an answer in September. Monthly slots stay: they do
  // run at this time of year, and the popup says which week of the month.
  if (ev.event_kind === "weekly" && !dateInSeason(today, patternOf(ev))) {
    return false;
  }
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
      // Two slots on the same weekday and time are only the same slot when
      // they keep the same schedule: a first-Friday devotion is not a
      // duplicate of a Friday one that runs every week.
      const key = `${e.day_of_week!.toLowerCase()}-${e.start_time}-${patternKey(patternOf(e))}`;
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

  // One reading of "now" for the whole pass; this runs per event on the
  // slider-drag path.
  const today = new Date();
  const grouped = new Map<number, RawEvent[]>();
  for (const ev of allEvents) {
    if (!typeSet.has(ev.event_type)) continue;
    if (!eventMatchesFilters(ev, filters, today)) continue;
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
  const db = await getDb();
  const { churches, events } = await loadCaches(db);
  return collectMapItems(churches, events, filters);
}

/** What the typeahead gets back: the shared church row, geocoded ones only. */
export type ChurchSearchResult = ChurchBase;

export async function fetchAllChurchesForSearch(): Promise<
  ChurchSearchResult[]
> {
  const db = await getDb();
  const stmt = db.prepare(
    `SELECT ${CHURCH_COLUMNS} FROM church
     WHERE latitude IS NOT NULL AND longitude IS NOT NULL
     ORDER BY name`,
  );
  try {
    const results: ChurchSearchResult[] = [];
    while (stmt.step()) {
      results.push(mapChurchRow(stmt.getAsObject()));
    }
    return results;
  } finally {
    stmt.free();
  }
}

export async function fetchChurch(slug: string): Promise<ChurchDetail> {
  const db = await getDb();
  const stmt = db.prepare(
    `SELECT ${CHURCH_DETAIL_COLUMNS} FROM church WHERE slug = ?`,
  );
  try {
    stmt.bind([slug]);
    if (!stmt.step()) {
      throw new ChurchNotFoundError(slug);
    }
    return mapChurchDetailRow(stmt.getAsObject());
  } finally {
    stmt.free();
  }
}

export async function fetchChurchEvents(
  slug: string,
  types: EventType[],
): Promise<EventSummary[]> {
  const db = await getDb();
  const effectiveTypes = types.length > 0 ? types : EVENT_TYPE_ORDER;
  const typeSet = new Set(effectiveTypes);

  const { churches, events: allEvents } = await loadCaches(db);
  const church = churches.find((c) => c.slug === slug);
  if (!church) throw new ChurchNotFoundError(slug);

  return allEvents
    .filter((e) => e.church_id === church.id && typeSet.has(e.event_type))
    .filter((e) => e.occurrence !== null)
    .map(toEventSummary)
    .sort((a, b) => compareSchedule(a, b));
}
