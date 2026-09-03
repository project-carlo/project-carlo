import { DAY_ORDER, type WeekdayKey } from "../constants/days";
import {
  dateMatchesPattern,
  type SchedulePattern,
  type WeekOfMonth,
} from "./schedulePattern";

/**
 * Shared schedule logic for both the SPA and the prerenderer so that a static
 * church page and the live React page show the same set of events in the same
 * order.  Pure functions only; no DOM, React, or sql.js dependencies.
 */

const MONDAY_INDEX: Record<string, number> = {
  monday: 0,
  tuesday: 1,
  wednesday: 2,
  thursday: 3,
  friday: 4,
  saturday: 5,
  sunday: 6,
};

const EVENING_START_MINUTES = 16 * 60;

/**
 * How far ahead a weekly slot's next occurrence is searched for.
 *
 * Seven years, because the qualifiers multiply: a last-Thursday Holy Hour that
 * only runs June 4 through June 20 offers three candidate dates a year, and one
 * of them is the last Thursday of its month far less often than that. A slot
 * that resolves to nothing is dropped from the church page, so the loop is
 * cheap insurance — it exits on the first match, which for all but a handful of
 * slots is the coming week.
 */
const MAX_LOOKAHEAD_WEEKS = 366;

export interface OccurrenceInput {
  cancelled: boolean;
  event_kind: string;
  day_of_week: string | null;
  start_time: number;
  date: string | null;
  /** Weeks of the month the slot falls on; absent or empty means every week. */
  weeks_of_month?: WeekOfMonth[];
  /** Inclusive range of the year the slot runs in; absent means all year. */
  season_start_month?: number | null;
  season_start_day?: number | null;
  season_end_month?: number | null;
  season_end_day?: number | null;
}

/** The recurrence qualifiers of an event, defaulted to a plain weekly slot. */
export function patternOf(event: Partial<SchedulePattern>): SchedulePattern {
  return {
    weeks_of_month: event.weeks_of_month ?? [],
    season_start_month: event.season_start_month ?? null,
    season_start_day: event.season_start_day ?? null,
    season_end_month: event.season_end_month ?? null,
    season_end_day: event.season_end_day ?? null,
  };
}

export interface CompareInput {
  kind: "weekly" | "specific_date";
  day_of_week: string | null;
  date: string | null;
  start_time: number;
}

function todayDate(): Date {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate());
}

function parseEventDate(value: string): Date | null {
  // Prefer explicit YYYY-MM-DD parsing to avoid timezone/date shifts.
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
  pattern: SchedulePattern,
): Date | null {
  const dayIdx = MONDAY_INDEX[dayOfWeek.toLowerCase()];
  if (dayIdx === undefined) return null;
  const hours = Math.floor(startMinutes / 60);
  const minutes = startMinutes % 60;
  const jsDay = (dayIdx + 1) % 7; // Python: Monday=0; JS: Sunday=0
  const daysAhead = (jsDay - today.getDay() + 7) % 7;
  const candidate = new Date(today);
  candidate.setDate(candidate.getDate() + daysAhead);
  // A slot qualified by week of the month or by season skips most of the
  // weekdays it nominally falls on, so walk forward a week at a time until one
  // of them is an occurrence the slot actually keeps.
  for (let week = 0; week < MAX_LOOKAHEAD_WEEKS; week += 1) {
    if (dateMatchesPattern(candidate, pattern)) {
      const target = new Date(candidate);
      target.setHours(hours, minutes, 0, 0);
      return target;
    }
    candidate.setDate(candidate.getDate() + 7);
  }
  return null;
}

function nextForSpecific(
  eventDate: string,
  startMinutes: number,
  today: Date,
): Date | null {
  const parsed = parseEventDate(eventDate);
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
 * A weekly slot resolves to the next date it genuinely runs, which for a
 * seasonal or monthly one can be months out. That is deliberate: the church
 * page lists a slot that is out of season alongside the note saying when it
 * resumes, rather than dropping it as though the parish had stopped offering
 * it.
 */
export function computeNextOccurrence(
  event: OccurrenceInput,
  today: Date = todayDate(),
): string | null {
  if (event.cancelled) return null;
  let occ: Date | null = null;
  if (event.event_kind === "weekly" && event.day_of_week) {
    occ = nextForWeekly(
      event.day_of_week, event.start_time, today, patternOf(event),
    );
  } else if (event.event_kind === "specific_date" && event.date) {
    occ = nextForSpecific(event.date, event.start_time, today);
  }
  return occ ? occ.toISOString() : null;
}

/**
 * Liturgical-week comparator used for map popups and the church page.
 *
 * Order: weekly Sunday, Saturday evening (>= 4 pm, vigil), Mon-Sat weekly by
 * weekday, then specific-date events by date.  Ties break on start_time.
 */
export function compareSchedule(a: CompareInput, b: CompareInput): number {
  const aIsSpecific = a.kind === "specific_date" && a.date;
  const bIsSpecific = b.kind === "specific_date" && b.date;

  if (aIsSpecific && bIsSpecific) {
    const dateCompare = (a.date ?? "").localeCompare(b.date ?? "");
    if (dateCompare !== 0) return dateCompare;
    return a.start_time - b.start_time;
  }
  if (aIsSpecific && !bIsSpecific) return 1;
  if (!aIsSpecific && bIsSpecific) return -1;

  const dayA = weekdayKeyFor(a);
  const dayB = weekdayKeyFor(b);
  if (!dayA) return 1;
  if (!dayB) return -1;

  const dayIdxA = DAY_ORDER.indexOf(dayA);
  const dayIdxB = DAY_ORDER.indexOf(dayB);
  const isSatEveA =
    dayA === "saturday" && a.start_time >= EVENING_START_MINUTES;
  const isSatEveB =
    dayB === "saturday" && b.start_time >= EVENING_START_MINUTES;

  return scheduleSortKey(dayA, dayIdxA, isSatEveA, a.start_time)
    - scheduleSortKey(dayB, dayIdxB, isSatEveB, b.start_time);
}

function weekdayKeyFor(e: CompareInput): WeekdayKey | null {
  if (e.kind === "weekly" && e.day_of_week) {
    return e.day_of_week.toLowerCase() as WeekdayKey;
  }
  if (e.date) {
    const d = new Date(e.date + "T12:00:00");
    return DAY_ORDER[d.getDay()];
  }
  return null;
}

function scheduleSortKey(
  day: WeekdayKey,
  dayIdx: number,
  isSatEve: boolean,
  startTime: number,
): number {
  if (day === "sunday") return startTime;
  if (isSatEve) return 1000 + startTime;
  return 2000 + dayIdx * 1000 + startTime;
}
