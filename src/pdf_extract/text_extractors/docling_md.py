"""PDF → text via IBM Docling (layout model + TableFormer + targeted OCR).

Docling renders every page, runs a DocLayNet-style layout detector over the
image and assigns the PDF's own text to the detected regions (text blocks,
section headers, tables, pictures), then orders the regions for reading. For
Publisher-style bulletins that is the point of this stack: a "Mass Schedule"
sidebar comes out as one block under its own header instead of being
interleaved line by line with the column next to it, which is what naive
text-layer extraction does.

Stock docling needs three changes to work well on bulletins:

* **Where to OCR.** Docling OCRs every layout region that overlaps any vector
  shape or bitmap. Bulletin pages are full of boxes and rules, so that ends
  up OCR-ing whole pages (minutes per bulletin on CPU) while still missing
  text: a page-sized crop is too coarse for the small text in a sidebar.
  What actually lacks a text layer in bulletins is (a) text the designer
  converted to outlines (vector paths shaped like glyphs, common for times
  in coloured boxes), (b) images (schedule graphics, scans, ads) and
  (c) text whose font has no usable ToUnicode map. `_scan_pdf` finds those
  areas with pdfium and the OCR model only reads them.
* **Merging OCR with the text layer.** Docling drops an OCR line if its box
  touches any PDF text box at all, so "Saturday: 8:30 AM" (label in the
  text layer, time in outlines) lost the time. `_trim_ocr_cells` removes
  just the words the text layer already has.
* **Serialization.** Docling's Markdown joins a block's lines with spaces
  ("Saturday: 8:30 am Sunday: 7:30 am ..."), drops the page structure and
  escapes HTML. `_render` writes each page under `page_header(n)`, keeps a
  block's visual lines, writes tables as one visual row per line with
  " | " between columns (TableFormer's grid is used only for layout; its
  cell assignment misplaces times in the tab-stop "tables" bulletins use)
  and prefixes every block with its coarse position on the page, e.g.
  `[x5-38 y22-60]`, so the LLM can tell which blocks share a column or box.

Everything runs on CPU. The converter (≈1 GB of models: layout "heron",
TableFormer, RapidOCR PP-OCRv6) loads once per process, lazily; the weights
are fetched from Hugging Face / the RapidOCR model host on first use.
Conversions are serialized behind a lock because docling's pipeline object
is not meant to be shared by concurrent callers.
"""

from __future__ import annotations

import logging
import re
import threading
import unicodedata
import uuid
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from io import BytesIO
from typing import Any

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from docling.datamodel.base_models import DocumentStream, InputFormat, Page
from docling.datamodel.document import ConversionResult
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    RapidOcrOptions,
    TableFormerMode,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.models.stages.ocr.rapid_ocr_model import RapidOcrModel
from docling.pipeline.standard_pdf_pipeline import StandardPdfPipeline
from docling.utils.locks import pypdfium2_lock
from docling_core.types.doc import (
    BoundingBox,
    ContentLayer,
    CoordOrigin,
    DocItem,
    DocItemLabel,
    DoclingDocument,
    ListItem,
    PictureItem,
    ProvenanceItem,
    SectionHeaderItem,
    TableItem,
    TextItem,
    TitleItem,
)
from docling_core.types.doc.page import BoundingRectangle, TextCell

from pdf_extract.text_extractors.base import page_header

LOGGER = logging.getLogger(__name__)

# Rect = (left, top, right, bottom) in PDF points, top-left origin (docling's page space).
Rect = tuple[float, float, float, float]

OCR_SCALE = 2.0  # OCR crops at 144 dpi: as accurate as 216 dpi on bulletin text, ~2x cheaper
TABLE_MODE = TableFormerMode.FAST  # only the table's extent is used, see module docstring

# A vector path counts as outlined text when it is glyph-sized and has many segments
# (letters are curves; boxes, rules and frames have 4-5 segments).
_GLYPH_MIN_SEGMENTS = 8
_GLYPH_MAX_HEIGHT = 80.0
_GLYPH_MAX_WIDTH = 500.0
_GLYPH_MIN_SIDE = 2.0
_MIN_IMAGE_SIDE = 16.0
_REGION_GAP = 4.0  # merge OCR areas closer than this (pt)
_REGION_PAD = 4.0
_LOW_TEXT_COVERAGE = 0.15  # layout regions over an image with less text-layer text get OCR'd
_JUNK_RATIO = 0.5

_LIGATURES = str.maketrans({"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl"})


@dataclass
class _PageScan:
    """What pdfium found on one page: areas needing OCR and where text-layer text is."""

    ink: list[Rect] = field(default_factory=list)  # outlined text, undecodable text
    images: list[Rect] = field(default_factory=list)
    text: list[Rect] = field(default_factory=list)
    rotated: bool = False

    def text_coverage(self, rect: Rect) -> float:
        area = _area(rect)
        if area <= 0:
            return 1.0
        return min(1.0, sum(_area(_intersect(rect, t)) for t in self.text) / area)


# ---------------------------------------------------------------------------- geometry


def _area(r: Rect | None) -> float:
    if r is None:
        return 0.0
    return max(0.0, r[2] - r[0]) * max(0.0, r[3] - r[1])


def _intersect(a: Rect, b: Rect) -> Rect | None:
    x0, y0, x1, y1 = max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])
    return (x0, y0, x1, y1) if x0 < x1 and y0 < y1 else None


def _pad(r: Rect, d: float) -> Rect:
    return (r[0] - d, r[1] - d, r[2] + d, r[3] + d)


def _merge_rects(rects: Iterable[Rect], gap: float) -> list[Rect]:
    """Union rects that overlap or lie within `gap` of each other."""
    pending = [r for r in rects if _area(r) > 0]
    merged: list[Rect] = []
    while pending:
        cur = pending.pop()
        changed = True
        while changed:
            changed = False
            rest = []
            for r in pending:
                if _intersect(_pad(cur, gap), r) is not None:
                    cur = (
                        min(cur[0], r[0]),
                        min(cur[1], r[1]),
                        max(cur[2], r[2]),
                        max(cur[3], r[3]),
                    )
                    changed = True
                else:
                    rest.append(r)
            pending = rest
        merged.append(cur)
    return merged


def _bbox_rect(bbox: BoundingBox, page_height: float) -> Rect:
    if bbox.coord_origin != CoordOrigin.TOPLEFT:
        bbox = bbox.to_top_left_origin(page_height)
    return (bbox.l, bbox.t, bbox.r, bbox.b)


# ---------------------------------------------------------------------------- pdf scan


def _junk_ratio(text: str) -> float:
    chars = [c for c in text if not c.isspace()]
    if not chars:
        return 0.0
    bad = sum(
        1 for c in chars if c == "�" or "" <= c <= "" or unicodedata.category(c) in ("Cc", "Co")
    )
    return bad / len(chars)


def _scan_page(page: pdfium.PdfPage) -> _PageScan:
    scan = _PageScan()
    if page.get_rotation() % 360:
        scan.rotated = True  # rare; fall back to docling's own OCR area selection
        return scan
    cl, cb, cr, ct = page.get_cropbox()
    page_rect: Rect = (0.0, 0.0, cr - cl, ct - cb)

    def to_rect(left: float, bottom: float, right: float, top: float) -> Rect | None:
        return _intersect((left - cl, ct - top, right - cl, ct - bottom), page_rect)

    textpage = page.get_textpage()
    try:
        for i in range(textpage.count_rects()):
            bounds = textpage.get_rect(i)
            rect = to_rect(*bounds)
            if rect is None:
                continue
            content = textpage.get_text_bounded(*bounds)
            if len(content.strip()) >= 3 and _junk_ratio(content) >= _JUNK_RATIO:
                scan.ink.append(rect)  # text layer present but undecodable
            else:
                scan.text.append(rect)
    finally:
        textpage.close()

    glyph_paths: list[Rect] = []

    def walk(objects: Iterable[Any], matrix: pdfium.PdfMatrix | None) -> None:
        for obj in objects:
            kind = obj.type
            if kind == pdfium_c.FPDF_PAGEOBJ_FORM:
                sub = obj.get_matrix()
                sub = sub if matrix is None else sub.multiply(matrix)
                children = (
                    pdfium.PdfObject(
                        pdfium_c.FPDFFormObj_GetObject(obj.raw, i), page=page, level=obj.level + 1
                    )
                    for i in range(pdfium_c.FPDFFormObj_CountObjects(obj.raw))
                )
                walk(children, sub)
                continue
            if kind not in (pdfium_c.FPDF_PAGEOBJ_IMAGE, pdfium_c.FPDF_PAGEOBJ_PATH):
                continue
            bounds = obj.get_bounds()
            if matrix is not None:
                bounds = matrix.on_rect(*bounds)
            rect = to_rect(*bounds)
            if rect is None:
                continue
            w, h = rect[2] - rect[0], rect[3] - rect[1]
            if kind == pdfium_c.FPDF_PAGEOBJ_IMAGE:
                if w >= _MIN_IMAGE_SIDE and h >= _MIN_IMAGE_SIDE:
                    scan.images.append(rect)
            elif (
                _GLYPH_MIN_SIDE <= h <= _GLYPH_MAX_HEIGHT
                and _GLYPH_MIN_SIDE <= w <= _GLYPH_MAX_WIDTH
                and pdfium_c.FPDFPath_CountSegments(obj.raw) >= _GLYPH_MIN_SEGMENTS
            ):
                glyph_paths.append(rect)

    walk(page.get_objects(max_depth=1), None)

    # Outlined text: glyph-like paths not already covered by text-layer text (paths
    # used as underlines/highlights sit under real text and are ignored).
    for rect in glyph_paths:
        covered = sum(_area(_intersect(rect, t)) for t in scan.text)
        if covered < 0.3 * _area(rect):
            scan.ink.append(rect)
    scan.ink = _merge_rects((_pad(r, _REGION_PAD) for r in scan.ink), _REGION_GAP)
    return scan


def _scan_pdf(pdf_bytes: bytes) -> dict[int, _PageScan]:
    """Per 1-indexed page: areas that need OCR and where the text layer has text."""
    scans: dict[int, _PageScan] = {}
    with pypdfium2_lock:  # pdfium is not thread-safe; docling uses the same lock
        pdf = pdfium.PdfDocument(pdf_bytes)
        try:
            for index in range(len(pdf)):
                page = pdf[index]
                try:
                    scans[index + 1] = _scan_page(page)
                except Exception:  # a malformed page must not sink the document
                    LOGGER.warning("pdfium scan failed on page %d", index + 1, exc_info=True)
                finally:
                    page.close()
        finally:
            pdf.close()
    return scans


# ---------------------------------------------------------------------------- OCR model

# Scan results for documents currently being converted, keyed by the stream name we give
# docling (a UUID), so the OCR stage (running on docling's worker threads) can find them.
_SCANS: dict[str, dict[int, _PageScan]] = {}
_SCANS_LOCK = threading.Lock()


def _overlap(a: float, b: float, c: float, d: float) -> float:
    return max(0.0, min(b, d) - max(a, c))


def _trim_ocr_cells(ocr_cells: Sequence[TextCell], pdf_cells: Sequence[TextCell]) -> list[TextCell]:
    """Keep only the OCR text the text layer does not already have on that line.

    OCR returns whole lines; one line can mix text-layer words and outlined words
    ("Saturday/Sábado: 8:30 AM"). Character positions are estimated proportionally
    along the OCR box, which is accurate enough to cut out the duplicated part: whole
    words when a word is (nearly) all inside or outside a text-layer box, single
    characters where a box edge falls inside a word ("Sábado:7:00"). Kept pieces are
    shrunk away from neighbouring text-layer boxes, because docling's own merge then
    discards any OCR cell whose box touches a text-layer box.
    """
    pdf = []
    for c in pdf_cells:
        if c.text.strip():
            bb = c.rect.to_bounding_box()
            pdf.append((bb.l, bb.t, bb.r, bb.b))
    kept: list[TextCell] = []
    for cell in ocr_cells:
        bb = cell.rect.to_bounding_box()
        left, top0, right, bottom0 = bb.l, bb.t, bb.r, bb.b
        text = cell.text
        height = bottom0 - top0
        if not text.strip() or right <= left or height <= 0:
            continue
        near = [
            p
            for p in pdf
            if _overlap(left, right, p[0], p[2]) > 0 and _overlap(top0, bottom0, p[1], p[3]) > 0
        ]
        same_line = [
            p for p in near if _overlap(top0, bottom0, p[1], p[3]) >= 0.5 * min(height, p[3] - p[1])
        ]
        pieces: list[tuple[str, float, float]] = []
        if not same_line:
            pieces.append((text, left, right))
        else:
            step = (right - left) / len(text)

            def inside(i: int) -> bool:
                x = left + (i + 0.5) * step
                return any(p[0] <= x <= p[2] for p in same_line)

            drop = [inside(i) for i in range(len(text))]
            for m in re.finditer(r"\S+", text):
                x0, x1 = left + m.start() * step, left + m.end() * step
                covered = sum(_overlap(x0, x1, p[0], p[2]) for p in same_line) / (x1 - x0)
                if covered >= 0.8 or covered <= 0.2:
                    drop[m.start() : m.end()] = [covered >= 0.8] * (m.end() - m.start())
            start = None
            for i in range(len(text) + 1):
                if i < len(text) and not drop[i]:
                    start = i if start is None else start
                    continue
                if start is not None:
                    piece = text[start:i]
                    lead = len(piece) - len(piece.lstrip())
                    piece = piece.strip()
                    if any(ch.isalnum() for ch in piece):
                        x0 = left + (start + lead) * step
                        pieces.append((piece, x0, x0 + len(piece) * step))
                    start = None
        for piece, x0, x1 in pieces:
            top, bottom = top0, bottom0
            for p in near:
                if p in same_line:  # beside us on this line: stay clear horizontally
                    if (p[0] + p[2]) / 2 < (x0 + x1) / 2:
                        x0 = max(x0, p[2] + 0.01)
                    else:
                        x1 = min(x1, p[0] - 0.01)
                elif (p[1] + p[3]) / 2 < (top0 + bottom0) / 2:  # line above/below grazes us
                    top = max(top, p[3] + 0.01)
                else:
                    bottom = min(bottom, p[1] - 0.01)
            if x1 - x0 < 1 or bottom - top < 1:
                continue
            rect = BoundingRectangle.from_bounding_box(
                BoundingBox(l=x0, t=top, r=x1, b=bottom, coord_origin=CoordOrigin.TOPLEFT)
            )
            kept.append(cell.model_copy(update={"text": piece, "orig": piece, "rect": rect}))
    return kept


class _BulletinOcrModel(RapidOcrModel):
    """RapidOCR restricted to the areas `_scan_pdf` found, with word-level merging."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._scans: dict[int, _PageScan] | None = None

    def __call__(self, conv_res: ConversionResult, page_batch: Iterable[Page]) -> Iterable[Page]:
        with _SCANS_LOCK:
            self._scans = _SCANS.get(conv_res.input.file.name)
        yield from super().__call__(conv_res, page_batch)

    def get_ocr_rects(self, page: Page) -> list[BoundingBox]:
        scan = self._scans.get(page.page_no) if self._scans else None
        if scan is None or scan.rotated or page.size is None:
            return super().get_ocr_rects(page)
        rects: list[Rect] = list(scan.ink)
        clusters = page.predictions.layout.clusters if page.predictions.layout else []
        cluster_rects = [_bbox_rect(c.bbox, page.size.height) for c in clusters]
        for image in scan.images:
            inside = [
                c for c in cluster_rects if _area(_intersect(c, image)) >= 0.5 * max(_area(c), 1)
            ]
            if not inside:
                rects.append(image)
            for c in inside:
                if scan.text_coverage(c) < _LOW_TEXT_COVERAGE:
                    clipped = _intersect(c, image)
                    if clipped is not None:
                        rects.append(clipped)
        page_rect: Rect = (0.0, 0.0, page.size.width, page.size.height)
        out = []
        for rect in _merge_rects(rects, _REGION_GAP):
            clipped = _intersect(rect, page_rect)
            if (
                clipped is not None
                and clipped[2] - clipped[0] >= 4
                and clipped[3] - clipped[1] >= 4
            ):
                out.append(BoundingBox(l=clipped[0], t=clipped[1], r=clipped[2], b=clipped[3]))
        return out

    def post_process_cells(
        self,
        ocr_cells: list[TextCell],
        page: Page,
        conv_res: ConversionResult,
        priority: Any = None,
    ) -> None:
        pdf_cells = list(page.cells)
        good_pdf = [c for c in pdf_cells if _junk_ratio(c.text) < _JUNK_RATIO]
        if len(good_pdf) != len(pdf_cells) and page.parsed_page is not None:
            # Undecodable text-layer cells: let the OCR text (read from the same spot) win.
            page.parsed_page.textline_cells = good_pdf
        trimmed = _trim_ocr_cells(ocr_cells, good_pdf)
        super().post_process_cells(trimmed, page, conv_res, priority)


class _BulletinPdfPipeline(StandardPdfPipeline):
    def _make_ocr_model(self, art_path: Any) -> Any:
        options = self.pipeline_options
        if not isinstance(options.ocr_options, RapidOcrOptions):
            return super()._make_ocr_model(art_path)
        return _BulletinOcrModel(
            enabled=options.do_ocr,
            artifacts_path=art_path,
            options=options.ocr_options,
            accelerator_options=options.accelerator_options,
        )


# ---------------------------------------------------------------------------- converter

_CONVERTER: DocumentConverter | None = None
_CONVERT_LOCK = threading.Lock()


def _ocr_backend() -> str:
    try:
        import onnxruntime  # noqa: F401
    except ImportError:
        return "torch"  # always present with docling; ~1.4x slower on CPU
    return "onnxruntime"


def _pipeline_options() -> PdfPipelineOptions:
    options = PdfPipelineOptions()
    options.accelerator_options.device = "cpu"
    options.do_table_structure = True
    options.table_structure_options.mode = TABLE_MODE
    options.do_ocr = True
    # PP-OCRv6 recognizes Latin-script languages incl. Spanish accents with one model.
    options.ocr_options = RapidOcrOptions(
        backend=_ocr_backend(),
        lang=["en"],
        scale=OCR_SCALE,
        # RapidOCR's default upscales every crop until its *short* side is 736 px, so a
        # one-line crop becomes a huge, slow (seconds) and less accurate detector input.
        # Only ever downscale instead.
        rapidocr_params={"Det.limit_type": "max", "Det.limit_side_len": 2000},
    )
    options.do_picture_classification = False
    options.do_picture_description = False
    options.do_code_enrichment = False
    options.do_formula_enrichment = False
    options.generate_page_images = False
    options.generate_picture_images = False
    options.generate_parsed_pages = False
    return options


def _converter() -> DocumentConverter:
    """The process-wide converter; call with `_CONVERT_LOCK` held."""
    global _CONVERTER
    if _CONVERTER is None:
        LOGGER.info("Loading docling models (first use downloads them)...")
        converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=_BulletinPdfPipeline, pipeline_options=_pipeline_options()
                )
            },
        )
        converter.initialize_pipeline(InputFormat.PDF)
        _CONVERTER = converter
    return _CONVERTER


# ---------------------------------------------------------------------------- rendering


def _cells_to_lines(cells: Sequence[TextCell], column_sep: str) -> list[str]:
    """Group cells into visual lines (top to bottom), cells left to right within a line.

    Cells separated by a wide horizontal gap are joined with `column_sep`, so a row
    like "Sun   2/15   8:00am   Mass" keeps its columns apart.
    """
    boxes = []
    for c in cells:
        text = c.text.translate(_LIGATURES).strip()
        if not text:
            continue
        bb = c.rect.to_bounding_box().to_top_left_origin(0)
        boxes.append((bb.l, bb.t, bb.r, bb.b, text))
    boxes.sort(key=lambda x: ((x[1] + x[3]) / 2, x[0]))
    lines: list[list[tuple[float, float, float, float, str]]] = []
    for box in boxes:
        h = box[3] - box[1]
        if lines:
            line = lines[-1]
            top, bottom = min(x[1] for x in line), max(x[3] for x in line)
            if _overlap(box[1], box[3], top, bottom) >= 0.5 * min(max(h, 0.1), bottom - top):
                line.append(box)
                continue
        lines.append([box])
    out = []
    for line in lines:
        line.sort(key=lambda x: x[0])
        parts: list[str] = []
        prev = None
        for box in line:
            if prev is not None:
                char_w = (prev[2] - prev[0]) / max(len(prev[4]), 1)
                gap = box[0] - prev[2]
                parts.append(column_sep if gap > max(3 * char_w, 8.0) else " ")
            parts.append(box[4])
            prev = box
        out.append("".join(parts))
    return out


def _letters(text: str) -> Counter[str]:
    return Counter(c for c in text.lower() if c.isalnum())


def _same_letters(a: str, b: str) -> bool:
    ca, cb = _letters(a), _letters(b)
    total = max(sum(ca.values()), sum(cb.values()))
    return total == 0 or sum((ca & cb).values()) >= 0.9 * total


def _location(prov: ProvenanceItem, doc: DoclingDocument) -> str:
    size = doc.pages[prov.page_no].size
    x0, y0, x1, y1 = _bbox_rect(prov.bbox, size.height)

    def pct(v: float, total: float) -> int:
        return max(0, min(100, round(100 * v / total)))

    return (
        f"[x{pct(x0, size.width)}-{pct(x1, size.width)} "
        f"y{pct(y0, size.height)}-{pct(y1, size.height)}]"
    )


class _CellIndex:
    """Finds the text cells docling assigned to a document item (via its layout cluster)."""

    def __init__(self, conv_res: ConversionResult) -> None:
        self._by_page: dict[int, list[tuple[Rect, Any]]] = {}
        for page in conv_res.pages:
            if page.assembled is None or page.size is None:
                continue
            entries = self._by_page.setdefault(page.page_no, [])
            for element in page.assembled.elements:
                cluster = getattr(element, "cluster", None)
                if cluster is not None and cluster.cells:
                    entries.append((_bbox_rect(cluster.bbox, page.size.height), cluster))

    def cells(self, prov: ProvenanceItem, doc: DoclingDocument) -> list[TextCell] | None:
        rect = _bbox_rect(prov.bbox, doc.pages[prov.page_no].size.height)
        for other, cluster in self._by_page.get(prov.page_no, []):
            if all(abs(a - b) < 0.5 for a, b in zip(rect, other, strict=True)):
                return list(cluster.cells)
        return None


def _blocks(
    item: DocItem, doc: DoclingDocument, index: _CellIndex, page_no: int
) -> list[tuple[ProvenanceItem, str]]:
    """The item's text on `page_no`, one block per layout region it was built from.

    Docling's reading-order step merges text it thinks continues across regions into
    one item (sometimes wrongly, e.g. a staff list and the Mass schedule box in the
    next column); keeping each region as its own block with its own location undoes
    the damage.
    """
    provs = [p for p in item.prov if p.page_no == page_no]
    if not provs:
        return []
    if isinstance(item, TableItem):
        rows = _cells_to_lines(index.cells(provs[0], doc) or [], column_sep=" | ")
        # No cells (e.g. a table read by OCR elsewhere): fall back to TableFormer's grid.
        return [(provs[0], "\n".join(rows) if rows else item.export_to_markdown(doc=doc))]
    if not isinstance(item, TextItem):
        return []
    text = " ".join(item.text.split())
    if isinstance(item, SectionHeaderItem | TitleItem):
        return [(provs[0], f"{'#' if isinstance(item, TitleItem) else '##'} {text}")]
    cell_groups = [index.cells(p, doc) for p in provs]
    lines_per_prov = [_cells_to_lines(c or [], column_sep=" | ") for c in cell_groups]
    all_lines = [line for lines in lines_per_prov for line in lines]
    if all(c is not None for c in cell_groups) and _same_letters("".join(all_lines), text):
        blocks = [(p, "\n".join(lines)) for p, lines in zip(provs, lines_per_prov, strict=True)]
    else:
        blocks = [(provs[0], text)]
    if isinstance(item, ListItem):
        blocks = [(p, f"- {t}") for p, t in blocks]
    return blocks


def _render(conv_res: ConversionResult, with_location: bool) -> str:
    doc = conv_res.document
    index = _CellIndex(conv_res)
    layers = {ContentLayer.BODY, ContentLayer.FURNITURE}
    out: list[str] = []
    for page_no in sorted(doc.pages):
        out.append(page_header(page_no))
        for item, _level in doc.iterate_items(
            page_no=page_no, included_content_layers=layers, traverse_pictures=True
        ):
            if not isinstance(item, DocItem) or isinstance(item, PictureItem) or not item.prov:
                continue
            if item.label == DocItemLabel.PAGE_FOOTER and len(getattr(item, "text", "")) < 4:
                continue  # bare page numbers
            for prov, text in _blocks(item, doc, index, page_no):
                text = text.strip()
                if text and text not in ("##", "#", "-"):
                    out.append(f"{_location(prov, doc)} {text}" if with_location else text)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------------------- extractor


class DoclingExtractor:
    """Docling layout analysis + targeted RapidOCR, rendered as page-marked text."""

    name = "docling"

    def __init__(self, with_location: bool = True) -> None:
        self.with_location = with_location
        self.version = (
            f"v1-heron-tf{TABLE_MODE.value}-rows-rapidocr{OCR_SCALE:g}"
            f"{'-loc' if with_location else ''}"
        )

    def extract_text(self, pdf_bytes: bytes) -> str:
        scans = _scan_pdf(pdf_bytes)
        key = f"{uuid.uuid4().hex}.pdf"
        with _SCANS_LOCK:
            _SCANS[key] = scans
        try:
            with _CONVERT_LOCK:
                result = _converter().convert(
                    DocumentStream(name=key, stream=BytesIO(pdf_bytes)), raises_on_error=True
                )
                return _render(result, self.with_location)
        finally:
            with _SCANS_LOCK:
                _SCANS.pop(key, None)
