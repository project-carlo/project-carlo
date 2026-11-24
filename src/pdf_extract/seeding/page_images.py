"""`seed pages`: a bulletin's pages as PNGs, sized for what the reader passes to the model.

The drafter looks at these with Claude Code's Read tool. Read scales any image down to
MAX_IMAGE_EDGE px on its long edge, and the high-resolution models (Claude 4.7 and later)
to MAX_IMAGE_TOKENS visual tokens of 28x28 px, so every render is fitted under both: a
larger one costs the same tokens and loses its extra detail anyway. Each image reports
its size and token cost, so the drafter sees what a choice costs.

Four shapes:
- the images with no text layer (`--images`): on the pages that have text, each image the
  text layer doesn't cover (`textless`), trimmed, tagged and packed into one image, all
  at one resolution. On the newest bulletins of 250 parishes, 205 had some, always on one
  image: a median 110 dpi (lowest 65) and ~1,900 tokens (90% under ~4,000);
- a sheet (`--sheet`): several pages tiled into one labelled image, to find which pages
  hold something (an older issue's dated items) before reading them;
- a page, at PAGE_DPI unless `--dpi` says otherwise: on 14 image-only Camden schedule
  pages (191 times), Opus 5.5 read the same times at 100, 120 and 150 dpi;
- a region (`--region`): part of a page, zoomed to ZOOM_LONG_EDGE px, for small print
  and an unclear digit.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pypdfium2 as pdfium
from PIL import Image, ImageChops, ImageDraw, ImageFont

from pdf_extract.seeding import textless

# What Read passes on: the long-edge cap of Claude Code's Read tool, and the visual-token
# cap of the high-resolution tier (https://platform.claude.com/docs/en/build-with-claude/vision).
MAX_IMAGE_EDGE = 2000
MAX_IMAGE_TOKENS = 4784
PATCH = 28

MIN_DPI, MAX_DPI = 36, 600      # the range `--dpi` accepts
PAGE_DPI = 100                  # a whole page, by default
ZOOM_LONG_EDGE = 1600           # a region, by default: this long edge in px...
ZOOM_MAX_DPI = 300              # ...up to this, past which scans hold no more detail
SHEET_MIN_DPI = 50              # a sheet's pages are at least this sharp (else more sheets)
SHEET_LABEL_PX = 20             # the strip above each page on a sheet, with its number
SHEET_GUTTER_PX = 8
# `--images`: every tile at one resolution, the highest in this range that packs them into
# one image; below the lowest, more images.
IMAGES_MAX_DPI, IMAGES_MIN_DPI, IMAGES_DPI_STEP = 110, 50, 5
TILE_MAX_EDGE = 1100            # a longer tile is shrunk, so a full-page flyer can't shrink all
TILE_GUTTER_PX = 3
TILE_LABEL_PX = 13              # the red tag above a tile, with its number and page...
TILE_TAG_PX = TILE_LABEL_PX + 4  # ...in a strip of this height, so it covers none of its print
TILE_TRIM_TOLERANCE = 18        # a border within this of its corner's colour is trimmed off
TILE_BLANK_SHARE = 0.01         # a tile with less marked than this, trimmed, is left out
IMAGES_MIN_WIDTH, IMAGES_WIDTH_STEP = 400, 40  # widths tried for packing, up to MAX_IMAGE_EDGE

# Named regions, from the page's top left as shown. Halves and quarters overlap by a
# tenth of the page, so a box on the middle line is whole in one of them.
REGIONS: dict[str, tuple[float, float, float, float]] = {
    "top": (0, 0, 1, 0.55),
    "bottom": (0, 0.45, 1, 1),
    "left": (0, 0, 0.55, 1),
    "right": (0.45, 0, 1, 1),
    "top-left": (0, 0, 0.55, 0.55),
    "top-right": (0.45, 0, 1, 0.55),
    "bottom-left": (0, 0.45, 0.55, 1),
    "bottom-right": (0.45, 0.45, 1, 1),
}
REGION_HELP = (f"part of the page: {', '.join(REGIONS)}, or x0,y0,x1,y1 as fractions of "
               "the page from its top left (0.4,0.6,1,1: the lower right, from 40%% across)")


class PageImageError(ValueError):
    """A bad page, region or resolution: the message says what to fix."""


def image_tokens(width: int, height: int) -> int:
    """Visual tokens an image costs: one for each 28x28 px patch."""
    return math.ceil(width / PATCH) * math.ceil(height / PATCH)


def fits(width: int, height: int) -> bool:
    """Whether Read and the model take an image at this size without shrinking it."""
    return (max(width, height) <= MAX_IMAGE_EDGE
            and image_tokens(width, height) <= MAX_IMAGE_TOKENS)


def _px(points: float, dpi: int) -> int:
    return math.ceil(points * dpi / 72)


def fit_dpi(width_pt: float, height_pt: float, dpi: int) -> int:
    """The highest resolution up to `dpi` at which a width x height (PDF points) area fits."""
    dpi = min(dpi, math.floor(MAX_IMAGE_EDGE * 72 / max(width_pt, height_pt)))
    while dpi > 1 and not fits(_px(width_pt, dpi), _px(height_pt, dpi)):
        dpi -= 1
    return max(dpi, 1)


def parse_pages(spec: str | int | None, total: int) -> list[int]:
    """`3`, `3-10` or `2,4-10` (None: every page) as page numbers, checked against `total`."""
    if spec is None:
        return list(range(1, total + 1))
    numbers: list[int] = []
    for part in str(spec).split(","):
        m = re.fullmatch(r"\s*(\d+)\s*(?:-\s*(\d+)\s*)?", part)
        if not m:
            raise PageImageError(f"--page takes a number, a range or a list (3, 3-10, "
                                 f"2,4-10), not {spec!r}")
        first, last = int(m[1]), int(m[2] or m[1])
        if not (1 <= first <= last <= total):
            raise PageImageError(f"The bulletin has pages 1 to {total}")
        numbers += [n for n in range(first, last + 1) if n not in numbers]
    return numbers


def parse_region(spec: str) -> tuple[str, tuple[float, float, float, float]]:
    """A region's name for file names, and its fractions (x0, y0, x1, y1)."""
    if spec in REGIONS:
        return spec, REGIONS[spec]
    try:
        x0, y0, x1, y1 = (float(v) for v in spec.split(","))
    except ValueError:
        raise PageImageError(f"--region is {REGION_HELP.replace('%%', '%')}; not {spec!r}") \
            from None
    if not (0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1):
        raise PageImageError("--region x0,y0,x1,y1 needs 0 <= x0 < x1 <= 1 and "
                             "0 <= y0 < y1 <= 1")
    name = "r" + "-".join(f"{round(v * 100)}" for v in (x0, y0, x1, y1))
    return name, (x0, y0, x1, y1)


def region_spec(box: tuple[float, float, float, float]) -> str:
    """Fractions as `--region` takes them, rounded outward to hundredths: `0.06,0.08,0.57,1`."""
    x0, y0 = (max(0.0, math.floor(v * 100 + 1e-6) / 100) for v in box[:2])
    x1, y1 = (min(1.0, math.ceil(v * 100 - 1e-6) / 100) for v in box[2:])
    return ",".join(f"{v:g}" for v in (x0, y0, x1, y1))


@dataclass
class _Image:
    path: Path
    pages: list[int]
    image: Image.Image
    dpi: int
    asked_dpi: int | None
    region: str | None = None
    tiles: list[dict[str, Any]] | None = None

    def save(self) -> dict[str, Any]:
        if not fits(*self.image.size):  # rounding at the edge: never pass Read a shrinkable one
            scale = min(MAX_IMAGE_EDGE / max(self.image.size),
                        math.sqrt(MAX_IMAGE_TOKENS / image_tokens(*self.image.size)))
            while True:
                size = (max(1, int(self.image.width * scale)),
                        max(1, int(self.image.height * scale)))
                if fits(*size):
                    break
                scale *= 0.99
            self.image = self.image.resize(size, Image.Resampling.LANCZOS)
        self.image.save(self.path, format="PNG")
        width, height = self.image.size
        return {
            "path": self.path.as_posix(), "pages": self.pages, "region": self.region,
            "dpi": self.dpi, "lowered_from": self.asked_dpi
            if self.asked_dpi is not None and self.asked_dpi > self.dpi else None,
            "width": width, "height": height, "tokens": image_tokens(width, height),
            "tiles": self.tiles,
        }


def _render(page: pdfium.PdfPage, dpi: int,
            fractions: tuple[float, float, float, float] | None = None) -> Image.Image:
    width, height = page.get_size()
    crop = (0.0, 0.0, 0.0, 0.0)
    if fractions:
        x0, y0, x1, y1 = fractions
        crop = (x0 * width, (1 - y1) * height, (1 - x1) * width, y0 * height)
    return page.render(scale=dpi / 72, crop=crop).to_pil().convert("RGB")


def page_ranges(pages: list[int], sep: str = "_") -> str:
    """2,3,4,7 as `2-4_7` (a sheet's file name) or, with sep=",", `2-4,7`."""
    runs: list[list[int]] = []
    for n in pages:
        if runs and n == runs[-1][-1] + 1:
            runs[-1].append(n)
        else:
            runs.append([n])
    return sep.join(f"{r[0]}-{r[-1]}" if len(r) > 1 else f"{r[0]}" for r in runs)


def _sheet_size(cols: int, rows: int, cell_w: int, cell_h: int) -> tuple[int, int]:
    return (cols * cell_w + (cols - 1) * SHEET_GUTTER_PX,
            rows * (cell_h + SHEET_LABEL_PX) + (rows - 1) * SHEET_GUTTER_PX)


def sheet_layout(count: int, cell_pt: tuple[float, float],
                 max_dpi: int) -> tuple[int, int, int]:
    """(columns, rows, dpi) tiling `count` pages into one image as sharp as fits."""
    best = (count, 1, 0)
    for cols in range(1, count + 1):
        rows = math.ceil(count / cols)
        dpi = max_dpi
        while dpi > 1 and not fits(*_sheet_size(cols, rows, _px(cell_pt[0], dpi),
                                                _px(cell_pt[1], dpi))):
            dpi -= 1
        if dpi > best[2]:
            best = (cols, rows, dpi)
    return best


def _sheets(count: int, cell_pt: tuple[float, float], max_dpi: int) -> list[int]:
    """How many pages go on each sheet: the fewest sheets whose pages reach SHEET_MIN_DPI."""
    for sheets in range(1, count + 1):
        per = math.ceil(count / sheets)
        if per == 1 or sheet_layout(per, cell_pt, max_dpi)[2] >= min(SHEET_MIN_DPI, max_dpi):
            base, extra = divmod(count, sheets)
            return [base + (i < extra) for i in range(sheets)]
    return [1] * count


def _font(size: int) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    try:
        return ImageFont.load_default(size=size)
    except (TypeError, OSError):  # Pillow without FreeType: the small bitmap font
        return ImageFont.load_default()


def _sheet_image(pdf: pdfium.PdfDocument, pages: list[int], cell_pt: tuple[float, float],
                 max_dpi: int) -> tuple[Image.Image, int]:
    cols, rows, dpi = sheet_layout(len(pages), cell_pt, max_dpi)
    cell_w, cell_h = _px(cell_pt[0], dpi), _px(cell_pt[1], dpi)
    sheet = Image.new("RGB", _sheet_size(cols, rows, cell_w, cell_h), (190, 190, 190))
    draw, font = ImageDraw.Draw(sheet), _font(SHEET_LABEL_PX - 4)
    for i, number in enumerate(pages):
        x = (i % cols) * (cell_w + SHEET_GUTTER_PX)
        y = (i // cols) * (cell_h + SHEET_LABEL_PX + SHEET_GUTTER_PX)
        draw.text((x + 4, y + 1), f"p{number}", fill=(0, 0, 0), font=font)
        page = pdf[number - 1]
        try:
            sheet.paste(_render(page, dpi), (x, y + SHEET_LABEL_PX))
        finally:
            page.close()
    return sheet, dpi


# ── `--images`: the images with no text layer, packed ───────────────────────
@dataclass
class _Tile:
    """A textless image as tiled: its page, its box trimmed (fractions of the page as
    shown), its size in points, and the other pages it is on."""

    page: int
    box: tuple[float, float, float, float]
    size_pt: tuple[float, float]
    also_on: list[int]

    def size(self, dpi: int) -> tuple[int, int]:
        """Its size in px at `dpi`, shrunk to TILE_MAX_EDGE on its long edge."""
        width, height = _px(self.size_pt[0], dpi), _px(self.size_pt[1], dpi)
        scale = min(1.0, TILE_MAX_EDGE / max(width, height))
        return max(1, math.floor(width * scale)), max(1, math.floor(height * scale))

    def label(self, number: int) -> str:
        return f"{number} p{','.join(str(p) for p in [self.page, *self.also_on])}"

    def cell(self, dpi: int, tag_width: int) -> tuple[int, int]:
        """Its size in px with the strip above it that holds its tag."""
        width, height = self.size(dpi)
        return max(width, tag_width), height + TILE_TAG_PX


def _tag_width(label: str) -> int:
    return math.ceil(_font(TILE_LABEL_PX).getlength(label)) + 6


def _trim(image: Image.Image) -> tuple[tuple[int, int, int, int] | None, float]:
    """The box inside `image` that differs from its top-left colour, and the share of
    that box that does (None: all one colour)."""
    background = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    marked = ImageChops.difference(image, background).convert("L").point(
        lambda v: 255 if v > TILE_TRIM_TOLERANCE else 0)
    box = marked.getbbox()
    if box is None:
        return None, 0.0
    inside = marked.crop(box)
    return box, inside.histogram()[255] / (inside.width * inside.height)


def _fingerprint(image: Image.Image) -> tuple:
    """An average hash and the shape: equal for the same picture printed twice."""
    small = image.convert("L").resize((12, 12), Image.Resampling.BILINEAR)
    pixels = list(small.get_flattened_data())
    mean = sum(pixels) / len(pixels)
    return tuple(p > mean for p in pixels), round(image.width / image.height, 1)


def _tiles(pages: dict[int, pdfium.PdfPage],
           found: list[textless.TextlessImage]) -> list[_Tile]:
    """Each textless image trimmed of its border; slivers, blanks and repeats on other
    pages left out (two alike on one page are both kept, in case they only look alike)."""
    tiles: list[_Tile] = []
    seen: dict[tuple, _Tile] = {}
    scale = IMAGES_MAX_DPI / 72
    for area in found:
        image = _render(pages[area.page], IMAGES_MAX_DPI, area.box)
        box, marked = _trim(image)
        if box is None or marked < TILE_BLANK_SHARE:
            continue
        x0, y0, x1, y1 = area.box
        left, top, right, bottom = box
        size_pt = ((right - left) / scale, (bottom - top) / scale)
        if min(size_pt) < textless.MIN_SIDE_PT:
            continue
        fingerprint = _fingerprint(image.crop(box))
        prior = seen.get(fingerprint)
        if prior is not None and area.page != prior.page:
            if area.page not in prior.also_on:
                prior.also_on.append(area.page)
            continue
        span_x, span_y = (x1 - x0) / image.width, (y1 - y0) / image.height
        tile = _Tile(area.page, (x0 + left * span_x, y0 + top * span_y,
                                 x0 + right * span_x, y0 + bottom * span_y), size_pt, [])
        seen.setdefault(fingerprint, tile)
        tiles.append(tile)
    return tiles


Size = tuple[int, int]
_ORDERS: list[Callable[[Size], Any]] = [  # tallest, widest, largest, longest first
    lambda s: (-s[1], -s[0]), lambda s: (-s[0], -s[1]), lambda s: -s[0] * s[1],
    lambda s: -max(s),
]


def skyline_pack(sizes: list[Size], width: int, height: int,
                 order: Callable[[Size], Any] = _ORDERS[0]) -> list[Size] | None:
    """Top-left positions placing `sizes` in a width x height area, each in turn (by
    `order`) as high and then as far left as it goes on the skyline of those before it;
    None if they don't all fit."""
    sky = [(0, width, 0)]  # the skyline's runs, left to right: x, width, lowest free y
    positions: list[Size] = [(0, 0)] * len(sizes)
    for k in sorted(range(len(sizes)), key=lambda k: order(sizes[k])):
        w, h = sizes[k]
        best: tuple[int, int] | None = None
        for i, (x, _, _) in enumerate(sky):
            if x + w > width:
                break
            y, j = 0, i
            while j < len(sky) and sky[j][0] < x + w:
                y = max(y, sky[j][2])
                j += 1
            if y + h <= height and (best is None or (y, x) < best):
                best = (y, x)
        if best is None:
            return None
        y, x = best
        positions[k] = (x, y)
        runs = []
        for rx, rw, ry in sky:
            if rx < x:
                runs.append((rx, min(rw, x - rx), ry))
            if rx + rw > x + w:
                start = max(rx, x + w)
                runs.append((start, rx + rw - start, ry))
        runs.append((x, w, y + h))
        runs.sort()
        sky = [runs[0]]
        for run in runs[1:]:
            if run[2] == sky[-1][2]:
                sky[-1] = (sky[-1][0], sky[-1][1] + run[1], run[2])
            else:
                sky.append(run)
    return positions


def _used(sizes: list[Size], positions: list[Size]) -> Size:
    return (max(x + w for (w, _), (x, _) in zip(sizes, positions)),
            max(y + h for (_, h), (_, y) in zip(sizes, positions)))


def _padded(sizes: list[Size]) -> list[Size]:
    return [(w + TILE_GUTTER_PX, h + TILE_GUTTER_PX) for w, h in sizes]


def pack(sizes: list[Size]) -> list[Size] | None:
    """Positions packing `sizes` (and a TILE_GUTTER_PX gutter) into one image Read takes
    whole, the one costing fewest tokens of the widths and orders tried; None if none fits.
    """
    gutter, padded = TILE_GUTTER_PX, _padded(sizes)
    area = sum(w * h for w, h in padded)
    widest = max(w for w, _ in sizes)
    widths = list(range(max(widest, IMAGES_MIN_WIDTH), MAX_IMAGE_EDGE + 1, IMAGES_WIDTH_STEP))
    if not widths or widths[-1] != MAX_IMAGE_EDGE:
        widths.append(MAX_IMAGE_EDGE)
    best: tuple[int, list[Size]] | None = None
    for width in widths:
        height = min(MAX_IMAGE_EDGE, MAX_IMAGE_TOKENS // math.ceil(width / PATCH) * PATCH)
        if area > (width + gutter) * (height + gutter):
            continue
        for order in _ORDERS:
            positions = skyline_pack(padded, width + gutter, height + gutter, order)
            if positions is None:
                continue
            cost = image_tokens(*_used(sizes, positions))
            if best is None or cost < best[0]:
                best = (cost, positions)
    return best[1] if best else None


# Where more images are needed, each is filled on this canvas first (68 x 70 patches).
_CANVAS = (1904, 1960)


def _plan(tiles: list[_Tile]) -> tuple[int, list[tuple[list[int], list[Size]]]]:
    """The resolution, and each image's tiles and their positions: the highest dpi at
    which all fit one image, else IMAGES_MIN_DPI on as many as they need, each filled
    tallest first. Tile k is numbered k + 1."""
    tags = [_tag_width(t.label(k + 1)) for k, t in enumerate(tiles)]

    def cells(dpi: int, ks: list[int]) -> list[Size]:
        return [tiles[k].cell(dpi, tags[k]) for k in ks]

    for dpi in range(IMAGES_MAX_DPI, IMAGES_MIN_DPI - 1, -IMAGES_DPI_STEP):
        positions = pack(cells(dpi, list(range(len(tiles)))))
        if positions is not None:
            return dpi, [(list(range(len(tiles))), positions)]
    dpi = IMAGES_MIN_DPI
    canvas = (_CANVAS[0] + TILE_GUTTER_PX, _CANVAS[1] + TILE_GUTTER_PX)
    left = sorted(range(len(tiles)), key=lambda k: -tiles[k].size(dpi)[1])
    sheets = []
    while left:
        group: list[int] = []
        for k in left:
            if skyline_pack(_padded(cells(dpi, group + [k])), *canvas) is not None:
                group.append(k)
        group = sorted(group or left[:1])
        left = [k for k in left if k not in group]
        sizes = cells(dpi, group)
        positions = pack(sizes) or skyline_pack(_padded(sizes), *canvas)
        assert positions is not None
        sheets.append((group, positions))
    return dpi, sheets


def _tile_sheet(pages: dict[int, pdfium.PdfPage], tiles: list[tuple[int, _Tile]],
                positions: list[Size], dpi: int) -> Image.Image:
    """`tiles` (numbered) rendered at `dpi`, placed, each tagged with its number above it."""
    labels = [tile.label(number) for number, tile in tiles]
    cells = [tile.cell(dpi, _tag_width(label)) for (_, tile), label in zip(tiles, labels)]
    sheet = Image.new("RGB", _used(cells, positions), (190, 190, 190))
    draw, font = ImageDraw.Draw(sheet), _font(TILE_LABEL_PX)
    for (_, tile), label, (x, y) in zip(tiles, labels, positions):
        image = _render(pages[tile.page], dpi, tile.box)
        size = tile.size(dpi)
        if image.size != size:  # rounding, or shrunk to TILE_MAX_EDGE
            image = image.resize(size, Image.Resampling.LANCZOS)
        sheet.paste(image, (x, y + TILE_TAG_PX))
        draw.rectangle((x, y, x + _tag_width(label) - 1, y + TILE_TAG_PX - 2), fill=(200, 0, 0))
        draw.text((x + 3, y + 1), label, fill=(255, 255, 255), font=font)
    return sheet


def _textless_images(pdf: pdfium.PdfDocument, numbers: list[int], out_dir: Path,
                     short: str) -> tuple[list[int], list[_Image]]:
    """The pages only an image, and the sheets of the others' textless images."""
    pages = {number: pdf[number - 1] for number in numbers}
    try:
        image_only, found = textless.find(pages)
        tiles = _tiles(pages, found)
        images = []
        dpi, sheets = _plan(tiles) if tiles else (0, [])
        for group, positions in sheets:
            numbered = [(k + 1, tiles[k]) for k in group]
            on = sorted({p for _, t in numbered for p in [t.page, *t.also_on]})
            listed = [{"tile": n, "page": t.page, "region": region_spec(t.box),
                       "also_on": t.also_on} for n, t in numbered]
            images.append(_Image(out_dir / f"{short}-images-p{page_ranges(on)}-{dpi}dpi.png",
                                 on, _tile_sheet(pages, numbered, positions, dpi), dpi, None,
                                 tiles=listed))
    finally:
        for page in pages.values():
            page.close()
    return image_only, images


def render(
    data: bytes, out_dir: Path, short: str, *,
    page: str | int | None = None, dpi: int | None = None,
    region: str | None = None, sheet: bool = False, images: bool = False,
) -> dict[str, Any]:
    """Render a bulletin's pages (all, or `page`), a region of them, sheets of them, or
    (`images`) their images with no text layer, packed."""
    if images and (sheet or region or dpi is not None):
        raise PageImageError("--images packs every image with no text layer at one "
                             "resolution; zoom into one with --page N --region R without it")
    if dpi is not None and not MIN_DPI <= dpi <= MAX_DPI:
        raise PageImageError(f"--dpi must be between {MIN_DPI} and {MAX_DPI}")
    if sheet and region:
        raise PageImageError("--sheet tiles whole pages; zoom into one page's --region "
                             "without it")
    if region and page is None:
        raise PageImageError("--region zooms into the pages you name: add --page N")
    fractions = None
    if region:
        region, fractions = parse_region(region)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(data)
    try:
        total = len(pdf)
        numbers = parse_pages(page, total)
        rendered: list[_Image] = []
        image_only = None
        if images:
            image_only, rendered = _textless_images(pdf, numbers, out_dir, short)
        elif sheet:
            sizes = []
            for number in numbers:
                p = pdf[number - 1]
                sizes.append(p.get_size())
                p.close()
            cell_pt = (max(w for w, _ in sizes), max(h for _, h in sizes))
            start = 0
            for count in _sheets(len(numbers), cell_pt, dpi or PAGE_DPI):
                group = numbers[start:start + count]
                start += count
                image, used = _sheet_image(pdf, group, cell_pt, dpi or PAGE_DPI)
                path = out_dir / f"{short}-sheet-p{page_ranges(group)}-{used}dpi.png"
                rendered.append(_Image(path, group, image, used, None))
        else:
            for number in numbers:
                p = pdf[number - 1]
                try:
                    width, height = p.get_size()
                    if fractions:
                        x0, y0, x1, y1 = fractions
                        width, height = (x1 - x0) * width, (y1 - y0) * height
                        wanted = dpi or min(ZOOM_MAX_DPI, math.floor(
                            ZOOM_LONG_EDGE * 72 / max(width, height)))
                    else:
                        wanted = dpi or PAGE_DPI
                    used = fit_dpi(width, height, wanted)
                    image = _render(p, used, fractions)
                finally:
                    p.close()
                name = f"{short}-p{number}" + (f"-{region}" if region else "")
                rendered.append(_Image(out_dir / f"{name}-{used}dpi.png", [number], image,
                                       used, dpi, region))
    finally:
        pdf.close()
    saved = [image.save() for image in rendered]
    result = {"pages": total, "paths": [s["path"] for s in saved], "images": saved,
              "tokens": sum(s["tokens"] for s in saved)}
    if images:
        result.update(searched=numbers, image_only=image_only)
    return result
