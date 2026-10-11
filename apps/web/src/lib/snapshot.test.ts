import { afterEach, describe, expect, it, vi } from "vitest";
import { computeNextOccurrence } from "./schedule";
import { parseSnapshot, SnapshotVersionError, SNAPSHOT_VERSION } from "./snapshot";
// Written by the pipeline's encoder: tests/test_extract_frontend_db.py checks
// that encoding the same rows still gives exactly this document.
import fixture from "./snapshot.fixture.json";

const snapshot = () => parseSnapshot(JSON.stringify(fixture));

describe("parseSnapshot", () => {
  it("decodes the churches in file order", () => {
    expect(snapshot().churches).toEqual([
      {
        id: 7,
        parish_id: 1,
        slug: "b",
        name: "B",
        address_line1: null,
        address_line2: null,
        city: "Rochester",
        state: "NY",
        postal_code: null,
        latitude: 43.1,
        longitude: -77.6,
      },
      {
        id: 3,
        parish_id: 1,
        slug: "a",
        name: "A",
        address_line1: "1 Main St",
        address_line2: null,
        city: null,
        state: "NY",
        postal_code: "14620",
        latitude: null,
        longitude: null,
      },
    ]);
  });

  it("decodes plain, dictionary-coded and delta-coded event columns", () => {
    const events = snapshot().events.map((ev) => ({ ...ev }));
    // Negative ids (schedule entries) decode from the same deltas.
    expect(events.map((ev) => ev.id)).toEqual([-118, 10, 11, 15]);
    expect(events[0]).toMatchObject({
      church_id: 3,
      event_type: "mass",
      event_kind: "weekly",
      day_of_week: "Friday",
      date: null,
      start_time: 0,
      end_time: null,
      cancelled: false,
      page_number: null,
      note: null,
      weeks_of_month: ["fourth", "last"],
      exclude_weeks: false,
      season_start_month: 10,
      season_start_day: null,
      season_end_month: 6,
      season_end_day: 15,
      cancels_event_id: null,
    });
    expect(events[1]).toMatchObject({
      day_of_week: "Sunday",
      weeks_of_month: ["last"],
      exclude_weeks: true,
    });
    expect(events[2]).toMatchObject({
      church_id: 3,
      event_type: "mass",
      event_kind: "specific_date",
      day_of_week: null,
      date: "2026-12-25",
      start_time: 0,
      end_time: 60,
      cancelled: true,
      page_number: null,
      note: "Midnight",
      weeks_of_month: [],
      season_start_month: null,
      cancels_event_id: -118,
    });
    expect(events[3]).toMatchObject({
      church_id: 7,
      event_type: "adoration",
      event_kind: "weekly",
      day_of_week: "Friday",
      date: null,
      start_time: 1140,
      end_time: 1200,
      cancelled: false,
      page_number: 3,
      note: "Midnight",
      weeks_of_month: [],
      season_end_day: null,
      cancels_event_id: null,
    });
  });

  describe("next occurrence", () => {
    afterEach(() => {
      vi.useRealTimers();
    });

    it("is computed when first read, skipping cancelled dates", () => {
      const [weekly, sunday, cancellation, adoration] = snapshot().events;
      expect(weekly.occurrence).toBe(
        computeNextOccurrence(weekly, undefined, new Set(["2026-12-25"])),
      );
      expect(sunday.occurrence).toBe(computeNextOccurrence(sunday));
      expect(adoration.occurrence).toBe(computeNextOccurrence(adoration));
      // Cancelled: never occurs.
      expect(cancellation.occurrence).toBeNull();
    });

    it("moves past a weekly event's cancelled date to its next kept week", () => {
      vi.useFakeTimers({ toFake: ["Date"] });
      // Sunday 2026-12-20. Friday the 25th is a fourth and last Friday in
      // season, but cancelled; January's fourth Friday is the 22nd.
      vi.setSystemTime(new Date(2026, 11, 20, 9));
      const [weekly, , , adoration] = snapshot().events;
      expect(new Date(weekly.occurrence!)).toEqual(new Date(2027, 0, 22, 0, 0));
      // Another church's Friday slot isn't cancelled by it.
      expect(new Date(adoration.occurrence!)).toEqual(new Date(2026, 11, 25, 19, 0));
    });
  });

  it("looks up a church's page details by slug", () => {
    const s = snapshot();
    expect(s.churchDetail("a")).toEqual({
      ...s.churches[1],
      homepage_url: "https://a",
      bulletin_url: null,
      bulletin_week: null,
    });
    expect(s.churchDetail("b")?.bulletin_week).toBe("2026-09-20");
    expect(s.churchDetail("missing")).toBeNull();
  });

  it("reads a column added since version 1 as null when a snapshot lacks it", () => {
    const churches: Partial<typeof fixture.churches> = { ...fixture.churches };
    delete churches.bulletin_week;
    const older = parseSnapshot(JSON.stringify({ ...fixture, churches }));
    expect(older.churchDetail("b")?.bulletin_week).toBeNull();
  });

  it("reads a snapshot without exclude_weeks as no exclusions", () => {
    const events: Partial<typeof fixture.events> = { ...fixture.events };
    delete events.exclude_weeks;
    const older = parseSnapshot(JSON.stringify({ ...fixture, events }));
    expect(older.events.map((ev) => ev.exclude_weeks)).toEqual([
      false,
      false,
      false,
      false,
    ]);
  });

  it("groups events by church, in id order", () => {
    const s = snapshot();
    expect(s.eventsOf(7).map((ev) => ev.id)).toEqual([10, 15]);
    expect(s.eventsOf(3).map((ev) => ev.id)).toEqual([-118, 11]);
    expect(s.eventsOf(99)).toEqual([]);
  });

  it("refuses another format version", () => {
    const other = { ...fixture, version: SNAPSHOT_VERSION + 1 };
    expect(() => parseSnapshot(JSON.stringify(other))).toThrow(
      `format version ${SNAPSHOT_VERSION + 1}`,
    );
    expect(() => parseSnapshot(JSON.stringify(other))).toThrow(SnapshotVersionError);
    expect(() => parseSnapshot("null")).toThrow(/format version undefined/);
  });
});
