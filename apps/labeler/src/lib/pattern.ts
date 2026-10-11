/**
 * Recurrence qualifiers of a weekly row: weeks of the month and season.
 *
 * Same representation as the pipeline's `schedule_pattern` (PR #22): weeks
 * are canonical ordinals with "last" distinct from "fourth" (a five-Friday
 * month has both), an empty list means every week, and a season is an
 * inclusive month/day range that may wrap past New Year (Sep-May = 9-5).
 * With `exclude_weeks` the listed weeks are the ones skipped: "all but last"
 * is `["last"]` excluded, since no list of ordinals can say it (the week it
 * drops is the fourth in some months and the fifth in others).
 */
import { WEEKS_OF_MONTH, type Season, type WeekOfMonth } from "../types";
import { MONTHS, monthFromName } from "./dates";

export const NUMBERED_WEEKS: WeekOfMonth[] = ["first", "second", "third", "fourth", "fifth"];

export const WEEK_LABELS: Record<WeekOfMonth, string> = {
  first: "1st",
  second: "2nd",
  third: "3rd",
  fourth: "4th",
  fifth: "5th",
  last: "Last",
};

// February gets 29: a season boundary recurs every year, leap years included.
const DAYS_IN_MONTH = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

export function sortWeeks(weeks: WeekOfMonth[]): WeekOfMonth[] {
  return WEEKS_OF_MONTH.filter((w) => weeks.includes(w));
}

/** Weeks that name every occurrence (all five numbered weeks) are just "every week". */
function normalizeWeeks(weeks: WeekOfMonth[]): WeekOfMonth[] {
  const sorted = sortWeeks(weeks);
  return NUMBERED_WEEKS.every((w) => sorted.includes(w)) ? [] : sorted;
}

export function toggleWeek(weeks: WeekOfMonth[], week: WeekOfMonth): WeekOfMonth[] {
  return normalizeWeeks(
    weeks.includes(week) ? weeks.filter((w) => w !== week) : [...weeks, week],
  );
}

export interface WeeksSelection {
  weeks: WeekOfMonth[];
  exclude: boolean;
}

/**
 * The one way to write a selection, as the pipeline's `canonical_weeks`: an
 * exclusion without "last" is the weeks that remain, one with "last" drops
 * "fifth" (a fifth weekday is always the last), and excluding nothing is
 * every week.
 */
export function canonicalWeeks(weeks: WeekOfMonth[], exclude: boolean): WeeksSelection {
  const sorted = sortWeeks(weeks);
  if (!exclude || sorted.length === 0) return { weeks: sorted, exclude: false };
  if (!sorted.includes("last")) {
    const remaining = NUMBERED_WEEKS.filter((w) => !sorted.includes(w));
    return remaining.length ? { weeks: remaining, exclude: false } : { weeks: sorted, exclude: true };
  }
  return { weeks: sorted.filter((w) => w !== "fifth"), exclude: true };
}

/**
 * "All but <week>" as stored weeks: "all but 2nd" is [first, third, fourth,
 * fifth], and "all but last" is [last] excluded.
 */
export function allBut(week: WeekOfMonth): WeeksSelection {
  if (week === "last") return { weeks: ["last"], exclude: true };
  return { weeks: NUMBERED_WEEKS.filter((w) => w !== week), exclude: false };
}

/** The single week an "all but" selection leaves out, if the selection is one. */
export function allButWeek(weeks: WeekOfMonth[], exclude = false): WeekOfMonth | null {
  if (exclude) return weeks.length === 1 ? weeks[0] : null;
  if (weeks.length !== 4 || weeks.includes("last")) return null;
  const missing = NUMBERED_WEEKS.filter((w) => !weeks.includes(w));
  return missing.length === 1 ? missing[0] : null;
}

export function describeWeeks(weeks: WeekOfMonth[], exclude = false): string {
  if (weeks.length === 0) return "Every week";
  if (exclude) return `All but ${sortWeeks(weeks).map((w) => WEEK_LABELS[w]).join(" & ")}`;
  const skipped = allButWeek(weeks);
  if (skipped) return `All but ${WEEK_LABELS[skipped]}`;
  return sortWeeks(weeks).map((w) => WEEK_LABELS[w]).join(" & ");
}

// ── Seasons ────────────────────────────────────────────────────────────────
export function seasonProblems(season: Season): string[] {
  const problems: string[] = [];
  for (const edge of ["start", "end"] as const) {
    const month = season[`${edge}_month`];
    const day = season[`${edge}_day`];
    if (!Number.isInteger(month) || month < 1 || month > 12) {
      problems.push(`${edge} month must be 1-12`);
    } else if (day !== null && (!Number.isInteger(day) || day < 1 || day > DAYS_IN_MONTH[month - 1])) {
      problems.push(`${edge} day ${day} is not in ${MONTHS[month - 1]}`);
    }
  }
  return problems;
}

/** Whether (month, day) falls in the season; a season whose start is after its end wraps New Year. */
export function inSeason(season: Season, month: number, day: number): boolean {
  const start = season.start_month * 100 + (season.start_day ?? 1);
  const end = season.end_month * 100 + (season.end_day ?? DAYS_IN_MONTH[season.end_month - 1]);
  const at = month * 100 + day;
  return start <= end ? at >= start && at <= end : at >= start || at <= end;
}

function describeEdge(month: number, day: number | null): string {
  const name = MONTHS[month - 1]?.slice(0, 3) ?? `?${month}`;
  return day === null ? name : `${name} ${day}`;
}

export function describeSeason(season: Season | null): string {
  if (!season) return "All year";
  return `${describeEdge(season.start_month, season.start_day)} – ${describeEdge(season.end_month, season.end_day)}`;
}

function parseEdge(text: string): { month: number; day: number | null } | null {
  const t = text.trim().toLowerCase().replace(/(\d)(st|nd|rd|th)\b/g, "$1");
  let m = /^(\d{1,2})(?:[/.](\d{1,2}))?$/.exec(t);
  if (m) {
    return { month: Number(m[1]), day: m[2] === undefined ? null : Number(m[2]) };
  }
  m = /^([a-z]+)\.?\s*(\d{1,2})?$/.exec(t);
  if (m) {
    const month = monthFromName(m[1]);
    if (month === null) return null;
    return { month, day: m[2] === undefined ? null : Number(m[2]) };
  }
  m = /^(\d{1,2})\s*([a-z]+)\.?$/.exec(t);
  if (m) {
    const month = monthFromName(m[2]);
    return month === null ? null : { month, day: Number(m[1]) };
  }
  return null;
}

/**
 * Parse a season: "Sep-May", "9-5", "Oct through June", "Jun 4 - Sep 10",
 * "6/4-9/10". Empty input (or "all year") is no season: `{ season: null }`.
 * Returns null when unreadable or impossible.
 */
export function parseSeason(input: string): { season: Season | null } | null {
  const t = input.trim().toLowerCase().replace(/[–—]/g, "-");
  if (!t || t === "all year" || t === "year round" || t === "-") return { season: null };
  const parts = t.split(/\s*(?:-|\bthrough\b|\bthru\b|\bto\b|\buntil\b)\s*/).filter(Boolean);
  if (parts.length !== 2) return null;
  const start = parseEdge(parts[0]);
  const end = parseEdge(parts[1]);
  if (!start || !end) return null;
  const season: Season = {
    start_month: start.month,
    start_day: start.day,
    end_month: end.month,
    end_day: end.day,
  };
  return seasonProblems(season).length ? null : { season };
}
