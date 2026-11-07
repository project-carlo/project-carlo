"""Shrink bulletin PDFs before they are stored.

Bulletins are mostly photos and scanned pages, several MB each, and every week
adds one per parish, so they are nearly all of the bucket. Only the first
`MAX_BULLETIN_PAGES` pages, or a parish's own limit, are ever read (see
`pdf_truncate.max_pages_for`), so `fetch` stores just those, with
Ghostscript downsampling images to 150 dpi. Text and
vector art are left as they are.

Images are re-encoded as JPEG, and the stored copy is what classifiers read
from then on, so the JPEG quality is Ghostscript's high-quality setting (no
chroma subsampling) rather than `/ebook`'s default, which blurs small print
in scanned pages.

Nearly all of Ghostscript's time goes on converting images to sRGB, not on the
size of the file: a 39 MB bulletin of colour-managed scans takes minutes while
most take seconds. When that conversion times out or fails, a second pass
leaves colours as they are, which takes seconds on the same files at the cost
of some size (CMYK images stay four-channel).

A bulletin is only stored if it ends up within `MAX_STORED_BULLETIN_BYTES`.
Compaction fails open below that limit (when it fails, or would not make the
file smaller, the bytes as downloaded are the result) and above it tries a lower
resolution rather than give up on the week's bulletin. `fetch` stores nothing
when even that is over the limit, and reports the parish as `too_large`.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import tempfile
import threading
import time
from collections.abc import Callable
from io import BytesIO
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader, PdfWriter

from pdf_extract.pdf_truncate import MAX_BULLETIN_PAGES

LOGGER = logging.getLogger(__name__)

# The most a bulletin may take up in the bucket. Over twice the largest bulletin
# Ghostscript produced in 1,750 compactions (9.5 MB, October 2026).
MAX_STORED_BULLETIN_BYTES = 20_000_000

GHOSTSCRIPT_TIMEOUT_SECONDS = 180
# For the passes that skip colour conversion, which only run when a bulletin
# would otherwise be stored uncompacted or not at all.
GHOSTSCRIPT_RETRY_TIMEOUT_SECONDS = 600
_HIGH_QUALITY_JPEG = "<< /QFactor 0.4 /Blend 1 /HSamples [1 1 1 1] /VSamples [1 1 1 1] >>"
# Ghostscript's own default, which subsamples chroma.
_SMALLER_JPEG = "<< /QFactor 0.76 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >>"
_KEEP_COLOURS = ("-sColorConversionStrategy=LeaveColorUnchanged",)
_LOW_RESOLUTION = (
    *_KEEP_COLOURS,
    "-dColorImageResolution=110", "-dColorImageDownsampleThreshold=1.0",
    "-dGrayImageResolution=110", "-dGrayImageDownsampleThreshold=1.0",
)
# PDFium is not thread-safe, and `fetch` compacts from several workers.
_PDFIUM_LOCK = threading.Lock()


def _page_count(data: bytes) -> int:
    return len(PdfReader(BytesIO(data)).pages)


def _pdfium_page_count(data: bytes) -> int:
    with _PDFIUM_LOCK, pdfium.PdfDocument(data) as document:
        return len(document)


def _truncate(data: bytes, pages: int) -> bytes:
    reader = PdfReader(BytesIO(data))
    writer = PdfWriter()
    for page in reader.pages[:pages]:
        writer.add_page(page)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def _ghostscript(
    data: bytes,
    pages: int,
    *,
    options: tuple[str, ...] = (),
    jpeg: str = _HIGH_QUALITY_JPEG,
    timeout: int = GHOSTSCRIPT_TIMEOUT_SECONDS,
) -> bytes | None:
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
                    *options,
                    "-dFirstPage=1", f"-dLastPage={pages}",
                    f"-sOutputFile={target}",
                    "-c",
                    f"<< /ColorACSImageDict {jpeg}"
                    f" /GrayACSImageDict {jpeg} >> setdistillerparams",
                    "-f", str(source),
                ],
                check=True,
                capture_output=True,
                timeout=timeout,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            stderr = getattr(exc, "stderr", None) or b""
            LOGGER.warning(
                "Ghostscript failed: %s %s", exc, stderr.decode("utf-8", "replace")[-500:],
            )
            return None
        return target.read_bytes() if target.is_file() else None


# A bulletin posted as an image is stored as a one-page PDF at this resolution
# (a 2100-pixel-wide spread becomes a 14-inch page).
IMAGE_PDF_DPI = 150.0
PDF_MAGIC = b"%PDF-"


def image_as_pdf(data: bytes) -> bytes | None:
    """An image bulletin (St. Mary, Waymart posts each week's as one JPEG) as a
    one-page PDF, or None if `data` is not an image.

    The PDF carries a fixed date, so the same image always makes the same PDF
    and a re-fetched issue is recognised as one already stored.
    """
    try:
        image = Image.open(BytesIO(data))
        image.load()
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        return None
    out = BytesIO()
    epoch = time.gmtime(0)
    image.convert("RGB").save(
        out, format="PDF", resolution=IMAGE_PDF_DPI, creationDate=epoch, modDate=epoch,
    )
    return out.getvalue()


def as_bulletin_pdf(data: bytes) -> bytes:
    """`data` as a PDF: a PDF as it is, an image wrapped in one, else unchanged."""
    if data.startswith(PDF_MAGIC):
        return data
    return image_as_pdf(data) or data


def compact_bulletin_pdf(data: bytes, *, max_pages: int = MAX_BULLETIN_PAGES) -> bytes:
    """The smallest faithful copy of a bulletin's first `max_pages` pages.

    Tries Ghostscript (again without converting colours, if that fails), then
    (for a long bulletin) plain truncation, and keeps whichever is smallest
    among those that open with the expected page count, including the original.
    What is still over `MAX_STORED_BULLETIN_BYTES` gets a lower resolution.

    The result can still be over the limit: the caller decides what to do then.
    """
    try:
        pages = _page_count(data)
    except Exception:
        if len(data) <= MAX_STORED_BULLETIN_BYTES:
            LOGGER.warning("Not compacting an unreadable PDF (%d bytes)", len(data), exc_info=True)
            return data
        # pypdf gives up on very large streams that Ghostscript reads, and this
        # one is not stored as it is, so there is nothing to lose by trying. The
        # page count still has to come from somewhere other than Ghostscript:
        # it can recover part of a damaged file and report success.
        LOGGER.warning("Compacting a PDF pypdf cannot read (%d bytes)", len(data), exc_info=True)
        try:
            pages = _pdfium_page_count(data)
        except Exception:
            LOGGER.warning("Not compacting an unreadable PDF (%d bytes)", len(data), exc_info=True)
            return data
    keep = min(pages, max_pages)

    best = data

    def attempt(name: str, make: Callable[[], bytes | None]) -> bool:
        """Whether `make` gave a complete copy, which is kept if it is the smallest yet."""
        nonlocal best
        try:
            candidate = make()
            if candidate is None:
                return False
            count = _page_count(candidate)
        except Exception:
            LOGGER.warning("Compacting with %s failed", name, exc_info=True)
            return False
        if count != keep:
            LOGGER.warning("Discarding %s output: expected %d pages", name, keep)
            return False
        if len(candidate) < len(best):
            best = candidate
        return True

    ghostscript_worked = attempt(
        "ghostscript", lambda: _ghostscript(data, keep),
    ) or attempt("ghostscript keeping colours", lambda: _ghostscript(
        data, keep, options=_KEEP_COLOURS, timeout=GHOSTSCRIPT_RETRY_TIMEOUT_SECONDS,
    ))
    if pages > keep:
        attempt("truncate", lambda: _truncate(data, keep))
    # When Ghostscript failed twice on these same bytes a third pass would most
    # likely fail too, and could take as long again, every week.
    if len(best) > MAX_STORED_BULLETIN_BYTES and (ghostscript_worked or best is not data):
        attempt("ghostscript at low resolution", lambda: _ghostscript(
            best, keep, options=_LOW_RESOLUTION, jpeg=_SMALLER_JPEG,
            timeout=GHOSTSCRIPT_RETRY_TIMEOUT_SECONDS,
        ))

    if best is not data:
        LOGGER.info(
            "Compacted bulletin %.1f MB -> %.1f MB (%d of %d pages)",
            len(data) / 1e6, len(best) / 1e6, keep, pages,
        )
    return best
