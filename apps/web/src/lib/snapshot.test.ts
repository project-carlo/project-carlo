import { describe, expect, it } from "vitest";
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
    expect(events.map((ev) => ev.id)).toEqual([10, 11, 15]);
    expect(events[1]).toMatchObject({
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
    });
    expect(events[2]).toMatchObject({
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
    });
  });

  it("computes each event's next occurrence when first read", () => {
    for (const ev of snapshot().events) {
      expect(ev.occurrence).toBe(computeNextOccurrence(ev));
    }
    // Cancelled: never occurs.
    expect(snapshot().events[1].occurrence).toBeNull();
  });

  it("looks up a church's page details by slug", () => {
    const s = snapshot();
    expect(s.churchDetail("a")).toEqual({
      ...s.churches[1],
      homepage_url: "https://a",
      bulletin_url: null,
    });
    expect(s.churchDetail("missing")).toBeNull();
  });

  it("groups events by church, in id order", () => {
    const s = snapshot();
    expect(s.eventsOf(7).map((ev) => ev.id)).toEqual([10, 15]);
    expect(s.eventsOf(3).map((ev) => ev.id)).toEqual([11]);
    expect(s.eventsOf(99)).toEqual([]);
  });

  it("refuses another format version", () => {
    const other = { ...fixture, version: SNAPSHOT_VERSION + 1 };
    expect(() => parseSnapshot(JSON.stringify(other))).toThrow(/format version 2/);
    expect(() => parseSnapshot(JSON.stringify(other))).toThrow(SnapshotVersionError);
    expect(() => parseSnapshot("null")).toThrow(/format version undefined/);
  });
});
