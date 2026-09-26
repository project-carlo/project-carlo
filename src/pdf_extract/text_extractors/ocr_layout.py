"""PDF → text by rendering every page and OCR-ing it, then rebuilding the layout.

Bulletins are laid out like posters: multi-column pages, shaded sidebars with a
"Mass Schedule" grid, church names as headers above lists of times, day × time
tables. Their text layer is unreliable — the schedule block is often a pasted
image or outlined text, and fonts with broken ToUnicode maps turn into
gibberish. This extractor ignores the text layer entirely: it renders each page
(PyMuPDF), runs a CPU OCR engine on the picture (RapidOCR: ONNX models that
ship inside the wheel, so no system binaries and no downloads) and so reads
every bulletin the way a vision model would.

OCR returns one box per text line, in no useful order. The layout step turns
those boxes into text an LLM can follow:

* Junk is dropped: low-confidence lines, and tall narrow boxes (sideways text,
  ornamental borders read as letters).
* A recursive XY-cut splits the page into blocks, columns first, so a column
  is read to the end before the next one starts. A column boundary is an
  empty strip between OCR boxes; or a straight vertical edge in the picture
  that no text crosses (a box border, a rule, the side of a shaded panel
  butted right against the next column); or a strip with no ink over five
  or more rows, which also catches gutters that OCR ran one box across (such
  boxes are split there by their word positions).
* A boundary is *not* cut when its two sides look like the columns of one
  table (lines on exactly the same baselines, one side holding short cells
  such as times or days): splitting "Saturday | 4:00 PM" into a list of days
  followed by a list of times would lose which time belongs to which day.
* Without a column boundary the widest horizontal gap is cut, preferring gaps
  with a box edge or rule across them and avoiding gaps that are only a pause
  inside side-by-side columns (that would interleave the columns' halves). A
  heading row that touches the columns below it is peeled off so the columns
  can still be separated.
* Inside a block, boxes on the same baseline are merged into one row, with
  " | " between cells that are far apart, so table rows read as one line.
  Rows separated by a paragraph-sized gap get a blank line between them.
* Each block on a multi-block page is introduced by its position on the page,
  e.g. ``[x 5-38% y 20-77%]``, which tells the LLM that a block is a sidebar,
  a footer or the main column.
"""

from __future__ import annotations

import logging
import re
import statistics
import threading
from dataclasses import dataclass

import numpy as np
import pymupdf
from rapidocr import RapidOCR

from pdf_extract.text_extractors.base import page_header

LOGGER = logging.getLogger(__name__)

RENDER_DPI = 300
"""Pages are rendered at this resolution and recognition reads crops of it:
at 200 dpi small-caps suffixes get lost ("6:45 A" for "6:45 AM")."""

MAX_RENDER_SIDE = 3300
"""Longest rendered side in pixels (letter at 300 dpi), so tabloid pages
don't blow up memory and time."""

DET_MAX_SIDE = 2200
"""Text *detection* runs on the page scaled down to this longest side (about
200 dpi for letter): finding lines doesn't need 300 dpi and detection is the
expensive half. Much lower (150 dpi) and boxes start clipping first digits."""

MIN_CONFIDENCE = 0.6
"""OCR lines below this recognition score are dropped (mostly noise read off
photos and ornaments)."""

MIN_GUTTER = 0.2
"""Narrowest empty vertical strip, in median line heights, that can separate
columns. Designers put boxes close together, and OCR boxes are padded."""

ANALYSIS_DPI = 150
"""Resolution at which the picture is scanned for rules and ink."""

RULE_MIN_INCHES = 0.75
"""Shortest straight edge that counts as a box border or rule."""

RULE_CONTRAST = 12
"""Grey-level step (0-255) across an edge; low enough for the side of a
pastel panel on white."""

INK_CONTRAST = 40
"""Grey-level step (0-255) that marks a pixel as ink (letter strokes, photos),
on light and dark backgrounds alike."""


@dataclass(frozen=True)
class _Word:
    x0: float
    x1: float
    text: str


@dataclass(frozen=True)
class _Line:
    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    words: tuple[_Word, ...] = ()

    @property
    def height(self) -> float:
        return self.y1 - self.y0

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2


@dataclass(frozen=True)
class _Rule:
    """A straight edge in the picture (box border, rule, side of a panel).

    `at` is its x (vertical rules) or y (horizontal ones), and `start`/`end`
    its extent along the other axis, in page pixels.
    """

    at: float
    start: float
    end: float


class OCRLayoutExtractor:
    name = "ocr-layout"
    version = f"v1-rapidocr-grey{RENDER_DPI}dpi-det{DET_MAX_SIDE}-conf{MIN_CONFIDENCE}"

    _engine: RapidOCR | None = None
    _lock = threading.Lock()
    """Serializes all work: the OCR engine mutates its own state on every call
    and MuPDF is not thread-safe. Little is lost, since ONNX Runtime already
    spreads a single page over every core."""

    def extract_text(self, pdf_bytes: bytes) -> str:
        parts: list[str] = []
        with self._lock:
            engine = self._get_engine()
            with pymupdf.open(stream=pdf_bytes, filetype="pdf") as doc:
                for index, page in enumerate(doc):
                    image = _render(page)
                    lines = _ocr(engine, image)
                    picture = _analyse_picture(image)
                    parts.append(page_header(index + 1))
                    parts.append(layout_page(lines, picture))
        return "\n".join(parts).rstrip() + "\n"

    @classmethod
    def _get_engine(cls) -> RapidOCR:
        if cls._engine is None:
            cls._engine = RapidOCR(
                params={
                    "Global.log_level": "error",  # else it warns on every blank page
                    "Global.use_cls": False,  # bulletin text is upright
                    "Global.max_side_len": MAX_RENDER_SIDE + 1,
                    "Det.limit_type": "max",
                    "Det.limit_side_len": DET_MAX_SIDE,
                }
            )
        return cls._engine


def _render(page: pymupdf.Page) -> np.ndarray:
    """The page as a greyscale image in three channels, the shape OCR expects.

    Grey, not colour: recognition misreads light text on tinted panels in
    colour ("6:45 A English" for white "6:45 AM English" on tan) and gets it
    right in grey.
    """
    rect = page.rect
    scale = min(RENDER_DPI / 72, MAX_RENDER_SIDE / max(rect.width, rect.height, 1.0))
    pixmap = page.get_pixmap(
        matrix=pymupdf.Matrix(scale, scale), colorspace=pymupdf.csGRAY, alpha=False
    )
    pixels = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(pixmap.height, pixmap.stride)
    grey = pixels[:, : pixmap.width]
    return np.repeat(grey[:, :, np.newaxis], 3, axis=2)


def _ocr(engine: RapidOCR, image: np.ndarray) -> list[_Line]:
    """OCR one page image into text lines with word boxes."""
    result = engine(image, return_word_box=True)
    lines: list[_Line] = []
    if result.boxes is None:
        return lines
    word_results = result.word_results or ((),) * len(result.boxes)
    for box, text, score, words in zip(result.boxes, result.txts, result.scores, word_results):
        text = " ".join(str(text).split())
        if not text or float(score) < MIN_CONFIDENCE:
            continue
        xs = [float(point[0]) for point in box]
        ys = [float(point[1]) for point in box]
        word_boxes = tuple(
            _Word(
                min(float(point[0]) for point in word_box),
                max(float(point[0]) for point in word_box),
                str(word_text),
            )
            for word_text, _, word_box in (words or ())
            if str(word_text).strip()
        )
        lines.append(_Line(min(xs), min(ys), max(xs), max(ys), text, word_boxes))
    return lines


@dataclass(frozen=True)
class _Picture:
    """What the layout needs from the page image besides the OCR text."""

    width: int
    height: int
    step: int
    """Page pixels per pixel of `ink` (which is ~ANALYSIS_DPI)."""
    ink: np.ndarray
    """Boolean mask of pixels with a sharp grey-level change: letter strokes,
    rules, photos. Empty strips in it are gutters, even where OCR ran one
    box across them."""
    vertical: list[_Rule]
    horizontal: list[_Rule]


def _analyse_picture(image: np.ndarray) -> _Picture:
    """Find ink, and long straight edges (box borders, rules, panel sides).

    An edge is a run of pixels where the grey level steps across it, pixel
    after pixel along it; text never does that for long.
    """
    height, width = image.shape[:2]
    step = max(1, round(max(height, width) / (11 * ANALYSIS_DPI)))
    grey = image[::step, ::step].mean(axis=2)
    across = np.abs(np.diff(grey, axis=1))
    down = np.abs(np.diff(grey, axis=0))
    ink = np.zeros(grey.shape, dtype=bool)
    ink[:, 1:] |= across >= INK_CONTRAST
    ink[1:, :] |= down >= INK_CONTRAST
    vertical = _straight_runs((across >= RULE_CONTRAST).T, step)
    horizontal = _straight_runs(down >= RULE_CONTRAST, step)
    return _Picture(width, height, step, ink, vertical, horizontal)


def _straight_runs(edges: np.ndarray, step: int) -> list[_Rule]:
    """Runs of True along each row of `edges` at least RULE_MIN_INCHES long."""
    edges = edges.copy()
    edges[1:] |= edges[:-1].copy()  # tolerate a one-pixel wobble
    change = np.diff(np.pad(edges, ((0, 0), (1, 1))).astype(np.int8), axis=1)
    rows, starts = np.nonzero(change == 1)
    _, ends = np.nonzero(change == -1)
    min_length = RULE_MIN_INCHES * ANALYSIS_DPI
    return [
        _Rule(float((row + 1) * step), float(start * step), float(end * step))
        for row, start, end in zip(rows, starts, ends)
        if end - start >= min_length
    ]


# ---------------------------------------------------------------------------
# Layout reconstruction: geometry of OCR lines, helped by the picture.


def layout_page(lines: list[_Line], picture: _Picture) -> str:
    """Render one page's OCR lines as ordered, row-merged text blocks."""
    lines = [_clean(line) for line in lines if not _is_junk(line)]
    if not lines:
        return "(no text found)"
    layout = _Layout(statistics.median(line.height for line in lines), picture)
    blocks = layout.xy_cut(lines)
    out: list[str] = []
    for block in blocks:
        if len(blocks) > 1:
            out.append(_position_label(block, picture.width, picture.height))
        out.extend(_block_rows(block, layout.unit))
        out.append("")
    return "\n".join(out).rstrip()


def _is_junk(line: _Line) -> bool:
    # Tall narrow boxes: sideways credits, or ornament borders read as letters.
    return line.height > 2.5 * (line.x1 - line.x0) and len(line.text) > 2


_TIME_ZERO = re.compile(r"(?<=\d[:.])[OoÖöÓóÒò](?=\d)|(?<=\d[:.]\d)[OoÖöÓóÒò]")


def _clean(line: _Line) -> _Line:
    """Fix the one OCR confusion that changes a time: O for 0 after the colon."""
    text = _TIME_ZERO.sub("0", line.text)
    words = tuple(_Word(word.x0, word.x1, _TIME_ZERO.sub("0", word.text)) for word in line.words)
    return _Line(line.x0, line.y0, line.x1, line.y1, text, words)


def _split_at(line: _Line, x: float, tolerance: float) -> tuple[_Line, _Line] | None:
    """Split a box the detector ran across a gutter at x, by its words."""
    left = [word for word in line.words if (word.x0 + word.x1) / 2 < x]
    right = [word for word in line.words if (word.x0 + word.x1) / 2 >= x]
    if not left or not right or left[-1].x1 > x + tolerance or right[0].x0 < x - tolerance:
        return None
    return (
        _Line(line.x0, line.y0, left[-1].x1, line.y1, " ".join(w.text for w in left), tuple(left)),
        _Line(
            right[0].x0, line.y0, line.x1, line.y1, " ".join(w.text for w in right), tuple(right)
        ),
    )


def _gaps(intervals: list[tuple[float, float]], min_gap: float) -> list[tuple[float, float]]:
    """Empty stretches between the union of `intervals`, at least `min_gap` wide."""
    ordered = sorted(intervals)
    gaps: list[tuple[float, float]] = []
    reach = ordered[0][1]
    for start, end in ordered[1:]:
        if start - reach >= min_gap:
            gaps.append((reach, start))
        reach = max(reach, end)
    return gaps


def _covered(segments: list[tuple[float, float]], start: float, end: float) -> float:
    """Length of [start, end] covered by the union of `segments`."""
    total, reach = 0.0, start
    for seg_start, seg_end in sorted(segments):
        seg_start, seg_end = max(seg_start, reach), min(seg_end, end)
        if seg_end > seg_start:
            total += seg_end - seg_start
            reach = seg_end
    return total


@dataclass(frozen=True)
class _Layout:
    unit: float
    """Median OCR line height on the page, the yardstick for every gap."""
    picture: _Picture

    @property
    def slack(self) -> float:
        """How far OCR boxes are padded past the ink."""
        return 0.35 * self.unit

    def xy_cut(self, lines: list[_Line]) -> list[list[_Line]]:
        """Split lines into reading-ordered blocks; a block never spans a column cut."""
        if len(lines) <= 1:
            return [lines]
        columns = self.column_cut(lines)
        if columns is not None:
            return self.xy_cut(columns[0]) + self.xy_cut(columns[1])

        bands = _gaps([(line.y0, line.y1) for line in lines], 1.0)
        clean_bands = [
            (self.ruled(lines, gap), gap[1] - gap[0], gap)
            for gap in bands
            if self.ruled(lines, gap) or not self.inside_columns(lines, gap)
        ]
        if clean_bands:
            return self.cut_rows(lines, max(clean_bands)[2])

        peeled = self.peel(lines)
        if peeled is not None:
            head, body, tail = peeled
            return [block for part in (head, body, tail) if part for block in self.xy_cut(part)]

        if bands:
            return self.cut_rows(lines, max(bands, key=lambda gap: gap[1] - gap[0]))
        return [lines]

    def column_cut(self, lines: list[_Line]) -> tuple[list[_Line], list[_Line]] | None:
        """Where to split lines into a left and a right column, if anywhere.

        Skips any boundary whose two sides read as one table.
        """
        for x in self.boundaries(lines):
            left: list[_Line] = []
            right: list[_Line] = []
            for line in lines:
                if line.x0 < x - self.slack and line.x1 > x + self.slack:
                    pieces = _split_at(line, x, self.slack)
                    if pieces is None:
                        break
                    left.append(pieces[0])
                    right.append(pieces[1])
                else:
                    (left if line.cx < x else right).append(line)
            else:
                if left and right and not _looks_like_table(left, right):
                    return left, right
        return None

    def boundaries(self, lines: list[_Line]) -> list[float]:
        """Candidate column boundaries (x), most convincing first.

        Empty strips between OCR boxes (widest first), then edges in the
        picture, then empty strips in the ink, which also catch gutters OCR
        ran a box across.
        """
        found: list[float] = []
        gutters = _gaps([(line.x0, line.x1) for line in lines], MIN_GUTTER * self.unit)
        for start, end in sorted(gutters, key=lambda gap: gap[0] - gap[1]):
            found.append((start + end) / 2)
        found += self.rule_positions(lines)
        found += self.ink_gutters(lines)
        return found

    def ink_gutters(self, lines: list[_Line]) -> list[float]:
        """Centres of vertical strips with no ink over the lines' full height.

        Only over five rows or more: across fewer, word spaces line up by chance.
        """
        rows = 1
        centres = sorted(line.cy for line in lines)
        for above, below in zip(centres, centres[1:]):
            rows += below - above > 0.5 * self.unit
        if rows < 5:
            return []
        step = self.picture.step
        top = int(min(line.y0 for line in lines) / step)
        bottom = int(max(line.y1 for line in lines) / step) + 1
        left = int(min(line.x0 for line in lines) / step)
        right = int(max(line.x1 for line in lines) / step) + 1
        profile = self.picture.ink[top:bottom, left:right].sum(axis=0)
        free = np.concatenate(([False], profile <= 0.01 * (bottom - top), [False]))
        change = np.diff(free.astype(np.int8))
        starts = np.nonzero(change == 1)[0]
        ends = np.nonzero(change == -1)[0]
        min_width = 0.4 * self.unit / step
        runs = [
            (end - start, (left + (start + end) / 2) * step)
            for start, end in zip(starts, ends)
            if end - start >= min_width and start > 0 and end < len(profile)
        ]
        return [float(x) for _, x in sorted(runs, reverse=True)]

    def rule_positions(self, lines: list[_Line]) -> list[float]:
        """x of picture edges that run down most of these lines and cross none.

        Stacked boxes rarely share an exact edge, so edges less than a line
        height apart count together towards covering the lines' height.
        """
        top = min(line.y0 for line in lines)
        bottom = max(line.y1 for line in lines)
        left = min(line.x0 for line in lines)
        right = max(line.x1 for line in lines)
        slack = self.slack
        near = sorted(
            (
                rule
                for rule in self.picture.vertical
                if left + slack < rule.at < right - slack and rule.end > top and rule.start < bottom
            ),
            key=lambda rule: rule.at,
        )
        clusters: list[list[_Rule]] = []
        for rule in near:
            if clusters and rule.at - clusters[-1][0].at <= 1.5 * self.unit:
                clusters[-1].append(rule)
            else:
                clusters.append([rule])
        scored: list[tuple[float, float]] = []
        for cluster in clusters:
            segments = [(rule.start, rule.end) for rule in cluster]
            coverage = _covered(segments, top, bottom) / (bottom - top)
            if coverage < 0.6:
                continue
            for x in sorted({rule.at for rule in cluster}):
                if not any(line.x0 < x - slack and line.x1 > x + slack for line in lines):
                    scored.append((coverage, x))
                    break
        return [x for _, x in sorted(scored, reverse=True)]

    def ruled(self, lines: list[_Line], gap: tuple[float, float]) -> bool:
        """Whether a horizontal edge spans the lines' width inside a gap.

        The top or bottom of a box or a full-width rule ends a band of
        columns even where the next band has its gutter at the same x.
        """
        left = min(line.x0 for line in lines)
        right = max(line.x1 for line in lines)
        segments = [
            (rule.start, rule.end)
            for rule in self.picture.horizontal
            if gap[0] - self.slack <= rule.at <= gap[1] + self.slack
        ]
        return bool(segments) and _covered(segments, left, right) >= 0.8 * (right - left)

    def cut_rows(self, lines: list[_Line], gap: tuple[float, float]) -> list[list[_Line]]:
        middle = (gap[0] + gap[1]) / 2
        top = self.xy_cut([line for line in lines if line.y1 <= middle])
        bottom = self.xy_cut([line for line in lines if line.y0 >= middle])
        if len(top) == 1 and len(bottom) == 1:
            return [top[0] + bottom[0]]  # neither half has columns: one block
        return top + bottom

    def peel(self, lines: list[_Line]) -> tuple[list[_Line], list[_Line], list[_Line]] | None:
        """Split off up to 3 heading/footer rows that block a column boundary.

        A page title that overlaps the top of the columns below it leaves no
        horizontal gap to cut and no gutter either; without it, the columns
        separate. Whole rows only, so a table row is never torn apart.
        """
        rows = _rows(lines)
        limit = min(3, len(rows) - 2)
        for top in range(limit + 1):
            for bottom in range(limit + 1 - top):
                if top == bottom == 0:
                    continue
                body = [line for row in rows[top : len(rows) - bottom] for line in row]
                if self.column_cut(body) is not None:
                    head = [line for row in rows[:top] for line in row]
                    tail = [line for row in rows[len(rows) - bottom :] for line in row]
                    return head, body, tail
        return None

    def inside_columns(self, lines: list[_Line], gap: tuple[float, float]) -> bool:
        """Whether a horizontal gap is only a pause inside side-by-side columns.

        Cutting there would read the top halves of every column, then the
        bottom halves. It is one if a column boundary runs through the text
        just above and just below the gap, with text on both sides of it on
        both sides of the gap.
        """
        window = 3 * self.unit
        above = [line for line in lines if gap[0] - window <= line.y1 <= gap[0]]
        below = [line for line in lines if gap[1] <= line.y0 <= gap[1] + window]
        if not above or not below:
            return False
        for x in self.boundaries(above + below):
            if all(
                any(line.x0 < x - self.slack for line in side)
                and any(line.x1 > x + self.slack for line in side)
                for side in (above, below)
            ):
                return True
        return False


def _looks_like_table(left: list[_Line], right: list[_Line]) -> bool:
    """Whether a boundary separates the cells of one table rather than two columns.

    Most lines of the sparser side (e.g. "Sun 2/15" beside that day's list of
    Masses) sit exactly on the baseline of a line across the boundary, and at
    least one side holds short cells (times, days, dates). Two independent
    columns rarely line up that exactly, and when they do both hold long lines.
    """
    sparse, dense = sorted((left, right), key=len)
    aligned = sum(
        1 for a in sparse if any(abs(a.cy - b.cy) <= 0.12 * min(a.height, b.height) for b in dense)
    )
    # A lone cell ("4:00 PM" beside a three-line intention) counts too.
    if aligned < min(2, len(sparse)) or aligned < 0.6 * len(sparse):
        return False
    short_cells = min(
        statistics.median(len(line.text) for line in left),
        statistics.median(len(line.text) for line in right),
    )
    return short_cells <= 24


def _rows(lines: list[_Line]) -> list[list[_Line]]:
    """Group boxes on the same baseline into rows, top to bottom, left to right."""
    rows: list[list[_Line]] = []
    for line in sorted(lines, key=lambda item: item.cy):
        # Same row only if each box's centre lies within the other's height, so
        # a tall display line can't swallow several rows of small text.
        if rows and all(
            other.y0 <= line.cy <= other.y1 and line.y0 <= other.cy <= line.y1 for other in rows[-1]
        ):
            rows[-1].append(line)
        else:
            rows.append([line])
    for row in rows:
        row.sort(key=lambda item: item.x0)
    return rows


def _block_rows(block: list[_Line], unit: float) -> list[str]:
    """Render a block top-down, one line of text per row of boxes."""
    out: list[str] = []
    previous_bottom: float | None = None
    for row in _rows(block):
        top = min(item.y0 for item in row)
        if previous_bottom is not None and top - previous_bottom > 0.9 * unit:
            out.append("")
        previous_bottom = max(item.y1 for item in row)
        text = row[0].text
        for before, after in zip(row, row[1:]):
            gap = after.x0 - before.x1
            text += (" | " if gap > 1.2 * unit else " ") + after.text
        out.append(text)
    return out


def _position_label(block: list[_Line], width: float, height: float) -> str:
    x0 = min(line.x0 for line in block) / width * 100
    x1 = max(line.x1 for line in block) / width * 100
    y0 = min(line.y0 for line in block) / height * 100
    y1 = max(line.y1 for line in block) / height * 100
    return f"[x {x0:.0f}-{x1:.0f}% y {y0:.0f}-{y1:.0f}%]"
