import type { Database } from "sql.js";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

// The api module keeps the snapshot's rows (and the map item memo) in module
// state for the whole page session, which is exactly what these tests are
// about: each one gets a fresh copy of the module over a fake database, then
// moves the clock across midnight between calls.
const db = vi.hoisted(() => ({ current: null as unknown }));
vi.mock("./db", () => ({ getDb: () => Promise.resolve(db.current) }));

type Api = typeof import("./api");
type Row = Record<string, unknown>;

/** Just enough of sql.js for `loadCaches`, recording each query it runs. */
function fakeDb(tables: { church: Row[]; event: Row[] }) {
  const queries: string[] = [];
  const database = {
    prepare(sql: string) {
      queries.push(sql);
      const rows = /\bFROM church\b/.test(sql)
        ? tables.church
        : /\bFROM event\b/.test(sql)
          ? tables.event
          : [];
      let i = -1;
      return {
        step: () => ++i < rows.length,
        getAsObject: () => rows[i],
        free: () => {},
      };
    },
  };
  return { database: database as unknown as Database, queries };
}

function churchRow(id: number, slug: string): Row {
  return {
    id,
    parish_id: id,
    slug,
    name: slug,
    address_line1: null,
    address_line2: null,
    city: "Rochester",
    state: "NY",
    postal_code: null,
    latitude: 43.15,
    longitude: -77.6,
  };
}

function eventRow(id: number, churchId: number, overrides: Row): Row {
  return {
    id,
    church_id: churchId,
    event_type: "mass",
    event_kind: "specific_date",
    day_of_week: null,
    date: null,
    start_time: 19 * 60,
    end_time: null,
    cancelled: 0,
    page_number: null,
    note: null,
    ...overrides,
  };
}

// A parish with only dated events (a week of evening Masses, starting on the
// first test day) so its map popup takes the "five soonest" fallback, and one
// with a single weekly Mass.
const DATED = 1;
const WEEKLY = 2;
const datedEvents = [10, 11, 12, 13, 14, 15, 16].map((day) =>
  eventRow(100 + day, DATED, { date: `2026-06-${day}` }),
);
const weeklyEvent = eventRow(200, WEEKLY, {
  event_kind: "weekly",
  day_of_week: "wednesday",
  start_time: 9 * 60,
});

// Wednesday 2026-06-10, half an hour before midnight, and the next morning.
const WEDNESDAY_NIGHT = new Date(2026, 5, 10, 23, 30);
const THURSDAY_MORNING = new Date(2026, 5, 11, 0, 30);

describe("event occurrences across midnight", () => {
  let api: Api;
  let queries: string[];

  beforeEach(async () => {
    vi.useFakeTimers({ toFake: ["Date"] });
    vi.setSystemTime(WEDNESDAY_NIGHT);
    const fake = fakeDb({
      church: [churchRow(DATED, "dated"), churchRow(WEEKLY, "weekly")],
      event: [...datedEvents, weeklyEvent],
    });
    db.current = fake.database;
    queries = fake.queries;
    vi.resetModules();
    api = await import("./api");
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  const eventQueries = () => queries.filter((q) => /\bFROM event\b/.test(q));

  it("drops a church's dated events once their day has passed", async () => {
    const before = await api.fetchChurchEvents("dated", []);
    expect(before.map((e) => e.date)).toEqual([
      "2026-06-10",
      "2026-06-11",
      "2026-06-12",
      "2026-06-13",
      "2026-06-14",
      "2026-06-15",
      "2026-06-16",
    ]);

    vi.setSystemTime(THURSDAY_MORNING);
    const after = await api.fetchChurchEvents("dated", []);

    expect(after.map((e) => e.date)).toEqual([
      "2026-06-11",
      "2026-06-12",
      "2026-06-13",
      "2026-06-14",
      "2026-06-15",
      "2026-06-16",
    ]);
    // The rows themselves are still read from sql.js only once.
    expect(eventQueries()).toHaveLength(1);
  });

  it("moves weekly events' next occurrence on to the following week", async () => {
    const [before] = await api.fetchChurchEvents("weekly", []);
    expect(new Date(before.next_occurrence!).getDate()).toBe(10);

    vi.setSystemTime(THURSDAY_MORNING);
    const [after] = await api.fetchChurchEvents("weekly", []);

    expect(new Date(after.next_occurrence!).getDate()).toBe(17);
  });

  it("rebuilds the map popup's soonest dated events after midnight", async () => {
    const filters = { types: [] };
    const popupDates = (items: Awaited<ReturnType<Api["fetchChurches"]>>) =>
      items
        .find((item) => item.id === DATED)!
        .upcoming_events.map((e) => e.date);

    const first = await api.fetchChurches(filters);
    const again = await api.fetchChurches(filters);
    expect(popupDates(first)).toEqual([
      "2026-06-10",
      "2026-06-11",
      "2026-06-12",
      "2026-06-13",
      "2026-06-14",
    ]);
    // Within a day the memo still hands back the very same items.
    expect(again[0]).toBe(first[0]);
    expect(again[1]).toBe(first[1]);

    vi.setSystemTime(THURSDAY_MORNING);
    const next = await api.fetchChurches(filters);

    expect(popupDates(next)).toEqual([
      "2026-06-11",
      "2026-06-12",
      "2026-06-13",
      "2026-06-14",
      "2026-06-15",
    ]);
    // Every item embeds occurrences, so none may be served from yesterday.
    expect(next[0]).not.toBe(first[0]);
    expect(next[1]).not.toBe(first[1]);
    expect(eventQueries()).toHaveLength(1);
  });
});
