"""`factory quota backfill`: metadata and tokens for attempts from before quota tracking.

Tokens, models and the CLI version come from the copied transcripts; the requested model,
effort and prompt version from the stage spec at the attempt's commit. Existing readings
are linked to attempts by time. What can't be recovered is listed in each attempt's gaps,
and its quota is marked approximate (a minimum at best): no settled reading is invented.
Running it again changes nothing.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from pdf_extract.factory import git
from pdf_extract.factory.config import Config, FactoryError
from pdf_extract.factory.ledger import Ledger
from pdf_extract.factory.quota import fingerprint, work_units
from pdf_extract.factory.tokens import Tokens, parse_transcript
from pdf_extract.factory.usage import account_plan

Show = Callable[[str], str | None]  # `git show <rev>:<path>`, None if it isn't there
# A selection reading is taken just before its attempt starts.
BEFORE_WITHIN = timedelta(minutes=5)


def git_show(repo: Path) -> Show:
    def show(spec: str) -> str | None:
        try:
            return git.git(repo, "show", spec)
        except FactoryError:
            return None
    return show


def backfill(ledger: Ledger, config: Config, show: Show, root: Path = Path(".")) -> dict[str, Any]:
    done: list[dict[str, Any]] = []
    seen: dict[str, set[str]] = {}  # message ids counted per transcript, attempt by attempt
    rows = ledger.all("SELECT a.* FROM attempt a LEFT JOIN attempt_meta m ON m.attempt_id = "
                      "a.id WHERE m.attempt_id IS NULL AND a.finished_at IS NOT NULL "
                      "ORDER BY a.id")
    for a in rows:
        job = ledger.job(a["job_id"])
        run = ledger.run(job["run_id"])
        gaps = ["SDK version not recorded"]
        tokens = Tokens()
        path = Path(a["transcript"]) if a["transcript"] else None
        if path is not None and not path.is_absolute():
            path = root / path
        if path is not None and path.exists():
            ids = seen.setdefault(str(path), set())
            with path.open(encoding="utf-8") as f:
                tokens = parse_transcript(f, since=datetime.fromisoformat(a["started_at"]),
                                          seen=ids)
            ids |= tokens.message_ids
            gaps += tokens.gaps
        else:
            gaps.append("no transcript: tokens, models and CLI version unknown")
        spec: dict[str, Any] = {}
        spec_text = show(f"{a['commit_sha']}:factory/stages/{job['stage']}.yaml") \
            if a["commit_sha"] else None
        if spec_text:
            spec = yaml.safe_load(spec_text) or {}
        else:
            gaps.append("stage spec at its commit unavailable: model, effort and prompt "
                        "version unknown")
        prompt = (show(f"{a['commit_sha']}:{spec['prompt']}") or "") if spec.get("prompt") \
            else ""
        batches = None
        if job["stage"] == "map":
            text = show(f"{a['commit_sha']}:data/dioceses/{run['diocese']}/batches.json")
            batches = (json.loads(text) or {}).get("batches") if text else None
        units = work_units(job["stage"], json.loads(job["input"]), batches)
        if units is None:
            gaps.append("work units unknown (no batches.json at its commit)")
        steps = ledger.one("SELECT COUNT(*) AS n FROM step WHERE attempt_id = ? AND kind = "
                           "'rate_limit'", a["id"])["n"]
        if steps:
            gaps.append(f"{steps} rate-limit events kept without their utilization")
        account = next((x for x in config.accounts if x.name == a["account"]), None)
        plan = account_plan(account) if account else None
        gaps.append("plan read at backfill time" if plan else "plan unknown")
        if not _settled_reading(ledger, a, config.quota_settle_seconds):
            gaps.append("no settled reading after it")
        resumed = ledger.one("SELECT id FROM attempt WHERE session_id = ? AND id < ? ORDER BY "
                             "id DESC LIMIT 1", a["session_id"], a["id"]) \
            if a["session_id"] and a["kind"] not in ("start", "fresh") else None
        ledger.set_attempt_meta(
            a["id"], source="backfill", approximate=1, requested_model=spec.get("model"),
            effort=spec.get("effort"), sdk_version=None, cli_version=tokens.cli_version,
            entrypoint=tokens.entrypoint, plan=plan,
            config_hash=fingerprint(spec_text, prompt, list(spec.get("skills") or []))
            if spec_text else None,
            resumed_from=resumed["id"] if resumed else None, work_units=units, gaps=gaps,
            **tokens.columns())
        done.append({"attempt": a["id"], "job": f"{job['run_id']}/{job['name']}",
                     "tokens": tokens.columns(), "gaps": gaps})
    return {"attempts": done, "linked": _link_readings(ledger)}


def _settled_reading(ledger: Ledger, a: Any, settle_seconds: int) -> bool:
    if not a["account"]:
        return False
    after = (datetime.fromisoformat(a["finished_at"])
             + timedelta(seconds=settle_seconds)).isoformat(timespec="microseconds")
    nxt = ledger.one("SELECT MIN(started_at) AS at FROM attempt WHERE account = ? AND "
                     "started_at > ?", a["account"], a["finished_at"])["at"]
    return ledger.one("SELECT 1 FROM usage WHERE account = ? AND at >= ? AND (? IS NULL OR "
                      "at <= ?)", a["account"], after, nxt, nxt) is not None


def _link_readings(ledger: Ledger) -> int:
    """Selection readings linked by time: the one just before an attempt is its before;
    the first one after an attempt not already some attempt's before, its after."""
    linked = 0
    attempts = ledger.all("SELECT * FROM attempt WHERE account IS NOT NULL AND finished_at IS "
                          "NOT NULL AND id NOT IN (SELECT attempt_id FROM usage WHERE "
                          "attempt_id IS NOT NULL) ORDER BY id")
    for a in attempts:
        start = datetime.fromisoformat(a["started_at"])
        row = ledger.one("SELECT id FROM usage WHERE account = ? AND attempt_id IS NULL AND "
                         "source = 'select' AND at <= ? AND at >= ? ORDER BY at DESC LIMIT 1",
                         a["account"], a["started_at"],
                         (start - BEFORE_WITHIN).isoformat(timespec="microseconds"))
        if row:
            ledger.run_sql("UPDATE usage SET source = 'before', attempt_id = ?, job_id = ? "
                           "WHERE id = ?", a["id"], a["job_id"], row["id"])
            linked += 1
    for a in attempts:
        row = ledger.one("SELECT id FROM usage WHERE account = ? AND attempt_id IS NULL AND "
                         "source = 'select' AND at >= ? ORDER BY at LIMIT 1",
                         a["account"], a["finished_at"])
        nxt = ledger.one("SELECT MIN(started_at) AS at FROM attempt WHERE account = ? AND "
                         "started_at > ?", a["account"], a["finished_at"])["at"]
        if row and (nxt is None or ledger.one("SELECT at FROM usage WHERE id = ?",
                                              row["id"])["at"] <= nxt):
            ledger.run_sql("UPDATE usage SET source = 'after', attempt_id = ?, job_id = ? "
                           "WHERE id = ?", a["id"], a["job_id"], row["id"])
            linked += 1
    return linked
