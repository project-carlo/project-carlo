import type { EventSummary } from "../types";
import {
  formatMinutesMissal,
  formatQualifiedTime,
  formatSlotQualifier,
  titleCase,
} from "../utils";

/**
 * Rolls a church's upcoming events up into one row per day, so a church with
 * three Sunday Masses reads as a single "Sunday — 8 a.m. · 10:30 a.m. · 5
 * p.m." line in the map popup instead of filling the preview with three
 * near-identical rows.
 *
 * Pure formatting logic; the input order is preserved (events arrive sorted by
 * `compareSchedule`) and each row's times are sorted earliest-first.
 */
export interface ScheduleRollupRow {
  /** Stable key for React lists. */
  key: string;
  /** Day heading, e.g. "Sunday" or "Tue, Mar 17". */
  label: string;
  /**
   * Distinct start times for the day, earliest first, each formatted with its
   * own meridiem so no time in the popup can be read as the wrong half of the
   * day, and followed by its slot's qualifier when it isn't every week of the
   * year: "10 a.m. (1st & 3rd)".
   */
  times: string[];
}

function rollupKey(event: EventSummary): string {
  if (event.kind === "weekly" && event.day_of_week) {
    return `weekly:${event.day_of_week.toLowerCase()}`;
  }
  if (event.date) return `date:${event.date}`;
  // Nothing to group on — keep the event on a row of its own.
  return `event:${event.id}`;
}

function rollupLabel(event: EventSummary): string {
  if (event.kind === "weekly" && event.day_of_week) {
    return titleCase(event.day_of_week);
  }
  if (event.date) return formatCompactDate(event.date);
  return "";
}

// `Date.prototype.toLocaleDateString` builds a formatter on every call, which
// showed up as the single hottest frame while filtering the map. Building it
// once — and remembering the handful of distinct dates a snapshot contains —
// makes repeat formatting free.
const COMPACT_DATE_FORMATTER = new Intl.DateTimeFormat("en-US", {
  weekday: "short",
  month: "short",
  day: "numeric",
});
const compactDateCache = new Map<string, string>();

/**
 * Abbreviated date for the popup's narrow day column — "Wed, Sep 17" rather
 * than the church page's fuller "Wednesday, September 17th", which would wrap
 * onto two lines and squeeze the times beside it.
 */
function formatCompactDate(dateStr: string): string {
  const cached = compactDateCache.get(dateStr);
  if (cached !== undefined) return cached;
  const parsed = new Date(dateStr + "T12:00:00");
  const formatted = Number.isNaN(parsed.getTime())
    ? dateStr
    : COMPACT_DATE_FORMATTER.format(parsed);
  compactDateCache.set(dateStr, formatted);
  return formatted;
}

/** A start time and the qualifier of the slot it starts, as a row lists them. */
export interface QualifiedTime {
  start_time: number;
  qualifier: string | null;
}

/** Add an event's time to a row's, unless an equal one is already there. */
export function addQualifiedTime(times: QualifiedTime[], event: EventSummary): void {
  const qualifier = event.kind === "weekly" ? formatSlotQualifier(event) : null;
  if (
    !times.some(
      (t) => t.start_time === event.start_time && t.qualifier === qualifier,
    )
  ) {
    times.push({ start_time: event.start_time, qualifier });
  }
}

/** A row's times, earliest first, formatted for display. */
export function formatQualifiedTimes(times: QualifiedTime[]): string[] {
  return [...times]
    .sort((a, b) => {
      if (a.start_time !== b.start_time) return a.start_time - b.start_time;
      // An every-week time ("") before qualified ones at the same hour.
      const qa = a.qualifier ?? "";
      const qb = b.qualifier ?? "";
      return qa < qb ? -1 : qa > qb ? 1 : 0;
    })
    .map((t) => formatQualifiedTime(formatMinutesMissal(t.start_time), t.qualifier));
}

export function rollUpEventsByDay(
  events: EventSummary[],
): ScheduleRollupRow[] {
  const rows = new Map<string, { label: string; times: QualifiedTime[] }>();

  for (const event of events) {
    const key = rollupKey(event);
    let row = rows.get(key);
    if (!row) {
      row = { label: rollupLabel(event), times: [] };
      rows.set(key, row);
    }
    // Two events can share a slot (e.g. a Mass and a Confession at 4 p.m.);
    // the preview only shows the time, so list it once.
    addQualifiedTime(row.times, event);
  }

  return [...rows.entries()].map(([key, row]) => ({
    key,
    label: row.label,
    times: formatQualifiedTimes(row.times),
  }));
}
