"""PyMuPDF text extraction with a column-aware reading order and an OCR fallback.

Bulletins are laid out like newsletters: two or three columns, boxed sidebars
with the Mass schedule, church names set as bold headers over a list of times,
and grids of day x time. A plain `page.get_text()` follows the content-stream
order, which for Publisher/InDesign output often jumps between columns or
reads a table column by column (all the days, then all the times), and the
downstream LLM then pairs times with the wrong day or church. This module
rebuilds a reading order from the geometry instead:

* Every text line becomes a unit with a bounding box, font size and weight.
* The page is cut recursively (XY-cut) into columns and horizontal bands. A
  vertical cut is kept only between two real columns: each side at least 15%
  of the page wide and not lined up row by row with the other like table
  cells. Narrow side-by-side cells (day | date | time) are therefore never
  separated; they are read row by row and joined with " | ".
* Whenever the page was split into columns, each column starts with a coarse
  position tag such as `[x8-50% y22-95%]`, so the LLM can tell a sidebar from
  the main column. Bold or large short lines are marked as `## ` headings and
  struck-through text (a common way to cancel a Mass) is wrapped in `~~`.

Text that is only visible as pixels is recovered with RapidOCR (ONNX models
shipped in the wheel, CPU only, no system binaries): pages without a usable
text layer, text with broken ToUnicode maps (replacement or private-use
characters), large embedded images (a schedule pasted in as a picture), and
text converted to vector outlines (common in designed schedule boxes). Only
those regions are OCR'd; the native text inside them is painted over first so
OCR never duplicates it, and the OCR lines then join the same layout pass.

PyMuPDF is not thread-safe, so every call into it runs under one module-wide
lock; OCR (the slow part) runs outside that lock under its own lock, so one
thread can parse a PDF while another is OCR'ing.
"""

from __future__ import annotations

import hashlib
import logging
import re
import statistics
import threading
from dataclasses import dataclass, field
from itertools import pairwise
from typing import Any

import numpy as np
import pymupdf

from pdf_extract.text_extractors.base import page_header

LOGGER = logging.getLogger(__name__)

# PyMuPDF / MuPDF share global state: never call into them from two threads.
_PYMUPDF_LOCK = threading.Lock()
# RapidOCR is created once, lazily; calls are serialized (onnxruntime already
# uses every core for one image, so parallel OCR would not be faster anyway).
_OCR_LOCK = threading.Lock()
_OCR_ENGINE: Any = None

_TEXT_FLAGS = pymupdf.TEXT_MEDIABOX_CLIP  # expand ligatures, whitespace -> spaces
_OCR_DPI = 200
_OCR_MAX_SIDE = 1600  # pixels
_OCR_MIN_SCORE = 0.6
_OCR_IMAGE_MIN_AREA = 0.03  # fraction of the page an image must cover to be OCR'd
_OCR_IMAGE_MIN_SIDE = 40.0  # points
_OUTLINE_MIN_CURVES = 150  # curve segments in a cluster of glyph-like paths
_MIN_PAGE_CHARS = 40  # below this the page is treated as having no text layer

_MIN_GUTTER = 2.0  # points of empty space that can separate two columns...
_GUTTER_SLACK = 1.5  # ...after trimming this much off both ends of every line
_MIN_COLUMN_FRAC = 0.15  # a text column is at least this share of the page width
_PIPE_GAP = 1.2  # gap (in font sizes) above which row cells are joined with " | "

_BOLD_FONT_RE = re.compile(r"bold|black|heavy|semibold|demi", re.IGNORECASE)
_SPACE_RE = re.compile(r"\s+")
_WORD_RE = re.compile(r"[A-Za-z]{4,}")
_VOWEL_RE = re.compile(r"[aeiouyAEIOUY]")
_URLISH_RE = re.compile(r"[@/]|\.\w")


@dataclass(slots=True)
class _Unit:
    """One line of text (or one OCR line) with its box, in page points."""

    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    size: float
    bold: bool = False
    font: str = ""
    ocr: bool = False
    strike: bool = False

    @property
    def w(self) -> float:
        return self.x1 - self.x0

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def h(self) -> float:
        return self.y1 - self.y0

    @property
    def rect(self) -> pymupdf.Rect:
        return pymupdf.Rect(self.x0, self.y0, self.x1, self.y1)


@dataclass(slots=True)
class _Crop:
    """A rendered page region to OCR, with native text painted over."""

    img: np.ndarray
    x: float  # page position (points) of the image's top-left pixel
    y: float
    scale: float  # pixels per point


@dataclass(slots=True)
class _PageData:
    """Everything taken from one page while holding the PyMuPDF lock."""

    number: int
    width: float
    height: float
    units: list[_Unit] = field(default_factory=list)
    rotated: list[str] = field(default_factory=list)
    ocr_crops: list[_Crop] = field(default_factory=list)


class PyMuPDFLayoutExtractor:
    """Column-aware PyMuPDF text with RapidOCR for text that has no text layer."""

    name = "pymupdf-layout"
    version = "v1"

    def __init__(self, *, ocr: bool = True) -> None:
        # ocr=False keeps only the native text layer (for timing / ablations).
        self.ocr = ocr

    def extract_text(self, pdf_bytes: bytes) -> str:
        with _PYMUPDF_LOCK:
            doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
            try:
                pages = [_read_page(page, ocr=self.ocr) for page in doc]
            finally:
                doc.close()
        out: list[str] = []
        ocr_cache: dict[bytes, list[Any]] = {}
        for data in pages:
            if data.ocr_crops:
                data.units.extend(_ocr_units(data, ocr_cache))
            out.append(page_header(data.number))
            body = _render_page(data)
            if body:
                out.append(body)
        return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- #
# Native text                                                                  #
# --------------------------------------------------------------------------- #


def _read_page(page: pymupdf.Page, *, ocr: bool = True) -> _PageData:
    if page.rotation:
        # Bake /Rotate into the content (in memory only) so text, drawings,
        # images and renders all share the coordinates of the page as viewed.
        page.remove_rotation()
    units, rotated, turn = _read_lines(page)
    if turn:
        # Most text runs up or down the page (a landscape page placed sideways):
        # turn the page so it reads left to right.
        page.set_rotation(turn)
        page.remove_rotation()
        units, rotated, _ = _read_lines(page)
    rect = page.rect
    data = _PageData(number=page.number + 1, width=rect.width, height=rect.height)
    data.units, data.rotated = units, rotated
    data.units = _dedupe(data.units)

    soup_fonts = _letter_soup_fonts(data.units)
    garbled = [u for u in data.units if u.font in soup_fonts or _is_garbled(u)]
    if garbled:
        LOGGER.info(
            "Page %d: %d lines look garbled (letter-soup fonts %s); OCR'ing them",
            data.number, len(garbled), sorted(soup_fonts),
        )
        garbled_ids = {id(u) for u in garbled}
        data.units = [u for u in data.units if id(u) not in garbled_ids]
    # Stray icon glyphs (Wingdings bullets, private-use symbols) carry no text.
    for unit in data.units:
        if any(map(_is_bad_char, unit.text)):
            unit.text = _clean("".join(c for c in unit.text if not _is_bad_char(c)))
    data.units = [u for u in data.units if u.text]

    drawings = page.get_drawings()
    _mark_strikeouts(data.units, drawings)

    native_chars = sum(len(u.text) for u in data.units)
    regions: list[pymupdf.Rect] = []
    if native_chars < _MIN_PAGE_CHARS:
        regions.append(pymupdf.Rect(rect))
    else:
        regions.extend(u.rect for u in garbled)
        regions.extend(_image_regions(page, data.units))
        regions.extend(_outline_regions(drawings, data.units, rect))
    regions = _merge_rects([r & rect for r in regions if not (r & rect).is_empty])
    if ocr:
        for region in regions:
            # Cap the long side: text detection cost grows with the pixel
            # count, and ~140 dpi still reads a full page of 8pt text.
            scale = min(_OCR_DPI / 72, _OCR_MAX_SIDE / max(region.width, region.height))
            pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale), clip=region, alpha=False)
            if pix.w < 8 or pix.h < 8:
                continue
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n).copy()
            crop = _Crop(img=img, x=pix.x / scale, y=pix.y / scale, scale=scale)
            _paint_over(crop, data.units)
            data.ocr_crops.append(crop)
    return data


def _read_lines(page: pymupdf.Page) -> tuple[list[_Unit], list[str], int]:
    """Horizontal lines as units, other lines as plain text, and a suggested turn.

    The turn (90 or 270 degrees, else 0) is set when most characters run
    vertically, i.e. the whole page is sideways.
    """
    units: list[_Unit] = []
    rotated: list[str] = []
    chars = {"h": 0, "down": 0, "up": 0}
    for block in page.get_text("rawdict", flags=_TEXT_FLAGS)["blocks"]:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            spans = [piece for span in line["spans"] for piece in _span_pieces(span)]
            count = sum(len(s["text"]) for s in spans)
            dx, dy = line["dir"]
            if abs(dy) <= 0.2 and dx > 0:
                chars["h"] += count
                units.extend(_line_units(spans))
                continue
            if abs(dx) <= 0.2:
                chars["down" if dy > 0 else "up"] += count
            text = _clean(" ".join(s["text"] for s in spans))
            if text:
                rotated.append(text)
    turn = 0
    vertical = max(chars["down"], chars["up"])
    if vertical > 100 and vertical > 2 * chars["h"]:
        turn = 270 if chars["down"] >= chars["up"] else 90
    return units, rotated, turn


def _span_pieces(span: dict[str, Any]) -> list[dict[str, Any]]:
    """Split a rawdict span at wide runs of spaces, with boxes tight around the ink.

    Line boxes from MuPDF include trailing spaces, and some producers align
    table cells with runs of spaces inside one span; both would hide the gap
    between two columns.
    """
    pieces: list[dict[str, Any]] = []
    chars: list[dict[str, Any]] = []
    size = span["size"]

    def flush() -> None:
        ink = [c for c in chars if not c["c"].isspace()]
        if ink:
            pieces.append({
                "text": "".join(c["c"] for c in chars).strip(),
                "bbox": (
                    min(c["bbox"][0] for c in ink), min(c["bbox"][1] for c in ink),
                    max(c["bbox"][2] for c in ink), max(c["bbox"][3] for c in ink),
                ),
                "size": size,
                "flags": span["flags"],
                "font": span["font"],
            })
        chars.clear()

    last_x1: float | None = None
    for char in span["chars"]:
        if char["c"].isspace():
            if chars:
                chars.append(char)
            continue
        if last_x1 is not None and char["bbox"][0] - last_x1 > 3.0 * max(size, 4.0):
            flush()
        chars.append(char)
        last_x1 = char["bbox"][2]
    flush()
    return pieces


def _line_units(spans: list[dict[str, Any]]) -> list[_Unit]:
    """Turn one PyMuPDF line into units, splitting it where spans are far apart."""
    units: list[_Unit] = []
    parts: list[dict[str, Any]] = []

    def flush() -> None:
        if not parts:
            return
        text = ""
        prev_x1: float | None = None
        for span in parts:
            gap = 0.0 if prev_x1 is None else span["bbox"][0] - prev_x1
            if text and gap > 0.15 * span["size"] and not text.endswith(" "):
                text += " "
            text += span["text"]
            prev_x1 = span["bbox"][2]
        text = _clean(text)
        if not text:
            parts.clear()
            return
        weights = [(len(s["text"].strip()), s) for s in parts]
        total = sum(n for n, _ in weights) or 1
        main = max(weights, key=lambda item: item[0])[1]
        bold_chars = sum(
            n for n, s in weights if s["flags"] & 16 or _BOLD_FONT_RE.search(s["font"])
        )
        units.append(
            _Unit(
                x0=min(s["bbox"][0] for s in parts),
                y0=min(s["bbox"][1] for s in parts),
                x1=max(s["bbox"][2] for s in parts),
                y1=max(s["bbox"][3] for s in parts),
                text=text,
                size=main["size"],
                bold=bold_chars / total > 0.9,
                font=main["font"],
            )
        )
        parts.clear()

    for span in spans:
        if parts and span["bbox"][0] - parts[-1]["bbox"][2] > 3.0 * max(span["size"], 4.0):
            flush()
        parts.append(span)
    flush()
    return units


def _clean(text: str) -> str:
    return _SPACE_RE.sub(" ", text.replace("\u00ad", "")).strip()


def _dedupe(units: list[_Unit]) -> list[_Unit]:
    """Drop repeated lines (fake bold / shadow effects print text twice)."""
    kept: list[_Unit] = []
    seen: dict[str, list[_Unit]] = {}
    for unit in units:
        same = seen.setdefault(unit.text, [])
        if any(_overlap_area(unit, other) > 0.7 * min(unit.w * unit.h, other.w * other.h)
               for other in same):
            continue
        same.append(unit)
        kept.append(unit)
    return kept


def _overlap_area(a: _Unit, b: _Unit) -> float:
    w = min(a.x1, b.x1) - max(a.x0, b.x0)
    h = min(a.y1, b.y1) - max(a.y0, b.y0)
    return w * h if w > 0 and h > 0 else 0.0


def _is_bad_char(ch: str) -> bool:
    code = ord(ch)
    return (
        ch == "\ufffd"
        or 0xE000 <= code <= 0xF8FF
        or code >= 0xF0000
        or (code < 0x20 and ch not in "\t\n")
    )


def _is_garbled(unit: _Unit) -> bool:
    """Mostly replacement / private-use characters: a font without a usable ToUnicode map."""
    bad = sum(map(_is_bad_char, unit.text))
    return bad >= 3 and bad > 0.3 * sum(not c.isspace() for c in unit.text)


def _letter_soup_fonts(units: list[_Unit]) -> set[str]:
    """Fonts whose text decodes to letters but not to words (a shifted glyph mapping).

    Real English or Spanish words of four letters or more nearly always have a
    vowel; text from a scrambled mapping (e.g. "Pdvv" for "Mass") mostly does
    not. All-caps words are included, since headings are often set in caps.
    """
    by_font: dict[str, list[str]] = {}
    for unit in units:
        # URLs and e-mail addresses are legitimately vowel-poor ("hmgfh.com").
        text = " ".join(t for t in unit.text.split() if not _URLISH_RE.search(t))
        by_font.setdefault(unit.font, []).append(text)
    soup: set[str] = set()
    for font, texts in by_font.items():
        words = _WORD_RE.findall(" ".join(texts))
        if len(words) >= 8:
            vowelless = sum(1 for w in words if not _VOWEL_RE.search(w))
            if vowelless / len(words) > 0.35:
                soup.add(font)
    return soup


def _mark_strikeouts(units: list[_Unit], drawings: list[dict[str, Any]]) -> None:
    """Flag lines crossed through the middle by a thin horizontal rule."""
    rules: list[tuple[float, float, float]] = []
    for path in drawings:
        r = path["rect"]
        if r.height <= 1.5 and r.width >= 4:
            rules.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
    if not rules:
        return
    for unit in units:
        lo, hi = unit.y0 + 0.35 * unit.h, unit.y0 + 0.75 * unit.h
        covered = sum(
            max(0.0, min(x1, unit.x1) - max(x0, unit.x0))
            for x0, x1, y in rules
            if lo <= y <= hi
        )
        if covered >= 0.7 * unit.w:
            unit.strike = True


# --------------------------------------------------------------------------- #
# OCR                                                                          #
# --------------------------------------------------------------------------- #


def _image_regions(page: pymupdf.Page, units: list[_Unit]) -> list[pymupdf.Rect]:
    """Large images that are not already covered by native text."""
    page_area = page.rect.width * page.rect.height
    regions: list[pymupdf.Rect] = []
    for info in page.get_image_info():
        r = pymupdf.Rect(info["bbox"]) & page.rect
        if r.is_empty or r.width < _OCR_IMAGE_MIN_SIDE or r.height < _OCR_IMAGE_MIN_SIDE:
            continue
        if r.width * r.height < _OCR_IMAGE_MIN_AREA * page_area:
            continue
        text_area = sum((u.rect & r).get_area() for u in units)
        if text_area > 0.25 * r.get_area():  # a background behind real text
            continue
        regions.append(r)
    return regions


def _outline_regions(
    drawings: list[dict[str, Any]], units: list[_Unit], page_rect: pymupdf.Rect,
) -> list[pymupdf.Rect]:
    """Clusters of filled, curvy, text-height paths: text converted to outlines."""
    native = [u.rect for u in units]
    glyphs: list[tuple[pymupdf.Rect, int]] = []
    for path in drawings:
        r = path["rect"]
        if path.get("fill") is None or not (3 <= r.height <= 40) or r.width > 0.9 * page_rect.width:
            continue
        curves = sum(1 for item in path["items"] if item[0] == "c")
        if curves < 3:
            continue
        if any(r.intersects(n) and (r & n).get_area() > 0.5 * r.get_area() for n in native):
            continue
        glyphs.append((pymupdf.Rect(r), curves))
    clusters: list[tuple[pymupdf.Rect, int]] = []
    for r, curves in sorted(glyphs, key=lambda g: (g[0].y0, g[0].x0)):
        grown = r + (-8, -8, 8, 8)
        for i, (cr, ccount) in enumerate(clusters):
            if cr.intersects(grown):
                clusters[i] = (cr | r, ccount + curves)
                break
        else:
            clusters.append((r, curves))
    # One more pass so clusters that grew into each other are joined.
    merged = _merge_weighted(clusters)
    return [r + (-3, -3, 3, 3) for r, count in merged if count >= _OUTLINE_MIN_CURVES]


def _merge_weighted(items: list[tuple[pymupdf.Rect, int]]) -> list[tuple[pymupdf.Rect, int]]:
    items = list(items)
    changed = True
    while changed:
        changed = False
        out: list[tuple[pymupdf.Rect, int]] = []
        for r, n in items:
            for i, (o, m) in enumerate(out):
                if (o + (-8, -8, 8, 8)).intersects(r):
                    out[i] = (o | r, m + n)
                    changed = True
                    break
            else:
                out.append((r, n))
        items = out
    return items


def _merge_rects(rects: list[pymupdf.Rect]) -> list[pymupdf.Rect]:
    return [r for r, _ in _merge_weighted([(pymupdf.Rect(r), 0) for r in rects])]


def _paint_over(crop: _Crop, units: list[_Unit]) -> None:
    """Hide native text in the render so OCR only reads what the text layer lacks."""
    img, scale = crop.img, crop.scale
    h, w = img.shape[:2]
    for u in units:
        x0 = max(int((u.x0 - crop.x) * scale) - 1, 0)
        y0 = max(int((u.y0 - crop.y) * scale) - 1, 0)
        x1 = min(int((u.x1 - crop.x) * scale) + 2, w)
        y1 = min(int((u.y1 - crop.y) * scale) + 2, h)
        if x1 <= x0 or y1 <= y0:
            continue
        patch = img[y0:y1, x0:x1]
        patch[:] = np.median(patch.reshape(-1, patch.shape[-1]), axis=0).astype(np.uint8)


def _get_ocr_engine() -> Any:
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        from rapidocr import RapidOCR  # noqa: PLC0415 - heavy, only when OCR is needed

        _OCR_ENGINE = RapidOCR(
            params={
                "Global.log_level": "warning",
                # Bulletin text is upright; the 0/180 classifier only costs time.
                "Global.use_cls": False,
                # Only ever shrink for detection: the default ("min") scales a
                # thin strip up until its short side is 736 px, which is slow.
                "Det.limit_type": "max",
            },
        )
    return _OCR_ENGINE


def _ocr_units(data: _PageData, cache: dict[bytes, list[Any]]) -> list[_Unit]:
    """OCR each rendered region of the page and return its lines as units.

    `cache` maps a render's digest to its OCR lines, so a logo or header image
    repeated on every page of a bulletin is only recognised once.
    """
    units: list[_Unit] = []
    for crop in data.ocr_crops:
        key = hashlib.blake2b(crop.img.tobytes(), digest_size=16).digest()
        key += str(crop.img.shape).encode()
        if key not in cache:
            cache[key] = _ocr_image(crop.img)
        for bx0, by0, bx1, by1, text in cache[key]:
            x0, y0 = crop.x + bx0 / crop.scale, crop.y + by0 / crop.scale
            x1, y1 = crop.x + bx1 / crop.scale, crop.y + by1 / crop.scale
            units.append(_Unit(x0, y0, x1, y1, text=text, size=0.75 * (y1 - y0), ocr=True))
    LOGGER.debug("Page %d: OCR added %d lines", data.number, len(units))
    return units


def _ocr_image(img: np.ndarray) -> list[Any]:
    """(x0, y0, x1, y1, text) in pixels for each confident, horizontal line."""
    with _OCR_LOCK:
        result = _get_ocr_engine()(img)
    if result.boxes is None:
        return []
    lines: list[Any] = []
    for box, raw, score in zip(result.boxes, result.txts, result.scores, strict=False):
        text = _clean(raw)
        if float(score) < _OCR_MIN_SCORE or len(text) < 2 or not any(c.isalnum() for c in text):
            continue
        xs, ys = box[:, 0], box[:, 1]
        width, height = float(xs.max() - xs.min()), float(ys.max() - ys.min())
        # Tilted or vertical text is artwork or photo credits, and reads as junk.
        if abs(float(box[1][1] - box[0][1])) > 0.5 * height or height > 1.5 * width:
            continue
        lines.append((float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max()), text))
    return lines


# --------------------------------------------------------------------------- #
# Layout                                                                       #
# --------------------------------------------------------------------------- #


@dataclass(slots=True)
class _Block:
    """A run of lines to print together, optionally opened by a position tag."""

    units: list[_Unit]
    tag: str | None = None


def _render_page(data: _PageData) -> str:
    units = [u for u in data.units if u.w > 0 and u.h > 0]
    if not units and not data.rotated:
        return ""
    ctx = _Ctx(data.width, data.height, units)
    blocks = ctx.cut(units, tag=None)
    out: list[str] = []
    for block in blocks:
        lines = [ctx.format_row(row) for row in _rows(block.units)]
        if block.tag:
            lines.insert(0, block.tag)
        if out:
            out.append("")
        out.extend(lines)
    if data.rotated:
        out.extend(["", "[rotated text] " + " / ".join(data.rotated)])
    return "\n".join(out)


class _Ctx:
    def __init__(self, width: float, height: float, units: list[_Unit]) -> None:
        self.width = width
        self.height = height
        sizes = [u.size for u in units for _ in range(max(1, len(u.text) // 8))]
        self.body_size = statistics.median(sizes) if sizes else 10.0
        heights = [u.h for u in units]
        self.line_h = statistics.median(heights) if heights else 10.0

    # ---- recursive XY-cut ------------------------------------------------ #

    def cut(self, units: list[_Unit], tag: str | None) -> list[_Block]:
        if len(units) <= 1:
            return [_Block(units, tag)]
        gutters = self.gutters(units)
        if gutters:
            # Each column gets its own, more precise tag in place of the parent's.
            bounds = [-np.inf, *gutters, np.inf]
            blocks: list[_Block] = []
            for lo, hi in pairwise(bounds):
                column = [u for u in units if lo < u.cx <= hi]
                blocks.extend(self.cut(column, self.tag(column)))
            return blocks
        strips = self.strips(units)
        if len(strips) == 1:
            return [_Block(units, tag)]
        blocks = []
        for i, (start, end) in enumerate(self.column_runs(strips)):
            group = [u for strip in strips[start:end] for u in strip]
            blocks.extend(self.cut(group, tag if i == 0 else None))
        return blocks

    def column_runs(self, strips: list[list[_Unit]]) -> list[tuple[int, int]]:
        """Group consecutive bands that share a column gutter, longest runs first.

        Two columns rarely have a common gap on every line, so bands found by
        `strips` often cut through a multi-column area; such bands must be
        re-joined, or the page would read band by band across the columns. A
        header band next to the columns can share a spurious gutter with the
        first band, so the longest run wins rather than the first one.
        """
        n = len(strips)
        ends: list[int] = []  # ends[i]: exclusive end of the longest run from i
        end = 0
        for i in range(n):
            end = max(end, i + 1)
            while end < n and (
                end - i + 1 < n and self.gutters([u for s in strips[i:end + 1] for u in s])
            ):
                end += 1
            ends.append(end)
        taken = [False] * n
        runs: list[tuple[int, int]] = []
        for start in sorted(range(n), key=lambda i: (i - ends[i], i)):
            stop = ends[start]
            if stop - start > 1 and not any(taken[start:stop]):
                runs.append((start, stop))
                taken[start:stop] = [True] * (stop - start)
        runs += [(i, i + 1) for i in range(n) if not taken[i]]
        return sorted(runs)

    def gutters(self, units: list[_Unit]) -> list[float]:
        """x positions at which `units` split into side-by-side text columns.

        Every vertical strip of empty space is a candidate. Segments narrower
        than a text column (a column of days, dates or times) are merged into a
        neighbour across the narrower gap, then gaps between segments that
        line up row by row like a table are dropped too; what survives
        separates real columns.
        """
        # Boxes are shrunk a little: tightly set columns can sit < 1pt apart.
        spans = sorted(
            (u.x0 + min(_GUTTER_SLACK, u.w / 4), u.x1 - min(_GUTTER_SLACK, u.w / 4))
            for u in units
        )
        gaps: list[tuple[float, float]] = []  # (split x, width)
        reach = spans[0][1]
        for x0, x1 in spans[1:]:
            if x0 - reach >= _MIN_GUTTER:
                gaps.append((reach + (x0 - reach) / 2, x0 - reach))
            reach = max(reach, x1)
        min_width = _MIN_COLUMN_FRAC * self.width
        while gaps:
            bounds = [-np.inf, *(g for g, _ in gaps), np.inf]
            segments = [[u for u in units if lo < u.cx <= hi] for lo, hi in pairwise(bounds)]
            widths = [max(u.x1 for u in s) - min(u.x0 for u in s) for s in segments]
            narrow = min(range(len(segments)), key=widths.__getitem__)
            if widths[narrow] < min_width:
                # Gap indices next to segment i are i - 1 and i.
                sides = [i for i in (narrow - 1, narrow) if 0 <= i < len(gaps)]
                del gaps[min(sides, key=lambda i: gaps[i][1])]
                continue
            tables = [
                i for i in range(len(gaps)) if self.table_like(segments[i], segments[i + 1])
            ]
            if not tables:
                break
            del gaps[min(tables, key=lambda i: gaps[i][1])]
        return [g for g, _ in gaps]

    def table_like(self, left: list[_Unit], right: list[_Unit]) -> bool:
        """Short cells on one side sitting on the same baselines as the other side.

        Columns of prose on a shared baseline grid line up too, so this only
        fires when the side with fewer lines reads like table cells (days,
        dates, times), and only for exact baseline matches.
        """
        few, many = (left, right) if len(left) <= len(right) else (right, left)
        if len(few) < 3:
            return False
        chars = sorted(len(u.text) for u in few)
        if chars[len(chars) // 2] > 20:
            return False
        aligned = sum(
            1 for u in few
            if any(
                abs(u.y1 - v.y1) <= 0.15 * min(u.h, v.h)
                and abs(u.size - v.size) <= 0.25 * max(u.size, v.size)
                for v in many
            )
        )
        return aligned >= 0.7 * len(few)

    def strips(self, units: list[_Unit]) -> list[list[_Unit]]:
        """Split into horizontal bands at empty vertical gaps."""
        ordered = sorted(units, key=lambda u: u.y0)
        min_gap = max(1.5, 0.3 * self.line_h)
        strips: list[list[_Unit]] = [[ordered[0]]]
        bottom = ordered[0].y1
        for unit in ordered[1:]:
            if unit.y0 - bottom >= min_gap:
                strips.append([unit])
            else:
                strips[-1].append(unit)
            bottom = max(bottom, unit.y1)
        return strips

    def tag(self, units: list[_Unit]) -> str | None:
        if not units:
            return None
        x0 = min(u.x0 for u in units) / self.width * 100
        x1 = max(u.x1 for u in units) / self.width * 100
        y0 = min(u.y0 for u in units) / self.height * 100
        y1 = max(u.y1 for u in units) / self.height * 100
        return f"[x{x0:.0f}-{x1:.0f}% y{y0:.0f}-{y1:.0f}%]"

    # ---- rows ------------------------------------------------------------ #

    def format_row(self, row: list[_Unit]) -> str:
        text = ""
        prev: _Unit | None = None
        for unit in row:
            piece = f"~~{unit.text}~~" if unit.strike else unit.text
            if prev is None:
                text = piece
            else:
                gap = unit.x0 - prev.x1
                size = max(min(unit.size, prev.size), 4.0)
                if gap < 0.12 * size and not (unit.ocr or prev.ocr):
                    text += piece
                elif gap < _PIPE_GAP * size:
                    text += " " + piece
                else:
                    text += " | " + piece
            prev = unit
        if len(text) <= 70 and any(c.isalpha() for c in text):
            if all(u.size >= 1.8 * self.body_size for u in row):
                return "# " + text
            if all(u.bold or u.size >= 1.25 * self.body_size for u in row):
                return "## " + text
        return text


def _rows(units: list[_Unit]) -> list[list[_Unit]]:
    """Group units whose boxes share a baseline band into left-to-right rows."""
    rows: list[tuple[float, float, list[_Unit]]] = []
    for unit in sorted(units, key=lambda u: (u.y0 + u.y1) / 2):
        if rows:
            top, bottom, members = rows[-1]
            overlap = min(bottom, unit.y1) - max(top, unit.y0)
            if overlap > 0.5 * min(bottom - top, unit.h):
                members.append(unit)
                continue
        rows.append((unit.y0, unit.y1, [unit]))
    return [sorted(members, key=lambda u: u.x0) for _, _, members in rows]
