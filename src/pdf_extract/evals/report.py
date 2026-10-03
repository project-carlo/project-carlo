"""Score one eval run against the ground-truth labels: `python -m pdf_extract eval report`.

Reads the predictions `eval run` wrote under `data/runs/<classifier>/eval/<version>/`
and the matching labels in `data/labels/` (by default those marked done; skipped
labels are never scored), and writes `report.md` and `report.json` next to the
predictions.

Within each bulletin every label event is paired with at most one predicted event,
in tiers from strictest to loosest; a pair made in one tier is out of the running
for the next. The tiers, in the order they are tried:

- `exact`: church, type, kind, weekday or date, start time, cancelled, end time,
  `weeks_of_month` and `season` all agree (notes and page numbers are ignored).
- `core`: the first six agree; end time or a recurrence qualifier differs.
- `weekly_vs_dated`: weekly on one side and dated on the other, on the same weekday,
  with church, type, start time and cancelled agreeing.
- `wrong_church`: everything in `core` but the church.
- `wrong_type`: everything in `core` but the event type.
- `wrong_time`: church, type, kind, weekday or date and cancelled agree; the start
  time differs (by any amount; the closest time pairs first).

`exact`, `core`, `weekly_vs_dated` and `wrong_time` count as found, at four levels:
strict (`exact`), core (+ `core`), loose (+ `weekly_vs_dated`) and any_time (+
`wrong_time`), so a wrong start time only counts at the last. `wrong_church` and
`wrong_type` never count as found: they are reported on their own so it is clear
how often the classifier saw the event but put it at the wrong church or called it
the wrong thing, and they are tried before `wrong_time` because a pair that agrees
on everything but the church is likelier the same event than one at another hour.
A label event left unpaired is missed; a prediction left unpaired is spurious.
"""

from __future__ import annotations

import json
import logging
import statistics
from collections import Counter
from collections.abc import Callable, Iterable
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.classifiers import get_classifier
from pdf_extract.evals.run import DEFAULT_STATUSES, version_dir_name
from pdf_extract.labeling.labels import DAYS, LABELS_DIR, is_valid_hash, is_valid_slug
from pdf_extract.runner import run_dir
from pdf_extract.storage import utc_now_iso
from pdf_extract.timeparse import time_to_minutes

LOGGER = logging.getLogger(__name__)

# Matching order (see the module docstring).
TIERS = ("exact", "core", "weekly_vs_dated", "wrong_church", "wrong_type", "wrong_time")
FOUND_TIERS = ("exact", "core", "weekly_vs_dated", "wrong_time")
DIAGNOSTIC_TIERS = ("wrong_church", "wrong_type")
LEVELS = {
    "strict": ("exact",),
    "core": ("exact", "core"),
    "loose": ("exact", "core", "weekly_vs_dated"),
    "any_time": FOUND_TIERS,
}
# Label-side outcomes in display order; they sum to the number of label events.
LABEL_OUTCOMES = (*FOUND_TIERS, *DIAGNOSTIC_TIERS, "missed")

CORE_FIELDS = (
    "church_slug", "event_type", "event_kind", "day_of_week", "date", "start_time", "cancelled",
)


# ── Comparing two events ────────────────────────────────────────────────────
def _weeks(event: dict[str, Any]) -> frozenset[str]:
    return frozenset(event.get("weeks_of_month") or ())


def _season(event: dict[str, Any]) -> tuple[Any, ...] | None:
    season = event.get("season")
    if not isinstance(season, dict):
        return None
    return tuple(season.get(k) for k in ("start_month", "start_day", "end_month", "end_day"))


def _weekday(event: dict[str, Any]) -> str | None:
    if event.get("event_kind") == "weekly":
        return event.get("day_of_week")
    try:
        return DAYS[date.fromisoformat(event.get("date") or "").weekday()]
    except ValueError:
        return None


def _same(label: dict[str, Any], pred: dict[str, Any], fields: Iterable[str]) -> bool:
    return all(label.get(f) == pred.get(f) for f in fields)


def _detail_diffs(label: dict[str, Any], pred: dict[str, Any]) -> int:
    """How many of end time, `weeks_of_month` and `season` disagree."""
    return (
        (label.get("end_time") != pred.get("end_time"))
        + (_weeks(label) != _weeks(pred))
        + (_season(label) != _season(pred))
    )


def _without(*fields: str) -> tuple[str, ...]:
    return tuple(f for f in CORE_FIELDS if f not in fields)


def _minutes_apart(label: dict[str, Any], pred: dict[str, Any]) -> int:
    a, b = time_to_minutes(label.get("start_time")), time_to_minutes(pred.get("start_time"))
    return 24 * 60 if a is None or b is None else abs(a - b)


# Each tier: does the pair qualify, and its cost (lower pairs first).
Tier = Callable[[dict[str, Any], dict[str, Any]], int | None]


def _tier_exact(g: dict[str, Any], p: dict[str, Any]) -> int | None:
    return 0 if _same(g, p, CORE_FIELDS) and _detail_diffs(g, p) == 0 else None


def _tier_core(g: dict[str, Any], p: dict[str, Any]) -> int | None:
    return _detail_diffs(g, p) if _same(g, p, CORE_FIELDS) else None


def _tier_weekly_vs_dated(g: dict[str, Any], p: dict[str, Any]) -> int | None:
    if g.get("event_kind") == p.get("event_kind"):
        return None
    if not _same(g, p, ("church_slug", "event_type", "start_time", "cancelled")):
        return None
    return 0 if _weekday(g) is not None and _weekday(g) == _weekday(p) else None


def _tier_wrong_church(g: dict[str, Any], p: dict[str, Any]) -> int | None:
    ok = g.get("church_slug") != p.get("church_slug") and _same(g, p, _without("church_slug"))
    return _detail_diffs(g, p) if ok else None


def _tier_wrong_type(g: dict[str, Any], p: dict[str, Any]) -> int | None:
    ok = g.get("event_type") != p.get("event_type") and _same(g, p, _without("event_type"))
    return _detail_diffs(g, p) if ok else None


def _tier_wrong_time(g: dict[str, Any], p: dict[str, Any]) -> int | None:
    ok = g.get("start_time") != p.get("start_time") and _same(g, p, _without("start_time"))
    return _minutes_apart(g, p) if ok else None


TIER_RULES: dict[str, Tier] = {
    "exact": _tier_exact,
    "core": _tier_core,
    "weekly_vs_dated": _tier_weekly_vs_dated,
    "wrong_church": _tier_wrong_church,
    "wrong_type": _tier_wrong_type,
    "wrong_time": _tier_wrong_time,
}


def match_events(
    label_events: list[dict[str, Any]], pred_events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Pair one bulletin's label events with its predicted events, tier by tier.

    Returns one record per label event and per unpaired prediction:
    `{"tier", "label", "pred"}`, with tier `missed` (no pred) or `spurious` (no
    label) for the unpaired ones.
    """
    open_labels = set(range(len(label_events)))
    open_preds = set(range(len(pred_events)))
    records: list[dict[str, Any]] = []
    for tier in TIERS:
        rule = TIER_RULES[tier]
        candidates = []
        for i in open_labels:
            for j in open_preds:
                cost = rule(label_events[i], pred_events[j])
                if cost is not None:
                    candidates.append((cost, i, j))
        for _, i, j in sorted(candidates):
            if i in open_labels and j in open_preds:
                open_labels.discard(i)
                open_preds.discard(j)
                records.append({"tier": tier, "label": label_events[i], "pred": pred_events[j]})
    records.extend(
        {"tier": "missed", "label": label_events[i], "pred": None} for i in sorted(open_labels)
    )
    records.extend(
        {"tier": "spurious", "label": None, "pred": pred_events[j]} for j in sorted(open_preds)
    )
    return records


# ── Scores ──────────────────────────────────────────────────────────────────
def _ratio(num: int, den: int) -> float | None:
    return num / den if den else None


def _f1(found_label: int, found_pred: int, n_label: int, n_pred: int) -> float:
    """Found events on both sides over all events on both sides: 2·TP / (labels +
    predictions) when every pair is whole; 1.0 when both sides are empty."""
    total = n_label + n_pred
    return 1.0 if total == 0 else (found_label + found_pred) / total


def score_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Counts and precision/recall/F1 at each level for a set of match records.

    Recall reads off the label side and precision off the prediction side, so a
    record holding only one side of a pair (see `_slice`) counts on that side only.
    """
    label_side = Counter(r["tier"] for r in records if r["label"] is not None)
    pred_side = Counter(r["tier"] for r in records if r["pred"] is not None)
    n_label, n_pred = sum(label_side.values()), sum(pred_side.values())
    levels = {}
    for level, tiers in LEVELS.items():
        found_label = sum(label_side[t] for t in tiers)
        found_pred = sum(pred_side[t] for t in tiers)
        levels[level] = {
            "found": found_label,
            "precision": _ratio(found_pred, n_pred),
            "recall": _ratio(found_label, n_label),
            "f1": _f1(found_label, found_pred, n_label, n_pred),
        }
    return {
        "label_events": n_label,
        "predicted_events": n_pred,
        "outcomes": {t: label_side[t] for t in LABEL_OUTCOMES},
        "spurious": pred_side["spurious"],
        "rates": {
            **{t: _ratio(label_side[t], n_label) for t in (*DIAGNOSTIC_TIERS, "missed")},
            "spurious": _ratio(pred_side["spurious"], n_pred),
        },
        "levels": levels,
    }


def _slice(records: list[dict[str, Any]], field: str) -> dict[str, dict[str, Any]]:
    """`score_records` per value of `field`: label events by their own value,
    predictions by theirs. A pair whose two sides fall in different slices (a
    weekly label found as a dated prediction) keeps its tier on each side."""
    values: set[str] = set()
    for r in records:
        for side in ("label", "pred"):
            if r[side] is not None and r[side].get(field) is not None:
                values.add(r[side][field])
    out = {}
    for value in sorted(values):
        sliced = []
        for r in records:
            label = r["label"] if r["label"] is not None and r["label"].get(field) == value else None
            pred = r["pred"] if r["pred"] is not None and r["pred"].get(field) == value else None
            if label is not None or pred is not None:
                sliced.append({"tier": r["tier"], "label": label, "pred": pred})
        out[value] = score_records(sliced)
    return out


def _presence_category(label_value: Any, pred_value: Any, same: bool) -> str:
    if not label_value and not pred_value:
        return "both_empty"
    if not pred_value:
        return "missing"
    if not label_value:
        return "extra"
    return "match" if same else "different"


def field_accuracy(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """How often each secondary field agrees, over the pairs found at the loose level.

    `weeks_of_month` and `season` only over pairs that are weekly on both sides.
    Each field's outcomes: both_empty, match, different, missing (label has it,
    prediction does not), extra (prediction has it, label does not); notes are
    compared by presence only, so a note on both sides is a match.
    """
    pairs = [r for r in records if r["tier"] in LEVELS["loose"]]
    weekly = [
        r for r in pairs
        if r["label"]["event_kind"] == "weekly" and r["pred"].get("event_kind") == "weekly"
    ]
    fields: dict[str, tuple[list[dict[str, Any]], Callable[[dict[str, Any]], Any]]] = {
        "end_time": (pairs, lambda e: e.get("end_time")),
        "weeks_of_month": (weekly, _weeks),
        "season": (weekly, _season),
        "note": (pairs, lambda e: bool((e.get("note") or "").strip())),
    }
    out = {}
    for name, (subset, value) in fields.items():
        counts = Counter(
            _presence_category(
                value(r["label"]), value(r["pred"]), value(r["label"]) == value(r["pred"]),
            )
            for r in subset
        )
        agree = counts["both_empty"] + counts["match"]
        out[name] = {
            "pairs": len(subset),
            "accuracy": _ratio(agree, len(subset)),
            **{k: counts[k] for k in ("both_empty", "match", "different", "missing", "extra")},
        }
    return out


# ── Loading ─────────────────────────────────────────────────────────────────
def report_dir(
    classifier_name: str,
    version: str | None = None,
    classifier_options: dict[str, Any] | None = None,
) -> Path:
    """The eval output for `classifier_name` at `version`.

    `version` is a classifier version (`gpt-6-luna+strict+...`) or the name of
    its directory under `eval/`, as the "Versions with output" list prints it.
    The default is the version the classifier has when built with
    `classifier_options`: the same options `eval run` was given.
    """
    # Built only for its name and version (a `--model` override changes both).
    classifier = get_classifier(classifier_name, **(classifier_options or {}))
    eval_root = run_dir(classifier.name) / "eval"
    if version is None:
        version = classifier.version
    elif (eval_root / version).is_dir():
        return eval_root / version
    return eval_root / version_dir_name(classifier.name, version)


def load_scored_bulletins(
    out_dir: Path, labels_dir: Path = LABELS_DIR, *, statuses: Iterable[str] = DEFAULT_STATUSES,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """(label + prediction for every scorable bulletin, labels with no prediction)."""
    wanted = set(statuses) - {"skipped"}
    predictions: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted((out_dir / "predictions").glob("*/*.json")):
        try:
            pred = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            LOGGER.warning("Skipping unreadable prediction %s", path)
            continue
        # Keyed by the full hash inside: the file name is only its first characters.
        content_hash = pred.get("content_hash") if isinstance(pred, dict) else None
        predictions[(path.parent.name, content_hash or path.stem)] = pred

    scored, unpredicted = [], []
    for path in sorted(labels_dir.glob("*/*.json")):
        slug, content_hash = path.parent.name, path.stem
        if not (is_valid_slug(slug) and is_valid_hash(content_hash)):
            continue
        try:
            label = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            LOGGER.warning("Skipping unreadable label %s", path)
            continue
        if not isinstance(label, dict) or label.get("status") not in wanted:
            continue
        pred = predictions.get((slug, content_hash))
        if pred is None:
            unpredicted.append({"parish_slug": slug, "content_hash": content_hash})
        else:
            scored.append({
                "parish_slug": slug, "content_hash": content_hash, "label": label, "pred": pred,
            })
    return scored, unpredicted


# ── Building the report ─────────────────────────────────────────────────────
def _bulletin_level(bulletins: list[dict[str, Any]]) -> dict[str, Any]:
    perfect = Counter()
    published = Counter()
    wrong_bulletin = Counter()
    count_errors = []
    for b in bulletins:
        score = b["score"]
        for level, values in score["levels"].items():
            if values["found"] == score["label_events"] == score["predicted_events"]:
                perfect[level] += 1
        label_date = b["label"].get("published_date")
        pred_date = b["pred"].get("published_date")
        if label_date:
            published["labeled"] += 1
            published["correct"] += label_date == pred_date
            published["missing"] += not pred_date
        flag = bool((b["label"].get("flags") or {}).get("wrong_bulletin"))
        said = bool(b["pred"].get("wrong_bulletin"))
        wrong_bulletin[{(True, True): "tp", (False, True): "fp",
                        (True, False): "fn", (False, False): "tn"}[(flag, said)]] += 1
        count_errors.append(score["predicted_events"] - score["label_events"])
    n = len(bulletins)
    return {
        "bulletins": n,
        "perfect": {level: perfect[level] for level in LEVELS},
        "perfect_rate": {level: _ratio(perfect[level], n) for level in LEVELS},
        "published_date": {
            "labeled": published["labeled"],
            "correct": published["correct"],
            "missing": published["missing"],
            "accuracy": _ratio(published["correct"], published["labeled"]),
        },
        "wrong_bulletin": {k: wrong_bulletin[k] for k in ("tp", "fp", "fn", "tn")},
        "event_count": {
            "mean_abs_error": statistics.fmean(abs(e) for e in count_errors) if n else None,
            "over": sum(e > 0 for e in count_errors),
            "under": sum(e < 0 for e in count_errors),
            "exact": sum(e == 0 for e in count_errors),
        },
    }


def _cost(bulletins: list[dict[str, Any]]) -> dict[str, Any]:
    usage: Counter[str] = Counter()
    seconds = []
    for b in bulletins:
        for key, value in (b["pred"].get("usage") or {}).items():
            if isinstance(value, int):
                usage[key] += value
        if isinstance(b["pred"].get("seconds"), int | float):
            seconds.append(b["pred"]["seconds"])
    return {
        "usage": dict(sorted(usage.items())),
        "from_cache": sum(bool(b["pred"].get("from_cache")) for b in bulletins),
        "seconds_total": round(sum(seconds), 3),
        "seconds_mean": round(statistics.fmean(seconds), 3) if seconds else None,
        "seconds_median": round(statistics.median(seconds), 3) if seconds else None,
    }


def _strip(event: dict[str, Any] | None) -> dict[str, Any] | None:
    if event is None:
        return None
    return {k: v for k, v in event.items() if k not in ("raw", "problems", "origin")}


def build_report(
    out_dir: Path, labels_dir: Path = LABELS_DIR, *, statuses: Iterable[str] = DEFAULT_STATUSES,
) -> dict[str, Any]:
    """Score every predicted labeled bulletin in `out_dir`; the report as a dict."""
    statuses = tuple(statuses)
    bulletins, unpredicted = load_scored_bulletins(out_dir, labels_dir, statuses=statuses)
    all_records: list[dict[str, Any]] = []
    for b in bulletins:
        b["records"] = match_events(b["label"].get("events") or [], b["pred"].get("events") or [])
        b["score"] = score_records(b["records"])
        all_records.extend(b["records"])

    try:
        run_summary = json.loads((out_dir / "run.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        run_summary = {}
    first_pred = bulletins[0]["pred"] if bulletins else {}

    return {
        "classifier": run_summary.get("classifier") or first_pred.get("classifier"),
        "classifier_version": (
            run_summary.get("classifier_version") or first_pred.get("classifier_version")
        ),
        "generated_at": utc_now_iso(),
        "eval_dir": out_dir.as_posix(),
        "label_statuses": [s for s in statuses if s != "skipped"],
        "unpredicted": unpredicted,
        "run_errors": run_summary.get("errors") or [],
        "overall": score_records(all_records),
        "macro_f1": {
            level: (
                statistics.fmean(b["score"]["levels"][level]["f1"] for b in bulletins)
                if bulletins else None
            )
            for level in LEVELS
        },
        "by_event_type": _slice(all_records, "event_type"),
        "by_event_kind": _slice(all_records, "event_kind"),
        "fields": field_accuracy(all_records),
        "bulletin_level": _bulletin_level(bulletins),
        "cost": _cost(bulletins),
        "bulletins": [
            {
                "parish_slug": b["parish_slug"],
                "content_hash": b["content_hash"],
                **b["score"],
                "records": [
                    {"tier": r["tier"], "label": _strip(r["label"]), "pred": _strip(r["pred"])}
                    for r in b["records"]
                ],
            }
            for b in bulletins
        ],
    }


# ── Markdown ────────────────────────────────────────────────────────────────
def _pct(value: float | None) -> str:
    return "–" if value is None else f"{value * 100:.1f}%"


def _table(header: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines.extend("| " + " | ".join(str(c) for c in row) + " |" for row in rows)
    return lines


def _describe(event: dict[str, Any]) -> str:
    when = event.get("day_of_week") if event.get("event_kind") == "weekly" else event.get("date")
    time = event.get("start_time") or "?"
    if event.get("end_time"):
        time += f"–{event['end_time']}"
    parts = [f"{event.get('event_type') or '?'} {when or '?'} {time} @ {event.get('church_slug') or '?'}"]
    if event.get("weeks_of_month"):
        parts.append("weeks " + ",".join(event["weeks_of_month"]))
    season = _season(event)
    if season is not None:
        start_m, start_d, end_m, end_d = season
        parts.append(
            f"season {start_m}{'/' + str(start_d) if start_d else ''}"
            f"–{end_m}{'/' + str(end_d) if end_d else ''}"
        )
    if event.get("cancelled"):
        parts.append("CANCELLED")
    if (event.get("note") or "").strip():
        parts.append(f"note: {event['note'].strip()}")
    return "; ".join(parts)


def _level_rows(score: dict[str, Any], macro: dict[str, float | None] | None = None) -> list[list[Any]]:
    rows = []
    for level, values in score["levels"].items():
        row = [
            level, values["found"], _pct(values["precision"]), _pct(values["recall"]),
            _pct(values["f1"]),
        ]
        if macro is not None:
            row.append(_pct(macro[level]))
        rows.append(row)
    return rows


def _slice_rows(slices: dict[str, dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for value, s in slices.items():
        rows.append([
            value, s["label_events"], s["predicted_events"],
            _pct(s["levels"]["strict"]["f1"]), _pct(s["levels"]["core"]["f1"]),
            _pct(s["levels"]["loose"]["recall"]), _pct(s["levels"]["loose"]["precision"]),
            _pct(s["levels"]["loose"]["f1"]), _pct(s["levels"]["any_time"]["f1"]),
            _pct(s["rates"]["wrong_church"]), _pct(s["rates"]["wrong_type"]),
        ])
    return rows


SLICE_HEADER = [
    "", "Label", "Pred", "Strict F1", "Core F1", "Loose R", "Loose P", "Loose F1",
    "Any-time F1", "Wrong church", "Wrong type",
]


def render_markdown(report: dict[str, Any]) -> str:
    overall = report["overall"]
    n_label = overall["label_events"]
    bl = report["bulletin_level"]
    lines = [
        f"# Eval report: {report['classifier']}",
        "",
        f"- Version: `{report['classifier_version']}`",
        f"- Generated: {report['generated_at']}",
        f"- Bulletins scored: {bl['bulletins']} (labels: {', '.join(report['label_statuses'])})",
        f"- Label events: {n_label}; predicted events: {overall['predicted_events']}",
    ]
    if report["unpredicted"]:
        lines.append(
            f"- **{len(report['unpredicted'])} labeled bulletin(s) have no prediction** "
            "and are not scored: "
            + ", ".join(f"{u['parish_slug']}/{u['content_hash'][:8]}" for u in report["unpredicted"])
        )
    if report["run_errors"]:
        lines.append(f"- Classifier errors in the run: {len(report['run_errors'])}")

    lines += ["", "## Headline", ""]
    lines += _table(
        ["Level", "Found", "Precision", "Recall", "F1 (micro)", "F1 (macro)"],
        _level_rows(overall, report["macro_f1"]),
    )
    lines += [
        "",
        "Strict = everything agrees; core = end time / weeks / season may differ; "
        "loose = also weekly-vs-dated on the same weekday; any_time = also a wrong "
        "start time (same church, type and day). "
        "Micro pools every event; macro averages per-bulletin F1.",
        "",
        "## Errors",
        "",
    ]
    rates = overall["rates"]
    lines += _table(
        ["", "Count", "Share"],
        [
            ["Wrong church (of label events)", overall["outcomes"]["wrong_church"],
             _pct(rates["wrong_church"])],
            ["Wrong type (of label events)", overall["outcomes"]["wrong_type"],
             _pct(rates["wrong_type"])],
            ["Missed (of label events)", overall["outcomes"]["missed"], _pct(rates["missed"])],
            ["Spurious (of predicted events)", overall["spurious"], _pct(rates["spurious"])],
        ],
    )
    lines += ["", "### Where each label event ended up", ""]
    lines += _table(
        ["Outcome", "Count", "Share"],
        [[t, overall["outcomes"][t], _pct(_ratio(overall["outcomes"][t], n_label))]
         for t in LABEL_OUTCOMES],
    )

    lines += ["", "## By event type", ""]
    lines += _table(SLICE_HEADER, _slice_rows(report["by_event_type"]))
    lines += ["", "## By event kind", ""]
    lines += _table(SLICE_HEADER, _slice_rows(report["by_event_kind"]))

    lines += [
        "", "## Field accuracy (pairs found at the loose level)", "",
        "Missing = the label has it, the prediction does not; extra = the reverse. "
        "Weeks and season are over weekly–weekly pairs; notes by presence only.",
        "",
    ]
    lines += _table(
        ["Field", "Pairs", "Accuracy", "Both empty", "Match", "Different", "Missing", "Extra"],
        [
            [name, f["pairs"], _pct(f["accuracy"]), f["both_empty"], f["match"],
             f["different"], f["missing"], f["extra"]]
            for name, f in report["fields"].items()
        ],
    )

    pd, wb, ec = bl["published_date"], bl["wrong_bulletin"], bl["event_count"]
    lines += ["", "## Bulletins", ""]
    lines += _table(
        ["", "Value"],
        [
            *[[f"Perfect ({level})", f"{bl['perfect'][level]} ({_pct(bl['perfect_rate'][level])})"]
              for level in LEVELS],
            ["Published date correct",
             f"{pd['correct']}/{pd['labeled']} ({_pct(pd['accuracy'])}); {pd['missing']} not given"],
            ["Wrong bulletin (tp / fp / fn / tn)", f"{wb['tp']} / {wb['fp']} / {wb['fn']} / {wb['tn']}"],
            ["Event count: mean abs error",
             "–" if ec["mean_abs_error"] is None else f"{ec['mean_abs_error']:.2f}"],
            ["Event count: over / under / exact", f"{ec['over']} / {ec['under']} / {ec['exact']}"],
        ],
    )

    cost = report["cost"]
    lines += ["", "## Cost", ""]
    lines += _table(
        ["", "Value"],
        [
            *[[k, f"{v:,}"] for k, v in cost["usage"].items()],
            ["Served from cache", cost["from_cache"]],
            ["Seconds (total / mean / median)",
             f"{cost['seconds_total']} / {cost['seconds_mean']} / {cost['seconds_median']}"],
        ],
    )

    worst = sorted(
        report["bulletins"],
        key=lambda b: (b["levels"]["loose"]["f1"], b["levels"]["strict"]["f1"], b["parish_slug"]),
    )
    lines += ["", "## Per bulletin (worst first)", ""]
    lines += _table(
        ["Bulletin", "Label", "Pred", "Strict F1", "Loose F1", "Any-time F1", "Wrong church",
         "Wrong type", "Missed", "Spurious"],
        [
            [f"{b['parish_slug']}/{b['content_hash'][:8]}", b["label_events"],
             b["predicted_events"], _pct(b["levels"]["strict"]["f1"]),
             _pct(b["levels"]["loose"]["f1"]), _pct(b["levels"]["any_time"]["f1"]),
             b["outcomes"]["wrong_church"],
             b["outcomes"]["wrong_type"], b["outcomes"]["missed"], b["spurious"]]
            for b in worst
        ],
    )

    lines += ["", "## Differences", ""]
    any_diff = False
    for b in worst:
        diffs = [r for r in b["records"] if r["tier"] != "exact"]
        if not diffs:
            continue
        any_diff = True
        lines += [f"### {b['parish_slug']}/{b['content_hash'][:8]}", ""]
        order = {t: i for i, t in enumerate((*LABEL_OUTCOMES, "spurious"))}
        for r in sorted(diffs, key=lambda r: order[r["tier"]]):
            if r["label"] is not None and r["pred"] is not None:
                lines.append(
                    f"- **{r['tier']}**: label `{_describe(r['label'])}` → "
                    f"predicted `{_describe(r['pred'])}`"
                )
            elif r["label"] is not None:
                lines.append(f"- **missed**: `{_describe(r['label'])}`")
            else:
                lines.append(f"- **spurious**: `{_describe(r['pred'])}`")
        lines.append("")
    if not any_diff:
        lines.append("Every scored bulletin matches its label exactly.")
    return "\n".join(lines).rstrip() + "\n"


# ── Main entry point ────────────────────────────────────────────────────────
def write_report(
    *,
    classifier_name: str,
    version: str | None = None,
    classifier_options: dict[str, Any] | None = None,
    statuses: Iterable[str] = DEFAULT_STATUSES,
    labels_dir: Path = LABELS_DIR,
) -> dict[str, Any]:
    """Score an eval run and write `report.md` and `report.json` next to its predictions."""
    out_dir = report_dir(classifier_name, version, classifier_options)
    if not (out_dir / "predictions").is_dir():
        versions = sorted(p.name for p in out_dir.parent.glob("*") if p.is_dir())
        raise FileNotFoundError(
            f"No eval predictions in {out_dir}; run `pnpm eval --classifier {classifier_name}` "
            f"with the same flags first, or pass one of the versions with output as --version: "
            f"{', '.join(versions) or 'none'}"
        )
    report = build_report(out_dir, labels_dir, statuses=statuses)
    json_path, md_path = out_dir / "report.json", out_dir / "report.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    overall = report["overall"]
    return {
        "report_md": md_path.as_posix(),
        "report_json": json_path.as_posix(),
        "bulletins_scored": report["bulletin_level"]["bulletins"],
        "unpredicted": len(report["unpredicted"]),
        "f1": {level: round(v["f1"], 4) for level, v in overall["levels"].items()},
        "wrong_church_rate": overall["rates"]["wrong_church"],
        "wrong_type_rate": overall["rates"]["wrong_type"],
    }
