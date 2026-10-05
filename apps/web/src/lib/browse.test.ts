import { describe, expect, it } from "vitest";
import placesData from "../generated/places.json";
import type { ChurchBase, EventType } from "../types";
import {
  buildChurchPlaceContext,
  buildChurchTimes,
  buildCityModel,
  buildDioceseIndex,
  buildDioceseModel,
  buildHighlights,
  buildStateModel,
  churchCrumbs,
  computeStats,
  createPlaceIndex,
  formatDistance,
  formatSlot,
  formatTime,
  formatTimeList,
  groupTownsByLetter,
  mapLinkFor,
  serviceByDay,
  townLinks,
  weekdayMassSummary,
  weekendLine,
  weekendRows,
  type BrowseEntry,
} from "./browse";

const h = (hour: number, min = 0) => hour * 60 + min;

type Ev = Parameters<typeof buildChurchTimes>[0][number];
function ev(
  type: EventType,
  day: string,
  start: number,
  end: number | null = null,
): Ev {
  return {
    event_type: type,
    event_kind: "weekly",
    day_of_week: day,
    start_time: start,
    end_time: end,
    cancelled: false,
  };
}

let nextId = 1;
function entry(
  name: string,
  city: string | null,
  events: Ev[],
  at: [number, number] | null = null,
  slug = `c${nextId}`,
): BrowseEntry {
  const church: ChurchBase = {
    id: nextId++,
    parish_id: 1,
    slug,
    name,
    address_line1: "1 Main St",
    address_line2: null,
    city,
    state: "NY",
    postal_code: null,
    latitude: at?.[0] ?? null,
    longitude: at?.[1] ?? null,
  };
  return { church, times: buildChurchTimes(events) };
}

describe("time formatting", () => {
  it("formats single times", () => {
    expect(formatTime(h(8))).toBe("8 a.m.");
    expect(formatTime(h(17, 30))).toBe("5:30 p.m.");
    expect(formatTime(h(12))).toBe("12 p.m.");
    expect(formatTime(0)).toBe("12 a.m.");
  });

  it("drops a meridiem the next time shares", () => {
    expect(formatTimeList([h(8), h(10, 30), h(17)])).toBe("8, 10:30 a.m., 5 p.m.");
    expect(formatTimeList([h(17), h(8), h(8)])).toBe("8 a.m., 5 p.m.");
    expect(formatTimeList([h(11), h(12)])).toBe("11 a.m., 12 p.m.");
    expect(formatTimeList([])).toBe("");
  });

  it("formats ranges", () => {
    expect(formatSlot({ start: h(15), end: h(16) })).toBe("3–4 p.m.");
    expect(formatSlot({ start: h(11, 30), end: h(12, 30) })).toBe(
      "11:30 a.m.–12:30 p.m.",
    );
    expect(formatSlot({ start: h(9), end: null })).toBe("9 a.m.");
  });

  it("formats distances", () => {
    expect(formatDistance(0.04)).toBe("under 0.1 mi");
    expect(formatDistance(2.14)).toBe("2.1 mi");
    expect(formatDistance(12.6)).toBe("13 mi");
  });
});

describe("buildChurchTimes", () => {
  it("keeps weekly events, dedupes and sorts, and skips cancelled/specific-date", () => {
    const times = buildChurchTimes([
      ev("mass", "Sunday", h(10)),
      ev("mass", "sunday", h(8)),
      ev("mass", "sunday", h(8)),
      ev("confession", "Saturday", h(15), h(16)),
      { ...ev("mass", "monday", h(7)), cancelled: true },
      { ...ev("mass", "monday", h(9)), event_kind: "specific_date" },
      ev("adoration", "friday", h(9), h(17)),
      ev("mass", "someday", h(9)),
    ]);
    expect(times.mass.sunday).toEqual([h(8), h(10)]);
    expect(times.mass.monday).toEqual([]);
    expect(times.confession.saturday).toEqual([{ start: h(15), end: h(16) }]);
    expect(times.adoration.friday).toHaveLength(1);
  });

  it("summarises the weekend and weekdays", () => {
    const { times } = entry("St A", "X", [
      ev("mass", "saturday", h(8)),
      ev("mass", "saturday", h(16, 30)),
      ev("mass", "sunday", h(9)),
      ev("mass", "monday", h(8)),
      ev("mass", "tuesday", h(8)),
      ev("mass", "wednesday", h(8)),
      ev("mass", "thursday", h(19)),
      ev("mass", "friday", h(8)),
    ]);
    expect(weekendLine(times)).toBe("Sat 4:30 p.m. · Sun 9 a.m.");
    // Saturday 8 a.m. is a weekday-style Mass, not the vigil.
    expect(weekdayMassSummary(times)).toBe(
      "Mon–Wed, Fri & Sat 8 a.m.; Thu 7 p.m.",
    );
  });
});

describe("highlights", () => {
  const entries = [
    entry("St Early", "Albion", [
      ev("mass", "sunday", h(7)),
      ev("mass", "sunday", h(9)),
      ev("mass", "sunday", h(11)),
      ev("mass", "saturday", h(17)),
      ...["monday", "tuesday", "wednesday", "thursday", "friday"].map((d) =>
        ev("mass", d, h(8)),
      ),
      ev("confession", "saturday", h(15), h(16)),
    ]),
    entry("St Late", "Albion", [
      ev("mass", "sunday", h(10)),
      ev("mass", "sunday", h(19)),
      ev("confession", "friday", h(12)),
      ev("adoration", "friday", h(9), h(17)),
    ]),
    entry("St Twin", "Albion", [ev("mass", "sunday", h(7))]),
  ];

  it("computes the extremes and counts", () => {
    const stats = computeStats(entries);
    expect(stats.churchCount).toBe(3);
    expect(stats.townCount).toBe(1);
    expect(stats.earliestSunday?.minutes).toBe(h(7));
    expect(stats.earliestSunday?.churches.map((c) => c.name)).toEqual([
      "St Early",
      "St Twin",
    ]);
    expect(stats.latestSunday?.minutes).toBe(h(19));
    expect(stats.mostSunday?.count).toBe(3);
    expect(stats.withDailyMass).toBe(1);
    expect(stats.withVigil).toBe(1);
    expect(stats.withSaturdayConfession).toBe(1);
    expect(stats.withConfession).toBe(2);
    expect(stats.withAdoration).toBe(1);
  });

  it("words the highlights from the data", () => {
    const hs = buildHighlights(computeStats(entries));
    const byId = Object.fromEntries(hs.map((x) => [x.id, x]));
    expect(byId["earliest-sunday"].value).toBe("7 a.m.");
    expect(byId["earliest-sunday"].detail).toBe("at St Early and 1 other");
    expect(byId["latest-sunday"].detail).toBe("at St Late");
    expect(byId["daily-mass"].value).toBe("1");
    expect(byId["saturday-confession"].detail).toContain("of 2 with Confession");
  });

  it("copes with no data", () => {
    expect(buildHighlights(computeStats([]))).toEqual([]);
    expect(buildHighlights(computeStats([entry("Quiet", "X", [])]))).toEqual([]);
  });
});

describe("serviceByDay and weekendRows", () => {
  const entries = [
    entry("B Church", "Yonkers", [
      ev("confession", "saturday", h(16), h(17)),
      ev("mass", "sunday", h(9)),
    ]),
    entry("A Church", "Yonkers", [
      ev("confession", "saturday", h(16), h(17)),
      ev("confession", "monday", h(9)),
    ]),
  ];

  it("groups slots by weekday, earliest first then by name", () => {
    const days = serviceByDay(entries, "confession");
    expect(days.map((d) => d.day)).toEqual(["monday", "saturday"]);
    expect(days[1].rows.map((r) => r.church.name)).toEqual(["A Church", "B Church"]);
    expect(days[1].label).toBe("Saturdays");
    expect(days[1].churchCount).toBe(2);
    expect(serviceByDay(entries, "adoration")).toEqual([]);
  });

  it("builds weekend rows", () => {
    const rows = weekendRows(entries);
    expect(rows.map((r) => r.church.name)).toEqual(["A Church", "B Church"]);
    expect(rows[1].sunday).toBe("9 a.m.");
    expect(rows[0].sunday).toBe("");
  });
});

describe("city, state and church models", () => {
  const entries = [
    entry("St One", "Troy", [ev("mass", "sunday", h(9))], [42.73, -73.69], "st-one"),
    entry("St Two", "Troy", [ev("mass", "sunday", h(11))], [42.74, -73.68], "st-two"),
    entry("St Near", "Lansingburgh", [ev("mass", "sunday", h(8))], [42.77, -73.67], "st-near"),
    entry("St Far", "Buffalo", [ev("mass", "sunday", h(8))], [42.89, -78.88], "st-far"),
    entry("St Lone", "Albany", [], [42.65, -73.75], "st-lone"),
  ];
  const index = createPlaceIndex(entries);

  it("builds a city page with nearby churches outside the city", () => {
    const model = buildCityModel(index, "ny", "troy");
    expect(model).not.toBeNull();
    expect(model!.title).toBe(
      "Mass & Confession Times in Troy, NY · 2 Catholic Churches | Project Carlo",
    );
    expect(model!.path).toBe("/mass-times/ny/troy/");
    expect(model!.stats.churchCount).toBe(2);
    expect(model!.nearby.map((n) => n.name)).toEqual(["St Near", "St Lone"]);
    expect(model!.nearby[0].distanceLabel).toMatch(/mi$/);
    expect(model!.crumbs.map((c) => c.name)).toEqual(["Home", "New York", "Troy"]);
    expect(model!.items).toHaveLength(2);
    expect(model!.description.length).toBeLessThanOrEqual(160);
  });

  it("has no page for single-church or unknown towns", () => {
    expect(buildCityModel(index, "ny", "albany")).toBeNull();
    expect(buildCityModel(index, "ny", "nowhere")).toBeNull();
    expect(buildCityModel(index, "nj", "troy")).toBeNull();
  });

  it("links one-church towns straight to the church", () => {
    const towns = townLinks(entries);
    const albany = towns.find((t) => t.city === "Albany")!;
    expect(albany.path).toBe("/churches/st-lone/");
    expect(albany.churchName).toBe("St Lone");
    expect(towns.find((t) => t.city === "Troy")!.path).toBe("/mass-times/ny/troy/");
    const letters = groupTownsByLetter(towns);
    expect(letters.map((l) => l.letter)).toEqual(["A", "B", "L", "T"]);
  });

  it("builds the state hub", () => {
    const model = buildStateModel(index, "NY");
    expect(model!.cityPages).toEqual([
      { city: "Troy", path: "/mass-times/ny/troy/", count: 2 },
    ]);
    expect(model!.towns).toHaveLength(4);
    expect(model!.path).toBe("/mass-times/ny/");
    expect(buildStateModel(index, "TX")).toBeNull();
  });

  it("gives a church its city link, crumbs and nearest neighbours", () => {
    const one = entries[0].church;
    const ctx = buildChurchPlaceContext(index, one);
    expect(ctx.cityPage).toEqual({ path: "/mass-times/ny/troy/", name: "Troy" });
    expect(ctx.nearby).toHaveLength(4);
    expect(ctx.nearby[0].name).toBe("St Two");
    expect(ctx.nearby.map((n) => n.name)).not.toContain("St One");
    expect(churchCrumbs(one, ctx).map((c) => c.name)).toEqual([
      "Home",
      "New York",
      "Troy",
      "St One",
    ]);

    const lone = entries[4].church;
    const loneCtx = buildChurchPlaceContext(index, lone);
    expect(loneCtx.cityPage).toBeNull();
    expect(churchCrumbs(lone, loneCtx).map((c) => c.name)).toEqual([
      "Home",
      "New York",
      "St Lone",
    ]);
  });

  it("builds the map link", () => {
    expect(mapLinkFor(entries[0].church)).toBe("/map?lat=42.73&lng=-73.69&z=15");
    expect(mapLinkFor(entries[0].church, 17)).toContain("z=17");
    expect(mapLinkFor({ ...entries[0].church, latitude: null })).toBeNull();
  });
});

describe("diocese pages", () => {
  const keys = Object.keys(placesData.dioceses);
  const slugForKey = (key: string) =>
    Object.entries(placesData.churchDiocese).find(([, k]) => k === key)![0];

  it("lists dioceses that have churches and builds their pages", () => {
    const key = keys[0];
    const entries = [
      entry("In Diocese", "Troy", [ev("mass", "sunday", h(9))], null, slugForKey(key)),
      entry("Unmapped", "Troy", [], null, "not-in-places"),
    ];
    const index = createPlaceIndex(entries);
    const cards = buildDioceseIndex(index).cards;
    expect(cards).toHaveLength(1);
    expect(cards[0].diocese.key).toBe(key);
    expect(cards[0].churchCount).toBe(1);

    const model = buildDioceseModel(index, key);
    expect(model!.path).toBe(`/dioceses/${key}/`);
    expect(model!.towns).toHaveLength(1);
    expect(model!.towns[0].cityPagePath).toBeNull();
    expect(buildDioceseModel(index, "nope")).toBeNull();
  });
});
