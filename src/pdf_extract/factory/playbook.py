"""What the dispatcher writes in `diocese.md`: lessons, accepted rules and seeding precedents.

Each goes in as one bullet, as the worker wrote it, under its heading. Appending is
idempotent by text, so a dispatcher restarted partway through doesn't add a line twice.

The playbook is the part every map job is given: *Bulletin publishers here*, *Rules
settled* and *New lessons*. `integrate` keeps the first two near `TARGETS`; the sizes are
measured here, for its input and the PR.
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
# The size integrate keeps each section near, in bytes (1 KB = 1,000). A guide for now: a
# gate waits for a full Run's sizes (docs/factory-refactor-plan.md, Phase 3).
TARGETS = {PUBLISHERS: 8_000, RULES: 6_000}
# A section missing from the file goes before the first of these that exists.
_BEFORE = {NEW_LESSONS: (RULES, LOG), PRECEDENTS: (LOG,), RULES: (LOG,)}


def headings(lines: list[str]) -> dict[int, tuple[int, str]]:
    """Each Markdown heading's line: its level and title. A `#` line in a fenced code block
    (an example record's `## Publisher`, a shell comment) isn't one."""
    found, fence = {}, None
    for i, line in enumerate(lines):
        if m := re.match(r"\s*(`{3,}|~{3,})", line):
            if fence is None:
                fence = m.group(1)
            elif m.group(1).startswith(fence):
                fence = None
        elif fence is None and (m := re.fullmatch(r"(#+)\s+(.*?)\s*", line)):
            found[i] = (len(m.group(1)), m.group(2))
    return found


def _span(lines: list[str], heading: str) -> tuple[int, int] | None:
    """The section's lines after its heading, up to the next heading of its level or above."""
    found = headings(lines)
    level, title = len(heading) - len(heading.lstrip("#")), heading.lstrip("#").strip()
    start = next((i for i, h in found.items() if h == (level, title)), None)
    if start is None:
        return None
    end = next((i for i, (lv, _) in found.items() if i > start and lv <= level), len(lines))
    return start + 1, end


def section(path: Path, heading: str) -> str:
    return section_of(path.read_text(encoding="utf-8"), heading)


def section_of(text: str, heading: str) -> str:
    lines = text.splitlines()
    span = _span(lines, heading)
    return "" if span is None else "\n".join(lines[span[0]:span[1]]).strip()


def items(body: str) -> list[str]:
    """A section's bullets, each whole and on one line: a bullet runs on through its
    wrapped and indented lines, up to the next bullet, heading or unindented paragraph."""
    out: list[str] = []
    current: list[str] | None = None
    blank = False
    for line in body.splitlines():
        if line.startswith("- "):
            current = [line[2:]]
            out.append("")
        elif current is None or line.startswith("#") or (blank and not line[:1].isspace()
                                                          and line.strip()):
            current = None
        elif line.strip():
            current.append(line)
        blank = not line.strip()
        if current is not None:
            out[-1] = " ".join(" ".join(current).split())
    return out


def rule_key(text: str) -> str:
    """A rule as compared with its copy in a handoff: wrapping and emphasis don't count."""
    return " ".join(text.replace("*", "").split())


def size(text: str, heading: str) -> int:
    return len(section_of(text, heading).encode("utf-8"))


def sizes(text: str) -> dict[str, int]:
    """The playbook in `text` (a `diocese.md`): its two kept sections' sizes in bytes, and
    how many lessons wait in *New lessons*."""
    return {"publishers": size(text, PUBLISHERS), "rules": size(text, RULES),
            "lessons": len([b for b in section_of(text, NEW_LESSONS).splitlines()
                            if b.startswith("- ")])}


def kb(n: int) -> str:
    return f"{n / 1000:.1f} KB"


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
