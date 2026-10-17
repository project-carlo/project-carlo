import type { Season, WeekOfMonth } from "../types";

/**
 * The shape of a recurring slot: which weeks of the month it falls on, and
 * which part of the year it runs.
 *
 * A parish schedule is not always a plain (weekday, time) pair. Confessions at
 * Holy Trinity run Tuesdays at 4:30, October through June. First Friday
 * devotions are a Friday slot that happens once a month.
 *
 * A season is bounded to the day, because bulletins bound it that way: a summer
 * schedule that runs "June 4 through September 10" is not the whole of June. A
 * boundary with no day is not a missing value but a coarser statement of the
 * same thing: "January to April" runs the whole of both months, and is
 * described back in those months, never as a January 1st and an April 30th the
 * parish never printed.
 *
 * The descriptions mirror `describe_schedule_pattern` in
 * `src/pdf_extract/schedule/qualifiers.py`. Pure functions only, so the SPA
 * and the prerenderer read a schedule the same way.
 */

export const WEEKS_OF_MONTH: readonly WeekOfMonth[] = [
  "first",
  "second",
  "third",
  "fourth",
  "fifth",
  "last",
];

/** What a weekly slot keeps beyond its weekday and time. */
export interface SchedulePattern {
  /** Weeks of the month the slot falls on; empty means every week. */
  weeks_of_month: readonly WeekOfMonth[];
  /**
   * The listed weeks are the ones the slot skips: "every Sunday except the
   * last" is `["last"]` excluded, which no list of the weeks that remain can
   * say. Missing means false.
   */
  exclude_weeks?: boolean;
  /** The part of the year it runs; null means all year. */
  season: Season | null;
}

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

/**
 * Whether `date` falls inside an inclusive season range (null: all year).
 *
 * A range that wraps the new year (October through June) is the common case for
 * a schedule tied to the school year, so a start later in the calendar than the
 * end reads as "start to New Year's Eve, then New Year's Day to end". A
 * boundary with no day covers its whole month, which is what "January to April"
 * means when the bulletin named no dates.
 */
export function dateInSeason(date: Date, season: Season | null): boolean {
  if (!season) return true;
  // Month * 100 + day orders a year's days.
  const at = (date.getMonth() + 1) * 100 + date.getDate();
  const start = season.start_month * 100 + (season.start_day ?? 1);
  const end =
    season.end_month * 100 +
    (season.end_day ?? DAYS_IN_MONTH[season.end_month - 1]);
  return start <= end ? start <= at && at <= end : at >= start || at <= end;
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
 * Whether `date` is one of the weeks of the month this slot falls on, or,
 * when `exclude` is set, is not one of the weeks it skips.
 *
 * "last" stays distinct from "fourth": a month with five Fridays has a fourth
 * Friday and a different last one, and a bulletin that says "last Friday" means
 * the later date.
 */
export function dateMatchesWeeks(
  date: Date,
  weeks: readonly WeekOfMonth[],
  exclude = false,
): boolean {
  if (weeks.length === 0) return true;
  const ordinal = WEEKS_OF_MONTH[ordinalOfMonth(date) - 1];
  const listed =
    (ordinal !== undefined && ordinal !== "last" && weeks.includes(ordinal)) ||
    (weeks.includes("last") && isLastOfMonth(date));
  return listed !== exclude;
}

/** Whether this slot actually happens on `date`, weeks and season both. */
export function dateMatchesPattern(
  date: Date,
  pattern: SchedulePattern,
): boolean {
  return (
    dateMatchesWeeks(date, pattern.weeks_of_month, pattern.exclude_weeks) &&
    dateInSeason(date, pattern.season)
  );
}

/** True when the slot is a plain every-week, all-year one. */
export function isPlainWeekly(pattern: SchedulePattern): boolean {
  return pattern.weeks_of_month.length === 0 && pattern.season === null;
}

/** Stable identity for a pattern, for grouping slots that share a schedule. */
export function patternKey(pattern: SchedulePattern): string {
  if (isPlainWeekly(pattern)) return "";
  const { season } = pattern;
  const weeks = WEEKS_OF_MONTH.filter((week) =>
    pattern.weeks_of_month.includes(week),
  ).join("+");
  return [
    pattern.exclude_weeks && weeks ? `except+${weeks}` : weeks,
    season?.start_month ?? "",
    season?.start_day ?? "",
    season?.end_month ?? "",
    season?.end_day ?? "",
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
 * "First Friday of the month", "First and third Fridays of the month"; an
 * exclusion reads "Every Sunday except the last".
 *
 * Needs the weekday because the ordinals count occurrences of that weekday, not
 * calendar weeks: the first Friday of a month can fall in its second week.
 */
export function describeWeeksOfMonth(
  weeks: readonly WeekOfMonth[],
  dayOfWeek: string | null,
  exclude = false,
): string | null {
  if (weeks.length === 0) return null;
  const ordered = WEEKS_OF_MONTH.filter((week) => weeks.includes(week));
  const day = dayOfWeek?.trim();
  if (exclude) {
    const every = day
      ? day.charAt(0).toUpperCase() + day.slice(1).toLowerCase()
      : "week";
    return `Every ${every} except the ${joinWithAnd(ordered)}`;
  }
  if (!day) {
    return `${joinWithAnd(ordered.map(titleCaseWeek))} week of the month`;
  }
  const dayLabel = day.charAt(0).toUpperCase() + day.slice(1).toLowerCase();
  const ordinals = ordered.map((week, index) =>
    index === 0 ? titleCaseWeek(week) : week,
  );
  const plural = ordered.length > 1 ? "s" : "";
  return `${joinWithAnd(ordinals)} ${dayLabel}${plural} of the month`;
}

/** "October", or "June 4" once the bulletin has dated the boundary. */
function describeBoundary(month: number, day: number | null): string {
  const name = MONTH_NAMES[month - 1] ?? String(month);
  return day === null ? name : `${name} ${day}`;
}

/**
 * When the slot runs, at the grain the bulletin stated it.
 *
 * A boundary carries a day only where the parish printed one, so a range given
 * in whole months is described in whole months ("January through April"), not
 * the January 1st and April 30th filtering reads underneath it.
 */
export function describeSeason(season: Season | null): string | null {
  if (!season) return null;
  return (
    `${describeBoundary(season.start_month, season.start_day)} through ` +
    describeBoundary(season.end_month, season.end_day)
  );
}

/**
 * The whole qualifier as one phrase ("First Friday of the month, October
 * through June"), or null for a plain weekly slot.
 *
 * The church page lists a slot whether or not it is running today, so this is
 * what tells a reader why a slot they can see there is not on the map today.
 */
export function describeSchedulePattern(
  pattern: SchedulePattern,
  dayOfWeek: string | null,
): string | null {
  const parts = [
    describeWeeksOfMonth(
      pattern.weeks_of_month,
      dayOfWeek,
      pattern.exclude_weeks,
    ),
    describeSeason(pattern.season),
  ].filter((part): part is string => part !== null);
  return parts.length > 0 ? parts.join(", ") : null;
}
