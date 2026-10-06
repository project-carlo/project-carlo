import { describe, expect, it } from "vitest";
import {
  LASTMOD_PLACEHOLDER,
  contentForHash,
  latestDate,
  parseLastmodManifest,
  resolveLastmod,
} from "./lastmod";

describe("parseLastmodManifest", () => {
  it("reads a valid manifest", () => {
    const text = JSON.stringify({
      version: 1,
      pages: { "/churches/a/": { hash: "abc", lastmod: "2026-09-01" } },
    });
    expect(parseLastmodManifest(text)).toEqual({
      version: 1,
      pages: { "/churches/a/": { hash: "abc", lastmod: "2026-09-01" } },
    });
  });

  it("rejects what isn't a manifest", () => {
    expect(parseLastmodManifest("<!DOCTYPE html>")).toBeNull();
    expect(parseLastmodManifest("null")).toBeNull();
    expect(parseLastmodManifest(JSON.stringify({ version: 2, pages: {} }))).toBeNull();
    expect(parseLastmodManifest(JSON.stringify({ version: 1 }))).toBeNull();
  });

  it("drops malformed entries and keeps the rest", () => {
    const text = JSON.stringify({
      version: 1,
      pages: {
        "/a/": { hash: "x", lastmod: "2026-09-01" },
        "/b/": { hash: "y", lastmod: "yesterday" },
        "/c/": { lastmod: "2026-09-01" },
        "/d/": null,
      },
    });
    expect(parseLastmodManifest(text)?.pages).toEqual({
      "/a/": { hash: "x", lastmod: "2026-09-01" },
    });
  });
});

describe("contentForHash", () => {
  it("ignores asset filenames and the date placeholder", () => {
    const page = (css: string, date: string) =>
      `<link href="${css}"><script>{"dateModified":"${date}"}</script><p>Mass 9:00</p>`;
    const a = contentForHash(page("/assets/index-AAA.css", LASTMOD_PLACEHOLDER), [
      "/assets/index-AAA.css",
    ]);
    const b = contentForHash(page("/assets/index-BBB.css", LASTMOD_PLACEHOLDER), [
      "/assets/index-BBB.css",
    ]);
    expect(a).toBe(b);
  });

  it("keeps content changes", () => {
    expect(contentForHash("<p>Mass 9:00</p>", [])).not.toBe(
      contentForHash("<p>Mass 9:30</p>", []),
    );
  });
});

describe("resolveLastmod", () => {
  const previous = { hash: "abc", lastmod: "2026-09-01" };

  it("keeps the previous date while the content is unchanged", () => {
    expect(resolveLastmod(previous, "abc", "2026-10-06")).toBe("2026-09-01");
  });

  it("uses the build date for changed or new pages", () => {
    expect(resolveLastmod(previous, "def", "2026-10-06")).toBe("2026-10-06");
    expect(resolveLastmod(undefined, "abc", "2026-10-06")).toBe("2026-10-06");
  });
});

describe("latestDate", () => {
  it("picks the latest date, or the fallback when there are none", () => {
    expect(latestDate(["2026-09-01", "2026-10-02", "2026-08-30"], "x")).toBe("2026-10-02");
    expect(latestDate([], "2026-10-06")).toBe("2026-10-06");
  });
});
