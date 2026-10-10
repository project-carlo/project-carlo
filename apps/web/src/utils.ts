import type { Season, WeekOfMonth } from "./types";

/** Format minutes since midnight for display: e.g. `7:30 a.m.` — lowercase
 *  meridiem. Omits `:00` for on-the-hour times so `8 a.m.` reads naturally. */
export function formatMinutesMissal(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  const meridiem = h < 12 ? "a.m." : "p.m.";
  const displayH = h === 0 ? 12 : h > 12 ? h - 12 : h;
  if (m === 0) return `${displayH} ${meridiem}`;
  return `${displayH}:${m.toString().padStart(2, "0")} ${meridiem}`;
}

/** Capitalize the first letter of a string. */
export function titleCase(value: string): string {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

// Formatters built once and reused: constructing an Intl formatter costs far
// more than formatting with it, and a church page formats one date per listed
// service. (Weekday and month stay separate formatters — asking for both at
// once yields "March Tuesday" in en-US.)
const LONG_WEEKDAY_FORMATTER = new Intl.DateTimeFormat("en-US", {
  weekday: "long",
});
const LONG_MONTH_FORMATTER = new Intl.DateTimeFormat("en-US", { month: "long" });
const eventDateCache = new Map<string, string>();

/** Format YYYY-MM-DD to "Tuesday, March 17th" style. */
export function formatEventDate(dateStr: string): string {
  const cached = eventDateCache.get(dateStr);
  if (cached !== undefined) return cached;
  const d = new Date(dateStr + "T12:00:00");
  const weekday = LONG_WEEKDAY_FORMATTER.format(d);
  const month = LONG_MONTH_FORMATTER.format(d);
  const day = d.getDate();
  const suffix =
    day >= 11 && day <= 13
      ? "th"
      : { 1: "st", 2: "nd", 3: "rd" }[day % 10] ?? "th";
  const formatted = `${weekday}, ${month} ${day}${suffix}`;
  eventDateCache.set(dateStr, formatted);
  return formatted;
}

const LONG_MONTH_DAY_FORMATTER = new Intl.DateTimeFormat("en-US", {
  month: "long",
  day: "numeric",
});

/** Format YYYY-MM-DD to "October 5" style. */
export function formatLongMonthDay(dateStr: string): string {
  return LONG_MONTH_DAY_FORMATTER.format(new Date(dateStr + "T12:00:00"));
}

const SHORT_MONTH_DAY_FORMATTER = new Intl.DateTimeFormat("en-US", {
  month: "short",
  day: "numeric",
});

/** Format YYYY-MM-DD to "Oct 7" style. */
export function formatMonthDay(dateStr: string): string {
  return SHORT_MONTH_DAY_FORMATTER.format(new Date(dateStr + "T12:00:00"));
}

/** Format structured address fields into a single display string. */
export function formatAddress(church: {
  address_line1: string | null;
  address_line2: string | null;
  city: string | null;
  state: string | null;
  postal_code: string | null;
}): string | null {
  const parts: string[] = [];
  if (church.address_line1) parts.push(church.address_line1);
  if (church.address_line2) parts.push(church.address_line2);
  const stateZip = [church.state, church.postal_code].filter(Boolean).join(" ");
  const cityStateZip = [church.city, stateZip].filter(Boolean).join(", ");
  if (cityStateZip) parts.push(cityStateZip);
  return parts.length > 0 ? parts.join(", ") : null;
}

const WEEK_LABELS: Record<WeekOfMonth, string> = {
  first: "1st",
  second: "2nd",
  third: "3rd",
  fourth: "4th",
  fifth: "5th",
  last: "last",
};
const SHORT_MONTHS = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

/** "1st", "1st & 3rd", "1st, 3rd & last". */
function joinWithAmpersand(items: string[]): string {
  if (items.length <= 1) return items.join("");
  return `${items.slice(0, -1).join(", ")} & ${items[items.length - 1]}`;
}

function formatSeasonEnd(month: number, day: number | null): string {
  const name = SHORT_MONTHS[month - 1] ?? String(month);
  return day == null ? name : `${name} ${day}`;
}

/**
 * What qualifies a weekly slot that isn't every week of the year: the weeks
 * of the month it keeps and its season, e.g. "1st & 3rd", "May–Oct" or
 * "last, Jun 15–Sep 7". Null for a slot held every week, all year.
 */
export function formatSlotQualifier(slot: {
  weeks_of_month: readonly WeekOfMonth[];
  season: Season | null;
}): string | null {
  const parts: string[] = [];
  if (slot.weeks_of_month.length > 0) {
    const weeks = (Object.keys(WEEK_LABELS) as WeekOfMonth[]).filter((week) =>
      slot.weeks_of_month.includes(week),
    );
    parts.push(joinWithAmpersand(weeks.map((week) => WEEK_LABELS[week])));
  }
  const { season } = slot;
  if (season) {
    const start = formatSeasonEnd(season.start_month, season.start_day);
    const end = formatSeasonEnd(season.end_month, season.end_day);
    parts.push(start === end ? start : `${start}–${end}`);
  }
  return parts.length > 0 ? parts.join(", ") : null;
}

/** A slot's time with its qualifier, if any: "10 a.m. (1st & 3rd)". */
export function formatQualifiedTime(time: string, qualifier: string | null): string {
  return qualifier ? `${time} (${qualifier})` : time;
}
