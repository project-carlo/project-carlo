"""What the dispatcher writes in `diocese.md`: lessons, accepted rules and seeding precedents.

Each goes in as one bullet, as the worker wrote it, under its heading. Appending is
idempotent by text, so a dispatcher restarted partway through doesn't add a line twice.
"""

from __future__ import annotations

import re
from pathlib import Path

NEW_LESSONS = "## New lessons"
PUBLISHERS = "### Bulletin publishers here"
RULES = "## Rules settled for this diocese"
PRECEDENTS = "## Seeding precedents"
LOG = "## Log"

_INTROS = {
    NEW_LESSONS: "Lessons map jobs reported, as written, for the next `integrate` to merge into "
                 "*Bulletin publishers here* and *Rules settled*. Every map job reads them.",
    PRECEDENTS: "Seed questions `seed-review` settled that no rule covered: the situation, the "
                "choice and the parishes. Later reviews in this diocese follow them; only the "
                "owner turns one into a rule.",
}
# A section missing from the file goes before the first of these that exists.
_BEFORE = {NEW_LESSONS: (RULES, LOG), PRECEDENTS: (LOG,), RULES: (LOG,)}


def _level(line: str) -> int:
    m = re.match(r"(#+)\s", line)
    return len(m.group(1)) if m else 0


def _span(lines: list[str], heading: str) -> tuple[int, int] | None:
    """The section's lines after its heading, up to the next heading of its level or above."""
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        return None
    level = _level(heading)
    end = next((i for i in range(start + 1, len(lines))
                if 0 < _level(lines[i]) <= level), len(lines))
    return start + 1, end


def section(path: Path, heading: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    span = _span(lines, heading)
    return "" if span is None else "\n".join(lines[span[0]:span[1]]).strip()


def bullets(path: Path, heading: str) -> list[str]:
    return [line[2:].strip() for line in section(path, heading).splitlines()
            if line.startswith("- ")]


def append(path: Path, heading: str, items: list[str]) -> list[str]:
    """Add each item as a bullet under `heading`, creating the section; returns those added."""
    lines = path.read_text(encoding="utf-8").splitlines()
    span = _span(lines, heading)
    if span is None:
        at = next((i for h in _BEFORE.get(heading, ()) for i, line in enumerate(lines)
                   if line.strip() == h), len(lines))
        block = [heading, ""] + ([_INTROS[heading], ""] if heading in _INTROS else [])
        if at and lines[at - 1].strip():
            block.insert(0, "")
        lines[at:at] = block + [""]
        span = _span(lines, heading)
        assert span is not None
    present = {b.strip() for b in bullets_in(lines[span[0]:span[1]])}
    added = [" ".join(i.split()) for i in items if " ".join(i.split()) not in present]
    added = list(dict.fromkeys(added))
    if not added:
        return []
    end = span[1]
    while end > span[0] and not lines[end - 1].strip():
        end -= 1
    new = [f"- {item}" for item in added]
    if end > span[0] and not lines[end - 1].startswith(("- ", "  ")):
        new.insert(0, "")  # after the section's intro paragraph
    lines[end:end] = new
    text = "\n".join(lines).rstrip("\n") + "\n"
    path.write_text(text, encoding="utf-8")
    return added


def bullets_in(lines: list[str]) -> list[str]:
    return [line[2:] for line in lines if line.startswith("- ")]
