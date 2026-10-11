"""Local PDF features and unfitted detail routing, without classifier/API calls.

Image count measures draw occurrences, including repeated/off-page placements.
Image areas use visible axis-aligned placement bounds, unioned for coverage.
Rotation, clipping paths and transparency can overestimate these areas. Raster
components are text-like geometry, not OCR. Low-detail sizes assume a whole-page
resize to a configurable maximum side, not a provider processing contract.
"""

from __future__ import annotations

import math
from contextlib import closing
from dataclasses import asdict, dataclass
from io import BytesIO
from pathlib import Path
from statistics import median
from typing import Any

import pypdfium2 as pdfium
from PIL import Image
from pypdf import PdfReader
from pypdf.generic import ContentStream

from pdf_extract.classifiers.openai_responses import _PDFIUM_LOCK


@dataclass(frozen=True)
class DetailThresholds:
    """Exploratory defaults only; paired evaluation must establish useful cutoffs."""

    text_poor_chars: int = 80
    mixed_image_coverage: float = 0.2
    min_ink_density: float = 0.015
    max_ink_density: float = 0.35
    min_text_like_components: int = 100
    max_component_height_low_detail_px: float = 6.0
    max_line_pitch_low_detail_px: float = 12.0
    max_native_height_low_detail_px: float = 3.0


def _quantile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    return float(ordered[int((len(ordered) - 1) * fraction)])


def _compose(inner: list[float], outer: list[float]) -> list[float]:
    inner_xx, inner_xy, inner_yx, inner_yy, inner_tx, inner_ty = inner
    outer_xx, outer_xy, outer_yx, outer_yy, outer_tx, outer_ty = outer
    return [
        inner_xx * outer_xx + inner_xy * outer_yx,
        inner_xx * outer_xy + inner_xy * outer_yy,
        inner_yx * outer_xx + inner_yy * outer_yx,
        inner_yx * outer_xy + inner_yy * outer_yy,
        inner_tx * outer_xx + inner_ty * outer_yx + outer_tx,
        inner_tx * outer_xy + inner_ty * outer_yy + outer_ty,
    ]


def _image_features(page: Any, reader: PdfReader) -> dict[str, Any]:
    box = page.cropbox
    bounds = tuple(float(value) for value in (box.left, box.bottom, box.right, box.top))
    page_area = (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])
    rectangles: list[tuple[float, float, float, float]] = []
    count = 0

    def record(matrix: list[float]) -> None:
        nonlocal count
        count += 1
        xx, xy, yx, yy, tx, ty = matrix
        xs = (tx, xx + tx, yx + tx, xx + yx + tx)
        ys = (ty, xy + ty, yy + ty, xy + yy + ty)
        left, right = max(min(xs), bounds[0]), min(max(xs), bounds[2])
        bottom, top = max(min(ys), bounds[1]), min(max(ys), bounds[3])
        if right > left and top > bottom:
            rectangles.append((left, bottom, right, top))

    def walk(content: Any, resources: Any, matrix: list[float], ancestors: set) -> None:
        stack: list[list[float]] = []
        for operands, operator in ContentStream(content, reader).operations:
            if operator == b"q":
                stack.append(matrix[:])
            elif operator == b"Q" and stack:
                matrix = stack.pop()
            elif operator == b"cm":
                matrix = _compose([float(value) for value in operands], matrix)
            elif operator == b"INLINE IMAGE":
                record(matrix)
            elif operator == b"Do":
                objects = resources["/XObject"].get_object()
                obj = objects[operands[0]].get_object()
                if obj.get("/Subtype") == "/Image":
                    record(matrix)
                elif obj.get("/Subtype") == "/Form":
                    identity = id(obj)
                    if identity in ancestors or len(ancestors) >= 32:
                        raise ValueError("Cyclic or excessively nested image forms")
                    transform = [float(value) for value in obj.get("/Matrix", [1, 0, 0, 1, 0, 0])]
                    walk(
                        obj,
                        obj.get("/Resources", resources),
                        _compose(transform, matrix),
                        ancestors | {identity},
                    )

    walk(page.get_contents(), page.get("/Resources", {}), [1, 0, 0, 1, 0, 0], set())
    xs = sorted({value for rectangle in rectangles for value in (rectangle[0], rectangle[2])})
    area = 0.0
    for left, right in zip(xs, xs[1:]):
        intervals = sorted(
            (bottom, top) for x0, bottom, x1, top in rectangles if x0 < right and x1 > left
        )
        end = -math.inf
        height = 0.0
        for bottom, top in intervals:
            height += max(0.0, top - max(bottom, end))
            end = max(end, top)
        area += (right - left) * height
    maximum = max(
        ((right - left) * (top - bottom) for left, bottom, right, top in rectangles), default=0.0
    )
    return {
        "image_count": count,
        "image_coverage_fraction_estimate": min(1.0, area / page_area),
        "max_displayed_image_area_fraction_estimate": min(1.0, maximum / page_area),
    }


def _raster_features(image: Image.Image, low_scale: float, ink_threshold: int) -> dict[str, Any]:
    width, height = image.size
    with closing(image.convert("L")) as grayscale:
        pixels = grayscale.tobytes()
    ink = bytearray(value < ink_threshold for value in pixels)
    rows = [sum(ink[start : start + width]) for start in range(0, len(ink), width)]
    density = sum(rows) / len(ink)
    cutoff = max(width * 0.003, max(rows, default=0) * 0.15)
    centers: list[float] = []
    start = None
    for row, amount in enumerate([*rows, 0]):
        if amount > cutoff and start is None:
            start = row
        elif amount <= cutoff and start is not None:
            centers.append((start + row - 1) / 2)
            start = None
    pitches = [second - first for first, second in zip(centers, centers[1:])]
    component_heights: list[float] = []
    component_widths: list[float] = []
    component_count = 0
    for origin in range(len(ink)):
        if not ink[origin]:
            continue
        component_count += 1
        ink[origin] = 0
        pending = [origin]
        left = right = origin % width
        top = bottom = origin // width
        area = 0
        while pending:
            position = pending.pop()
            column, row = position % width, position // width
            left, right = min(left, column), max(right, column)
            top, bottom = min(top, row), max(bottom, row)
            area += 1
            for neighbor_row in range(max(0, row - 1), min(height, row + 2)):
                for neighbor_column in range(max(0, column - 1), min(width, column + 2)):
                    neighbor = neighbor_row * width + neighbor_column
                    if ink[neighbor]:
                        ink[neighbor] = 0
                        pending.append(neighbor)
        component_width, component_height = right - left + 1, bottom - top + 1
        if (
            area >= 3
            and 2 <= component_height <= height * 0.06
            and component_width <= width * 0.06
            and 0.1 <= component_width / component_height <= 8
            and area / (component_width * component_height) >= 0.08
        ):
            component_heights.append(float(component_height))
            component_widths.append(float(component_width))
    pitch = float(median(pitches)) if pitches else None
    component_height = _quantile(component_heights, 0.5)
    return {
        "render_width_px": width,
        "render_height_px": height,
        "ink_density": density,
        "projection_line_count": len(centers),
        "line_pitch_px": pitch,
        "line_pitch_low_detail_px": pitch * low_scale if pitch is not None else None,
        "connected_component_count": component_count,
        "text_like_component_count": len(component_heights),
        "text_like_height_p10_px": _quantile(component_heights, 0.1),
        "text_like_height_median_px": component_height,
        "text_like_width_median_px": _quantile(component_widths, 0.5),
        "text_like_height_median_low_detail_px": (
            component_height * low_scale if component_height is not None else None
        ),
    }


def extract_pdf_features(
    source: bytes | str | Path,
    *,
    dpi: float = 100,
    low_detail_max_side: int = 512,
    ink_threshold: int = 200,
    max_render_pixels: int = 2_000_000,
    max_pages: int | None = None,
) -> dict[str, Any]:
    """Return versioned JSON primitives; unavailable measurements are null.

    Pages are one-based. Native heights are PDFium glyph bounds in points (up to
    10,000 glyphs/page), including invisible OCR text. Raster sizes use actual
    capped dimensions. Parse/render failures raise; structural failures appear
    independently in each page's errors. Character counts exclude edge whitespace.
    """
    if not math.isfinite(dpi) or dpi <= 0 or low_detail_max_side <= 0:
        raise ValueError("dpi and low_detail_max_side must be positive")
    if not 1 <= ink_threshold <= 255 or max_render_pixels < 4:
        raise ValueError("Invalid ink_threshold or max_render_pixels")
    if max_pages is not None and max_pages < 1:
        raise ValueError("max_pages must be positive")
    data = source if isinstance(source, bytes) else Path(source).read_bytes()
    reader = PdfReader(BytesIO(data))
    pages: list[dict[str, Any]] = []
    with _PDFIUM_LOCK, closing(pdfium.PdfDocument(data)) as document:
        page_count = len(document)
        for index in range(min(page_count, max_pages or page_count)):
            structural_page = reader.pages[index]
            features: dict[str, Any] = {"page_number": index + 1, "errors": []}
            try:
                features["text_chars"] = len((structural_page.extract_text() or "").strip())
            except Exception as exc:
                features["text_chars"] = None
                features["errors"].append(f"text: {type(exc).__name__}")
            try:
                features.update(_image_features(structural_page, reader))
            except Exception as exc:
                features.update(
                    image_count=None,
                    image_coverage_fraction_estimate=None,
                    max_displayed_image_area_fraction_estimate=None,
                )
                features["errors"].append(f"images: {type(exc).__name__}")
            with closing(document[index]) as page:
                width, height = page.get_size()
                scale = min(dpi / 72, math.sqrt(max_render_pixels / (width * height)))
                while math.ceil(width * scale) * math.ceil(height * scale) > max_render_pixels:
                    scale *= 0.99
                features.update(width_pt=width, height_pt=height, render_dpi=scale * 72)
                heights: list[float] = []
                try:
                    with closing(page.get_textpage()) as textpage:
                        for char_index in range(min(textpage.count_chars(), 10_000)):
                            if not textpage.get_text_range(char_index, 1).strip():
                                continue
                            left, bottom, right, top = textpage.get_charbox(char_index)
                            if right > left and top > bottom:
                                heights.append(top - bottom)
                except Exception as exc:
                    features["errors"].append(f"native_heights: {type(exc).__name__}")
                    heights = []
                native_height = _quantile(heights, 0.1)
                features.update(
                    native_height_sample_count=len(heights),
                    native_char_height_p10_pt=native_height,
                    native_char_height_median_pt=_quantile(heights, 0.5),
                    native_char_height_p10_low_detail_px=(
                        native_height * low_detail_max_side / max(width, height)
                        if native_height is not None
                        else None
                    ),
                )
                with closing(page.render(scale=scale)) as bitmap:
                    with closing(bitmap.to_pil()) as image:
                        features.update(
                            _raster_features(
                                image,
                                low_detail_max_side / max(image.size),
                                ink_threshold,
                            )
                        )
            pages.append(features)
    return {
        "schema_version": 1,
        "page_count": page_count,
        "analyzed_page_count": len(pages),
        "truncated": len(pages) < page_count,
        "settings": {
            "dpi": dpi,
            "low_detail_max_side": low_detail_max_side,
            "ink_threshold": ink_threshold,
            "max_render_pixels": max_render_pixels,
        },
        "pages": pages,
    }


def route_pdf_detail(
    features: dict[str, Any],
    *,
    thresholds: DetailThresholds | None = None,
) -> dict[str, Any]:
    """High requires positive small-text evidence; low does not guarantee readability.

    Missing measurements do not trigger high. The caller must handle extraction
    failures/truncated pages. These rules are not fitted quality predictions.
    """
    limits = thresholds or DetailThresholds()
    decisions = []
    for page in features["pages"]:
        reasons = []
        density = page.get("ink_density")
        if density is not None and limits.min_ink_density <= density <= limits.max_ink_density:
            chars = page.get("text_chars")
            coverage = page.get("image_coverage_fraction_estimate")
            raster_candidate = (chars is not None and chars < limits.text_poor_chars) or (
                coverage is not None and coverage >= limits.mixed_image_coverage
            )
            component_height = page.get("text_like_height_median_low_detail_px")
            pitch = page.get("line_pitch_low_detail_px")
            if (
                raster_candidate
                and page.get("text_like_component_count", 0) >= limits.min_text_like_components
                and component_height is not None
                and component_height <= limits.max_component_height_low_detail_px
                and pitch is not None
                and pitch <= limits.max_line_pitch_low_detail_px
            ):
                reasons.append("dense_small_raster_text")
            native_height = page.get("native_char_height_p10_low_detail_px")
            if (
                chars is not None
                and chars >= limits.text_poor_chars
                and page.get("native_height_sample_count", 0) >= limits.text_poor_chars
                and native_height is not None
                and native_height <= limits.max_native_height_low_detail_px
            ):
                reasons.append("small_native_text")
        decisions.append(
            {
                "page_number": page["page_number"],
                "detail": "high" if reasons else "low",
                "reasons": reasons,
            }
        )
    return {
        "detail": "high" if any(page["detail"] == "high" for page in decisions) else "low",
        "thresholds": asdict(limits),
        "pages": decisions,
        "incomplete": features.get("truncated", False)
        or any(page.get("errors") for page in features["pages"]),
    }


def route_scan_risk(
    features: dict[str, Any],
    *,
    thresholds: DetailThresholds | None = None,
    first_pages: int = 3,
    min_scan_coverage: float = 0.7,
) -> dict[str, Any]:
    """Route scan-resolution risk, not a trained or guaranteed-benefit prediction.

    Early scan evidence reduces triggers from image-only advertising at the end
    of otherwise native-text bulletins. A predominantly scanned document with
    any small-text evidence also triggers high to cover later schedules and
    uncertain projection profiles. Errors/truncation trigger high conservatively. Native glyph size
    alone never triggers this rule; route_pdf_detail remains exploratory.
    """
    if first_pages < 1 or not math.isfinite(min_scan_coverage) or not 0 <= min_scan_coverage <= 1:
        raise ValueError("Invalid first_pages or min_scan_coverage")
    limits = thresholds or DetailThresholds()
    pages = features["pages"]
    evidence_pages = []
    scan_pages = []
    early_pages = []
    error_pages = []
    decisions = []
    for index, page in enumerate(pages):
        chars = page.get("text_chars")
        coverage = page.get("image_coverage_fraction_estimate")
        components = page.get("text_like_component_count")
        density = page.get("ink_density")
        height = page.get("text_like_height_median_low_detail_px")
        pitch = page.get("line_pitch_low_detail_px")
        scanned = (
            chars is not None
            and chars < limits.text_poor_chars
            and coverage is not None
            and coverage >= min_scan_coverage
        )
        if scanned:
            scan_pages.append(page["page_number"])
        evidence = (
            scanned
            and components is not None
            and components >= limits.min_text_like_components
            and density is not None
            and limits.min_ink_density <= density <= limits.max_ink_density
            and height is not None
            and 0 < height <= limits.max_component_height_low_detail_px
            and pitch is not None
            and 0 < pitch <= limits.max_line_pitch_low_detail_px
        )
        page_reasons = []
        if evidence:
            evidence_pages.append(page["page_number"])
            page_reasons.append("scan_small_text_evidence")
            if index < first_pages:
                early_pages.append(page["page_number"])
        if page.get("errors"):
            error_pages.append(page["page_number"])
            page_reasons.append("page_feature_errors")
        decisions.append(
            {
                "page_number": page["page_number"],
                "scan_small_text": evidence,
                "reasons": page_reasons,
            }
        )
    reasons = []
    if early_pages:
        reasons.append("early_scan_small_text")
    if pages and evidence_pages and len(scan_pages) * 2 >= len(pages):
        reasons.append("predominantly_scanned_with_small_text")
    if error_pages:
        reasons.append("page_feature_errors")
    if features.get("errors"):
        reasons.append("document_feature_errors")
    if features.get("truncated", False):
        reasons.append("truncated_document")
    if not pages:
        reasons.append("no_analyzed_pages")
    return {
        "detail": "high" if reasons else "low",
        "reasons": reasons,
        "scan_small_page_numbers": evidence_pages,
        "scan_page_numbers": scan_pages,
        "early_scan_small_page_numbers": early_pages,
        "error_page_numbers": error_pages,
        "analyzed_page_count": len(pages),
        "thresholds": {
            "first_pages": first_pages,
            "min_scan_coverage": min_scan_coverage,
            "text_poor_chars": limits.text_poor_chars,
            "min_text_like_components": limits.min_text_like_components,
            "min_ink_density": limits.min_ink_density,
            "max_ink_density": limits.max_ink_density,
            "max_component_height_low_detail_px": limits.max_component_height_low_detail_px,
            "max_line_pitch_low_detail_px": limits.max_line_pitch_low_detail_px,
        },
        "pages": decisions,
    }
