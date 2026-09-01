/**
 * The shape of a recurring slot: which weeks of the month it falls on, and
 * which part of the year it runs.
 *
 * A parish schedule is not always the plain (weekday, time) pair the event
 * table started with. Confessions at Holy Trinity run Tuesdays at 4:30 —
 * October through June. First Friday devotions are a Friday slot that happens
 * once a month. Both used to reach the browser only as free-text notes, so the
 * map offered the confession slot in September and listed the devotions as
 * though they happened every Friday.
 *
 * The rules here mirror `src/pdf_extract/schedule_pattern.py`, which normalises
 * the same two qualifiers on the way into the snapshot. Pure functions only, so
 * the SPA and the prerenderer read a schedule the same way.
 */

export const WEEKS_OF_MONTH = [
  "first",
  "second",
  "third",
  "fourth",
  "fifth",
  "last",
] as const;

export type WeekOfMonth = (typeof WEEKS_OF_MONTH)[number];

export interface SchedulePattern {
  /** Weeks of the month the slot falls on; empty means every week. */
  weeks_of_month: WeekOfMonth[];
  /** Inclusive month range the slot runs in, 1-12; null means all year. */
  season_start_month: number | null;
  season_end_month: number | null;
}

const WEEK_SET = new Set<string>(WEEKS_OF_MONTH);

const MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

/** Parse the stored `weeks_of_month` column ("first,third") into tokens. */
export function parseWeeksOfMonth(value: unknown): WeekOfMonth[] {
  if (Array.isArray(value)) {
    return value.filter((week): week is WeekOfMonth =>
      typeof week === "string" && WEEK_SET.has(week),
    );
  }
  if (typeof value !== "string" || value.trim() === "") return [];
  return value
    .split(",")
    .map((part) => part.trim().toLowerCase())
    .filter((part): part is WeekOfMonth => WEEK_SET.has(part));
}

/** Parse a stored season month, keeping only a usable 1-12 value. */
export function parseSeasonMonth(value: unknown): number | null {
  const month = typeof value === "number" ? value : Number(value);
  if (!Number.isInteger(month) || month < 1 || month > 12) return null;
  return month;
}

/**
 * Whether a month falls inside an inclusive season range.
 *
 * A range that wraps the new year (October through June) is the common case for
 * a schedule tied to the school year, so `start > end` reads as "start month to
 * December, then January to end month".
 */
export function monthInSeason(
  month: number,
  start: number | null,
  end: number | null,
): boolean {
  if (start === null || end === null) return true;
  if (start <= end) return month >= start && month <= end;
  return month >= start || month <= end;
}

/** Whether `date` falls in the part of the year this slot runs. */
export function dateInSeason(date: Date, pattern: SchedulePattern): boolean {
  return monthInSeason(
    date.getMonth() + 1,
    pattern.season_start_month,
    pattern.season_end_month,
  );
}

/** Which occurrence of its weekday within the month `date` is, 1-5. */
function ordinalOfMonth(date: Date): number {
  return Math.floor((date.getDate() - 1) / 7) + 1;
}

/** Whether `date` is the last occurrence of its weekday in the month. */
function isLastOfMonth(date: Date): boolean {
  const next = new Date(date);
  next.setDate(date.getDate() + 7);
  return next.getMonth() !== date.getMonth();
}

/**
 * Whether `date` is one of the weeks of the month this slot falls on.
 *
 * "last" stays distinct from "fourth": a month with five Fridays has a fourth
 * Friday and a different last one, and a bulletin that says "last Friday" means
 * the later date.
 */
export function dateMatchesWeeks(date: Date, weeks: WeekOfMonth[]): boolean {
  if (weeks.length === 0) return true;
  const ordinal = WEEKS_OF_MONTH[ordinalOfMonth(date) - 1];
  if (ordinal !== undefined && ordinal !== "last" && weeks.includes(ordinal)) {
    return true;
  }
  return weeks.includes("last") && isLastOfMonth(date);
}

/** Whether this slot actually happens on `date`, weeks and season both. */
export function dateMatchesPattern(
  date: Date,
  pattern: SchedulePattern,
): boolean {
  return (
    dateMatchesWeeks(date, pattern.weeks_of_month) && dateInSeason(date, pattern)
  );
}

/** True when the slot is a plain every-week, all-year one. */
export function isPlainWeekly(pattern: SchedulePattern): boolean {
  return (
    pattern.weeks_of_month.length === 0 && pattern.season_start_month === null
  );
}

/** Stable identity for a pattern, for grouping slots that share a schedule. */
export function patternKey(pattern: SchedulePattern): string {
  if (isPlainWeekly(pattern)) return "";
  return [
    pattern.weeks_of_month.join("+"),
    pattern.season_start_month ?? "",
    pattern.season_end_month ?? "",
  ].join(":");
}

function titleCaseWeek(week: WeekOfMonth): string {
  return week.charAt(0).toUpperCase() + week.slice(1);
}

function joinWithAnd(parts: string[]): string {
  if (parts.length <= 1) return parts[0] ?? "";
  if (parts.length === 2) return `${parts[0]} and ${parts[1]}`;
  return `${parts.slice(0, -1).join(", ")}, and ${parts[parts.length - 1]}`;
}

/**
 * "First Friday of the month", "First and third Fridays of the month".
 *
 * Needs the weekday because the ordinals count occurrences of that weekday, not
 * calendar weeks: the first Friday of a month can fall in its second week.
 */
export function describeWeeksOfMonth(
  weeks: WeekOfMonth[],
  dayOfWeek: string | null,
): string | null {
  if (weeks.length === 0) return null;
  const day = dayOfWeek?.trim();
  if (!day) return `${joinWithAnd(weeks.map(titleCaseWeek))} week of the month`;
  const dayLabel = day.charAt(0).toUpperCase() + day.slice(1).toLowerCase();
  const ordinals = weeks.map((week, index) =>
    index === 0 ? titleCaseWeek(week) : week,
  );
  const plural = weeks.length > 1 ? "s" : "";
  return `${joinWithAnd(ordinals)} ${dayLabel}${plural} of the month`;
}

/** "October through June". */
export function describeSeason(
  start: number | null,
  end: number | null,
): string | null {
  if (start === null || end === null) return null;
  return `${MONTH_NAMES[start - 1]} through ${MONTH_NAMES[end - 1]}`;
}

/**
 * The whole qualifier as one phrase, or null for a plain weekly slot.
 *
 * This is what the frontend shows in place of the free-text note these
 * qualifiers used to live in, so a reader can tell why a slot they can see on
 * the church page is not on the map today.
 */
export function describeSchedulePattern(
  pattern: SchedulePattern,
  dayOfWeek: string | null,
): string | null {
  const parts = [
    describeWeeksOfMonth(pattern.weeks_of_month, dayOfWeek),
    describeSeason(pattern.season_start_month, pattern.season_end_month),
  ].filter((part): part is string => part !== null);
  return parts.length > 0 ? parts.join(", ") : null;
}
