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
} from "./lib/schedule";
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
}

// frontend.snapshot is loaded once and never mutated, so the church and event
// tables can be read into memory once and reused for every filter change.
// This keeps the slider drag → map update path JS-only after the first call.
let allChurchesPromise: Promise<ChurchBase[]> | null = null;
let allEventsPromise: Promise<RawEvent[]> | null = null;

function mapEventRow(row: Record<string, unknown>): RawEvent {
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
            page_number, note
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

export async function fetchChurches(
  filters: ChurchFilters,
): Promise<ChurchMapItem[]> {
  const db = await getDb();
  const types = filters.types.length > 0 ? filters.types : EVENT_TYPE_ORDER;
  const typeSet = new Set<EventType>(types);

  const { churches, events: allEvents } = await loadCaches(db);

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

  return churches
    .map((c) => {
      const churchEvents = grouped.get(c.id) ?? [];
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
        ...c,
        event_types: eventTypes,
        upcoming_events: popupSchedule,
      };
    })
    .filter((church) => church.event_types.length > 0);
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
