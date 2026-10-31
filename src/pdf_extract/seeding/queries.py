"""What a seeding agent reads: a parish's bulletins, their PDFs, and extract mode's history.

Everything here reads the local database (`pnpm data:pull`) and the blob store,
as the labeler does, and nothing calls a model.
"""

from __future__ import annotations

import io
import re
import sqlite3
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

import pypdfium2 as pdfium
from pypdf import PdfReader

from pdf_extract.blobstore import CachedBlobStore, bulletin_pdf_key, get_store
from pdf_extract.bulletin_week import bulletin_week
from pdf_extract.labeling.labels import (
    DAYS,
    WEEKS_OF_MONTH,
    is_valid_hash,
)
from pdf_extract.schedule.store import normalize_as_of
from pdf_extract.seeding.checks import COVERED_DAYS, covered_weeks
from pdf_extract.seeding.files import (
    SEEDS_DIR,
    WORK_DIR,
)
from pdf_extract.storage import (
    list_churches,
    load_events,
    read_bulletin_pdf,
)
from pdf_extract.timeparse import time_to_minutes

# Shortest hash prefix a command accepts for a bulletin.
MIN_REF_CHARS = 6
# Fewer characters than this on a page: it is only an image (`seed text`).
MIN_PAGE_TEXT_CHARS = 40
# How many bulletins `seed history` shows, and `seed diff` compares when the
# blob store can't say which PDFs it holds.
HISTORY_BULLETINS = 4
# `seed brief` lists recent history up to this many distinct events, else points to it.
BRIEF_HISTORY_ROWS = 40


class SeedError(ValueError):
    """Bad input to a seed command: the message says what to fix."""


# ── Where drafts go ──────────────────────────────────────────────────────────
@dataclass
class SeedContext:
    """Where a command reads and writes seed files: `data/seeds/`, or a test's folder."""

    seeds_dir: Path = SEEDS_DIR


# ── Parishes and bulletins ──────────────────────────────────────────────────
def parish_row(conn: sqlite3.Connection, parish_slug: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT id, slug, name, homepage_url FROM parish WHERE slug = ?", (parish_slug,),
    ).fetchone()
    if row is None:
        raise SeedError(f"Parish not found: {parish_slug} (is it in data/parishes.csv?)")
    return row


def parish_bulletins(
    conn: sqlite3.Connection, parish_slug: str,
) -> list[dict[str, Any]]:
    """The parish's stored bulletins, newest fetched first.

    `duplicate_of` names the newer row with the same PDF, when one exists (a
    site that served one PDF under several addresses before fetch compared
    downloads by their bytes).
    """
    parish = parish_row(conn, parish_slug)
    rows = conn.execute(
        """SELECT id, content_hash, source_url, fetched_at, published_date, processed_at,
                  COALESCE(wrong_bulletin, 0) AS wrong_bulletin
           FROM bulletin WHERE parish_id = ? AND content_hash IS NOT NULL
           ORDER BY fetched_at DESC, id DESC""",
        (parish["id"],),
    ).fetchall()
    out: list[dict[str, Any]] = []
    first: dict[str, str] = {}
    for row in rows:
        if not is_valid_hash(row["content_hash"]):
            continue
        item = dict(row)
        item["short"] = row["content_hash"][:12]
        item["wrong_bulletin"] = bool(row["wrong_bulletin"])
        item["duplicate_of"] = first.get(row["content_hash"])
        first.setdefault(row["content_hash"], item["short"])
        out.append(item)
    return out


def resolve_bulletin(
    conn: sqlite3.Connection, parish_slug: str, ref: str,
) -> dict[str, Any]:
    """The bulletin `ref` names: `latest`, or a prefix of its content hash."""
    bulletins = [b for b in parish_bulletins(conn, parish_slug)
                 if b["duplicate_of"] is None]
    if not bulletins:
        raise SeedError(f"{parish_slug} has no stored bulletin")
    if ref == "latest":
        return bulletins[0]
    ref = ref.strip().lower().removesuffix("…")
    if len(ref) < MIN_REF_CHARS or any(ch not in "0123456789abcdef" for ch in ref):
        raise SeedError(
            f"Name a bulletin by `latest` or at least {MIN_REF_CHARS} hex characters of its "
            f"hash (see `pnpm seed bulletins {parish_slug}`), not {ref!r}"
        )
    matches = [b for b in bulletins if b["content_hash"].startswith(ref)]
    if not matches:
        raise SeedError(f"{parish_slug} has no bulletin {ref}")
    if len(matches) > 1:
        raise SeedError(f"{ref} names {len(matches)} bulletins of {parish_slug}; give more")
    return matches[0]


def bulletin_pdf(parish_slug: str, content_hash: str) -> bytes:
    """The stored compacted PDF, cut to the pages the pipeline reads, so pages match."""
    if not pdf_stored(parish_slug, content_hash):
        raise SeedError(
            f"The PDF of {parish_slug}/{content_hash[:12]} is no longer stored: its history "
            "can still be cited, but it can't be read"
        )
    return _read_pdf(parish_slug, content_hash)


def _read_pdf(parish_slug: str, content_hash: str) -> bytes:
    data = read_bulletin_pdf(parish_slug, content_hash)
    if data is None:
        raise SeedError(
            f"The PDF of {parish_slug}/{content_hash[:12]} is not in the blob store "
            "(are the R2 read keys set?)"
        )
    return data


def page_count(pdf: bytes) -> int:
    return len(PdfReader(io.BytesIO(pdf)).pages)


def pdf_stored(parish_slug: str, content_hash: str) -> bool:
    """Whether the blob store still holds the bulletin's PDF (old ones may be pruned)."""
    try:
        return get_store().exists(bulletin_pdf_key(parish_slug, content_hash))
    except Exception:  # an unreachable store: let reading the PDF say why
        return True


def stored_pdfs(parish_slug: str) -> set[str] | None:
    """The content hashes of the parish's bulletins whose PDF the blob store holds.

    One listing of the parish's folder rather than a lookup per bulletin (each a
    request to R2). A PDF pruned from R2 may still be in the local cache, where
    reading it works, so both are listed. None when the store can't be listed.
    """
    key = bulletin_pdf_key(parish_slug, "")
    prefix = key[:key.rindex("/") + 1]
    store = get_store()
    try:
        keys = set(store.list(prefix))
        if isinstance(store, CachedBlobStore) and store.remote is not None:
            keys |= set(store.local.list(prefix))
    except Exception:  # an unreachable store: let reading the PDF say why
        return None
    return {k[len(prefix):-len(".pdf")] for k in keys if k.endswith(".pdf")}


def list_bulletins(
    conn: sqlite3.Connection, parish_slug: str, *, limit: int = 8,
) -> dict[str, Any]:
    """`seed bulletins`: the newest `limit` bulletins with their page counts.

    `stored` is false for a bulletin whose PDF the blob store no longer holds:
    extract mode's history of it can still be cited, but it can't be read.
    """
    bulletins = parish_bulletins(conn, parish_slug)
    shown = bulletins[:limit] if limit > 0 else bulletins
    stored = stored_pdfs(parish_slug) if shown else set()
    for b in shown:
        b["pages"] = None
        b["stored"] = stored is None or b["content_hash"] in stored
        if not b["stored"]:
            continue
        try:
            b["pages"] = page_count(_read_pdf(parish_slug, b["content_hash"]))
        except Exception:  # unreadable: say so, don't stop
            pass
    return {
        "parish": parish_slug,
        "bulletins": [
            {k: b.get(k) for k in (
                "short", "content_hash", "fetched_at", "published_date", "pages", "stored",
                "wrong_bulletin", "duplicate_of", "source_url",
            )}
            for b in shown
        ],
        "not_shown": len(bulletins) - len(shown),
    }


def export_pdf(
    conn: sqlite3.Connection, parish_slug: str, ref: str, *,
    work_dir: Path = WORK_DIR,
) -> dict[str, Any]:
    """`seed pdf`: write the stored PDF the pipeline reads to a local file."""
    bulletin = resolve_bulletin(conn, parish_slug, ref)
    data = bulletin_pdf(parish_slug, bulletin["content_hash"])
    path = work_dir / parish_slug / f"{bulletin['short']}.pdf"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {
        "parish": parish_slug,
        "bulletin": bulletin["content_hash"],
        "fetched_at": bulletin["fetched_at"],
        "pages": page_count(data),
        "path": path.as_posix(),
    }


def render_pages(
    conn: sqlite3.Connection, parish_slug: str, ref: str, *,
    page: int | None = None, dpi: int = 150,
    work_dir: Path = WORK_DIR,
) -> dict[str, Any]:
    """`seed pages`: render one page, or all, to PNGs for a closer look."""
    if not 36 <= dpi <= 600:
        raise SeedError("--dpi must be between 36 and 600")
    bulletin = resolve_bulletin(conn, parish_slug, ref)
    data = bulletin_pdf(parish_slug, bulletin["content_hash"])
    out_dir = work_dir / parish_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = pdfium.PdfDocument(data)
    try:
        total = len(pdf)
        if page is not None and not 1 <= page <= total:
            raise SeedError(f"The bulletin has pages 1 to {total}")
        numbers = [page] if page is not None else list(range(1, total + 1))
        paths = []
        for number in numbers:
            pdf_page = pdf[number - 1]
            try:
                image = pdf_page.render(scale=dpi / 72).to_pil()
            finally:
                pdf_page.close()
            path = out_dir / f"{bulletin['short']}-p{number}-{dpi}dpi.png"
            image.save(path, format="PNG")
            paths.append(path.as_posix())
    finally:
        pdf.close()
    return {"parish": parish_slug, "bulletin": bulletin["content_hash"], "pages": total,
            "paths": paths}


def page_texts(
    conn: sqlite3.Connection, parish_slug: str, ref: str, *,
    page: int | None = None,
) -> dict[str, Any]:
    """`seed text`: each page's text layer, a cheap read of a bulletin.

    A page with too little text (`image_only`) is only an image: render it
    with `seed pages` to read it.
    """
    bulletin = resolve_bulletin(conn, parish_slug, ref)
    total, pages = _pdf_texts(bulletin_pdf(parish_slug, bulletin["content_hash"]), page)
    return {"parish": parish_slug, "bulletin": bulletin["content_hash"],
            "fetched_at": bulletin["fetched_at"], "pages": total, "texts": pages}


def _pdf_texts(data: bytes, page: int | None = None) -> tuple[int, list[dict[str, Any]]]:
    """The PDF's page count, and the text layer of one page or all."""
    pdf = pdfium.PdfDocument(data)
    try:
        total = len(pdf)
        if page is not None and not 1 <= page <= total:
            raise SeedError(f"The bulletin has pages 1 to {total}")
        numbers = [page] if page is not None else list(range(1, total + 1))
        pages = []
        for number in numbers:
            pdf_page = pdf[number - 1]
            try:
                textpage = pdf_page.get_textpage()
                try:
                    text = textpage.get_text_range().replace("\r\n", "\n").strip()
                finally:
                    textpage.close()
            finally:
                pdf_page.close()
            pages.append({"page": number, "text": text,
                          "image_only": len(text) < MIN_PAGE_TEXT_CHARS})
    finally:
        pdf.close()
    return total, pages


# ── Searching bulletins ─────────────────────────────────────────────────────
# `seed grep`'s pattern when given none: the words schedule slots and their
# changes are printed with.
SCHEDULE_PATTERN = (
    r"\bmass(es)?\b|\bvigil\b|confess|reconcil|penance|adoration|exposition|holy hour"
    r"|benediction|blessed sacrament|cancel|suspend|communion service"
    r"|first (friday|saturday)"
)


def _hunks(lines: list[str], hits: list[int]) -> list[list[dict[str, Any]]]:
    """Each matching line with a line of context either side, overlapping runs merged."""
    hit = set(hits)
    hunks: list[list[dict[str, Any]]] = []
    end = -1
    for i in hits:
        lo, hi = max(0, i - 1), min(len(lines) - 1, i + 1)
        if not hunks or lo > end + 1:
            hunks.append([])
        for j in range(max(lo, end + 1), hi + 1):
            hunks[-1].append({"text": lines[j], "match": j in hit})
        end = max(end, hi)
    return hunks


def grep_bulletins(
    conn: sqlite3.Connection, parish_slug: str, pattern: str | None = None, *,
    bulletins: int = 0,
) -> dict[str, Any]:
    """`seed grep`: the matching lines of every bulletin with a stored PDF, newest first.

    Searches the text layer, as `seed text` reads it, line by line and in any
    case; `pattern` is a regular expression, `SCHEDULE_PATTERN` when None. A
    page that is only an image can't be searched, and is listed as such.
    `bulletins` limits it to the newest N (0: all).
    """
    try:
        regex = re.compile(pattern or SCHEDULE_PATTERN, re.IGNORECASE)
    except re.error as exc:
        raise SeedError(f"Not a regular expression: {pattern!r} ({exc})") from exc
    rows = [b for b in parish_bulletins(conn, parish_slug)
            if b["duplicate_of"] is None]
    held = stored_pdfs(parish_slug) if rows else set()
    readable = [b for b in rows if held is None or b["content_hash"] in held]
    shown = readable[:bulletins] if bulletins > 0 else readable
    out = []
    for b in shown:
        item = {k: b[k] for k in ("short", "content_hash", "fetched_at", "published_date")}
        try:
            _, pages = _pdf_texts(_read_pdf(parish_slug, b["content_hash"]))
        except Exception as exc:  # unreadable: say so, don't stop
            out.append({**item, "error": str(exc), "pages": []})
            continue
        found = []
        for p in pages:
            lines = [line.strip() for line in p["text"].splitlines() if line.strip()]
            hits = [i for i, line in enumerate(lines) if regex.search(line)]
            if p["image_only"] or hits:
                found.append({"page": p["page"], "image_only": p["image_only"],
                              "hunks": _hunks(lines, hits)})
        out.append({**item, "error": None, "pages": found})
    return {
        "parish": parish_slug,
        "pattern": regex.pattern,
        "default_pattern": not pattern,
        "bulletins": out,
        "not_searched": len(rows) - len(shown),
    }


# ── Extract mode's history ──────────────────────────────────────────────────
def _hhmm(value: Any) -> str | None:
    minutes = time_to_minutes(value) if isinstance(value, str) else None
    return None if minutes is None else f"{minutes // 60:02d}:{minutes % 60:02d}"


def history(
    conn: sqlite3.Connection, parish_slug: str, *, bulletins: int = HISTORY_BULLETINS,
) -> dict[str, Any]:
    """`seed history`: extract mode's stored events for the parish's last processed bulletins.

    They came from the older production prompt, after weekly promotion, so a
    difference from the bulletin is a reason to look closer, not a vote.
    """
    rows = [b for b in parish_bulletins(conn, parish_slug)
            if b["processed_at"] and b["duplicate_of"] is None][:max(1, bulletins)]
    return {"parish": parish_slug, "bulletins": _history_of(conn, rows)}


def recent_history(
    conn: sqlite3.Connection, parish_slug: str, *, bulletins: int | None = None,
) -> list[dict[str, Any]]:
    """`history`'s bulletins for comparing with a seed (`seed diff`, `seed finalize`).

    By default the processed bulletins whose PDF is still stored, the ones a
    drafter can read (the newest `HISTORY_BULLETINS` when the store can't be
    listed); `bulletins` takes the newest N instead.
    """
    rows = [b for b in parish_bulletins(conn, parish_slug)
            if b["processed_at"] and b["duplicate_of"] is None]
    if bulletins is None:
        held = stored_pdfs(parish_slug) if rows else set()
        rows = (rows[:HISTORY_BULLETINS] if held is None
                else [b for b in rows if b["content_hash"] in held])
    else:
        rows = rows[:max(1, bulletins)]
    return _history_of(conn, rows)


def _history_of(conn: sqlite3.Connection, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract mode's events for each of `rows` (`parish_bulletins` items), with pages."""
    events = load_events(conn, [b["id"] for b in rows])
    by_bulletin: dict[int, list[dict[str, Any]]] = {b["id"]: [] for b in rows}
    for ev in events:
        by_bulletin[ev["bulletin_id"]].append({
            "church_slug": ev["church_slug"],
            "event_type": ev["event_type"],
            "event_kind": ev["event_kind"],
            "day_of_week": ev["day_of_week"],
            "date": ev["date"],
            "start_time": _hhmm(ev["start_time"]),
            "end_time": _hhmm(ev["end_time"]),
            "cancelled": ev["cancelled"],
            "page_number": ev["page_number"],
            "note": ev["note"],
        })
    return [
        {
            "short": b["short"],
            "content_hash": b["content_hash"],
            "fetched_at": b["fetched_at"],
            "published_date": b["published_date"],
            "wrong_bulletin": b["wrong_bulletin"],
            "events": sorted(by_bulletin[b["id"]], key=_event_order),
        }
        for b in rows
    ]


_DAY_ORDER = {d: i for i, d in enumerate(
    ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"))}


def _event_order(ev: dict[str, Any]) -> tuple:
    return (
        ev["church_slug"] or "", ev["event_kind"] != "weekly",
        _DAY_ORDER.get(ev["day_of_week"] or "", 7), ev["date"] or "", ev["start_time"] or "",
        ev["event_type"] or "",
    )


# ── Churches, and where a draft starts ──────────────────────────────────────
def _address(row: sqlite3.Row) -> str:
    town = " ".join(x for x in (row["state"], row["postal_code"]) if x)
    return ", ".join(x for x in (row["address_line1"], row["address_line2"], row["city"], town)
                     if x)


def _church_words(text: str) -> str:
    """`text` lowercased, punctuation and hyphens as spaces, and "saint" as "st", so a
    bulletin's "St. Mary's, Oswego" and a slug's "st-marys-oswego" compare alike."""
    text = re.sub(r"['’]", "", re.sub(r"['’]s\b", "", text.lower()))
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return f" {re.sub(r'\bsaint\b', 'st', text).strip()} "


def find_churches(conn: sqlite3.Connection, query: str) -> dict[str, Any]:
    """`seed church`: the churches whose slug, name and address (town included), with
    their parish's slug and name, hold every word of `query` in any case and order
    ("Immaculate Conception Ithaca" finds the church named one in the town of the
    other). Read from churches.csv and parishes.csv as the database loaded them,
    retired churches left out."""
    words = _church_words(query).split()
    if not words:
        raise SeedError("Name something to look for: a slug, a name, a town or an address")
    rows = conn.execute(
        """SELECT c.slug, c.name, c.address_line1, c.address_line2, c.city, c.state,
                  c.postal_code, p.slug AS parish, p.name AS parish_name
           FROM church c JOIN parish p ON p.id = c.parish_id
           WHERE c.retired_at IS NULL ORDER BY p.slug, c.slug""",
    ).fetchall()
    found = []
    for row in rows:
        address = _address(row)
        fields = (row["slug"], row["name"], address, row["parish"], row["parish_name"])
        haystack = _church_words(" ".join(f or "" for f in fields))
        if all(f" {word}" in haystack for word in words):
            found.append({"church": row["slug"], "parish": row["parish"], "name": row["name"],
                          "address": address})
    return {"query": query, "churches": found}


def _history_summary(past: list[dict[str, Any]], since: str | None) -> list[dict[str, Any]]:
    """Each distinct event in `history`'s bulletins (newest first), with how many of them it
    is in, dated ones before `since` left out. Notes and pages may differ between
    bulletins: the newest's are kept."""
    seen: dict[tuple, dict[str, Any]] = {}
    for b in past:
        if b["wrong_bulletin"]:
            continue
        for ev in b["events"]:
            if ev["event_kind"] != "weekly" and since and (ev["date"] or "") < since:
                continue
            key = tuple(ev[k] for k in ev if k not in ("page_number", "note"))
            row = seen.setdefault(key, {"event": ev, "bulletins": 0, "in": set()})
            if b["short"] not in row["in"]:
                row["in"].add(b["short"])
                row["bulletins"] += 1
    for row in seen.values():
        del row["in"]
    return sorted(seen.values(), key=lambda r: _event_order(r["event"]))


def brief(
    conn: sqlite3.Connection, parish_slug: str, *,
    work_dir: Path = WORK_DIR,
) -> dict[str, Any]:
    """`seed brief`, which `seed start` prints too: what a drafter starts a parish from.

    The parish's website and churches, its bulletins (`seed bulletins`), the
    distinct events of its last `HISTORY_BULLETINS` processed bulletins with how
    many each is in, but dated ones before the newest bulletin's fetch date
    (outside a seed's scope; `history` null past `BRIEF_HISTORY_ROWS`, for a
    pointer to `seed history`), the newest PDF, written as `seed pdf <parish>
    latest` writes it, and the days the newest bulletin covers with the weeks of
    the month each weekday falls in then (`checks.covered_weeks`): a "First
    Friday" slot it can't hold may be settled from an older bulletin.
    """
    parish = conn.execute(
        "SELECT id, slug, name, homepage_url FROM parish WHERE slug = ?", (parish_slug,),
    ).fetchone()
    if parish is None:
        raise SeedError(f"Parish not found: {parish_slug} (is it in data/parishes.csv?)")
    churches = [{"church": c["slug"], "name": c["name"], "address": _address(c)}
                for c in list_churches(conn, parish["id"])]
    bulletins = list_bulletins(conn, parish_slug)
    newest = bulletins["bulletins"][0]["fetched_at"] if bulletins["bulletins"] else None
    since = normalize_as_of(newest)[:10] if newest else None
    past = history(conn, parish_slug)["bulletins"]
    summary = _history_summary(past, since)
    try:
        pdf: dict[str, Any] = export_pdf(conn, parish_slug, "latest",
                                         work_dir=work_dir)
    except Exception as exc:  # no PDF to read: say why, don't stop
        pdf = {"error": str(exc)}
    week = None
    if bulletins["bulletins"]:
        first = bulletins["bulletins"][0]
        start = bulletin_week(first)
        if start is not None:
            week = {
                "from": start.isoformat(),
                "to": (start + timedelta(days=COVERED_DAYS - 1)).isoformat(),
                "weeks": {day: sorted(covered_weeks(first, day) or [], key=WEEKS_OF_MONTH.index)
                          for day in DAYS},
            }
    return {
        "parish": parish_slug,
        "name": parish["name"],
        "website": parish["homepage_url"],
        "churches": churches,
        "bulletins": bulletins,
        "newest_week": week,
        "history_bulletins": [b["short"] for b in past if not b["wrong_bulletin"]],
        "history_since": since,
        "history_events": len(summary),
        "history": summary if len(summary) <= BRIEF_HISTORY_ROWS else None,
        "pdf": pdf,
    }


