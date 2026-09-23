/**
 * Generates raster share/app-icon assets from the brand palette.
 *
 * Social platforms (Facebook, X/Twitter, iMessage, LinkedIn, Slack) do not
 * render SVG for `og:image`, so we rasterize the branded layout to PNG here
 * and commit the output. Re-run with `pnpm --filter web og:gen` when the brand
 * mark or palette changes.
 *
 * OG layout: Option 01 "Missal title page" from docs/share-image-options.html.
 * Rendered via headless Chromium (Playwright) so oklch colors, Cardo small-caps,
 * and paper grain match the design reference — sharp/librsvg cannot reproduce those.
 * Requires Playwright's Chromium: `pnpm --filter web test:e2e:install`.
 *
 * The raw screenshot is ~650 KB because of the paper grain, well over the
 * ~300 KB some link-preview consumers accept (WhatsApp is widely reported to
 * drop larger previews). `compressOgPng` palette-quantizes it to a PNG about a
 * fifth that size that keeps the grain and every accent color.
 *
 * Outputs (into apps/web/public):
 *   - og-default.png      1200x630  link-share preview image (palette PNG)
 *   - apple-touch-icon.png 180x180  iOS home-screen icon
 *   - icon-192.png         192x192  web manifest icon
 *   - icon-512.png         512x512  web manifest icon (maskable-safe)
 */
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "@playwright/test";
import sharp from "sharp";

const WEB_DIR = resolve(import.meta.dirname, "..");
const PUBLIC_DIR = resolve(WEB_DIR, "public");
const OG_TEMPLATE = resolve(import.meta.dirname, "og-template.html");

/** Keep og-default.png under the ~300 KB some link-preview consumers accept. */
const OG_MAX_BYTES = 300 * 1024;
/**
 * First-pass palette quality (0-100). At 95 libimagequant renders the paper
 * gradient and grain faithfully with ~25 colors.
 */
const OG_BASE_QUALITY = 95;
/** Restore pixels the first pass moved further than this (0-255, any channel). */
const OG_RESTORE_THRESHOLD = 6;

const kb = (bytes: number) => `${(bytes / 1024).toFixed(1)} KB`;

async function decodeRgb(png: Buffer): Promise<Buffer> {
  return sharp(png).removeAlpha().raw().toBuffer();
}

/**
 * Shrinks the OG screenshot (~650 KB) to a palette PNG (~140 KB) and reports
 * the largest per-channel difference from the screenshot.
 *
 * A single palette quantization hits the size target, but libimagequant weights
 * colors by pixel count. The thin gold ornament covers only a few hundred
 * pixels, so it gets merged into the red "Carlo" shades and turns pink. Raising
 * the quality until the gold survives costs ~250 KB and still leaves a pink
 * fringe, and JPEG turns the grain into 8x8 blocks. Two passes avoid all three:
 *   1. Quantize to a small palette that covers the paper and grain.
 *   2. Put back the original color of every pixel that pass moved noticeably
 *      (the ornament and antialiased text edges), then re-quantize at full
 *      quality. The paper still needs only its few colors, so the rest of the
 *      256-color palette goes to the restored pixels.
 */
async function compressOgPng(
  screenshot: Buffer,
): Promise<{ png: Buffer; maxError: number }> {
  const { data: source, info } = await sharp(screenshot)
    .removeAlpha()
    .raw()
    .toBuffer({ resolveWithObject: true });

  const base = await decodeRgb(
    await sharp(screenshot)
      .png({ palette: true, quality: OG_BASE_QUALITY, effort: 10 })
      .toBuffer(),
  );
  for (let i = 0; i < source.length; i += 3) {
    const drift = Math.max(
      Math.abs(source[i] - base[i]),
      Math.abs(source[i + 1] - base[i + 1]),
      Math.abs(source[i + 2] - base[i + 2]),
    );
    if (drift > OG_RESTORE_THRESHOLD) source.copy(base, i, i, i + 3);
  }

  const png = await sharp(base, {
    raw: { width: info.width, height: info.height, channels: 3 },
  })
    .png({ palette: true, quality: 100, dither: 0, effort: 10, compressionLevel: 9 })
    .toBuffer();

  const output = await decodeRgb(png);
  let maxError = 0;
  for (let i = 0; i < source.length; i++) {
    maxError = Math.max(maxError, Math.abs(source[i] - output[i]));
  }
  return { png, maxError };
}

async function renderOgPng(): Promise<void> {
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({
      viewport: { width: 1200, height: 630 },
      deviceScaleFactor: 1,
    });
    await page.goto(pathToFileURL(OG_TEMPLATE).href, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    const screenshot = await page.locator("#og-frame").screenshot({ type: "png" });
    const { png, maxError } = await compressOgPng(screenshot);
    if (png.length > OG_MAX_BYTES) {
      throw new Error(
        `og-default.png is ${kb(png.length)}, over the ${kb(OG_MAX_BYTES)} budget; ` +
          "simplify og-template.html or retune compressOgPng.",
      );
    }
    writeFileSync(resolve(PUBLIC_DIR, "og-default.png"), png);
    console.log(
      `Wrote og-default.png (1200x630, ${kb(png.length)}; screenshot was ` +
        `${kb(screenshot.length)}, max channel error ${maxError}/255)`,
    );
  } finally {
    await browser.close();
  }
}

async function main() {
  await renderOgPng();

  const favicon = readFileSync(resolve(PUBLIC_DIR, "favicon.svg"));
  const iconSizes = [
    ["apple-touch-icon.png", 180],
    ["icon-192.png", 192],
    ["icon-512.png", 512],
  ] as const;
  for (const [name, size] of iconSizes) {
    await sharp(favicon, { density: 384 })
      .resize(size, size)
      .png()
      .toFile(resolve(PUBLIC_DIR, name));
    console.log(`Wrote ${name} (${size}x${size})`);
  }
}

void main();
