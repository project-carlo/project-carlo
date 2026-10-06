import { DAY_ORDER } from "../constants/days";
import type { EventSummary } from "../types";
import { formatMinutesMissal } from "../utils";
import type { ScheduleRollupRow } from "./eventRollup";

/**
 * A compact weekly schedule for listing many churches on one page (a city
 * page): one row per day, with runs of days that share the same times folded
 * into one row ("Mon – Fri  8 a.m."). Pure formatting logic.
 */

const DAY_ABBR: Record<string, string> = {
  sunday: "Sun",
  monday: "Mon",
  tuesday: "Tue",
  wednesday: "Wed",
  thursday: "Thu",
  friday: "Fri",
  saturday: "Sat",
};

function pluralDay(day: string): string {
  return day.charAt(0).toUpperCase() + day.slice(1) + "s";
}

function runLabel(days: string[]): string {
  if (days.length === 1) return pluralDay(days[0]);
  const first = DAY_ABBR[days[0]];
  const last = DAY_ABBR[days[days.length - 1]];
  return days.length === 2 ? `${first} & ${last}` : `${first} – ${last}`;
}

/** Weekly events as rows in Sunday-first order, merging adjacent days with identical times. */
export function weeklyScheduleRows(events: EventSummary[]): ScheduleRollupRow[] {
  const timesByDay = new Map<string, number[]>();
  for (const event of events) {
    if (event.kind !== "weekly" || !event.day_of_week) continue;
    const day = event.day_of_week.toLowerCase();
    const times = timesByDay.get(day) ?? [];
    if (!times.includes(event.start_time)) times.push(event.start_time);
    timesByDay.set(day, times);
  }

  const runs: { days: string[]; times: number[]; signature: string }[] = [];
  let previousDayListed = false;
  for (const day of DAY_ORDER) {
    const times = timesByDay.get(day);
    if (!times) {
      previousDayListed = false;
      continue;
    }
    const sorted = [...times].sort((a, b) => a - b);
    const signature = sorted.join(",");
    const last = runs[runs.length - 1];
    if (previousDayListed && last.signature === signature) {
      last.days.push(day);
    } else {
      runs.push({ days: [day], times: sorted, signature });
    }
    previousDayListed = true;
  }

  return runs.map((run) => ({
    key: `weekly:${run.days.join("-")}`,
    label: runLabel(run.days),
    times: run.times.map(formatMinutesMissal),
  }));
}
