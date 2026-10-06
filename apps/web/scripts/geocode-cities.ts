/**
 * Geocode the center of every city (or town, village or hamlet) that has a
 * city page, from OpenStreetMap's Nominatim, into src/data/cityCenters.json.
 * City pages measure "nearby churches" from these points; a city missing
 * from the file falls back to the mean position of its churches.
 *
 * Reads the cities from the data snapshot (public/frontend.json.gz, as the
 * prerenderer does) and only looks up cities the file doesn't have yet, so
 * rerun it after new dioceses land. Entries can be corrected by hand: the
 * script never overwrites one unless asked to.
 *
 *   pnpm --filter web geocode:cities             # look up missing cities
 *   pnpm --filter web geocode:cities --refresh   # look up every city again
 *   pnpm --filter web geocode:cities --only east-aurora-ny,elma-ny
 *   pnpm --filter web geocode:cities --dry-run   # report, don't write
 *
 * Nominatim's usage policy allows one request a second with an identifying
 * User-Agent: https://operations.osmfoundation.org/policies/nominatim/
 */
import { gunzipSync } from "node:zlib";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { parseArgs } from "node:util";
import { parseSnapshot, SNAPSHOT_FILE } from "../src/lib/snapshot";
import { buildCityIndex, distanceMiles, type City } from "../src/lib/cities";

const WEB_DIR = resolve(import.meta.dirname, "..");
const SNAPSHOT_PATH = resolve(WEB_DIR, "public", SNAPSHOT_FILE);
const CENTERS_PATH = resolve(WEB_DIR, "src", "data", "cityCenters.json");

const NOMINATIM_URL = "https://nominatim.openstreetmap.org/search";
const USER_AGENT =
  "project-carlo-city-geocoder/0.1 (+https://github.com/lyonsl2/project-carlo)";
const PAUSE_MS = 1100;

/**
 * A match farther than this from the city's churches is taken to be a
 * same-named place elsewhere in the state, and rejected.
 */
const DEFAULT_MAX_MILES = 15;

interface CenterEntry {
  /** "East Aurora, NY", for reading the file. */
  name: string;
  lat: number;
  lng: number;
  /** The OpenStreetMap object the point came from, e.g. "node/158488665". */
  osm: string;
  /** Its place type, e.g. "village" or "hamlet". */
  type: string;
}

interface NominatimResult {
  lat: string;
  lon: string;
  name?: string;
  osm_type?: string;
  osm_id?: number;
  type?: string;
  addresstype?: string;
}

/**
 * Compare place names loosely: case, punctuation, "St."/"Saint" and a "Town
 * of"/"Village of"/"City of" prefix aside.
 */
function nameKey(name: string): string {
  return name
    .replace(/^(town|village|city) of\s+/i, "")
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/\bst\b\.?/g, "saint")
    .replace(/\bmt\b\.?/g, "mount")
    .replace(/\bft\b\.?/g, "fort")
    .replace(/[^a-z0-9]/g, "");
}

async function search(city: City): Promise<NominatimResult[]> {
  const params = new URLSearchParams({
    format: "jsonv2",
    city: city.name,
    countrycodes: "us",
    featureType: "settlement",
    limit: "5",
  });
  if (city.state) params.set("state", city.state);
  const response = await fetch(`${NOMINATIM_URL}?${params}`, {
    headers: { "User-Agent": USER_AGENT, Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Nominatim answered ${response.status} for ${city.label}`);
  }
  const payload: unknown = await response.json();
  return Array.isArray(payload) ? (payload as NominatimResult[]) : [];
}

/**
 * The result to use: the nearest one named like the city, else the nearest
 * of any name (a postal city name can differ from OpenStreetMap's), and in
 * either case only within `maxMiles` of the city's churches.
 */
function pick(
  city: City,
  results: NominatimResult[],
  maxMiles: number,
): { result: NominatimResult; miles: number | null } | string {
  if (results.length === 0) return "no match";
  const scored = results
    .map((result) => ({
      result,
      named: nameKey(result.name ?? "") === nameKey(city.name),
      miles: city.center
        ? distanceMiles(city.center, { lat: Number(result.lat), lng: Number(result.lon) })
        : null,
    }))
    .filter((r) => Number.isFinite(Number(r.result.lat)) && Number.isFinite(Number(r.result.lon)));
  const inRange = scored.filter((r) => r.miles === null || r.miles <= maxMiles);
  if (inRange.length === 0) {
    const nearest = Math.min(...scored.map((r) => r.miles ?? Infinity));
    return `nearest match is ${nearest.toFixed(1)} mi from its churches`;
  }
  const byDistance = (a: { miles: number | null }, b: { miles: number | null }) =>
    (a.miles ?? 0) - (b.miles ?? 0);
  const best = inRange.filter((r) => r.named).sort(byDistance)[0] ?? inRange.sort(byDistance)[0];
  return { result: best.result, miles: best.miles };
}

function readCenters(): Record<string, CenterEntry> {
  if (!existsSync(CENTERS_PATH)) return {};
  return JSON.parse(readFileSync(CENTERS_PATH, "utf-8")) as Record<string, CenterEntry>;
}

function writeCenters(centers: Record<string, CenterEntry>): void {
  const sorted = Object.fromEntries(
    Object.entries(centers).sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)),
  );
  writeFileSync(CENTERS_PATH, JSON.stringify(sorted, null, 2) + "\n", "utf-8");
}

const sleep = (ms: number) => new Promise((done) => setTimeout(done, ms));

async function main() {
  const { values } = parseArgs({
    options: {
      refresh: { type: "boolean", default: false },
      only: { type: "string" },
      "dry-run": { type: "boolean", default: false },
      "max-miles": { type: "string", default: String(DEFAULT_MAX_MILES) },
    },
  });
  const maxMiles = Number(values["max-miles"]);
  const only = values.only ? new Set(values.only.split(",").map((s) => s.trim())) : null;

  if (!existsSync(SNAPSHOT_PATH)) {
    throw new Error(
      `${SNAPSHOT_PATH} is missing. Run \`pnpm data:pull --snapshot-only\` from the repo root first.`,
    );
  }
  const snapshot = parseSnapshot(gunzipSync(readFileSync(SNAPSHOT_PATH)).toString("utf-8"));
  // No centers passed: each city's center is its churches' mean, which is
  // what a match is checked against.
  const { cities } = buildCityIndex(snapshot.churches);

  const centers = readCenters();
  const todo = cities.filter((city) =>
    only ? only.has(city.slug) : values.refresh || !centers[city.slug],
  );
  console.log(
    `${cities.length} cities, ${cities.length - cities.filter((c) => !centers[c.slug]).length} ` +
      `already geocoded; looking up ${todo.length}.`,
  );

  const failures: string[] = [];
  let found = 0;
  for (const [i, city] of todo.entries()) {
    if (i > 0) await sleep(PAUSE_MS);
    let outcome: ReturnType<typeof pick>;
    try {
      outcome = pick(city, await search(city), maxMiles);
    } catch (error) {
      outcome = error instanceof Error ? error.message : String(error);
    }
    if (typeof outcome === "string") {
      failures.push(`${city.slug} (${city.label}): ${outcome}`);
      console.log(`  ✗ ${city.label}: ${outcome}`);
      continue;
    }
    const { result, miles } = outcome;
    centers[city.slug] = {
      name: city.label,
      lat: Number(Number(result.lat).toFixed(6)),
      lng: Number(Number(result.lon).toFixed(6)),
      osm: `${result.osm_type ?? "?"}/${result.osm_id ?? "?"}`,
      type: result.addresstype ?? result.type ?? "place",
    };
    found++;
    const away = miles === null ? "" : `, ${miles.toFixed(1)} mi from its churches`;
    console.log(`  ✓ ${city.label}: ${result.name ?? "?"} (${centers[city.slug].type}${away})`);
  }

  if (values["dry-run"]) {
    console.log(`Dry run: found ${found}, not writing ${CENTERS_PATH}.`);
  } else {
    writeCenters(centers);
    console.log(`Wrote ${CENTERS_PATH} (${found} found).`);
  }
  if (failures.length > 0) {
    console.log(
      `\n${failures.length} not geocoded; their pages fall back to their churches' ` +
        "mean position. Add them to the file by hand, or rerun with --max-miles:",
    );
    for (const failure of failures) console.log(`  ${failure}`);
  }
}

await main();
