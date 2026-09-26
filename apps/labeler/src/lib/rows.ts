import type {
  Day,
  EditorRow,
  EventKind,
  EventType,
  GeminiRow,
  LabelEvent,
  Origin,
} from "../types";
import { dateForWeekday, dayOfDate, daysBetween, formatDate } from "./dates";
import { seasonProblems } from "./pattern";
import { formatTime, minutesOf } from "./time";

let counter = 0;
export function newId(): string {
  counter += 1;
  return `r${Date.now().toString(36)}${counter}`;
}

export interface RowDefaults {
  church_slug: string;
  event_type: EventType;
  event_kind: EventKind;
  page_number: number | null;
}

/**
 * A new row: the previous row's church, type, kind and page, or the parish's
 * only church. The page being viewed in the PDF wins over the previous row's,
 * since that is where the labeller is reading.
 */
export function blankRow(
  previous: EditorRow | undefined,
  { churches, viewedPage }: { churches: string[]; viewedPage: number | null },
): EditorRow {
  return {
    id: newId(),
    church_slug: previous?.church_slug ?? (churches.length === 1 ? churches[0] : ""),
    event_type: previous?.event_type ?? "mass",
    event_kind: previous?.event_kind ?? "weekly",
    day_of_week: null,
    date: null,
    start_time: "",
    end_time: null,
    cancelled: false,
    weeks_of_month: [],
    season: null,
    page_number: viewedPage ?? previous?.page_number ?? null,
    note: null,
    origin: "human",
  };
}

/** A Gemini row accepted as ground truth. Unreadable fields stay empty for the labeller to fill. */
export function fromGemini(g: GeminiRow): EditorRow {
  const kind = g.event_kind ?? "weekly";
  return {
    id: newId(),
    gemini_id: g.id,
    church_slug: g.church_slug,
    event_type: g.event_type ?? "mass",
    event_kind: kind,
    day_of_week: kind === "weekly" ? g.day_of_week : null,
    date: kind === "specific_date" ? g.date : null,
    start_time: g.start_time ?? "",
    end_time: g.end_time,
    cancelled: g.cancelled,
    weeks_of_month: kind === "weekly" ? [...g.weeks_of_month] : [],
    season: kind === "weekly" && g.season ? { ...g.season } : null,
    page_number: g.page_number,
    note: g.note,
    origin: "gemini",
  };
}

function editedOrigin(origin: Origin): Origin {
  return origin === "human" ? "human" : "gemini-edited";
}

type Patch = Partial<Omit<EditorRow, "id" | "origin" | "gemini_id">>;

const SAME = (a: unknown, b: unknown) => JSON.stringify(a) === JSON.stringify(b);

/**
 * Apply an edit. A Gemini row that actually changes becomes "gemini-edited".
 * Switching kind clears what the other kind carries: a dated row has no
 * weekday, weeks of the month or season, and a weekly row has no date.
 */
export function editRow(row: EditorRow, patch: Patch): EditorRow {
  const changed = (Object.keys(patch) as (keyof Patch)[]).some((k) => !SAME(row[k], patch[k]));
  if (!changed) return row;
  const next: EditorRow = { ...row, ...patch, origin: editedOrigin(row.origin) };
  if (next.event_kind === "specific_date") {
    next.day_of_week = null;
    next.weeks_of_month = [];
    next.season = null;
  } else {
    next.date = null;
  }
  const pending = next.pending_split;
  if (!pending || !(next.event_kind === "weekly" ? pending.days : pending.dates)) delete next.pending_split;
  return next;
}

/**
 * Set a weekly row's day. Several days keep the first on the row and wait in
 * `pending_split` until focus leaves the row (see `expandPending`).
 */
export function setDays(row: EditorRow, days: Day[]): EditorRow {
  return editRow(row, {
    event_kind: "weekly",
    day_of_week: days[0] ?? null,
    pending_split: days.length > 1 ? { days } : undefined,
  });
}

/**
 * The one weekday a row is about: a weekly row's day, or the weekday of a
 * dated row. Several pending days or dates are not one weekday.
 */
export function weekdayOf(row: {
  event_kind: EventKind | null;
  day_of_week: Day | null;
  date: string | null;
  pending_split?: { days?: Day[]; dates?: string[] };
}): Day | null {
  const pendingDays = row.pending_split?.days;
  const pendingDates = row.pending_split?.dates;
  if ((pendingDays && pendingDays.length > 1) || (pendingDates && pendingDates.length > 1)) return null;
  if (row.event_kind === "specific_date") return row.date ? dayOfDate(row.date) : null;
  if (row.day_of_week) return row.day_of_week;
  return row.date ? dayOfDate(row.date) : null;
}

/**
 * Weekly, on that weekday, and only the first week of the month.
 * A dated row takes the weekday of its date. The note is cleared: it is
 * usually just "first of the month". Unchanged when there is no single weekday.
 */
export function asFirstOfMonth(row: EditorRow): EditorRow {
  const day = weekdayOf(row);
  if (!day) return row;
  return editRow(row, {
    event_kind: "weekly",
    day_of_week: day,
    weeks_of_month: ["first"],
    note: null,
  });
}

/** Already weekly on one weekday, first week only, with no note. */
export function isFirstOfMonth(row: EditorRow): boolean {
  return (
    row.event_kind === "weekly" &&
    !!row.day_of_week &&
    row.weeks_of_month.length === 1 &&
    row.weeks_of_month[0] === "first" &&
    !row.note?.trim() &&
    !row.pending_split
  );
}

/**
 * A weekly row as the date of its weekday in the bulletin's week.
 * Several pending days become several dates. Already-dated rows stay as they are.
 * With no bulletin date or no weekday, the row becomes dated and the date stays empty.
 */
export function asDated(row: EditorRow, bulletinDate: string | null): EditorRow {
  if (row.event_kind === "specific_date") return row;
  const days = row.pending_split?.days ?? (row.day_of_week ? [row.day_of_week] : []);
  const dates = bulletinDate ? days.map((day) => dateForWeekday(bulletinDate, day)).filter((d): d is string => !!d) : [];
  if (!dates.length) return editRow(row, { event_kind: "specific_date" });
  return setDates(row, dates);
}

/** Set a dated row's date, or several dates to split later. */
export function setDates(row: EditorRow, dates: string[]): EditorRow {
  return editRow(row, {
    event_kind: "specific_date",
    date: dates[0] ?? null,
    pending_split: dates.length > 1 ? { dates } : undefined,
  });
}

/** A row with several days or dates as one row each; any other row as itself. */
export function expandPending(row: EditorRow): EditorRow[] {
  const pending = row.pending_split;
  if (!pending) return [row];
  const base = { ...row };
  delete base.pending_split;
  if (pending.days) return splitDays(base, pending.days);
  if (pending.dates) return splitDates(base, pending.dates);
  return [base];
}

export function expandAllPending(rows: EditorRow[]): EditorRow[] {
  return rows.some((r) => r.pending_split) ? rows.flatMap(expandPending) : rows;
}

/** The rows a save writes: pending splits expanded, incomplete rows left out. */
export function savableRows(rows: EditorRow[]): EditorRow[] {
  return expandAllPending(rows).filter((r) => rowProblems(r).length === 0);
}

/** One row per day ("Mon-Fri"): the first keeps the row's identity. */
export function splitDays(row: EditorRow, days: Day[]): EditorRow[] {
  if (days.length === 0) return [row];
  return days.map((day, i) => {
    const edited = editRow(row, { day_of_week: day, event_kind: "weekly" });
    return i === 0 ? edited : { ...edited, id: newId() };
  });
}

/** One row per date ("10/2; 10/9"). */
export function splitDates(row: EditorRow, dates: string[]): EditorRow[] {
  if (dates.length === 0) return [row];
  return dates.map((date, i) => {
    const edited = editRow(row, { date, event_kind: "specific_date" });
    return i === 0 ? edited : { ...edited, id: newId() };
  });
}

export function duplicateRow(row: EditorRow): EditorRow {
  const copy: EditorRow = { ...row, id: newId(), origin: editedOrigin(row.origin) };
  delete copy.gemini_id;
  return copy;
}

/** What stops a row from being saved (the label file requires these). */
export function rowProblems(row: EditorRow): string[] {
  const problems: string[] = [];
  if (!row.church_slug) problems.push("church");
  if (row.event_kind === "weekly" && !row.day_of_week) problems.push("day");
  if (row.event_kind === "specific_date" && !row.date) problems.push("date");
  if (minutesOf(row.start_time) === null) problems.push("start time");
  if (row.season && seasonProblems(row.season).length) problems.push("season");
  return problems;
}

export function toLabelEvent(row: EditorRow): LabelEvent {
  return {
    church_slug: row.church_slug,
    event_type: row.event_type,
    event_kind: row.event_kind,
    day_of_week: row.event_kind === "weekly" ? row.day_of_week : null,
    date: row.event_kind === "specific_date" ? row.date : null,
    start_time: row.start_time,
    end_time: row.end_time || null,
    cancelled: row.cancelled,
    weeks_of_month: row.event_kind === "weekly" ? row.weeks_of_month : [],
    season: row.event_kind === "weekly" ? row.season : null,
    page_number: row.page_number,
    note: row.note?.trim() ? row.note.trim() : null,
    origin: row.origin,
  };
}

export function fromLabelEvent(event: LabelEvent): EditorRow {
  return { ...event, id: newId() };
}

type Slot = Pick<
  EditorRow,
  "church_slug" | "event_type" | "event_kind" | "day_of_week" | "date" | "start_time" | "cancelled"
>;

/** What makes two rows the same event (for duplicates, and for matching Gemini rows). */
export function slotKey(row: Slot & Partial<Pick<EditorRow, "weeks_of_month" | "season">>): string {
  return JSON.stringify([
    row.church_slug,
    row.event_type,
    row.event_kind,
    row.event_kind === "weekly" ? row.day_of_week : row.date,
    row.start_time,
    row.cancelled,
    row.weeks_of_month ?? [],
    row.season ?? null,
  ]);
}

type Matchable = Pick<GeminiRow, "church_slug" | "day_of_week" | "date" | "cancelled"> & {
  event_type: EventType | null;
  event_kind: EventKind | null;
  start_time: string | null;
};

function matchKey(r: Matchable): string {
  return JSON.stringify([
    r.church_slug,
    r.event_type,
    r.event_kind,
    r.event_kind === "weekly" ? r.day_of_week : r.date,
    r.start_time,
    r.cancelled,
  ]);
}

/**
 * Gemini rows already accounted for: accepted in this session, or matching a
 * ground-truth row on church, type, day or date, time and cancellation.
 */
export function handledGeminiIds(rows: EditorRow[], gemini: GeminiRow[]): Set<string> {
  const accepted = new Set(rows.map((r) => r.gemini_id).filter((id): id is string => !!id));
  const truth = new Set(rows.map(matchKey));
  return new Set(
    gemini.filter((g) => accepted.has(g.id) || truth.has(matchKey(g))).map((g) => g.id),
  );
}

export interface Warning {
  rowId?: string;
  geminiId?: string;
  message: string;
}

/** How far a dated event can sit from the bulletin's date before it looks misread. */
export const DATE_WINDOW_DAYS = 35;

/** Non-blocking checks on the ground truth. */
export function labelWarnings(
  rows: EditorRow[],
  {
    gemini,
    dismissed,
    bulletinDate,
    churches,
  }: { gemini: GeminiRow[]; dismissed: Set<string>; bulletinDate: string | null; churches: string[] },
): Warning[] {
  const warnings: Warning[] = [];
  const seen = new Map<string, number>();
  rows.forEach((row, i) => {
    const n = i + 1;
    const start = minutesOf(row.start_time);
    const end = minutesOf(row.end_time);
    if (start !== null && end !== null && end <= start) {
      warnings.push({
        rowId: row.id,
        message: `Row ${n}: ends (${formatTime(row.end_time)}) before it starts (${formatTime(row.start_time)})`,
      });
    }
    if (row.event_kind === "specific_date" && row.date && bulletinDate) {
      const gap = daysBetween(row.date, bulletinDate);
      if (Math.abs(gap) > DATE_WINDOW_DAYS) {
        warnings.push({
          rowId: row.id,
          message: `Row ${n}: ${formatDate(row.date)} is ${Math.abs(gap)} days ${gap < 0 ? "before" : "after"} the bulletin date`,
        });
      }
    }
    if (row.church_slug && !churches.includes(row.church_slug)) {
      warnings.push({ rowId: row.id, message: `Row ${n}: church ${row.church_slug} is not in this parish` });
    }
    if (rowProblems(row).length === 0) {
      const key = slotKey(row);
      const first = seen.get(key);
      if (first !== undefined) {
        warnings.push({ rowId: row.id, message: `Row ${n} duplicates row ${first}` });
      } else {
        seen.set(key, n);
      }
    }
  });
  const handled = handledGeminiIds(rows, gemini);
  const pending = gemini.filter((g) => !handled.has(g.id) && !dismissed.has(g.id));
  if (pending.length) {
    warnings.push({
      geminiId: pending[0].id,
      message: `${pending.length} Gemini row${pending.length === 1 ? "" : "s"} not yet accepted or dismissed`,
    });
  }
  return warnings;
}

const DAY_ORDER: Record<string, number> = {
  Sunday: 0,
  Monday: 1,
  Tuesday: 2,
  Wednesday: 3,
  Thursday: 4,
  Friday: 5,
  Saturday: 6,
};
const TYPE_ORDER: Record<EventType, number> = { mass: 0, confession: 1, adoration: 2 };

/** Church (parish order), type, weekly before dated, then day or date, then time. */
export function sortRows(rows: EditorRow[], churches: string[]): EditorRow[] {
  const churchIndex = (slug: string) => {
    const i = churches.indexOf(slug);
    return i === -1 ? churches.length : i;
  };
  return [...rows].sort(
    (a, b) =>
      churchIndex(a.church_slug) - churchIndex(b.church_slug) ||
      TYPE_ORDER[a.event_type] - TYPE_ORDER[b.event_type] ||
      Number(a.event_kind === "specific_date") - Number(b.event_kind === "specific_date") ||
      (a.event_kind === "weekly"
        ? (DAY_ORDER[a.day_of_week ?? ""] ?? 9) - (DAY_ORDER[b.day_of_week ?? ""] ?? 9)
        : (a.date ?? "").localeCompare(b.date ?? "")) ||
      (minutesOf(a.start_time) ?? 9999) - (minutesOf(b.start_time) ?? 9999),
  );
}
