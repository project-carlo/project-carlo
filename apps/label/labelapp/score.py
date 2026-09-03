"""Scores classifier runs against human ground truth.

`pdf_extract.compare` measures how much two classifiers agree; this measures
whether either of them is right. Both use the same `event_key`, so a run scored
here and compared there are talking about the same events.

Only bulletins labeled `complete` count towards precision and recall: a
partially labeled bulletin cannot tell you what a model *missed*, because the
labeler has not yet asserted that the accepted set is exhaustive. Partial work
is not wasted, though — it still scores precision over the candidates that were
ruled on, reported separately as `decided_only`.

Beyond the headline numbers, mismatches are attributed to a logical field: a
false positive one field away from a false negative is the model reading a real
event slightly wrong, which is a different problem from inventing one.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from pdf_extract.compare import EventKey, event_key
from pdf_extract.runner import RUNS_DIR
from pdf_extract.storage import utc_now_iso

from labelapp import corpus, events as ev, store

SCORE_DIR = RUNS_DIR / "score"


def _f1(precision: float | None, recall: float | None) -> float | None:
    if precision is None or recall is None or precision + recall == 0:
        return None
    return round(2 * precision * recall / (precision + recall), 4)


def _ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 4) if denominator else None


def _event_from_key(key: EventKey) -> dict[str, Any]:
    """Rebuild a displayable event dict from its identity tuple."""
    church, event_type, kind, day_of_week, date_value, start, end, cancelled = key
    return {
        "church_slug": church,
        "event_type": event_type,
        "event_kind": kind,
        "day_of_week": day_of_week,
        "date": date_value,
        "start_time": start,
        "end_time": end,
        "cancelled": cancelled,
    }


def attribute_errors(
    false_positives: list[EventKey],
    false_negatives: list[EventKey],
) -> dict[str, Any]:
    """Pair near-miss errors and name the field each one turns on.

    A false positive that sits one logical field from a false negative is the
    same slot read wrong, not an invented one; pairing them greedily keeps the
    `spurious` and `missed` buckets for genuine additions and omissions.
    """
    unmatched_fp = [_event_from_key(key) for key in false_positives]
    unmatched_fn = [_event_from_key(key) for key in false_negatives]
    by_field: Counter[str] = Counter()
    pairs: list[dict[str, Any]] = []

    remaining_fp = list(unmatched_fp)
    remaining_fn = []
    for truth in unmatched_fn:
        match = next(
            (
                candidate
                for candidate in remaining_fp
                if len(ev.differing_fields(candidate, truth)) == 1
            ),
            None,
        )
        if match is None:
            remaining_fn.append(truth)
            continue
        remaining_fp.remove(match)
        field_name = ev.differing_fields(match, truth)[0]
        by_field[field_name] += 1
        pairs.append(
            {
                "field": field_name,
                "field_label": ev.FIELD_LABELS.get(field_name, field_name),
                "predicted": ev.describe_event(match),
                "truth": ev.describe_event(truth),
            }
        )

    return {
        "near_misses": pairs,
        "near_miss_by_field": dict(by_field.most_common()),
        "spurious": [ev.describe_event(row) for row in remaining_fp],
        "missed": [ev.describe_event(row) for row in remaining_fn],
    }


def score_run(
    run: corpus.Run,
    labels: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Precision, recall and error attribution for one run."""
    per_bulletin: list[dict[str, Any]] = []
    true_positives = total_fp = total_fn = 0
    decided_hits = decided_total = 0
    all_fp: list[EventKey] = []
    all_fn: list[EventKey] = []
    partial_bulletins = 0

    for source_url, label in sorted(labels.items()):
        if source_url not in run.covered:
            continue
        predicted = {
            event_key(row) for row in run.events_by_bulletin.get(source_url, [])
        }
        accepted = store.accepted_keys(label)
        rejected = {event_key(row) for row in label.get("rejected") or []}

        # Partial labels still score precision over candidates that were ruled on.
        ruled_on = predicted & (accepted | rejected)
        decided_hits += len(predicted & accepted)
        decided_total += len(ruled_on)

        if label.get("status") != store.STATUS_COMPLETE:
            if ruled_on:
                partial_bulletins += 1
            continue

        hits = predicted & accepted
        misses = accepted - predicted
        extras = predicted - accepted
        true_positives += len(hits)
        total_fn += len(misses)
        total_fp += len(extras)
        all_fp.extend(extras)
        all_fn.extend(misses)

        precision = _ratio(len(hits), len(predicted))
        recall = _ratio(len(hits), len(accepted))
        per_bulletin.append(
            {
                "bulletin_source_url": source_url,
                "parish_slug": label.get("parish_slug"),
                "predicted": len(predicted),
                "truth": len(accepted),
                "true_positives": len(hits),
                "false_positives": len(extras),
                "false_negatives": len(misses),
                "precision": precision,
                "recall": recall,
                "f1": _f1(precision, recall),
                "errors": attribute_errors(sorted(extras), sorted(misses)),
            }
        )

    precision = _ratio(true_positives, true_positives + total_fp)
    recall = _ratio(true_positives, true_positives + total_fn)
    return {
        "classifier": run.name,
        "version": run.version,
        "scored_bulletins": len(per_bulletin),
        "partial_bulletins": partial_bulletins,
        "true_positives": true_positives,
        "false_positives": total_fp,
        "false_negatives": total_fn,
        "precision": precision,
        "recall": recall,
        "f1": _f1(precision, recall),
        "decided_only": {
            "candidates_ruled_on": decided_total,
            "accepted": decided_hits,
            "precision": _ratio(decided_hits, decided_total),
        },
        "error_attribution": attribute_errors(all_fp, all_fn),
        "per_bulletin": per_bulletin,
    }


def score(
    run_names: list[str],
    *,
    out_path: Path | None = None,
) -> dict[str, Any]:
    """Score one or more runs against `data/labels.json` and write a report."""
    labels = store.load_labels()
    if not labels:
        raise ValueError(
            f"No labels found at {store.LABELS_PATH}. "
            "Label some bulletins first: `pnpm label`."
        )

    runs = corpus.load_runs(run_names)
    report = {
        "generated_at": utc_now_iso(),
        "labels_path": str(store.LABELS_PATH),
        "labeled_bulletins": len(labels),
        "complete_bulletins": sum(
            1 for label in labels.values() if label.get("status") == store.STATUS_COMPLETE
        ),
        "runs": [score_run(runs[name], labels) for name in run_names],
    }

    if out_path is None:
        SCORE_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        out_path = SCORE_DIR / f"score_{stamp}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    report["report_path"] = str(out_path)
    return report


def format_markdown(report: dict[str, Any]) -> str:
    """Terminal summary: headline metrics, then what each run gets wrong."""
    lines = [
        f"Ground truth: {report['complete_bulletins']} complete "
        f"of {report['labeled_bulletins']} labeled bulletins",
        "",
        "| Classifier | Bulletins | TP | FP | FN | Precision | Recall | F1 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for run in report["runs"]:
        lines.append(
            f"| {run['classifier']} | {run['scored_bulletins']} | {run['true_positives']} | "
            f"{run['false_positives']} | {run['false_negatives']} | "
            f"{_fmt(run['precision'])} | {_fmt(run['recall'])} | {_fmt(run['f1'])} |"
        )

    for run in report["runs"]:
        attribution = run["error_attribution"]
        lines.extend(["", f"### {run['classifier']} errors"])
        by_field = attribution["near_miss_by_field"]
        if by_field:
            lines.append("Near misses (right slot, one field wrong):")
            for name, count in by_field.items():
                lines.append(f"  - {ev.FIELD_LABELS.get(name, name)}: {count}")
        lines.append(f"Invented events: {len(attribution['spurious'])}")
        lines.append(f"Missed events: {len(attribution['missed'])}")
        decided = run["decided_only"]
        if decided["candidates_ruled_on"]:
            lines.append(
                f"Precision over all candidates ruled on (includes partly labeled "
                f"bulletins): {_fmt(decided['precision'])} "
                f"({decided['accepted']}/{decided['candidates_ruled_on']})"
            )
    return "\n".join(lines)


def _fmt(value: float | None) -> str:
    return "—" if value is None else f"{value:.3f}"
