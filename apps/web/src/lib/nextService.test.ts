import { describe, expect, it } from "vitest";
import {
  formatDistance,
  formatWhen,
  nextEvent,
  nextOccurrenceAfter,
} from "./nextService";

// Local-time dates throughout, matching how the snapshot computes occurrences.
// Wed 2026-10-07 10:00.
const NOW = new Date(2026, 9, 7, 10, 0);

function weekly(date: Date) {
  return { kind: "weekly" as const, next_occurrence: date.toISOString() };
}

describe("nextOccurrenceAfter", () => {
  it("keeps an occurrence that is still ahead", () => {
    const later = new Date(2026, 9, 7, 17, 0);
    expect(nextOccurrenceAfter(weekly(later), NOW)?.getTime()).toBe(
      later.getTime(),
    );
  });

  it("rolls a weekly slot that has passed today forward a week", () => {
    const earlier = new Date(2026, 9, 7, 8, 0);
    const next = nextOccurrenceAfter(weekly(earlier), NOW);
    expect(next?.getTime()).toBe(new Date(2026, 9, 14, 8, 0).getTime());
  });

  it("drops a passed one-off date, and events with no occurrence", () => {
    const earlier = new Date(2026, 9, 7, 8, 0);
    expect(
      nextOccurrenceAfter(
        { kind: "specific_date", next_occurrence: earlier.toISOString() },
        NOW,
      ),
    ).toBeNull();
    expect(
      nextOccurrenceAfter({ kind: "weekly", next_occurrence: null }, NOW),
    ).toBeNull();
    expect(
      nextOccurrenceAfter({ kind: "weekly", next_occurrence: "nope" }, NOW),
    ).toBeNull();
  });
});

describe("nextEvent", () => {
  it("picks the soonest across events", () => {
    const events = [
      weekly(new Date(2026, 9, 11, 9, 0)), // Sunday
      weekly(new Date(2026, 9, 7, 8, 0)), // already past today -> next Wed
      weekly(new Date(2026, 9, 7, 12, 10)), // today noon
    ];
    expect(nextEvent(events, NOW)?.event).toBe(events[2]);
    expect(nextEvent([], NOW)).toBeNull();
  });
});

describe("formatWhen", () => {
  it("says today, tomorrow, a weekday, then a date", () => {
    expect(formatWhen(new Date(2026, 9, 7, 17, 0), NOW)).toBe("Today 5:00 PM");
    expect(formatWhen(new Date(2026, 9, 8, 8, 30), NOW)).toBe(
      "Tomorrow 8:30 AM",
    );
    expect(formatWhen(new Date(2026, 9, 10, 16, 30), NOW)).toBe("Sat 4:30 PM");
    expect(formatWhen(new Date(2026, 9, 14, 8, 0), NOW)).toBe(
      "Wed, Oct 14 8:00 AM",
    );
  });
});

describe("formatDistance", () => {
  it("rounds sensibly", () => {
    expect(formatDistance(0.04)).toBe("< 0.1 mi");
    expect(formatDistance(0.84)).toBe("0.8 mi");
    expect(formatDistance(9.96)).toBe("10 mi");
    expect(formatDistance(14.4)).toBe("14 mi");
  });
});
