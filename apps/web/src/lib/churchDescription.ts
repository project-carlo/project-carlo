/**
 * The search-result description of a church page: its weekly times, when
 * they fit, rather than a sentence promising them.
 *
 * Google shows a page's meta description only when it answers the search;
 * otherwise it quotes the page itself. A search for a church's Mass times
 * is answered by the times, so the description leads with them, and since
 * no two churches share a schedule, no two pages share a description.
 * Lives apart from seo.ts, which may import only types from @carlo/core.
 */
import {
  type ChurchDetail,
  type ContinuousAdoration,
  continuousTimes,
  DAY_ORDER,
  dateMatchesPattern,
  EVENT_TYPE_LABELS,
  EVENT_TYPE_ORDER,
  type EventSummary,
  type EventType,
  formatTimeRange,
  jsDayFor,
  titleCase,
  VIGIL_START_MINUTES,
} from "@carlo/core";
import { SOURCE_NAMES } from "../copy";
import { churchLocation } from "./seo";

/** Past this, Google cuts the description off with an ellipsis. */
export const DESCRIPTION_MAX_LENGTH = 160;

const SUNDAY = 0;
const SATURDAY = 6;
const DAYS_IN_WEEK = 7;

const ON_THE_CLOCK = /^(\d+(?::\d+)?) ([ap]\.m\.)$/;
const RANGE = /^(\d+(?::\d+)?) ([ap]\.m\.) – (\d+(?::\d+)?) ([ap]\.m\.)$/;

/** "12 – 4 p.m." for "12 p.m. – 4 p.m.": a range drops its first meridiem when both share it. */
function shortRange(time: string): string {
  const range = RANGE.exec(time);
  return range && range[2] === range[4] ? `${range[1]} – ${range[3]} ${range[4]}` : time;
}

/** "9 a.m., 12 & 5 p.m.": a start time drops its meridiem when the next one shares it. */
function joinTimes(times: string[]): string {
  const short = times.map((time, i) => {
    const here = ON_THE_CLOCK.exec(time);
    const next = ON_THE_CLOCK.exec(times[i + 1] ?? "");
    return here && next && here[2] === next[2] ? here[1] : shortRange(time);
  });
  return joinList(short);
}

/** "a", "a & b", "a, b & c". */
function joinList(items: string[]): string {
  if (items.length <= 1) return items.join("");
  return `${items.slice(0, -1).join(", ")} & ${items[items.length - 1]}`;
}

/** "Mon" for 1, Sunday-first like DAY_ORDER. */
function dayAbbr(day: number): string {
  return titleCase(DAY_ORDER[day]).slice(0, 3);
}

/**
 * "Mon – Fri", "Tue & Thu", "Mon – Wed & Fri": three days or more in a row
 * as a span. All seven are "every day".
 */
function dayLabel(days: number[]): string {
  if (days.length === DAYS_IN_WEEK) return "every day";
  const parts: string[] = [];
  for (let i = 0; i < days.length; ) {
    let j = i;
    while (j + 1 < days.length && days[j + 1] === days[j] + 1) j++;
    if (j - i >= 2) parts.push(`${dayAbbr(days[i])} – ${dayAbbr(days[j])}`);
    else for (let k = i; k <= j; k++) parts.push(dayAbbr(days[k]));
    i = j + 1;
  }
  return joinList(parts);
}

/** One day's slots as one entry's times: "9 a.m., 12 & 5 p.m.". */
function slotTimes(slots: EventSummary[]): string {
  const sorted = [...slots].sort(
    (a, b) => a.start_time - b.start_time || (a.end_time ?? -1) - (b.end_time ?? -1),
  );
  return joinTimes([...new Set(sorted.map((e) => formatTimeRange(e.start_time, e.end_time)))]);
}

/**
 * Whether the slot is a weekly time in effect on `today`. One kept only on
 * certain weeks of the month is on the page with its note, too long to carry
 * here; one in another season, or not yet begun or already ended, isn't the
 * church's time now. A dated or seasonal slot in effect today is, with no
 * qualifier: the pages are rebuilt each day.
 */
function inEffect(event: EventSummary, today: Date): boolean {
  return (
    event.kind === "weekly" &&
    !event.cancelled &&
    event.weeks_of_month.length === 0 &&
    dateMatchesPattern(today, event)
  );
}

interface Runs {
  /** "Sat 4 p.m.", "Sun 9 a.m. & 5 p.m.", "Mon – Fri 8 a.m.", ... */
  runs: string[];
  /** How many of `runs`, from the first, are the weekend's Masses. */
  weekend: number;
}

/**
 * The service's times in effect, the days that share them together:
 * "Sun 9 a.m., 12 & 5 p.m.", "Tue & Thu 8 a.m.". Mass leads with the
 * weekend, the Saturday vigil and then Sunday, as the times most searched
 * for, each alone; a Saturday morning Mass goes with the weekdays.
 */
function weeklyRuns(events: EventSummary[], type: EventType, today: Date): Runs {
  const isMass = type === "mass";
  const slotsByDay = new Map<number, EventSummary[]>();
  const vigil: EventSummary[] = [];
  for (const event of events) {
    if (event.type !== type || !inEffect(event, today)) continue;
    const day = jsDayFor(event.day_of_week ?? "");
    if (day < 0) continue;
    if (isMass && day === SATURDAY && event.start_time >= VIGIL_START_MINUTES) {
      vigil.push(event);
    } else {
      slotsByDay.set(day, [...(slotsByDay.get(day) ?? []), event]);
    }
  }

  const weekend: string[] = [];
  if (isMass) {
    if (vigil.length > 0) weekend.push(`Sat ${slotTimes(vigil)}`);
    const sunday = slotsByDay.get(SUNDAY);
    if (sunday) weekend.push(`Sun ${slotTimes(sunday)}`);
    slotsByDay.delete(SUNDAY);
  }

  const byTimes = new Map<string, number[]>();
  for (const day of [...slotsByDay.keys()].sort((a, b) => a - b)) {
    const times = slotTimes(slotsByDay.get(day)!);
    byTimes.set(times, [...(byTimes.get(times) ?? []), day]);
  }
  const rest = [...byTimes].map(([times, days]) => `${dayLabel(days)} ${times}`);
  return { runs: [...weekend, ...rest], weekend: weekend.length };
}

/** A sentence's text with its stop: "a.m." and "p.m." already end in one. */
function sentence(text: string): string {
  return text.endsWith(".") ? text : `${text}.`;
}

interface Service extends Runs {
  type: EventType;
}

/**
 * Each service in order, its times listed or only named, then the church:
 * "Mass: Sat 4 p.m.; Sun 9 a.m.; Mon – Fri 8 a.m. Confession & Adoration
 * times for St. Mary in East Aurora, NY."
 */
function compose(
  services: Service[],
  listed: (service: Service) => string[] | null,
  who: string,
): string {
  const parts: string[] = [];
  const named: string[] = [];
  for (const service of services) {
    const runs = listed(service);
    if (runs && runs.length > 0) {
      parts.push(sentence(`${EVENT_TYPE_LABELS[service.type]}: ${runs.join("; ")}`));
    } else {
      named.push(EVENT_TYPE_LABELS[service.type]);
    }
  }
  parts.push(
    named.length > 0
      ? `${joinList(named)} times for ${who}.`
      : `Weekly times for ${who}.`,
  );
  return parts.join(" ");
}

/** The description before times were known, or for a church with none in effect. */
function genericDescription(church: ChurchDetail, who: string): string {
  const from = church.schedule_source
    ? SOURCE_NAMES[church.schedule_source]
    : "the parish’s weekly bulletin";
  const services =
    church.kind === "adoration_chapel"
      ? "Adoration times"
      : "Mass, Confession, and Adoration times";
  return `${services} for ${who}, from ${from}.`;
}

/**
 * SERP-snippet description for a church page, kept under
 * DESCRIPTION_MAX_LENGTH. Lists the church's weekly times in effect on
 * `today`, Mass first. When they don't all fit, the town is dropped; then
 * Adoration is only named, then Confession instead, then both; then the Mass
 * times are cut to the weekend's.
 */
export function buildChurchDescription(
  church: ChurchDetail,
  events: EventSummary[] = [],
  continuous: ContinuousAdoration | null = null,
  today: Date = new Date(),
): string {
  const name = church.name?.trim() || "this church";
  const loc = churchLocation(church);
  const where = loc ? `${name} in ${loc}` : name;

  const types: EventType[] =
    church.kind === "adoration_chapel" ? ["adoration"] : EVENT_TYPE_ORDER;
  // Each service the church has; one with no weekly times in effect is only named.
  const services: Service[] = types
    .filter(
      (type) =>
        events.some((e) => e.type === type && !e.cancelled) ||
        (type === "adoration" && continuous !== null),
    )
    .map((type) => {
      const { runs, weekend } = weeklyRuns(events, type, today);
      if (type === "adoration" && continuous) {
        runs.unshift(`every day, ${continuousTimes(continuous).toLowerCase()}`);
      }
      return { type, runs, weekend };
    });
  if (!services.some((s) => s.runs.length > 0)) {
    return genericDescription(church, where);
  }

  const lead = services[0];
  const weekend = lead.runs.slice(0, lead.weekend);
  // Most preferred first: every service listed, then fewer.
  const choices: ((service: Service) => string[] | null)[] = [
    (s) => s.runs,
    (s) => (s.type === "adoration" ? null : s.runs),
    (s) => (s.type === "confession" ? null : s.runs),
    (s) => (s === lead ? s.runs : null),
  ];
  if (weekend.length > 0 && weekend.length < lead.runs.length) {
    choices.push((s) => (s === lead ? weekend : null));
  }

  // The town goes before any times: the page's title names it too.
  for (const listed of choices) {
    for (const who of [where, name]) {
      const description = compose(services, listed, who);
      if (description.length <= DESCRIPTION_MAX_LENGTH) return description;
    }
  }
  return genericDescription(church, where);
}
