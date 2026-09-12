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
 * Monday-first labels used by the filter UI. Indexes line up with
 * `FilterState.daysOfWeek`, where 0 = Monday and 6 = Sunday.
 */
export const FILTER_DAY_LABELS: ReadonlyArray<{ full: string; abbr: string }> = [
  { full: "Monday", abbr: "Mon" },
  { full: "Tuesday", abbr: "Tue" },
  { full: "Wednesday", abbr: "Wed" },
  { full: "Thursday", abbr: "Thu" },
  { full: "Friday", abbr: "Fri" },
  { full: "Saturday", abbr: "Sat" },
  { full: "Sunday", abbr: "Sun" },
];

/**
 * Display order for the weekday pickers: Sunday first, as both the map's
 * filter panel and the landing page's refine section show it. Values are
 * indices into FILTER_DAY_LABELS — keeping that array Monday-first avoids
 * touching URL state or the filter wire format.
 */
export const FILTER_DAY_DISPLAY_ORDER: readonly number[] = [6, 0, 1, 2, 3, 4, 5];
