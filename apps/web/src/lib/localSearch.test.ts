import type { ChurchBase } from "@carlo/core";
import { describe, expect, it } from "vitest";
import type { PlaceSearchResult } from "../placeSearch";
import {
  buildLocalSearchIndex,
  chooseSearchCenter,
  normalizePlaceName,
  parsePlaceQuery,
  PLACE_RESULT_LIMIT,
  rankPlaces,
  searchChurches,
  spellOutState,
} from "./localSearch";

let nextId = 1;

function church(
  name: string,
  city: string,
  state: string,
  latitude: number,
  longitude: number,
): ChurchBase {
  const id = nextId++;
  return {
    id,
    slug: `church-${id}`,
    name,
    city,
    state,
    latitude,
    longitude,
  } as ChurchBase;
}

const CHURCHES = [
  church("Sacred Heart Cathedral", "Rochester", "NY", 43.19, -77.63),
  church("St. John of Rochester", "Fairport", "NY", 43.1, -77.44),
  church("St. Mary's", "Rochester", "NY", 43.15, -77.6),
  church("St. Mary's", "Corning", "NY", 42.14, -77.05),
  church("St. Mary's", "Erie", "PA", 42.13, -80.08),
  church("St. Peter", "Binghamton", "NY", 42.1, -75.92),
  church("St. Paul", "Greene", "NY", 42.33, -75.77),
  church("St. Paul", "New Brighton", "PA", 40.73, -80.31),
  church("St. Paul", "Webster", "NY", 43.21, -77.43),
  church("St. Paul", "Rochester", "PA", 40.7, -80.28),
  church("St. Paul", "Marlton", "NJ", 39.89, -74.92),
  church("St. Paul", "Morton", "PA", 39.91, -75.33),
  church("St. Paul", "St. Marys", "PA", 41.43, -78.56),
];

const index = buildLocalSearchIndex(CHURCHES);
const ROCHESTER = { lat: 43.16, lng: -77.61 };
const PITTSBURGH = { lat: 40.44, lng: -80 };

function place(
  title: string,
  placeName: string,
  stateCode: string,
  resultType: PlaceSearchResult["resultType"] = "city",
): PlaceSearchResult {
  return {
    id: `${title}-${stateCode}`,
    title,
    subtitle: stateCode,
    lat: 0,
    lng: 0,
    resultType,
    placeName,
    stateCode,
  };
}

const titles = (places: PlaceSearchResult[]) => places.map((p) => p.title);

describe("parsePlaceQuery", () => {
  it("takes a state off the end, as a code or by name", () => {
    expect(parsePlaceQuery("Erie, PA")).toEqual({ name: "erie", state: "PA" });
    expect(parsePlaceQuery("albany ny")).toEqual({ name: "albany", state: "NY" });
    expect(parsePlaceQuery("Ithaca New York")).toEqual({
      name: "ithaca",
      state: "NY",
    });
  });

  it("takes a two-word state whole when its last word is a state too", () => {
    expect(parsePlaceQuery("Morgantown West Virginia")).toEqual({
      name: "morgantown",
      state: "WV",
    });
  });

  it("leaves a query that is only a state's name alone", () => {
    expect(parsePlaceQuery("New York")).toEqual({
      name: "new york",
      state: null,
    });
    expect(parsePlaceQuery("West Virginia")).toEqual({
      name: "west virginia",
      state: null,
    });
  });
});

describe("spellOutState", () => {
  it("spells out a state code at the end", () => {
    expect(spellOutState("boston ma")).toBe("boston Massachusetts");
    expect(spellOutState("Erie, PA")).toBe("Erie, Pennsylvania");
    expect(spellOutState("washington dc")).toBe("washington District of Columbia");
    expect(spellOutState("100 Main St, Buffalo NY")).toBe(
      "100 Main St, Buffalo New York",
    );
  });

  it("leaves anything else as typed", () => {
    expect(spellOutState("boston m")).toBe("boston m");
    expect(spellOutState("boston mass")).toBe("boston mass");
    expect(spellOutState("ma")).toBe("ma");
    expect(spellOutState("Main St")).toBe("Main St");
    expect(spellOutState("Buffalo NY 14202")).toBe("Buffalo NY 14202");
    expect(spellOutState(" Erie ")).toBe("Erie");
  });
});

describe("normalizePlaceName", () => {
  it("spells out the abbreviations names are written both ways with", () => {
    expect(normalizePlaceName("St. Marys")).toBe("saint marys");
    expect(normalizePlaceName("Mt Lebanon")).toBe("mount lebanon");
    expect(normalizePlaceName("Ft. Lee")).toBe("fort lee");
  });
});

describe("rankPlaces", () => {
  it("puts a served city ahead of a same-named place far away", () => {
    const provider = [place("Webster, MA", "webster", "MA")];
    expect(titles(rankPlaces("Webster", index, provider, ROCHESTER))).toEqual([
      "Webster, NY",
      "Webster, MA",
    ]);
  });

  it("answers from the served cities alone before the provider has", () => {
    expect(titles(rankPlaces("Corn", index, [], null))).toEqual(["Corning, NY"]);
  });

  it("corrects a misspelling the provider takes literally", () => {
    const provider = [place("Binghampton, IL", "binghampton", "IL")];
    expect(titles(rankPlaces("Binghampton", index, provider, null))[0]).toBe(
      "Binghamton, NY",
    );
  });

  it("keeps an exact place in a covered state above a merely similar city", () => {
    const greece = [place("Greece, NY", "greece", "NY")];
    expect(titles(rankPlaces("Greece NY", index, greece, ROCHESTER))).toEqual([
      "Greece, NY",
      "Greene, NY",
    ]);
  });

  it("keeps a served city up while its state is being typed", () => {
    expect(titles(rankPlaces("Corning, New", index, [], null))).toEqual([
      "Corning, NY",
    ]);
    expect(titles(rankPlaces("Corning, Oh", index, [], null))).toEqual([]);
  });

  it("takes a name ending in a state for a place of its own", () => {
    const provider = [
      place("Greene Road", "greene road", "NY", "street"),
      place("Fort Washington, PA", "fort washington", "PA"),
    ];
    expect(titles(rankPlaces("Fort Washington", index, provider, null))[0]).toBe(
      "Fort Washington, PA",
    );
  });

  it("doesn't take a street for the exact place", () => {
    const street = [place("Greece Road", "greece", "NY", "street")];
    expect(titles(rankPlaces("Greece", index, street, ROCHESTER))).toEqual([
      "Greene, NY",
      "Greece Road",
    ]);
  });

  it("puts the state that was asked for first", () => {
    const provider = [
      place("Rochester, NY", "rochester", "NY"),
      place("Rochester, MN", "rochester", "MN"),
    ];
    expect(titles(rankPlaces("Rochester MN", index, provider, ROCHESTER))[0]).toBe(
      "Rochester, MN",
    );
  });

  it("keeps a served city to its own state when one is given", () => {
    expect(titles(rankPlaces("Rochester, PA", index, [], ROCHESTER))).toEqual([
      "Rochester, PA",
    ]);
  });

  it("lists same-named cities nearest first", () => {
    expect(titles(rankPlaces("Rochester", index, [], ROCHESTER))[0]).toBe(
      "Rochester, NY",
    );
    expect(titles(rankPlaces("Rochester", index, [], PITTSBURGH))[0]).toBe(
      "Rochester, PA",
    );
  });

  it("lists the bigger city first when it's unknown what's near", () => {
    expect(titles(rankPlaces("Rochester", index, [], null))[0]).toBe(
      "Rochester, NY",
    );
  });

  it("lists a place once when the provider also has the served city", () => {
    const provider = [place("Webster, NY", "webster", "NY")];
    const results = rankPlaces("Webster", index, provider, ROCHESTER);
    expect(results).toHaveLength(1);
    expect(results[0].isServedCity).toBe(true);
  });

  it("says how many churches a served city has", () => {
    const [rochester] = rankPlaces("Rochester", index, [], ROCHESTER);
    expect(rochester.subtitle).toBe("2 churches");
    const [webster] = rankPlaces("Webster", index, [], ROCHESTER);
    expect(webster.subtitle).toBe("1 church");
  });

  it("matches a city written with an abbreviation", () => {
    expect(titles(rankPlaces("St Marys", index, [], null))[0]).toBe(
      "St. Marys, PA",
    );
  });

  it("finds a city by the start of its name", () => {
    expect(titles(rankPlaces("Roch", index, [], ROCHESTER))[0]).toBe(
      "Rochester, NY",
    );
  });

  it("leaves digits to the provider", () => {
    const zip = [place("14620", "14620", "NY", "postcode")];
    expect(titles(rankPlaces("14620", index, zip, ROCHESTER))).toEqual(["14620"]);
  });

  it("caps the list", () => {
    const provider = Array.from({ length: 10 }, (_, i) =>
      place(`Webster Place ${i}`, `webster place ${i}`, "NY", "street"),
    );
    expect(rankPlaces("Webster", index, provider, ROCHESTER)).toHaveLength(
      PLACE_RESULT_LIMIT,
    );
  });
});

describe("searchChurches", () => {
  const names = (churches: ChurchBase[]) =>
    churches.map((c) => `${c.name}, ${c.city}`);

  it("finds a church by its name and city", () => {
    expect(names(searchChurches("Sacred Heart Rochester", index, null))).toEqual([
      "Sacred Heart Cathedral, Rochester",
    ]);
    expect(names(searchChurches("St. Mary Corning", index, null))).toEqual([
      "St. Mary's, Corning",
    ]);
  });

  it("spells saint both ways", () => {
    expect(names(searchChurches("Saint Marys Corning", index, null))).toEqual([
      "St. Mary's, Corning",
    ]);
  });

  it("forgives a slip", () => {
    expect(names(searchChurches("Sacred Hart", index, null))).toEqual([
      "Sacred Heart Cathedral, Rochester",
    ]);
  });

  it("doesn't let a similar name crowd out the one typed", () => {
    const stMark = church("St. Mark", "Corning", "NY", 42.14, -77.05);
    const similar = ["St. Mary", "St. Mara", "St. Marc"].map((name) =>
      church(name, "Rochester", "NY", 43.16, -77.61),
    );
    const crowded = buildLocalSearchIndex([...similar, stMark]);
    expect(names(searchChurches("St Mark", crowded, ROCHESTER))[0]).toBe(
      "St. Mark, Corning",
    );
  });

  it("doesn't need a name to say church or parish", () => {
    expect(names(searchChurches("Sacred Heart Church", index, null))).toEqual([
      "Sacred Heart Cathedral, Rochester",
    ]);
    expect(
      names(searchChurches("St Mary Catholic Parish Corning", index, null)),
    ).toEqual(["St. Mary's, Corning"]);
  });

  it("takes a state at the end", () => {
    expect(names(searchChurches("Sacred Heart Rochester NY", index, null))).toEqual(
      ["Sacred Heart Cathedral, Rochester"],
    );
    expect(names(searchChurches("St Mary Corning New York", index, null))).toEqual(
      ["St. Mary's, Corning"],
    );
    expect(searchChurches("Sacred Heart Rochester PA", index, null)).toEqual([]);
  });

  it("keeps a town named like a state", () => {
    const washington = church("St. Hilary", "Washington", "PA", 40.17, -80.24);
    const town = buildLocalSearchIndex([washington]);
    expect(names(searchChurches("St Hilary Washington", town, null))).toEqual([
      "St. Hilary, Washington",
    ]);
  });

  it("spells fort both ways", () => {
    const lee = church("Madonna", "Fort Lee", "NJ", 40.85, -73.97);
    const town = buildLocalSearchIndex([lee]);
    expect(names(searchChurches("Madonna Ft Lee", town, null))).toEqual([
      "Madonna, Fort Lee",
    ]);
  });

  it("doesn't list a city's churches for the city's name", () => {
    expect(searchChurches("Erie", index, null)).toEqual([]);
    expect(names(searchChurches("Rochester", index, null))).toEqual([
      "St. John of Rochester, Fairport",
    ]);
  });

  it("doesn't match on a common word alone", () => {
    expect(searchChurches("church", index, null)).toEqual([]);
    expect(searchChurches("saint", index, null)).toEqual([]);
  });

  it("lists the nearest of a common name first", () => {
    expect(names(searchChurches("St Mary", index, PITTSBURGH))[0]).toBe(
      "St. Mary's, Erie",
    );
  });
});

describe("chooseSearchCenter", () => {
  const churches = CHURCHES;

  it("takes the first candidate near a church", () => {
    expect(chooseSearchCenter([ROCHESTER, PITTSBURGH], churches)).toEqual(
      ROCHESTER,
    );
  });

  it("skips a missing candidate", () => {
    expect(chooseSearchCenter([null, undefined, PITTSBURGH], churches)).toEqual(
      PITTSBURGH,
    );
  });

  it("skips somewhere Carlo doesn't cover", () => {
    const denver = { lat: 39.74, lng: -104.99 };
    expect(chooseSearchCenter([denver, ROCHESTER], churches)).toEqual(ROCHESTER);
    expect(chooseSearchCenter([denver], churches)).toBeNull();
  });
});
