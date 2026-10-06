import { gunzipSync } from "node:zlib";
import { existsSync, readFileSync, mkdirSync, writeFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";
import { renderToStaticMarkup } from "react-dom/server";
import { createElement } from "react";
import { churchSchedule, cityIndex, cityPageData, findChurch } from "../src/api";
import { cityPath, type CityCenters } from "../src/lib/cities";
import cityCentersJson from "../src/data/cityCenters.json";
import { parseSnapshot, SNAPSHOT_FILE } from "../src/lib/snapshot";
import { StaticChurchPage } from "../src/prerender/StaticChurchPage";
import { StaticChurchIndexPage } from "../src/prerender/StaticChurchIndexPage";
import { StaticCityPage } from "../src/prerender/StaticCityPage";
import { CHURCH_INDEX_PATH } from "../src/lib/seo";
import { EVENT_TYPE_ORDER } from "../src/constants/eventTypes";

const WEB_DIR = resolve(import.meta.dirname, "..");
// The Cloudflare Vite plugin puts the browser build in dist/client, beside
// the Worker's own bundle.
const DIST_DIR = resolve(WEB_DIR, "dist", "client");
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
    throw new Error("Could not find built CSS file in dist/client/assets/");
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
  citySlugs: string[],
  buildDate: string,
): number {
  const urls: { loc: string; lastmod: string }[] = [
    { loc: absoluteUrl(origin, "/"), lastmod: buildDate },
    { loc: absoluteUrl(origin, "/landing"), lastmod: buildDate },
    { loc: absoluteUrl(origin, CHURCH_INDEX_PATH), lastmod: buildDate },
    ...slugs.map((slug) => ({
      loc: canonicalUrlForChurchSlug(origin, slug),
      lastmod: buildDate,
    })),
    ...citySlugs.map((slug) => ({
      loc: absoluteUrl(origin, cityPath(slug)),
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

  console.log(`Pre-rendering ${slugs.length} church pages...`);

  // The snapshot has no per-church modification dates, so the pages' JSON-LD
  // dateModified and the sitemap's <lastmod> are the build date.
  const buildDate = new Date().toISOString().slice(0, 10);

  let count = 0;
  for (const slug of slugs) {
    const church = findChurch(snapshot, slug);
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
      }),
    );
  mkdirSync(resolve(DIST_DIR, "churches"), { recursive: true });
  writeFileSync(resolve(DIST_DIR, "churches", "index.html"), indexHtml, "utf-8");
  console.log("Wrote churches/index.html (all-parishes index).");

  const cityCenters = cityCentersJson as CityCenters;
  const { cities } = cityIndex(snapshot, cityCenters);
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
    const html =
      "<!DOCTYPE html>" +
      renderToStaticMarkup(
        createElement(StaticCityPage, {
          data: cityPageData(snapshot, citySlug, cityCenters),
          cssPath,
          fontPaths,
          canonicalUrl: absoluteUrl(origin, path),
        }),
      );
    const outDir = resolve(DIST_DIR, "mass-times", citySlug);
    mkdirSync(outDir, { recursive: true });
    writeFileSync(resolve(outDir, "index.html"), html, "utf-8");
  }
  console.log(`Pre-rendered ${citySlugs.length} city pages.`);

  const urlCount = writeSitemapAndRobots(DIST_DIR, origin, slugs, citySlugs, buildDate);
  console.log(`Wrote sitemap.xml and robots.txt (${urlCount} URLs).`);

  console.log(`Pre-rendered ${count} church pages.`);
}

main();
