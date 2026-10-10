import { DAY_ORDER, jsDayFor } from "../constants/days";
import type { EventSummary } from "../types";
import { formatMinutesMissal, titleCase } from "../utils";
import type { ScheduleRollupRow } from "./eventRollup";
import {
  describeSchedulePattern,
  patternKey,
  type SchedulePattern,
} from "./schedulePattern";

/**
 * A compact weekly schedule for listing many churches on one page (a city
 * page): one row per day, with runs of days that share the same times folded
 * into one row ("Mon – Fri  8 a.m."). A slot that isn't every week of the
 * year gets a row of its own with its qualifier as the row's note, as in the
 * map popup. Pure formatting logic.
 */

/** "Mon" for "monday". */
function dayAbbr(day: string): string {
  return titleCase(day).slice(0, 3);
}

function runLabel(days: string[]): string {
  if (days.length === 1) return titleCase(days[0]);
  const first = dayAbbr(days[0]);
  const last = dayAbbr(days[days.length - 1]);
  return days.length === 2 ? `${first} & ${last}` : `${first} – ${last}`;
}

interface PatternDays {
  pattern: SchedulePattern;
  timesByDay: Map<string, number[]>;
}

interface Run {
  key: string;
  days: string[];
  times: number[];
  note: string | null;
  /** Where the run starts in DAY_ORDER, for ordering the rows. */
  firstDay: number;
}

/**
 * Weekly events as rows in Sunday-first order, merging adjacent days with
 * identical times and the same pattern.
 *
 * Runs of days with weeks of the month are never merged: the weeks count
 * occurrences of each weekday, so "first Saturday and Sunday" names two
 * dates that may fall in different weeks, and the note names the weekday.
 */
export function weeklyScheduleRows(events: EventSummary[]): ScheduleRollupRow[] {
  const byPattern = new Map<string, PatternDays>();
  for (const event of events) {
    if (event.kind !== "weekly" || !event.day_of_week) continue;
    const day = DAY_ORDER[jsDayFor(event.day_of_week)];
    if (!day) continue;
    const key = patternKey(event);
    let group = byPattern.get(key);
    if (!group) {
      group = { pattern: event, timesByDay: new Map() };
      byPattern.set(key, group);
    }
    const times = group.timesByDay.get(day) ?? [];
    if (!times.includes(event.start_time)) times.push(event.start_time);
    group.timesByDay.set(day, times);
  }

  const runs: Run[] = [];
  for (const [key, { pattern, timesByDay }] of byPattern) {
    const mergeDays = pattern.weeks_of_month.length === 0;
    let previous: (Run & { signature: string }) | null = null;
    for (const [index, day] of DAY_ORDER.entries()) {
      const times = timesByDay.get(day);
      if (!times) {
        previous = null;
        continue;
      }
      const sorted = [...times].sort((a, b) => a - b);
      const signature = sorted.join(",");
      if (mergeDays && previous && previous.signature === signature) {
        previous.days.push(day);
        continue;
      }
      previous = {
        key,
        days: [day],
        times: sorted,
        note: describeSchedulePattern(pattern, day),
        firstDay: index,
        signature,
      };
      runs.push(previous);
    }
  }

  // Sunday first; on the same day, the every-week row before qualified ones.
  runs.sort((a, b) => a.firstDay - b.firstDay || a.key.localeCompare(b.key));
  return runs.map((run) => ({
    key: `weekly:${run.days.join("-")}:${run.key}`,
    label: runLabel(run.days),
    times: run.times.map(formatMinutesMissal),
    note: run.note,
  }));
}
