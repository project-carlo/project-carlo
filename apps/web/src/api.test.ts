import { beforeEach, describe, expect, it } from "vitest";
import {
  ChurchNotFoundError,
  CityNotFoundError,
  churchCity,
  cityPageData,
  churchSchedule,
  collectMapItems,
  eventMatchesFilters,
  findChurch,
  resetMapItemCache,
  type ChurchFilters,
} from "./api";
import { parseSnapshot } from "./lib/snapshot";
import fixture from "./lib/snapshot.fixture.json";
import type { ChurchBase, RawEvent } from "./types";

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
    exclude_weeks: false,
    season_start_month: null,
    season_start_day: null,
    season_end_month: null,
    season_end_day: null,
    cancels_event_id: null,
    ...overrides,
  };
}

describe("eventMatchesFilters", () => {
  it("hides a weekly slot out of season, and keeps a monthly one", () => {
    const filters: ChurchFilters = { types: [] };
    const september = new Date(2026, 8, 15);
    const octoberToJune = rawEvent({ season_start_month: 10, season_end_month: 6 });
    expect(eventMatchesFilters(octoberToJune, filters, september)).toBe(false);
    expect(eventMatchesFilters(octoberToJune, filters, new Date(2026, 9, 1))).toBe(
      true,
    );
    // The map answers "this time of year", so a first-Monday slot stays.
    expect(
      eventMatchesFilters(rawEvent({ weeks_of_month: ["first"] }), filters, september),
    ).toBe(true);
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

  it("keeps weekly slots at one time that keep different weeks apart", () => {
    const churches = [church(151)];
    const events = [
      rawEvent({ id: -1501, church_id: 151, weeks_of_month: ["first"] }),
      rawEvent({ id: -1502, church_id: 151, weeks_of_month: ["third"] }),
      rawEvent({ id: 1503, church_id: 151, weeks_of_month: ["third"] }),
    ];

    const [item] = collectMapItems(churches, events, allTypes);

    expect(item.upcoming_events.map((e) => e.id)).toEqual([-1502, -1501]);
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

describe("church page lookups", () => {
  const snapshot = parseSnapshot(JSON.stringify(fixture));

  it("finds a church with its parish links, or throws ChurchNotFoundError", () => {
    expect(findChurch(snapshot, "a")).toMatchObject({
      id: 3,
      homepage_url: "https://a",
      bulletin_url: null,
    });
    expect(() => findChurch(snapshot, "missing")).toThrow(ChurchNotFoundError);
  });

  it("lists a church's upcoming events of the chosen types in schedule order", () => {
    // Church 7 has a Friday adoration (id 15) and a Sunday Mass (id 10).
    expect(churchSchedule(snapshot, "b", []).map((ev) => ev.id)).toEqual([10, 15]);
    expect(churchSchedule(snapshot, "b", ["adoration"]).map((ev) => ev.id)).toEqual([15]);
    expect(churchSchedule(snapshot, "b", ["confession"])).toEqual([]);
  });

  it("leaves out events with no next occurrence", () => {
    // Church 3's cancellation (id 11) never occurs; its weekly Mass does.
    expect(churchSchedule(snapshot, "a", []).map((ev) => ev.id)).toEqual([-118]);
  });

  it("carries a weekly slot's weeks of the month and season", () => {
    expect(churchSchedule(snapshot, "a", [])[0]).toMatchObject({
      weeks_of_month: ["fourth", "last"],
      season: { start_month: 10, start_day: null, end_month: 6, end_day: 15 },
    });
    expect(churchSchedule(snapshot, "b", [])[0].season).toBeNull();
  });
});

describe("city page lookups", () => {
  const snapshot = parseSnapshot(JSON.stringify(fixture));

  it("lists a city's churches with their schedules", () => {
    // Church 7 ("b") is the fixture's only church with a city.
    const data = cityPageData(snapshot, "rochester-ny", {});
    expect(data.city).toMatchObject({ label: "Rochester, NY" });
    expect(data.churches).toHaveLength(1);
    expect(data.churches[0]).toMatchObject({
      church: { id: 7 },
      citySlug: "rochester-ny",
      distanceMiles: null,
    });
    expect(data.churches[0].schedule.map((ev) => ev.id)).toEqual([10, 15]);
    // Church 3 has no coordinates, so nothing is nearby.
    expect(data.nearby).toEqual([]);
  });

  it("centers the city on its geocoded center when there is one", () => {
    const centers = { "rochester-ny": { lat: 43.16, lng: -77.61 } };
    expect(cityPageData(snapshot, "rochester-ny", centers).city).toMatchObject({
      center: { lat: 43.16, lng: -77.61 },
      geocodedCenter: true,
    });
    expect(cityPageData(snapshot, "rochester-ny", {}).city).toMatchObject({
      center: { lat: 43.1, lng: -77.6 },
      geocodedCenter: false,
    });
  });

  it("names a church's city as its city page does", () => {
    // Church 3 ("a") spells its city "rochester"; church 7's "Rochester" names the page.
    const twoSpellings = parseSnapshot(
      JSON.stringify({
        ...fixture,
        churches: {
          ...fixture.churches,
          city: { values: ["Rochester", "rochester"], codes: [0, 1] },
        },
      }),
    );
    const city = { slug: "rochester-ny", label: "Rochester, NY" };
    expect(churchCity(twoSpellings, findChurch(twoSpellings, "a"))).toEqual(city);
    expect(churchCity(twoSpellings, findChurch(twoSpellings, "b"))).toEqual(city);
    // In the plain fixture church 3 has no city, so no city page.
    expect(churchCity(snapshot, findChurch(snapshot, "a"))).toBeNull();
  });

  it("throws CityNotFoundError for a city with no churches", () => {
    expect(() => cityPageData(snapshot, "east-aurora-ny", {})).toThrow(CityNotFoundError);
  });
});
