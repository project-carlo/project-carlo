import { DAY_ORDER, jsDayFor } from "../constants/days";
import type { Season } from "../types";

/**
 * Shared schedule logic for both the SPA and the prerenderer so that a static
 * church page and the live React page show the same set of events in the same
 * order.  Pure functions only; no DOM or React dependencies.
 */

const EVENING_START_MINUTES = 16 * 60;
// compareSchedule ranks Sunday 0, the Saturday vigil 1, Mon-Sat weekly events
// 2-7, then these.
const UNKNOWN_DAY_RANK = 8;
const SPECIFIC_DATE_RANK = 9;
// How far ahead a weekly slot's next kept date is looked for: over a year, so
// a seasonal slot out of season, or a "fifth" week that skips months, is
// still found.
const WEEKLY_HORIZON_DAYS = 400;
const NO_DATES: ReadonlySet<string> = new Set();

export interface OccurrenceInput {
  cancelled: boolean;
  event_kind: string;
  day_of_week: string | null;
  start_time: number;
  date: string | null;
  /** Weekly only; missing or empty for every week (see `WeekOfMonth`). */
  weeks_of_month?: readonly string[];
  /** Weekly only; all missing or null for all year (see `Season`). */
  season_start_month?: number | null;
  season_start_day?: number | null;
  season_end_month?: number | null;
  season_end_day?: number | null;
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

/** A weekly row's season, or null when it runs all year. */
export function seasonOf(event: OccurrenceInput): Season | null {
  const { season_start_month: startMonth, season_end_month: endMonth } = event;
  if (startMonth == null || endMonth == null) return null;
  return {
    start_month: startMonth,
    start_day: event.season_start_day ?? null,
    end_month: endMonth,
    end_day: event.season_end_day ?? null,
  };
}

/** Local YYYY-MM-DD of a date, as cancellations name the dates they cancel. */
function isoDateLocal(d: Date): string {
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${month}-${day}`;
}

/** The week of the month each ordinal names: days 1–7 are the first. */
const WEEK_INDEX: Record<string, number | undefined> = {
  first: 1,
  second: 2,
  third: 3,
  fourth: 4,
  fifth: 5,
};

/** Whether `d` falls in one of the weeks of the month listed (none: every week). */
function inWeeksOfMonth(d: Date, weeks: readonly string[]): boolean {
  if (weeks.length === 0) return true;
  const day = d.getDate();
  const daysInMonth = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
  return weeks.some((week) =>
    week === "last" ? day + 7 > daysInMonth : WEEK_INDEX[week] === Math.ceil(day / 7),
  );
}

/** Whether `d` falls in `season` (null: all year). */
function inSeason(d: Date, season: Season | null): boolean {
  if (!season) return true;
  // Month * 100 + day orders a year's days; 31 stands for any month's last day.
  const at = (d.getMonth() + 1) * 100 + d.getDate();
  const start = season.start_month * 100 + (season.start_day ?? 1);
  const end = season.end_month * 100 + (season.end_day ?? 31);
  return start <= end ? start <= at && at <= end : at >= start || at <= end;
}

function nextForWeekly(
  event: OccurrenceInput,
  dayOfWeek: string,
  today: Date,
  cancelledDates: ReadonlySet<string>,
): Date | null {
  const jsDay = jsDayFor(dayOfWeek);
  if (jsDay < 0) return null;
  const weeks = event.weeks_of_month ?? [];
  const season = seasonOf(event);
  const hours = Math.floor(event.start_time / 60);
  const minutes = event.start_time % 60;
  for (
    let daysAhead = (jsDay - today.getDay() + 7) % 7;
    daysAhead <= WEEKLY_HORIZON_DAYS;
    daysAhead += 7
  ) {
    const target = new Date(today);
    target.setDate(target.getDate() + daysAhead);
    if (
      inWeeksOfMonth(target, weeks) &&
      inSeason(target, season) &&
      !cancelledDates.has(isoDateLocal(target))
    ) {
      target.setHours(hours, minutes, 0, 0);
      return target;
    }
  }
  return null;
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
 *
 * A weekly event occurs on its weekday from today on (today included, even
 * once its time has passed), in the weeks of the month and the season it
 * keeps, except on `cancelledDates` (local YYYY-MM-DD dates a cancellation
 * names for it); null when no such day comes within about a year.
 */
export function computeNextOccurrence(
  event: OccurrenceInput,
  today: Date = todayDate(),
  cancelledDates: ReadonlySet<string> = NO_DATES,
): string | null {
  if (event.cancelled) return null;
  let occ: Date | null = null;
  if (event.event_kind === "weekly" && event.day_of_week) {
    occ = nextForWeekly(event, event.day_of_week, today, cancelledDates);
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
