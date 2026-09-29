"""Score classifier runs against the hand-made labels in data/labels/.

A label is ground truth for one bulletin (see `labels`); only labels marked
`done` are scored. Each classifier's run (data/runs/<name>/, as written by
`extract` or `bench`) is matched to the labels by parish and content hash, and
scored on the labeled bulletins it served.

Events are counted as found at four tiers, each adding fields to the last:

- `slot`: event type, day, start time and cancellation. A dated event counts
  as its weekday, so a weekly Sunday matches a dated Sunday.
- `kind`: also weekly vs dated, and the exact date of a dated event.
- `church`: also the church.
- `exact`: also the end time: every field a classifier emits but page and note.

Matching is by multiset, so two churches' Sunday 9 AM Masses are two events to
find. Events paired at the `slot` tier (one label row to one predicted row,
preferring the pairing that agrees on the most fields) are then checked field
by field: weekly vs dated, church, end time, page number and whether there is
a note.
"""

from __future__ import annotations

import json
import logging
import statistics
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

from pdf_extract.compare import (
    EVENT_TYPES,
    _format_event_line,
    _load_run,
    _prf,
    load_manifest,
    model_price,
    usage_cost,
)
from pdf_extract.labeling.bulletins import gemini_rows
from pdf_extract.labeling.labels import LABELS_DIR, validate_label
from pdf_extract.runner import RUNS_DIR
from pdf_extract.storage import utc_now_iso

LOGGER = logging.getLogger(__name__)

SCORE_DIR = RUNS_DIR / "labels"

TIERS = ("slot", "kind", "church", "exact")
# The tiers broken down per event type in the report.
TYPE_TIERS = ("slot", "kind")
ATTRIBUTES = ("weekly_vs_dated", "church", "end_time", "page_number", "note_presence")

BulletinKey = tuple[str, str]  # (parish slug, content hash)


# ── Labels ──────────────────────────────────────────────────────────────────
def load_truth(
    labels_dir: Path = LABELS_DIR, *, statuses: tuple[str, ...] = ("done",),
) -> dict[BulletinKey, dict[str, Any]]:
    """Every valid label with one of `statuses`, by (parish slug, content hash)."""
    truth: dict[BulletinKey, dict[str, Any]] = {}
    for path in sorted(labels_dir.glob("*/*.json")):
        try:
            label = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            LOGGER.warning("Skipping unreadable label %s", path)
            continue
        errors = validate_label(label)
        if errors:
            LOGGER.warning("Skipping invalid label %s: %s", path, "; ".join(errors[:3]))
            continue
        if label["status"] in statuses:
            truth[(label["parish_slug"], label["content_hash"])] = label
    return truth


# ── Matching ────────────────────────────────────────────────────────────────
def _weekday(ev: dict[str, Any]) -> str | None:
    if ev["event_kind"] == "weekly":
        return ev["day_of_week"]
    return date.fromisoformat(ev["date"]).strftime("%A") if ev["date"] else None


def tier_key(ev: dict[str, Any], tier: str) -> tuple[Any, ...]:
    """What must agree for an event to count as found at `tier`."""
    key: tuple[Any, ...] = (ev["event_type"], _weekday(ev), ev["start_time"], ev["cancelled"])
    if tier == "slot":
        return key
    key += (ev["event_kind"], ev["date"])
    if tier == "kind":
        return key
    key += (ev["church_slug"],)
    if tier == "church":
        return key
    return key + (ev["end_time"],)


def _found(predicted: list[dict[str, Any]], expected: list[dict[str, Any]], tier: str) -> int:
    got = Counter(tier_key(ev, tier) for ev in predicted)
    want = Counter(tier_key(ev, tier) for ev in expected)
    return sum((got & want).values())


def _attribute_checks(pred: dict[str, Any], truth: dict[str, Any]) -> dict[str, bool | None]:
    """Whether a paired prediction gets each field right (None: not scored)."""
    return {
        "weekly_vs_dated": (pred["event_kind"], pred["date"]) == (truth["event_kind"], truth["date"]),
        "church": pred["church_slug"] == truth["church_slug"],
        "end_time": pred["end_time"] == truth["end_time"],
        # A label without a page number cannot say whether the prediction's is right.
        "page_number": None if truth["page_number"] is None
        else pred["page_number"] == truth["page_number"],
        "note_presence": (pred["note"] is None) == (truth["note"] is None),
    }


def align(
    predicted: list[dict[str, Any]], expected: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Pair predicted with labeled events that match at the `slot` tier, one to one.

    Within a slot, the pairs that agree on the most fields are taken first
    (church weighs most), so two churches' 9 AM Masses pair with their own.
    """
    by_slot: dict[tuple[Any, ...], tuple[list[int], list[int]]] = defaultdict(lambda: ([], []))
    for i, ev in enumerate(predicted):
        by_slot[tier_key(ev, "slot")][0].append(i)
    for j, ev in enumerate(expected):
        by_slot[tier_key(ev, "slot")][1].append(j)
    weights = {"church": 8, "weekly_vs_dated": 4, "end_time": 2, "page_number": 1, "note_presence": 1}
    pairs = []
    for pred_ids, truth_ids in by_slot.values():
        scored = sorted(
            (
                (
                    -sum(w for field, w in weights.items()
                         if _attribute_checks(predicted[i], expected[j])[field]),
                    i, j,
                )
                for i in pred_ids for j in truth_ids
            ),
        )
        used_p: set[int] = set()
        used_t: set[int] = set()
        for _, i, j in scored:
            if i in used_p or j in used_t:
                continue
            used_p.add(i)
            used_t.add(j)
            pairs.append((predicted[i], expected[j]))
    return pairs


# ── Scoring ─────────────────────────────────────────────────────────────────
def _rate(correct: int, total: int) -> dict[str, Any]:
    return {"correct": correct, "total": total, "rate": round(correct / total, 4) if total else None}


def _bulletin_key(row: dict[str, Any]) -> BulletinKey | None:
    """(parish slug, content hash) of a run manifest row."""
    slug, content_hash = row.get("parish_slug"), row.get("content_hash")
    if not isinstance(content_hash, str) and isinstance(row.get("pdf_path"), str):
        # Manifests written before `content_hash` was: bulletins/<slug>/<hash>.pdf.
        content_hash = Path(row["pdf_path"]).stem
    if isinstance(slug, str) and isinstance(content_hash, str):
        return slug, content_hash
    return None


def score_classifier(name: str, truth: dict[BulletinKey, dict[str, Any]]) -> dict[str, Any]:
    """One classifier's run scored against the labels it served."""
    grouped, summary = _load_run(name)
    manifest = load_manifest(name)
    served: dict[BulletinKey, tuple[str, dict[str, Any]]] = {}
    for url, row in manifest.items():
        key = _bulletin_key(row)
        if key in truth:
            served[key] = (url, row)

    counts = {tier: {"tp": 0, "predicted": 0, "expected": 0} for tier in TIERS}
    by_type = {
        t: {tier: {"tp": 0, "predicted": 0, "expected": 0} for tier in TYPE_TIERS}
        for t in EVENT_TYPES
    }
    checks: dict[str, list[bool]] = {field: [] for field in ATTRIBUTES}
    notes = {"missed": 0, "extra": 0}
    matched = 0
    exact_bulletins = {tier: 0 for tier in TIERS}
    missed_entirely: list[str] = []
    dates: list[bool] = []
    per_bulletin: list[dict[str, Any]] = []

    for key in sorted(served):
        url, row = served[key]
        label = truth[key]
        predicted = gemini_rows(grouped.get(url, []))
        expected = label["events"]
        for tier in TIERS:
            found = _found(predicted, expected, tier)
            counts[tier]["tp"] += found
            counts[tier]["predicted"] += len(predicted)
            counts[tier]["expected"] += len(expected)
            exact_bulletins[tier] += found == len(predicted) == len(expected)
        for event_type in EVENT_TYPES:
            got = [ev for ev in predicted if ev["event_type"] == event_type]
            want = [ev for ev in expected if ev["event_type"] == event_type]
            for tier in TYPE_TIERS:
                by_type[event_type][tier]["tp"] += _found(got, want, tier)
                by_type[event_type][tier]["predicted"] += len(got)
                by_type[event_type][tier]["expected"] += len(want)
        if expected and not predicted:
            missed_entirely.append(key[0])
        if label["published_date"]:
            dates.append(row.get("published_date_extracted") == label["published_date"])

        pairs = align(predicted, expected)
        matched += len(pairs)
        mismatched = []
        for pred, want in pairs:
            result = _attribute_checks(pred, want)
            for field, ok in result.items():
                if ok is not None:
                    checks[field].append(ok)
            notes["missed"] += want["note"] is not None and pred["note"] is None
            notes["extra"] += want["note"] is None and pred["note"] is not None
            wrong = [field for field, ok in result.items() if ok is False]
            if wrong:
                mismatched.append({"label": want, "predicted": pred, "fields": wrong})
        paired_pred = {id(p) for p, _ in pairs}
        paired_truth = {id(t) for _, t in pairs}
        bulletin_slot = _prf(_found(predicted, expected, "slot"), len(predicted), len(expected))
        bulletin_exact = _prf(_found(predicted, expected, "exact"), len(predicted), len(expected))
        per_bulletin.append({
            "parish_slug": key[0],
            "content_hash": key[1],
            "bulletin_source_url": url,
            "label_events": len(expected),
            "events": len(predicted),
            "slot_f1": bulletin_slot["f1"] if expected or predicted else 1.0,
            "exact_f1": bulletin_exact["f1"] if expected or predicted else 1.0,
            "missed": [ev for ev in expected if id(ev) not in paired_truth],
            "extra": [ev for ev in predicted if id(ev) not in paired_pred],
            "mismatched": mismatched,
        })

    usage_rows = [row for _, row in served.values() if row.get("usage")]
    price = model_price(summary.get("classifier_version"))
    costs = [usage_cost(row["usage"], price) for row in usage_rows] if price else []
    llm_seconds = [
        row["timing"]["llm_seconds"] for _, row in served.values()
        if isinstance(row.get("timing"), dict) and "llm_seconds" in row["timing"]
    ]
    return {
        "classifier": name,
        "version": summary.get("classifier_version"),
        "bulletins_scored": len(served),
        "bulletins_not_served": sorted(slug for slug, _ in set(truth) - set(served)),
        "events": counts["slot"]["predicted"],
        "label_events": counts["slot"]["expected"],
        "tiers": {tier: {**c, **_prf(**c)} for tier, c in counts.items()},
        "by_event_type": {
            t: {tier: _prf(**c) for tier, c in tiers.items()} for t, tiers in by_type.items()
        },
        "matched_events": matched,
        "attributes": {field: _rate(sum(v), len(v)) for field, v in checks.items()},
        "notes_missed": notes["missed"],
        "notes_extra": notes["extra"],
        "bulletins_exact": exact_bulletins,
        "bulletins_missed_entirely": missed_entirely,
        "published_date": _rate(sum(dates), len(dates)),
        # Told today was the bulletin's Sunday (`bench --labels`); None: not recorded.
        "bulletins_as_of_sunday": (
            sum(bool(row["extracted_as_of"]) for _, row in served.values())
            if any("extracted_as_of" in row for _, row in served.values()) else None
        ),
        "cost_usd_per_bulletin": round(statistics.fmean(costs), 5) if costs else None,
        "llm_seconds_mean": round(statistics.fmean(llm_seconds), 3) if llm_seconds else None,
        "per_bulletin": sorted(per_bulletin, key=lambda b: (b["slot_f1"] or 0.0, b["parish_slug"])),
    }


def score_against_labels(
    classifier_names: list[str],
    *,
    labels_dir: Path = LABELS_DIR,
    bulletins: set[BulletinKey] | None = None,
    out_path: Path | None = None,
) -> dict[str, Any]:
    """Score each classifier's run against the `done` labels and write the report.

    `bulletins` limits scoring to those labeled bulletins (the benchmark's sample).
    """
    truth = load_truth(labels_dir)
    if bulletins is not None:
        truth = {key: label for key, label in truth.items() if key in bulletins}
    if not truth:
        raise ValueError(f"No labels marked done in {labels_dir}")
    report: dict[str, Any] = {
        "generated_at": utc_now_iso(),
        "labels_dir": str(labels_dir),
        "labels": len(truth),
        "label_events": sum(len(label["events"]) for label in truth.values()),
        "classifiers": classifier_names,
        "results": [score_classifier(name, truth) for name in classifier_names],
    }
    if out_path is None:
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        out_path = SCORE_DIR / f"labels_{ts}.json"
    markdown_path = out_path.with_suffix(".md")
    report["report_json"] = str(out_path)
    report["report_markdown"] = str(markdown_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_path.write_text(format_details_markdown(report) + "\n", encoding="utf-8")
    print(format_markdown(report))
    print(f"\nFull JSON report: {out_path}")
    print(f"Per-bulletin report: {markdown_path}")
    return report


# ── Report ──────────────────────────────────────────────────────────────────
def _f(value: float | None) -> str:
    return "–" if value is None else f"{value:.3f}"


def _pct(stat: dict[str, Any]) -> str:
    if stat["rate"] is None:
        return "–"
    return f"{stat['rate']:.1%} ({stat['correct']}/{stat['total']})"


def format_markdown(report: dict[str, Any]) -> str:
    rows = report["results"]
    lines = [
        f"## Against ground truth: {report['labels']} labeled bulletins, "
        f"{report['label_events']} events",
        "",
        "Events found, by what must match. *Slot*: type, day (a dated event counts as its "
        "weekday), start time, cancelled. *Kind*: also weekly vs dated and the date. "
        "*Church*: also the church. *Exact*: also the end time.",
        "",
        "| Classifier | Bulletins | Events (labels) "
        + "".join(f"| {t.capitalize()} P | {t.capitalize()} R | {t.capitalize()} F1 " for t in TIERS)
        + "|",
        "|---|---:|---:" + "|---:" * 3 * len(TIERS) + "|",
    ]
    for r in rows:
        cells = "".join(
            f"| {_f(r['tiers'][t]['precision'])} | {_f(r['tiers'][t]['recall'])} "
            f"| **{_f(r['tiers'][t]['f1'])}** "
            for t in TIERS
        )
        lines.append(
            f"| {r['classifier']} | {r['bulletins_scored']}/{report['labels']} "
            f"| {r['events']} ({r['label_events']}) {cells}|"
        )

    lines.extend([
        "",
        "### By event type (precision / recall)",
        "",
        "| Classifier " + "".join(
            f"| {t.capitalize()} slot | {t.capitalize()} kind " for t in EVENT_TYPES
        ) + "|",
        "|---" + "|---:" * 2 * len(EVENT_TYPES) + "|",
    ])
    for r in rows:
        cells = "".join(
            f"| {_f(r['by_event_type'][t][tier]['precision'])} / "
            f"{_f(r['by_event_type'][t][tier]['recall'])} "
            for t in EVENT_TYPES for tier in TYPE_TIERS
        )
        lines.append(f"| {r['classifier']} {cells}|")

    lines.extend([
        "",
        "### Fields of matched events",
        "",
        "Of the events matched at the slot tier, how many get each field right. Page "
        "counts only events whose label has a page; note is whether there is one.",
        "",
        "| Classifier | Matched | Weekly vs dated | Church | End time | Page | Note there or not "
        "| Notes missed | Notes extra |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for r in rows:
        a = r["attributes"]
        lines.append(
            f"| {r['classifier']} | {r['matched_events']} "
            + "".join(f"| {_pct(a[field])} " for field in ATTRIBUTES)
            + f"| {r['notes_missed']} | {r['notes_extra']} |"
        )

    lines.extend([
        "",
        "### Bulletins",
        "",
        "| Classifier | All events found (slot) | All events exact | Missed entirely "
        "| Published date | Told its Sunday | $/bulletin | LLM s |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ])
    for r in rows:
        cost = r["cost_usd_per_bulletin"]
        as_of = r["bulletins_as_of_sunday"]
        told = "–" if as_of is None else f"{as_of}/{r['bulletins_scored']}"
        lines.append(
            f"| {r['classifier']} | {r['bulletins_exact']['slot']}/{r['bulletins_scored']} "
            f"| {r['bulletins_exact']['exact']}/{r['bulletins_scored']} "
            f"| {len(r['bulletins_missed_entirely'])} | {_pct(r['published_date'])} "
            f"| {told} "
            f"| {'–' if cost is None else f'${cost:.5f}'} | {_f(r['llm_seconds_mean'])} |"
        )
    if any(r["bulletins_as_of_sunday"] not in (None, r["bulletins_scored"]) for r in rows):
        lines.extend(["", "*Told its Sunday*: results extracted with today set to the Sunday "
                      "the bulletin is dated to; the rest were extracted the day they ran "
                      "(production Gemini: the week the bulletin was fetched)."])
    partial = [r for r in rows if r["bulletins_not_served"]]
    if partial:
        lines.extend(["", "Scored only on the labeled bulletins each classifier served; missing: "
                      + "; ".join(
                          f"{r['classifier']} ({', '.join(r['bulletins_not_served'])})"
                          for r in partial
                      ) + "."])
    return "\n".join(lines)


def format_details_markdown(report: dict[str, Any]) -> str:
    lines = ["# Classifiers against ground truth", "", format_markdown(report), "",
             "## Per bulletin", ""]
    for r in report["results"]:
        lines.extend([f"### {r['classifier']}", ""])
        for b in r["per_bulletin"]:
            lines.append(
                f"#### {b['parish_slug']}: slot F1 {_f(b['slot_f1'])}, exact F1 "
                f"{_f(b['exact_f1'])} ({b['events']} events, {b['label_events']} labeled)"
            )
            lines.append(f"- Source URL: {b['bulletin_source_url']}")
            for title, events in (("Missed", b["missed"]), ("Extra", b["extra"])):
                if events:
                    lines.append(f"- **{title}**")
                    lines.extend(f"  - {_format_event_line(ev)}" for ev in events)
            if b["mismatched"]:
                lines.append("- **Wrong fields**")
                for m in b["mismatched"]:
                    lines.append(f"  - {', '.join(m['fields'])}")
                    lines.append(f"    - label: {_format_event_line(m['label'])}")
                    lines.append(f"    - got:   {_format_event_line(m['predicted'])}")
            lines.append("")
    return "\n".join(lines).rstrip()
