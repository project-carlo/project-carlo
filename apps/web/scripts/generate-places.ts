/**
 * Generates src/generated/places.json: the diocese records and the
 * church -> diocese mapping the snapshot (frontend.json.gz) does not carry.
 *
 *   pnpm places:gen          (run from apps/web; commit the output)
 *
 * Inputs (repo root `data/`):
 *   churches.csv                             parish_id (parish slug), slug (church slug), city, state, ...
 *   dioceses/<key>/diocese.md                YAML front matter (name, state, website) + research notes
 *   dioceses/<key>/parishes/<parish>.md      one file per parish the diocese contains
 *
 * A church belongs to the diocese whose `parishes/` folder holds its parish_id.
 * Churches with no such record are left out of `churchDiocese` (reported below).
 */
import { existsSync, readdirSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { citySlug } from "../src/lib/slug";

const WEB_DIR = resolve(import.meta.dirname, "..");
const DATA_DIR = resolve(WEB_DIR, "..", "..", "data");
const OUT_PATH = resolve(WEB_DIR, "src", "generated", "places.json");

/** Cities with at least this many churches are listed in `cities`. */
const MIN_CITY_CHURCHES = 2;

/**
 * Some diocese.md bodies open with a research log rather than a description
 * (or with a section heading, so there is no opening paragraph). These
 * hand-written one-liners stand in for them.
 */
const DESCRIPTION_OVERRIDES: Record<string, string> = {
  buffalo:
    "The eight counties of western New York: Erie (Buffalo), Niagara, Chautauqua, Cattaraugus, Allegany, Genesee, Orleans and Wyoming.",
  "new-york":
    "The Archdiocese of New York covers Manhattan, the Bronx, Staten Island and seven counties to the north. Project Carlo has only begun covering it, so only a few of its parishes appear here so far.",
};

interface DioceseRecord {
  key: string;
  name: string;
  shortName: string;
  state: string;
  website: string | null;
  description: string | null;
}

/** Minimal CSV parser (quoted fields, "" escapes, newlines inside quotes). */
function parseCsv(text: string): Record<string, string>[] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') {
        field += '"';
        i++;
      } else if (ch === '"') quoted = false;
      else field += ch;
    } else if (ch === '"') quoted = true;
    else if (ch === ",") {
      row.push(field);
      field = "";
    } else if (ch === "\n" || ch === "\r") {
      if (ch === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      field = "";
      if (row.length > 1 || row[0] !== "") rows.push(row);
      row = [];
    } else field += ch;
  }
  if (field !== "" || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  const [header, ...body] = rows;
  return body.map((r) => Object.fromEntries(header.map((h, i) => [h, r[i] ?? ""])));
}

/** Split `---` front matter from the body. Only flat `key: value` lines are read. */
function parseFrontMatter(text: string): { data: Record<string, string>; body: string } {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(text);
  if (!match) return { data: {}, body: text };
  const data: Record<string, string> = {};
  for (const line of match[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z_][\w-]*):\s*(.*)$/.exec(line);
    if (!kv) continue;
    data[kv[1]] = kv[2].trim().replace(/^(['"])(.*)\1$/, "$2");
  }
  return { data, body: match[2] };
}

/**
 * The opening paragraph's first sentence (before any heading), with light
 * markdown stripped. The rest of these paragraphs is the research log
 * ("Explored in full on ..."), which does not belong on a public page.
 */
function firstParagraph(body: string): string | null {
  const para: string[] = [];
  for (const line of body.split(/\r?\n/)) {
    if (/^#{1,6}\s/.test(line)) {
      if (para.length > 0) break;
      return null; // body opens with a heading: no descriptive paragraph
    }
    if (line.trim() === "") {
      if (para.length > 0) break;
      continue;
    }
    para.push(line.trim());
  }
  if (para.length === 0) return null;
  const text = para
    .join(" ")
    .replace(/\[([^\]]+)\]\([^)]*\)/g, "$1")
    .replace(/[`*_]/g, "")
    .replace(/\s+/g, " ")
    .trim();
  return /^.+?[.!?](?=\s+[A-Z]|$)/.exec(text)?.[0] ?? text;
}

function shortName(name: string): string {
  return name.replace(/^Roman Catholic\s+/i, "").trim();
}

function main() {
  const dioceseRoot = resolve(DATA_DIR, "dioceses");
  const keys = readdirSync(dioceseRoot, { withFileTypes: true })
    .filter((e) => e.isDirectory() && existsSync(resolve(dioceseRoot, e.name, "diocese.md")))
    .map((e) => e.name)
    .sort();

  const dioceses: Record<string, DioceseRecord> = {};
  const parishDiocese = new Map<string, string>();
  for (const key of keys) {
    const { data, body } = parseFrontMatter(
      readFileSync(resolve(dioceseRoot, key, "diocese.md"), "utf-8"),
    );
    const name = data.name || key;
    dioceses[key] = {
      key,
      name,
      shortName: shortName(name),
      state: data.state || "",
      website: data.website || null,
      description: DESCRIPTION_OVERRIDES[key] ?? firstParagraph(body),
    };
    const parishDir = resolve(dioceseRoot, key, "parishes");
    if (!existsSync(parishDir)) continue;
    for (const file of readdirSync(parishDir)) {
      if (!file.endsWith(".md")) continue;
      const parish = file.slice(0, -3);
      const prior = parishDiocese.get(parish);
      if (prior && prior !== key) {
        console.warn(`parish ${parish} is in both ${prior} and ${key}; keeping ${prior}`);
        continue;
      }
      parishDiocese.set(parish, key);
    }
  }

  const churches = parseCsv(readFileSync(resolve(DATA_DIR, "churches.csv"), "utf-8"));
  const churchDiocese: Record<string, string> = {};
  const unmapped: string[] = [];
  const cityTally = new Map<
    string,
    { state: string; names: Map<string, number>; slug: string; count: number }
  >();

  for (const church of [...churches].sort((a, b) => a.slug.localeCompare(b.slug))) {
    const key = parishDiocese.get(church.parish_id);
    if (key) churchDiocese[church.slug] = key;
    else unmapped.push(church.slug);

    const city = church.city.trim();
    const state = church.state.trim().toUpperCase();
    if (!city || !state) continue;
    const slug = citySlug(city);
    if (!slug) continue;
    const id = `${state}/${slug}`;
    const entry = cityTally.get(id) ?? { state, names: new Map(), slug, count: 0 };
    entry.count++;
    entry.names.set(city, (entry.names.get(city) ?? 0) + 1);
    cityTally.set(id, entry);
  }

  const cities = [...cityTally.values()]
    .filter((c) => c.count >= MIN_CITY_CHURCHES)
    .map((c) => ({
      state: c.state,
      name: [...c.names.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0][0],
      slug: c.slug,
      count: c.count,
    }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));

  const output = { dioceses, churchDiocese, cities };
  mkdirSync(dirname(OUT_PATH), { recursive: true });
  writeFileSync(OUT_PATH, JSON.stringify(output, null, 2) + "\n", "utf-8");

  console.log(`Wrote ${OUT_PATH}`);
  console.log(
    `${keys.length} dioceses, ${Object.keys(churchDiocese).length}/${churches.length} churches mapped, ${cities.length} cities with ${MIN_CITY_CHURCHES}+ churches.`,
  );
  if (unmapped.length > 0) {
    console.log(`${unmapped.length} churches have no diocese record: ${unmapped.join(", ")}`);
  }
}

main();
