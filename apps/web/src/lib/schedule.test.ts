import { describe, expect, it } from "vitest";
import {
  compareSchedule,
  computeNextOccurrence,
  parseIsoDateLocal,
  type CompareInput,
  type OccurrenceInput,
} from "./schedule";

// ---------------------------------------------------------------------------
// computeNextOccurrence
// ---------------------------------------------------------------------------

function weeklyOccurrence(
  dayOfWeek: string | null,
  startTime: number,
  overrides: Partial<OccurrenceInput> = {},
): OccurrenceInput {
  return {
    cancelled: false,
    event_kind: "weekly",
    day_of_week: dayOfWeek,
    start_time: startTime,
    date: null,
    ...overrides,
  };
}

function specificOccurrence(
  date: string | null,
  startTime: number,
  overrides: Partial<OccurrenceInput> = {},
): OccurrenceInput {
  return {
    cancelled: false,
    event_kind: "specific_date",
    day_of_week: null,
    start_time: startTime,
    date,
    ...overrides,
  };
}

describe("computeNextOccurrence", () => {
  // Wednesday, 2026-06-10 (JS getDay() === 3). Fixed so tests never touch the
  // real clock.
  const today = new Date(2026, 5, 10);

  // Monday-first day_of_week strings -> the next matching calendar day given a
  // Wednesday "today". Exercises the (dayIdx + 1) % 7 Monday->Sunday-first
  // conversion across all seven weekdays.
  const weekdayCases: Array<{
    dow: string;
    jsDay: number;
    expectedDate: number;
  }> = [
    { dow: "monday", jsDay: 1, expectedDate: 15 },
    { dow: "tuesday", jsDay: 2, expectedDate: 16 },
    { dow: "wednesday", jsDay: 3, expectedDate: 10 }, // today itself
    { dow: "thursday", jsDay: 4, expectedDate: 11 },
    { dow: "friday", jsDay: 5, expectedDate: 12 },
    { dow: "saturday", jsDay: 6, expectedDate: 13 },
    { dow: "sunday", jsDay: 0, expectedDate: 14 },
  ];

  it.each(weekdayCases)(
    "resolves weekly $dow to the next matching weekday",
    ({ dow, jsDay, expectedDate }) => {
      const iso = computeNextOccurrence(weeklyOccurrence(dow, 9 * 60), today);
      expect(iso).not.toBeNull();
      const d = new Date(iso!);
      expect(d.getDay()).toBe(jsDay);
      expect(d.getFullYear()).toBe(2026);
      expect(d.getMonth()).toBe(5);
      expect(d.getDate()).toBe(expectedDate);
      expect(d.getHours()).toBe(9);
      expect(d.getMinutes()).toBe(0);
    },
  );

  it("returns today when today is the event's weekday", () => {
    const iso = computeNextOccurrence(weeklyOccurrence("wednesday", 600), today);
    const d = new Date(iso!);
    expect(d.getDate()).toBe(10);
  });

  it("is case-insensitive for day_of_week", () => {
    const iso = computeNextOccurrence(weeklyOccurrence("MONDAY", 600), today);
    expect(new Date(iso!).getDate()).toBe(15);
  });

  it("uses a specific_date event's date as-is", () => {
    const iso = computeNextOccurrence(
      specificOccurrence("2026-06-20", 10 * 60 + 30),
      today,
    );
    const d = new Date(iso!);
    expect(d.getFullYear()).toBe(2026);
    expect(d.getMonth()).toBe(5);
    expect(d.getDate()).toBe(20);
    expect(d.getHours()).toBe(10);
    expect(d.getMinutes()).toBe(30);
  });

  it("returns null for a specific_date whose calendar day is past", () => {
    expect(
      computeNextOccurrence(specificOccurrence("2020-01-01", 600), today),
    ).toBeNull();
    // Yesterday relative to the fixed today (2026-06-10).
    expect(
      computeNextOccurrence(specificOccurrence("2026-06-09", 600), today),
    ).toBeNull();
  });

  it("still shows a specific_date occurring today, even earlier in the day", () => {
    // today is 2026-06-10; an 08:00 event already started but the day is current.
    const iso = computeNextOccurrence(specificOccurrence("2026-06-10", 8 * 60), today);
    expect(iso).not.toBeNull();
    const d = new Date(iso!);
    expect(d.getDate()).toBe(10);
    expect(d.getHours()).toBe(8);
  });

  it("returns null for cancelled events", () => {
    expect(
      computeNextOccurrence(
        weeklyOccurrence("monday", 600, { cancelled: true }),
        today,
      ),
    ).toBeNull();
    expect(
      computeNextOccurrence(
        specificOccurrence("2026-06-20", 600, { cancelled: true }),
        today,
      ),
    ).toBeNull();
  });

  it("returns null for an unknown weekday string", () => {
    expect(
      computeNextOccurrence(weeklyOccurrence("funday", 600), today),
    ).toBeNull();
  });

  it("returns null for a weekly event with no day_of_week", () => {
    expect(computeNextOccurrence(weeklyOccurrence(null, 600), today)).toBeNull();
  });

  it("returns null for a specific_date event with no date", () => {
    expect(computeNextOccurrence(specificOccurrence(null, 600), today)).toBeNull();
  });

  it("returns null for an unparseable specific date", () => {
    expect(
      computeNextOccurrence(specificOccurrence("not-a-date", 600), today),
    ).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// compareSchedule
// ---------------------------------------------------------------------------

interface LabeledCompare extends CompareInput {
  label: string;
}

// Every fixture gets its own id, as every snapshot event row does.
let nextId = 1;

function weekly(
  label: string,
  dayOfWeek: string | null,
  startTime: number,
): LabeledCompare {
  return {
    label,
    id: nextId++,
    kind: "weekly",
    day_of_week: dayOfWeek,
    date: null,
    start_time: startTime,
  };
}

function specific(
  label: string,
  date: string | null,
  startTime: number,
): LabeledCompare {
  return {
    label,
    id: nextId++,
    kind: "specific_date",
    day_of_week: null,
    date,
    start_time: startTime,
  };
}

function sortedLabels(events: LabeledCompare[]): string[] {
  return [...events].sort(compareSchedule).map((e) => e.label);
}

describe("compareSchedule", () => {
  it("orders the liturgical week: Sunday, Sat vigil, Mon-Sat, then specific dates", () => {
    const events: LabeledCompare[] = [
      specific("specific-late", "2026-06-20", 600),
      weekly("sat-regular", "saturday", 9 * 60), // 09:00 -> regular Saturday
      weekly("friday", "friday", 8 * 60),
      weekly("monday", "monday", 8 * 60),
      weekly("sat-vigil-late", "saturday", 18 * 60), // 18:00 vigil
      weekly("sat-vigil", "saturday", 16 * 60), // 16:00 vigil boundary
      weekly("sunday", "sunday", 10 * 60),
      specific("specific-early", "2026-06-15", 600),
    ];
    expect(sortedLabels(events)).toEqual([
      "sunday",
      "sat-vigil",
      "sat-vigil-late",
      "monday",
      "friday",
      "sat-regular",
      "specific-early",
      "specific-late",
    ]);
  });

  it("treats Saturday 16:00 as a vigil but 15:59 as a regular Saturday", () => {
    const vigil = weekly("vigil", "saturday", 16 * 60); // 960
    const regular = weekly("regular", "saturday", 15 * 60 + 59); // 959
    const sunday = weekly("sunday", "sunday", 10 * 60);
    const monday = weekly("monday", "monday", 8 * 60);
    const friday = weekly("friday", "friday", 8 * 60);

    // Vigil ranks after Sunday but before Monday.
    expect(compareSchedule(sunday, vigil)).toBeLessThan(0);
    expect(compareSchedule(vigil, monday)).toBeLessThan(0);

    // 15:59 is just under the 16:00 threshold -> regular Saturday, last weekday.
    expect(compareSchedule(regular, friday)).toBeGreaterThan(0);
    expect(compareSchedule(regular, monday)).toBeGreaterThan(0);

    // And the vigil sorts ahead of the regular Saturday.
    expect(compareSchedule(vigil, regular)).toBeLessThan(0);
  });

  it("orders Mon-Sat weekly events by weekday", () => {
    const events: LabeledCompare[] = [
      weekly("thu", "thursday", 600),
      weekly("mon", "monday", 600),
      weekly("wed", "wednesday", 600),
      weekly("tue", "tuesday", 600),
      weekly("fri", "friday", 600),
    ];
    expect(sortedLabels(events)).toEqual(["mon", "tue", "wed", "thu", "fri"]);
  });

  it("breaks ties on start_time within the same weekday", () => {
    const early = weekly("early", "monday", 8 * 60);
    const late = weekly("late", "monday", 11 * 60);
    expect(compareSchedule(early, late)).toBeLessThan(0);
    expect(compareSchedule(late, early)).toBeGreaterThan(0);

    // Same applies to Sunday.
    const sun8 = weekly("sun8", "sunday", 8 * 60);
    const sun10 = weekly("sun10", "sunday", 10 * 60);
    expect(compareSchedule(sun8, sun10)).toBeLessThan(0);
  });

  it("orders two specific-date events by date, breaking ties on start_time", () => {
    const earlierDate = specific("a", "2026-06-15", 18 * 60);
    const laterDate = specific("b", "2026-06-20", 8 * 60);
    expect(compareSchedule(earlierDate, laterDate)).toBeLessThan(0);

    const sameDateEarly = specific("early", "2026-06-15", 8 * 60);
    const sameDateLate = specific("late", "2026-06-15", 18 * 60);
    expect(compareSchedule(sameDateEarly, sameDateLate)).toBeLessThan(0);
  });

  it("sorts all weekly events ahead of specific-date events", () => {
    const sat = weekly("sat-regular", "saturday", 9 * 60);
    const spec = specific("spec", "2026-06-15", 8 * 60);
    expect(compareSchedule(sat, spec)).toBeLessThan(0);
    expect(compareSchedule(spec, sat)).toBeGreaterThan(0);
  });

  it("derives the weekday from the date when a weekly event lacks day_of_week", () => {
    // The date fallback: a non-specific event with no day_of_week but a date
    // string takes that date's weekday. 2026-06-14 is a Sunday.
    const fromDate = weekly("from-date", null, 10 * 60);
    fromDate.date = "2026-06-14"; // Sunday
    const realSunday = weekly("real-sunday", "sunday", 8 * 60);
    const monday = weekly("monday", "monday", 8 * 60);

    // Behaves like a Sunday: before Monday, and ordered with the real Sunday by
    // start_time (10:00 after 08:00).
    expect(compareSchedule(fromDate, monday)).toBeLessThan(0);
    expect(compareSchedule(realSunday, fromDate)).toBeLessThan(0);

    // A Wednesday date lands between Tuesday and Thursday.
    const fromWednesday = weekly("from-wed", null, 10 * 60);
    fromWednesday.date = "2026-06-10"; // Wednesday
    expect(compareSchedule(fromWednesday, monday)).toBeGreaterThan(0);
    expect(
      compareSchedule(fromWednesday, weekly("thu", "thursday", 600)),
    ).toBeLessThan(0);
  });

  it("ranks a late-evening slot ahead of the next day's early-morning one", () => {
    const mondayLate = weekly("mon-late", "monday", 23 * 60);
    const tuesdayEarly = weekly("tue-early", "tuesday", 30);
    expect(compareSchedule(mondayLate, tuesdayEarly)).toBeLessThan(0);

    const fridayLate = weekly("fri-late", "friday", 20 * 60);
    const saturdayMidnight = weekly("sat-midnight", "saturday", 0);
    expect(compareSchedule(fridayLate, saturdayMidnight)).toBeLessThan(0);
  });

  it("sorts an unrecognized day_of_week after the week, before specific dates", () => {
    const abbreviated = weekly("abbr", "Sun", 7 * 60);
    const saturday = weekly("sat-regular", "saturday", 9 * 60);
    const sunday = weekly("sunday", "sunday", 10 * 60);
    const spec = specific("spec", "2026-06-15", 8 * 60);
    expect(compareSchedule(sunday, abbreviated)).toBeLessThan(0);
    expect(compareSchedule(saturday, abbreviated)).toBeLessThan(0);
    expect(compareSchedule(abbreviated, spec)).toBeLessThan(0);
  });

  it("orders two events with no resolvable weekday by start_time", () => {
    const early = weekly("early", null, 8 * 60);
    const late = weekly("late", "", 10 * 60);
    expect(compareSchedule(early, late)).toBeLessThan(0);
    expect(compareSchedule(late, early)).toBeGreaterThan(0);
  });

  it("derives the weekday from a date that is not plain YYYY-MM-DD", () => {
    // parseIsoDateLocal falls back to Date parsing; 2026-06-14 is a Sunday.
    const fromDateTime = weekly("from-datetime", null, 10 * 60);
    fromDateTime.date = "2026-06-14T09:00:00";
    const monday = weekly("monday", "monday", 8 * 60);
    expect(compareSchedule(fromDateTime, monday)).toBeLessThan(0);
  });

  it("breaks a tie on weekday and start_time by id", () => {
    const first = weekly("mass", "monday", 9 * 60);
    const second = weekly("confession", "monday", 9 * 60);
    expect(compareSchedule(first, second)).toBeLessThan(0);
    expect(compareSchedule(second, first)).toBeGreaterThan(0);
  });
});

describe("compareSchedule ordering properties", () => {
  // Every branch of the comparator: each weekday rank, the vigil boundary,
  // late-evening vs next-morning slots, Title-case days as the snapshot stores
  // them, weekdays derived from a date, unresolvable weekdays, specific dates,
  // and pairs that tie on everything but id.
  function representativeEvents(): LabeledCompare[] {
    const withDate = (e: LabeledCompare, date: string): LabeledCompare => ({
      ...e,
      date,
    });
    return [
      specific("spec-b", "2026-06-20", 7 * 60),
      weekly("sun-8", "Sunday", 8 * 60),
      weekly("sun-8-dup", "Sunday", 8 * 60),
      weekly("sun-lower", "sunday", 10 * 60),
      withDate(weekly("sun-from-date", null, 12 * 60), "2026-06-14"),
      withDate(
        weekly("sun-from-datetime", null, 12 * 60 + 30),
        "2026-06-14T09:00:00",
      ),
      weekly("sat-vigil", "Saturday", 16 * 60),
      weekly("sat-vigil-dup", "Saturday", 16 * 60),
      weekly("mon-late", "Monday", 23 * 60),
      weekly("mon-9", "Monday", 9 * 60),
      weekly("tue-early", "Tuesday", 30),
      withDate(weekly("wed-from-date", "Wed", 9 * 60), "2026-06-10"),
      weekly("fri-late", "Friday", 20 * 60),
      weekly("sat-midnight", "Saturday", 0),
      weekly("sat-regular", "Saturday", 15 * 60 + 59),
      weekly("unknown-abbr", "Sun", 7 * 60),
      weekly("unknown-empty", "", 9 * 60),
      weekly("unknown-null", null, 9 * 60),
      withDate(weekly("unknown-bad-date", null, 6 * 60), "not-a-date"),
      specific("unknown-no-date", null, 5 * 60),
      specific("spec-a", "2026-06-15", 8 * 60),
      specific("spec-a-dup", "2026-06-15", 8 * 60),
    ];
  }

  // Deterministic PRNG (mulberry32) so a failing permutation is reproducible.
  function seededRandom(seed: number): () => number {
    let state = seed;
    return () => {
      state = (state + 0x6d2b79f5) | 0;
      let t = Math.imul(state ^ (state >>> 15), 1 | state);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function shuffled<T>(items: T[], random: () => number): T[] {
    const out = [...items];
    for (let i = out.length - 1; i > 0; i--) {
      const j = Math.floor(random() * (i + 1));
      [out[i], out[j]] = [out[j], out[i]];
    }
    return out;
  }

  it("sorts the representative set into the documented order", () => {
    expect(sortedLabels(representativeEvents())).toEqual([
      "sun-8",
      "sun-8-dup",
      "sun-lower",
      "sun-from-date",
      "sun-from-datetime",
      "sat-vigil",
      "sat-vigil-dup",
      "mon-9",
      "mon-late",
      "tue-early",
      "wed-from-date",
      "fri-late",
      "sat-midnight",
      "sat-regular",
      "unknown-no-date",
      "unknown-bad-date",
      "unknown-abbr",
      "unknown-empty",
      "unknown-null",
      "spec-a",
      "spec-a-dup",
      "spec-b",
    ]);
  });

  it("is antisymmetric, and only ties an event with itself", () => {
    const events = representativeEvents();
    const violations: string[] = [];
    for (const a of events) {
      for (const b of events) {
        const ab = Math.sign(compareSchedule(a, b));
        const ba = Math.sign(compareSchedule(b, a));
        if (ab + ba !== 0 || (ab === 0) !== (a === b)) {
          violations.push(`${a.label} vs ${b.label}: ${ab}, ${ba}`);
        }
      }
    }
    expect(violations).toEqual([]);
  });

  it("is transitive", () => {
    const events = representativeEvents();
    const violations: string[] = [];
    for (const a of events) {
      for (const b of events) {
        if (compareSchedule(a, b) >= 0) continue;
        for (const c of events) {
          if (compareSchedule(b, c) < 0 && compareSchedule(a, c) >= 0) {
            violations.push(`${a.label} < ${b.label} < ${c.label}`);
          }
        }
      }
    }
    expect(violations).toEqual([]);
  });

  it("gives the same order whatever order the events arrive in", () => {
    const events = representativeEvents();
    const expected = sortedLabels(events);
    const random = seededRandom(20260614);
    const permutations = [
      [...events].reverse(),
      ...Array.from({ length: 50 }, () => shuffled(events, random)),
    ];
    for (const permutation of permutations) {
      expect(sortedLabels(permutation)).toEqual(expected);
    }
  });
});

describe("parseIsoDateLocal", () => {
  it("parses an ISO YYYY-MM-DD date in local time", () => {
    const d = parseIsoDateLocal("2026-06-07");
    expect(d).not.toBeNull();
    expect(d!.getFullYear()).toBe(2026);
    expect(d!.getMonth()).toBe(5);
    expect(d!.getDate()).toBe(7);
  });

  it("trims surrounding whitespace before parsing", () => {
    const d = parseIsoDateLocal("  2026-06-07  ");
    expect(d!.getDate()).toBe(7);
  });

  it("returns null for an unparseable string", () => {
    expect(parseIsoDateLocal("not-a-date")).toBeNull();
  });
});
