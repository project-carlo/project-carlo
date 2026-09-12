import { beforeEach, describe, expect, it } from "vitest";
import {
  collectMapItems,
  eventMatchesFilters,
  resetMapItemCache,
  type ChurchFilters,
  type RawEvent,
} from "./api";
import type { ChurchBase } from "./types";

function rawEvent(overrides: Partial<RawEvent> = {}): RawEvent {
  return {
    id: 1,
    church_id: 1,
    event_type: "mass",
    event_kind: "weekly",
    day_of_week: "monday",
    date: null,
    start_time: 9 * 60,
    end_time: null,
    cancelled: false,
    occurrence: null,
    page_number: null,
    note: null,
    weeks_of_month: [],
    season_start_month: null,
    season_start_day: null,
    season_end_month: null,
    season_end_day: null,
    ...overrides,
  };
}

describe("eventMatchesFilters", () => {
  describe("season", () => {
    const september = new Date(2026, 8, 1);
    const november = new Date(2026, 10, 1);
    // The bug this exists for: Holy Trinity Webster prints "Confessions
    // Tuesdays 4:30, October through June", and the map offered it in
    // September.
    const seasonal = rawEvent({
      event_type: "confession",
      day_of_week: "tuesday",
      start_time: 16 * 60 + 30,
      season_start_month: 10,
      season_end_month: 6,
    });

    it("hides a weekly slot that is out of season", () => {
      expect(eventMatchesFilters(seasonal, { types: [] }, september)).toBe(
        false,
      );
    });

    it("shows the same slot once its season has started", () => {
      expect(eventMatchesFilters(seasonal, { types: [] }, november)).toBe(true);
    });

    it("holds a dated season to the day, not just the month", () => {
      // "Summer Masses, June 4 - September 10": the two days either side of
      // the range fall in months the season also touches.
      const summer = rawEvent({
        day_of_week: "thursday",
        season_start_month: 6,
        season_start_day: 4,
        season_end_month: 9,
        season_end_day: 10,
      });
      const filters: ChurchFilters = { types: [] };
      expect(eventMatchesFilters(summer, filters, new Date(2026, 5, 3))).toBe(
        false,
      );
      expect(eventMatchesFilters(summer, filters, new Date(2026, 5, 4))).toBe(
        true,
      );
      expect(eventMatchesFilters(summer, filters, new Date(2026, 8, 10))).toBe(
        true,
      );
      expect(eventMatchesFilters(summer, filters, new Date(2026, 8, 11))).toBe(
        false,
      );
    });

    it("keeps a monthly slot: it does run at this time of year", () => {
      const monthly = rawEvent({ weeks_of_month: ["first"] });
      expect(eventMatchesFilters(monthly, { types: [] }, september)).toBe(true);
    });

    it("leaves a dated event to its own date", () => {
      // A specific_date row already names the day it happens; a season on it
      // would be the extractor contradicting itself.
      const dated = rawEvent({
        event_kind: "specific_date",
        day_of_week: null,
        date: "2026-09-04",
        season_start_month: 10,
        season_end_month: 6,
      });
      expect(eventMatchesFilters(dated, { types: [] }, september)).toBe(true);
    });
  });

  it("rejects cancelled events regardless of other filters", () => {
    const filters: ChurchFilters = { types: [] };
    expect(eventMatchesFilters(rawEvent({ cancelled: true }), filters)).toBe(
      false,
    );
  });

  it("accepts an event when no day or time filters are set", () => {
    expect(eventMatchesFilters(rawEvent(), { types: [] })).toBe(true);
  });

  describe("weekly weekday filter", () => {
    it("accepts when the event weekday is selected", () => {
      const ev = rawEvent({ event_kind: "weekly", day_of_week: "monday" });
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [0] })).toBe(true);
    });

    it("rejects when the event weekday is not selected", () => {
      const ev = rawEvent({ event_kind: "weekly", day_of_week: "monday" });
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [1] })).toBe(false);
    });

    it("is case-insensitive on day_of_week", () => {
      const ev = rawEvent({ event_kind: "weekly", day_of_week: "MONDAY" });
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [0] })).toBe(true);
    });

    it("rejects an unknown weekday string", () => {
      const ev = rawEvent({ event_kind: "weekly", day_of_week: "funday" });
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [0, 1, 2] })).toBe(
        false,
      );
    });
  });

  describe("specific_date weekday filter", () => {
    it("maps a Sunday date to index 6 (Monday-first)", () => {
      // 2026-06-07 is a Sunday -> getDay() 0 -> index 6.
      const ev = rawEvent({
        event_kind: "specific_date",
        day_of_week: null,
        date: "2026-06-07",
      });
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [6] })).toBe(true);
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [0] })).toBe(false);
    });

    it("maps a Monday date to index 0 (Monday-first)", () => {
      // 2026-06-08 is a Monday -> getDay() 1 -> index 0.
      const ev = rawEvent({
        event_kind: "specific_date",
        day_of_week: null,
        date: "2026-06-08",
      });
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [0] })).toBe(true);
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [6] })).toBe(false);
    });

    it("rejects an unparseable date when a day filter is set", () => {
      const ev = rawEvent({
        event_kind: "specific_date",
        day_of_week: null,
        date: "not-a-date",
      });
      expect(eventMatchesFilters(ev, { types: [], daysOfWeek: [0] })).toBe(false);
    });
  });

  describe("time-window filter", () => {
    it("applies only when both timeFrom and timeTo are set", () => {
      const ev = rawEvent({ start_time: 60 }); // 01:00, well before any window
      // Only one bound set -> window check skipped, event passes.
      expect(eventMatchesFilters(ev, { types: [], timeFrom: 8 * 60 })).toBe(true);
      expect(eventMatchesFilters(ev, { types: [], timeTo: 8 * 60 })).toBe(true);
    });

    it("rejects events outside the window when both bounds are set", () => {
      const filters: ChurchFilters = {
        types: [],
        timeFrom: 8 * 60,
        timeTo: 12 * 60,
      };
      expect(eventMatchesFilters(rawEvent({ start_time: 7 * 60 }), filters)).toBe(
        false,
      );
      expect(
        eventMatchesFilters(rawEvent({ start_time: 13 * 60 }), filters),
      ).toBe(false);
      expect(eventMatchesFilters(rawEvent({ start_time: 10 * 60 }), filters)).toBe(
        true,
      );
    });

    it("treats the window bounds as inclusive", () => {
      const filters: ChurchFilters = {
        types: [],
        timeFrom: 8 * 60,
        timeTo: 12 * 60,
      };
      expect(eventMatchesFilters(rawEvent({ start_time: 8 * 60 }), filters)).toBe(
        true,
      );
      expect(
        eventMatchesFilters(rawEvent({ start_time: 12 * 60 }), filters),
      ).toBe(true);
    });
  });
});

function church(id: number, overrides: Partial<ChurchBase> = {}): ChurchBase {
  return {
    id,
    parish_id: id,
    slug: `parish-${id}`,
    name: `Parish ${id}`,
    address_line1: "1 Main St",
    address_line2: null,
    city: "Rochester",
    state: "NY",
    postal_code: "14600",
    latitude: 43.15,
    longitude: -77.6,
    ...overrides,
  };
}

describe("collectMapItems", () => {
  const allTypes: ChurchFilters = { types: [] };

  // The memo is module state. It also checks church identity, so cases that
  // build a fresh fixture each time are already safe; this keeps the ones
  // sharing a church object (below) honest.
  beforeEach(resetMapItemCache);

  it("drops churches with no matching events", () => {
    const churches = [church(101), church(102)];
    const events = [rawEvent({ id: 1001, church_id: 101 })];

    const items = collectMapItems(churches, events, allTypes);

    expect(items.map((item) => item.id)).toEqual([101]);
  });

  it("summarises a church's matching events", () => {
    const churches = [church(111)];
    const events = [
      rawEvent({ id: 1101, church_id: 111, start_time: 9 * 60 }),
      rawEvent({
        id: 1102,
        church_id: 111,
        event_type: "confession",
        day_of_week: "saturday",
        start_time: 15 * 60,
      }),
    ];

    const [item] = collectMapItems(churches, events, allTypes);

    expect(item.event_types).toEqual(["confession", "mass"]);
    // Sorted by the schedule order the popup uses: Monday before Saturday.
    expect(item.upcoming_events.map((e) => e.start_time)).toEqual([
      9 * 60,
      15 * 60,
    ]);
  });

  it("returns the identical item when a church's matching events are unchanged", () => {
    const churches = [church(121), church(122)];
    const events = [
      rawEvent({ id: 1201, church_id: 121, start_time: 9 * 60 }),
      rawEvent({ id: 1202, church_id: 122, start_time: 17 * 60 }),
    ];

    const first = collectMapItems(churches, events, {
      types: [],
      timeFrom: 0,
      timeTo: 24 * 60,
    });
    // Narrowing the window drops the evening parish and leaves the other's
    // events untouched — the map should get the very same object back for it,
    // which is what lets the marker skip re-rendering.
    const second = collectMapItems(churches, events, {
      types: [],
      timeFrom: 0,
      timeTo: 12 * 60,
    });

    expect(second.map((item) => item.id)).toEqual([121]);
    expect(second[0]).toBe(first[0]);
  });

  // Guards `resetMapItemCache`. The memo keys on church identity *and* event
  // ids, so a leak needs a shared church fixture — which is exactly what a
  // hoisted `const` in a describe block gives you. Both halves reuse the same
  // church object and event id with different data on purpose; without the
  // reset above, the second is served the first one's item and sees 9:00.
  const sharedChurch = church(140);

  it("does not leak a memoised item into a later test (part 1)", () => {
    const items = collectMapItems(
      [sharedChurch],
      [rawEvent({ id: 1400, church_id: 140, start_time: 9 * 60 })],
      allTypes,
    );
    expect(items[0].upcoming_events[0].start_time).toBe(9 * 60);
  });

  it("does not leak a memoised item into a later test (part 2)", () => {
    const items = collectMapItems(
      [sharedChurch],
      [rawEvent({ id: 1400, church_id: 140, start_time: 17 * 60 })],
      allTypes,
    );
    expect(items[0].upcoming_events[0].start_time).toBe(17 * 60);
  });

  it("rebuilds an item when the church's matching events change", () => {
    const churches = [church(131)];
    const events = [
      rawEvent({ id: 1301, church_id: 131, start_time: 9 * 60 }),
      rawEvent({ id: 1302, church_id: 131, start_time: 17 * 60 }),
    ];

    const both = collectMapItems(churches, events, allTypes);
    const morningOnly = collectMapItems(churches, events, {
      types: [],
      timeFrom: 0,
      timeTo: 12 * 60,
    });

    expect(both[0].upcoming_events).toHaveLength(2);
    expect(morningOnly[0].upcoming_events).toHaveLength(1);
    expect(morningOnly[0]).not.toBe(both[0]);
  });
});
