"""Parsing helpers for the loosely formatted times and dates the LLM returns.

Extracted events carry human-readable strings ("5:30pm", "August 5, 2026")
rather than normalised values. Both the DB loader and the weekly-recurrence
detector need the same interpretation of those strings, so the parsers live
here instead of in either caller.
"""

from __future__ import annotations

import re
from datetime import datetime

_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_LOOSE_DATE_FORMATS = ("%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%m/%d/%y")


def time_to_minutes(s: str | None) -> int | None:
    """Parse time string (h:MM AM/PM, a.m./p.m., etc.) to minutes since midnight.

    Returns None for null/empty. Handles: 8:00 AM, 5:30pm, 8:00 a.m., midnight, noon.
    """
    if s is None or not isinstance(s, str):
        return None
    raw = s.strip()
    if not raw:
        return None

    # Normalize a.m. / p.m. to AM / PM
    raw = re.sub(r"a\.m\.?(?=\s|$)", "AM", raw, flags=re.I)
    raw = re.sub(r"p\.m\.?(?=\s|$)", "PM", raw, flags=re.I)

    if re.match(r"^midnight$", raw, re.I):
        return 0
    if re.match(r"^noon$", raw, re.I):
        return 720

    m = re.match(r"^(\d{1,2}):(\d{2})\s*(AM|PM)$", raw, re.I)
    if m:
        h = int(m[1])
        mins = int(m[2])
        ampm = m[3].upper()
        if ampm == "PM" and h != 12:
            h += 12
        elif ampm == "AM" and h == 12:
            h = 0
        return h * 60 + mins

    m = re.match(r"^(\d{1,2})\s*(AM|PM)$", raw, re.I)
    if m:
        h = int(m[1])
        ampm = m[2].upper()
        if ampm == "PM" and h != 12:
            h += 12
        elif ampm == "AM" and h == 12:
            h = 0
        return h * 60

    m = re.match(r"^(\d{1,2}):(\d{2})$", raw)
    if m:
        h, mins = int(m[1]), int(m[2])
        if 0 <= h <= 23 and 0 <= mins <= 59:
            return h * 60 + mins

    m = re.match(r"^(\d{2})(\d{2})$", raw)
    if m:
        h, mins = int(m[1]), int(m[2])
        if 0 <= h <= 23 and 0 <= mins <= 59:
            return h * 60 + mins

    return None


def normalize_event_date(value: str | None) -> str | None:
    """Normalize date strings to YYYY-MM-DD for specific-date events."""
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if not raw:
        return None

    # Keep canonical ISO dates as-is after validating.
    if _ISO_DATE_RE.match(raw):
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return None

    for fmt in _LOOSE_DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue

    return None
