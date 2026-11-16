"""`seed pages`: a bulletin's pages as PNGs, sized for what the reader passes to the model.

The drafter looks at these with Claude Code's Read tool. Read scales any image down to
MAX_IMAGE_EDGE px on its long edge, and the high-resolution models (Claude 4.7 and later)
to MAX_IMAGE_TOKENS visual tokens of 28x28 px, so every render is fitted under both: a
larger one costs the same tokens and loses its extra detail anyway. Each image reports
its size and token cost, so the drafter sees what a choice costs.

Three shapes, cheapest first:
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
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

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


@dataclass
class _Image:
    path: Path
    pages: list[int]
    image: Image.Image
    dpi: int
    asked_dpi: int | None
    region: str | None = None

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


def render(
    data: bytes, out_dir: Path, short: str, *,
    page: str | int | None = None, dpi: int | None = None,
    region: str | None = None, sheet: bool = False,
) -> dict[str, Any]:
    """Render a bulletin's pages (all, or `page`), a region of them, or sheets of them."""
    if dpi is not None and not MIN_DPI <= dpi <= MAX_DPI:
        raise PageImageError(f"--dpi must be between {MIN_DPI} and {MAX_DPI}")
    if sheet and region:
        raise PageImageError("--sheet tiles whole pages; zoom into one page's --region "
                             "without it")
    fractions = None
    if region:
        region, fractions = parse_region(region)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(data)
    try:
        total = len(pdf)
        numbers = parse_pages(page, total)
        images: list[_Image] = []
        if sheet:
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
                images.append(_Image(path, group, image, used, None))
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
                images.append(_Image(out_dir / f"{name}-{used}dpi.png", [number], image,
                                     used, dpi, region))
    finally:
        pdf.close()
    saved = [image.save() for image in images]
    return {"pages": total, "paths": [s["path"] for s in saved], "images": saved,
            "tokens": sum(s["tokens"] for s in saved)}
