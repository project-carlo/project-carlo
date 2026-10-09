import { describe, expect, it } from "vitest";
import type { ChurchDetail, EventSummary } from "../types";
import { buildChurchCalendar, churchCalendarPath, escapeText, foldLine } from "./calendar";

const CHURCH: ChurchDetail = {
  id: 1,
  parish_id: 1,
  slug: "st-marys-corning",
  name: "St. Mary's Catholic Church",
  address_line1: "155 State Street",
  address_line2: null,
  city: "Corning",
  state: "NY",
  postal_code: "14830",
  latitude: null,
  longitude: null,
  homepage_url: null,
  bulletin_url: null,
  bulletin_week: "2026-10-04",
};

const OPTIONS = {
  pageUrl: "https://projectcarlo.com/churches/st-marys-corning/",
  uidDomain: "projectcarlo.com",
  now: new Date("2026-10-07T12:34:56.789Z"),
  // A Wednesday.
  today: new Date(2026, 9, 7),
};

let nextId = 1;
function weekly(day: string, start: number, extra: Partial<EventSummary> = {}): EventSummary {
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
    ...extra,
  };
}

function dated(date: string, start: number, extra: Partial<EventSummary> = {}): EventSummary {
  return weekly("", start, { kind: "specific_date", day_of_week: null, date, ...extra });
}

/** The VEVENT blocks, unfolded, each as a map of property line → value. */
function vevents(ics: string): Record<string, string>[] {
  const unfolded = ics.replace(/\r\n /g, "");
  return [...unfolded.matchAll(/BEGIN:VEVENT\r\n([\s\S]*?)END:VEVENT/g)].map((m) =>
    Object.fromEntries(
      m[1]
        .split("\r\n")
        .filter(Boolean)
        .map((line) => {
          const at = line.indexOf(":");
          return [line.slice(0, at), line.slice(at + 1)];
        }),
    ),
  );
}

describe("buildChurchCalendar", () => {
  it("recurs weekly events from their first day on or after today", () => {
    const [sunday, wednesday] = vevents(
      buildChurchCalendar(CHURCH, [weekly("Sunday", 9 * 60), weekly("wednesday", 7 * 60 + 30)], OPTIONS),
    );
    expect(sunday["DTSTART"]).toBe("20261011T090000");
    expect(sunday["DTEND"]).toBe("20261011T100000");
    expect(sunday["RRULE"]).toBe("FREQ=WEEKLY;BYDAY=SU");
    expect(wednesday["DTSTART"]).toBe("20261007T073000");
    expect(wednesday["RRULE"]).toBe("FREQ=WEEKLY;BYDAY=WE");
  });

  it("places dated events once, on their date, with their end time", () => {
    const [event] = vevents(
      buildChurchCalendar(
        CHURCH,
        [dated("2026-12-24", 23 * 60, { end_time: 60, type: "confession" })],
        OPTIONS,
      ),
    );
    expect(event["DTSTART"]).toBe("20261224T230000");
    // Ends past midnight, so on the next day.
    expect(event["DTEND"]).toBe("20261225T010000");
    expect(event["RRULE"]).toBeUndefined();
    expect(event["SUMMARY"]).toBe("Confession at St. Mary's Catholic Church");
  });

  it("leaves out events nothing places on a day", () => {
    const ics = buildChurchCalendar(
      CHURCH,
      [weekly("someday", 9 * 60), dated("", 9 * 60), weekly("Monday", 8 * 60)],
      OPTIONS,
    );
    expect(vevents(ics)).toHaveLength(1);
  });

  it("names, locates, sources and links each event", () => {
    const [event] = vevents(
      buildChurchCalendar(CHURCH, [weekly("Sunday", 9 * 60, { note: "Spanish; choir" })], OPTIONS),
    );
    expect(event["LOCATION"]).toBe("155 State Street\\, Corning\\, NY 14830");
    expect(event["DESCRIPTION"]).toBe(
      "Spanish\\; choir\\nFrom the parish bulletin for the week of October 4. " +
        "Times can change\\, so check the bulletin before you go.\\n" +
        OPTIONS.pageUrl,
    );
    expect(event["URL"]).toBe(OPTIONS.pageUrl);
    expect(event["DTSTAMP"]).toBe("20261007T123456Z");
  });

  it("gives events UIDs that survive renumbering and never collide", () => {
    const first = vevents(
      buildChurchCalendar(CHURCH, [weekly("Sunday", 9 * 60), weekly("Sunday", 9 * 60)], OPTIONS),
    ).map((e) => e["UID"]);
    expect(first).toEqual([
      "st-marys-corning-mass-sunday-540@projectcarlo.com",
      "st-marys-corning-mass-sunday-540-2@projectcarlo.com",
    ]);
    const again = vevents(buildChurchCalendar(CHURCH, [weekly("Sunday", 9 * 60)], OPTIONS));
    expect(again[0]["UID"]).toBe(first[0]);
  });

  it("writes a well-formed calendar with CRLF lines of at most 75 octets", () => {
    const ics = buildChurchCalendar(
      { ...CHURCH, name: "Basilica of Our Lady of Victory and the Holy Infant Jesus, Lackawanna" },
      [weekly("Sunday", 9 * 60, { note: "Celebrated in Español with the parish choir and organ" })],
      OPTIONS,
    );
    expect(ics.startsWith("BEGIN:VCALENDAR\r\nVERSION:2.0\r\n")).toBe(true);
    expect(ics.endsWith("END:VCALENDAR\r\n")).toBe(true);
    expect(ics.replace(/\r\n/g, "")).not.toMatch(/[\r\n]/);
    const encoder = new TextEncoder();
    for (const line of ics.split("\r\n")) {
      expect(encoder.encode(line).length).toBeLessThanOrEqual(75);
    }
  });
});

describe("churchCalendarPath", () => {
  it("sits beside the church page", () => {
    expect(churchCalendarPath("st-marys-corning")).toBe("/churches/st-marys-corning/schedule.ics");
  });
});

describe("escapeText", () => {
  it("escapes backslashes, separators and newlines", () => {
    expect(escapeText("a\\b;c,d\ne")).toBe("a\\\\b\\;c\\,d\\ne");
  });
});

describe("foldLine", () => {
  it("leaves short lines alone", () => {
    expect(foldLine("SUMMARY:Mass")).toBe("SUMMARY:Mass");
  });

  it("folds long lines without splitting a character", () => {
    const line = `SUMMARY:${"é".repeat(60)}`;
    const folded = foldLine(line);
    const pieces = folded.split("\r\n");
    expect(pieces.length).toBeGreaterThan(1);
    expect(pieces.slice(1).every((piece) => piece.startsWith(" "))).toBe(true);
    const encoder = new TextEncoder();
    expect(pieces.every((piece) => encoder.encode(piece).length <= 75)).toBe(true);
    expect(folded.replace(/\r\n /g, "")).toBe(line);
  });
});
