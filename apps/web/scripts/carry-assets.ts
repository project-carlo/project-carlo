import { appendFileSync, existsSync, mkdirSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { SITE_ORIGIN, absoluteUrl } from "../src/lib/seo";
import {
  ASSET_MANIFEST_FILE,
  MAX_DEPLOY_FILES,
  RETENTION_DAYS,
  parseAssetManifest,
  planCarryOver,
  type AssetManifest,
} from "../src/lib/assetManifest";

// The Cloudflare Vite plugin puts the browser build in dist/client, and
// wrangler.jsonc's assets deploy exactly that directory.
const DIST_DIR = resolve(import.meta.dirname, "..", "dist", "client");
const ASSETS_DIR = resolve(DIST_DIR, "assets");
const CONCURRENCY = 8;
const TIMEOUT_MS = 30_000;

/** Every file under a directory, as `/`-separated paths relative to `root`. */
function listFiles(root: string, dir = root): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    return entry.isDirectory()
      ? listFiles(root, path)
      : [path.slice(root.length + 1).split("\\").join("/")];
  });
}

/** One attempt: the response body, or why it was rejected. Only a 200 that
 *  isn't HTML is a file: a missing asset answers with 404.html, and an SPA
 *  fallback would answer 200 with a page. */
async function fetchOnce(
  url: string,
): Promise<{ body: Buffer } | { error: string; retry: boolean }> {
  try {
    const res = await fetch(url, { signal: AbortSignal.timeout(TIMEOUT_MS), cache: "no-store" });
    if (res.status >= 500) return { error: `HTTP ${res.status}`, retry: true };
    if (res.status !== 200) return { error: `HTTP ${res.status}`, retry: false };
    const type = res.headers.get("content-type") ?? "";
    if (/^text\/html\b/i.test(type)) return { error: `unexpected ${type}`, retry: false };
    return { body: Buffer.from(await res.arrayBuffer()) };
  } catch (error) {
    return { error: String(error), retry: true };
  }
}

/** Fetches with one retry for network errors, timeouts and 5xx; an answer
 *  that isn't a file (404, HTML) is final. */
async function fetchWithRetry(url: string): Promise<{ body: Buffer } | { error: string }> {
  let result = await fetchOnce(url);
  if ("error" in result && result.retry) {
    await new Promise((done) => setTimeout(done, 1_000));
    result = await fetchOnce(url);
  }
  return result;
}

/**
 * The asset manifest the live site published with its last deploy, or null (the
 * first deploy, the site down, or a response that isn't a manifest): nothing is
 * then carried, and this build's manifest starts the chain again.
 */
async function fetchLiveManifest(origin: string): Promise<AssetManifest | null> {
  const url = absoluteUrl(origin, `/${ASSET_MANIFEST_FILE}`);
  const result = await fetchWithRetry(url);
  if ("error" in result) {
    console.warn(`Warning: couldn't read ${url} (${result.error}), so nothing is carried over.`);
    return null;
  }
  const manifest = parseAssetManifest(result.body.toString("utf-8"));
  if (!manifest) {
    console.warn(`Warning: ${url} isn't an asset manifest, so nothing is carried over.`);
    return null;
  }
  console.log(`Read ${Object.keys(manifest.files).length} assets from ${url}.`);
  return manifest;
}

/** Downloads the files into the build, a few at a time; returns those that failed. */
async function download(origin: string, paths: string[]): Promise<string[]> {
  const failed: string[] = [];
  const queue = [...paths];
  const worker = async () => {
    for (let path = queue.shift(); path !== undefined; path = queue.shift()) {
      const result = await fetchWithRetry(absoluteUrl(origin, `/${path}`));
      if ("error" in result) {
        console.warn(`Warning: skipped ${path} (${result.error}).`);
        failed.push(path);
        continue;
      }
      const target = resolve(DIST_DIR, path);
      mkdirSync(dirname(target), { recursive: true });
      writeFileSync(target, result.body);
    }
  };
  await Promise.all(Array.from({ length: Math.min(CONCURRENCY, paths.length) }, worker));
  return failed.sort();
}

async function main() {
  if (!existsSync(ASSETS_DIR)) {
    throw new Error(`${ASSETS_DIR} is missing. Run \`pnpm --filter web build\` first.`);
  }
  const manifestPath = resolve(DIST_DIR, ASSET_MANIFEST_FILE);
  if (existsSync(manifestPath)) {
    // Carried files already in assets/ would read as this build's own.
    throw new Error(`${manifestPath} already exists: this build was carried into once. Rebuild first.`);
  }
  const origin = (process.env.CARRY_ASSETS_ORIGIN || SITE_ORIGIN).replace(/\/+$/, "");

  const built = listFiles(ASSETS_DIR).map((file) => `assets/${file}`);
  // The manifest itself is one more file in the deploy.
  const buildFileCount = listFiles(DIST_DIR).length + 1;
  const live = await fetchLiveManifest(origin);
  const plan = planCarryOver({ built, live, now: new Date(), buildFileCount });

  for (const path of plan.capped) {
    console.warn(`Warning: dropped ${path}, over the ${MAX_DEPLOY_FILES} file cap.`);
  }
  const failed = await download(origin, plan.carry);
  for (const path of failed) delete plan.manifest.files[path];

  writeFileSync(manifestPath, JSON.stringify(plan.manifest), "utf-8");

  const carried = plan.carry.length - failed.length;
  const counts = {
    new: plan.added.length,
    carried,
    expired: plan.expired.length,
    capped: plan.capped.length,
    failed: failed.length,
    "total files": listFiles(DIST_DIR).length,
  };
  const line = Object.entries(counts)
    .map(([name, n]) => `${n} ${name}`)
    .join(", ");
  console.log(`Wrote ${ASSET_MANIFEST_FILE}: ${line}.`);
  if (process.env.GITHUB_STEP_SUMMARY) {
    appendFileSync(
      process.env.GITHUB_STEP_SUMMARY,
      [
        "### Carried-over assets",
        "",
        `Files retired less than ${RETENTION_DAYS} days ago stay live.`,
        "",
        "| New | Carried | Expired | Over cap | Failed | Total files |",
        "| --: | --: | --: | --: | --: | --: |",
        `| ${Object.values(counts).join(" | ")} |`,
        "",
      ].join("\n"),
    );
  }
}

await main();
