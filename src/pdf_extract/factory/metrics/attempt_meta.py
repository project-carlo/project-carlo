"""What an attempt ran with and used, one `attempt_meta` row each (docs/factory-quota.md).

The requested and actual models, effort, SDK and CLI versions, the account's plan, a
fingerprint of what the worker was given, its tokens and its work units. Recording it
never stops a job.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime
from functools import cache
from pathlib import Path
from typing import Any

from pdf_extract.factory import git, render
from pdf_extract.factory.config import Account, FactoryError
from pdf_extract.factory.ledger import Ledger
from pdf_extract.factory.metrics.tokens import Tokens, from_result, parse_transcript
from pdf_extract.factory.plan import ordered_batches
from pdf_extract.factory.spec import StageSpec, spec_path
from pdf_extract.factory.workers import WorkerResult

LOGGER = logging.getLogger(__name__)


def work_units(stage: str, inputs: dict[str, Any],
               batches: list[dict[str, Any]] | None = None) -> int | None:
    """What a job completes: map, the batch's roster entries; seed and seed-review, their
    parishes; anything else (survey, its review, integrate...) 1. None if unknown."""
    if stage == "map":
        entries = inputs.get("entries")
        if not entries and batches is not None:
            entries = next((b.get("entries") for b in batches
                            if b.get("id") == inputs.get("batch")), None)
        return len(entries) if entries else None
    if stage in ("seed", "seed-review"):
        parishes = inputs.get("parishes") or ([inputs["parish"]] if inputs.get("parish")
                                              else [])
        return len(parishes) or 1
    return 1


def fingerprint(spec_text: str, prompt_text: str, skills: list[str],
                code: dict[str, Any] | None = None) -> str:
    """The stage's prompt and context configuration: its spec, prompt file and skill names,
    and `code`: hashes of what else shapes what the worker is given (the code that builds
    its first message, the skills' contents, its reads) and the dispatcher's commit.
    Attempts recorded before `code` existed hash without it."""
    blob = json.dumps([spec_text, prompt_text, sorted(skills)]
                      + ([code] if code is not None else []), sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


def account_plan(account: Account) -> str | None:
    """The account's plan: its login's subscription and rate-limit tier, else local.yaml's."""
    try:
        oauth = json.loads((account.config_dir / ".credentials.json").read_text(
            encoding="utf-8"))["claudeAiOauth"]
        parts = [str(oauth[k]) for k in ("subscriptionType", "rateLimitTier") if oauth.get(k)]
    except (OSError, ValueError, KeyError, TypeError):
        parts = []
    return "/".join(parts) or account.plan


@cache
def code_commit() -> str | None:
    """The commit of the checkout this dispatcher's code was loaded from, if it is one."""
    try:
        return git.head(Path(__file__).resolve().parent)
    except (FactoryError, OSError):
        return None


def record(ledger: Ledger, attempt_id: int, run: Any, job: Any, spec: StageSpec,
           worktree: Path, account: Account | None, result: WorkerResult,
           transcript: Path | None, session: str | None, started: str,
           finished: str) -> None:
    """How the attempt ran and its tokens: from the ResultMessage, else (a crash, a
    timeout) from its transcript. A failure is logged, never raised."""
    try:
        _record(ledger, attempt_id, run, job, spec, worktree, account, result, transcript,
                session, started, finished)
    except Exception:
        LOGGER.exception("attempt %s: recording its metadata failed", attempt_id)


def _record(ledger: Ledger, attempt_id: int, run: Any, job: Any, spec: StageSpec,
            worktree: Path, account: Account | None, result: WorkerResult,
            transcript: Path | None, session: str | None, started: str,
            finished: str) -> None:
    info, gaps = result.info, []
    if result.usage or result.model_usage:
        source = "live"
        tokens = from_result(result.usage, result.model_usage, info.get("messages", 0),
                             info.get("duplicates", 0))
    elif transcript is not None:
        source = "transcript"
        with transcript.open(encoding="utf-8") as f:
            tokens = parse_transcript(f, since=datetime.fromisoformat(started),
                                      until=datetime.fromisoformat(finished))
    else:
        source, tokens = "live", Tokens()
        gaps.append("no token usage reported")
    prompt = (worktree / spec.prompt).read_text(encoding="utf-8") \
        if spec.prompt and (worktree / spec.prompt).exists() else ""
    spec_file = worktree / spec_path(job["stage"])
    spec_text = spec_file.read_text(encoding="utf-8") if spec_file.exists() else ""
    models = sorted(set(tokens.per_model) | set(info.get("models") or []))
    ledger.set_attempt_meta(
        attempt_id, source=source, approximate=0, requested_model=spec.model,
        effort=spec.effort, sdk_version=info.get("sdk_version"),
        cli_version=info.get("cli_version") or tokens.cli_version,
        entrypoint=info.get("entrypoint") or tokens.entrypoint,
        plan=account_plan(account) if account else None,
        config_hash=fingerprint(spec_text, prompt, list(spec.skills),
                                render.context_hashes(worktree, spec)
                                | {"dispatcher": code_commit()}),
        resumed_from=ledger.previous_in_session(session, attempt_id),
        work_units=work_units(job["stage"], json.loads(job["input"]),
                              ordered_batches(worktree, run["diocese"])),
        gaps=gaps + tokens.gaps,
        **(tokens.columns() | {"models": models, "model": tokens.model or info.get("model")}))
