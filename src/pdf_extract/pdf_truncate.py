"""Cap bulletin PDFs at a maximum page count before sending to Gemini."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from pypdf import PdfReader, PdfWriter

from pdf_extract.paths import DATA_DIR

LOGGER = logging.getLogger(__name__)

MAX_BULLETIN_PAGES = 10

# Parishes whose bulletin prints a schedule past page MAX_BULLETIN_PAGES, with
# the limit to read them to instead. Every extra page is stored and read every
# week, so a parish is listed here only when its schedule is known to be cut.
PAGE_LIMITS_CSV_PATH = DATA_DIR / "bulletin_page_limits.csv"


def read_page_limits(path: Path | None = None) -> dict[str, int]:
    """Per-parish page limits from data/bulletin_page_limits.csv, by parish slug."""
    path = PAGE_LIMITS_CSV_PATH if path is None else path
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as fh:
        return {
            row["parish_slug"].strip(): int(row["max_pages"])
            for row in csv.DictReader(fh)
            if (row.get("parish_slug") or "").strip()
        }


def max_pages_for(parish_slug: str) -> int:
    """How many of a parish's bulletin pages are stored and read."""
    return read_page_limits().get(parish_slug, MAX_BULLETIN_PAGES)


def _truncated_path(pdf_path: Path) -> Path:
    return pdf_path.with_name(f"{pdf_path.stem}-truncated{pdf_path.suffix}")


def _page_count(pdf_path: Path) -> int:
    reader = PdfReader(str(pdf_path))
    return len(reader.pages)


def ensure_truncated_pdf(pdf_path: Path, *, max_pages: int = MAX_BULLETIN_PAGES) -> Path:
    """Return a path to a PDF with at most ``max_pages`` pages.

    If ``pdf_path`` has ``<= max_pages`` pages, returns ``pdf_path`` unchanged.
    Otherwise writes/returns ``<stem>-truncated.pdf`` next to the original
    containing only the first ``max_pages`` pages. Re-uses an existing
    truncated file whose page count already matches ``max_pages``.
    """
    original_pages = _page_count(pdf_path)
    if original_pages <= max_pages:
        return pdf_path

    target = _truncated_path(pdf_path)
    if target.exists():
        try:
            if _page_count(target) == max_pages:
                return target
        except Exception:
            LOGGER.warning(
                "Existing truncated PDF unreadable, regenerating: %s", target, exc_info=True,
            )

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    for page in reader.pages[:max_pages]:
        writer.add_page(page)
    with target.open("wb") as fh:
        writer.write(fh)

    LOGGER.info(
        "Truncated bulletin from %d to %d pages: %s -> %s",
        original_pages, max_pages, pdf_path, target,
    )
    return target
