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
    monkeypatch.setattr(pdf_compact, "_ghostscript", lambda _data, _pages: _blank_pdf(1))
    original = _photo_pdf(3, px=64)

    assert compact_bulletin_pdf(original) is original


def test_keeps_the_original_when_ghostscript_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(_data: bytes, _pages: int) -> bytes:
        raise RuntimeError("gs crashed")

    monkeypatch.setattr(pdf_compact, "_ghostscript", boom)
    original = _photo_pdf(1, px=64)

    assert compact_bulletin_pdf(original) is original


def test_stores_unreadable_bytes_unchanged(caplog: pytest.LogCaptureFixture) -> None:
    data = b"%PDF-1.4 not really"

    with caplog.at_level(logging.WARNING):
        assert compact_bulletin_pdf(data) is data
    assert "unreadable PDF" in caplog.text
