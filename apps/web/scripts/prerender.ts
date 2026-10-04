import { gunzipSync } from "node:zlib";
import { existsSync, readFileSync, mkdirSync, writeFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { renderToStaticMarkup } from "react-dom/server";
import { createElement } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";
import { churchSchedule, findChurch } from "../src/api";
import type { ChurchBase } from "../src/types";
import { parseSnapshot, SNAPSHOT_FILE } from "../src/lib/snapshot";
import { StaticChurchPage } from "../src/prerender/StaticChurchPage";
import { StaticChurchIndexPage } from "../src/prerender/StaticChurchIndexPage";
import {
  StaticBrowsePage,
  type BrowseModel,
} from "../src/prerender/StaticBrowsePage";
import { LandingPage } from "../src/views/LandingPage";
import {
  CHURCH_INDEX_PATH,
  HOME_DESCRIPTION,
  HOME_TITLE,
  MAP_DESCRIPTION,
  MAP_TITLE,
} from "../src/lib/seo";
import {
  MAIN_CITY_MIN_CHURCHES,
  citiesWithAtLeast,
  cityPath,
  dioceseKeyForChurch,
  placesCities,
} from "../src/lib/places";
import {
  buildBrowseEntries,
  buildChurchPlaceContext,
  buildCityModel,
  buildDioceseIndex,
  buildDioceseModel,
  buildStateModel,
  cityPageGroups,
  createPlaceIndex,
  statesIn,
  type PlaceIndex,
} from "../src/lib/browse";
import { EVENT_TYPE_ORDER } from "../src/constants/eventTypes";

const WEB_DIR = resolve(import.meta.dirname, "..");
const DIST_DIR = resolve(WEB_DIR, "dist");
const SNAPSHOT_PATH = resolve(WEB_DIR, "public", SNAPSHOT_FILE);
const SITE_ORIGIN = "https://projectcarlo.com";

/** Font filename prefixes to preload — Latin subsets of the two typefaces used
 *  on church pages (Cardo for display headings, EB Garamond for body text). */
const PRELOAD_FONT_PREFIXES = [
  "cardo-latin-400-normal-",
  "eb-garamond-latin-wght-normal-",
];

function discoverAssets(): { cssPath: string; fontPaths: string[] } {
  const assetsDir = resolve(DIST_DIR, "assets");
  const files = readdirSync(assetsDir);

  const cssFile = files.find((f) => f.startsWith("index-") && f.endsWith(".css"));
  if (!cssFile) {
    throw new Error("Could not find built CSS file in dist/assets/");
  }

  const fontPaths = PRELOAD_FONT_PREFIXES.map((prefix) => {
    const match = files.find((f) => f.startsWith(prefix) && f.endsWith(".woff2"));
    if (!match) throw new Error(`Could not find font file matching ${prefix}*.woff2`);
    return `/assets/${match}`;
  });

  return { cssPath: `/assets/${cssFile}`, fontPaths };
}

function getSiteOrigin(): string {
  return new URL(SITE_ORIGIN).origin;
}

function escapeXml(text: string): string {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function absoluteUrl(origin: string, pathname: string): string {
  return new URL(pathname, `${origin}/`).href;
}

function canonicalPathForChurchSlug(slug: string): string {
  return `/churches/${encodeURIComponent(slug)}/`;
}

function canonicalUrlForChurchSlug(origin: string, slug: string): string {
  return absoluteUrl(origin, canonicalPathForChurchSlug(slug));
}

function isAboutPageEnabledAtBuild(): boolean {
  const v = process.env.VITE_ABOUT_PAGE_ENABLED?.trim().toLowerCase();
  return v === "true" || v === "1";
}

function writeSitemapAndRobots(
  distDir: string,
  origin: string,
  slugs: string[],
  browsePaths: string[],
  buildDate: string,
): number {
  const urls: { loc: string; lastmod: string }[] = [
    { loc: absoluteUrl(origin, "/"), lastmod: buildDate },
    { loc: absoluteUrl(origin, "/map"), lastmod: buildDate },
    { loc: absoluteUrl(origin, CHURCH_INDEX_PATH), lastmod: buildDate },
    ...browsePaths.map((path) => ({
      loc: absoluteUrl(origin, path),
      lastmod: buildDate,
    })),
    ...slugs.map((slug) => ({
      loc: canonicalUrlForChurchSlug(origin, slug),
      lastmod: buildDate,
    })),
  ];
  if (isAboutPageEnabledAtBuild()) {
    urls.push({ loc: absoluteUrl(origin, "/about"), lastmod: buildDate });
  }

  const urlEntries = urls
    .map(
      (u) => `  <url>
    <loc>${escapeXml(u.loc)}</loc>
    <lastmod>${u.lastmod}</lastmod>
  </url>`,
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

function escapeAttr(text: string): string {
  return escapeXml(text);
}

/**
 * The `index.html` Vite built is the SPA shell. Point its head at another
 * route: title, description, canonical and the matching og/twitter tags.
 */
function retargetShell(
  shell: string,
  meta: { title: string; description: string; canonicalUrl: string },
): string {
  const title = escapeAttr(meta.title);
  const description = escapeAttr(meta.description);
  const canonical = escapeAttr(meta.canonicalUrl);
  const setContent = (html: string, attr: string, value: string) =>
    html.replace(
      new RegExp(`(<meta\\s+(?:name|property)="${attr}"\\s+content=")[^"]*(")`),
      `$1${value}$2`,
    );
  let out = shell.replace(/<title>[^<]*<\/title>/, `<title>${title}</title>`);
  out = out.replace(
    /(<link rel="canonical" href=")[^"]*(")/,
    `$1${canonical}$2`,
  );
  for (const attr of ["og:title", "twitter:title"]) out = setContent(out, attr, title);
  for (const attr of ["description", "og:description", "twitter:description"]) {
    out = setContent(out, attr, description);
  }
  return setContent(out, "og:url", canonical);
}

/** Clears the prerendered landing markup on any path but `/`, before first
 *  paint, so client routes served by the SPA fallback (index.html) don't
 *  flash the home page. */
const CLEAR_LANDING_ON_OTHER_PATHS =
  `<script>if(location.pathname!=="/"){document.getElementById("root").innerHTML=""}</script>`;

/**
 * `/` and `/map`.
 *
 *  - dist/index.html: the SPA shell with the landing page rendered into #root,
 *    so `/` is real HTML (the browse links included) for crawlers. The client
 *    uses createRoot, which simply replaces that markup. index.html is also
 *    what the Worker's SPA fallback serves for client-only routes, hence the
 *    inline guard above.
 *  - dist/map.html: the pristine shell with /map's head, served at `/map`
 *    (Workers static assets resolve `/map` to `map.html`).
 */
function writeHomeAndMapShells(origin: string, showAbout: boolean) {
  const shellPath = resolve(DIST_DIR, "index.html");
  const shell = readFileSync(shellPath, "utf-8");
  if (!shell.includes('<div id="root"></div>')) {
    throw new Error('dist/index.html has no empty <div id="root"></div> to render into.');
  }

  const landing = renderToStaticMarkup(
    createElement(
      QueryClientProvider,
      { client: new QueryClient() },
      createElement(
        MemoryRouter,
        { initialEntries: ["/"] },
        createElement(LandingPage, { showAbout }),
      ),
    ),
  );

  // The shell's own head already carries the home title/description/canonical.
  const home = retargetShell(shell, {
    title: HOME_TITLE,
    description: HOME_DESCRIPTION,
    canonicalUrl: absoluteUrl(origin, "/"),
  }).replace(
    '<div id="root"></div>',
    `<div id="root">${landing}</div>${CLEAR_LANDING_ON_OTHER_PATHS}`,
  );
  writeFileSync(shellPath, home, "utf-8");

  const map = retargetShell(shell, {
    title: MAP_TITLE,
    description: MAP_DESCRIPTION,
    canonicalUrl: absoluteUrl(origin, "/map"),
  });
  writeFileSync(resolve(DIST_DIR, "map.html"), map, "utf-8");
  console.log("Wrote index.html (prerendered landing) and map.html (SPA shell).");
}

/** Warn when the committed places.json has drifted from the data snapshot. */
function checkPlacesAgainstSnapshot(churches: ChurchBase[]) {
  const unmapped = churches.filter((c) => !dioceseKeyForChurch(c.slug));
  if (unmapped.length > 0) {
    console.warn(
      `places.json has no diocese for ${unmapped.length} snapshot churches ` +
        `(run \`pnpm places:gen\`?): ${unmapped.map((c) => c.slug).join(", ")}`,
    );
  }
  const fromSnapshot = citiesWithAtLeast(churches, MAIN_CITY_MIN_CHURCHES).length;
  const fromPlaces = placesCities(MAIN_CITY_MIN_CHURCHES).length;
  if (fromSnapshot !== fromPlaces) {
    console.warn(
      `main-city count differs: snapshot ${fromSnapshot}, places.json ${fromPlaces} ` +
        "(run `pnpm places:gen`?)",
    );
  }
}

/** `dist/{path}/index.html` for a site path like `/mass-times/ny/troy/`. */
function writePage(path: string, html: string) {
  const dir = resolve(DIST_DIR, path.replace(/^\/+|\/+$/g, ""));
  mkdirSync(dir, { recursive: true });
  writeFileSync(resolve(dir, "index.html"), html, "utf-8");
}

/**
 * The browse pages: diocese index, one page per diocese, the state hub and a
 * page for every city with enough churches. Returns the paths written (for the
 * sitemap).
 */
function writeBrowsePages(
  index: PlaceIndex,
  cssPath: string,
  fontPaths: string[],
  origin: string,
  buildDate: string,
  showAbout: boolean,
): string[] {
  const models: BrowseModel[] = [buildDioceseIndex(index)];
  for (const card of buildDioceseIndex(index).cards) {
    const model = buildDioceseModel(index, card.diocese.key);
    if (model) models.push(model);
  }
  for (const state of statesIn(index)) {
    const model = buildStateModel(index, state);
    if (model) models.push(model);
  }
  for (const group of cityPageGroups(index)) {
    const model = buildCityModel(index, group.state, group.slug);
    if (model) models.push(model);
  }

  for (const model of models) {
    const html =
      "<!DOCTYPE html>" +
      renderToStaticMarkup(
        createElement(StaticBrowsePage, {
          model,
          cssPath,
          fontPaths,
          canonicalUrl: absoluteUrl(origin, model.path),
          lastModified: buildDate,
          showAbout,
        }),
      );
    writePage(model.path, html);
  }

  // Every city the footer and landing page link to must have a page.
  const written = new Set(models.map((m) => m.path));
  for (const c of placesCities()) {
    const path = cityPath(c.state, c.name);
    if (!written.has(path)) {
      console.warn(`places.json lists ${path} but no page was built (run \`pnpm places:gen\`?)`);
    }
  }

  const counts = (kind: BrowseModel["kind"]) => models.filter((m) => m.kind === kind).length;
  console.log(
    `Wrote ${models.length} browse pages ` +
      `(${counts("dioceses")} diocese index, ${counts("diocese")} dioceses, ` +
      `${counts("state")} state hub, ${counts("city")} cities).`,
  );
  return models.map((m) => m.path);
}

function main() {
  if (!existsSync(SNAPSHOT_PATH)) {
    // The snapshot is published data, not source: it is downloaded, not committed.
    throw new Error(
      `${SNAPSHOT_PATH} is missing. Run \`pnpm data:pull --snapshot-only\` from the repo root first.`,
    );
  }
  const snapshot = parseSnapshot(gunzipSync(readFileSync(SNAPSHOT_PATH)).toString("utf-8"));

  const { cssPath, fontPaths } = discoverAssets();
  const slugs = snapshot.churches.map((church) => church.slug);
  const origin = getSiteOrigin();
  const showAbout = isAboutPageEnabledAtBuild();
  checkPlacesAgainstSnapshot(snapshot.churches);
  const placeIndex = createPlaceIndex(
    buildBrowseEntries(snapshot.churches, (id) => snapshot.eventsOf(id)),
  );

  console.log(`Pre-rendering ${slugs.length} church pages...`);

  // The snapshot has no per-church modification dates, so the pages' JSON-LD
  // dateModified and the sitemap's <lastmod> are the build date.
  const buildDate = new Date().toISOString().slice(0, 10);

  let count = 0;
  for (const slug of slugs) {
    const church = findChurch(snapshot, slug);
    const place = buildChurchPlaceContext(placeIndex, church);
    const events = churchSchedule(snapshot, slug, EVENT_TYPE_ORDER);

    const html =
      "<!DOCTYPE html>" +
      renderToStaticMarkup(
        createElement(StaticChurchPage, {
          church,
          events,
          cssPath,
          fontPaths,
          canonicalUrl: canonicalUrlForChurchSlug(origin, slug),
          lastModified: buildDate,
          showAbout,
          place,
        }),
      );

    const outDir = resolve(DIST_DIR, "churches", slug);
    mkdirSync(outDir, { recursive: true });
    writeFileSync(resolve(outDir, "index.html"), html, "utf-8");
    count++;
  }

  const indexHtml =
    "<!DOCTYPE html>" +
    renderToStaticMarkup(
      createElement(StaticChurchIndexPage, {
        churches: snapshot.churches,
        cssPath,
        fontPaths,
        canonicalUrl: absoluteUrl(origin, CHURCH_INDEX_PATH),
        lastModified: buildDate,
        showAbout,
      }),
    );
  mkdirSync(resolve(DIST_DIR, "churches"), { recursive: true });
  writeFileSync(resolve(DIST_DIR, "churches", "index.html"), indexHtml, "utf-8");
  console.log("Wrote churches/index.html (all-parishes index).");

  const browsePaths = writeBrowsePages(
    placeIndex,
    cssPath,
    fontPaths,
    origin,
    buildDate,
    showAbout,
  );

  writeHomeAndMapShells(origin, showAbout);

  const urlCount = writeSitemapAndRobots(DIST_DIR, origin, slugs, browsePaths, buildDate);
  console.log(`Wrote sitemap.xml and robots.txt (${urlCount} URLs).`);

  console.log(`Pre-rendered ${count} church pages.`);
}

main();
