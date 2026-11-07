"""Fetch gaps: parishes whose bulletin is published, but which `fetch` can't collect yet.

A parish record's optional `fetch_gap` names the pattern (`kind`, a slug shared by every
parish with the same problem) and what fails. `pnpm diocese gaps` (`report.gaps`) lists
them across every diocese, grouped by kind, so a collector can be written once for all the
parishes that need it. When a fix lands, its parishes are rechecked with `fetch:check` and
the field is removed (`"fetch_gap": null` in a `diocese write` patch).
"""

from __future__ import annotations

import datetime as dt
import re
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

FIELDS = {"kind", "url", "seen", "note"}
_KIND_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def errors(gap: Any) -> list[str]:
    """What is wrong with one `fetch_gap`, without trusting a hand-edited record's types."""
    if not isinstance(gap, Mapping):
        return ["fetch_gap must be an object with kind, seen, note and an optional url"]
    out = [f"fetch_gap: unknown field {f!r}" for f in gap if f not in FIELDS]
    kind = gap.get("kind")
    if not isinstance(kind, str) or not _KIND_RE.match(kind):
        out.append("fetch_gap: kind must be a slug like 'solutio-file-403'; reuse one that "
                   "`pnpm diocese gaps` already lists when the problem is the same")
    if not isinstance(gap.get("note"), str) or not gap["note"].strip():
        out.append("fetch_gap: note is required: what fails, and where the bulletin is")
    seen = gap.get("seen")
    try:
        if not isinstance(seen, str) or len(seen) != 10:
            raise ValueError
        dt.date.fromisoformat(seen)
    except ValueError:
        out.append("fetch_gap: seen must be a date like 2026-09-06")
    url = gap.get("url")
    if url is not None:
        try:
            parts = urlsplit(url) if isinstance(url, str) else None
            valid = bool(parts and parts.scheme in ("http", "https") and parts.netloc)
        except ValueError:
            valid = False
        if not valid:
            out.append("fetch_gap: url must start with http:// or https://")
    return out

