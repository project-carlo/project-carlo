import type { ChurchBase } from "@carlo/core";
import { isNearAnyChurch } from "./approximateLocation";
import { foldSearchText, searchHaystack } from "./churchIndexSearch";
import {
  buildCityIndex,
  distanceMiles,
  type City,
  type LatLng,
} from "./cities";
import type { PlaceSearchResult } from "../placeSearch";

/**
 * The search box's local half: the cities and churches Carlo already knows,
 * matched in the browser, and merged with what the place-search provider
 * returns. A city Carlo serves answers at once, spelling slips included, and
 * outranks a same-named place far away that has no churches to show.
 *
 * The rules came from a benchmark on 182 queries (issue #198). Simpler ones
 * did as well as weighted scoring, and a stricter match beat a fuzzier one.
 */

/** How many places the dropdown lists. */
export const PLACE_RESULT_LIMIT = 5;
/** How many of those a city Carlo serves may take. */
const CITY_RESULT_LIMIT = 3;
/** How many churches the dropdown lists. */
const CHURCH_RESULT_LIMIT = 3;
/** Fewer letters than this can't start a match. */
const MIN_QUERY_LENGTH = 3;

const STATE_CODES: Record<string, string> = {
  alabama: "AL", alaska: "AK", arizona: "AZ", arkansas: "AR", california: "CA",
  colorado: "CO", connecticut: "CT", delaware: "DE", "district of columbia": "DC",
  florida: "FL", georgia: "GA", hawaii: "HI", idaho: "ID", illinois: "IL",
  indiana: "IN", iowa: "IA", kansas: "KS", kentucky: "KY", louisiana: "LA",
  maine: "ME", maryland: "MD", massachusetts: "MA", michigan: "MI",
  minnesota: "MN", mississippi: "MS", missouri: "MO", montana: "MT",
  nebraska: "NE", nevada: "NV", "new hampshire": "NH", "new jersey": "NJ",
  "new mexico": "NM", "new york": "NY", "north carolina": "NC",
  "north dakota": "ND", ohio: "OH", oklahoma: "OK", oregon: "OR",
  pennsylvania: "PA", "rhode island": "RI", "south carolina": "SC",
  "south dakota": "SD", tennessee: "TN", texas: "TX", utah: "UT", vermont: "VT",
  virginia: "VA", washington: "WA", "west virginia": "WV", wisconsin: "WI",
  wyoming: "WY",
};
const KNOWN_STATE_CODES = new Set(Object.values(STATE_CODES));
/** Longest first, so "West Virginia" isn't taken for Virginia. */
const STATE_NAMES = Object.keys(STATE_CODES).sort((a, b) => b.length - a.length);

/** The abbreviations place names are spelled both ways with. */
const SPELLED_OUT: Record<string, string> = {
  st: "saint",
  mt: "mount",
  ft: "fort",
};

/** Words a search may include whether or not the church's name does. */
const CHURCH_FILLER_WORDS = new Set([
  "and",
  "catholic",
  "church",
  "of",
  "parish",
  "the",
]);

/** Words too common in church names to mean a church was asked for. */
const GENERIC_CHURCH_WORDS = new Set([
  ...CHURCH_FILLER_WORDS,
  "our",
  "saint",
  "st",
]);

/** A place's name in the one form names are compared in. */
export function normalizePlaceName(name: string): string {
  return foldSearchText(name)
    .split(" ")
    .map((word) => SPELLED_OUT[word] ?? word)
    .join(" ");
}

interface PlaceQuery {
  /** The normalized query, with any state taken off the end. */
  name: string;
  /** The state it ended with, as a postal code. */
  state: string | null;
}

/** Splits "Erie, PA" or "Ithaca New York" into a name and a state. */
export function parsePlaceQuery(query: string): PlaceQuery {
  const folded = foldSearchText(query);
  const words = folded.split(" ");
  const lastWord = words[words.length - 1];
  if (words.length > 1 && KNOWN_STATE_CODES.has(lastWord.toUpperCase())) {
    return {
      name: normalizePlaceName(words.slice(0, -1).join(" ")),
      state: lastWord.toUpperCase(),
    };
  }
  if (!Object.hasOwn(STATE_CODES, folded)) {
    for (const stateName of STATE_NAMES) {
      if (folded.endsWith(` ${stateName}`)) {
        return {
          name: normalizePlaceName(folded.slice(0, -stateName.length - 1)),
          state: STATE_CODES[stateName],
        };
      }
    }
  }
  return { name: normalizePlaceName(folded), state: null };
}

/** How many slips a word of this length may have and still be recognized. */
function typoAllowance(length: number): number {
  if (length < 4) return 0;
  return length < 8 ? 1 : 2;
}

/**
 * Whether `typed` is within `maxEdits` of `target`, counting a missing, extra
 * or wrong letter, or two swapped ones, as one edit each (optimal string
 * alignment distance).
 */
function withinEdits(typed: string, target: string, maxEdits: number): boolean {
  if (Math.abs(typed.length - target.length) > maxEdits) return false;
  let beforePrevious: number[] = [];
  let previous = Array.from({ length: target.length + 1 }, (_, i) => i);
  for (let i = 1; i <= typed.length; i++) {
    const current = [i];
    let rowBest = i;
    for (let j = 1; j <= target.length; j++) {
      let cost = Math.min(
        previous[j] + 1,
        current[j - 1] + 1,
        previous[j - 1] + (typed[i - 1] === target[j - 1] ? 0 : 1),
      );
      if (
        i > 1 &&
        j > 1 &&
        typed[i - 1] === target[j - 2] &&
        typed[i - 2] === target[j - 1]
      ) {
        cost = Math.min(cost, beforePrevious[j - 2] + 1);
      }
      current[j] = cost;
      rowBest = Math.min(rowBest, cost);
    }
    if (rowBest > maxEdits) return false;
    beforePrevious = previous;
    previous = current;
  }
  return previous[target.length] <= maxEdits;
}

/** A spelling slip, not a different word: the first letter has to agree. */
function isTypoOf(typed: string, target: string): boolean {
  const allowance = typoAllowance(typed.length);
  return (
    allowance > 0 &&
    typed[0] === target[0] &&
    withinEdits(typed, target, allowance)
  );
}

interface IndexedCity {
  city: City;
  name: string;
}

interface IndexedChurch {
  church: ChurchBase;
  nameWords: string[];
  cityWords: string[];
}

/** What local search looks in, built once from the church list. */
export interface LocalSearchIndex {
  cities: IndexedCity[];
  churches: IndexedChurch[];
  /** The states Carlo has churches in. */
  states: Set<string>;
}

export function buildLocalSearchIndex(
  churches: ChurchBase[],
): LocalSearchIndex {
  const { cities } = buildCityIndex(churches);
  return {
    cities: cities
      .filter((city) => city.center !== null)
      .map((city) => ({ city, name: normalizePlaceName(city.name) })),
    churches: churches
      .filter((church) => church.name)
      .map((church) => ({
        church,
        nameWords: searchHaystack(church.name ?? "").split(" "),
        cityWords: searchHaystack(church.city ?? "").split(" "),
      })),
    states: new Set(
      cities.map((city) => city.state).filter((state) => state !== null),
    ),
  };
}

type CityMatchKind = "exact" | "prefix" | "typo";

interface CityMatch {
  city: City;
  kind: CityMatchKind;
}

const CITY_MATCH_ORDER: Record<CityMatchKind, number> = {
  exact: 0,
  prefix: 1,
  typo: 2,
};

function cityMatchKind(typed: string, name: string): CityMatchKind | null {
  if (name === typed) return "exact";
  if (name.startsWith(typed)) return "prefix";
  return isTypoOf(typed, name) ? "typo" : null;
}

/** The states a partly typed one could still become. */
function statesStartingWith(typed: string): Set<string> {
  const states = new Set<string>();
  for (const [name, code] of Object.entries(STATE_CODES)) {
    if (name.startsWith(typed) || code.toLowerCase().startsWith(typed)) {
      states.add(code);
    }
  }
  return states;
}

function findCities(
  typed: string,
  states: ReadonlySet<string> | null,
  index: LocalSearchIndex,
  near: LatLng | null,
): CityMatch[] {
  const matches: CityMatch[] = [];
  for (const { city, name } of index.cities) {
    if (states && !(city.state && states.has(city.state))) continue;
    const kind = cityMatchKind(typed, name);
    if (kind) matches.push({ city, kind });
  }
  // Nearest first, when it's known what's near; otherwise the biggest.
  const away = (city: City) =>
    near && city.center
      ? distanceMiles(near, city.center)
      : -city.churches.length;
  return matches.sort(
    (a, b) =>
      CITY_MATCH_ORDER[a.kind] - CITY_MATCH_ORDER[b.kind] ||
      away(a.city) - away(b.city),
  );
}

/** The cities Carlo serves that a query names, best match first. */
function matchCities(
  query: string,
  index: LocalSearchIndex,
  near: LatLng | null,
): CityMatch[] {
  const { name, state } = parsePlaceQuery(query);
  if (name.length < MIN_QUERY_LENGTH || /\d/.test(name)) return [];
  const withState = state ? findCities(name, new Set([state]), index, near) : [];
  if (withState.length > 0) return withState;
  // "Fort Washington" ends in a state and is still a place of its own.
  const whole = findCities(normalizePlaceName(query), null, index, near);
  if (whole.length > 0) return whole;
  // "Buffalo, New" is on its way to a state, and Buffalo stays listed meanwhile.
  const comma = query.indexOf(",");
  if (comma < 0) return [];
  const beforeComma = normalizePlaceName(query.slice(0, comma));
  const partialState = foldSearchText(query.slice(comma + 1));
  return beforeComma.length < MIN_QUERY_LENGTH
    ? []
    : findCities(beforeComma, statesStartingWith(partialState), index, near);
}

function cityPlace(city: City): PlaceSearchResult {
  const count = city.churches.length;
  return {
    id: `city-${city.slug}`,
    title: city.label,
    subtitle: `${count} ${count === 1 ? "church" : "churches"}`,
    lat: city.center?.lat ?? 0,
    lng: city.center?.lng ?? 0,
    resultType: "city",
    placeName: normalizePlaceName(city.name),
    stateCode: city.state,
    isServedCity: true,
  };
}

/** A settlement rather than an address, a street or something on a street. */
const SETTLEMENT_TYPES = new Set(["city", "suburb", "district", "county"]);

function isSamePlace(place: PlaceSearchResult, city: City): boolean {
  return (
    SETTLEMENT_TYPES.has(place.resultType) &&
    place.stateCode === city.state &&
    place.placeName === normalizePlaceName(city.name)
  );
}

/**
 * Orders a query's places: a served city it names exactly, then the
 * provider's place of exactly that name, then other served cities (nearby
 * names and likely misspellings), then whatever else the provider found.
 *
 * The provider's exact match has to be in a state Carlo covers, or was the
 * state asked for. Otherwise "Binghampton" would stop at the hamlet of that
 * name in Illinois instead of correcting to Binghamton, NY; and inside those
 * states it has to come before the cities that only resemble the query, or
 * "Greece" would become Greene and "Brighton" New Brighton.
 */
export function rankPlaces(
  query: string,
  index: LocalSearchIndex,
  providerPlaces: PlaceSearchResult[],
  near: LatLng | null,
): PlaceSearchResult[] {
  const { name, state } = parsePlaceQuery(query);
  const cities = matchCities(query, index, near).slice(0, CITY_RESULT_LIMIT);
  const others = providerPlaces.filter(
    (place) => !cities.some(({ city }) => isSamePlace(place, city)),
  );
  // Asked for by state, so that state's results go ahead of nearer ones.
  const remaining = state
    ? [
        ...others.filter((place) => place.stateCode === state),
        ...others.filter((place) => place.stateCode !== state),
      ]
    : others;
  // "Fort Washington" ends in a state and is still a place of its own.
  const wholeName = normalizePlaceName(query);
  const exactPlace = remaining.find(
    (place) =>
      SETTLEMENT_TYPES.has(place.resultType) &&
      (place.placeName === wholeName
        ? place.stateCode != null && index.states.has(place.stateCode)
        : place.placeName === name && place.stateCode === state),
  );
  return [
    ...cities.filter(({ kind }) => kind === "exact").map(({ city }) => cityPlace(city)),
    ...(exactPlace ? [exactPlace] : []),
    ...cities.filter(({ kind }) => kind !== "exact").map(({ city }) => cityPlace(city)),
    ...remaining.filter((place) => place !== exactPlace),
  ].slice(0, PLACE_RESULT_LIMIT);
}

/** How far off `typed` is from the closest of `words`: 0 when one starts with
 *  it, 1 when it's a slip for one, Infinity when it's neither. */
function wordSlips(typed: string, words: string[]): number {
  if (words.some((word) => word.startsWith(typed))) return 0;
  return words.some((word) => isTypoOf(typed, word)) ? 1 : Infinity;
}

interface ChurchMatch {
  church: ChurchBase;
  /** How many of the query's words only matched as misspellings. */
  slips: number;
}

function findChurches(
  words: string[],
  state: string | null,
  index: LocalSearchIndex,
): ChurchMatch[] {
  const required = words.filter((word) => !CHURCH_FILLER_WORDS.has(word));
  const named = required.filter(
    (word) => word.length >= MIN_QUERY_LENGTH && !GENERIC_CHURCH_WORDS.has(word),
  );
  if (named.length === 0) return [];
  const matches: ChurchMatch[] = [];
  for (const { church, nameWords, cityWords } of index.churches) {
    if (state && church.state !== state) continue;
    if (!named.some((word) => wordSlips(word, nameWords) < Infinity)) continue;
    const slips = required.reduce(
      (total, word) =>
        total + Math.min(wordSlips(word, nameWords), wordSlips(word, cityWords)),
      0,
    );
    if (slips < Infinity) matches.push({ church, slips });
  }
  return matches;
}

/**
 * The churches a query names: every word has to be in the church's name or
 * its city's, and something other than a town or a word like "saint" has to
 * be in its name, so "Erie" doesn't list every church in Erie. Words like
 * "church" can be left out of a name, and a state at the end narrows the
 * search. Churches spelled as typed go ahead of ones that only resemble the
 * query, so "St Mark" doesn't turn into every St. Mary nearby; among equals,
 * the nearest comes first.
 */
export function searchChurches(
  query: string,
  index: LocalSearchIndex,
  near: LatLng | null,
): ChurchBase[] {
  const { name, state } = parsePlaceQuery(query);
  const inState = state ? findChurches(name.split(" "), state, index) : [];
  // "St Mary Washington" ends in a state, and may be the town of that name.
  const matches =
    inState.length > 0
      ? inState
      : findChurches(foldSearchText(query).split(" ").filter(Boolean), null, index);
  const away = ({ church }: ChurchMatch) =>
    near && church.latitude != null && church.longitude != null
      ? distanceMiles(near, { lat: church.latitude, lng: church.longitude })
      : 0;
  return matches
    .sort(
      (a, b) =>
        a.slips - b.slips ||
        away(a) - away(b) ||
        (a.church.name ?? "").localeCompare(b.church.name ?? ""),
    )
    .slice(0, CHURCH_RESULT_LIMIT)
    .map(({ church }) => church);
}

/**
 * The point to rank results around: the first candidate within reach of a
 * church. A visitor far from anywhere Carlo covers gets no bias at all, since
 * ranking around them would only push the places Carlo serves down the list.
 * Null candidates are skipped.
 */
export function chooseSearchCenter(
  candidates: ReadonlyArray<LatLng | null | undefined>,
  churches: ReadonlyArray<Pick<ChurchBase, "latitude" | "longitude">>,
): LatLng | null {
  for (const candidate of candidates) {
    if (candidate && isNearAnyChurch(candidate, churches)) return candidate;
  }
  return null;
}
