/** Sunday-first week order (display / map event sorting). */
export const DAY_ORDER = [
  "sunday",
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
  "saturday",
] as const;

export type WeekdayKey = (typeof DAY_ORDER)[number];

/**
 * Index of a weekday name in `DAY_ORDER`, or -1 if it is not a weekday name.
 *
 * DAY_ORDER is Sunday-first, so this is also the value `Date.prototype.getDay`
 * returns for that day.
 */
export function jsDayFor(dayOfWeek: string): number {
  return (DAY_ORDER as readonly string[]).indexOf(dayOfWeek.trim().toLowerCase());
}

/**
 * Monday-first labels used by the filter UI. Indexes line up with
 * `FilterState.daysOfWeek`, where 0 = Monday and 6 = Sunday.
 */
export const FILTER_DAY_LABELS: ReadonlyArray<{ full: string; abbr: string }> =
  // Sunday moves from the front of DAY_ORDER to the back.
  [...DAY_ORDER.slice(1), DAY_ORDER[0]].map((day) => {
    const full = day.charAt(0).toUpperCase() + day.slice(1);
    return { full, abbr: full.slice(0, 3) };
  });

/**
 * The `FilterState.daysOfWeek` index (0 = Monday) for a `Date`, or for a
 * `jsDayFor` result. Returns -1 for an input that is not a weekday.
 */
export function filterDayFromJsDay(jsDay: number): number {
  if (jsDay < 0) return -1;
  return (jsDay + 6) % 7;
}
