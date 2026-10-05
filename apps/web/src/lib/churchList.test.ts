import { describe, expect, it } from "vitest";
import type { ChurchMapItem, EventSummary } from "../types";
import { DEFAULT_FILTER_STATE } from "../components/filterState";
import {
  boundsContain,
  boundsMoved,
  buildRows,
  countSummary,
  describeDays,
  describeFilters,
  describeTimeRange,
  formatDistance,
  formatNextTimes,
  nearestRow,
  nextStart,
  parseListSort,
  sortRows,
  thenText,
  upcomingSlots,
  type GeoBounds,
} from "./churchList";

// Saturday 3 Oct 2026, 3:30 p.m. local.
const SAT = new Date(2026, 9, 3, 15, 30);

let nextId = 1;
function weekly(day: string, start: number): EventSummary {
  return {
    id: nextId++,
    type: "mass",
    kind: "weekly",
    day_of_week: day,
    date: null,
    start_time: start,
    end_time: null,
    cancelled: false,
    next_occurrence: null,
    page_number: null,
    note: null,
  };
}

function church(
  id: number,
  name: string,
  lat: number,
  lng: number,
  events: EventSummary[],
): ChurchMapItem {
  return {
    id,
    parish_id: id,
    slug: `church-${id}`,
    name,
    address_line1: null,
    address_line2: null,
    city: "Rochester",
    state: "NY",
    postal_code: null,
    latitude: lat,
    longitude: lng,
    event_types: ["mass"],
    upcoming_events: events,
  };
}

const BOUNDS: GeoBounds = { south: 43, west: -78, north: 44, east: -77 };

describe("nextStart", () => {
  it("sanity: the fixed date is the weekday the tests assume", () => {
    expect(SAT.getDay()).toBe(6);
  });

  it("returns later today for a weekly slot still to come", () => {
    const at = nextStart(weekly("saturday", 17 * 60), SAT)!;
    expect(at.getDate()).toBe(3);
    expect(at.getHours()).toBe(17);
  });

  it("rolls a weekly slot already past today to next week", () => {
    const at = nextStart(weekly("saturday", 8 * 60), SAT)!;
    expect(at.getDate()).toBe(10);
  });

  it("finds a later weekday", () => {
    const at = nextStart(weekly("monday", 9 * 60), SAT)!;
    expect(at.getDate()).toBe(5);
  });

  it("skips cancelled, unknown-day and past dated events", () => {
    expect(
      nextStart({ ...weekly("saturday", 1000), cancelled: true }, SAT),
    ).toBeNull();
    expect(nextStart(weekly("someday", 600), SAT)).toBeNull();
    const dated: EventSummary = {
      ...weekly("saturday", 600),
      kind: "specific_date",
      day_of_week: null,
      date: "2026-10-01",
    };
    expect(nextStart(dated, SAT)).toBeNull();
    expect(nextStart({ ...dated, date: "2026-10-09" }, SAT)!.getDate()).toBe(9);
  });
});

describe("upcomingSlots", () => {
  it("sorts by the instant, not by liturgical week order", () => {
    const c = church(1, "A", 43.1, -77.6, [
      weekly("sunday", 8 * 60),
      weekly("saturday", 17 * 60),
    ]);
    const slots = upcomingSlots(c, SAT);
    expect(slots.map((s) => s.at.getDate())).toEqual([3, 4]);
  });

  it("drops duplicate instants", () => {
    const c = church(1, "A", 43.1, -77.6, [
      weekly("sunday", 8 * 60),
      weekly("sunday", 8 * 60),
    ]);
    expect(upcomingSlots(c, SAT)).toHaveLength(1);
  });
});

describe("buildRows and sortRows", () => {
  const near = church(1, "Near", 43.16, -77.61, [weekly("sunday", 10 * 60)]);
  const far = church(2, "Far", 43.5, -77.2, [weekly("saturday", 17 * 60)]);
  const outside = church(3, "Outside", 45, -70, [weekly("saturday", 17 * 60)]);
  const unmapped = {
    ...church(4, "Nowhere", 0, 0, []),
    latitude: null,
    longitude: null,
  };
  const ref = { lat: 43.16, lng: -77.6 };

  it("keeps only mapped churches inside the bounds", () => {
    const rows = buildRows([near, far, outside, unmapped], BOUNDS, ref, SAT);
    expect(rows.map((r) => r.church.id).sort()).toEqual([1, 2]);
    expect(boundsContain(BOUNDS, { lat: 45, lng: -70 })).toBe(false);
  });

  it("sorts nearest first", () => {
    const rows = buildRows([far, near], BOUNDS, ref, SAT);
    expect(sortRows(rows, "nearest").map((r) => r.church.id)).toEqual([1, 2]);
  });

  it("sorts soonest first, with no upcoming time last", () => {
    const empty = church(5, "Empty", 43.16, -77.6, []);
    const rows = buildRows([near, far, empty], BOUNDS, ref, SAT);
    expect(sortRows(rows, "soonest").map((r) => r.church.id)).toEqual([
      2, 1, 5,
    ]);
  });

  it("finds the nearest church wherever it is", () => {
    expect(nearestRow([far, outside], ref, SAT)?.church.id).toBe(2);
    expect(nearestRow([], ref, SAT)).toBeNull();
  });
});

describe("formatNextTimes", () => {
  it("emphasises the next time and flags Soon within 90 minutes", () => {
    const c = church(1, "A", 43.1, -77.6, [
      weekly("saturday", 16 * 60 + 30),
      weekly("saturday", 19 * 60),
      weekly("sunday", 8 * 60),
      weekly("sunday", 10 * 60 + 30),
    ]);
    const [row] = buildRows([c], BOUNDS, null, SAT);
    const times = formatNextTimes(row, SAT);
    expect(times.next).toEqual({
      day: "Today",
      time: "4:30 p.m.",
      minutesUntil: 60,
      soon: true,
    });
    expect(thenText(times.then)).toBe(
      "Today 7 p.m. · Tomorrow 8 a.m., 10:30 a.m.",
    );
  });

  it("is not Soon when the next service is hours away", () => {
    const c = church(1, "A", 43.1, -77.6, [weekly("saturday", 21 * 60)]);
    const [row] = buildRows([c], BOUNDS, null, SAT);
    expect(formatNextTimes(row, SAT).next?.soon).toBe(false);
  });

  it("caps the then line and counts the days left out", () => {
    const c = church(
      1,
      "A",
      43.1,
      -77.6,
      ["sunday", "monday", "tuesday", "wednesday", "thursday"].map((d) =>
        weekly(d, 9 * 60),
      ),
    );
    const [row] = buildRows([c], BOUNDS, null, SAT);
    const times = formatNextTimes(row, SAT);
    expect(times.next?.day).toBe("Tomorrow");
    expect(times.then).toHaveLength(3);
    expect(times.moreDays).toBe(1);
  });

  it("has no next time for a church with nothing upcoming", () => {
    const [row] = buildRows(
      [church(1, "A", 43.1, -77.6, [])],
      BOUNDS,
      null,
      SAT,
    );
    expect(formatNextTimes(row, SAT)).toEqual({
      next: null,
      then: [],
      moreDays: 0,
    });
  });
});

describe("formatting helpers", () => {
  it("formats distances", () => {
    expect(formatDistance(0.04)).toBe("<0.1 mi");
    expect(formatDistance(2.34)).toBe("2.3 mi");
    expect(formatDistance(14.4)).toBe("14 mi");
  });

  it("describes time ranges", () => {
    expect(describeTimeRange(0, 1439)).toBeNull();
    expect(describeTimeRange(16 * 60, 18 * 60)).toBe("between 4 and 6 p.m.");
    expect(describeTimeRange(10 * 60, 14 * 60)).toBe(
      "between 10 a.m. and 2 p.m.",
    );
    expect(describeTimeRange(16 * 60, 1439)).toBe("after 4 p.m.");
    expect(describeTimeRange(0, 9 * 60)).toBe("before 9 a.m.");
  });

  it("describes days", () => {
    expect(describeDays([])).toBeNull();
    expect(describeDays([5])).toBe("on Saturday");
    expect(describeDays([5, 6])).toBe("on Saturday or Sunday");
    expect(describeDays([0, 1, 2, 3])).toBe("on 4 days");
  });

  it("describes a filter state", () => {
    expect(
      describeFilters({
        ...DEFAULT_FILTER_STATE,
        eventType: "confession",
        daysOfWeek: [5],
        timeFrom: 16 * 60,
        timeTo: 18 * 60,
      }),
    ).toEqual({
      type: "Confession",
      days: "on Saturday",
      time: "between 4 and 6 p.m.",
    });
  });

  it("summarises counts", () => {
    expect(countSummary(18, 112)).toBe("18 churches in this area · 112 in all");
    expect(countSummary(1, undefined)).toBe("1 church in this area");
  });

  it("parses the sort param", () => {
    expect(parseListSort("soonest")).toBe("soonest");
    expect(parseListSort("junk")).toBe("nearest");
    expect(parseListSort(null)).toBe("nearest");
  });
});

describe("boundsMoved", () => {
  it("ignores a small nudge and flags a real move or zoom", () => {
    expect(
      boundsMoved(BOUNDS, { ...BOUNDS, west: -77.98, east: -76.98 }),
    ).toBe(false);
    expect(boundsMoved(BOUNDS, { ...BOUNDS, west: -77.5, east: -76.5 })).toBe(
      true,
    );
    expect(
      boundsMoved(BOUNDS, { south: 42.5, west: -78.5, north: 44.5, east: -76.5 }),
    ).toBe(true);
  });
});
