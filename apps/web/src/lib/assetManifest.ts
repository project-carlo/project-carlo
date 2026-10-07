/**
 * Keeps the previous builds' hashed assets live across deploys.
 *
 * Each deploy replaces the asset set wholesale, so a page loaded before it
 * 404s on the lazy chunks (`/assets/HomePage-<hash>.js`) its old entry script
 * still names. Instead each build publishes `asset-manifest.json` listing every
 * file under `assets/` with the date it left the build, and the next build
 * (scripts/carry-assets.ts) downloads the files retired less than
 * RETENTION_DAYS ago from the live site back into its own output, so they
 * deploy again.
 */

export const ASSET_MANIFEST_FILE = "asset-manifest.json";

/** How long a file that left the build stays live. */
export const RETENTION_DAYS = 14;

/** The most files a deploy will hold. Workers Free allows 20,000 per version;
 *  the rest is headroom for the build's own growth. */
export const MAX_DEPLOY_FILES = 15_000;

export interface AssetEntry {
  /** ISO date the file left the build; null while the current build has it. */
  retired: string | null;
}

/** Keyed by path relative to the site root, e.g. `assets/HomePage-1a2b3c.js`. */
export interface AssetManifest {
  version: 1;
  files: Record<string, AssetEntry>;
}

const DAY_MS = 24 * 60 * 60 * 1000;
const ASSET_PATH = /^assets\/(?:[\w.@+~-]+\/)*[\w.@+~-]+$/;

/** Only plain paths under `assets/` are ever fetched and written, whatever a
 *  manifest says. */
export function isAssetPath(path: string): boolean {
  return ASSET_PATH.test(path) && !path.split("/").includes("..");
}

/** The live site's manifest, or null when it is missing or malformed — which
 *  only costs the carry-over, never the deploy. */
export function parseAssetManifest(text: string): AssetManifest | null {
  let data: unknown;
  try {
    data = JSON.parse(text);
  } catch {
    return null;
  }
  if (typeof data !== "object" || data === null) return null;
  const { version, files } = data as Partial<AssetManifest>;
  if (version !== 1 || typeof files !== "object" || files === null) return null;
  const valid: Record<string, AssetEntry> = {};
  for (const [path, entry] of Object.entries(files)) {
    const retired = entry?.retired;
    const dated = typeof retired === "string" && Number.isFinite(Date.parse(retired));
    if (isAssetPath(path) && (retired === null || dated)) valid[path] = { retired };
  }
  return { version: 1, files: valid };
}

export interface CarryPlan {
  /** What to publish: the build's files, then the carried ones with their dates. */
  manifest: AssetManifest;
  /** In the live manifest but not the build, and still within the window: to download. */
  carry: string[];
  /** Retired RETENTION_DAYS or more ago. */
  expired: string[];
  /** Still within the window, but dropped to keep the deploy under the file cap. */
  capped: string[];
  /** In the build but not the live manifest. */
  added: string[];
}

/**
 * Merges the live manifest with the new build's files. A file in the build has
 * no retired date (so one that returns loses its date); one that just left it
 * is dated `now`, and kept while it is under RETENTION_DAYS old. `buildFileCount`
 * is every file the deploy holds before carrying, the manifest included. When
 * the carried files would take it past `maxFiles`, those retired earliest go
 * first. With no live manifest nothing is carried.
 */
export function planCarryOver(options: {
  built: readonly string[];
  live: AssetManifest | null;
  now: Date;
  buildFileCount: number;
  maxFiles?: number;
}): CarryPlan {
  const { built, live, now, buildFileCount, maxFiles = MAX_DEPLOY_FILES } = options;
  const builtSet = new Set(built);
  const files: Record<string, AssetEntry> = {};
  for (const path of [...builtSet].sort()) files[path] = { retired: null };

  const added = [...builtSet].filter((path) => !live || !(path in live.files)).sort();
  const expired: string[] = [];
  const candidates: { path: string; retired: string }[] = [];
  for (const [path, entry] of Object.entries(live?.files ?? {})) {
    if (builtSet.has(path)) continue;
    const retired = entry.retired ?? now.toISOString();
    if (now.getTime() - Date.parse(retired) >= RETENTION_DAYS * DAY_MS) expired.push(path);
    else candidates.push({ path, retired });
  }

  // Newest first, so the cap keeps the most recently retired.
  candidates.sort(
    (a, b) => Date.parse(b.retired) - Date.parse(a.retired) || a.path.localeCompare(b.path),
  );
  const room = Math.max(0, maxFiles - buildFileCount);
  const kept = candidates.slice(0, room);
  const capped = candidates.slice(room).map(({ path }) => path);
  for (const { path, retired } of kept) files[path] = { retired };

  return {
    manifest: { version: 1, files },
    carry: kept.map(({ path }) => path).sort(),
    expired: expired.sort(),
    capped: capped.sort(),
    added,
  };
}
