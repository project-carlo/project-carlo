from __future__ import annotations

import json
import zlib
from dataclasses import replace
from io import BytesIO

import pytest
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    NumberObject,
)

from pdf_extract import pdf_detail
from pdf_extract.pdf_detail import (
    DetailThresholds,
    extract_pdf_features,
    route_pdf_detail,
    route_scan_risk,
)


def _pdf(
    *,
    scan: str | None = None,
    native_size: int | None = None,
    placements: bytes | None = None,
    pages: int = 1,
) -> bytes:
    writer = PdfWriter()
    for _ in range(pages):
        page = writer.add_blank_page(width=612, height=792)
        resources = DictionaryObject()
        commands = b""
        if scan is not None:
            with Image.new("L", (612, 792), 255) as image:
                draw = ImageDraw.Draw(image)
                if scan == "dense":
                    font = ImageFont.load_default(size=10)
                    for row in range(40, 750, 15):
                        draw.text(
                            (25, row),
                            "Small printed schedule text 0123456789 " * 3,
                            fill=0,
                            font=font,
                        )
                elif scan == "solid":
                    draw.rectangle((0, 0, 611, 791), fill=0)
                elif scan == "large":
                    draw.text((30, 120), "LARGE TEXT", fill=0, font=ImageFont.load_default(size=60))
                image_object = DecodedStreamObject()
                image_object.set_data(zlib.compress(image.tobytes()))
            image_object.update(
                {
                    NameObject("/Type"): NameObject("/XObject"),
                    NameObject("/Subtype"): NameObject("/Image"),
                    NameObject("/Width"): NumberObject(612),
                    NameObject("/Height"): NumberObject(792),
                    NameObject("/ColorSpace"): NameObject("/DeviceGray"),
                    NameObject("/BitsPerComponent"): NumberObject(8),
                    NameObject("/Filter"): NameObject("/FlateDecode"),
                }
            )
            resources[NameObject("/XObject")] = DictionaryObject(
                {
                    NameObject("/Im0"): writer._add_object(image_object),
                }
            )
            commands += placements or b"q 612 0 0 792 0 0 cm /Im0 Do Q\n"
        if native_size is not None:
            font_object = DictionaryObject(
                {
                    NameObject("/Type"): NameObject("/Font"),
                    NameObject("/Subtype"): NameObject("/Type1"),
                    NameObject("/BaseFont"): NameObject("/Helvetica"),
                }
            )
            resources[NameObject("/Font")] = DictionaryObject(
                {
                    NameObject("/F1"): writer._add_object(font_object),
                }
            )
            commands += f"BT /F1 {native_size} Tf 30 740 Td 14 TL\n".encode()
            commands += b"(Native text schedule 0123456789 repeated for testing.) Tj T*\n" * 40
            commands += b"ET\n"
        page[NameObject("/Resources")] = resources
        content = DecodedStreamObject()
        content.set_data(commands)
        page[NameObject("/Contents")] = writer._add_object(content)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


@pytest.fixture(scope="module")
def dense_features():
    return extract_pdf_features(_pdf(scan="dense"))


def test_dense_scan_features_and_routing(dense_features):
    page = dense_features["pages"][0]
    assert dense_features["schema_version"] == 1
    assert (page["width_pt"], page["height_pt"]) == (612, 792)
    assert page["text_chars"] == 0
    assert page["image_count"] == 1
    assert page["image_coverage_fraction_estimate"] == 1
    assert page["max_displayed_image_area_fraction_estimate"] == 1
    assert page["native_char_height_p10_pt"] is None
    assert 0.015 < page["ink_density"] < 0.35
    assert page["text_like_component_count"] > 100
    assert page["projection_line_count"] > 30
    assert 15 < page["line_pitch_px"] < 25
    assert page["text_like_height_p10_px"] > 0
    assert page["text_like_width_median_px"] > 0
    assert page["errors"] == []
    decision = route_pdf_detail(dense_features)
    assert decision["detail"] == "high"
    assert decision["pages"][0]["reasons"] == ["dense_small_raster_text"]
    assert not decision["incomplete"]
    assert json.loads(json.dumps(dense_features, allow_nan=False)) == dense_features
    assert json.loads(json.dumps(decision, allow_nan=False)) == decision


@pytest.mark.parametrize("scan", [None, "empty", "solid", "large"])
def test_empty_nontext_and_large_print_do_not_trigger(scan):
    features = extract_pdf_features(_pdf(scan=scan))
    assert route_pdf_detail(features)["detail"] == "low"
    if scan in (None, "empty"):
        page = features["pages"][0]
        assert page["ink_density"] == 0
        assert page["text_like_component_count"] == 0
        assert page["line_pitch_px"] is None
        assert page["text_like_height_median_px"] is None
        assert page["errors"] == []


def test_native_glyph_height_and_rule():
    small = extract_pdf_features(_pdf(native_size=7))
    larger = extract_pdf_features(_pdf(native_size=14))
    page = small["pages"][0]
    assert page["text_chars"] > 1000
    assert page["image_count"] == 0
    assert page["image_coverage_fraction_estimate"] == 0
    assert 3 < page["native_char_height_p10_pt"] < 7
    assert page["native_height_sample_count"] > 1000
    assert page["native_char_height_p10_low_detail_px"] == pytest.approx(
        page["native_char_height_p10_pt"] * 512 / 792,
    )
    assert larger["pages"][0]["native_char_height_p10_pt"] == pytest.approx(
        2 * page["native_char_height_p10_pt"],
        rel=0.01,
    )
    assert route_pdf_detail(small)["pages"][0]["reasons"] == ["small_native_text"]
    assert route_pdf_detail(larger)["detail"] == "low"


def test_mixed_image_and_native_text():
    features = extract_pdf_features(_pdf(scan="dense", native_size=14))
    assert features["pages"][0]["text_chars"] > 80
    assert "dense_small_raster_text" in route_pdf_detail(features)["pages"][0]["reasons"]


def test_displayed_placements_overlap_not_pixel_dimensions():
    data = _pdf(
        scan="empty",
        placements=(b"q 306 0 0 792 0 0 cm /Im0 Do Q\nq 306 0 0 792 153 0 cm /Im0 Do Q\n"),
    )
    page = extract_pdf_features(data)["pages"][0]
    assert page["image_count"] == 2
    assert page["image_coverage_fraction_estimate"] == pytest.approx(0.75)
    assert page["max_displayed_image_area_fraction_estimate"] == pytest.approx(0.5)


def test_form_image_transform_and_saved_graphics_state():
    reader = PdfReader(BytesIO(_pdf(scan="empty")))
    writer = PdfWriter()
    page = writer.add_page(reader.pages[0])
    form = DecodedStreamObject()
    form.set_data(b"q 306 0 0 396 0 0 cm /Im0 Do Q")
    form.update(
        {
            NameObject("/Type"): NameObject("/XObject"),
            NameObject("/Subtype"): NameObject("/Form"),
            NameObject("/Resources"): page["/Resources"],
            NameObject("/BBox"): page.mediabox,
        }
    )
    page[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/XObject"): DictionaryObject({NameObject("/Fm"): writer._add_object(form)}),
        }
    )
    content = DecodedStreamObject()
    content.set_data(b"q 1 0 0 1 306 396 cm /Fm Do Q /Fm Do")
    page[NameObject("/Contents")] = writer._add_object(content)
    out = BytesIO()
    writer.write(out)
    features = extract_pdf_features(out.getvalue())["pages"][0]
    assert features["errors"] == []
    assert features["image_count"] == 2
    assert features["image_coverage_fraction_estimate"] == pytest.approx(0.5)
    assert features["max_displayed_image_area_fraction_estimate"] == pytest.approx(0.25)


def test_parameterized_rule_and_missing_measurements(dense_features):
    limits = replace(DetailThresholds(), min_text_like_components=100_000)
    assert route_pdf_detail(dense_features, thresholds=limits)["detail"] == "low"
    incomplete = {"pages": [{"page_number": 1, "errors": ["text: ValueError"]}]}
    assert route_pdf_detail(incomplete)["detail"] == "low"
    assert route_pdf_detail(incomplete)["incomplete"]


def test_path_page_limit_and_render_cap(tmp_path):
    path = tmp_path / "pages.pdf"
    path.write_bytes(_pdf(pages=2))
    features = extract_pdf_features(path, max_pages=1, max_render_pixels=100_000)
    assert features["page_count"] == 2
    assert features["analyzed_page_count"] == 1
    assert features["truncated"]
    assert route_pdf_detail(features)["incomplete"]
    page = features["pages"][0]
    assert page["render_width_px"] * page["render_height_px"] <= 100_000
    assert page["render_dpi"] < 100


def test_lock_and_resources_released_after_failure(monkeypatch):
    original = pdf_detail._raster_features
    document_class = pdf_detail.pdfium.PdfDocument
    page_class = pdf_detail.pdfium.PdfPage
    document_factory = pdf_detail.pdfium.PdfDocument
    get_page = document_class.get_page
    get_textpage = page_class.get_textpage
    render = page_class.render
    resources = []
    images = []

    def track_document(*args, **kwargs):
        document = document_factory(*args, **kwargs)
        resources.append(document)
        return document

    def track_page(*args, **kwargs):
        page = get_page(*args, **kwargs)
        resources.append(page)
        return page

    def track_textpage(*args, **kwargs):
        textpage = get_textpage(*args, **kwargs)
        resources.append(textpage)
        return textpage

    def track_bitmap(*args, **kwargs):
        bitmap = render(*args, **kwargs)
        resources.append(bitmap)
        return bitmap

    def fail(*args):
        assert pdf_detail._PDFIUM_LOCK.locked()
        images.append(args[0])
        raise RuntimeError("synthetic raster failure")

    monkeypatch.setattr(pdf_detail.pdfium, "PdfDocument", track_document)
    monkeypatch.setattr(document_class, "get_page", track_page)
    monkeypatch.setattr(page_class, "get_textpage", track_textpage)
    monkeypatch.setattr(page_class, "render", track_bitmap)
    monkeypatch.setattr(pdf_detail, "_raster_features", fail)
    with pytest.raises(RuntimeError, match="synthetic raster failure"):
        extract_pdf_features(_pdf())
    assert pdf_detail._PDFIUM_LOCK.acquire(blocking=False)
    pdf_detail._PDFIUM_LOCK.release()
    assert len(resources) == 4
    assert all(resource.raw is None for resource in resources)
    with pytest.raises(ValueError):
        images[0].getpixel((0, 0))
    monkeypatch.setattr(pdf_detail, "_raster_features", original)
    assert extract_pdf_features(_pdf())["pages"][0]["errors"] == []


@pytest.mark.parametrize(
    "kwargs",
    [
        {"dpi": 0},
        {"dpi": float("nan")},
        {"low_detail_max_side": 0},
        {"ink_threshold": 256},
        {"max_render_pixels": 0},
        {"max_pages": 0},
    ],
)
def test_invalid_settings(kwargs):
    with pytest.raises(ValueError):
        extract_pdf_features(_pdf(), **kwargs)


def _scan_risk_document(count, scan_pages):
    return {
        "truncated": False,
        "pages": [
            {
                "page_number": number,
                "errors": [],
                "text_chars": 0 if number in scan_pages else 1000,
                "image_coverage_fraction_estimate": 0.7 if number in scan_pages else 0.1,
                "text_like_component_count": 100,
                "ink_density": 0.015,
                "text_like_height_median_low_detail_px": 6.0,
                "line_pitch_low_detail_px": 12.0,
            }
            for number in range(1, count + 1)
        ],
    }


def test_scan_risk_dense_scan_and_native_text(dense_features):
    decision = route_scan_risk(dense_features)
    assert decision["detail"] == "high"
    assert decision["reasons"] == ["early_scan_small_text", "predominantly_scanned_with_small_text"]
    assert decision["scan_small_page_numbers"] == [1]
    assert json.loads(json.dumps(decision, allow_nan=False)) == decision
    native = extract_pdf_features(_pdf(native_size=7))
    assert route_pdf_detail(native)["detail"] == "high"
    assert route_scan_risk(native)["detail"] == "low"


def test_scan_risk_early_page_not_late_advertising():
    early = route_scan_risk(_scan_risk_document(10, {3}))
    assert early["detail"] == "high"
    assert early["reasons"] == ["early_scan_small_text"]
    assert early["early_scan_small_page_numbers"] == [3]
    late = route_scan_risk(_scan_risk_document(10, {9, 10}))
    assert late["detail"] == "low"
    assert late["reasons"] == []
    assert late["scan_small_page_numbers"] == [9, 10]


@pytest.mark.parametrize(
    "count,scan_pages,detail",
    [
        (6, {4, 5, 6}, "high"),
        (7, {4, 5, 6}, "low"),
        (7, {4, 5, 6, 7}, "high"),
    ],
)
def test_scan_risk_at_least_half_including_later_schedule(count, scan_pages, detail):
    decision = route_scan_risk(_scan_risk_document(count, scan_pages))
    assert decision["detail"] == detail
    assert decision["reasons"] == (
        ["predominantly_scanned_with_small_text"] if detail == "high" else []
    )


def test_predominant_scan_with_only_one_later_small_text_measurement():
    features = _scan_risk_document(5, {1, 2, 3, 4, 5})
    for page in features["pages"]:
        if page["page_number"] != 4:
            page["line_pitch_low_detail_px"] = 40
    decision = route_scan_risk(features)
    assert decision["detail"] == "high"
    assert decision["reasons"] == ["predominantly_scanned_with_small_text"]
    assert decision["scan_small_page_numbers"] == [4]
    assert decision["scan_page_numbers"] == [1, 2, 3, 4, 5]
    features["pages"][3]["line_pitch_low_detail_px"] = 40
    assert route_scan_risk(features)["detail"] == "low"


@pytest.mark.parametrize(
    "field,value",
    [
        ("text_chars", 80),
        ("image_coverage_fraction_estimate", 0.699),
        ("text_like_component_count", 99),
        ("ink_density", 0.014),
        ("ink_density", 0.351),
        ("text_like_height_median_low_detail_px", 6.01),
        ("text_like_height_median_low_detail_px", 0),
        ("line_pitch_low_detail_px", 12.01),
        ("line_pitch_low_detail_px", 0),
        ("text_chars", None),
        ("image_coverage_fraction_estimate", None),
        ("text_like_component_count", None),
        ("ink_density", None),
        ("text_like_height_median_low_detail_px", None),
        ("line_pitch_low_detail_px", None),
    ],
)
def test_scan_risk_requires_all_positive_measurements(field, value):
    features = _scan_risk_document(1, {1})
    features["pages"][0][field] = value
    assert route_scan_risk(features)["detail"] == "low"


def test_scan_risk_errors_and_truncation_fallbacks():
    features = _scan_risk_document(1, set())
    features["pages"][0]["errors"] = ["images: ValueError"]
    features["truncated"] = True
    decision = route_scan_risk(features)
    assert decision["detail"] == "high"
    assert decision["reasons"] == ["page_feature_errors", "truncated_document"]
    assert decision["error_page_numbers"] == [1]
    assert decision["scan_small_page_numbers"] == []
    assert route_scan_risk({"pages": []})["reasons"] == ["no_analyzed_pages"]
    features = _scan_risk_document(1, set())
    features["errors"] = ["document unavailable"]
    assert route_scan_risk(features)["reasons"] == ["document_feature_errors"]


def test_scan_risk_parameters():
    features = _scan_risk_document(10, {4})
    assert route_scan_risk(features)["detail"] == "low"
    assert route_scan_risk(features, first_pages=4)["detail"] == "high"
    assert route_scan_risk(features, first_pages=4, min_scan_coverage=0.8)["detail"] == "low"
    limits = replace(DetailThresholds(), min_text_like_components=101)
    assert route_scan_risk(features, first_pages=4, thresholds=limits)["detail"] == "low"
    for kwargs in (
        {"first_pages": 0},
        {"min_scan_coverage": 1.1},
        {"min_scan_coverage": float("nan")},
    ):
        with pytest.raises(ValueError):
            route_scan_risk(features, **kwargs)
