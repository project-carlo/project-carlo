import type {
  ChurchBase,
  ChurchDetail,
  EventType,
  RawEvent,
  WeekOfMonth,
} from "../types";
import { computeNextOccurrence } from "./schedule";

/**
 * The data snapshot (`frontend.json.gz`): every church and event the site
 * shows, as gzipped column-oriented JSON written by
 * src/pdf_extract/extract_frontend_db.py, whose docstring describes the
 * format. Decoded once into objects, shared by the SPA (api.ts) and the
 * prerenderer (scripts/prerender.ts). Pure; no DOM or React dependencies.
 */
export const SNAPSHOT_FILE = "frontend.json.gz";

/** The format version this code reads; must match the pipeline's SNAPSHOT_VERSION. */
export const SNAPSHOT_VERSION = 2;

type Column<T> =
  | T[]
  | { values: NonNullable<T>[]; codes: (number | null)[] }
  | { deltas: number[] };

/** An event as the snapshot stores it: everything but the computed occurrence. */
type EventRow = Omit<RawEvent, "occurrence">;

/** A table as stored: one encoded column per field. */
type Table<Row> = { [K in keyof Row]: Column<Row[K]> };

/** A table decoded: one plain array per field. */
type Columns<Row> = { [K in keyof Row]: Row[K][] };

/**
 * Church columns added since version 1 shipped (the pipeline's
 * ADDED_COLUMNS). A snapshot written before one was added lacks it, and it
 * reads as null: such a snapshot is still served while a deploy is pending.
 */
type AddedChurchColumns = "bulletin_week";

/** Event columns added since version 1 shipped; a snapshot without one reads it as false. */
type AddedEventColumns = "exclude_weeks";

/** An event row's columns as stored, the added ones possibly missing. */
type EventTable = Table<Omit<EventRow, AddedEventColumns>> &
  Partial<Table<Pick<EventRow, AddedEventColumns>>>;
type EventColumns = Columns<Omit<EventRow, AddedEventColumns>> &
  Partial<Columns<Pick<EventRow, AddedEventColumns>>>;

interface SnapshotDocument {
  version: number;
  churches: Table<Omit<ChurchDetail, AddedChurchColumns>> &
    Partial<Table<Pick<ChurchDetail, AddedChurchColumns>>>;
  events: EventTable;
}

function decodeColumn<T>(column: Column<T>): T[] {
  if (Array.isArray(column)) return column;
  if ("codes" in column) {
    const { values, codes } = column;
    return codes.map((code) => (code === null ? null : values[code]) as T);
  }
  let total = 0;
  return column.deltas.map((delta) => (total += delta) as T);
}

function decodeTable<Row>(table: Table<Row>): Columns<Row> {
  const columns = {} as Columns<Row>;
  for (const name of Object.keys(table) as (keyof Row)[]) {
    columns[name] = decodeColumn(table[name]);
  }
  return columns;
}

/** Weekly event id → the dates (YYYY-MM-DD) cancellations name for it. */
type CancelledDates = Map<number, Set<string>>;

const NO_CANCELLED_DATES: ReadonlySet<string> = new Set();

/**
 * Which dates each weekly event is cancelled on: the `date` of every
 * cancelled row, under the `cancels_event_id` it names.
 */
function cancelledDatesByEvent(columns: EventColumns): CancelledDates {
  const byEvent: CancelledDates = new Map();
  columns.cancels_event_id.forEach((eventId, row) => {
    const date = columns.date[row];
    if (eventId === null || date === null || !columns.cancelled[row]) return;
    const dates = byEvent.get(eventId);
    if (dates) dates.add(date);
    else byEvent.set(eventId, new Set([date]));
  });
  return byEvent;
}

/**
 * A snapshot event. Its next occurrence is worked out the first time
 * something reads it: only the events a map popup or a church page shows
 * ever need one.
 */
class SnapshotEvent implements RawEvent {
  id: number;
  church_id: number;
  event_type: EventType;
  event_kind: "weekly" | "specific_date";
  day_of_week: string | null;
  date: string | null;
  start_time: number;
  end_time: number | null;
  cancelled: boolean;
  page_number: number | null;
  note: string | null;
  weeks_of_month: WeekOfMonth[];
  exclude_weeks: boolean;
  season_start_month: number | null;
  season_start_day: number | null;
  season_end_month: number | null;
  season_end_day: number | null;
  cancels_event_id: number | null;
  private readonly cancelledDates: CancelledDates;
  private nextOccurrence: string | null | undefined = undefined;

  constructor(
    columns: EventColumns,
    row: number,
    cancelledDates: CancelledDates,
  ) {
    this.id = columns.id[row];
    this.church_id = columns.church_id[row];
    this.event_type = columns.event_type[row];
    this.event_kind = columns.event_kind[row];
    this.day_of_week = columns.day_of_week[row];
    this.date = columns.date[row];
    this.start_time = columns.start_time[row];
    this.end_time = columns.end_time[row];
    this.cancelled = columns.cancelled[row];
    this.page_number = columns.page_number[row];
    this.note = columns.note[row];
    this.weeks_of_month = columns.weeks_of_month[row];
    this.exclude_weeks = columns.exclude_weeks?.[row] ?? false;
    this.season_start_month = columns.season_start_month[row];
    this.season_start_day = columns.season_start_day[row];
    this.season_end_month = columns.season_end_month[row];
    this.season_end_day = columns.season_end_day[row];
    this.cancels_event_id = columns.cancels_event_id[row];
    this.cancelledDates = cancelledDates;
  }

  get occurrence(): string | null {
    if (this.nextOccurrence === undefined) {
      this.nextOccurrence = computeNextOccurrence(
        this,
        undefined,
        this.cancelledDates.get(this.id) ?? NO_CANCELLED_DATES,
      );
    }
    return this.nextOccurrence;
  }
}

export interface Snapshot {
  /** Every church, ordered by name (then id). */
  churches: ChurchBase[];
  /** Every event, in id order. */
  events: RawEvent[];
  /** The church with this slug, plus the parish links its page shows. */
  churchDetail(slug: string): ChurchDetail | null;
  /** One church's events, in id order. */
  eventsOf(churchId: number): RawEvent[];
}

/** The snapshot is in a format this code doesn't read. */
export class SnapshotVersionError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "SnapshotVersionError";
  }
}

/** Decode the (already gunzipped) snapshot JSON. */
export function parseSnapshot(json: string): Snapshot {
  const document = JSON.parse(json) as SnapshotDocument;
  if (document?.version !== SNAPSHOT_VERSION) {
    throw new SnapshotVersionError(
      `${SNAPSHOT_FILE} is format version ${String(document?.version)}, but this ` +
        `code reads version ${SNAPSHOT_VERSION}. Rebuild it with the pipeline ` +
        "code from this checkout (`pnpm extract:web`, or `pnpm data:pull`).",
    );
  }

  const c = decodeTable(document.churches) as Columns<
    Omit<ChurchDetail, AddedChurchColumns>
  > &
    Partial<Columns<Pick<ChurchDetail, AddedChurchColumns>>>;
  const churches: ChurchBase[] = c.id.map((id, row) => ({
    id,
    parish_id: c.parish_id[row],
    slug: c.slug[row],
    name: c.name[row],
    address_line1: c.address_line1[row],
    address_line2: c.address_line2[row],
    city: c.city[row],
    state: c.state[row],
    postal_code: c.postal_code[row],
    latitude: c.latitude[row],
    longitude: c.longitude[row],
  }));
  const rowBySlug = new Map(c.slug.map((slug, row) => [slug, row]));
  const {
    homepage_url: homepageUrls,
    bulletin_url: bulletinUrls,
    bulletin_week: bulletinWeeks,
  } = c;

  const e = decodeTable(document.events) as EventColumns;
  const cancelled = cancelledDatesByEvent(e);
  const events: RawEvent[] = e.id.map(
    (_, row) => new SnapshotEvent(e, row, cancelled),
  );

  let eventsByChurch: Map<number, RawEvent[]> | null = null;

  return {
    churches,
    events,
    churchDetail(slug) {
      const row = rowBySlug.get(slug);
      if (row === undefined) return null;
      return {
        ...churches[row],
        homepage_url: homepageUrls[row],
        bulletin_url: bulletinUrls[row],
        bulletin_week: bulletinWeeks?.[row] ?? null,
      };
    },
    eventsOf(churchId) {
      if (!eventsByChurch) {
        eventsByChurch = new Map();
        for (const ev of events) {
          const list = eventsByChurch.get(ev.church_id);
          if (list) list.push(ev);
          else eventsByChurch.set(ev.church_id, [ev]);
        }
      }
      return eventsByChurch.get(churchId) ?? [];
    },
  };
}
