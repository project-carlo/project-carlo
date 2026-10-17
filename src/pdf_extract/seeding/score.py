"""`seed score RUN`: a test run's drafts against the labels (docs/seeding-plan.md, "Testing it first").

Each draft in `data/seed-evals/<run>/seeds/` is compared with the label of the
bulletin its parish was cut off at, using the eval report's matching
(`evals.report.match_events`). Only what a seed holds is compared: the label's
weekly rows, and its dated rows and cancellations on or after the cutoff date.

The numbers, per parish and in total:

- **settled precision**: of the slots the agent settled and included, how many
  the label has. This matters most, since a reviewer may approve settled
  slots without reading each one. At `strict` (everything agrees) and `core`
  (church, type, day or date, start time and cancelled agree).
- **settled recall**: of the label's required rows, how many a settled slot
  covers. The rest are open questions, slots the agent left out, or misses.
- **wrongly excluded**: settled slots the agent left out that a required label
  row the settled slots miss matches.
- **leaning**: how often the option the agent leaned to on an open question
  matched the label. A leaning entry is right when it matches a label row the
  label wants (required, or optional and preferably included); leaning to
  leave the slot out is right when no option matches a required row.
- open questions, external calls and their cost.

Writes `report.json` and `report.md` in the run's directory.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pdf_extract.evals.report import LEVELS, OPTIONAL, match_events, score_records
from pdf_extract.labeling.labels import LABELS_DIR, read_label
from pdf_extract.seeding.files import (
    EXCLUDE,
    INCLUDE,
    NEEDS_HUMAN,
    SETTLED,
    calls_cost,
    paid_calls,
    question_count,
    read_seed,
)
from pdf_extract.seeding.queries import SeedContext, SeedError
from pdf_extract.storage import utc_now_iso

FOUND = set(LEVELS["loose"])


def _event(entry: dict[str, Any]) -> dict[str, Any]:
    """A seed entry as a label row, for the matcher."""
    weekly = entry.get("event_kind") == "weekly"
    return {
        "church_slug": entry.get("church_slug"),
        "event_type": entry.get("event_type"),
        "event_kind": entry.get("event_kind"),
        "day_of_week": entry.get("day_of_week") if weekly else None,
        "date": None if weekly else entry.get("date"),
        "start_time": entry.get("start_time"),
        "end_time": entry.get("end_time"),
        "cancelled": bool(entry.get("cancelled")),
        "weeks_of_month": list(entry.get("weeks_of_month") or []) if weekly else [],
        "exclude_weeks": weekly and entry.get("exclude_weeks") is True,
        "season": entry.get("season") if weekly else None,
        "page_number": None,
        "note": entry.get("note"),
        "optional": None,
    }


def seed_scope(events: list[dict[str, Any]], as_of_date: str) -> list[dict[str, Any]]:
    """The label rows a seed as of `as_of_date` could hold."""
    return [
        e for e in events
        if e.get("event_kind") == "weekly" or (e.get("date") or "") >= as_of_date
    ]


def _matches(label_events: list[dict[str, Any]], entry: dict[str, Any]) -> bool:
    """Whether `entry` alone pairs with one of `label_events` in a tier that counts as found."""
    required = [{**e, "optional": None} for e in label_events]
    return any(
        r["tier"] in FOUND and r["label"] is not None and r["pred"] is not None
        for r in match_events(required, [_event(entry)])
    )


def score_parish(seed: dict[str, Any], label: dict[str, Any], as_of_date: str) -> dict[str, Any]:
    labels = seed_scope(label.get("events") or [], as_of_date)
    required = [e for e in labels if not e.get("optional")]
    wanted = [e for e in labels if e.get("optional") in (None, INCLUDE)]
    slots = [s for s in seed.get("slots") or [] if isinstance(s, dict)]
    settled = [s for s in slots if s.get("status") == SETTLED and s.get("decision") == INCLUDE
               and s.get("entry")]
    records = match_events(labels, [_event(s["entry"]) for s in settled])
    scores = score_records(records)

    missed = [r["label"] for r in records if r["tier"] == "missed"]
    wrongly_excluded = [
        s["id"] for s in slots
        if s.get("status") == SETTLED and s.get("decision") == EXCLUDE and s.get("entry")
        and _matches(missed, s["entry"])
    ]

    leanings = []
    for slot in slots:
        if slot.get("status") != NEEDS_HUMAN:
            continue
        options = [o for o in slot.get("options") or [] if isinstance(o, dict)]
        leaning = next((o for o in options if o.get("leaning")), None)
        if leaning is None:
            continue
        if leaning.get("entry"):
            right = _matches(wanted, leaning["entry"])
        else:
            right = not any(o.get("entry") and _matches(required, o["entry"]) for o in options)
        leanings.append({"slot": slot.get("id"), "question": slot.get("question"),
                         "matched_label": right})

    return {
        "label_events": len(required),
        "optional_label_events": sum(1 for r in records if r["tier"] == OPTIONAL),
        "settled_included": len(settled),
        # Settled slots scored: those paired only with optional label rows are left
        # out, as the eval report leaves them out of precision.
        "settled_scored": scores["predicted_events"],
        "settled": {
            level: {
                "precision": scores["levels"][level]["precision"],
                "recall": scores["levels"][level]["recall"],
                "found": scores["levels"][level]["found_predicted"],
                "covered": scores["levels"][level]["found"],
            }
            for level in ("strict", "core")
        },
        "spurious": [_brief(r["pred"]) for r in records if r["tier"] == "spurious"],
        "missed": [_brief(e) for e in missed],
        "wrongly_excluded": wrongly_excluded,
        "open_questions": question_count(seed),
        "leaning": leanings,
        "calls": len(seed.get("calls") or []),
        "paid_calls": paid_calls(seed),
        "cost_usd": round(calls_cost(seed), 4),
    }


def _brief(event: dict[str, Any]) -> str:
    when = event.get("day_of_week") or event.get("date") or "?"
    weeks = "/".join(event.get("weeks_of_month") or [])
    if weeks:
        weeks = f" except {weeks}" if event.get("exclude_weeks") else f" {weeks}"
    cancelled = " cancelled" if event.get("cancelled") else ""
    return (f"{event.get('church_slug')} {event.get('event_type')} {when}{weeks} "
            f"{event.get('start_time')}{cancelled}")


def _ratio(num: int, den: int) -> float | None:
    return round(num / den, 3) if den else None


def score_run(eval_run: str, *, labels_dir: Path = LABELS_DIR, ctx: SeedContext | None = None,
              ) -> dict[str, Any]:
    ctx = ctx or SeedContext.for_run(eval_run)
    run_dir = ctx.seeds_dir.parent
    parishes: dict[str, Any] = {}
    not_drafted, blocked = [], []
    for slug, info in sorted((ctx.manifest.get("parishes") or {}).items()):
        seed = read_seed(slug, ctx.seeds_dir)
        if seed is None:
            not_drafted.append(slug)
            continue
        if seed.get("status") == "blocked":
            blocked.append({"parish": slug, "reason": seed.get("blocked_reason")})
            continue
        label = read_label(slug, info["label_hash"], labels_dir)
        if label is None:
            raise SeedError(f"The label {slug}/{info['label_hash'][:12]} is gone")
        parishes[slug] = score_parish(seed, label, info["fetched_at"][:10])

    totals: dict[str, Any] = {"parishes": len(parishes)}
    for level in ("strict", "core"):
        found = sum(p["settled"][level]["found"] for p in parishes.values())
        settled = sum(p["settled_scored"] for p in parishes.values())
        totals[f"settled_precision_{level}"] = _ratio(found, settled)
    covered = sum(p["settled"]["core"]["covered"] for p in parishes.values())
    labels_total = sum(p["label_events"] for p in parishes.values())
    leanings = [x for p in parishes.values() for x in p["leaning"]]
    totals.update({
        "settled_included": sum(p["settled_included"] for p in parishes.values()),
        "label_events": labels_total,
        "settled_recall_core": _ratio(covered, labels_total),
        "wrongly_excluded": sum(len(p["wrongly_excluded"]) for p in parishes.values()),
        "open_questions": sum(p["open_questions"] for p in parishes.values()),
        "open_questions_per_parish": _ratio(
            sum(p["open_questions"] for p in parishes.values()), len(parishes),
        ),
        "leaning_matched": _ratio(sum(x["matched_label"] for x in leanings), len(leanings)),
        "calls": sum(p["calls"] for p in parishes.values()),
        "paid_calls": sum(p["paid_calls"] for p in parishes.values()),
        "cost_usd": round(sum(p["cost_usd"] for p in parishes.values()), 4),
    })
    totals["cost_usd_per_parish"] = (
        round(totals["cost_usd"] / len(parishes), 4) if parishes else None
    )
    report = {
        "eval_run": eval_run,
        "scored_at": utc_now_iso(),
        "totals": totals,
        "not_drafted": not_drafted,
        "blocked": blocked,
        "parishes": parishes,
    }
    (run_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    (run_dir / "report.md").write_text(render_markdown(report), encoding="utf-8")
    return report


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{100 * value:.0f}%"


def render_markdown(report: dict[str, Any]) -> str:
    t = report["totals"]
    lines = [
        f"# Seeding test run `{report['eval_run']}`",
        "",
        f"{t['parishes']} parishes scored against their labels, "
        f"{len(report['not_drafted'])} not drafted, {len(report['blocked'])} blocked.",
        "",
        "| | |",
        "| :-- | --: |",
        f"| Settled slots included | {t['settled_included']} |",
        f"| Settled precision, strict | {_pct(t['settled_precision_strict'])} |",
        f"| Settled precision, core | {_pct(t['settled_precision_core'])} |",
        f"| Label rows covered by settled slots (core) | {_pct(t['settled_recall_core'])} |",
        f"| Settled slots wrongly left out | {t['wrongly_excluded']} |",
        f"| Open questions | {t['open_questions']} ({t['open_questions_per_parish']} per parish) |",
        f"| Leaning answer matched the label | {_pct(t['leaning_matched'])} |",
        f"| External calls (not cached) | {t['calls']} ({t['paid_calls']}) |",
        f"| Cost | ${t['cost_usd']:.4f} ({t['cost_usd_per_parish'] or 0:.4f} per parish) |",
        "",
        "## Parishes",
        "",
        "| Parish | Settled | Precision (strict / core) | Covered (core) | Open | Calls | Cost |",
        "| :-- | --: | --: | --: | --: | --: | --: |",
    ]
    for slug, p in report["parishes"].items():
        s = p["settled"]
        lines.append(
            f"| {slug} | {p['settled_included']} | {_pct(s['strict']['precision'])} / "
            f"{_pct(s['core']['precision'])} | {_pct(s['core']['recall'])} | "
            f"{p['open_questions']} | {p['calls']} | ${p['cost_usd']:.4f} |"
        )
    details = [
        (slug, p) for slug, p in report["parishes"].items()
        if p["spurious"] or p["missed"] or p["wrongly_excluded"]
    ]
    if details:
        lines += ["", "## Differences", ""]
        for slug, p in details:
            lines.append(f"- **{slug}**")
            lines += [f"  - settled but not in the label: {x}" for x in p["spurious"]]
            lines += [f"  - in the label, no settled slot: {x}" for x in p["missed"]]
            lines += [f"  - left out, but in the label: slot {x}" for x in p["wrongly_excluded"]]
    if report["blocked"]:
        lines += ["", "## Blocked", ""]
        lines += [f"- **{b['parish']}**: {b['reason']}" for b in report["blocked"]]
    return "\n".join(lines) + "\n"
