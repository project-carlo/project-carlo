"""Is a downloaded bulletin one we already have?

The fetch stage used to answer that from the address: a known address was a
known bulletin. It is not. Discover Mass serves one PDF under a new
`download.php?bulletin=` token on every request (the 2026-09-28 database holds
31 extra rows of a week's Discover Mass bulletin, every one byte-identical to
that week's first), and a site that overwrites `/bulletin.pdf` each week puts
new bulletins at an old address.

So a download is compared by what it is, cheapest test first:

1. **Not modified.** `validators_for` gives the ETag and Last-Modified the
   server sent last time for this address; a 304 answer to them means the
   bulletin stored from there is still current, and nothing is downloaded.
2. **Byte hash** against every bulletin of the parish: the same bytes are the
   same bulletin, whenever and wherever they were seen.
3. **Text fingerprint** against the parish's last few bulletins, for a server
   that rebuilds the file on each request (new bytes, same words). Some sites
   briefly fall back to last week's file, so not just the latest.

The text test is guarded, because many bulletins are scans under a fixed text
layer (a typed cover, ads): on the 2026-09-28 database, 11 runs of different
weeks from 7 parishes had word-for-word identical text, every one with fewer
than 100 words a page, against a median of about 420 for a typed bulletin. So
a PDF gets a fingerprint only when it has enough words a page to be typed
throughout, and a parish whose text has ever repeated across two different
weeks is never matched by text at all.

A duplicate is not stored again. The fetch stage records on the existing row
that the site served it (`last_seen_at`), so the report can tell a site that
is alive but unchanged from one that stopped answering.
"""

from __future__ import annotations

import hashlib
import logging
import re
from collections.abc import Iterable
from dataclasses import dataclass
from io import BytesIO
from typing import Any

from pypdf import PdfReader

from pdf_extract.bulletin_week import bulletin_week
from pdf_extract.pdf_truncate import MAX_BULLETIN_PAGES

LOGGER = logging.getLogger(__name__)

# How many of the parish's most recently fetched bulletins a download's text
# is compared with.
RECENT_BULLETINS = 4

# Below these, the text is too thin to tell one week from the next.
MIN_FINGERPRINT_WORDS = 500
MIN_WORDS_PER_PAGE = 150

_WORD = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class Validators:
    """What the server said identifies the copy it sent, for a conditional GET."""

    etag: str | None = None
    last_modified: str | None = None

    def __bool__(self) -> bool:
        return bool(self.etag or self.last_modified)

    def request_headers(self) -> dict[str, str]:
        headers = {}
        if self.etag:
            headers["If-None-Match"] = self.etag
        if self.last_modified:
            headers["If-Modified-Since"] = self.last_modified
        return headers


@dataclass(frozen=True)
class Duplicate:
    """The stored bulletin a download turned out to be, and how we knew."""

    bulletin: dict[str, Any]
    how: str

    def describe(self) -> str:
        return f"same bulletin as #{self.bulletin['id']} ({self.how})"


def validators_for(source_url: str, stored: Iterable[dict[str, Any]]) -> Duplicate | None:
    """The latest stored bulletin from `source_url` that a 304 would confirm.

    Its `etag` and `last_modified` are what to send; None when no bulletin
    from that address came with either.
    """
    candidates = [
        entry for entry in stored
        if entry.get("source_url") == source_url
        and (entry.get("etag") or entry.get("last_modified"))
    ]
    if not candidates:
        return None
    latest = max(candidates, key=lambda e: (str(e.get("fetched_at") or ""), int(e["id"])))
    return Duplicate(latest, "not modified")


def text_fingerprint(pdf_bytes: bytes) -> str | None:
    """A hash of the words on the pages a classifier reads, or None if too few.

    Words are lowercased letters and digits, so a rebuilt file that lays the
    same text out with other spacing or fonts still matches. The page count
    is part of it, so an extra insert page is a different bulletin.
    """
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        pages = reader.pages[:MAX_BULLETIN_PAGES]
        words = _WORD.findall(" ".join(page.extract_text() or "" for page in pages).lower())
    except Exception:
        LOGGER.debug("No text fingerprint: the PDF could not be read", exc_info=True)
        return None
    if not pages or len(words) < MIN_FINGERPRINT_WORDS:
        return None
    if len(words) < MIN_WORDS_PER_PAGE * len(pages):
        return None
    digest = hashlib.sha256(" ".join(words).encode("utf-8")).hexdigest()
    return f"{len(pages)}:{digest}"


def text_repeats_across_weeks(stored: Iterable[dict[str, Any]]) -> bool:
    """Whether two of these bulletins for different weeks share a fingerprint.

    Then the parish's text layer does not change from week to week, and its
    fingerprint cannot tell one bulletin from the next.
    """
    weeks: dict[str, set] = {}
    for entry in stored:
        fingerprint = entry.get("text_fingerprint")
        if fingerprint:
            weeks.setdefault(fingerprint, set()).add(bulletin_week(entry))
    return any(len(seen) > 1 for seen in weeks.values())


@dataclass(frozen=True)
class Identified:
    """A downloaded PDF's fingerprints, and the stored bulletin it is, if any."""

    content_hash: str
    text_fingerprint: str | None
    duplicate: Duplicate | None


def identify(pdf_bytes: bytes, stored: list[dict[str, Any]]) -> Identified:
    """Fingerprint a download and look for it among `stored` (one parish's bulletins).

    The text is read only when the bytes match nothing: it is the slow part.
    """
    # The hash names the bulletin as published, so it stays the bulletin's
    # identity however the stored copy is compacted.
    content_hash = hashlib.sha256(pdf_bytes).hexdigest()
    for entry in stored:
        if entry.get("content_hash") == content_hash:
            return Identified(
                content_hash, entry.get("text_fingerprint"), Duplicate(entry, "byte hash"),
            )
    fingerprint = text_fingerprint(pdf_bytes)
    if fingerprint is None or text_repeats_across_weeks(stored):
        return Identified(content_hash, fingerprint, None)
    recent = sorted(stored, key=lambda e: (str(e.get("fetched_at") or ""), int(e["id"])))
    for entry in reversed(recent[-RECENT_BULLETINS:]):
        if entry.get("text_fingerprint") == fingerprint:
            return Identified(content_hash, fingerprint, Duplicate(entry, "same text"))
    return Identified(content_hash, fingerprint, None)
