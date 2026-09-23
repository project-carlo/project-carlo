import { DAY_ORDER, jsDayFor } from "../constants/days";

/**
 * Shared schedule logic for both the SPA and the prerenderer so that a static
 * church page and the live React page show the same set of events in the same
 * order.  Pure functions only; no DOM, React, or sql.js dependencies.
 */

const EVENING_START_MINUTES = 16 * 60;
// compareSchedule ranks Sunday 0, the Saturday vigil 1, Mon-Sat weekly events
// 2-7, then these.
const UNKNOWN_DAY_RANK = 8;
const SPECIFIC_DATE_RANK = 9;

export interface OccurrenceInput {
  cancelled: boolean;
  event_kind: string;
  day_of_week: string | null;
  start_time: number;
  date: string | null;
}

export interface CompareInput {
  /** Event row id; the final tiebreak, so equal slots never depend on input order. */
  id: number;
  kind: "weekly" | "specific_date";
  day_of_week: string | null;
  date: string | null;
  start_time: number;
}

function todayDate(): Date {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate());
}

/**
 * Parse an event date to a local-midnight `Date`, or null if unparseable.
 *
 * YYYY-MM-DD is read field by field: `new Date("2026-06-07")` is parsed as UTC
 * and renders as the day before in any negative-offset timezone.
 */
export function parseIsoDateLocal(value: string): Date | null {
  const isoMatch = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value.trim());
  if (isoMatch) {
    const year = Number.parseInt(isoMatch[1], 10);
    const month = Number.parseInt(isoMatch[2], 10);
    const day = Number.parseInt(isoMatch[3], 10);
    const parsed = new Date(year, month - 1, day);
    return Number.isNaN(parsed.getTime()) ? null : parsed;
  }
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function nextForWeekly(
  dayOfWeek: string,
  startMinutes: number,
  today: Date,
): Date | null {
  const jsDay = jsDayFor(dayOfWeek);
  if (jsDay < 0) return null;
  const hours = Math.floor(startMinutes / 60);
  const minutes = startMinutes % 60;
  const daysAhead = (jsDay - today.getDay() + 7) % 7;
  const target = new Date(today);
  target.setDate(target.getDate() + daysAhead);
  target.setHours(hours, minutes, 0, 0);
  return target;
}

function nextForSpecific(
  eventDate: string,
  startMinutes: number,
  today: Date,
): Date | null {
  const parsed = parseIsoDateLocal(eventDate);
  if (!parsed) return null;
  // Drop events whose calendar day is already past; same-day events still show
  // (date-only comparison, so an earlier start_time today is not filtered out).
  const eventDay = new Date(
    parsed.getFullYear(),
    parsed.getMonth(),
    parsed.getDate(),
  );
  if (eventDay.getTime() < today.getTime()) return null;
  const d = new Date(parsed);
  d.setHours(Math.floor(startMinutes / 60), startMinutes % 60, 0, 0);
  return Number.isNaN(d.getTime()) ? null : d;
}

/**
 * ISO timestamp of the next occurrence of `event`, or null if the event is
 * cancelled, unparseable, or (for specific_date events) already past.
 */
export function computeNextOccurrence(
  event: OccurrenceInput,
  today: Date = todayDate(),
): string | null {
  if (event.cancelled) return null;
  let occ: Date | null = null;
  if (event.event_kind === "weekly" && event.day_of_week) {
    occ = nextForWeekly(event.day_of_week, event.start_time, today);
  } else if (event.event_kind === "specific_date" && event.date) {
    occ = nextForSpecific(event.date, event.start_time, today);
  }
  return occ ? occ.toISOString() : null;
}

/**
 * Liturgical-week comparator used for map popups and the church page.
 *
 * Order: weekly Sunday, Saturday evening (>= 4 pm, vigil), Mon-Sat weekly by
 * weekday, events whose weekday can't be resolved, then specific-date events
 * by date.  Ties break on start_time, then id, so the result never depends on
 * the order events arrive in; neither the SPA's nor the prerenderer's query
 * orders its rows.
 */
export function compareSchedule(a: CompareInput, b: CompareInput): number {
  const rankA = scheduleRank(a);
  const rankB = scheduleRank(b);
  if (rankA !== rankB) return rankA - rankB;
  if (rankA === SPECIFIC_DATE_RANK) {
    const dateCompare = compareCodeUnits(a.date ?? "", b.date ?? "");
    if (dateCompare !== 0) return dateCompare;
  }
  if (a.start_time !== b.start_time) return a.start_time - b.start_time;
  return a.id - b.id;
}

/**
 * The event's place in the week, compared before start_time rather than folded
 * into one number with it, so a late Monday slot still sorts ahead of an early
 * Tuesday one.
 */
function scheduleRank(e: CompareInput): number {
  if (e.kind === "specific_date" && e.date) return SPECIFIC_DATE_RANK;
  const jsDay = weekdayFor(e);
  if (jsDay < 0) return UNKNOWN_DAY_RANK;
  const day = DAY_ORDER[jsDay];
  if (day === "sunday") return 0;
  if (day === "saturday" && e.start_time >= EVENING_START_MINUTES) return 1;
  return jsDay + 1;
}

/**
 * The `jsDayFor` weekday of an event: its day_of_week if that names a weekday,
 * else the weekday of its date, else -1.
 */
function weekdayFor(e: CompareInput): number {
  if (e.kind === "weekly" && e.day_of_week) {
    const jsDay = jsDayFor(e.day_of_week);
    if (jsDay >= 0) return jsDay;
  }
  if (e.date) {
    const parsed = parseIsoDateLocal(e.date);
    if (parsed) return parsed.getDay();
  }
  return -1;
}

// Code-unit order rather than localeCompare: YYYY-MM-DD dates sort the same
// either way, and this can't vary with the browser's or Node's ICU data.
function compareCodeUnits(a: string, b: string): number {
  if (a < b) return -1;
  return a > b ? 1 : 0;
}
