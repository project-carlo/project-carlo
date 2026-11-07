from __future__ import annotations

import logging
import random
import shutil
import zlib
from io import BytesIO

import pytest
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    NameObject,
    NumberObject,
    StreamObject,
)

from pdf_extract import pdf_compact
from pdf_extract.pdf_compact import compact_bulletin_pdf

needs_gs = pytest.mark.skipif(shutil.which("gs") is None, reason="Ghostscript not installed")


def _blank_pdf(pages: int) -> bytes:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=612, height=792)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def _photo_pdf(pages: int, *, px: int = 1200) -> bytes:
    """Letter pages each holding a `px`-square photo-like RGB image (well over 150 dpi)."""
    rng = random.Random(0)
    writer = PdfWriter()
    for _ in range(pages):
        page = writer.add_blank_page(width=612, height=792)
        rows = bytearray()
        for y in range(px):
            for x in range(px):
                rows += bytes(((x + y) % 256, (x * 3) % 256, rng.randrange(256)))
        image = StreamObject()
        image._data = zlib.compress(bytes(rows))
        image.update({
            NameObject("/Type"): NameObject("/XObject"),
            NameObject("/Subtype"): NameObject("/Image"),
            NameObject("/Width"): NumberObject(px),
            NameObject("/Height"): NumberObject(px),
            NameObject("/ColorSpace"): NameObject("/DeviceRGB"),
            NameObject("/BitsPerComponent"): NumberObject(8),
            NameObject("/Filter"): NameObject("/FlateDecode"),
        })
        content = DecodedStreamObject()
        content.set_data(b"q 540 0 0 540 36 126 cm /Im0 Do Q")
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/XObject"): DictionaryObject({
                NameObject("/Im0"): writer._add_object(image),
            }),
        })
        page[NameObject("/Contents")] = writer._add_object(content)
        page[NameObject("/MediaBox")] = ArrayObject(
            [NumberObject(0), NumberObject(0), NumberObject(612), NumberObject(792)],
        )
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def _pages(data: bytes) -> int:
    return len(PdfReader(BytesIO(data)).pages)


@needs_gs
def test_downsamples_images() -> None:
    original = _photo_pdf(2)

    compacted = compact_bulletin_pdf(original)

    assert _pages(compacted) == 2
    assert len(compacted) < len(original) / 2


@needs_gs
def test_keeps_only_the_pages_classifiers_read() -> None:
    compacted = compact_bulletin_pdf(_photo_pdf(3), max_pages=2)

    assert _pages(compacted) == 2


def test_truncates_without_ghostscript(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pdf_compact.shutil, "which", lambda _name: None)

    compacted = compact_bulletin_pdf(_blank_pdf(14))

    assert _pages(compacted) == 10


def test_keeps_the_original_when_nothing_is_smaller(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pdf_compact.shutil, "which", lambda _name: None)
    original = _blank_pdf(3)

    assert compact_bulletin_pdf(original) is original


def test_keeps_the_original_when_ghostscript_output_is_wrong(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # A tiny but wrong result (one page instead of three) must not be stored.
    monkeypatch.setattr(pdf_compact, "_ghostscript", lambda _data, _pages, **_: _blank_pdf(1))
    original = _photo_pdf(3, px=64)

    assert compact_bulletin_pdf(original) is original


def test_keeps_the_original_when_ghostscript_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(_data: bytes, _pages: int, **_: object) -> bytes:
        raise RuntimeError("gs crashed")

    monkeypatch.setattr(pdf_compact, "_ghostscript", boom)
    original = _photo_pdf(1, px=64)

    assert compact_bulletin_pdf(original) is original


def test_stores_unreadable_bytes_unchanged(caplog: pytest.LogCaptureFixture) -> None:
    data = b"%PDF-1.4 not really"

    with caplog.at_level(logging.WARNING):
        assert compact_bulletin_pdf(data) is data
    assert "unreadable PDF" in caplog.text


def _gs_recording(monkeypatch: pytest.MonkeyPatch, results: list[bytes | None]) -> list[dict]:
    """Make each Ghostscript pass give the next of `results`; returns the passes' options."""
    passes: list[dict] = []
    outcomes = iter(results)

    def fake(_data: bytes, _pages: int, **options: object) -> bytes | None:
        passes.append(options)
        return next(outcomes)

    monkeypatch.setattr(pdf_compact, "_ghostscript", fake)
    return passes


def test_retries_without_converting_colours_when_ghostscript_times_out(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = _photo_pdf(2, px=64)
    smaller = _blank_pdf(2)
    passes = _gs_recording(monkeypatch, [None, smaller])

    assert compact_bulletin_pdf(original) == smaller
    assert passes[1]["options"] == pdf_compact._KEEP_COLOURS
    assert passes[1]["timeout"] > pdf_compact.GHOSTSCRIPT_TIMEOUT_SECONDS


def test_does_not_retry_when_ghostscript_worked(monkeypatch: pytest.MonkeyPatch) -> None:
    passes = _gs_recording(monkeypatch, [_blank_pdf(2)])

    compact_bulletin_pdf(_photo_pdf(2, px=64))

    assert len(passes) == 1


def test_a_copy_over_the_limit_tries_a_lower_resolution(monkeypatch: pytest.MonkeyPatch) -> None:
    original = _photo_pdf(2, px=256)
    first = _blank_pdf(2) + b"\n" * 2000
    second = _blank_pdf(2)
    monkeypatch.setattr(pdf_compact, "MAX_STORED_BULLETIN_BYTES", len(second) + 1000)
    passes = _gs_recording(monkeypatch, [first, second])

    assert compact_bulletin_pdf(original) == second
    assert passes[1]["options"] == pdf_compact._LOW_RESOLUTION


def test_returns_what_it_has_when_nothing_gets_under_the_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # What to do about it is the caller's: compaction only reports the size.
    monkeypatch.setattr(pdf_compact, "MAX_STORED_BULLETIN_BYTES", 10)
    original = _photo_pdf(1, px=64)
    _gs_recording(monkeypatch, [None, None, None])

    assert compact_bulletin_pdf(original) is original


def test_gives_ghostscript_a_pdf_too_large_to_store_that_pypdf_cannot_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    unreadable = b"%PDF-1.4 not really"
    monkeypatch.setattr(pdf_compact, "MAX_STORED_BULLETIN_BYTES", 10)
    readable = _blank_pdf(2)
    _gs_recording(monkeypatch, [readable])

    # Repeated only so that the two blank pages count as smaller.
    assert compact_bulletin_pdf(unreadable * 1000) == readable


@needs_gs
def test_ghostscript_accepts_a_last_page_past_the_end() -> None:
    # An unreadable PDF's page count is unknown, so `max_pages` is passed as it is.
    assert _pages(pdf_compact._ghostscript(_photo_pdf(2, px=64), 10)) == 2


@needs_gs
@pytest.mark.parametrize(
    ("options", "jpeg"),
    [
        (pdf_compact._KEEP_COLOURS, pdf_compact._HIGH_QUALITY_JPEG),
        (pdf_compact._LOW_RESOLUTION, pdf_compact._SMALLER_JPEG),
    ],
)
def test_ghostscript_runs_with_each_fallback(options: tuple[str, ...], jpeg: str) -> None:
    original = _photo_pdf(2)

    compacted = pdf_compact._ghostscript(original, 2, options=options, jpeg=jpeg)

    assert compacted is not None and _pages(compacted) == 2
    assert len(compacted) < len(original) / 2


@needs_gs
def test_low_resolution_is_smaller_than_the_ordinary_copy() -> None:
    ordinary = pdf_compact._ghostscript(_photo_pdf(2), 2)

    low = pdf_compact._ghostscript(
        ordinary, 2, options=pdf_compact._LOW_RESOLUTION, jpeg=pdf_compact._SMALLER_JPEG,
    )

    assert len(low) < len(ordinary)
