/**
 * "Next Mass" for a church, relative to a moment: the soonest upcoming
 * occurrence among its events, and how to say it ("Today 5:00 PM").
 *
 * The snapshot's `next_occurrence` is computed once, as of the first read, from
 * the start of that day: a weekly event whose time has passed today still
 * carries today's date. So a weekly occurrence in the past is rolled forward a
 * week here rather than trusted. Pure; no DOM, no React.
 */
import type { EventSummary } from "../types";

type OccurrenceSource = Pick<EventSummary, "kind" | "next_occurrence">;

/** The first time at or after `now` this event happens, or null if it never does again. */
export function nextOccurrenceAfter(
  event: OccurrenceSource,
  now: Date,
): Date | null {
  if (!event.next_occurrence) return null;
  const when = new Date(event.next_occurrence);
  if (Number.isNaN(when.getTime())) return null;
  if (when.getTime() >= now.getTime()) return when;
  // A one-off date that has passed is over; a weekly slot recurs.
  if (event.kind !== "weekly") return null;
  while (when.getTime() < now.getTime()) {
    when.setDate(when.getDate() + 7);
  }
  return when;
}

export interface NextEvent<T extends OccurrenceSource> {
  event: T;
  when: Date;
}

/** The soonest-happening event, or null when none has an upcoming occurrence. */
export function nextEvent<T extends OccurrenceSource>(
  events: readonly T[],
  now: Date,
): NextEvent<T> | null {
  let best: NextEvent<T> | null = null;
  for (const event of events) {
    const when = nextOccurrenceAfter(event, now);
    if (when && (!best || when.getTime() < best.when.getTime())) {
      best = { event, when };
    }
  }
  return best;
}

/** `5:00 PM`, in the viewer's locale-independent en-US form. */
export function formatClock(when: Date): string {
  return when.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
  });
}

function startOfDay(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

/**
 * "Today 5:00 PM", "Tomorrow 8:30 AM", "Sat 4:30 PM" within the coming week,
 * and "Sat, Oct 12 4:30 PM" beyond it.
 */
export function formatWhen(when: Date, now: Date): string {
  const days = Math.round(
    (startOfDay(when).getTime() - startOfDay(now).getTime()) / 86_400_000,
  );
  const clock = formatClock(when);
  if (days <= 0) return `Today ${clock}`;
  if (days === 1) return `Tomorrow ${clock}`;
  if (days < 7) {
    return `${when.toLocaleDateString("en-US", { weekday: "short" })} ${clock}`;
  }
  const date = when.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
  });
  return `${date} ${clock}`;
}

/** "0.4 mi", "3.2 mi", "14 mi"; small values never read as "0 mi". */
export function formatDistance(miles: number): string {
  if (miles < 0.1) return "< 0.1 mi";
  const tenths = Math.round(miles * 10) / 10;
  return tenths < 10 ? `${tenths.toFixed(1)} mi` : `${Math.round(miles)} mi`;
}
