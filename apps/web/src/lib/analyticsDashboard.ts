/**
 * The analytics dashboard's arithmetic (src/views/AnalyticsDashboardPage.tsx),
 * kept apart from React so it can be tested: the daily series with its empty
 * days filled in, a clean top for the chart's scale, and row labels.
 */
import type { AnalyticsRow } from "./analyticsReports";

export interface DayTotals {
  /** UTC date, YYYY-MM-DD. */
  date: string;
  visits: number;
  pageviews: number;
}

const DAY_MS = 24 * 60 * 60 * 1000;

/**
 * One entry per UTC day the report covers, oldest first, zero where nothing
 * happened (the report has no row for those). A report of the last `days`
 * days reaches back into a part of the day `days` ago, so that day is shown.
 */
export function fillDays(rows: AnalyticsRow[], days: number, now: number = Date.now()): DayTotals[] {
  const byDate = new Map<string, DayTotals>();
  for (const row of rows) {
    const date = String(row.day).slice(0, 10);
    byDate.set(date, { date, visits: Number(row.visits) || 0, pageviews: Number(row.pageviews) || 0 });
  }
  const out: DayTotals[] = [];
  for (let back = days; back >= 0; back--) {
    const date = new Date(now - back * DAY_MS).toISOString().slice(0, 10);
    out.push(byDate.get(date) ?? { date, visits: 0, pageviews: 0 });
  }
  return out;
}

/** The smallest of 1, 2 or 5 × a power of ten at or above `value`. */
export function niceMax(value: number): number {
  if (!(value > 0)) return 1;
  const power = 10 ** Math.floor(Math.log10(value));
  for (const step of [1, 2, 5, 10]) {
    if (step * power >= value) return step * power;
  }
  return 10 * power;
}

/** A ranked row's count: its last column. */
export function rowCount(row: AnalyticsRow): number {
  const values = Object.values(row);
  return Number(values[values.length - 1]) || 0;
}

/** A ranked row's label: every column before the count, joined. */
export function rowLabel(row: AnalyticsRow): string {
  const values = Object.values(row).slice(0, -1).map(String);
  return values.filter(Boolean).join(" · ") || "(none)";
}
