"""What the labeler shows: the bulletin queue, and each bulletin's Gemini output.

Gemini's output for a bulletin is read from the classifier's result cache,
which holds the extraction exactly as the model returned it: first under the
current classifier version and church list (the key `process` would use), then
under any version the cache has for the same PDF. Only when nothing is cached
does it fall back to the bulletin's rows in the `event` table, which have been
through storage and weekly promotion ("post-processing") and are marked so.

For a parish in update mode the model is not asked for the whole schedule, so
its answer is the schedule its call was shown (the view) with the call's
applied proposals made, the pages coming from the call's sightings and
proposals (`update_mode_source`).
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import get_store
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.labeling.labels import (
    DAYS,
    EVENT_KINDS,
    EVENT_TYPES,
    WEEKS_OF_MONTH,
    is_valid_hash,
    label_statuses,
)
from pdf_extract.runner import _cache_version_component, cache_key
from pdf_extract.schedule.store import church_slugs, load_entries, table_exists
from pdf_extract.storage import (
    church_list_for_prompt,
    latest_bulletin_order,
    load_events,
)
from pdf_extract.timeparse import normalize_event_date, time_to_minutes

LOGGER = logging.getLogger(__name__)

UNLABELED = "unlabeled"

# A cache directory is `<readable version>-<digest>`; the Gemini classifier's
# version is `<model>+prompt-<fingerprint>`, whose `+` the readable part turns to `_`.
_VERSION_DIR_RE = re.compile(r"^(?P<model>.+?)_prompt-(?P<prompt>[0-9a-f]{12})-[0-9a-f]{12}$")

_LISTING_TTL_SECONDS = 300.0
_listing_lock = threading.Lock()
_listing: dict[str, Any] = {"store": None, "prefix": None, "at": 0.0, "keys": []}


# ── Queue ───────────────────────────────────────────────────────────────────
def list_bulletins(conn: sqlite3.Connection, labels_dir: Path) -> list[dict[str, Any]]:
    """Every labelable bulletin, in queue order, with its label status.

    Queue order takes parishes in turn: each parish's latest bulletin first
    (alphabetically by parish), then each parish's second latest, and so on.
    A PDF fetched under two URLs is one bulletin to label; its best-ranked row
    stands for it.
    """
    rows = conn.execute(
        f"""
        SELECT p.slug AS parish_slug, p.name AS parish_name, b.id AS bulletin_id,
               b.source_url, b.content_hash, b.published_date, b.fetched_at, b.processed_at,
               ROW_NUMBER() OVER (
                   PARTITION BY b.parish_id ORDER BY {latest_bulletin_order("b")}
               ) - 1 AS row_rank
        FROM bulletin b JOIN parish p ON p.id = b.parish_id
        WHERE b.content_hash IS NOT NULL
        """
    ).fetchall()
    statuses = label_statuses(labels_dir)
    seen: set[tuple[str, str]] = set()
    by_parish_rank: dict[str, int] = {}
    out: list[dict[str, Any]] = []
    for r in sorted(rows, key=lambda r: (r["parish_slug"], r["row_rank"])):
        key = (r["parish_slug"], r["content_hash"])
        if key in seen or not is_valid_hash(r["content_hash"]):
            continue
        seen.add(key)
        rank = by_parish_rank.get(r["parish_slug"], 0)
        by_parish_rank[r["parish_slug"]] = rank + 1
        item = dict(r)
        del item["row_rank"]
        item["rank"] = rank
        item["status"] = statuses.get(key, UNLABELED)
        out.append(item)
    out.sort(key=lambda b: (b["rank"], b["parish_name"].lower(), b["parish_slug"]))
    return out


def next_bulletin(
    queue: list[dict[str, Any]],
    *,
    after: tuple[str, str] | None = None,
    parish_slug: str | None = None,
    unlabeled_parishes: bool = False,
) -> dict[str, Any] | None:
    """The next bulletin to label: unlabeled first, then ones left in progress.

    Searches forward from `after` (wrapping round), never returning `after`
    itself, so "next" from a bulletin moves on even if it is unfinished.

    With `unlabeled_parishes`, only the latest bulletin of each parish that
    has no label yet is eligible, in the same queue order. A parish counts as
    labeled once any of its bulletins is in progress, done, or skipped.
    """
    if unlabeled_parishes:
        labeled = {b["parish_slug"] for b in queue if b["status"] != UNLABELED}
        candidates = [
            b for b in queue
            if b["rank"] == 0
            and b["parish_slug"] not in labeled
            and (parish_slug is None or b["parish_slug"] == parish_slug)
        ]
    else:
        candidates = [b for b in queue if parish_slug is None or b["parish_slug"] == parish_slug]
    start = 0
    if after is not None:
        for i, b in enumerate(candidates):
            if (b["parish_slug"], b["content_hash"]) == after:
                start = i + 1
                break
    ordered = candidates[start:] + candidates[:start]
    ordered = [b for b in ordered if (b["parish_slug"], b["content_hash"]) != after]
    for wanted in (UNLABELED, "in_progress"):
        for b in ordered:
            if b["status"] == wanted:
                return b
    return None


def progress(queue: list[dict[str, Any]]) -> dict[str, int]:
    """Bulletin counts, plus how many parishes have at least one label.

    `parishes_labeled` is the tracker: a parish counts once any bulletin has
    a label (in progress, done, or skipped), not only when its latest is done.
    `latest_done` remains the count of latest bulletins marked done or skipped.
    """
    latest = [b for b in queue if b["rank"] == 0]
    labeled = {b["parish_slug"] for b in queue if b["status"] != UNLABELED}
    counts = {
        "latest_total": len(latest),
        "latest_done": sum(1 for b in latest if b["status"] in ("done", "skipped")),
        "parishes_labeled": len(labeled),
        "total": len(queue),
    }
    for status in (UNLABELED, "in_progress", "done", "skipped"):
        counts[status] = sum(1 for b in queue if b["status"] == status)
    return counts


def parish_bulletins(queue: list[dict[str, Any]], parish_slug: str) -> list[dict[str, Any]]:
    """Every bulletin of one parish, latest first, for the bulletin switcher."""
    rows = [b for b in queue if b["parish_slug"] == parish_slug]
    rows.sort(key=lambda b: b["rank"])
    return [
        {
            "content_hash": b["content_hash"],
            "published_date": b["published_date"],
            "fetched_at": b["fetched_at"],
            "rank": b["rank"],
            "status": b["status"],
        }
        for b in rows
    ]


# ── Gemini's output ─────────────────────────────────────────────────────────
def _hhmm(raw: Any) -> str | None:
    minutes = time_to_minutes(raw) if isinstance(raw, str) else None
    return None if minutes is None else f"{minutes // 60:02d}:{minutes % 60:02d}"


def _day(raw: Any) -> str | None:
    if not isinstance(raw, str) or len(raw.strip()) < 2:
        return None
    prefix = raw.strip().lower()[:3]
    return next((d for d in DAYS if d.lower().startswith(prefix)), None)


def _weeks(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    weeks = {str(w).strip().lower() for w in raw}
    return [w for w in WEEKS_OF_MONTH if w in weeks]


def _season(ev: dict[str, Any]) -> dict[str, int | None] | None:
    """A season from the flat `season_*` fields the pipeline adds in schema v2, if any."""
    start, end = ev.get("season_start_month"), ev.get("season_end_month")
    if not (isinstance(start, int) and isinstance(end, int)):
        return None
    if not (1 <= start <= 12 and 1 <= end <= 12):
        return None
    start_day, end_day = ev.get("season_start_day"), ev.get("season_end_day")
    return {
        "start_month": start,
        "start_day": start_day if isinstance(start_day, int) else None,
        "end_month": end,
        "end_day": end_day if isinstance(end_day, int) else None,
    }


def gemini_rows(events: list[Any]) -> list[dict[str, Any]]:
    """Gemini's flat events in the label's row shape, keeping the raw strings.

    `problems` lists what could not be read (an unparseable time, say), so the
    labeler sees it instead of the row silently vanishing.
    """
    out = []
    for i, ev in enumerate(events):
        if not isinstance(ev, dict):
            continue
        event_type = ev.get("type", ev.get("event_type"))
        kind = ev.get("kind", ev.get("event_kind"))
        weekly = kind == "weekly"
        row = {
            "id": f"g{i}",
            "church_slug": ev.get("church_slug") if isinstance(ev.get("church_slug"), str) else "",
            "event_type": event_type if event_type in EVENT_TYPES else None,
            "event_kind": kind if kind in EVENT_KINDS else None,
            "day_of_week": _day(ev.get("day_of_week")) if weekly else None,
            "date": None if weekly else normalize_event_date(ev.get("date")),
            "start_time": _hhmm(ev.get("start_time")),
            "end_time": _hhmm(ev.get("end_time")),
            "cancelled": bool(ev.get("cancelled", False)),
            "weeks_of_month": _weeks(ev.get("weeks_of_month")) if weekly else [],
            "season": _season(ev) if weekly else None,
            "page_number": ev.get("page_number") if isinstance(ev.get("page_number"), int) else None,
            "note": ev.get("note") if isinstance(ev.get("note"), str) and ev["note"].strip() else None,
            "raw": {
                k: ev.get(k) for k in ("day_of_week", "date", "start_time", "end_time")
                if ev.get(k) is not None
            },
        }
        problems = []
        if row["event_type"] is None:
            problems.append(f"unknown type {event_type!r}")
        if row["event_kind"] is None:
            problems.append(f"unknown kind {kind!r}")
        elif weekly and row["day_of_week"] is None:
            problems.append(f"unreadable day {ev.get('day_of_week')!r}")
        elif not weekly and row["date"] is None:
            problems.append(f"unreadable date {ev.get('date')!r}")
        if row["start_time"] is None:
            problems.append(f"unreadable start time {ev.get('start_time')!r}")
        if ev.get("end_time") and row["end_time"] is None:
            problems.append(f"unreadable end time {ev.get('end_time')!r}")
        row["problems"] = problems
        out.append(row)
    return out


def _describe_version_dir(version_dir: str) -> dict[str, str | None]:
    m = _VERSION_DIR_RE.match(version_dir)
    if not m:
        return {"model": None, "prompt_version": None}
    return {"model": m["model"], "prompt_version": m["prompt"]}


def _cache_keys(prefix: str) -> list[str]:
    """Keys under `prefix`, remembered for a few minutes when they come from R2."""
    store = get_store()
    now = time.monotonic()
    with _listing_lock:
        fresh = (
            _listing["store"] is store
            and _listing["prefix"] == prefix
            and now - _listing["at"] < _LISTING_TTL_SECONDS
        )
        if fresh and store.is_remote:
            return list(_listing["keys"])
    keys = list(store.list(prefix))
    with _listing_lock:
        _listing.update(store=store, prefix=prefix, at=now, keys=keys)
    return keys


def _read_json(key: str) -> dict[str, Any] | None:
    try:
        data = get_store().get(key)
    except Exception:
        LOGGER.warning("Reading %s failed", key, exc_info=True)
        return None
    if data is None:
        return None
    try:
        parsed = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        LOGGER.warning("Unreadable cached result %s", key)
        return None
    return parsed if isinstance(parsed, dict) else None


def update_mode_source(conn: sqlite3.Connection, bulletin_id: int) -> dict[str, Any] | None:
    """The bulletin's latest successful update call as an answer, or None if it has none.

    The rows are the call's view with its applied proposals made: modified
    and deleted entries out, added and modified ones in.
    """
    if not table_exists(conn, "llm_call"):
        return None
    call = conn.execute(
        """SELECT c.id, c.model, c.version, c.published_date, c.wrong_bulletin,
                  c.church_list_needs_review, v.json AS view_json
           FROM llm_call c JOIN schedule_view v ON v.hash = c.view_hash
           WHERE c.bulletin_id = ? AND c.status IN ('ok', 'lenient')
           ORDER BY c.id DESC LIMIT 1""",
        (bulletin_id,),
    ).fetchone()
    if call is None:
        return None
    pages = dict(conn.execute(
        "SELECT entry_id, page_number FROM entry_sighting WHERE bulletin_id = ?",
        (bulletin_id,),
    ).fetchall())
    applied = conn.execute(
        """SELECT op, target_entry_id, entry_id, page_number FROM proposed_change
           WHERE llm_call_id = ? AND decision = 'applied' ORDER BY seq""",
        (call["id"],),
    ).fetchall()
    removed = {row["target_entry_id"] for row in applied if row["target_entry_id"]}
    events: list[dict[str, Any]] = []
    for church in json.loads(call["view_json"])["churches"]:
        for item in church["entries"]:
            if item["id"] in removed:
                continue
            events.append(_view_event(church["slug"], item, pages.get(item["id"])))
    added = [row for row in applied if row["entry_id"] is not None]
    entries = load_entries(conn, [row["entry_id"] for row in added])
    slugs = church_slugs(conn, [e.church_id for e in entries.values()])
    for row in added:
        entry = entries[row["entry_id"]]
        events.append(_view_event(
            slugs[entry.church_id], entry.view(row["entry_id"]), row["page_number"],
        ))
    return {
        "source": {
            "kind": "update",
            "classifier": "schedule_update",
            "llm_call_id": call["id"],
            "model": call["model"],
            "prompt_version": call["version"][:12],
        },
        "published_date": call["published_date"],
        "wrong_bulletin": bool(call["wrong_bulletin"]),
        "church_list_needs_review": bool(call["church_list_needs_review"]),
        "events": gemini_rows(events),
    }


def _view_event(church_slug: str, item: dict[str, Any], page: int | None) -> dict[str, Any]:
    """A view entry in the flat shape `gemini_rows` reads."""
    season = item.get("season") or {}
    return {
        **{k: v for k, v in item.items() if k not in ("id", "season")},
        "church_slug": church_slug,
        "page_number": page,
        "season_start_month": season.get("start_month"),
        "season_start_day": season.get("start_day"),
        "season_end_month": season.get("end_month"),
        "season_end_day": season.get("end_day"),
    }


def load_gemini_source(
    conn: sqlite3.Connection,
    *,
    bulletin_id: int,
    content_hash: str,
    churches: list[dict[str, Any]],
    published_date: str | None,
    processed_at: str | None,
) -> dict[str, Any]:
    """Gemini's output for one bulletin, and where it came from."""
    update = update_mode_source(conn, bulletin_id)
    if update is not None:
        return update
    classifier = GeminiClassifier()
    current_dir = _cache_version_component(classifier.version)
    exact = cache_key(classifier.name, classifier.version, content_hash, churches)
    model, _, prompt = classifier.version.partition("+prompt-")

    candidates = [exact]
    prefix = f"runs/{classifier.name}/cache/"
    try:
        listed = [
            k for k in _cache_keys(prefix)
            if k != exact and k.rsplit("/", 1)[-1].startswith(f"{content_hash}-")
        ]
    except Exception:
        LOGGER.warning("Listing %s failed; only the exact cache key is tried", prefix, exc_info=True)
        listed = []
    candidates += sorted(listed, key=lambda k: (k.split("/")[3] != current_dir, k))

    fingerprint = exact.rsplit("-", 1)[-1]
    for key in candidates:
        cached = _read_json(key)
        if cached is None:
            continue
        version_dir = key.split("/")[3]
        described = (
            {"model": model, "prompt_version": prompt}
            if version_dir == current_dir else _describe_version_dir(version_dir)
        )
        return {
            "source": {
                "kind": "cache",
                "classifier": classifier.name,
                "version_dir": version_dir,
                "is_current_version": version_dir == current_dir,
                "church_list_matches": key.rsplit("-", 1)[-1] == fingerprint,
                "key": key,
                **described,
            },
            "published_date": cached.get("published_date")
            if isinstance(cached.get("published_date"), str) else None,
            "wrong_bulletin": bool(cached.get("wrong_bulletin", False)),
            "church_list_needs_review": bool(cached.get("church_list_needs_review", False)),
            "events": gemini_rows(cached.get("events") or []),
        }

    stored = load_events(conn, [bulletin_id])
    if stored or processed_at:
        events = [
            {**ev, "type": ev["event_type"], "kind": ev["event_kind"]} for ev in stored
        ]
        return {
            "source": {
                "kind": "post-processing",
                "classifier": classifier.name,
                "model": None,
                "prompt_version": None,
                "processed_at": processed_at,
            },
            "published_date": published_date,
            "wrong_bulletin": None,
            "church_list_needs_review": None,
            "events": gemini_rows(events),
        }
    return {
        "source": {"kind": "none", "classifier": classifier.name},
        "published_date": None,
        "wrong_bulletin": None,
        "church_list_needs_review": None,
        "events": [],
    }


# ── One bulletin ────────────────────────────────────────────────────────────
def find_bulletin(
    conn: sqlite3.Connection, parish_slug: str, content_hash: str,
) -> sqlite3.Row | None:
    """The best-ranked bulletin row for this parish and PDF, if there is one."""
    return conn.execute(
        f"""SELECT b.id, b.parish_id, b.source_url, b.content_hash, b.published_date,
                   b.fetched_at, b.processed_at
            FROM bulletin b JOIN parish p ON p.id = b.parish_id
            WHERE p.slug = ? AND b.content_hash = ?
            ORDER BY {latest_bulletin_order("b")}
            LIMIT 1""",
        (parish_slug, content_hash),
    ).fetchone()


def bulletin_detail(
    conn: sqlite3.Connection, parish_slug: str, content_hash: str,
) -> dict[str, Any] | None:
    bulletin = find_bulletin(conn, parish_slug, content_hash)
    if bulletin is None:
        return None
    parish = conn.execute(
        "SELECT slug, name, homepage_url FROM parish WHERE id = ?", (bulletin["parish_id"],)
    ).fetchone()
    churches = church_list_for_prompt(conn, bulletin["parish_id"])
    return {
        "parish": dict(parish),
        "churches": churches,
        "bulletin": {
            "source_url": bulletin["source_url"],
            "content_hash": bulletin["content_hash"],
            "published_date": bulletin["published_date"],
            "fetched_at": bulletin["fetched_at"],
            "processed_at": bulletin["processed_at"],
        },
        "gemini": load_gemini_source(
            conn,
            bulletin_id=bulletin["id"],
            content_hash=content_hash,
            churches=churches,
            published_date=bulletin["published_date"],
            processed_at=bulletin["processed_at"],
        ),
    }
