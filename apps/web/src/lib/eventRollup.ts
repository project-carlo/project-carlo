import type { EventSummary } from "../types";
import { formatMinutesMissal, titleCase } from "../utils";
import { patternOf } from "./schedule";
import { describeSchedulePattern, patternKey } from "./schedulePattern";

/**
 * Rolls a church's upcoming events up into one row per day, so a parish with
 * three Sunday Masses reads as a single "Sundays — 8 a.m. · 10:30 a.m. · 5
 * p.m." line in the map popup instead of filling the preview with three
 * near-identical rows.
 *
 * Pure formatting logic; the input order is preserved (events arrive sorted by
 * `compareSchedule`) and each row's times are sorted earliest-first.
 */
export interface ScheduleRollupRow {
  /** Stable key for React lists. */
  key: string;
  /** Day heading, e.g. "Sundays" or "Tue, Mar 17". */
  label: string;
  /**
   * Distinct start times for the day, earliest first, each formatted with its
   * own meridiem so no time in the popup can be read as the wrong half of the
   * day.
   */
  times: string[];
  /**
   * When the slot does not simply happen every week, the qualifier that says
   * so — "First Friday of the month". Without it the day heading alone would
   * promise a monthly devotion every week.
   */
  note: string | null;
}

function rollupKey(event: EventSummary): string {
  if (event.kind === "weekly" && event.day_of_week) {
    // Slots on the same weekday still get their own rows when they keep
    // different schedules, so a first-Friday devotion is never folded into the
    // times of a Mass that runs every Friday.
    return `weekly:${event.day_of_week.toLowerCase()}:${patternKey(patternOf(event))}`;
  }
  if (event.date) return `date:${event.date}`;
  // Nothing to group on — keep the event on a row of its own.
  return `event:${event.id}`;
}

function rollupLabel(event: EventSummary): string {
  if (event.kind === "weekly" && event.day_of_week) {
    return titleCase(event.day_of_week) + "s";
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

export function rollUpEventsByDay(
  events: EventSummary[],
): ScheduleRollupRow[] {
  const rows = new Map<
    string,
    { label: string; startTimes: number[]; note: string | null }
  >();

  for (const event of events) {
    const key = rollupKey(event);
    let row = rows.get(key);
    if (!row) {
      row = {
        label: rollupLabel(event),
        startTimes: [],
        note:
          event.kind === "weekly"
            ? describeSchedulePattern(patternOf(event), event.day_of_week)
            : null,
      };
      rows.set(key, row);
    }
    // Two events can share a slot (e.g. a Mass and a Confession at 4 p.m.);
    // the preview only shows the time, so list it once.
    if (!row.startTimes.includes(event.start_time)) {
      row.startTimes.push(event.start_time);
    }
  }

  return [...rows.entries()].map(([key, row]) => ({
    key,
    label: row.label,
    times: [...row.startTimes].sort((a, b) => a - b).map(formatMinutesMissal),
    note: row.note,
  }));
}
