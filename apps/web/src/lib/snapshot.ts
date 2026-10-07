import type { ChurchBase, ChurchDetail, EventType, RawEvent } from "../types";
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
export const SNAPSHOT_VERSION = 1;

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

interface SnapshotDocument {
  version: number;
  churches: Table<ChurchDetail>;
  events: Table<EventRow>;
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
  private nextOccurrence: string | null | undefined = undefined;

  constructor(columns: Columns<EventRow>, row: number) {
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
  }

  get occurrence(): string | null {
    if (this.nextOccurrence === undefined) {
      this.nextOccurrence = computeNextOccurrence(this);
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

  const c = decodeTable(document.churches);
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
  const { homepage_url: homepageUrls, bulletin_url: bulletinUrls } = c;

  const e = decodeTable(document.events);
  const events: RawEvent[] = e.id.map((_, row) => new SnapshotEvent(e, row));

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
