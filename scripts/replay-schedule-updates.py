"""Replay selected stored update calls against a new prompt, without changing the source DB.

uv run python scripts/replay-schedule-updates.py --db /path/to/run.db \
    --spec data/update-evals/2026-10-18/spec.json --out data/out/replay

Each trial restores the first call's historical schedule and processes that
parish's bulletins in order. Calls are real and billable; nothing is published.
Cases marked required=false are exploratory controls; their failures remain
in the report but do not change the targeted regression's exit status.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import date
from pathlib import Path

from pdf_extract.__main__ import _load_dotenv
from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.classifiers.schedule_update import (
    POLICY,
    POLICY_HASH,
    OpenAIScheduleUpdater,
    parse_response,
    render_context,
)
from pdf_extract.db import migrate
from pdf_extract.schedule.policy import APPLIED, Proposal, decide, whole_call_reason
from pdf_extract.schedule.store import (
    Change,
    append_revision,
    fold_revision,
    intern_entry,
    live_entries,
    parish_churches,
    render_view,
)
from pdf_extract.storage import church_list_for_prompt


def trial(db: Path, case: dict, number: int, out: Path, tier: str, detail: str = 'low') -> dict:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    with sqlite3.connect(f"file:{db.resolve()}?mode=ro", uri=True) as source:
        source.backup(conn)
    migrate(conn)
    calls = [dict(conn.execute(
        "SELECT c.*, b.content_hash FROM llm_call c JOIN bulletin b ON b.id=c.bulletin_id "
        "WHERE c.id=?", (call_id,),
    ).fetchone()) for call_id in case["calls"]]
    parish_id = calls[0]["parish_id"]
    assert all(c["parish_id"] == parish_id for c in calls)
    assert [c["call_date"] for c in calls] == sorted(c["call_date"] for c in calls)
    conn.execute("DELETE FROM current_schedule WHERE parish_id=?", (parish_id,))
    for revision in range(1, calls[0]["base_revision"] + 1):
        fold_revision(conn, parish_id, revision)
    updater = OpenAIScheduleUpdater(service_tier=tier, file_detail=detail)
    records = []
    for original in calls:
        today = date.fromisoformat(original["call_date"])
        view, _ = render_view(conn, parish_id, today)
        context = render_context(church_list_for_prompt(conn, parish_id), today, view)
        pdf = get_store().get(bulletin_pdf_key(case["parish"], original["content_hash"]))
        if pdf is None:
            raise RuntimeError(f"Missing PDF for call {original['id']}")
        reply = updater.call(pdf, context)
        (out / f"{case['parish']}-{number}-call-{original['id']}-raw.json").write_text(
            json.dumps(asdict(reply), indent=2) + "\n",
        )
        parsed = parse_response(reply.text)
        if parsed.status not in ("ok", "lenient"):
            raise RuntimeError(f"Call {original['id']} failed to parse: {parsed.error}")
        proposals = [Proposal(
            seq=p.seq, op=p.op, raw=p.raw, target_entry_id=p.entry_id,
            entry=p.entry, page_number=p.page_number, rationale=p.rationale,
        ) for p in parsed.changes]
        whole = whole_call_reason(
            wrong_bulletin=parsed.wrong_bulletin, stale=False,
            proposals=proposals, live=live_entries(conn, parish_id),
        )
        decisions = decide(
            proposals, live=live_entries(conn, parish_id),
            churches=parish_churches(conn, parish_id), today=today, whole_call=whole,
            targetable={e["id"] for c in json.loads(view)["churches"] for e in c["entries"]},
        )
        changes = [Change(
            d.proposal.op, before_entry_id=d.proposal.target_entry_id,
            after_entry_id=intern_entry(conn, d.entry) if d.entry else None,
        ) for d in decisions if d.decision == APPLIED]
        if changes:
            append_revision(conn, parish_id, source_kind="human", changes=changes,
                            actor="isolated-replay")
        records.append({"original_call_id": original["id"], "context": context,
                        "reply": asdict(reply), "decisions": [asdict(d) for d in decisions]})
    state = live_entries(conn, parish_id)
    checks = {f"entry_{i}_retained": i in state for i in case.get("retain_entry_ids", [])}
    for raw in case.get("absent", []):
        checks["absent_" + json.dumps(raw, sort_keys=True)] = not any(
            all(getattr(e, k) == v for k, v in raw.items()) for e in state.values()
        )
    for raw in case.get("present", []):
        checks["present_" + json.dumps(raw, sort_keys=True)] = any(
            all(getattr(e, k) == v for k, v in raw.items()) for e in state.values()
        )
    checks["responses_valid"] = all(
        not json.loads(r["reply"]["text"])["wrong_bulletin"]
        and all(d["decision"] == APPLIED or d["reason"] in case.get("allowed_rejection_reasons", [])
                for d in r["decisions"]) for r in records
    )
    result = {"parish": case["parish"], "trial": number,
              "required": case.get("required", True), "checks": checks,
              "passed": all(checks.values()), "calls": records}
    (out / f"{case['parish']}-{number}.json").write_text(json.dumps(result, indent=2) + "\n")
    conn.close()
    return {k: v for k, v in result.items() if k != "calls"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--service-tier", default="default", choices=("default", "flex"))
    parser.add_argument("--file-detail", default="low", choices=("auto", "low", "high"))
    args = parser.parse_args()
    if args.trials < 1:
        parser.error("--trials must be positive")
    _load_dotenv()
    args.out.mkdir(parents=True, exist_ok=True)
    cases = json.loads(args.spec.read_text())["cases"]
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(trial, args.db, case, n, args.out, args.service_tier, args.file_detail)
                   for case in cases for n in range(1, args.trials + 1)]
        results = []
        for future in futures:
            result = future.result()
            results.append(result)
            print(json.dumps(result), flush=True)
    summary = {"policy_hash": POLICY_HASH,
               "version": OpenAIScheduleUpdater(file_detail=args.file_detail).version,
               "file_detail": args.file_detail,
               "service_tier": args.service_tier, "results": results,
               "passed": all(r["passed"] for r in results if r["required"]),
               "all_expectations_passed": all(r["passed"] for r in results)}
    (args.out / "policy.txt").write_text(POLICY)
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not summary["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
