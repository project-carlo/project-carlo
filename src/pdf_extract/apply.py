"""Apply detect and geocode results back into the source CSV files."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from pdf_extract.address import address_key
from pdf_extract.storage import (
    CHURCHES_CSV_PATH,
    DETECT_RESULTS_PATH,
    GEOCODE_RESULTS_PATH,
    PARISHES_CSV_PATH,
    load_json_dict,
    load_json_list,
)

LOGGER = logging.getLogger(__name__)

_PARISHES_FIELDNAMES = ["slug", "name", "website", "bulletin_provider", "provider_id"]
_CHURCHES_FIELDNAMES = [
    "parish_id", "slug", "name", "line1", "line2", "city", "state", "postal_code",
    "name_verified", "address_verified", "latitude", "longitude",
]


def _read_csv(path: Path) -> list[dict[str, str]]:
    """Read a CSV into plain dicts, one per row."""
    with open(path, encoding="utf-8") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    """Write rows to a CSV via a temp file, then atomically rename."""
    tmp = path.with_suffix(".csv.tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(path)


def apply_detect_results() -> dict[str, int]:
    """Merge detect_results.json into parishes.csv."""
    results = load_json_dict(DETECT_RESULTS_PATH)
    if not results:
        LOGGER.info("No detect_results.json found, nothing to apply")
        return {"updated": 0, "unchanged": 0}

    rows = _read_csv(PARISHES_CSV_PATH)

    updated = 0
    unchanged = 0
    for row in rows:
        slug = row["slug"]
        if slug in results:
            info = results[slug]
            row["bulletin_provider"] = info.get("bulletin_provider") or ""
            row["provider_id"] = info.get("provider_id") or ""
            updated += 1
        else:
            row.setdefault("bulletin_provider", "")
            row.setdefault("provider_id", "")
            unchanged += 1

    _write_csv(PARISHES_CSV_PATH, _PARISHES_FIELDNAMES, rows)
    DETECT_RESULTS_PATH.unlink()
    LOGGER.info("Applied detect results to parishes.csv: %d updated, %d unchanged", updated, unchanged)
    return {"updated": updated, "unchanged": unchanged}


def apply_geocode_results() -> dict[str, int]:
    """Merge geocode_results.json into churches.csv."""
    geocode_results = load_json_list(GEOCODE_RESULTS_PATH)
    if not geocode_results:
        LOGGER.info("No geocode_results.json found, nothing to apply")
        return {"updated": 0}

    # Build lookup: address_key -> (lat, lng)
    geo_lookup: dict[str, tuple[float, float]] = {}
    for geo in geocode_results:
        lat = geo.get("latitude")
        lng = geo.get("longitude")
        if not isinstance(lat, (int, float)) or not isinstance(lng, (int, float)):
            continue
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            continue
        key = address_key(
            geo.get("line1"), geo.get("line2"),
            geo.get("city"), geo.get("state"), geo.get("postal_code"),
        )
        geo_lookup[key] = (lat, lng)

    rows = _read_csv(CHURCHES_CSV_PATH)

    updated = 0
    for row in rows:
        key = address_key(
            row.get("line1"), row.get("line2"),
            row.get("city"), row.get("state"), row.get("postal_code"),
        )
        if key in geo_lookup:
            lat, lng = geo_lookup[key]
            row["latitude"] = str(lat)
            row["longitude"] = str(lng)
            updated += 1
        else:
            row.setdefault("latitude", "")
            row.setdefault("longitude", "")

    _write_csv(CHURCHES_CSV_PATH, _CHURCHES_FIELDNAMES, rows)
    GEOCODE_RESULTS_PATH.unlink()
    LOGGER.info("Applied geocode results to churches.csv: %d updated", updated)
    return {"updated": updated}
