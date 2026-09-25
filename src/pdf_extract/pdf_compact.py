"""Shrink bulletin PDFs before they are stored.

Bulletins are mostly photos and scanned pages, several MB each, and every week
adds one per parish, so they are nearly all of the bucket. Only the first
`MAX_BULLETIN_PAGES` pages are ever read (see `pdf_truncate`), so `fetch`
stores just those, with Ghostscript downsampling images to 150 dpi. Text and
vector art are left as they are.

Compaction only saves space: whenever it fails, or would not make the file
smaller, the bytes as downloaded are stored instead.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_extract.pdf_truncate import MAX_BULLETIN_PAGES

LOGGER = logging.getLogger(__name__)

GHOSTSCRIPT_TIMEOUT_SECONDS = 180


def _page_count(data: bytes) -> int:
    return len(PdfReader(BytesIO(data)).pages)


def _truncate(data: bytes, pages: int) -> bytes:
    reader = PdfReader(BytesIO(data))
    writer = PdfWriter()
    for page in reader.pages[:pages]:
        writer.add_page(page)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def _ghostscript(data: bytes, pages: int) -> bytes | None:
    """The first `pages` pages rewritten by Ghostscript, or None if it is unavailable or fails."""
    gs = shutil.which("gs")
    if gs is None:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "in.pdf"
        target = Path(tmp) / "out.pdf"
        source.write_bytes(data)
        try:
            subprocess.run(
                [
                    gs, "-q", "-dSAFER", "-dBATCH", "-dNOPAUSE",
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.5",
                    # 150 dpi colour and greyscale images, 300 dpi monochrome.
                    "-dPDFSETTINGS=/ebook",
                    "-dDetectDuplicateImages=true",
                    "-dFirstPage=1", f"-dLastPage={pages}",
                    f"-sOutputFile={target}",
                    str(source),
                ],
                check=True,
                capture_output=True,
                timeout=GHOSTSCRIPT_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            stderr = getattr(exc, "stderr", None) or b""
            LOGGER.warning(
                "Ghostscript failed: %s %s", exc, stderr.decode("utf-8", "replace")[-500:],
            )
            return None
        return target.read_bytes() if target.is_file() else None


def compact_bulletin_pdf(data: bytes, *, max_pages: int = MAX_BULLETIN_PAGES) -> bytes:
    """The smallest faithful copy of a bulletin's first `max_pages` pages.

    Tries Ghostscript, then (for a long bulletin) plain truncation, and keeps
    whichever is smallest among those that open with the expected page count,
    including the original.
    """
    try:
        pages = _page_count(data)
    except Exception:
        LOGGER.warning("Not compacting an unreadable PDF (%d bytes)", len(data), exc_info=True)
        return data
    keep = min(pages, max_pages)

    best = data
    for name, make in (
        ("ghostscript", lambda: _ghostscript(data, keep)),
        ("truncate", lambda: _truncate(data, keep) if pages > keep else None),
    ):
        try:
            candidate = make()
            if candidate is None or len(candidate) >= len(best):
                continue
            if _page_count(candidate) != keep:
                LOGGER.warning("Discarding %s output: expected %d pages", name, keep)
                continue
        except Exception:
            LOGGER.warning("Compacting with %s failed", name, exc_info=True)
            continue
        best = candidate

    if best is not data:
        LOGGER.info(
            "Compacted bulletin %.1f MB -> %.1f MB (%d of %d pages)",
            len(data) / 1e6, len(best) / 1e6, keep, pages,
        )
    return best
