import { DAYS, type Day } from "../types";

const DAY_ALIASES: Record<string, Day[]> = {
  weekdays: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
  weekday: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
  weekends: ["Saturday", "Sunday"],
  weekend: ["Saturday", "Sunday"],
  daily: [...DAYS],
  everyday: [...DAYS],
  all: [...DAYS],
};

const SINGLE_LETTER: Record<string, Day> = { m: "Monday", w: "Wednesday", f: "Friday" };

function matchDay(token: string): Day | null {
  if (SINGLE_LETTER[token]) return SINGLE_LETTER[token];
  if (token.length < 2) return null;
  const found = DAYS.filter((d) => d.toLowerCase().startsWith(token));
  return found.length === 1 ? found[0] : null;
}

/**
 * Parse a day list: "Sun", "Mon-Fri", "sat, sun", "Tue & Thu", "weekdays",
 * "fri-mon" (wrapping). Returns days in week order, or null if any part is
 * unreadable.
 */
export function parseDays(input: string): Day[] | null {
  const text = input
    .trim()
    .toLowerCase()
    .replace(/[–—]/g, "-")
    .replace(/\s*-\s*/g, "-")
    .replace(/\b(and|&)\b|&/g, ",")
    .replace(/every\s*day/g, "everyday")
    .replace(/\.(?=\s|,|-|$)/g, "");
  if (!text) return null;
  const picked = new Set<Day>();
  for (const token of text.split(/[\s,/+]+/).filter(Boolean)) {
    const alias = DAY_ALIASES[token] ?? DAY_ALIASES[token.replace(/s$/, "")];
    if (alias) {
      alias.forEach((d) => picked.add(d));
      continue;
    }
    const range = token.split("-");
    if (range.length === 2) {
      const from = matchDay(range[0]);
      const to = matchDay(range[1]);
      if (!from || !to) return null;
      let i = DAYS.indexOf(from);
      const end = DAYS.indexOf(to);
      picked.add(DAYS[i]);
      while (i !== end) {
        i = (i + 1) % 7;
        picked.add(DAYS[i]);
      }
      continue;
    }
    const day = matchDay(token.replace(/s$/, "")) ?? matchDay(token);
    if (!day) return null;
    picked.add(day);
  }
  return DAYS.filter((d) => picked.has(d));
}

export const MONTHS = [
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

/** Month number from a name or abbreviation ("Sept", "oct"), or null. */
export function monthFromName(token: string): number | null {
  const t = token.toLowerCase().replace(/\.$/, "");
  if (t.length < 3) return null;
  const i = MONTHS.findIndex((m) => m.toLowerCase().startsWith(t));
  return i === -1 ? null : i + 1;
}

function iso(y: number, m: number, d: number): string | null {
  const date = new Date(Date.UTC(y, m - 1, d));
  if (date.getUTCFullYear() !== y || date.getUTCMonth() !== m - 1 || date.getUTCDate() !== d) {
    return null;
  }
  return `${y}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
}

/** The year that puts month/day closest to `ref` (a bulletin reaches a few months either way). */
function nearestYear(m: number, d: number, ref: string | null): number {
  const refDate = ref ? new Date(`${ref}T00:00:00Z`) : new Date();
  const base = refDate.getUTCFullYear();
  let best = base;
  let bestGap = Infinity;
  for (const y of [base - 1, base, base + 1]) {
    const gap = Math.abs(Date.UTC(y, m - 1, d) - refDate.getTime());
    if (gap < bestGap) {
      best = y;
      bestGap = gap;
    }
  }
  return best;
}

/**
 * Parse one date: "2026-10-05", "10/5", "10/5/26", "Oct 5", "5 October".
 * A date without a year takes the year nearest `ref` (the bulletin's date).
 */
export function parseLooseDate(input: string, ref: string | null): string | null {
  const t = input.trim().toLowerCase().replace(/,/g, " ").replace(/\s+/g, " ");
  if (!t) return null;
  let m = /^(\d{4})-(\d{1,2})-(\d{1,2})$/.exec(t);
  if (m) return iso(Number(m[1]), Number(m[2]), Number(m[3]));
  m = /^(\d{1,2})[/.-](\d{1,2})(?:[/.-](\d{2}|\d{4}))?$/.exec(t);
  if (m) {
    const month = Number(m[1]);
    const day = Number(m[2]);
    let year = m[3] ? Number(m[3]) : nearestYear(month, day, ref);
    if (year < 100) year += 2000;
    return iso(year, month, day);
  }
  // Optional weekday in front: "Mon Oct 5", "Monday, October 5 2026".
  const words = t.split(" ").filter((w) => !DAYS.some((d) => d.toLowerCase().startsWith(w) && w.length >= 3));
  let month: number | null = null;
  let day: number | null = null;
  let year: number | null = null;
  for (const w of words) {
    const num = /^(\d{1,4})(st|nd|rd|th)?$/.exec(w);
    if (num) {
      const n = Number(num[1]);
      if (n > 31) year = n;
      else if (day === null) day = n;
      else year = n < 100 ? 2000 + n : n;
      continue;
    }
    const mm = monthFromName(w);
    if (mm === null) return null;
    month = mm;
  }
  if (month === null || day === null) return null;
  return iso(year ?? nearestYear(month, day, ref), month, day);
}

/** Several dates separated by commas or semicolons ("10/2; 10/9"); null if any is unreadable. */
export function parseDates(input: string, ref: string | null): string[] | null {
  const parts = input.split(/;|,(?=\s*(?:\d{1,2}[/.-]|\d{4}-|[a-z]{3}))/i).map((p) => p.trim()).filter(Boolean);
  if (parts.length === 0) return null;
  const out: string[] = [];
  for (const part of parts) {
    const date = parseLooseDate(part, ref);
    if (!date) return null;
    if (!out.includes(date)) out.push(date);
  }
  return out;
}

/**
 * The first `day` on or after `bulletinDate`.
 *
 * A bulletin dated Sunday covers that Sunday through the following Saturday.
 * The same rule the pipeline uses when it credits a weekly row to a week:
 * `(weekday - bulletin weekday) mod 7`.
 */
export function dateForWeekday(bulletinDate: string, day: Day): string | null {
  const bulletin = new Date(`${bulletinDate}T00:00:00Z`);
  if (Number.isNaN(bulletin.getTime())) return null;
  const target = DAYS.indexOf(day);
  if (target < 0) return null;
  const bulletinWeekday = (bulletin.getUTCDay() + 6) % 7;
  const offset = (target - bulletinWeekday + 7) % 7;
  return new Date(bulletin.getTime() + offset * 86_400_000).toISOString().slice(0, 10);
}

/** Weekday of an ISO date, in the same Monday-first order as `DAYS`. */
export function dayOfDate(isoDate: string): Day | null {
  const d = new Date(`${isoDate}T00:00:00Z`);
  if (Number.isNaN(d.getTime())) return null;
  return DAYS[(d.getUTCDay() + 6) % 7] ?? null;
}

export function daysBetween(a: string, b: string): number {
  return Math.round(
    (Date.parse(`${a}T00:00:00Z`) - Date.parse(`${b}T00:00:00Z`)) / 86_400_000,
  );
}

/** "Mon Oct 5" for an ISO date. */
export function formatDate(isoDate: string | null): string {
  if (!isoDate) return "";
  const d = new Date(`${isoDate}T00:00:00Z`);
  if (Number.isNaN(d.getTime())) return isoDate;
  const weekday = DAYS[(d.getUTCDay() + 6) % 7].slice(0, 3);
  return `${weekday} ${MONTHS[d.getUTCMonth()].slice(0, 3)} ${d.getUTCDate()}`;
}

export function shortDay(day: Day | null): string {
  return day ? day.slice(0, 3) : "";
}

/** "Mon–Fri" for three or more consecutive days (in week order), otherwise "Sat, Sun". */
export function describeDays(days: Day[]): string {
  const idx = days.map((d) => DAYS.indexOf(d));
  const consecutive = idx.every((v, i) => i === 0 || v === idx[i - 1] + 1);
  if (days.length >= 3 && consecutive) return `${shortDay(days[0])}–${shortDay(days[days.length - 1])}`;
  return days.map(shortDay).join(", ");
}
