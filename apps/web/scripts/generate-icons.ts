/**
 * Generates every raster app icon from public/favicon.svg, for the web app and
 * the Expo app in apps/mobile. Re-run with `pnpm --filter web icons:gen` when
 * the brand mark changes (`og:gen` runs it too).
 *
 * favicon.svg is the mark on a rounded red tile. Platforms that crop icons to
 * their own shape need the mark on a square, full-bleed background and kept
 * inside their safe zone, so the tile is replaced and the mark is scaled about
 * the centre. The mark reaches about 27 units from the centre of the 64-unit
 * viewBox, so `scale` sets how far it reaches:
 *   - maskable web icon: safe zone is a circle of radius 40% (25.6 units)
 *   - Android adaptive icon: safe zone is a 66dp circle on a 108dp layer
 *     (radius 19.6 units)
 *
 * Outputs:
 *   apps/web/public
 *     - apple-touch-icon.png      180x180    iOS home screen, full bleed (iOS rounds it)
 *     - icon-192.png, icon-512.png           web manifest, the favicon as drawn
 *     - icon-maskable-512.png     512x512    web manifest, maskable
 *   apps/mobile/assets/images
 *     - icon.png                  1024x1024  app icon, full bleed, no alpha
 *     - android-icon-foreground.png 512x512  adaptive icon mark on transparent
 *     - android-icon-background.png 512x512  adaptive icon background (solid red)
 *     - android-icon-monochrome.png 432x432  themed icon, white mark on transparent
 *     - splash-icon.png           512x512    splash mark on transparent
 */
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import sharp from "sharp";

const WEB_DIR = resolve(import.meta.dirname, "..");
const PUBLIC_DIR = resolve(WEB_DIR, "public");
const MOBILE_IMAGES_DIR = resolve(WEB_DIR, "../mobile/assets/images");

const RED = "#9B2F25";
const MARK_COLORS = ["#F3ECD8", "#E8C673"];
const TILE = /<rect width="64" height="64" rx="14" fill="#9B2F25" \/>\s*/;

/** The favicon's drawing without its outer <svg>, <title> and rounded tile. */
function readMark(): string {
  const favicon = readFileSync(resolve(PUBLIC_DIR, "favicon.svg"), "utf8");
  if (!TILE.test(favicon)) {
    throw new Error("favicon.svg no longer starts with the rounded red tile; update TILE.");
  }
  return favicon
    .replace(/^[\s\S]*?<svg[^>]*>/, "")
    .replace(/<\/svg>\s*$/, "")
    .replace(/<title[\s\S]*?<\/title>/, "")
    .replace(TILE, "");
}

interface Variant {
  /** Square background, or none for a transparent layer. */
  background?: string;
  /** Size of the mark relative to the favicon. */
  scale: number;
  /** Draw the whole mark in white, for Android's themed icons. */
  monochrome?: boolean;
}

function composeSvg(mark: string, { background, scale, monochrome }: Variant): string {
  const drawing = monochrome
    ? MARK_COLORS.reduce((svg, color) => svg.replaceAll(color, "#FFFFFF"), mark)
    : mark;
  return (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">' +
    (background ? `<rect width="64" height="64" fill="${background}"/>` : "") +
    `<g transform="translate(32 32) scale(${scale}) translate(-32 -32)">${drawing}</g>` +
    "</svg>"
  );
}

async function writePng(svg: string | Buffer, path: string, size: number, opaque = false) {
  let image = sharp(Buffer.from(svg), { density: 384 }).resize(size, size);
  if (opaque) image = image.removeAlpha();
  await image.png().toFile(path);
  console.log(`Wrote ${path.replace(`${resolve(WEB_DIR, "..")}/`, "")} (${size}x${size})`);
}

export async function generateIcons(): Promise<void> {
  const favicon = readFileSync(resolve(PUBLIC_DIR, "favicon.svg"));
  const mark = readMark();
  const fullBleed = composeSvg(mark, { background: RED, scale: 0.92 });

  await writePng(fullBleed, resolve(PUBLIC_DIR, "apple-touch-icon.png"), 180, true);
  await writePng(favicon, resolve(PUBLIC_DIR, "icon-192.png"), 192);
  await writePng(favicon, resolve(PUBLIC_DIR, "icon-512.png"), 512);
  await writePng(
    composeSvg(mark, { background: RED, scale: 0.8 }),
    resolve(PUBLIC_DIR, "icon-maskable-512.png"),
    512,
    true,
  );

  await writePng(fullBleed, resolve(MOBILE_IMAGES_DIR, "icon.png"), 1024, true);
  await writePng(
    composeSvg(mark, { scale: 0.7 }),
    resolve(MOBILE_IMAGES_DIR, "android-icon-foreground.png"),
    512,
  );
  await writePng(
    composeSvg("", { background: RED, scale: 1 }),
    resolve(MOBILE_IMAGES_DIR, "android-icon-background.png"),
    512,
    true,
  );
  await writePng(
    composeSvg(mark, { scale: 0.7, monochrome: true }),
    resolve(MOBILE_IMAGES_DIR, "android-icon-monochrome.png"),
    432,
  );
  await writePng(
    composeSvg(mark, { scale: 1 }),
    resolve(MOBILE_IMAGES_DIR, "splash-icon.png"),
    512,
  );
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  void generateIcons();
}
