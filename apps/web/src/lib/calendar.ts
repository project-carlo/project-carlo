import { jsDayFor } from "../constants/days";
import { EVENT_TYPE_LABELS } from "../constants/eventTypes";
import { UNNAMED_CHURCH } from "../copy";
import type { ChurchDetail, EventSummary } from "../types";
import { formatAddress, formatLongMonthDay } from "../utils";
import { SITE_NAME, churchPath } from "./seo";

/**
 * A church's schedule as an iCalendar file (RFC 5545), so a visitor can add
 * its times to their own calendar. scripts/prerender.ts writes one beside
 * each church page that lists times. Pure functions only.
 *
 * Times are floating (no time zone): the snapshot carries none, and a Mass at
 * 9 a.m. is at 9 a.m. on the church's wall clock, which is the visitor's
 * whenever they're there to attend it.
 */

/** The file's name beside a church page: `/churches/<slug>/schedule.ics`. */
export const CHURCH_CALENDAR_FILE = "schedule.ics";

/** Site path of a church's calendar file. */
export function churchCalendarPath(slug: string): string {
  return `${churchPath(slug)}${CHURCH_CALENDAR_FILE}`;
}

/**
 * How long a service without an end time lasts on the calendar. A guess, but
 * calendars draw zero-length events as slivers or drop them, so each gets one.
 */
const DEFAULT_DURATION_MINUTES = 60;

const BYDAY = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"] as const;

/** RFC 5545 caps content lines at 75 octets, excluding the CRLF. */
const MAX_LINE_OCTETS = 75;

const encoder = new TextEncoder();

interface CalendarOptions {
  /** Absolute URL of the church's page, linked from every event. */
  pageUrl: string;
  /** Host the event UIDs are scoped to, e.g. `projectcarlo.com`. */
  uidDomain: string;
  /** When the file is written; the DTSTAMP of every event. */
  now: Date;
  /** Local midnight of the day weekly events start recurring from. */
  today: Date;
}

/**
 * The church's events as a VCALENDAR: each weekly event recurring from its
 * first occurrence on or after `today`, each dated one once. Events with no
 * weekday or date to place them are left out, as `churchSchedule` already
 * leaves out cancelled and past ones.
 */
export function buildChurchCalendar(
  church: ChurchDetail,
  events: EventSummary[],
  options: CalendarOptions,
): string {
  const name = church.name?.trim() || UNNAMED_CHURCH;
  const lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    `PRODID:-//${SITE_NAME}//Church schedule//EN`,
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    `X-WR-CALNAME:${escapeText(name)}`,
    // Bulletins change weekly; a subscribed calendar picks up the new times.
    "REFRESH-INTERVAL;VALUE=DURATION:P1D",
    "X-PUBLISHED-TTL:P1D",
  ];

  const stamp = formatUtcStamp(options.now);
  const location = formatAddress(church);
  const source = church.bulletin_week
    ? `From the parish bulletin for the week of ${formatLongMonthDay(church.bulletin_week)}.`
    : "From the parish bulletin.";
  const usedUids = new Set<string>();

  for (const event of events) {
    const start = eventStart(event, options.today);
    if (!start) continue;

    const uid = uniqueUid(eventUid(church.slug, event, options.uidDomain), usedUids);
    const description = [
      event.note,
      `${source} Times can change, so check the bulletin before you go.`,
      options.pageUrl,
    ]
      .filter(Boolean)
      .join("\n");

    lines.push(
      "BEGIN:VEVENT",
      `UID:${uid}`,
      `DTSTAMP:${stamp}`,
      `DTSTART:${formatFloating(start, event.start_time)}`,
      `DTEND:${formatFloating(start, endMinutes(event))}`,
    );
    if (event.kind === "weekly") {
      lines.push(`RRULE:FREQ=WEEKLY;BYDAY=${BYDAY[start.getUTCDay()]}`);
    }
    lines.push(`SUMMARY:${escapeText(`${EVENT_TYPE_LABELS[event.type]} at ${name}`)}`);
    if (location) lines.push(`LOCATION:${escapeText(location)}`);
    lines.push(
      `DESCRIPTION:${escapeText(description)}`,
      `URL:${options.pageUrl}`,
      "END:VEVENT",
    );
  }

  lines.push("END:VCALENDAR");
  return lines.map(foldLine).join("\r\n") + "\r\n";
}

/**
 * The calendar day the event (first) falls on, as UTC midnight so the
 * arithmetic below never meets a DST shift; null if nothing places it.
 */
function eventStart(event: EventSummary, today: Date): Date | null {
  if (event.kind === "weekly") {
    const jsDay = event.day_of_week ? jsDayFor(event.day_of_week) : -1;
    if (jsDay < 0) return null;
    const base = Date.UTC(today.getFullYear(), today.getMonth(), today.getDate());
    const daysAhead = (jsDay - today.getDay() + 7) % 7;
    return new Date(base + daysAhead * 86_400_000);
  }
  const match = event.date ? /^(\d{4})-(\d{2})-(\d{2})$/.exec(event.date) : null;
  if (!match) return null;
  return new Date(Date.UTC(Number(match[1]), Number(match[2]) - 1, Number(match[3])));
}

/** Minutes after the start day's midnight the event ends; past midnight runs on. */
function endMinutes(event: EventSummary): number {
  if (event.end_time == null) return event.start_time + DEFAULT_DURATION_MINUTES;
  return event.end_time > event.start_time ? event.end_time : event.end_time + 24 * 60;
}

/**
 * Stable across builds, so re-importing or refreshing the file updates an
 * event rather than duplicating it. Snapshot row ids are not: they're
 * renumbered whenever the bulletin is processed again.
 */
function eventUid(slug: string, event: EventSummary, domain: string): string {
  const when = event.kind === "weekly" ? event.day_of_week?.toLowerCase() : event.date;
  return `${slug}-${event.type}-${when}-${event.start_time}@${domain}`;
}

function uniqueUid(uid: string, used: Set<string>): string {
  let candidate = uid;
  for (let n = 2; used.has(candidate); n++) candidate = uid.replace("@", `-${n}@`);
  used.add(candidate);
  return candidate;
}

function pad(value: number, width = 2): string {
  return value.toString().padStart(width, "0");
}

/** `YYYYMMDDTHHMMSS`: `minutes` after midnight of `day`, with no zone. */
function formatFloating(day: Date, minutes: number): string {
  const at = new Date(day.getTime() + minutes * 60_000);
  return (
    `${at.getUTCFullYear()}${pad(at.getUTCMonth() + 1)}${pad(at.getUTCDate())}` +
    `T${pad(at.getUTCHours())}${pad(at.getUTCMinutes())}00`
  );
}

function formatUtcStamp(date: Date): string {
  return date.toISOString().replace(/[-:]/g, "").replace(/\.\d{3}/, "");
}

/** Escapes a TEXT value (RFC 5545 §3.3.11). */
export function escapeText(value: string): string {
  return value
    .replace(/\\/g, "\\\\")
    .replace(/;/g, "\\;")
    .replace(/,/g, "\\,")
    .replace(/\r\n|\r|\n/g, "\\n");
}

/**
 * Folds a content line into 75-octet pieces, each continuation starting with
 * a space (RFC 5545 §3.1). Splits between code points, never inside one.
 */
export function foldLine(line: string): string {
  if (encoder.encode(line).length <= MAX_LINE_OCTETS) return line;
  const pieces: string[] = [];
  let piece = "";
  let octets = 0;
  // The leading space counts toward a continuation's 75.
  let limit = MAX_LINE_OCTETS;
  for (const char of line) {
    const size = encoder.encode(char).length;
    if (octets + size > limit) {
      pieces.push(piece);
      piece = "";
      octets = 0;
      limit = MAX_LINE_OCTETS - 1;
    }
    piece += char;
    octets += size;
  }
  pieces.push(piece);
  return pieces.join("\r\n ");
}
