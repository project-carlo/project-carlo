import { describe, expect, it } from "vitest";
import {
  MAX_EVENTS_PER_BATCH,
  analyticsDataPoint,
  isBotUserAgent,
  parseAnalyticsBatch,
} from "./analyticsApi";
import { deviceForWidth } from "./analytics";

const SESSION = "0123456789abcdef";

describe("parseAnalyticsBatch", () => {
  it("keeps a well-formed batch", () => {
    const batch = parseAnalyticsBatch({
      session: SESSION,
      device: "mobile",
      events: [
        { name: "pageview", path: "/churches/st-anne", referrer: "google.com", entry: true },
        { name: "outbound", path: "/churches/st-anne", kind: "bulletin", target: "example.org" },
      ],
    });
    expect(batch).toEqual({
      session: SESSION,
      device: "mobile",
      events: [
        {
          name: "pageview",
          path: "/churches/st-anne",
          kind: undefined,
          target: undefined,
          detail: undefined,
          referrer: "google.com",
          campaign: undefined,
          entry: true,
        },
        {
          name: "outbound",
          path: "/churches/st-anne",
          kind: "bulletin",
          target: "example.org",
          detail: undefined,
          referrer: undefined,
          campaign: undefined,
          entry: false,
        },
      ],
    });
  });

  it("refuses what isn't a batch", () => {
    expect(parseAnalyticsBatch(null)).toBeNull();
    expect(parseAnalyticsBatch([])).toBeNull();
    expect(parseAnalyticsBatch({ session: SESSION })).toBeNull();
    expect(parseAnalyticsBatch({ session: "x", events: [{ name: "pageview", path: "/" }] })).toBeNull();
    expect(
      parseAnalyticsBatch({ session: "ABC!@#0123456789", events: [{ name: "pageview", path: "/" }] }),
    ).toBeNull();
  });

  it("drops unknown events and bad paths, and refuses a batch left empty", () => {
    const batch = parseAnalyticsBatch({
      session: SESSION,
      events: [
        { name: "pageview", path: "/" },
        { name: "made_up", path: "/" },
        { name: "pageview", path: "https://elsewhere.example/" },
        { name: "pageview" },
        "pageview",
      ],
    });
    expect(batch?.events.map((e) => e.path)).toEqual(["/"]);
    expect(parseAnalyticsBatch({ session: SESSION, events: [{ name: "made_up", path: "/" }] })).toBeNull();
  });

  it("caps the batch and each field, and falls back to desktop", () => {
    const events = Array.from({ length: MAX_EVENTS_PER_BATCH + 5 }, () => ({
      name: "filter",
      path: "/" + "a".repeat(500),
      kind: "k".repeat(500),
    }));
    const batch = parseAnalyticsBatch({ session: SESSION, device: "fridge", events })!;
    expect(batch.device).toBe("desktop");
    expect(batch.events).toHaveLength(MAX_EVENTS_PER_BATCH);
    expect(batch.events[0].path).toHaveLength(200);
    expect(batch.events[0].kind).toHaveLength(100);
  });
});

describe("analyticsDataPoint", () => {
  it("lays an event out in the dataset's columns", () => {
    const batch = parseAnalyticsBatch({
      session: SESSION,
      device: "tablet",
      events: [
        {
          name: "pageview",
          path: "/mass-times/springfield",
          referrer: "news.example",
          campaign: "newsletter",
          entry: true,
        },
      ],
    })!;
    expect(
      analyticsDataPoint(batch, batch.events[0], { host: "projectcarlo.com", country: "US" }),
    ).toEqual({
      indexes: [SESSION],
      blobs: [
        "pageview",
        "/mass-times/springfield",
        "projectcarlo.com",
        "US",
        "tablet",
        "",
        "",
        "",
        "news.example",
        "newsletter",
      ],
      doubles: [1],
    });
  });
});

describe("isBotUserAgent", () => {
  it("tells crawlers and scripts from browsers", () => {
    expect(isBotUserAgent(null)).toBe(true);
    expect(isBotUserAgent("Mozilla/5.0 (compatible; Googlebot/2.1)")).toBe(true);
    expect(isBotUserAgent("Mozilla/5.0 (X11; Linux x86_64) HeadlessChrome/140.0")).toBe(true);
    expect(isBotUserAgent("curl/8.5.0")).toBe(true);
    expect(
      isBotUserAgent(
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
      ),
    ).toBe(false);
  });
});

describe("deviceForWidth", () => {
  it("buckets the viewport", () => {
    expect(deviceForWidth(375)).toBe("mobile");
    expect(deviceForWidth(768)).toBe("tablet");
    expect(deviceForWidth(1440)).toBe("desktop");
  });
});
