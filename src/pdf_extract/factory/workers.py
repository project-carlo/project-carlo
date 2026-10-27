"""Workers: a fresh Agent SDK session per job, or a stub that writes canned handoffs.

A worker runs in the Run's worktree in auto mode, on one account's Claude login, without
GitHub or git credentials, and can't start other agents. It ends with a handoff file;
everything else about the attempt (steps, cost, how it ended) comes back here.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from pdf_extract.factory.config import Account
from pdf_extract.factory.stages import StageSpec, fill

# How an attempt ended.
OK, CRASH, USAGE, TIMEOUT, PARTIAL = "ok", "crash", "usage", "timeout", "partial"

# Workers never commit, push, use gh or move HEAD; the dispatcher does.
DENIED = [
    "Agent", "Task",
    "Bash(git commit:*)", "Bash(git push:*)", "Bash(gh:*)", "Bash(git reset:*)",
    "Bash(git checkout:*)", "Bash(git switch:*)", "Bash(git rebase:*)", "Bash(git merge:*)",
    "Bash(git stash:*)",
]

OnStep = Callable[[str, str | None, str | None], None]


@dataclass
class WorkerRequest:
    job_id: int
    run_id: str
    job_name: str
    stage: str
    spec: StageSpec
    worktree: Path
    account: Account | None
    prompt: str
    system_append: str
    values: dict[str, str]
    session_id: str | None = None  # resume this session
    on_step: OnStep = field(default=lambda kind, name, detail: None)


@dataclass
class WorkerResult:
    outcome: str
    session_id: str | None = None
    cost_usd: float = 0.0
    turns: int = 0
    error: str | None = None
    resets_at: datetime | None = None
    transcript: Path | None = None


class Worker(Protocol):
    def run(self, request: WorkerRequest) -> WorkerResult: ...


def prompt_body(worktree: Path, path: str | None) -> str:
    """A stage's prompt file without its frontmatter (an agent file's model, tools...)."""
    if not path:
        return ""
    text = (worktree / path).read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5:]
    return text.strip()


def worker_env(account: Account | None) -> dict[str, str]:
    """No GitHub token, no git credentials, the account's Claude login, not an API key."""
    empty = Path(tempfile.gettempdir()) / "carlo-factory-empty-gh"
    empty.mkdir(exist_ok=True)
    env = {
        "GH_TOKEN": "", "GITHUB_TOKEN": "", "GH_CONFIG_DIR": str(empty),
        "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "", "SSH_ASKPASS": "",
        "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "credential.helper", "GIT_CONFIG_VALUE_0": "",
        "ANTHROPIC_API_KEY": "", "CARLO_FACTORY_WORKER": "1",
    }
    if account is not None:
        env["CLAUDE_CONFIG_DIR"] = str(account.config_dir)
    return env


def find_transcript(account: Account | None, session_id: str | None) -> Path | None:
    if not session_id:
        return None
    base = account.config_dir if account else Path(os.environ.get(
        "CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    return next(iter((base / "projects").glob(f"*/{session_id}.jsonl")), None)


class SdkWorker:
    """A Claude Agent SDK session (`claude_agent_sdk.query`) running the stage spec."""

    def run(self, request: WorkerRequest) -> WorkerResult:
        try:
            return asyncio.run(asyncio.wait_for(
                self._run(request), timeout=request.spec.max_minutes * 60))
        except TimeoutError:
            return WorkerResult(TIMEOUT, session_id=self._session, error="over max_minutes",
                                cost_usd=self._cost, turns=self._turns)
        except Exception as exc:  # the SDK or the CLI died: resume the session
            return WorkerResult(CRASH, session_id=self._session, error=repr(exc)[:2000],
                                cost_usd=self._cost, turns=self._turns)

    async def _run(self, request: WorkerRequest) -> WorkerResult:
        from claude_agent_sdk import (
            AssistantMessage,
            ClaudeAgentOptions,
            RateLimitEvent,
            ResultMessage,
            SystemMessage,
            TextBlock,
            ToolUseBlock,
            query,
        )

        spec = request.spec
        self._session, self._cost, self._turns = request.session_id, 0.0, 0
        tools = list(spec.tools) + (["Skill"] if spec.skills else [])
        options = ClaudeAgentOptions(
            cwd=str(request.worktree),
            model=spec.model,
            effort=spec.effort,
            permission_mode="auto",
            tools=tools,
            disallowed_tools=DENIED,
            system_prompt={"type": "preset", "preset": "claude_code",
                           "append": request.system_append},
            setting_sources=["project"],
            skills=list(spec.skills) or None,
            max_turns=spec.max_turns,
            resume=request.session_id,
            env=worker_env(request.account),
        )
        result = WorkerResult(CRASH, session_id=request.session_id, error="no result")
        n = 0
        async for message in query(prompt=request.prompt, options=options):
            if isinstance(message, SystemMessage) and message.subtype == "init":
                self._session = message.data.get("session_id") or self._session
            elif isinstance(message, AssistantMessage):
                if message.error == "rate_limit":
                    result = WorkerResult(USAGE, error="rate limit")
                for block in message.content:
                    n += 1
                    if isinstance(block, ToolUseBlock):
                        request.on_step("tool", block.name, json.dumps(block.input)[:500])
                    elif isinstance(block, TextBlock):
                        request.on_step("text", None, block.text[:500])
            elif isinstance(message, RateLimitEvent):
                info = message.rate_limit_info
                request.on_step("rate_limit", info.rate_limit_type, info.status)
                if info.status == "rejected":
                    resets = (datetime.fromtimestamp(info.resets_at, UTC)
                              if info.resets_at else None)
                    result = WorkerResult(USAGE, error="rate limit", resets_at=resets)
            elif isinstance(message, ResultMessage):
                self._session = message.session_id
                self._cost, self._turns = message.total_cost_usd or 0.0, message.num_turns
                if result.outcome == USAGE or message.api_error_status == 429:
                    result = WorkerResult(USAGE, error="rate limit", resets_at=result.resets_at)
                elif message.subtype == "error_max_turns":
                    result = WorkerResult(PARTIAL, error="max_turns")
                elif message.is_error:
                    result = WorkerResult(CRASH, error="; ".join(message.errors or [])
                                          or message.result or message.subtype)
                else:
                    result = WorkerResult(OK)
                request.on_step("result", message.subtype, (message.result or "")[:500])
        result.session_id, result.cost_usd, result.turns = self._session, self._cost, self._turns
        result.transcript = find_transcript(request.account, self._session)
        return result

    _session: str | None = None
    _cost: float = 0.0
    _turns: int = 0


# ── Stub workers: send-backs, parking and resuming without spending usage ────
@dataclass
class StubAction:
    """What a stub worker does on one attempt: write files and a handoff, then end."""

    handoff: dict[str, Any] | None = None
    # Paths may use {diocese}, {run}, {job}, {parish}; None deletes the file.
    files: dict[str, str | None] = field(default_factory=dict)
    outcome: str = OK
    resets_at: datetime | None = None


Script = Callable[[WorkerRequest, int], StubAction]


class StubWorker:
    """Plays a script: `script(request, attempt)` says what each attempt does.

    `attempt` counts this job's attempts from 1. Sessions are faked as `stub-<job>`,
    so resuming one is just the next attempt.
    """

    def __init__(self, script: Script) -> None:
        self.script = script
        self.calls: list[WorkerRequest] = []

    def run(self, request: WorkerRequest) -> WorkerResult:
        self.calls.append(request)
        attempt = sum(1 for r in self.calls if r.job_id == request.job_id)
        action = self.script(request, attempt)
        request.on_step("text", None, f"stub attempt {attempt}")
        for rel, content in action.files.items():
            path = request.worktree / fill(rel, request.values)
            if content is None:
                if path.exists():
                    path.unlink()
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        if action.handoff is not None:
            path = request.worktree / "scratch" / request.run_id / request.job_name / "handoff.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(action.handoff), encoding="utf-8")
        return WorkerResult(action.outcome, session_id=f"stub-{request.job_id}",
                            resets_at=action.resets_at)


def scenario_script(path: Path) -> Script:
    """A stub script from a JSON file, for `pnpm factory run --stub FILE`.

    `{"<stage>": [attempt 1, attempt 2, ...]}`, each attempt a StubAction's fields; a
    stage's last attempt repeats. A stage missing from the file finishes with a `done`
    handoff (reviewers approve everything, with no answers).
    """
    scenario: dict[str, list[dict[str, Any]]] = json.loads(path.read_text(encoding="utf-8"))

    def script(request: WorkerRequest, attempt: int) -> StubAction:
        steps = scenario.get(request.stage)
        if steps:
            raw = dict(steps[min(attempt, len(steps)) - 1])
            if raw.get("resets_at"):
                raw["resets_at"] = datetime.fromisoformat(raw["resets_at"])
            return StubAction(**raw)
        return StubAction(handoff=default_handoff(request))

    return script


def default_handoff(request: WorkerRequest) -> dict[str, Any]:
    handoff: dict[str, Any] = {"status": "done", "summary": f"stub {request.stage}"}
    if request.stage == "survey-review":
        handoff |= {"verdict": "approve"}
    if request.stage == "seed-review":
        parishes = request.values.get("parishes", "").split()
        handoff |= {"seeds": [{"parish": p, "verdict": "approve"} for p in parishes]}
    return handoff


def copy_transcript(result: WorkerResult, dest_dir: Path) -> Path | None:
    if result.transcript is None or not result.transcript.exists():
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{result.session_id}.jsonl"
    shutil.copyfile(result.transcript, dest)
    return dest
