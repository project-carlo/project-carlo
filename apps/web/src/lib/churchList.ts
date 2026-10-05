/**
 * Pure logic behind the map's results list: which churches are in the area,
 * how far each is, when each next has a matching service, and how that is
 * worded. No DOM, no React — `ChurchList` renders what this returns.
 */
import { FILTER_DAY_LABELS, jsDayFor } from "../constants/days";
import { EVENT_TYPE_LABELS } from "../constants/eventTypes";
import { MINUTES_PER_DAY, type FilterState } from "../components/filterState";
import type { ChurchMapItem, EventSummary } from "../types";
import { formatMinutesMissal } from "../utils";
import { haversineMiles, type LatLng } from "./places";
import { parseIsoDateLocal } from "./schedule";

// -------------------------------------------------------------- constants

/** A "Soon" badge shows when the next service starts within this many minutes. */
export const SOON_MINUTES = 90;

/** Rows shown before "Show more", and how many each press adds. */
export const LIST_PAGE_SIZE = 40;

/** Day groups a row's "then" line spells out before it summarises the rest. */
const MAX_THEN_GROUPS = 3;

const MS_PER_MINUTE = 60_000;

export type ListSort = "nearest" | "soonest";
export const DEFAULT_LIST_SORT: ListSort = "nearest";

export function parseListSort(raw: string | null): ListSort {
  return raw === "soonest" ? "soonest" : DEFAULT_LIST_SORT;
}

// ----------------------------------------------------------------- bounds

/** A lat/lng rectangle (never crossing the antimeridian — fine for New York). */
export interface GeoBounds {
  south: number;
  west: number;
  north: number;
  east: number;
}

export function boundsContain(bounds: GeoBounds, point: LatLng): boolean {
  return (
    point.lat >= bounds.south &&
    point.lat <= bounds.north &&
    point.lng >= bounds.west &&
    point.lng <= bounds.east
  );
}

export function boundsCenter(bounds: GeoBounds): LatLng {
  return {
    lat: (bounds.south + bounds.north) / 2,
    lng: (bounds.west + bounds.east) / 2,
  };
}

/**
 * Whether the map has moved far enough from `searched` that "Search this area"
 * is worth offering: its centre shifted by over a tenth of the area's size, or
 * the area grew or shrank by a fifth.
 */
export function boundsMoved(searched: GeoBounds, live: GeoBounds): boolean {
  const width = searched.east - searched.west;
  const height = searched.north - searched.south;
  if (width <= 0 || height <= 0) return true;
  const a = boundsCenter(searched);
  const b = boundsCenter(live);
  if (Math.abs(a.lng - b.lng) / width > 0.1) return true;
  if (Math.abs(a.lat - b.lat) / height > 0.1) return true;
  const ratio = (live.east - live.west) / width;
  return ratio < 0.8 || ratio > 1.25;
}

// ------------------------------------------------------------ occurrences

/** One concrete upcoming service. */
export interface Slot {
  at: Date;
  /** Minutes since midnight, as stored on the event. */
  minutes: number;
}

function startOfDay(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

function atMinutes(day: Date, minutes: number): Date {
  const d = new Date(day);
  d.setHours(Math.floor(minutes / 60), minutes % 60, 0, 0);
  return d;
}

/**
 * The next time this event starts at or after `now`, or null for a cancelled
 * event, an unreadable one, or a dated one that has passed.
 *
 * The snapshot's own `next_occurrence` is measured from midnight, so a weekly
 * slot earlier today still reads as "today"; the list wants what is still to
 * come, so it works the instant out itself.
 */
export function nextStart(event: EventSummary, now: Date): Date | null {
  if (event.cancelled) return null;
  if (event.kind === "weekly" && event.day_of_week) {
    const jsDay = jsDayFor(event.day_of_week);
    if (jsDay < 0) return null;
    const today = startOfDay(now);
    const daysAhead = (jsDay - today.getDay() + 7) % 7;
    const day = new Date(today);
    day.setDate(day.getDate() + daysAhead);
    let at = atMinutes(day, event.start_time);
    if (at.getTime() < now.getTime()) {
      day.setDate(day.getDate() + 7);
      at = atMinutes(day, event.start_time);
    }
    return at;
  }
  if (event.kind === "specific_date" && event.date) {
    const parsed = parseIsoDateLocal(event.date);
    if (!parsed) return null;
    const at = atMinutes(startOfDay(parsed), event.start_time);
    return at.getTime() < now.getTime() ? null : at;
  }
  return null;
}

/** A church's upcoming services (those its filters kept), soonest first. */
export function upcomingSlots(church: ChurchMapItem, now: Date): Slot[] {
  const seen = new Set<number>();
  const slots: Slot[] = [];
  for (const event of church.upcoming_events) {
    const at = nextStart(event, now);
    if (!at) continue;
    const stamp = at.getTime();
    if (seen.has(stamp)) continue;
    seen.add(stamp);
    slots.push({ at, minutes: event.start_time });
  }
  return slots.sort((a, b) => a.at.getTime() - b.at.getTime());
}

// ------------------------------------------------------------------- rows

export interface ListRow {
  church: ChurchMapItem;
  distanceMiles: number | null;
  slots: Slot[];
  /** Minutes until the first slot, or null when nothing is upcoming. */
  minutesUntilNext: number | null;
}

type MappedChurch = ChurchMapItem & { latitude: number; longitude: number };

function hasCoords(church: ChurchMapItem): church is MappedChurch {
  return church.latitude !== null && church.longitude !== null;
}

function toRow(
  church: MappedChurch,
  ref: LatLng | null,
  now: Date,
): ListRow {
  const slots = upcomingSlots(church, now);
  return {
    church,
    distanceMiles: ref
      ? haversineMiles(ref, { lat: church.latitude, lng: church.longitude })
      : null,
    slots,
    minutesUntilNext:
      slots.length > 0
        ? Math.max(0, Math.round((slots[0].at.getTime() - now.getTime()) / MS_PER_MINUTE))
        : null,
  };
}

/** Rows for the mapped churches inside `bounds`, unsorted. */
export function buildRows(
  churches: ChurchMapItem[],
  bounds: GeoBounds,
  ref: LatLng | null,
  now: Date,
): ListRow[] {
  const rows: ListRow[] = [];
  for (const church of churches) {
    if (!hasCoords(church)) continue;
    if (!boundsContain(bounds, { lat: church.latitude, lng: church.longitude })) {
      continue;
    }
    rows.push(toRow(church, ref, now));
  }
  return rows;
}

function compareDistance(a: ListRow, b: ListRow): number {
  const da = a.distanceMiles ?? Number.POSITIVE_INFINITY;
  const db = b.distanceMiles ?? Number.POSITIVE_INFINITY;
  if (da !== db) return da - db;
  return (a.church.name ?? "").localeCompare(b.church.name ?? "");
}

/** A sorted copy: "nearest" by distance, "soonest" by next service (then distance). */
export function sortRows(rows: ListRow[], sort: ListSort): ListRow[] {
  const sorted = [...rows];
  if (sort === "nearest") return sorted.sort(compareDistance);
  return sorted.sort((a, b) => {
    const ta = a.slots[0]?.at.getTime() ?? Number.POSITIVE_INFINITY;
    const tb = b.slots[0]?.at.getTime() ?? Number.POSITIVE_INFINITY;
    if (ta !== tb) return ta - tb;
    return compareDistance(a, b);
  });
}

/** The closest church to `ref` among all of `churches`, wherever it is. */
export function nearestRow(
  churches: ChurchMapItem[],
  ref: LatLng,
  now: Date,
): ListRow | null {
  let best: MappedChurch | null = null;
  let bestDistance = Number.POSITIVE_INFINITY;
  for (const church of churches) {
    if (!hasCoords(church)) continue;
    const distance = haversineMiles(ref, {
      lat: church.latitude,
      lng: church.longitude,
    });
    if (distance < bestDistance) {
      best = church;
      bestDistance = distance;
    }
  }
  return best ? toRow(best, ref, now) : null;
}

// ------------------------------------------------------------- formatting

/** "2.3 mi", "14 mi", "<0.1 mi". */
export function formatDistance(miles: number): string {
  if (miles < 0.1) return "<0.1 mi";
  if (miles < 10) return `${miles.toFixed(1)} mi`;
  return `${Math.round(miles)} mi`;
}

const SHORT_DATE = new Intl.DateTimeFormat("en-US", {
  weekday: "short",
  month: "short",
  day: "numeric",
});
const SHORT_WEEKDAY = new Intl.DateTimeFormat("en-US", { weekday: "short" });

function dayDiff(now: Date, at: Date): number {
  const a = startOfDay(now).getTime();
  const b = startOfDay(at).getTime();
  return Math.round((b - a) / (24 * 60 * MS_PER_MINUTE));
}

/** "Today", "Tomorrow", "Sat", "Next Sat", or "Sat, Oct 18". */
export function dayLabel(at: Date, now: Date): string {
  const diff = dayDiff(now, at);
  if (diff <= 0) return "Today";
  if (diff === 1) return "Tomorrow";
  if (diff < 7) return SHORT_WEEKDAY.format(at);
  if (diff === 7) return `Next ${SHORT_WEEKDAY.format(at)}`;
  return SHORT_DATE.format(at);
}

export interface DayGroup {
  key: string;
  label: string;
  times: string[];
}

function groupByDay(slots: Slot[], now: Date): DayGroup[] {
  const groups: DayGroup[] = [];
  for (const slot of slots) {
    const key = `${slot.at.getFullYear()}-${slot.at.getMonth()}-${slot.at.getDate()}`;
    const time = formatMinutesMissal(slot.minutes);
    const last = groups[groups.length - 1];
    if (last && last.key === key) {
      last.times.push(time);
    } else {
      groups.push({ key, label: dayLabel(slot.at, now), times: [time] });
    }
  }
  return groups;
}

export interface NextTimes {
  /** The very next service, or null when nothing is upcoming. */
  next: { day: string; time: string; minutesUntil: number; soon: boolean } | null;
  /** The services after it, a day to a group. */
  then: DayGroup[];
  /** Day groups left out of `then` to keep the row short. */
  moreDays: number;
}

/** What a row shows for its times: an emphasised next one, then the rest. */
export function formatNextTimes(row: ListRow, now: Date): NextTimes {
  const [first, ...rest] = row.slots;
  if (!first) return { next: null, then: [], moreDays: 0 };
  const minutesUntil = row.minutesUntilNext ?? 0;
  const groups = groupByDay(rest, now);
  return {
    next: {
      day: dayLabel(first.at, now),
      time: formatMinutesMissal(first.minutes),
      minutesUntil,
      soon: minutesUntil <= SOON_MINUTES,
    },
    then: groups.slice(0, MAX_THEN_GROUPS),
    moreDays: Math.max(0, groups.length - MAX_THEN_GROUPS),
  };
}

/** "Sat 4 p.m. · Sun 8, 10:30 a.m." — a day's times share its label. */
export function thenText(groups: DayGroup[]): string {
  return groups.map((g) => `${g.label} ${g.times.join(", ")}`).join(" · ");
}

// ---------------------------------------------------------- filter phrases

/** "between 4 and 6 p.m.", "after 4 p.m.", "before noon" — or null for all day. */
export function describeTimeRange(from: number, to: number): string | null {
  const fromOpen = from <= 0;
  const toOpen = to >= MINUTES_PER_DAY - 1;
  if (fromOpen && toOpen) return null;
  if (fromOpen) return `before ${formatMinutesMissal(to)}`;
  if (toOpen) return `after ${formatMinutesMissal(from)}`;
  const start = formatMinutesMissal(from);
  const end = formatMinutesMissal(to);
  // "4 and 6 p.m." when both ends share a half of the day.
  if (start.slice(-4) === end.slice(-4)) {
    return `between ${start.replace(/ [ap]\.m\.$/, "")} and ${end}`;
  }
  return `between ${start} and ${end}`;
}

/** "on Saturday", "on Saturday or Sunday", "on 4 days" — or null for any day. */
export function describeDays(days: number[]): string | null {
  if (days.length === 0) return null;
  const sorted = [...days].sort((a, b) => a - b);
  if (sorted.length > 3) return `on ${sorted.length} days`;
  const names = sorted.map((d) => FILTER_DAY_LABELS[d].full);
  if (names.length === 1) return `on ${names[0]}`;
  return `on ${names.slice(0, -1).join(", ")} or ${names[names.length - 1]}`;
}

export interface FilterPhrases {
  type: string;
  days: string | null;
  time: string | null;
}

export function describeFilters(filters: FilterState): FilterPhrases {
  return {
    type: EVENT_TYPE_LABELS[filters.eventType],
    days: describeDays(filters.daysOfWeek),
    time: describeTimeRange(filters.timeFrom, filters.timeTo),
  };
}

/** "18 churches in this area · 112 in all". */
export function countSummary(inArea: number, total: number | undefined): string {
  const noun = inArea === 1 ? "church" : "churches";
  const head = `${inArea} ${noun} in this area`;
  return total == null ? head : `${head} · ${total} in all`;
}
