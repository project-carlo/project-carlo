import { describe, expect, it } from "vitest";
import { geoFromCf, handleGeo, isLocalHost, pickMock } from "./geo";

const env: Env = { ASSETS: { fetch: async () => new Response("asset") } };

function req(url: string, cf?: IncomingRequestCfProperties): WorkerRequest {
  return Object.assign(new Request(url), { cf });
}

describe("geoFromCf", () => {
  it("maps Cloudflare's fields, parsing coordinates", () => {
    expect(
      geoFromCf({
        city: "Rochester",
        region: "New York",
        regionCode: "NY",
        country: "US",
        postalCode: "14604",
        latitude: "43.15780",
        longitude: "-77.61560",
        timezone: "America/New_York",
      }),
    ).toEqual({
      city: "Rochester",
      region: "New York",
      regionCode: "NY",
      country: "US",
      postalCode: "14604",
      lat: 43.1578,
      lng: -77.6156,
      timezone: "America/New_York",
      source: "ip",
    });
  });

  it("returns nulls when cf is missing or partial", () => {
    const empty = geoFromCf(undefined);
    expect(empty.city).toBeNull();
    expect(empty.lat).toBeNull();
    expect(empty.lng).toBeNull();
    expect(empty.source).toBe("ip");
    expect(geoFromCf({ latitude: "nope", country: "" })).toMatchObject({
      lat: null,
      country: null,
    });
  });
});

describe("mocks", () => {
  it("only apply on localhost", () => {
    expect(isLocalHost("localhost")).toBe(true);
    expect(isLocalHost("127.0.0.1")).toBe(true);
    expect(isLocalHost("projectcarlo.org")).toBe(false);
    expect(isLocalHost("evil-localhost.com")).toBe(false);
    expect(
      pickMock(new URL("https://projectcarlo.org/api/geo?mock=rochester"), {}),
    ).toBeNull();
    expect(
      pickMock(new URL("http://127.0.0.1:8787/api/geo?mock=rochester"), {}),
    ).toMatchObject({ city: "Rochester", lat: 43.1566 });
  });

  it("accept the GEO_MOCK var, and ignore unknown names", () => {
    const url = new URL("http://localhost:5173/api/geo");
    expect(pickMock(url, { GEO_MOCK: "columbus" })).toMatchObject({
      regionCode: "OH",
    });
    expect(pickMock(url, { GEO_MOCK: "atlantis" })).toBeNull();
    expect(pickMock(url, { GEO_MOCK: "constructor" })).toBeNull();
  });
});

describe("handleGeo", () => {
  it("returns the guess uncached", async () => {
    const res = handleGeo(
      req("https://projectcarlo.org/api/geo", {
        city: "Buffalo",
        latitude: "42.88",
        longitude: "-78.87",
      }),
      env,
    );
    expect(res.headers.get("Cache-Control")).toBe("private, no-store");
    expect(await res.json()).toMatchObject({
      city: "Buffalo",
      lat: 42.88,
      lng: -78.87,
      source: "ip",
    });
  });

  it("ignores ?mock= in production", async () => {
    const res = handleGeo(
      req("https://projectcarlo.org/api/geo?mock=rochester", { city: "Albany" }),
      env,
    );
    expect(await res.json()).toMatchObject({ city: "Albany" });
  });
});
