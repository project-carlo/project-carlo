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
 * A season is bounded to the day, because bulletins bound it that way: a summer
 * schedule that runs "June 4 through September 10" is not the whole of June. A
 * boundary with no day is not a missing value but a coarser statement of the
 * same thing — "January to April" runs the whole of both months, and is
 * described back in those months, never as a January 1st and an April 30th the
 * parish never printed.
 *
 * The rules here mirror `src/pdf_extract/schedule_pattern.py`, which normalises
 * the same qualifiers on the way into the snapshot. Pure functions only, so the
 * SPA and the prerenderer read a schedule the same way.
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
  /** Inclusive range of the year the slot runs in; null months mean all year. */
  season_start_month: number | null;
  /** Day of the start month; null puts the boundary at the 1st. */
  season_start_day: number | null;
  season_end_month: number | null;
  /** Day of the end month; null puts the boundary at the month's last day. */
  season_end_day: number | null;
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

// February gets 29: a season boundary is a calendar position that comes round
// every year, not a date in one of them.
const DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

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
 * Parse a stored season day against the month it belongs to.
 *
 * A day is only ever a refinement of that month, so dropping one that cannot
 * fall in it leaves the boundary at the whole month — coarser, still true.
 */
export function parseSeasonDay(value: unknown, month: number | null): number | null {
  if (month === null || value === null || value === undefined || value === "") {
    return null;
  }
  const day = typeof value === "number" ? value : Number(value);
  if (!Number.isInteger(day) || day < 1 || day > DAYS_IN_MONTH[month - 1]) {
    return null;
  }
  return day;
}

/**
 * Whether a (month, day) position falls inside an inclusive season range.
 *
 * A range that wraps the new year (October through June) is the common case for
 * a schedule tied to the school year, so a start later in the calendar than the
 * end reads as "start to New Year's Eve, then New Year's Day to end". A
 * boundary with no day covers its whole month, which is what "January to April"
 * means when the bulletin named no dates.
 */
export function dateInSeason(date: Date, pattern: SchedulePattern): boolean {
  const { season_start_month: startMonth, season_end_month: endMonth } = pattern;
  if (startMonth === null || endMonth === null) return true;
  const start = [startMonth, pattern.season_start_day ?? 1] as const;
  const end = [
    endMonth,
    pattern.season_end_day ?? DAYS_IN_MONTH[endMonth - 1],
  ] as const;
  const position = [date.getMonth() + 1, date.getDate()] as const;

  const onOrAfter = (a: readonly [number, number], b: readonly [number, number]) =>
    a[0] !== b[0] ? a[0] > b[0] : a[1] >= b[1];

  if (onOrAfter(end, start)) {
    return onOrAfter(position, start) && onOrAfter(end, position);
  }
  return onOrAfter(position, start) || onOrAfter(end, position);
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
    pattern.season_start_day ?? "",
    pattern.season_end_month ?? "",
    pattern.season_end_day ?? "",
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

/** "October", or "June 4" once the bulletin has dated the boundary. */
function describeBoundary(month: number, day: number | null): string {
  const name = MONTH_NAMES[month - 1];
  return day === null ? name : `${name} ${day}`;
}

/**
 * When the slot runs, at the grain the bulletin stated it.
 *
 * A boundary carries a day only where the parish printed one, so a range given
 * in whole months is described in whole months — "January through April", not
 * the January 1st and April 30th filtering reads underneath it.
 */
export function describeSeason(pattern: SchedulePattern): string | null {
  const { season_start_month: start, season_end_month: end } = pattern;
  if (start === null || end === null) return null;
  return (
    `${describeBoundary(start, pattern.season_start_day)} through ` +
    describeBoundary(end, pattern.season_end_day)
  );
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
    describeSeason(pattern),
  ].filter((part): part is string => part !== null);
  return parts.length > 0 ? parts.join(", ") : null;
}
