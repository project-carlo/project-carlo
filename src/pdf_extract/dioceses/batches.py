"""Validate a saved scout plan against all local rosters, without fetching sources."""

from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from pdf_extract.dioceses import records, rosters
from pdf_extract.dioceses.records import DioceseError


def validate(diocese: str, path: Path | None = None) -> dict[str, Any]:
    path = path if path is not None else records.diocese_dir(diocese) / "batches.json"
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DioceseError(f"cannot read batch manifest {path}: {exc}") from None
    errors: list[str] = []
    expected: set[str] = set()
    for name in rosters.roster_names(diocese):
        roster = rosters.load_roster(diocese, name)
        for index, entry in enumerate(roster["entries"], 1):
            entry_id = entry.get("id") if isinstance(entry, Mapping) else None
            if isinstance(entry_id, bool) or not isinstance(entry_id, str | int) \
                    or not str(entry_id).strip():
                errors.append(f"rosters/{name}.json entry #{index}: nonempty id is required")
                continue
            ref = f"{name}:{entry_id}"
            if ref in expected:
                errors.append(f"rosters/{name}.json: duplicate id {entry_id!r}")
            expected.add(ref)
    if not expected:
        errors.append("no roster entries to plan; fetch or import the local rosters first")

    def fields(value: Any, required: set[str], where: str) -> bool:
        if not isinstance(value, dict):
            errors.append(f"{where} must be an object")
            return False
        for key in sorted(required - value.keys()):
            errors.append(f"{where}: missing field {key}")
        for key in sorted(value.keys() - required):
            errors.append(f"{where}: unknown field {key}")
        return True

    def text(value: Any, where: str) -> bool:
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{where} must be nonempty text")
            return False
        return True

    uses: dict[str, list[str]] = defaultdict(list)
    assigned: set[str] = set()
    excluded: set[str] = set()

    def reference(value: Any, where: str, destination: set[str]) -> None:
        if text(value, where):
            uses[value].append(where)
            destination.add(value)

    batch_summaries = []
    ids: set[str] = set()
    if fields(plan, {"version", "diocese", "first_batch", "batches", "excluded"}, "manifest"):
        if type(plan.get("version")) is not int or plan["version"] != 1:
            errors.append("manifest.version must be 1")
        if plan.get("diocese") != diocese:
            errors.append(f"manifest.diocese must be {diocese!r}")
        batches = plan.get("batches")
        if not isinstance(batches, list) or not batches:
            errors.append("manifest.batches must be a nonempty list")
        else:
            for index, batch in enumerate(batches, 1):
                where = f"batches[{index}]"
                if not fields(batch, {"id", "name", "why", "entries"}, where):
                    continue
                batch_id = batch.get("id")
                if text(batch_id, f"{where}.id"):
                    if batch_id in ids:
                        errors.append(f"{where}: duplicate batch id {batch_id!r}")
                    ids.add(batch_id)
                text(batch.get("name"), f"{where}.name")
                text(batch.get("why"), f"{where}.why")
                entries = batch.get("entries")
                if not isinstance(entries, list) or not entries:
                    errors.append(f"{where}.entries must be a nonempty list")
                else:
                    for position, ref in enumerate(entries, 1):
                        reference(ref, f"{where}.entries[{position}]", assigned)
                batch_summaries.append({"id": batch_id, "name": batch.get("name"),
                                        "entries": len(entries) if isinstance(entries, list) else 0})
        first = plan.get("first_batch")
        if not isinstance(first, str) or first not in ids:
            errors.append("manifest.first_batch must name an existing batch id")
        exclusions = plan.get("excluded")
        if not isinstance(exclusions, list):
            errors.append("manifest.excluded must be a list")
        else:
            for index, exclusion in enumerate(exclusions, 1):
                where = f"excluded[{index}]"
                if not fields(exclusion, {"ref", "reason"}, where):
                    continue
                reference(exclusion.get("ref"), f"{where}.ref", excluded)
                text(exclusion.get("reason"), f"{where}.reason")

    missing = sorted(expected - uses.keys())
    unknown = sorted(uses.keys() - expected)
    duplicates = {ref: locations for ref, locations in sorted(uses.items()) if len(locations) > 1}
    errors.extend(f"missing roster entry: {ref}" for ref in missing)
    errors.extend(f"unknown roster reference: {ref}" for ref in unknown)
    errors.extend(f"roster entry assigned more than once: {ref} ({', '.join(locations)})"
                  for ref, locations in duplicates.items())
    return {
        "diocese": diocese, "manifest": str(path), "passed": not errors, "errors": errors,
        "counts": {"roster_entries": len(expected), "assigned": len(assigned & expected),
                   "excluded": len(excluded & expected), "batches": len(batch_summaries)},
        "first_batch": plan.get("first_batch") if isinstance(plan, dict) else None,
        "batches": batch_summaries, "missing": missing, "unknown": unknown,
        "duplicates": duplicates,
    }
