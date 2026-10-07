import { describe, expect, it } from "vitest";
import {
  MAX_DEPLOY_FILES,
  RETENTION_DAYS,
  isAssetPath,
  parseAssetManifest,
  planCarryOver,
  type AssetManifest,
} from "./assetManifest";

const NOW = new Date("2026-10-07T12:00:00.000Z");

/** An ISO date this many days before NOW. */
function daysAgo(days: number): string {
  return new Date(NOW.getTime() - days * 24 * 60 * 60 * 1000).toISOString();
}

function manifest(files: Record<string, string | null>): AssetManifest {
  return {
    version: 1,
    files: Object.fromEntries(Object.entries(files).map(([path, retired]) => [path, { retired }])),
  };
}

describe("parseAssetManifest", () => {
  it("reads a valid manifest", () => {
    const text = JSON.stringify(manifest({ "assets/a.js": null, "assets/b.js": daysAgo(3) }));
    expect(parseAssetManifest(text)).toEqual(
      manifest({ "assets/a.js": null, "assets/b.js": daysAgo(3) }),
    );
  });

  it("rejects what isn't a manifest", () => {
    expect(parseAssetManifest("<!DOCTYPE html>")).toBeNull();
    expect(parseAssetManifest("null")).toBeNull();
    expect(parseAssetManifest(JSON.stringify({ version: 2, files: {} }))).toBeNull();
    expect(parseAssetManifest(JSON.stringify({ version: 1 }))).toBeNull();
  });

  it("drops malformed entries and keeps the rest", () => {
    const text = JSON.stringify({
      version: 1,
      files: {
        "assets/ok.js": { retired: null },
        "assets/bad-date.js": { retired: "last week" },
        "assets/no-retired.js": {},
        "assets/null-entry.js": null,
        "../secret.js": { retired: null },
        "assets/../secret.js": { retired: null },
        "/assets/abs.js": { retired: null },
        "index.html": { retired: null },
      },
    });
    expect(parseAssetManifest(text)).toEqual(manifest({ "assets/ok.js": null }));
  });
});

describe("isAssetPath", () => {
  it("accepts files under assets/ and nothing that could leave it", () => {
    expect(isAssetPath("assets/HomePage-330_J145.js")).toBe(true);
    expect(isAssetPath("assets/fonts/cardo-latin-400-normal-ab12.woff2")).toBe(true);
    expect(isAssetPath("assets/")).toBe(false);
    expect(isAssetPath("assets/../index.html")).toBe(false);
    expect(isAssetPath("assets/a.js?x=1")).toBe(false);
    expect(isAssetPath("assets\\a.js")).toBe(false);
    expect(isAssetPath("other/a.js")).toBe(false);
  });
});

describe("planCarryOver", () => {
  const plan = (live: AssetManifest | null, built: string[], extra = {}) =>
    planCarryOver({ built, live, now: NOW, buildFileCount: built.length + 1, ...extra });

  it("carries a file that just left the build, dating it now", () => {
    const result = plan(manifest({ "assets/old.js": null, "assets/same.js": null }), [
      "assets/same.js",
      "assets/new.js",
    ]);
    expect(result.carry).toEqual(["assets/old.js"]);
    expect(result.added).toEqual(["assets/new.js"]);
    expect(result.manifest).toEqual(
      manifest({
        "assets/new.js": null,
        "assets/same.js": null,
        "assets/old.js": NOW.toISOString(),
      }),
    );
  });

  it("keeps the retired date once it is set", () => {
    const retired = daysAgo(5);
    const result = plan(manifest({ "assets/old.js": retired }), ["assets/new.js"]);
    expect(result.carry).toEqual(["assets/old.js"]);
    expect(result.manifest.files["assets/old.js"]).toEqual({ retired });
  });

  it("carries a file just inside the window and expires it at the limit", () => {
    const result = plan(
      manifest({
        "assets/inside.js": daysAgo(RETENTION_DAYS - 0.01),
        "assets/at-limit.js": daysAgo(RETENTION_DAYS),
        "assets/long-gone.js": daysAgo(RETENTION_DAYS + 30),
      }),
      ["assets/new.js"],
    );
    expect(result.carry).toEqual(["assets/inside.js"]);
    expect(result.expired).toEqual(["assets/at-limit.js", "assets/long-gone.js"]);
    expect(Object.keys(result.manifest.files).sort()).toEqual([
      "assets/inside.js",
      "assets/new.js",
    ]);
  });

  it("clears the retired date of a file that returns to the build", () => {
    const result = plan(manifest({ "assets/back.js": daysAgo(4) }), ["assets/back.js"]);
    expect(result.carry).toEqual([]);
    expect(result.added).toEqual([]);
    expect(result.manifest.files["assets/back.js"]).toEqual({ retired: null });
  });

  it("drops the earliest retired first when over the cap", () => {
    const result = plan(
      manifest({
        "assets/a-oldest.js": daysAgo(10),
        "assets/b-middle.js": daysAgo(6),
        "assets/c-newest.js": daysAgo(1),
        "assets/d-unset.js": null,
      }),
      ["assets/new.js"],
      // The build's 2 files (one is the manifest) leave room for 2 more.
      { maxFiles: 4 },
    );
    expect(result.carry).toEqual(["assets/c-newest.js", "assets/d-unset.js"]);
    expect(result.capped).toEqual(["assets/a-oldest.js", "assets/b-middle.js"]);
    expect(Object.keys(result.manifest.files)).not.toContain("assets/a-oldest.js");
  });

  it("carries nothing when the build alone fills the cap", () => {
    const result = plan(manifest({ "assets/old.js": null }), ["assets/new.js"], { maxFiles: 2 });
    expect(result.carry).toEqual([]);
    expect(result.capped).toEqual(["assets/old.js"]);
  });

  it("caps at MAX_DEPLOY_FILES by default", () => {
    const live = manifest(
      Object.fromEntries(Array.from({ length: 20 }, (_, i) => [`assets/f${i}.js`, daysAgo(i / 2)])),
    );
    const result = planCarryOver({
      built: ["assets/new.js"],
      live,
      now: NOW,
      buildFileCount: MAX_DEPLOY_FILES - 5,
    });
    expect(result.carry).toHaveLength(5);
    expect(result.capped).toHaveLength(15);
  });

  it("carries nothing without a live manifest", () => {
    const result = plan(null, ["assets/b.js", "assets/a.js"]);
    expect(result.carry).toEqual([]);
    expect(result.expired).toEqual([]);
    expect(result.added).toEqual(["assets/a.js", "assets/b.js"]);
    expect(result.manifest).toEqual(manifest({ "assets/a.js": null, "assets/b.js": null }));
  });
});
