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

Every repeat in that database was byte-identical, so nothing looser (such as
comparing the PDFs' text) is needed yet.

A duplicate is not stored again. The fetch stage records on the existing row
that the site served it (`last_seen_at`), so the report can tell a site that
is alive but unchanged from one that stopped answering.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any


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


def bulletin_hash(pdf_bytes: bytes) -> str:
    """A bulletin's identity: the SHA-256 of the PDF as downloaded.

    It names the bulletin as published, so it stays the same however the
    stored copy is compacted.
    """
    return hashlib.sha256(pdf_bytes).hexdigest()


def find_duplicate(content_hash: str, stored: Iterable[dict[str, Any]]) -> Duplicate | None:
    """The bulletin among `stored` (one parish's) with these bytes, if any."""
    for entry in stored:
        if entry.get("content_hash") == content_hash:
            return Duplicate(entry, "byte hash")
    return None
