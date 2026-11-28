import { describe, expect, it } from "vitest";
import type {
  ChurchDetail,
  ContinuousAdoration,
  EventSummary,
  EventType,
} from "@carlo/core";
import { buildChurchDescription, DESCRIPTION_MAX_LENGTH } from "./churchDescription";

const church: ChurchDetail = {
  id: 1,
  parish_id: 10,
  slug: "st-charles-borromeo",
  kind: "church",
  name: "St. Charles Borromeo",
  address_line1: "3003 Dewey Ave",
  address_line2: null,
  city: "Rochester",
  state: "NY",
  postal_code: "14616",
  latitude: 43.228,
  longitude: -77.647,
  homepage_url: "https://stcharlesgreece.org",
  bulletin_url: null,
  bulletin_week: null,
  schedule_source: null,
  source_url: null,
  checked_on: null,
};

const WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"];

let nextId = 1;

/** A plain every-week slot; `start` and `end` as "H:MM" on a 24-hour clock. */
function weekly(
  type: EventType,
  day: string,
  start: string,
  end: string | null = null,
  pattern: Partial<EventSummary> = {},
): EventSummary {
  const minutes = (time: string) => {
    const [h, m] = time.split(":").map(Number);
    return h * 60 + m;
  };
  return {
    id: nextId++,
    type,
    kind: "weekly",
    day_of_week: day,
    date: null,
    start_time: minutes(start),
    end_time: end ? minutes(end) : null,
    cancelled: false,
    next_occurrence: null,
    page_number: 1,
    note: null,
    weeks_of_month: [],
    exclude_weeks: false,
    season: null,
    ...pattern,
  };
}

const continuous: ContinuousAdoration = {
  id: 1,
  church_id: 1,
  access: "not_stated",
  open_from: null,
  open_until: null,
  note: null,
  page_number: null,
  valid_from: null,
  valid_until: null,
};

describe("buildChurchDescription", () => {
  it("lists every service's weekly times, dropping the town to fit them", () => {
    const events = [
      weekly("mass", "saturday", "16:00"),
      weekly("mass", "sunday", "8:30"),
      weekly("mass", "sunday", "11:00"),
      ...["tuesday", "wednesday", "thursday", "friday"].map((day) =>
        weekly("mass", day, "8:00"),
      ),
      weekly("confession", "saturday", "15:00", "15:45"),
      weekly("adoration", "friday", "9:00", "17:00"),
    ];
    expect(buildChurchDescription(church, events)).toBe(
      "Mass: Sun 8:30 & 11 a.m.; Tue – Fri 8 a.m.; Sat 4 p.m. Confession: Sat 3 – 3:45 p.m. Adoration: Fri 9 a.m. – 5 p.m. Weekly times for St. Charles Borromeo.",
    );
  });

  it("names the later services when their times don't fit, keeping the Mass times", () => {
    // Our Lady of Fatima Shrine, Lewiston: Confession before every Mass.
    const fatima = { ...church, name: "Our Lady of Fatima Shrine", city: "Lewiston" };
    const daily = [...WEEKDAYS, "saturday"];
    const events = [
      ...["9:00", "12:00", "17:00"].map((t) => weekly("mass", "sunday", t)),
      weekly("mass", "sunday", "13:30", null, { weeks_of_month: ["fourth"] }),
      ...daily.flatMap((day) => [
        weekly("mass", day, "11:30"),
        weekly("mass", day, "16:00"),
        weekly("confession", day, "11:15", "11:30"),
        weekly("confession", day, "15:45", "16:00"),
      ]),
      weekly("mass", "saturday", "8:00"),
      weekly("confession", "saturday", "7:45", "8:00"),
      weekly("adoration", "wednesday", "12:00", "16:00"),
      weekly("adoration", "friday", "12:00", "16:00"),
    ];
    const description = buildChurchDescription(fatima, events);
    expect(description).toBe(
      "Mass: Sun 9 a.m., 12 & 5 p.m.; Mon – Fri 11:30 a.m. & 4 p.m.; Sat 8, 11:30 a.m. & 4 p.m. Confession & Adoration times for Our Lady of Fatima Shrine.",
    );
    expect(description.length).toBeLessThanOrEqual(DESCRIPTION_MAX_LENGTH);
  });

  it("cuts the Mass times to Sunday's before giving up on them", () => {
    const events = [
      weekly("mass", "sunday", "7:30"),
      weekly("mass", "sunday", "9:00"),
      weekly("mass", "sunday", "10:30"),
      weekly("mass", "sunday", "12:00"),
      ...WEEKDAYS.map((day, i) => weekly("mass", day, `${6 + i}:15`)),
      weekly("mass", "saturday", "8:00"),
      weekly("mass", "saturday", "16:30"),
      weekly("confession", "saturday", "15:00", "16:00"),
    ];
    expect(buildChurchDescription(church, events)).toBe(
      "Mass: Sun 7:30, 9, 10:30 a.m. & 12 p.m. Confession times for St. Charles Borromeo in Rochester, NY.",
    );
  });

  it("puts days with the same times together, though not Sunday", () => {
    const events = [
      weekly("mass", "sunday", "8:00"),
      ...["monday", "wednesday", "friday"].map((day) => weekly("mass", day, "8:00")),
      ...["tuesday", "thursday"].map((day) => weekly("mass", day, "12:05")),
      weekly("mass", "saturday", "8:00"),
      weekly("mass", "saturday", "16:00"),
    ];
    expect(buildChurchDescription(church, events)).toBe(
      "Mass: Sun 8 a.m.; Mon, Wed & Fri 8 a.m.; Tue & Thu 12:05 p.m.; Sat 8 a.m. & 4 p.m. Weekly times for St. Charles Borromeo in Rochester, NY.",
    );
  });

  it("only names a service with no every-week times", () => {
    const events = [
      weekly("mass", "sunday", "10:00"),
      weekly("confession", "saturday", "15:00", null, { weeks_of_month: ["first"] }),
    ];
    expect(buildChurchDescription(church, events)).toBe(
      "Mass: Sun 10 a.m. Confession times for St. Charles Borromeo in Rochester, NY.",
    );
  });

  it("leaves out cancelled slots and services the church doesn't have", () => {
    const events = [
      weekly("mass", "sunday", "10:00"),
      weekly("mass", "sunday", "18:00", null, { cancelled: true }),
    ];
    expect(buildChurchDescription(church, events)).toBe(
      "Mass: Sun 10 a.m. Weekly times for St. Charles Borromeo in Rochester, NY.",
    );
  });

  it("gives a chapel open 24 hours as Adoration every day", () => {
    const chapel = { ...church, kind: "adoration_chapel" as const, name: "Adoration Chapel" };
    expect(buildChurchDescription(chapel, [], continuous)).toBe(
      "Adoration: every day, open 24 hours. Weekly times for Adoration Chapel in Rochester, NY.",
    );
  });

  it("names the bulletin, or the page a parish with none posts its times on, before times are known", () => {
    expect(buildChurchDescription(church)).toBe(
      "Mass, Confession, and Adoration times for St. Charles Borromeo in Rochester, NY, from the parish’s weekly bulletin.",
    );
    expect(
      buildChurchDescription({
        ...church,
        schedule_source: "facebook",
        source_url: "https://www.facebook.com/stcharles",
        checked_on: "2026-11-16",
      }),
    ).toBe(
      "Mass, Confession, and Adoration times for St. Charles Borromeo in Rochester, NY, from the parish’s Facebook page.",
    );
    const chapel = { ...church, kind: "adoration_chapel" as const, name: "Adoration Chapel" };
    expect(buildChurchDescription(chapel)).toBe(
      "Adoration times for Adoration Chapel in Rochester, NY, from the parish’s weekly bulletin.",
    );
  });
});
