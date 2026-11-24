import type {
  ChapelAccess,
  ChurchBase,
  ChurchDetail,
  ChurchKind,
  ContinuousAdoration,
  EventType,
  RawEvent,
  WeekOfMonth,
} from "./types";
import { computeNextOccurrence } from "./schedule";

/**
 * The data snapshot (`frontend.json.gz`): every church and event the site
 * shows, as gzipped column-oriented JSON written by
 * src/pdf_extract/extract_frontend_db.py, whose docstring describes the
 * format. Chapels open 24 hours (`continuous` rows, which have no day or
 * time) are read into their own list, so every event keeps a numeric
 * `start_time`. Decoded once into objects, shared by the SPA (apps/web/src/api.ts)
 * and the prerenderer (apps/web/scripts/prerender.ts). Pure; no DOM or React
 * dependencies.
 */
export const SNAPSHOT_FILE = "frontend.json.gz";

/** Latest format; must match the pipeline. The reader also accepts formats 2 and 3. */
export const SNAPSHOT_VERSION = 4;
const READABLE_VERSIONS = [2, 3, SNAPSHOT_VERSION];

type Column<T> =
  | T[]
  | { values: NonNullable<T>[]; codes: (number | null)[] }
  | { deltas: number[] };

/**
 * An event as the snapshot stores it: everything but the computed occurrence,
 * plus a chapel's access columns (null on every timed row). A `continuous`
 * row has a null `start_time`.
 */
type EventRow = Omit<RawEvent, "occurrence" | "event_kind"> & {
  event_kind: RawEvent["event_kind"] | "continuous";
  access: ChapelAccess | null;
  open_from: number | null;
  open_until: number | null;
};

/** A table as stored: one encoded column per field. */
type Table<Row> = { [K in keyof Row]: Column<Row[K]> };

/** A table decoded: one plain array per field. */
type Columns<Row> = { [K in keyof Row]: Row[K][] };

/**
 * Church columns added since version 1 shipped (the pipeline's
 * ADDED_COLUMNS). A snapshot written before one was added lacks it, and it
 * reads as null: such a snapshot is still served while a deploy is pending.
 */
type AddedChurchColumns =
  | "bulletin_week"
  | "schedule_source"
  | "source_url"
  | "checked_on"
  | "kind"
  | "diocese";

/** Older snapshots have no exclusions, absolute date bounds or chapels. */
type AddedEventColumns =
  | "exclude_weeks"
  | "valid_from"
  | "valid_until"
  | "access"
  | "open_from"
  | "open_until";

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
  valid_from: string | null;
  valid_until: string | null;
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
    this.event_kind = columns.event_kind[row] as RawEvent["event_kind"];
    this.day_of_week = columns.day_of_week[row];
    this.date = columns.date[row];
    this.start_time = columns.start_time[row] as number;
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
    this.valid_from = columns.valid_from?.[row] ?? null;
    this.valid_until = columns.valid_until?.[row] ?? null;
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
  /** Every timed event, in id order: chapels open 24 hours are in `continuous`. */
  events: RawEvent[];
  /** Every chapel open 24 hours, in id order. */
  continuous: ContinuousAdoration[];
  /** The church with this slug, plus the parish links its page shows. */
  churchDetail(slug: string): ChurchDetail | null;
  /** One church's events, in id order. */
  eventsOf(churchId: number): RawEvent[];
  /** One church's chapels open 24 hours (usually none or one), in id order. */
  continuousOf(churchId: number): ContinuousAdoration[];
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
  if (!READABLE_VERSIONS.includes(document?.version)) {
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
  const kinds = c.kind;
  const dioceses = c.diocese;
  const churches: ChurchBase[] = c.id.map((id, row) => ({
    id,
    parish_id: c.parish_id[row],
    slug: c.slug[row],
    kind: (kinds?.[row] ?? "church") as ChurchKind,
    name: c.name[row],
    address_line1: c.address_line1[row],
    address_line2: c.address_line2[row],
    city: c.city[row],
    state: c.state[row],
    postal_code: c.postal_code[row],
    latitude: c.latitude[row],
    longitude: c.longitude[row],
    diocese: dioceses?.[row] ?? null,
  }));
  const rowBySlug = new Map(c.slug.map((slug, row) => [slug, row]));
  const {
    homepage_url: homepageUrls,
    bulletin_url: bulletinUrls,
    bulletin_week: bulletinWeeks,
    schedule_source: scheduleSources,
    source_url: sourceUrls,
    checked_on: checkedOn,
  } = c;

  const e = decodeTable(document.events) as EventColumns;
  const cancelled = cancelledDatesByEvent(e);
  const events: RawEvent[] = [];
  const continuous: ContinuousAdoration[] = [];
  e.id.forEach((id, row) => {
    if (e.event_kind[row] !== "continuous") {
      events.push(new SnapshotEvent(e, row, cancelled));
      return;
    }
    continuous.push({
      id,
      church_id: e.church_id[row],
      access: e.access?.[row] ?? "not_stated",
      open_from: e.open_from?.[row] ?? null,
      open_until: e.open_until?.[row] ?? null,
      note: e.note[row],
      page_number: e.page_number[row],
      valid_from: e.valid_from?.[row] ?? null,
      valid_until: e.valid_until?.[row] ?? null,
    });
  });

  let eventsByChurch: Map<number, RawEvent[]> | null = null;
  let continuousByChurch: Map<number, ContinuousAdoration[]> | null = null;

  return {
    churches,
    events,
    continuous,
    churchDetail(slug) {
      const row = rowBySlug.get(slug);
      if (row === undefined) return null;
      return {
        ...churches[row],
        homepage_url: homepageUrls[row],
        bulletin_url: bulletinUrls[row],
        bulletin_week: bulletinWeeks?.[row] ?? null,
        schedule_source: scheduleSources?.[row] ?? null,
        source_url: sourceUrls?.[row] ?? null,
        checked_on: checkedOn?.[row] ?? null,
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
    continuousOf(churchId) {
      if (!continuousByChurch) {
        continuousByChurch = new Map();
        for (const chapel of continuous) {
          const list = continuousByChurch.get(chapel.church_id);
          if (list) list.push(chapel);
          else continuousByChurch.set(chapel.church_id, [chapel]);
        }
      }
      return continuousByChurch.get(churchId) ?? [];
    },
  };
}
