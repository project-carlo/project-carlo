"""Pairwise agreement metrics over experimental classifier runs.

Reads data/runs/<name>/events.json for each requested classifier and computes
exact-tuple-match agreement, broken down per-bulletin and aggregated. Also
surfaces per-classifier latency and cache stats from data/runs/<name>/run.json,
and token usage and list-price cost from data/runs/<name>/bulletins.json.

The match-key extraction is exposed as `event_key()` so the same matcher can
score against ground truth once labels exist.
"""

from __future__ import annotations

import itertools
import json
import logging
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import bulletin_pdf_key
from pdf_extract.extract_run import bulletins_path, events_path, run_summary_path
from pdf_extract.paths import DATA_DIR
from pdf_extract.pricing import price_for, summarize_usage
from pdf_extract.runner import RUNS_DIR
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db, load_bulletins, utc_now_iso

LOGGER = logging.getLogger(__name__)

COMPARE_DIR = RUNS_DIR / "compare"

EventKey = tuple[str, str, str, str | None, str | None, str, str | None, bool]
EventsByBulletin = dict[str, list[dict[str, Any]]]
EventKeysByBulletin = dict[str, set[EventKey]]
ManifestByBulletin = dict[str, dict[str, Any]]


def event_key(event: dict[str, Any]) -> EventKey:
    """Exact-match identity for an event row.

    Two events from different classifiers are considered to agree iff their
    `event_key()` tuples are equal. Notes and page numbers are excluded — they
    are commentary, not identity.
    """
    return (
        str(event.get("church_slug", "")),
        str(event.get("event_type", "")),
        str(event.get("event_kind", "")),
        event.get("day_of_week") if isinstance(event.get("day_of_week"), str) else None,
        event.get("date") if isinstance(event.get("date"), str) else None,
        str(event.get("start_time", "")),
        event.get("end_time") if isinstance(event.get("end_time"), str) else None,
        bool(event.get("cancelled", False)),
    )


def _load_run(
    classifier_name: str,
) -> tuple[EventsByBulletin, dict[str, Any], ManifestByBulletin]:
    """Return (events by bulletin_source_url, run.json summary, bulletins.json rows by URL)."""
    ev_path = events_path(classifier_name)
    if not ev_path.exists():
        raise FileNotFoundError(
            f"No events.json for classifier {classifier_name!r} at {ev_path}. "
            f"Run `pnpm extract --classifier {classifier_name}` first."
        )
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    manifest_rows: ManifestByBulletin = {}

    manifest_path = bulletins_path(classifier_name)
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            LOGGER.warning("Could not parse %s; ignoring", manifest_path, exc_info=True)
        else:
            for row in manifest:
                if not isinstance(row, dict):
                    continue
                url = row.get("bulletin_source_url") or row.get("source_url")
                if isinstance(url, str):
                    grouped.setdefault(url, [])
                    manifest_rows[url] = row

    rows = json.loads(ev_path.read_text(encoding="utf-8"))
    for row in rows:
        if not isinstance(row, dict):
            continue
        url = row.get("bulletin_source_url")
        if not isinstance(url, str):
            continue
        grouped[url].append(row)

    summary_path = run_summary_path(classifier_name)
    summary: dict[str, Any] = {}
    if summary_path.exists():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            LOGGER.warning("Could not parse %s; ignoring", summary_path, exc_info=True)

    return grouped, summary, manifest_rows


def _load_bulletin_metadata() -> dict[str, dict[str, Any]]:
    """Return selected bulletin fields keyed by bulletin source URL."""
    metadata: dict[str, dict[str, Any]] = {}
    if not DEFAULT_DB_PATH.exists():
        return metadata
    conn = connect_db()
    try:
        bulletins = load_bulletins(conn)
    finally:
        conn.close()
    for entry in bulletins:
        source_url = entry["source_url"]
        content_hash = entry.get("content_hash")
        metadata[source_url] = {
            "bulletin_source_url": source_url,
            "pdf_path": (
                (DATA_DIR / bulletin_pdf_key(entry["parish_slug"], content_hash)).as_posix()
                if content_hash
                else None
            ),
            "parish_slug": entry["parish_slug"],
            "published_date": entry.get("published_date"),
        }
    return metadata


def _event_keys_by_bulletin(grouped: EventsByBulletin) -> EventKeysByBulletin:
    return {url: {event_key(row) for row in rows} for url, rows in grouped.items()}


def _events_by_key(rows: list[dict[str, Any]]) -> dict[EventKey, dict[str, Any]]:
    keyed: dict[EventKey, dict[str, Any]] = {}
    for row in rows:
        keyed.setdefault(event_key(row), row)
    return keyed


def _sortable_event_key(key: EventKey) -> tuple[str, ...]:
    return tuple("" if part is None else str(part) for part in key)


def _event_for_report(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "church_slug": event.get("church_slug"),
        "event_type": event.get("event_type"),
        "event_kind": event.get("event_kind"),
        "day_of_week": event.get("day_of_week"),
        "date": event.get("date"),
        "start_time": event.get("start_time"),
        "end_time": event.get("end_time"),
        "cancelled": event.get("cancelled", False),
        "page_number": event.get("page_number"),
        "note": event.get("note"),
    }


def _pairwise_metrics(
    name_a: str,
    grouped_a: EventsByBulletin,
    name_b: str,
    grouped_b: EventsByBulletin,
    metadata: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    keys_a = _event_keys_by_bulletin(grouped_a)
    keys_b = _event_keys_by_bulletin(grouped_b)

    common_urls = sorted(set(keys_a) & set(keys_b))
    only_a_urls = sorted(set(keys_a) - set(keys_b))
    only_b_urls = sorted(set(keys_b) - set(keys_a))

    total_intersect = 0
    total_union = 0
    total_a = 0
    total_b = 0
    per_bulletin_jaccards: list[float] = []
    one_sided_zero: list[dict[str, Any]] = []  # one classifier returned 0 events

    for url in common_urls:
        a_set = keys_a[url]
        b_set = keys_b[url]
        intersect = len(a_set & b_set)
        union = len(a_set | b_set)
        total_intersect += intersect
        total_union += union
        total_a += len(a_set)
        total_b += len(b_set)
        if union:
            per_bulletin_jaccards.append(intersect / union)
        else:
            per_bulletin_jaccards.append(1.0)  # both empty: agree trivially
        if (len(a_set) == 0) != (len(b_set) == 0):
            one_sided_zero.append(
                {
                    "bulletin_source_url": url,
                    f"{name_a}_event_count": len(a_set),
                    f"{name_b}_event_count": len(b_set),
                }
            )

    micro_jaccard = (total_intersect / total_union) if total_union else None
    mean_jaccard = (
        round(statistics.fmean(per_bulletin_jaccards), 4) if per_bulletin_jaccards else None
    )
    median_jaccard = (
        round(statistics.median(per_bulletin_jaccards), 4) if per_bulletin_jaccards else None
    )

    return {
        "classifier_a": name_a,
        "classifier_b": name_b,
        "bulletins_in_both": len(common_urls),
        "bulletins_only_in_a": len(only_a_urls),
        "bulletins_only_in_b": len(only_b_urls),
        f"events_total_{name_a}": total_a,
        f"events_total_{name_b}": total_b,
        "events_in_both": total_intersect,
        "events_in_union": total_union,
        "micro_jaccard": round(micro_jaccard, 4) if micro_jaccard is not None else None,
        "mean_jaccard": mean_jaccard,
        "median_jaccard": median_jaccard,
        "one_sided_zero_event_bulletins": one_sided_zero,
        "per_bulletin": _pairwise_bulletin_details(
            name_a,
            grouped_a,
            name_b,
            grouped_b,
            metadata,
        ),
    }


def _pairwise_bulletin_details(
    name_a: str,
    grouped_a: EventsByBulletin,
    name_b: str,
    grouped_b: EventsByBulletin,
    metadata: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    details: list[dict[str, Any]] = []
    for url in sorted(set(grouped_a) | set(grouped_b)):
        a_rows = grouped_a.get(url, [])
        b_rows = grouped_b.get(url, [])
        a_by_key = _events_by_key(a_rows)
        b_by_key = _events_by_key(b_rows)
        a_keys = set(a_by_key)
        b_keys = set(b_by_key)
        same_keys = sorted(a_keys & b_keys, key=_sortable_event_key)
        only_a_keys = sorted(a_keys - b_keys, key=_sortable_event_key)
        only_b_keys = sorted(b_keys - a_keys, key=_sortable_event_key)
        union_count = len(a_keys | b_keys)
        jaccard = (len(same_keys) / union_count) if union_count else 1.0

        info = metadata.get(url, {"bulletin_source_url": url})
        details.append(
            {
                "bulletin_source_url": url,
                "pdf_path": info.get("pdf_path"),
                "parish_slug": info.get("parish_slug"),
                "published_date": info.get("published_date"),
                f"{name_a}_event_count": len(a_keys),
                f"{name_b}_event_count": len(b_keys),
                "same_count": len(same_keys),
                f"only_in_{name_a}_count": len(only_a_keys),
                f"only_in_{name_b}_count": len(only_b_keys),
                "jaccard": round(jaccard, 4),
                "same": [
                    {
                        name_a: _event_for_report(a_by_key[key]),
                        name_b: _event_for_report(b_by_key[key]),
                    }
                    for key in same_keys
                ],
                f"only_in_{name_a}": [_event_for_report(a_by_key[key]) for key in only_a_keys],
                f"only_in_{name_b}": [_event_for_report(b_by_key[key]) for key in only_b_keys],
            }
        )

    return sorted(
        details,
        key=lambda d: (
            str(d.get("parish_slug") or ""),
            str(d.get("published_date") or ""),
            str(d.get("bulletin_source_url") or ""),
        ),
    )


def _usage_over(
    manifest: ManifestByBulletin, summary: dict[str, Any], urls: list[str] | None = None,
) -> dict[str, Any]:
    """Usage and list-price cost over a run's bulletins (all of them, or `urls`)."""
    rows = manifest.values() if urls is None else [manifest[u] for u in urls if u in manifest]
    usages = [row.get("usage") if isinstance(row.get("usage"), dict) else None for row in rows]
    usage = summarize_usage(usages, price_for(summary.get("model")))
    priced = usage["results_with_usage"]
    cost = usage["cost_usd"]
    usage["cost_per_bulletin_usd"] = (
        round(cost / priced, 6) if cost is not None and priced else None
    )
    usage["api_cache_hit_rate"] = (
        round(usage["cached_prompt_tokens"] / usage["prompt_tokens"], 4)
        if usage["prompt_tokens"]
        else None
    )
    return usage


def _classifier_stats(
    name: str, grouped: EventsByBulletin, summary: dict[str, Any], manifest: ManifestByBulletin,
) -> dict[str, Any]:
    counts = [len(s) for s in _event_keys_by_bulletin(grouped).values()]
    hits = summary.get("cache_hits") or 0
    misses = summary.get("cache_misses") or 0
    return {
        "classifier": name,
        "version": summary.get("classifier_version"),
        "bulletins": len(grouped),
        "events_total": sum(counts),
        "events_per_bulletin_mean": round(statistics.fmean(counts), 2) if counts else 0.0,
        "events_per_bulletin_median": statistics.median(counts) if counts else 0,
        "events_per_bulletin_max": max(counts) if counts else 0,
        "cache_hits": summary.get("cache_hits"),
        "cache_misses": summary.get("cache_misses"),
        "cache_hit_rate": round(hits / (hits + misses), 4) if hits + misses else None,
        "wall_seconds": summary.get("wall_seconds"),
        "errors": len(summary.get("errors") or []),
        "model": summary.get("model"),
        "usage": _usage_over(manifest, summary),
        "paid_this_run_usd": (summary.get("usage_this_run") or {}).get("cost_usd"),
    }


def _pairwise_cost(
    name_a: str, run_a: tuple, name_b: str, run_b: tuple,
) -> dict[str, Any]:
    """Each side's cost over the bulletins both classifiers have usage for."""
    _, summary_a, manifest_a = run_a
    _, summary_b, manifest_b = run_b

    def priced(manifest: ManifestByBulletin) -> set[str]:
        return {u for u, row in manifest.items() if isinstance(row.get("usage"), dict)}

    shared = sorted(priced(manifest_a) & priced(manifest_b))
    usage_a = _usage_over(manifest_a, summary_a, shared)
    usage_b = _usage_over(manifest_b, summary_b, shared)
    cost_a = usage_a["cost_usd"]
    cost_b = usage_b["cost_usd"]
    return {
        "bulletins_priced_in_both": len(shared),
        name_a: usage_a,
        name_b: usage_b,
        "cost_ratio_b_over_a": round(cost_b / cost_a, 4) if cost_a and cost_b is not None else None,
    }


def compare(
    classifier_names: list[str],
    *,
    out_path: Path | None = None,
) -> dict[str, Any]:
    """Compute pairwise metrics across N classifier runs."""
    if len(classifier_names) < 2:
        raise ValueError("Need at least two classifiers to compare")

    runs = {name: _load_run(name) for name in classifier_names}
    metadata = _load_bulletin_metadata()

    per_classifier = [
        _classifier_stats(name, grouped, summary, manifest)
        for name, (grouped, summary, manifest) in runs.items()
    ]

    pairwise = [
        _pairwise_metrics(a, runs[a][0], b, runs[b][0], metadata)
        | {"cost": _pairwise_cost(a, runs[a], b, runs[b])}
        for a, b in itertools.combinations(classifier_names, 2)
    ]

    report = {
        "generated_at": utc_now_iso(),
        "classifiers": classifier_names,
        "per_classifier": per_classifier,
        "pairwise": pairwise,
    }

    if out_path is None:
        COMPARE_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        out_path = COMPARE_DIR / f"compare_{ts}.json"
    markdown_path = out_path.with_suffix(".md")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    report["markdown_report_path"] = str(markdown_path)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(
        format_side_by_side_markdown(report) + "\n",
        encoding="utf-8",
    )
    print(format_markdown(report))
    print(f"\nFull JSON report: {out_path}")
    print(f"Side-by-side report: {markdown_path}")

    return report


def format_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("## Per-classifier")
    lines.append("")
    lines.append(
        "| Classifier | Version | Bulletins | Events | Mean/bulletin | Cache hits/misses | Wall (s) | Errors |"
    )
    lines.append("|---|---|---:|---:|---:|---|---:|---:|")
    for c in report["per_classifier"]:
        cache = f"{c.get('cache_hits') or 0}/{c.get('cache_misses') or 0}"
        lines.append(
            f"| {c['classifier']} | {c.get('version') or ''} | {c['bulletins']} | {c['events_total']} | "
            f"{c['events_per_bulletin_mean']} | {cache} | {c.get('wall_seconds') or ''} | {c['errors']} |"
        )

    lines.append("")
    lines.append("## Pairwise agreement (exact tuple match)")
    lines.append("")
    lines.append(
        "| A | B | Bulletins shared | Events ∩ | Events ∪ | Micro-Jaccard | Mean Jaccard | One-sided-zero |"
    )
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for p in report["pairwise"]:
        lines.append(
            f"| {p['classifier_a']} | {p['classifier_b']} | {p['bulletins_in_both']} | "
            f"{p['events_in_both']} | {p['events_in_union']} | "
            f"{p['micro_jaccard']} | {p['mean_jaccard']} | {len(p['one_sided_zero_event_bulletins'])} |"
        )

    lines.extend(format_cost_markdown(report))
    return "\n".join(lines)


def _usd(value: float | None, usage: dict[str, Any]) -> str:
    """A dollar amount, marked as a lower bound when some results lack thinking tokens."""
    if value is None:
        return "n/a"
    floor = "≥" if usage.get("results_missing_thinking_tokens") else ""
    return f"{floor}${value:.4f}"


def _pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1%}"


def format_cost_markdown(report: dict[str, Any]) -> list[str]:
    lines = [
        "",
        "## Cost and cache (list price, all served bulletins)",
        "",
        "| Classifier | Model | Result-cache hits/misses | Result-cache hit rate | "
        "Bulletins priced | Input tok | API prompt-cache hit rate | Output tok | Thinking tok | "
        "Total | Per bulletin | Paid this run |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    lower_bound = []
    for c in report["per_classifier"]:
        u = c.get("usage") or {}
        if u.get("results_missing_thinking_tokens"):
            lower_bound.append(f"{c['classifier']} ({u['results_missing_thinking_tokens']})")
        paid = c.get("paid_this_run_usd")
        lines.append(
            f"| {c['classifier']} | {c.get('model') or ''} | "
            f"{c.get('cache_hits') or 0}/{c.get('cache_misses') or 0} | "
            f"{_pct(c.get('cache_hit_rate'))} | "
            f"{u.get('results_with_usage', 0)}/{c['bulletins']} | {u.get('prompt_tokens', 0):,} | "
            f"{_pct(u.get('api_cache_hit_rate'))} | {u.get('output_tokens', 0):,} | "
            f"{u.get('thinking_tokens', 0):,} | {_usd(u.get('cost_usd'), u)} | "
            f"{_usd(u.get('cost_per_bulletin_usd'), u)} | "
            f"{'n/a' if paid is None else f'${paid:.4f}'} |"
        )

    lines.extend([
        "",
        "## Cost head-to-head (bulletins priced for both)",
        "",
        "| A | B | Bulletins | A total | B total | A per bulletin | B per bulletin | B / A |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ])
    for p in report["pairwise"]:
        cost = p.get("cost") or {}
        a = cost.get(p["classifier_a"]) or {}
        b = cost.get(p["classifier_b"]) or {}
        ratio = cost.get("cost_ratio_b_over_a")
        lines.append(
            f"| {p['classifier_a']} | {p['classifier_b']} | "
            f"{cost.get('bulletins_priced_in_both', 0)} | "
            f"{_usd(a.get('cost_usd'), a)} | {_usd(b.get('cost_usd'), b)} | "
            f"{_usd(a.get('cost_per_bulletin_usd'), a)} | "
            f"{_usd(b.get('cost_per_bulletin_usd'), b)} | "
            f"{'n/a' if ratio is None else f'{ratio:.2f}x'} |"
        )

    if lower_bound:
        lines.extend([
            "",
            "≥: some cached results were recorded before thinking tokens were, so their "
            "thinking (billed as output) is missing from the cost: " + ", ".join(lower_bound) + ".",
        ])
    return lines


def format_side_by_side_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Classifier Compare",
        "",
        format_markdown(report),
        "",
        "## Per-bulletin side-by-side",
    ]

    for pair in report["pairwise"]:
        name_a = pair["classifier_a"]
        name_b = pair["classifier_b"]
        lines.extend(["", f"### {name_a} vs {name_b}"])
        for bulletin in pair.get("per_bulletin", []):
            lines.extend(_format_bulletin_detail(bulletin, name_a, name_b))

    return "\n".join(lines)


def _format_bulletin_detail(
    bulletin: dict[str, Any],
    name_a: str,
    name_b: str,
) -> list[str]:
    title_bits = [
        str(value)
        for value in (bulletin.get("parish_slug"), bulletin.get("published_date"))
        if value
    ]
    title = " - ".join(title_bits) or str(bulletin.get("bulletin_source_url") or "Bulletin")
    lines = ["", f"#### {title}"]
    if bulletin.get("bulletin_source_url"):
        lines.append(f"- Source URL: {bulletin['bulletin_source_url']}")
    if bulletin.get("pdf_path"):
        lines.append(f"- Source PDF: `{bulletin['pdf_path']}`")
    lines.append(
        f"- Counts: same {bulletin['same_count']}, "
        f"only {name_a} {bulletin[f'only_in_{name_a}_count']}, "
        f"only {name_b} {bulletin[f'only_in_{name_b}_count']}, "
        f"Jaccard {bulletin['jaccard']}"
    )

    lines.extend(["", "**Same**"])
    same = bulletin.get("same") or []
    if same:
        for item in same:
            lines.append(f"- {_format_event_line(item[name_a])}")
    else:
        lines.append("- None")

    for name in (name_a, name_b):
        lines.extend(["", f"**Only {name}**"])
        rows = bulletin.get(f"only_in_{name}") or []
        if rows:
            for row in rows:
                lines.append(f"- {_format_event_line(row)}")
        else:
            lines.append("- None")

    return lines


def _format_event_line(event: dict[str, Any]) -> str:
    type_bits = [
        str(value) for value in (event.get("event_type"), event.get("event_kind")) if value
    ]
    when = event.get("date") or event.get("day_of_week") or ""
    time_bits = [str(event.get("start_time") or "")]
    if event.get("end_time"):
        time_bits.append(str(event["end_time"]))
    parts = [
        str(event.get("church_slug") or ""),
        " ".join(type_bits),
        str(when),
        "-".join(part for part in time_bits if part),
    ]
    if event.get("cancelled"):
        parts.append("cancelled")
    if event.get("page_number") is not None:
        parts.append(f"page {event['page_number']}")
    if event.get("note"):
        parts.append(str(event["note"]))
    return " | ".join(part for part in parts if part)
