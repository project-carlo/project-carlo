import { createHash } from "node:crypto";
import { gunzipSync } from "node:zlib";
import { existsSync, readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { renderToStaticMarkup } from "react-dom/server";
import { loadEnv } from "vite";
import { createElement } from "react";
import {
  churchCity,
  churchMapData,
  churchSchedule,
  cityIndex,
  cityPageData,
  findChurch,
} from "../src/api";
import { cityPath, type CityCenters } from "../src/lib/cities";
import { CHURCH_INDEX_ENTRY, CITY_MAP_ENTRY } from "../src/lib/cityMapEntry";
import { HOME_LINK_ATTRIBUTE, HOME_SEARCH_KEY } from "../src/hooks/useHomeHref";
import cityCentersJson from "../src/data/cityCenters.json";
import { parseSnapshot, SNAPSHOT_FILE } from "../src/lib/snapshot";
import { StaticChurchPage } from "../src/prerender/StaticChurchPage";
import { StaticChurchIndexPage } from "../src/prerender/StaticChurchIndexPage";
import { StaticCityPage } from "../src/prerender/StaticCityPage";
import { CHURCH_INDEX_PATH, SITE_ORIGIN, absoluteUrl, churchPath } from "../src/lib/seo";
import {
  LASTMOD_FILE,
  LASTMOD_PLACEHOLDER,
  contentForHash,
  latestDate,
  parseLastmodManifest,
  resolveLastmod,
  type LastmodEntry,
  type LastmodManifest,
} from "../src/lib/lastmod";
import { EVENT_TYPE_ORDER } from "../src/constants/eventTypes";
import { CHURCH_CALENDAR_FILE, buildChurchCalendar } from "../src/lib/calendar";

const WEB_DIR = resolve(import.meta.dirname, "..");
// The Cloudflare Vite plugin puts the browser build in dist/client, beside
// the Worker's own bundle.
const DIST_DIR = resolve(WEB_DIR, "dist", "client");
const SNAPSHOT_PATH = resolve(WEB_DIR, "public", SNAPSHOT_FILE);
// Written because vite.config.ts sets build.manifest; public/.assetsignore
// keeps it out of the deployed assets.
const MANIFEST_PATH = resolve(DIST_DIR, ".vite", "manifest.json");

/** Font files to preload — Latin subsets of the two typefaces used on church
 *  pages (Cardo for display headings, EB Garamond for body text). */
const PRELOAD_FONTS = [
  /\/cardo-latin-400-normal-[^/]*\.woff2$/,
  /\/eb-garamond-latin-wght-normal-[^/]*\.woff2$/,
];

/** The parts of Vite's build manifest this script reads. */
interface ManifestChunk {
  file: string;
  isEntry?: boolean;
  css?: string[];
  assets?: string[];
}

/**
 * The app's stylesheet and the fonts to preload, as Vite's build manifest
 * lists them for the index.html entry, the city and church pages' map script, and the
 * church index's search script. The static pages link only that one
 * stylesheet, so the build fails if any CSS lands elsewhere (say, a
 * lazy-loaded route importing its own), or a font or a script goes missing,
 * rather than shipping pages without them.
 */
function discoverAssets(): {
  cssPath: string;
  fontPaths: string[];
  cityMapScript: string;
  churchIndexScript: string;
} {
  if (!existsSync(MANIFEST_PATH)) {
    throw new Error(`${MANIFEST_PATH} is missing. Run \`vite build\` first.`);
  }
  const manifest = JSON.parse(readFileSync(MANIFEST_PATH, "utf-8")) as Record<
    string,
    ManifestChunk
  >;
  const entry = manifest["index.html"];
  if (!entry) throw new Error("Vite's manifest has no index.html entry.");

  const css = entry.css ?? [];
  if (css.length !== 1) {
    throw new Error(
      `Expected index.html to build to one stylesheet, found ${css.length}: ${css.join(", ")}`,
    );
  }
  const strays = Object.entries(manifest).filter(
    ([key, chunk]) => key !== "index.html" && chunk.css?.length,
  );
  if (strays.length > 0) {
    throw new Error(
      "Static pages link only index.html's stylesheet, but these chunks have their own CSS: " +
        strays.map(([key, chunk]) => `${key} (${chunk.css!.join(", ")})`).join("; "),
    );
  }

  const assets = (entry.assets ?? []).map((file) => `/${file}`);
  const fontPaths = PRELOAD_FONTS.map((pattern) => {
    const match = assets.find((path) => pattern.test(path));
    if (!match) throw new Error(`Could not find a font matching ${pattern} in Vite's manifest`);
    return match;
  });

  const cityMap = manifest[CITY_MAP_ENTRY];
  if (!cityMap?.isEntry) throw new Error(`Vite's manifest has no ${CITY_MAP_ENTRY} entry.`);
  const churchIndex = manifest[CHURCH_INDEX_ENTRY];
  if (!churchIndex?.isEntry) throw new Error(`Vite's manifest has no ${CHURCH_INDEX_ENTRY} entry.`);

  return {
    cssPath: `/${css[0]}`,
    fontPaths,
    cityMapScript: `/${cityMap.file}`,
    churchIndexScript: `/${churchIndex.file}`,
  };
}

/**
 * Points the page's Map links at the map as the visitor left it, which the
 * app keeps in sessionStorage (src/hooks/useHomeHref.ts); a prerendered page
 * can only render a bare "/".
 */
const HOME_LINK_SCRIPT =
  "try{var s=sessionStorage.getItem(" +
  JSON.stringify(HOME_SEARCH_KEY) +
  ");if(s)document.addEventListener(\"DOMContentLoaded\",function(){" +
  `document.querySelectorAll("[${HOME_LINK_ATTRIBUTE}]").forEach(function(a){a.href="/"+s})` +
  "})}catch(e){}";

/**
 * Adds HOME_LINK_SCRIPT to the page's head, so its Map links open the map
 * where the visitor left it. Added after a page is dated (see datePage): the
 * script is not what the page says, so it stays out of the lastmod hash.
 */
function withHomeLinkScript(html: string): string {
  if (!html.includes("</head>")) throw new Error("A prerendered page has no </head>.");
  return html.replace("</head>", `<script>${HOME_LINK_SCRIPT}</script></head>`);
}

function escapeXml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function canonicalUrlForChurchSlug(origin: string, slug: string): string {
  return absoluteUrl(origin, churchPath(slug));
}

function isAboutPageEnabledAtBuild(): boolean {
  // Read the way `vite build` reads it for the bundle (.env.production files,
  // then the process environment), so the /about route and about.html agree.
  const v = loadEnv("production", WEB_DIR, "VITE_").VITE_ABOUT_PAGE_ENABLED?.trim().toLowerCase();
  return v === "true" || v === "1";
}

/** A sitemap entry; `lastmod` is left out where no honest date exists. */
interface SitemapUrl {
  path: string;
  lastmod?: string;
}

function writeSitemapAndRobots(distDir: string, origin: string, pages: SitemapUrl[]): number {
  const urls = [...pages];
  // Not /landing, which is noindex (see writeShellCopies). /about is rendered
  // by the app bundle, so it has no prerendered content to date.
  if (isAboutPageEnabledAtBuild()) urls.push({ path: "/about" });

  const urlEntries = urls
    .map(
      (u) =>
        `  <url>\n    <loc>${escapeXml(absoluteUrl(origin, u.path))}</loc>\n` +
        (u.lastmod ? `    <lastmod>${u.lastmod}</lastmod>\n` : "") +
        "  </url>",
    )
    .join("\n");

  const sitemap =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    `${urlEntries}\n` +
    `</urlset>\n`;

  writeFileSync(resolve(distDir, "sitemap.xml"), sitemap, "utf-8");

  const sitemapUrl = absoluteUrl(origin, "/sitemap.xml");
  const robots =
    "User-agent: *\n" +
    "Allow: /\n" +
    "\n" +
    `Sitemap: ${sitemapUrl}\n`;

  writeFileSync(resolve(distDir, "robots.txt"), robots, "utf-8");
  return urls.length;
}

const SHELL_CANONICAL = /<link rel="canonical" href="[^"]*"\s*\/?>/;
const SHELL_OG_URL = /<meta property="og:url" content="[^"]*"\s*\/?>/;

/** Replaces one tag in the SPA shell, failing the build if index.html stops
 *  carrying it rather than shipping a page with the homepage's tag. */
function replaceShellTag(html: string, pattern: RegExp, replacement: string): string {
  if (!pattern.test(html)) {
    throw new Error(`index.html no longer matches ${pattern}; update prerender.ts`);
  }
  return html.replace(pattern, replacement);
}

/** The shell marked noindex, without the homepage's canonical or og:url. */
function noindexShell(shell: string): string {
  const html = replaceShellTag(shell, SHELL_CANONICAL, '<meta name="robots" content="noindex" />');
  return replaceShellTag(html, SHELL_OG_URL, "");
}

/**
 * Writes the copies of the SPA shell (dist/client/index.html) that the
 * client-rendered routes are served from. wrangler.jsonc serves 404.html,
 * with a 404 status, for any URL no file matches, so every page the app
 * routes to needs a file of its own: `/landing` is served from landing.html.
 *
 * /landing, an alternate entry point that overlaps the homepage, is noindex.
 * 404.html is the shell too, so the router still renders the right "not
 * found" page (church, city or generic), and is noindex as well.
 */
function writeShellCopies(distDir: string, origin: string): void {
  const shell = readFileSync(resolve(distDir, "index.html"), "utf-8");
  writeFileSync(resolve(distDir, "landing.html"), noindexShell(shell), "utf-8");
  if (isAboutPageEnabledAtBuild()) {
    const url = absoluteUrl(origin, "/about");
    let html = replaceShellTag(shell, SHELL_CANONICAL, `<link rel="canonical" href="${url}" />`);
    html = replaceShellTag(html, SHELL_OG_URL, `<meta property="og:url" content="${url}" />`);
    writeFileSync(resolve(distDir, "about.html"), html, "utf-8");
  }
  writeFileSync(resolve(distDir, "404.html"), noindexShell(shell), "utf-8");
  console.log("Wrote 404.html and the SPA shell pages.");
}

/**
 * The page dates the live site published with its last build, or null (every
 * page is then dated today, as if new). LASTMOD_BASELINE_URL points it
 * elsewhere, e.g. at a local file server when testing.
 */
async function fetchPreviousDates(origin: string): Promise<LastmodManifest | null> {
  const url = process.env.LASTMOD_BASELINE_URL || absoluteUrl(origin, `/${LASTMOD_FILE}`);
  // A failure here redates every page for good once the build deploys, so
  // network errors, timeouts and 5xx get retried. A 404, or a response that
  // isn't a manifest, is an answer (no dates published yet): not retried.
  const attempts = 3;
  let failure = "";
  for (let attempt = 1; attempt <= attempts; attempt++) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(15_000) });
      if (res.status >= 500) throw new Error(`HTTP ${res.status}`);
      if (!res.ok) {
        failure = `HTTP ${res.status}`;
        break;
      }
      const manifest = parseLastmodManifest(await res.text());
      if (!manifest) {
        failure = "not a page-date manifest";
        break;
      }
      console.log(`Read ${Object.keys(manifest.pages).length} page dates from ${url}.`);
      return manifest;
    } catch (error) {
      failure = String(error);
      if (attempt < attempts) await new Promise((done) => setTimeout(done, attempt * 2_000));
    }
  }
  console.warn(
    `Warning: couldn't read the previous page dates from ${url} (${failure}), ` +
      "so every page is dated today.",
  );
  return null;
}

async function main() {
  if (!existsSync(SNAPSHOT_PATH)) {
    // The snapshot is published data, not source: it is downloaded, not committed.
    throw new Error(
      `${SNAPSHOT_PATH} is missing. Run \`pnpm data:pull --snapshot-only\` from the repo root first.`,
    );
  }
  const snapshot = parseSnapshot(gunzipSync(readFileSync(SNAPSHOT_PATH)).toString("utf-8"));

  const { cssPath, fontPaths, cityMapScript, churchIndexScript } = discoverAssets();
  const slugs = snapshot.churches.map((church) => church.slug);
  const origin = SITE_ORIGIN;

  console.log(`Pre-rendering ${slugs.length} church pages...`);

  // The snapshot has no per-church modification dates, so a page is dated by
  // when its rendered content last changed (src/lib/lastmod.ts): it keeps the
  // previous build's date unless its hash differs. The date feeds both the
  // sitemap's <lastmod> and the page's JSON-LD dateModified.
  const buildDate = new Date().toISOString().slice(0, 10);
  const previousDates = await fetchPreviousDates(origin);
  const assetPaths = [cssPath, ...fontPaths, cityMapScript, churchIndexScript];
  const pageDates: Record<string, LastmodEntry> = {};
  /** Dates a page rendered with LASTMOD_PLACEHOLDER and returns its final HTML. */
  const datePage = (path: string, html: string): string => {
    const hash = createHash("sha256")
      .update(contentForHash(html, assetPaths))
      .digest("hex")
      .slice(0, 16);
    const lastmod = resolveLastmod(previousDates?.pages[path], hash, buildDate);
    pageDates[path] = { hash, lastmod };
    return withHomeLinkScript(html.split(LASTMOD_PLACEHOLDER).join(lastmod));
  };

  // Calendar files aren't pages: no sitemap entry or date, and they may
  // change every build (weekly events recur from the build day).
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const uidDomain = new URL(origin).hostname;
  let calendarCount = 0;

  let count = 0;
  for (const slug of slugs) {
    const church = findChurch(snapshot, slug);
    const events = churchSchedule(snapshot, slug, EVENT_TYPE_ORDER);

    const html = datePage(
      churchPath(slug),
      "<!DOCTYPE html>" +
        renderToStaticMarkup(
          createElement(StaticChurchPage, {
            church,
            city: churchCity(snapshot, church),
            map: churchMapData(snapshot, church),
            events,
            cssPath,
            fontPaths,
            cityMapScript,
            canonicalUrl: canonicalUrlForChurchSlug(origin, slug),
            lastModified: LASTMOD_PLACEHOLDER,
          }),
        ),
    );

    const outDir = resolve(DIST_DIR, "churches", slug);
    mkdirSync(outDir, { recursive: true });
    writeFileSync(resolve(outDir, "index.html"), html, "utf-8");
    // ChurchPageContent links the file only when the page lists times.
    if (events.length > 0) {
      const calendar = buildChurchCalendar(church, events, {
        pageUrl: canonicalUrlForChurchSlug(origin, slug),
        uidDomain,
        now,
        today,
      });
      writeFileSync(resolve(outDir, CHURCH_CALENDAR_FILE), calendar, "utf-8");
      calendarCount++;
    }
    count++;
  }

  const cityCenters = cityCentersJson as CityCenters;
  const { cities } = cityIndex(snapshot, cityCenters);

  const indexHtml = datePage(
    CHURCH_INDEX_PATH,
    "<!DOCTYPE html>" +
      renderToStaticMarkup(
        createElement(StaticChurchIndexPage, {
          churches: snapshot.churches,
          cities,
          cssPath,
          fontPaths,
          churchIndexScript,
          canonicalUrl: absoluteUrl(origin, CHURCH_INDEX_PATH),
          lastModified: LASTMOD_PLACEHOLDER,
        }),
      ),
  );
  mkdirSync(resolve(DIST_DIR, "churches"), { recursive: true });
  writeFileSync(resolve(DIST_DIR, "churches", "index.html"), indexHtml, "utf-8");
  console.log("Wrote churches/index.html (all-churches index).");

  const ungeocoded = cities.filter((city) => !city.geocodedCenter);
  if (ungeocoded.length > 0) {
    console.warn(
      `Warning: ${ungeocoded.length} cities have no geocoded center, so their ` +
        "nearby churches are measured from their own churches' mean position. " +
        "Run `pnpm geocode:cities` and commit src/data/cityCenters.json: " +
        ungeocoded.map((city) => city.slug).join(", "),
    );
  }
  const citySlugs = cities.map((city) => city.slug);
  for (const citySlug of citySlugs) {
    const path = cityPath(citySlug);
    const html = datePage(
      path,
      "<!DOCTYPE html>" +
        renderToStaticMarkup(
          createElement(StaticCityPage, {
            data: cityPageData(snapshot, citySlug, cityCenters),
            cssPath,
            fontPaths,
            cityMapScript,
            canonicalUrl: absoluteUrl(origin, path),
          }),
        ),
    );
    const outDir = resolve(DIST_DIR, "mass-times", citySlug);
    mkdirSync(outDir, { recursive: true });
    writeFileSync(resolve(outDir, "index.html"), html, "utf-8");
  }
  console.log(`Pre-rendered ${citySlugs.length} city pages.`);

  writeShellCopies(DIST_DIR, origin);

  // The homepage is the app over the whole dataset, so it changes whenever
  // any prerendered page does.
  const datedPaths = Object.keys(pageDates);
  const homeLastmod = latestDate(
    datedPaths.map((path) => pageDates[path].lastmod),
    buildDate,
  );
  const urlCount = writeSitemapAndRobots(DIST_DIR, origin, [
    { path: "/", lastmod: homeLastmod },
    ...datedPaths.map((path) => ({ path, lastmod: pageDates[path].lastmod })),
  ]);
  console.log(`Wrote sitemap.xml and robots.txt (${urlCount} URLs).`);

  const manifest: LastmodManifest = { version: 1, pages: pageDates };
  writeFileSync(resolve(DIST_DIR, LASTMOD_FILE), JSON.stringify(manifest), "utf-8");
  const changed = datedPaths.filter((path) => pageDates[path].lastmod === buildDate);
  console.log(
    `Wrote ${LASTMOD_FILE}: ${changed.length} of ${datedPaths.length} pages dated ${buildDate}.`,
  );

  console.log(`Pre-rendered ${count} church pages and ${calendarCount} calendar files.`);
}

await main();
