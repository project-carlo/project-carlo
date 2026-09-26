"""Text-extractor protocol for the text → LLM classifier stacks.

A text extractor turns a bulletin PDF into the plain text an LLM reads in
place of the PDF. It never calls an LLM itself. Its output is one string for
the whole document, with each page introduced by a marker line produced by
`page_header()`, so the LLM can still report the page an event came from.
Anything else (layout hints, coordinates, table markup) is up to the extractor.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TextExtractor(Protocol):
    name: str
    """Stable identifier, e.g. "pymupdf-layout"."""

    version: str
    """Bump whenever the text it produces could change; it is part of the
    classifier's cache key."""

    def extract_text(self, pdf_bytes: bytes) -> str:
        """Return the document's text, pages separated by `page_header()` lines.

        Must be safe to call from several threads at once (the runner extracts
        bulletins concurrently); guard any shared, non-thread-safe state.
        """
        ...


def page_header(page_number: int) -> str:
    """The marker line that starts page `page_number` (1-indexed)."""
    return f"===== Page {page_number} ====="
