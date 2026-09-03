"""Reads the on-disk corpus the labeling app reviews.

Everything here is read-only: classifier runs under `data/runs/<name>/`, the
bulletin manifest in `data/metadata.json`, and the parish/church CSVs used for
display names. Writes go through `labelapp.store`.
"""

from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pdf_extract.runner import RUNS_DIR
from pdf_extract.storage import (
    BULLETINS_METADATA_PATH,
    CHURCHES_CSV_PATH,
    PARISHES_CSV_PATH,
    load_json_list,
)

LOGGER = logging.getLogger(__name__)

# `compare` writes its reports here; it is not a classifier run.
RESERVED_RUN_DIRS = {"compare", "cache"}


def normalize_pdf_path(raw: str) -> Path:
    """Interpret a `pdf_path` from metadata.json on the current platform.

    The pipeline records whatever separator the fetching machine used, so paths
    written on Windows arrive as `data\\bulletins\\...` and will not resolve on
    a POSIX host without this.
    """
    return Path(raw.replace("\\", "/"))


@dataclass
class Bulletin:
    """One fetched bulletin, as the labeling queue sees it."""

    source_url: str
    parish_slug: str
    content_hash: str | None
    pdf_path: Path | None
    published_date: str | None
    fetched_at: str | None


@dataclass
class Run:
    """One classifier run loaded from `data/runs/<name>/`."""

    name: str
    version: str | None = None
    #: bulletin source_url -> the events that run produced for it
    events_by_bulletin: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    #: bulletins the run actually served, including any it returned zero events for
    covered: set[str] = field(default_factory=set)
    #: bulletins this run flagged as not the bulletin it was asked for
    wrong_bulletin: set[str] = field(default_factory=set)


def available_runs() -> list[str]:
    """Names of classifier runs that have an events.json on disk."""
    if not RUNS_DIR.exists():
        return []
    names = [
        entry.name
        for entry in RUNS_DIR.iterdir()
        if entry.is_dir()
        and entry.name not in RESERVED_RUN_DIRS
        and (entry / "events.json").exists()
    ]
    return sorted(names)


def _read_json(path: Path) -> Any:
    """Read an optional JSON file. A missing one is normal; a broken one is not."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        LOGGER.warning("Could not read %s; treating as empty", path, exc_info=True)
        return None


def load_run(name: str) -> Run:
    """Load one classifier run. Raises FileNotFoundError if it was never run."""
    run_dir = RUNS_DIR / name
    events_file = run_dir / "events.json"
    if not events_file.exists():
        raise FileNotFoundError(
            f"No events.json for classifier {name!r} at {events_file}. "
            f"Run `pnpm extract -- --classifier {name}` first."
        )

    run = Run(name=name)

    summary = _read_json(run_dir / "run.json")
    if isinstance(summary, dict):
        version = summary.get("classifier_version")
        run.version = version if isinstance(version, str) else None

    # bulletins.json lists every bulletin the run served. Keep it: a bulletin
    # served with zero events is a real prediction ("nothing here"), and it is
    # indistinguishable from "never run" if we only look at events.json.
    manifest = _read_json(run_dir / "bulletins.json")
    if isinstance(manifest, list):
        for row in manifest:
            if not isinstance(row, dict) or not isinstance(row.get("bulletin_source_url"), str):
                continue
            url = row["bulletin_source_url"]
            run.covered.add(url)
            run.events_by_bulletin.setdefault(url, [])
            if row.get("wrong_bulletin"):
                run.wrong_bulletin.add(url)

    rows = _read_json(events_file)
    if isinstance(rows, list):
        for row in rows:
            if not isinstance(row, dict):
                continue
            url = row.get("bulletin_source_url")
            if not isinstance(url, str):
                continue
            run.covered.add(url)
            run.events_by_bulletin.setdefault(url, []).append(row)

    return run


def load_runs(names: list[str]) -> dict[str, Run]:
    return {name: load_run(name) for name in names}


def load_bulletins() -> dict[str, Bulletin]:
    """Bulletins from metadata.json, keyed by source URL."""
    bulletins: dict[str, Bulletin] = {}
    for entry in load_json_list(BULLETINS_METADATA_PATH):
        if not isinstance(entry, dict):
            continue
        source_url = entry.get("source_url")
        if not isinstance(source_url, str):
            continue
        raw_pdf_path = entry.get("pdf_path")
        bulletins[source_url] = Bulletin(
            source_url=source_url,
            parish_slug=str(entry.get("parish_slug") or ""),
            content_hash=(
                entry["content_hash"] if isinstance(entry.get("content_hash"), str) else None
            ),
            pdf_path=(
                normalize_pdf_path(raw_pdf_path) if isinstance(raw_pdf_path, str) else None
            ),
            published_date=(
                entry["published_date"] if isinstance(entry.get("published_date"), str) else None
            ),
            fetched_at=entry["fetched_at"] if isinstance(entry.get("fetched_at"), str) else None,
        )
    return bulletins


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_church_names() -> dict[str, str]:
    """church slug -> display name."""
    return {
        row["slug"]: row.get("name") or row["slug"]
        for row in _read_csv_rows(CHURCHES_CSV_PATH)
        if row.get("slug")
    }


def load_parish_names() -> dict[str, str]:
    """parish slug -> display name."""
    return {
        row["slug"]: row.get("name") or row["slug"]
        for row in _read_csv_rows(PARISHES_CSV_PATH)
        if row.get("slug")
    }


def churches_by_parish() -> dict[str, list[dict[str, str]]]:
    """parish slug -> its churches, for the manual add-event picker."""
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in _read_csv_rows(CHURCHES_CSV_PATH):
        slug = row.get("slug")
        parish_slug = row.get("parish_id")
        if not slug or not parish_slug:
            continue
        grouped.setdefault(parish_slug, []).append(
            {"slug": slug, "name": row.get("name") or slug}
        )
    return grouped
