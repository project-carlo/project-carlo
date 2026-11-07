import { YOUR_LOCATION } from "./copy";
import type { LatLng } from "./lib/cities";
import { normalizePlaceName } from "./lib/localSearch";

const GEOAPIFY_AUTOCOMPLETE_URL =
  "https://api.geoapify.com/v1/geocode/autocomplete";

/**
 * How many results to ask for: more than the dropdown lists, so the ones the
 * filter below takes out and the ones local cities replace still leave a full
 * list.
 */
const PLACE_RESULT_REQUEST_LIMIT = "10";
export const PLACE_SEARCH_ZOOM = 12;

/** A bias coordinate's precision: a tenth of a degree, about 10 km. Ranking
 *  can't tell the difference, and more precision would only miss the cache. */
const BIAS_PRECISION = 10;

const SEARCHABLE_RESULT_TYPES = new Set([
  "amenity",
  "building",
  "street",
  "suburb",
  "district",
  "postcode",
  "city",
  "county",
  "state",
]);

export type PlaceResultType =
  | "unknown"
  | "amenity"
  | "building"
  | "street"
  | "suburb"
  | "district"
  | "postcode"
  | "city"
  | "county"
  | "state"
  | "country";

export interface GeoapifyResult {
  place_id?: string;
  formatted?: string;
  address_line1?: string;
  address_line2?: string;
  name?: string;
  city?: string;
  state?: string;
  state_code?: string;
  postcode?: string;
  result_type?: PlaceResultType;
  lat?: number;
  lon?: number;
}

export interface GeoapifyResponse {
  results?: GeoapifyResult[];
}

export interface PlaceSearchResult {
  id: string;
  title: string;
  subtitle: string | null;
  lat: number;
  lng: number;
  resultType: PlaceResultType;
  /** The place's bare name, normalized, for comparing with what was typed. */
  placeName?: string;
  /** The state's postal code, when the result has one. */
  stateCode?: string | null;
  /** The visitor's own position rather than a place they searched for. */
  isCurrentLocation?: boolean;
  /** A city Carlo has churches in, from local search, not the provider. */
  isServedCity?: boolean;
}

/** The pin for where the browser says the visitor is. */
export function currentLocationPlace(lat: number, lng: number): PlaceSearchResult {
  return {
    id: `current-location-${lat}-${lng}`,
    title: YOUR_LOCATION,
    subtitle: null,
    lat,
    lng,
    resultType: "unknown",
    isCurrentLocation: true,
  };
}

export class PlaceSearchConfigurationError extends Error {
  constructor() {
    super("Geoapify place search is not configured.");
    this.name = "PlaceSearchConfigurationError";
  }
}

export function canSearchPlaces(query: string): boolean {
  const trimmed = query.trim();
  if (isZipCodeQuery(trimmed)) return true;
  return trimmed.length >= 3;
}

function isZipCodeQuery(query: string): boolean {
  return /^\d{2,5}(-\d{0,4})?$/.test(query);
}

/** "City of Lackawanna" is Lackawanna, as a visitor would type it. */
function bareName(result: GeoapifyResult, title: string): string {
  return normalizePlaceName(
    (result.name ?? title).replace(/^(city|town|village) of /i, ""),
  );
}

function toPlaceSearchResult(result: GeoapifyResult): PlaceSearchResult | null {
  if (typeof result.lat !== "number" || typeof result.lon !== "number") {
    return null;
  }

  const resultType = result.result_type ?? "unknown";
  if (!SEARCHABLE_RESULT_TYPES.has(resultType)) {
    return null;
  }

  const title =
    result.result_type === "postcode"
      ? (result.postcode ?? result.formatted)
      : (result.address_line1 ?? result.name ?? result.formatted);
  if (!title) return null;

  const addressParts = [result.city, result.state, result.postcode]
    .filter(Boolean)
    .join(", ");
  const subtitle = result.address_line2 ?? addressParts;

  return {
    id: result.place_id ?? `${result.lat}-${result.lon}-${title}`,
    title,
    subtitle: subtitle || null,
    lat: result.lat,
    lng: result.lon,
    resultType,
    placeName: bareName(result, title),
    stateCode: result.state_code?.toUpperCase() ?? null,
  };
}

/** The provider's results the dropdown can use, each listed once. */
export function parsePlaceResults(data: GeoapifyResponse): PlaceSearchResult[] {
  const seen = new Set<string>();
  const places: PlaceSearchResult[] = [];
  for (const result of data.results ?? []) {
    const place = toPlaceSearchResult(result);
    if (!place) continue;
    const label = `${place.title} ${place.subtitle ?? ""}`;
    if (seen.has(label)) continue;
    seen.add(label);
    places.push(place);
  }
  return places;
}

/** `point`, rounded to the precision the place search ranks around. */
export function roundToBiasPrecision(point: LatLng): LatLng {
  return {
    lat: Math.round(point.lat * BIAS_PRECISION) / BIAS_PRECISION,
    lng: Math.round(point.lng * BIAS_PRECISION) / BIAS_PRECISION,
  };
}

/** The provider's query string, without the key. */
export function placeSearchParams(
  query: string,
  near: LatLng | null,
): URLSearchParams {
  const trimmed = query.trim();
  const params = new URLSearchParams({
    text: trimmed,
    format: "json",
    limit: PLACE_RESULT_REQUEST_LIMIT,
    lang: "en",
    filter: "countrycode:us",
  });
  if (near) {
    params.set("bias", `proximity:${near.lng},${near.lat}`);
  }
  if (isZipCodeQuery(trimmed)) {
    params.set("type", "postcode");
  }
  return params;
}

export async function searchPlaces(
  query: string,
  options: { near?: LatLng | null; signal?: AbortSignal } = {},
): Promise<PlaceSearchResult[]> {
  const apiKey = import.meta.env.VITE_GEOAPIFY_API_KEY;
  if (!apiKey) {
    throw new PlaceSearchConfigurationError();
  }

  const params = placeSearchParams(query, options.near ?? null);
  params.set("apiKey", apiKey);
  const response = await fetch(`${GEOAPIFY_AUTOCOMPLETE_URL}?${params}`, {
    signal: options.signal,
  });
  if (!response.ok) {
    throw new Error(`Place search failed with status ${response.status}.`);
  }

  return parsePlaceResults((await response.json()) as GeoapifyResponse);
}
