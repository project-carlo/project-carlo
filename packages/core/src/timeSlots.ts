import type { EventSummary } from "./types";
import { formatTimeRange } from "./utils";

/** A slot's start and, when it has one, its end, in minutes since midnight. */
export interface TimeSlot {
  start: number;
  end: number | null;
}

/**
 * Adds an event's slot to a day's list unless it is already there. Two events
 * at the same time (a Mass and a Confession at 4 p.m.) are listed once, but
 * two windows with the same start and different ends are both kept.
 */
export function addSlot(slots: TimeSlot[], event: EventSummary): void {
  const end = event.end_time ?? null;
  if (!slots.some((s) => s.start === event.start_time && s.end === end)) {
    slots.push({ start: event.start_time, end });
  }
}

/** Earliest start first; on the same start, the shorter window first. */
export function sortSlots(slots: TimeSlot[]): TimeSlot[] {
  return [...slots].sort(
    (a, b) => a.start - b.start || (a.end ?? -1) - (b.end ?? -1),
  );
}

/** A sorted day's slots as one string, for telling whether two days match. */
export function slotsSignature(slots: TimeSlot[]): string {
  return slots.map((s) => `${s.start}-${s.end ?? ""}`).join(",");
}

export function formatSlots(slots: TimeSlot[]): string[] {
  return slots.map((s) => formatTimeRange(s.start, s.end));
}
