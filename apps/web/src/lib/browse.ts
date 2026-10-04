/**
 * Pure data builders for the browse pages: the diocese index, diocese pages,
 * the state hub and city pages, plus the "nearby churches" block on a church
 * page. The same functions feed the client routes (src/views/browse) and the
 * prerenderer (scripts/prerender.ts), so a static page and its live twin show
 * identical content. No DOM, no React, no router.
 *
 * Everything here is derived from the weekly schedule, never from "now": the
 * static pages are built once and served for days, so a "next Mass in 20
 * minutes" would be wrong most of the time they are read. Time-independent
 * summaries ("Sun 8, 10:30 a.m.") stay true until the next build.
 */
import { DAY_ORDER, jsDayFor, type WeekdayKey } from "../constants/days";
import type { ChurchBase, RawEvent } from "../types";
import { formatAddress } from "../utils";
import {
  CITY_PAGE_MIN_CHURCHES,
  DEFAULT_STATE,
  cityPath,
  churchPath,
  citySlug,
  dioceseKeyForChurch,
  dioceses,
  diocesePath,
  getDiocese,
  groupChurchesByCity,
  haversineMiles,
  nearestChurches,
  statePath,
  type CityGroup,
  type Diocese,
} from "./places";

export type DayKey = WeekdayKey;

/** A Saturday Mass starting at or after this is the vigil for Sunday. */
export const VIGIL_START_MINUTES = 16 * 60;

/** "Nearby, outside {city}" radius from the city's centroid. */
export const NEARBY_CITY_MILES = 10;
export const NEARBY_CITY_MAX = 12;
export const NEARBY_CHURCH_COUNT = 5;

// ----------------------------------------------------------------- times

export interface TimeSlot {
  start: number;
  end: number | null;
}

type PerDay<T> = Record<DayKey, T[]>;

/** A church's recurring weekly schedule, deduplicated and sorted. */
export interface ChurchTimes {
  mass: PerDay<number>;
  confession: PerDay<TimeSlot>;
  adoration: PerDay<TimeSlot>;
}

/** One church plus its weekly schedule: the unit every page builder takes. */
export interface BrowseEntry {
  church: ChurchBase;
  times: ChurchTimes;
}

function emptyPerDay<T>(): PerDay<T> {
  return {
    sunday: [],
    monday: [],
    tuesday: [],
    wednesday: [],
    thursday: [],
    friday: [],
    saturday: [],
  };
}

type WeeklyEvent = Pick<
  RawEvent,
  | "event_type"
  | "event_kind"
  | "day_of_week"
  | "start_time"
  | "end_time"
  | "cancelled"
>;

/** Fold a church's events into its weekly schedule. Specific-date events and
 *  cancelled ones are left out: they are not part of the standing schedule. */
export function buildChurchTimes(events: WeeklyEvent[]): ChurchTimes {
  const times: ChurchTimes = {
    mass: emptyPerDay(),
    confession: emptyPerDay(),
    adoration: emptyPerDay(),
  };
  for (const e of events) {
    if (e.cancelled || e.event_kind !== "weekly" || !e.day_of_week) continue;
    const jsDay = jsDayFor(e.day_of_week);
    if (jsDay < 0) continue;
    const day = DAY_ORDER[jsDay];
    if (e.event_type === "mass") {
      if (!times.mass[day].includes(e.start_time)) times.mass[day].push(e.start_time);
    } else {
      const list = times[e.event_type][day];
      if (!list.some((s) => s.start === e.start_time && s.end === e.end_time)) {
        list.push({ start: e.start_time, end: e.end_time });
      }
    }
  }
  for (const day of DAY_ORDER) {
    times.mass[day].sort((a, b) => a - b);
    times.confession[day].sort((a, b) => a.start - b.start);
    times.adoration[day].sort((a, b) => a.start - b.start);
  }
  return times;
}

/** Entries for a set of churches, given a lookup of each church's events. */
export function buildBrowseEntries(
  churches: ChurchBase[],
  eventsOf: (churchId: number) => WeeklyEvent[],
): BrowseEntry[] {
  return churches.map((church) => ({
    church,
    times: buildChurchTimes(eventsOf(church.id)),
  }));
}

export function vigilTimes(times: ChurchTimes): number[] {
  return times.mass.saturday.filter((m) => m >= VIGIL_START_MINUTES);
}

export function sundayTimes(times: ChurchTimes): number[] {
  return times.mass.sunday;
}

const WEEKDAY_MASS_DAYS: DayKey[] = [
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
];

/** Weekday Mass days (Mon–Sat morning) and their times. */
function weekdayMass(times: ChurchTimes): Map<DayKey, number[]> {
  const out = new Map<DayKey, number[]>();
  for (const day of [...WEEKDAY_MASS_DAYS, "saturday" as const]) {
    const list =
      day === "saturday"
        ? times.mass.saturday.filter((m) => m < VIGIL_START_MINUTES)
        : times.mass[day];
    if (list.length > 0) out.set(day, list);
  }
  return out;
}

/** Mass on all five weekdays, Monday through Friday. */
export function hasDailyMass(times: ChurchTimes): boolean {
  return WEEKDAY_MASS_DAYS.every((d) => times.mass[d].length > 0);
}

function meridiem(minutes: number): "a.m." | "p.m." {
  return Math.floor(minutes / 60) < 12 ? "a.m." : "p.m.";
}

function clock(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  const displayH = h === 0 ? 12 : h > 12 ? h - 12 : h;
  return m === 0 ? `${displayH}` : `${displayH}:${m.toString().padStart(2, "0")}`;
}

/** One time with its meridiem: "8 a.m.", "10:30 a.m.". */
export function formatTime(minutes: number): string {
  return `${clock(minutes)} ${meridiem(minutes)}`;
}

/**
 * Compact list of times: "8, 10:30 a.m., 5 p.m." — the meridiem is dropped
 * from a time when the next one shares it, so a long Sunday reads in one line.
 */
export function formatTimeList(minutes: number[]): string {
  const sorted = [...new Set(minutes)].sort((a, b) => a - b);
  return sorted
    .map((m, i) => {
      const next = sorted[i + 1];
      return next !== undefined && meridiem(next) === meridiem(m)
        ? clock(m)
        : formatTime(m);
    })
    .join(", ");
}

/** A time range: "3–4 p.m." or "11:30 a.m.–12:30 p.m."; a lone start is a time. */
export function formatSlot(slot: TimeSlot): string {
  if (slot.end == null || slot.end === slot.start) return formatTime(slot.start);
  if (meridiem(slot.start) === meridiem(slot.end)) {
    return `${clock(slot.start)}–${formatTime(slot.end)}`;
  }
  return `${formatTime(slot.start)}–${formatTime(slot.end)}`;
}

const DAY_ABBR: Record<DayKey, string> = {
  sunday: "Sun",
  monday: "Mon",
  tuesday: "Tue",
  wednesday: "Wed",
  thursday: "Thu",
  friday: "Fri",
  saturday: "Sat",
};

export function dayAbbr(day: DayKey): string {
  return DAY_ABBR[day];
}

export function dayPlural(day: DayKey): string {
  return `${day.charAt(0).toUpperCase()}${day.slice(1)}s`;
}

function formatDayRun(days: DayKey[]): string {
  // `days` are in Monday-first order and may have gaps: split into runs.
  const order = [...WEEKDAY_MASS_DAYS, "saturday" as const];
  const runs: DayKey[][] = [];
  for (const day of days) {
    const last = runs[runs.length - 1];
    if (last && order.indexOf(last[last.length - 1]) + 1 === order.indexOf(day)) {
      last.push(day);
    } else {
      runs.push([day]);
    }
  }
  return runs
    .map((run) => {
      if (run.length === 1) return DAY_ABBR[run[0]];
      if (run.length === 2) return `${DAY_ABBR[run[0]]} & ${DAY_ABBR[run[1]]}`;
      return `${DAY_ABBR[run[0]]}–${DAY_ABBR[run[run.length - 1]]}`;
    })
    .join(", ");
}

/**
 * Weekday Mass in one line: "Mon–Fri 8 a.m.; Wed 7 p.m." Days that share the
 * same times are folded together. Empty string when there is no weekday Mass.
 */
export function weekdayMassSummary(times: ChurchTimes): string {
  const byLabel = new Map<string, DayKey[]>();
  for (const [day, list] of weekdayMass(times)) {
    const label = formatTimeList(list);
    const days = byLabel.get(label);
    if (days) days.push(day);
    else byLabel.set(label, [day]);
  }
  return [...byLabel.entries()]
    .sort((a, b) => mondayFirstIndex(a[1][0]) - mondayFirstIndex(b[1][0]))
    .map(([label, days]) => `${formatDayRun(days)} ${label}`)
    .join("; ");
}

function mondayFirstIndex(day: DayKey): number {
  // Monday-first ordering for the weekday summary.
  return (DAY_ORDER.indexOf(day) + 6) % 7;
}

/** "Sat 4 p.m. · Sun 8, 10:30 a.m." — the weekend at a glance. */
export function weekendLine(times: ChurchTimes): string {
  const parts: string[] = [];
  const vigil = vigilTimes(times);
  if (vigil.length > 0) parts.push(`Sat ${formatTimeList(vigil)}`);
  if (times.mass.sunday.length > 0) {
    parts.push(`Sun ${formatTimeList(times.mass.sunday)}`);
  }
  return parts.join(" · ");
}

// ------------------------------------------------------------ highlights

export interface Highlight {
  id: string;
  /** Small-caps label, e.g. "Earliest Sunday Mass". */
  label: string;
  /** The headline figure, e.g. "7 a.m." or "12". */
  value: string;
  /** Qualifier under the figure, e.g. "at St. Mary's". */
  detail?: string;
  /** The church the figure belongs to, when there is a single one. */
  church?: { slug: string; name: string };
}

export interface PlaceStats {
  churchCount: number;
  townCount: number;
  withMass: number;
  withVigil: number;
  withDailyMass: number;
  withConfession: number;
  withSaturdayConfession: number;
  withAdoration: number;
  sundayMassCount: number;
  earliestSunday: { minutes: number; churches: ChurchBase[] } | null;
  latestSunday: { minutes: number; churches: ChurchBase[] } | null;
  mostSunday: { count: number; churches: ChurchBase[] } | null;
}

function churchName(c: ChurchBase): string {
  return c.name?.trim() || "Unnamed parish";
}

function byName(a: ChurchBase, b: ChurchBase): number {
  return churchName(a).localeCompare(churchName(b));
}

function townKey(c: ChurchBase): string | null {
  const city = c.city?.trim();
  const state = c.state?.trim().toUpperCase();
  if (!city || !state) return null;
  const slug = citySlug(city);
  return slug ? `${state}/${slug}` : null;
}

export function computeStats(entries: BrowseEntry[]): PlaceStats {
  const stats: PlaceStats = {
    churchCount: entries.length,
    townCount: new Set(entries.map((e) => townKey(e.church)).filter(Boolean)).size,
    withMass: 0,
    withVigil: 0,
    withDailyMass: 0,
    withConfession: 0,
    withSaturdayConfession: 0,
    withAdoration: 0,
    sundayMassCount: 0,
    earliestSunday: null,
    latestSunday: null,
    mostSunday: null,
  };
  for (const { church, times } of entries) {
    const sunday = sundayTimes(times);
    const vigil = vigilTimes(times);
    if (sunday.length > 0 || vigil.length > 0 || weekdayMass(times).size > 0) {
      stats.withMass++;
    }
    if (vigil.length > 0) stats.withVigil++;
    if (hasDailyMass(times)) stats.withDailyMass++;
    if (DAY_ORDER.some((d) => times.confession[d].length > 0)) stats.withConfession++;
    if (times.confession.saturday.length > 0) stats.withSaturdayConfession++;
    if (DAY_ORDER.some((d) => times.adoration[d].length > 0)) stats.withAdoration++;

    stats.sundayMassCount += sunday.length;
    if (sunday.length > 0) {
      const first = sunday[0];
      const last = sunday[sunday.length - 1];
      if (!stats.earliestSunday || first < stats.earliestSunday.minutes) {
        stats.earliestSunday = { minutes: first, churches: [church] };
      } else if (first === stats.earliestSunday.minutes) {
        stats.earliestSunday.churches.push(church);
      }
      if (!stats.latestSunday || last > stats.latestSunday.minutes) {
        stats.latestSunday = { minutes: last, churches: [church] };
      } else if (last === stats.latestSunday.minutes) {
        stats.latestSunday.churches.push(church);
      }
      if (!stats.mostSunday || sunday.length > stats.mostSunday.count) {
        stats.mostSunday = { count: sunday.length, churches: [church] };
      } else if (sunday.length === stats.mostSunday.count) {
        stats.mostSunday.churches.push(church);
      }
    }
  }
  for (const slot of [stats.earliestSunday, stats.latestSunday, stats.mostSunday]) {
    slot?.churches.sort(byName);
  }
  return stats;
}

function plural(n: number, one: string, many = `${one}s`): string {
  return `${n} ${n === 1 ? one : many}`;
}

function holder(churches: ChurchBase[]): {
  church?: { slug: string; name: string };
  detail: string;
} {
  const first = churches[0];
  const others = churches.length - 1;
  const name = churchName(first);
  return {
    church: { slug: first.slug, name },
    detail: others === 0 ? `at ${name}` : `at ${name} and ${plural(others, "other")}`,
  };
}

/** The data-driven headline figures shown on every place page. */
export function buildHighlights(stats: PlaceStats): Highlight[] {
  const out: Highlight[] = [];
  if (stats.earliestSunday) {
    const h = holder(stats.earliestSunday.churches);
    out.push({
      id: "earliest-sunday",
      label: "Earliest Sunday Mass",
      value: formatTime(stats.earliestSunday.minutes),
      detail: h.detail,
      church: h.church,
    });
  }
  if (stats.latestSunday) {
    const h = holder(stats.latestSunday.churches);
    out.push({
      id: "latest-sunday",
      label: "Latest Sunday Mass",
      value: formatTime(stats.latestSunday.minutes),
      detail: h.detail,
      church: h.church,
    });
  }
  if (stats.mostSunday && stats.mostSunday.count > 1) {
    const h = holder(stats.mostSunday.churches);
    out.push({
      id: "most-sunday",
      label: "Most Sunday Masses",
      value: String(stats.mostSunday.count),
      detail: h.detail,
      church: h.church,
    });
  }
  if (stats.withVigil > 0) {
    out.push({
      id: "vigil",
      label: "Saturday vigil Mass",
      value: String(stats.withVigil),
      detail: `${stats.withVigil === 1 ? "church" : "churches"} with an evening Mass`,
    });
  }
  if (stats.withDailyMass > 0) {
    out.push({
      id: "daily-mass",
      label: "Daily Mass",
      value: String(stats.withDailyMass),
      detail: `${stats.withDailyMass === 1 ? "church" : "churches"} with Mass Monday to Friday`,
    });
  }
  if (stats.withSaturdayConfession > 0) {
    out.push({
      id: "saturday-confession",
      label: "Confession on Saturdays",
      value: String(stats.withSaturdayConfession),
      detail: `${stats.withSaturdayConfession === 1 ? "church" : "churches"}${
        stats.withConfession > stats.withSaturdayConfession
          ? `, of ${stats.withConfession} with Confession`
          : ""
      }`,
    });
  } else if (stats.withConfession > 0) {
    out.push({
      id: "confession",
      label: "Confession",
      value: String(stats.withConfession),
      detail: stats.withConfession === 1 ? "church lists times" : "churches list times",
    });
  }
  if (stats.withAdoration > 0) {
    out.push({
      id: "adoration",
      label: "Eucharistic Adoration",
      value: String(stats.withAdoration),
      detail: stats.withAdoration === 1 ? "church lists times" : "churches list times",
    });
  }
  return out;
}

/** One data-driven paragraph for the top of a place page. */
export function buildIntro(
  subject: string,
  stats: PlaceStats,
  opts: { townNoun?: boolean } = {},
): string {
  const parts: string[] = [];
  parts.push(
    `${subject} has ${plural(
      stats.churchCount,
      "Catholic church",
      "Catholic churches",
    )}${opts.townNoun ? ` across ${plural(stats.townCount, "town")}` : ""} in this directory.`,
  );
  const extras: string[] = [];
  if (stats.withVigil > 0) extras.push(`${stats.withVigil} offer a Saturday vigil`);
  if (stats.withDailyMass > 0) extras.push(`${stats.withDailyMass} have daily Mass`);
  if (stats.withConfession > 0) extras.push(`${stats.withConfession} list Confession`);
  if (extras.length > 0) parts.push(`Of them, ${joinList(extras)}.`);
  if (stats.earliestSunday && stats.latestSunday) {
    const e = formatTime(stats.earliestSunday.minutes);
    const l = formatTime(stats.latestSunday.minutes);
    parts.push(
      e === l
        ? `Sunday Mass is at ${e}.`
        : `Sunday Masses run from ${e} to ${l}.`,
    );
  }
  // "...to 6:30 p.m." + "." must not become "p.m..".
  return parts.join(" ").replace(/\.\.(?=\s|$)/g, ".");
}

function joinList(items: string[]): string {
  if (items.length <= 1) return items.join("");
  if (items.length === 2) return `${items[0]} and ${items[1]}`;
  return `${items.slice(0, -1).join(", ")}, and ${items[items.length - 1]}`;
}

// ------------------------------------------------- services, by day

export interface ServiceRow {
  church: ChurchBase;
  slot: TimeSlot;
}

export interface ServiceDay {
  day: DayKey;
  /** "Saturdays" */
  label: string;
  churchCount: number;
  rows: ServiceRow[];
}

/** Every Confession (or Adoration) slot across the entries, grouped by weekday. */
export function serviceByDay(
  entries: BrowseEntry[],
  type: "confession" | "adoration",
): ServiceDay[] {
  const out: ServiceDay[] = [];
  for (const day of DAY_ORDER) {
    const rows: ServiceRow[] = [];
    for (const { church, times } of entries) {
      for (const slot of times[type][day]) rows.push({ church, slot });
    }
    if (rows.length === 0) continue;
    rows.sort(
      (a, b) =>
        a.slot.start - b.slot.start ||
        (a.slot.end ?? 0) - (b.slot.end ?? 0) ||
        byName(a.church, b.church),
    );
    out.push({
      day,
      label: dayPlural(day),
      churchCount: new Set(rows.map((r) => r.church.id)).size,
      rows,
    });
  }
  return out;
}

// -------------------------------------------------------- weekend table

export interface WeekendRow {
  church: ChurchBase;
  vigil: string;
  sunday: string;
  weekdays: string;
}

/** The "This weekend" table: churches in town/name order with compact times. */
export function weekendRows(entries: BrowseEntry[]): WeekendRow[] {
  return [...entries]
    .sort(
      (a, b) =>
        (a.church.city ?? "").localeCompare(b.church.city ?? "") ||
        byName(a.church, b.church),
    )
    .map(({ church, times }) => ({
      church,
      vigil: formatTimeList(vigilTimes(times)),
      sunday: formatTimeList(sundayTimes(times)),
      weekdays: weekdayMassSummary(times),
    }));
}

// --------------------------------------------------------- list helpers

export interface ChurchListItem {
  church: ChurchBase;
  name: string;
  path: string;
  address: string | null;
  weekend: string;
  /** "Confession Sat · Adoration Fri" style extras. */
  extras: string;
}

function serviceDays(times: ChurchTimes, type: "confession" | "adoration"): string {
  const days = DAY_ORDER.filter((d) => times[type][d].length > 0);
  if (days.length === 0) return "";
  if (days.length === 7) return "daily";
  return days.map((d) => DAY_ABBR[d]).join(", ");
}

export function churchListItem(entry: BrowseEntry): ChurchListItem {
  const { church, times } = entry;
  const extras: string[] = [];
  const conf = serviceDays(times, "confession");
  if (conf) extras.push(`Confession ${conf}`);
  const adore = serviceDays(times, "adoration");
  if (adore) extras.push(`Adoration ${adore}`);
  return {
    church,
    name: churchName(church),
    path: churchPath(church.slug),
    address: formatAddress(church),
    weekend: weekendLine(times) || weekdayMassSummary(times),
    extras: extras.join(" · "),
  };
}

// ------------------------------------------------------------- the index

/** Everything the page builders look churches and cities up in. */
export interface PlaceIndex {
  entries: BrowseEntry[];
  /** `STATE/slug` → how many churches the town has. */
  townCounts: Map<string, number>;
}

export function createPlaceIndex(entries: BrowseEntry[]): PlaceIndex {
  const townCounts = new Map<string, number>();
  for (const { church } of entries) {
    const key = townKey(church);
    if (key) townCounts.set(key, (townCounts.get(key) ?? 0) + 1);
  }
  return { entries, townCounts };
}

/** Whether a town has its own `/mass-times/{state}/{city}/` page. */
export function indexCityHasPage(index: PlaceIndex, church: ChurchBase): boolean {
  const key = townKey(church);
  return key !== null && (index.townCounts.get(key) ?? 0) >= CITY_PAGE_MIN_CHURCHES;
}

// ---------------------------------------------------------- page models

export interface Crumb {
  name: string;
  /** Site-relative path; the last crumb is the current page. */
  path: string;
}

export interface PageSeo {
  /** Site-relative canonical path. */
  path: string;
  title: string;
  description: string;
  crumbs: Crumb[];
  /** Links the page's ItemList JSON-LD points at. */
  items: { name: string; path: string }[];
}

const STATE_NAMES: Record<string, string> = { NY: "New York" };

export function stateName(state: string): string {
  return STATE_NAMES[state.toUpperCase()] ?? state.toUpperCase();
}

export const SITE_SHORT = "Project Carlo";

/**
 * A meta description: the base sentence, then as many of the data-driven
 * `facts` as fit under ~158 characters (cut whole facts, never mid-word).
 */
function buildDescription(base: string, facts: string[], max = 158): string {
  let out = base;
  const kept: string[] = [];
  for (const fact of facts) {
    const next = `${base} ${[...kept, fact].join("; ")}.`;
    if (next.length > max) break;
    kept.push(fact);
    out = next;
  }
  return out;
}

function seoFacts(stats: PlaceStats): string[] {
  const facts: string[] = [];
  if (stats.earliestSunday && stats.latestSunday) {
    const e = formatTime(stats.earliestSunday.minutes);
    const l = formatTime(stats.latestSunday.minutes);
    facts.push(e === l ? `Sunday Mass at ${e}` : `Sunday Mass ${e}–${l}`);
  }
  if (stats.withSaturdayConfession > 0) {
    facts.push(`Saturday Confession at ${stats.withSaturdayConfession}`);
  } else if (stats.withConfession > 0) {
    facts.push(`Confession at ${stats.withConfession}`);
  }
  if (stats.withAdoration > 0) facts.push(`Adoration at ${stats.withAdoration}`);
  return facts;
}

export interface PlaceSection {
  stats: PlaceStats;
  highlights: Highlight[];
  intro: string;
  /** Churches in town/name order, for the weekend table and lists. */
  entries: BrowseEntry[];
}

function placeSection(
  entries: BrowseEntry[],
  subject: string,
  townNoun: boolean,
): PlaceSection {
  const stats = computeStats(entries);
  return {
    stats,
    highlights: buildHighlights(stats),
    intro: buildIntro(subject, stats, { townNoun }),
    entries,
  };
}

// ---- diocese index

export interface DioceseCard {
  diocese: Diocese;
  path: string;
  churchCount: number;
  townCount: number;
  /** Largest towns, for a taste of the diocese. */
  topTowns: { city: string; path: string; count: number }[];
}

export interface DioceseIndexModel extends PageSeo {
  kind: "dioceses";
  cards: DioceseCard[];
  churchCount: number;
}

export function entriesInDiocese(entries: BrowseEntry[], key: string): BrowseEntry[] {
  return entries.filter((e) => dioceseKeyForChurch(e.church.slug) === key);
}

export function buildDioceseIndex(index: PlaceIndex): DioceseIndexModel {
  const cards: DioceseCard[] = dioceses()
    .map((diocese) => {
      const entries = entriesInDiocese(index.entries, diocese.key);
      const groups = groupChurchesByCity(entries.map((e) => e.church));
      return {
        diocese,
        path: diocesePath(diocese.key),
        churchCount: entries.length,
        townCount: groups.length,
        topTowns: groups
          .filter((g) => g.churches.length >= CITY_PAGE_MIN_CHURCHES)
          .sort((a, b) => b.churches.length - a.churches.length || a.city.localeCompare(b.city))
          .slice(0, 4)
          .map((g) => ({ city: g.city, path: g.path, count: g.churches.length })),
      };
    })
    .filter((c) => c.churchCount > 0)
    .sort((a, b) => b.churchCount - a.churchCount || a.diocese.shortName.localeCompare(b.diocese.shortName));
  const churchCount = cards.reduce((n, c) => n + c.churchCount, 0);
  return {
    kind: "dioceses",
    path: "/dioceses/",
    title: `Catholic Dioceses in New York State · Mass Times by Diocese | ${SITE_SHORT}`,
    description: buildDescription(
      `Browse ${churchCount} Catholic churches by diocese: ${joinList(
        cards.map((c) => c.diocese.shortName),
      )}.`,
      ["Mass, Confession and Adoration times from each parish bulletin"],
    ),
    crumbs: [
      { name: "Home", path: "/" },
      { name: "Dioceses", path: "/dioceses/" },
    ],
    items: cards.map((c) => ({ name: c.diocese.shortName, path: c.path })),
    cards,
    churchCount,
  };
}

// ---- diocese page

export interface TownBlock {
  city: string;
  slug: string;
  /** City page path when the town has one, else null. */
  cityPagePath: string | null;
  items: ChurchListItem[];
}

export interface DioceseModel extends PageSeo, PlaceSection {
  kind: "diocese";
  diocese: Diocese;
  towns: TownBlock[];
}

export function townBlocks(entries: BrowseEntry[]): TownBlock[] {
  const byId = new Map(entries.map((e) => [e.church.id, e]));
  return groupChurchesByCity(entries.map((e) => e.church)).map((group) => ({
    city: group.city,
    slug: group.slug,
    cityPagePath: group.churches.length >= CITY_PAGE_MIN_CHURCHES ? group.path : null,
    items: [...group.churches]
      .sort(byName)
      .map((c) => churchListItem(byId.get(c.id)!)),
  }));
}

export function buildDioceseModel(index: PlaceIndex, key: string): DioceseModel | null {
  const diocese = getDiocese(key);
  if (!diocese) return null;
  const entries = entriesInDiocese(index.entries, key).sort(
    (a, b) =>
      (a.church.city ?? "").localeCompare(b.church.city ?? "") || byName(a.church, b.church),
  );
  if (entries.length === 0) return null;
  const section = placeSection(entries, diocese.shortName, true);
  const facts = seoFacts(section.stats);
  return {
    kind: "diocese",
    diocese,
    ...section,
    towns: townBlocks(entries),
    path: diocesePath(key),
    title: `${diocese.shortName}: Mass & Confession Times at ${section.stats.churchCount} Churches | ${SITE_SHORT}`,
    description: buildDescription(
      `Mass, Confession and Adoration times at ${plural(
        section.stats.churchCount,
        "Catholic church",
        "Catholic churches",
      )} in ${plural(section.stats.townCount, "town")} of the ${diocese.shortName}.`,
      facts,
    ),
    crumbs: [
      { name: "Home", path: "/" },
      { name: "Dioceses", path: "/dioceses/" },
      { name: diocese.shortName, path: diocesePath(key) },
    ],
    items: entries.map((e) => ({ name: churchName(e.church), path: churchPath(e.church.slug) })),
  };
}

// ---- state hub

export interface TownLink {
  city: string;
  slug: string;
  count: number;
  /** City page for towns with several churches, else the only church's page. */
  path: string;
  /** For single-church towns, that church's name. */
  churchName: string | null;
}

export interface CityPageLink {
  city: string;
  path: string;
  count: number;
}

export interface StateModel extends PageSeo, PlaceSection {
  kind: "state";
  state: string;
  stateName: string;
  dioceseCards: DioceseCard[];
  cityPages: CityPageLink[];
  towns: TownLink[];
}

export function townLinks(entries: BrowseEntry[]): TownLink[] {
  return groupChurchesByCity(entries.map((e) => e.church)).map((g) => ({
    city: g.city,
    slug: g.slug,
    count: g.churches.length,
    path:
      g.churches.length >= CITY_PAGE_MIN_CHURCHES
        ? g.path
        : churchPath(g.churches[0].slug),
    churchName: g.churches.length >= CITY_PAGE_MIN_CHURCHES ? null : churchName(g.churches[0]),
  }));
}

/** States that have any churches, as upper-case codes. */
export function statesIn(index: PlaceIndex): string[] {
  return [
    ...new Set(
      index.entries
        .map((e) => e.church.state?.trim().toUpperCase())
        .filter((s): s is string => Boolean(s)),
    ),
  ].sort();
}

export function buildStateModel(index: PlaceIndex, stateCode: string): StateModel | null {
  const state = stateCode.trim().toUpperCase();
  const entries = index.entries.filter((e) => e.church.state?.trim().toUpperCase() === state);
  if (entries.length === 0) return null;
  const name = stateName(state);
  const section = placeSection(entries, name, true);
  const towns = townLinks(entries);
  const cityPages = towns
    .filter((t) => t.count >= CITY_PAGE_MIN_CHURCHES)
    .map((t) => ({ city: t.city, path: t.path, count: t.count }))
    .sort((a, b) => b.count - a.count || a.city.localeCompare(b.city));
  const dioceseCards = buildDioceseIndex(createPlaceIndex(entries)).cards;
  const facts = seoFacts(section.stats);
  return {
    kind: "state",
    state,
    stateName: name,
    ...section,
    dioceseCards,
    cityPages,
    towns,
    path: statePath(state),
    title: `Catholic Mass & Confession Times in ${name} · ${section.stats.churchCount} Churches | ${SITE_SHORT}`,
    description: buildDescription(
      `Mass, Confession and Adoration times at ${section.stats.churchCount} Catholic churches in ${plural(
        section.stats.townCount,
        "town",
      )} across ${name}, by diocese and city.`,
      facts,
    ),
    crumbs: [
      { name: "Home", path: "/" },
      { name, path: statePath(state) },
    ],
    items: [
      ...dioceseCards.map((c) => ({ name: c.diocese.shortName, path: c.path })),
      ...cityPages.map((c) => ({ name: `${c.city}, ${state}`, path: c.path })),
    ],
  };
}

// ---- city page

export interface NearbyItem extends ChurchListItem {
  distanceMiles: number;
  distanceLabel: string;
}

export interface CityModel extends PageSeo, PlaceSection {
  kind: "city";
  state: string;
  stateName: string;
  city: string;
  slug: string;
  /** The city's churches as list rows, by name. */
  churches: ChurchListItem[];
  /** Churches near the city centre but outside it. */
  nearby: NearbyItem[];
}

export function formatDistance(miles: number): string {
  if (miles < 0.1) return "under 0.1 mi";
  return `${miles < 10 ? miles.toFixed(1) : Math.round(miles)} mi`;
}

function nearbyItem(entry: BrowseEntry, miles: number): NearbyItem {
  return {
    ...churchListItem(entry),
    distanceMiles: miles,
    distanceLabel: formatDistance(miles),
  };
}

/** Churches within `miles` of the group's centroid that are not in the group. */
export function nearbyOutsideCity(
  index: PlaceIndex,
  group: CityGroup<ChurchBase>,
  miles: number = NEARBY_CITY_MILES,
  max: number = NEARBY_CITY_MAX,
): NearbyItem[] {
  const located = group.churches.filter(
    (c) => c.latitude != null && c.longitude != null,
  );
  if (located.length === 0) return [];
  const centre = {
    lat: located.reduce((s, c) => s + c.latitude!, 0) / located.length,
    lng: located.reduce((s, c) => s + c.longitude!, 0) / located.length,
  };
  const inCity = new Set(group.churches.map((c) => c.id));
  const outside = index.entries.filter((e) => !inCity.has(e.church.id));
  const byId = new Map(outside.map((e) => [e.church.id, e]));
  return nearestChurches(
    outside.map((e) => e.church),
    centre,
    outside.length,
  )
    .filter((n) => n.distanceMiles <= miles)
    .slice(0, max)
    .map((n) => nearbyItem(byId.get(n.church.id)!, haversineMiles(centre, {
      lat: n.church.latitude!,
      lng: n.church.longitude!,
    })));
}

/** All cities that get a page, as (state, slug) with their churches. */
export function cityPageGroups(index: PlaceIndex): CityGroup<ChurchBase>[] {
  return groupChurchesByCity(index.entries.map((e) => e.church)).filter(
    (g) => g.churches.length >= CITY_PAGE_MIN_CHURCHES,
  );
}

export function buildCityModel(
  index: PlaceIndex,
  stateCode: string,
  slug: string,
): CityModel | null {
  const state = stateCode.trim().toUpperCase();
  const group = cityPageGroups(index).find(
    (g) => g.state === state && g.slug === slug,
  );
  if (!group) return null;
  const ids = new Set(group.churches.map((c) => c.id));
  const entries = index.entries
    .filter((e) => ids.has(e.church.id))
    .sort((a, b) => byName(a.church, b.church));
  const section = placeSection(entries, group.city, false);
  const facts = seoFacts(section.stats);
  const name = stateName(state);
  return {
    kind: "city",
    state,
    stateName: name,
    city: group.city,
    slug,
    ...section,
    path: cityPath(state, group.city),
    title: `Mass & Confession Times in ${group.city}, ${state} · ${section.stats.churchCount} Catholic Churches | ${SITE_SHORT}`,
    description: buildDescription(
      `Mass, Confession and Adoration times at ${section.stats.churchCount} Catholic churches in ${group.city}, ${state}.`,
      facts,
    ),
    crumbs: [
      { name: "Home", path: "/" },
      { name, path: statePath(state) },
      { name: group.city, path: cityPath(state, group.city) },
    ],
    items: entries.map((e) => ({ name: churchName(e.church), path: churchPath(e.church.slug) })),
    churches: entries.map(churchListItem),
    nearby: nearbyOutsideCity(index, group),
  };
}

// ----------------------------------------------------- church page extras

export interface ChurchPlaceContext {
  /** The church's own city page, when its town has one. */
  cityPage: { path: string; name: string } | null;
  /** The nearest other churches, closest first. */
  nearby: NearbyItem[];
}

/** City-page link and "Nearby churches" for one church's page. */
export function buildChurchPlaceContext(
  index: PlaceIndex,
  church: ChurchBase,
): ChurchPlaceContext {
  const city = church.city?.trim();
  const state = church.state?.trim().toUpperCase();
  const cityPage =
    city && state && indexCityHasPage(index, church)
      ? { path: cityPath(state, city), name: city }
      : null;

  let nearby: NearbyItem[] = [];
  if (church.latitude != null && church.longitude != null) {
    const byId = new Map(index.entries.map((e) => [e.church.id, e]));
    nearby = nearestChurches(
      index.entries.map((e) => e.church),
      { lat: church.latitude, lng: church.longitude },
      NEARBY_CHURCH_COUNT,
      church.id,
    ).map((n) => nearbyItem(byId.get(n.church.id)!, n.distanceMiles));
  }
  return { cityPage, nearby };
}

/** Breadcrumb trail for a church page: Home › State › City (if a page) › Church. */
export function churchCrumbs(
  church: ChurchBase,
  context: Pick<ChurchPlaceContext, "cityPage"> | null,
): Crumb[] {
  const state = (church.state ?? DEFAULT_STATE).trim().toUpperCase();
  const crumbs: Crumb[] = [
    { name: "Home", path: "/" },
    { name: stateName(state), path: statePath(state) },
  ];
  if (context?.cityPage) crumbs.push({ name: context.cityPage.name, path: context.cityPage.path });
  crumbs.push({ name: churchName(church), path: churchPath(church.slug) });
  return crumbs;
}

/** `/map?lat=..&lng=..&z=15`, centred on a church; null when it has no coordinates. */
export function mapLinkFor(church: ChurchBase, zoom = 15): string | null {
  if (church.latitude == null || church.longitude == null) return null;
  const round = (n: number) => Math.round(n * 1e5) / 1e5;
  return `/map?lat=${round(church.latitude)}&lng=${round(church.longitude)}&z=${zoom}`;
}

/** Alphabet buckets for the A–Z town list. */
export function groupTownsByLetter(towns: TownLink[]): { letter: string; towns: TownLink[] }[] {
  const map = new Map<string, TownLink[]>();
  for (const town of [...towns].sort((a, b) => a.city.localeCompare(b.city))) {
    const first = town.city.normalize("NFD").charAt(0).toUpperCase();
    const letter = /[A-Z]/.test(first) ? first : "#";
    const list = map.get(letter);
    if (list) list.push(town);
    else map.set(letter, [town]);
  }
  return [...map.entries()].map(([letter, list]) => ({ letter, towns: list }));
}
