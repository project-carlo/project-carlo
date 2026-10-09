import { describe, expect, it } from "vitest";
import type { ChurchBase } from "../types";
import { buildCityIndex } from "./cities";
import {
  buildDioceseIndex,
  dioceseCoverage,
  dioceseLabel,
  dioceseLinkFor,
  diocesePath,
  type DioceseRecord,
  type DioceseRecords,
} from "./dioceses";
import committed from "../data/dioceses.json";

function church(overrides: Partial<ChurchBase> & { id: number }): ChurchBase {
  return {
    parish_id: 1,
    slug: `church-${overrides.id}`,
    name: `Church ${overrides.id}`,
    address_line1: null,
    address_line2: null,
    city: null,
    state: "NY",
    postal_code: null,
    latitude: null,
    longitude: null,
    ...overrides,
  };
}

function record(name: string, churches: string[], covered = true): DioceseRecord {
  return { name, state: "NY", website: null, covered, churches };
}

describe("dioceseLabel", () => {
  it("drops 'Roman Catholic' from the name", () => {
    expect(dioceseLabel("Roman Catholic Diocese of Buffalo")).toBe("Diocese of Buffalo");
    expect(dioceseLabel("The Roman Catholic Archdiocese of New York")).toBe(
      "Archdiocese of New York",
    );
    expect(dioceseLabel("Archdiocese of New York")).toBe("Archdiocese of New York");
  });

  it("builds the page path", () => {
    expect(diocesePath("new-york")).toBe("/dioceses/new-york/");
  });
});

describe("buildDioceseIndex", () => {
  const churches = [
    church({ id: 1, slug: "st-mary-buffalo", city: "Buffalo" }),
    church({ id: 2, slug: "holy-cross-buffalo", city: "Buffalo" }),
    church({ id: 3, slug: "st-joseph-batavia", city: "Batavia" }),
    church({ id: 4, slug: "chapel-nowhere" }),
    church({ id: 5, slug: "st-ann-yonkers", city: "Yonkers" }),
    church({ id: 6, slug: "st-paul-border", city: "Border" }),
    church({ id: 7, slug: "st-peter-border", city: "Border" }),
    church({ id: 8, slug: "unlisted", city: "Elsewhere" }),
    church({ id: 9, slug: "retired-buffalo", city: "Buffalo" }),
    church({ id: 10, slug: "retired-border", city: "Border" }),
  ];
  const { cities } = buildCityIndex(churches);
  const records: DioceseRecords = {
    buffalo: record("Roman Catholic Diocese of Buffalo", [
      "st-mary-buffalo",
      "holy-cross-buffalo",
      "st-joseph-batavia",
      "chapel-nowhere",
      "st-paul-border",
    ]),
    "new-york": record("Archdiocese of New York", ["st-ann-yonkers", "st-peter-border"], false),
    empty: record("Roman Catholic Diocese of Nowhere", ["closed-long-ago"]),
  };
  const index = buildDioceseIndex(churches, cities, records);
  const buffalo = index.bySlug.get("buffalo")!;

  it("sorts the dioceses with churches by place, leaving out the rest", () => {
    expect(index.dioceses.map((d) => d.label)).toEqual([
      "Diocese of Buffalo",
      "Archdiocese of New York",
    ]);
  });

  it("lists each diocese's cities by label, with its churches in them", () => {
    expect(buffalo.churches.map((c) => c.id)).toEqual([1, 2, 3, 4, 6, 9]);
    expect(buffalo.cities.map(({ city, churchCount }) => [city.slug, churchCount])).toEqual([
      ["batavia-ny", 1],
      ["border-ny", 1],
      ["buffalo-ny", 3],
    ]);
    expect(dioceseCoverage(buffalo)).toBe("6 churches in 3 cities and towns");
    expect(dioceseCoverage({ churches: [churches[0]], cities: [buffalo.cities[0]] })).toBe(
      "1 church in 1 city or town",
    );
  });

  it("gives a city the diocese all its churches are in, and a split city none", () => {
    expect(index.byCity.get("buffalo-ny")?.slug).toBe("buffalo");
    expect(index.byCity.get("yonkers-ny")?.slug).toBe("new-york");
    expect(index.byCity.has("border-ny")).toBe(false);
    expect(index.byCity.has("elsewhere-ny")).toBe(false);
    expect(index.byChurch.get("st-peter-border")?.slug).toBe("new-york");
    expect(index.byChurch.has("unlisted")).toBe(false);
  });

  it("puts a church the file doesn't list in its city's diocese, if the city has one", () => {
    expect(index.byChurch.get("retired-buffalo")?.slug).toBe("buffalo");
    expect(index.byChurch.has("retired-border")).toBe(false);
  });

  it("links only a diocese the site covers in full", () => {
    expect(dioceseLinkFor(buffalo)).toEqual({ slug: "buffalo", label: "Diocese of Buffalo" });
    expect(dioceseLinkFor(index.bySlug.get("new-york"))).toBeNull();
    expect(dioceseLinkFor(undefined)).toBeNull();
  });
});

describe("src/data/dioceses.json", () => {
  // Written by `pnpm diocese site-index`; pytest checks it matches data/dioceses/.
  const records = committed as DioceseRecords;

  it("puts each church in one diocese at most", () => {
    const all = Object.values(records).flatMap((r) => r.churches);
    expect(new Set(all).size).toBe(all.length);
  });

  it("names each diocese so its label reads 'Diocese of …'", () => {
    for (const r of Object.values(records)) {
      expect(dioceseLabel(r.name)).toMatch(/^(Archdiocese|Diocese) of \S/);
    }
  });
});
