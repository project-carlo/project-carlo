"""The dispatcher: picks the next job, checks usage, starts workers, runs gates, retries (§5).

One Run is active at a time, and one job runs at a time within it. Everything after a
job's gates is recorded in the ledger as it completes, so a dispatcher restarted partway
through skips what's done instead of committing or appending twice.
"""

from __future__ import annotations

import json
import logging
import shutil
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.factory import forge as forge_mod
from pdf_extract.factory import git, inputs, playbook, readiness, report
from pdf_extract.factory.config import QUEUE_PATH, RUNS_DIR, Account, Config, FactoryError
from pdf_extract.factory.forge import Forge
from pdf_extract.factory.handoff import (
    APPROVE,
    BLOCKING,
    SEND_BACK,
    Handoff,
    SeedReview,
    SurveyReview,
    handoff_path,
    read_handoff,
)
from pdf_extract.factory.handoff import (
    PARTIAL as HANDOFF_PARTIAL,
)
from pdf_extract.factory.ledger import (
    ACTIVE,
    ANSWERED,
    BLOCKED,
    DONE,
    GATING,
    IN_REVIEW,
    JOB_BLOCKED,
    MAP,
    MERGED,
    OPEN,
    PENDING,
    QUEUED,
    RUNNING,
    SEED,
    SENT_BACK,
    SETTLED,
    WAITING_USAGE,
    Ledger,
    now,
)
from pdf_extract.factory.plan import diocese_dir, next_job
from pdf_extract.factory.stages import CODE, StageSpec, fill, in_scope, load_stage, placeholders
from pdf_extract.factory.usage import (
    Fetch,
    UsageError,
    choose,
    fetch_usage,
    next_eligible,
    standings,
)
from pdf_extract.factory.workers import (
    CRASH,
    OK,
    PARTIAL,
    TIMEOUT,
    USAGE,
    Worker,
    WorkerRequest,
    copy_transcript,
    prompt_body,
)

LOGGER = logging.getLogger(__name__)
MAX_CRASHES = 3
REGENERATE = "pnpm --silent diocese promote {diocese}"


@dataclass
class Outcome:
    """What one tick did, for the log and the tests."""

    action: str  # idle | paused | waiting | ran | blocked
    detail: str = ""
    wait_until: datetime | None = None


def main_queue(repo: Path, upstream: str) -> list[dict[str, Any]]:
    """The queue as main has it (a PR edits it), else this checkout's copy."""
    try:
        text = git.git(repo, "show", f"{upstream}:{QUEUE_PATH.as_posix()}")
    except FactoryError:
        text = QUEUE_PATH.read_text(encoding="utf-8") if QUEUE_PATH.exists() else "[]"
    return json.loads(text)


def run_command(command: str, cwd: Path, timeout: int = 3600) -> tuple[bool, str]:
    try:
        proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    return proc.returncode == 0, (proc.stdout + proc.stderr)[-6000:]


class Dispatcher:
    def __init__(
        self,
        ledger: Ledger,
        config: Config,
        *,
        repo: Path,
        worker: Worker,
        forge: Forge,
        fetch_usage: Fetch = fetch_usage,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
        commands: Callable[[str, Path], tuple[bool, str]] = run_command,
        db_path: Path = Path("data") / "parish_events.db",
        runs_dir: Path = RUNS_DIR,
        queue_path: Path | None = None,
        pull_data: Callable[[], None] | None = None,
        backup: Callable[[], str] | None = None,
        push: bool = True,
    ) -> None:
        self.ledger, self.config, self.repo = ledger, config, repo
        self.worker, self.forge, self.fetch_usage = worker, forge, fetch_usage
        self.clock, self.commands = clock, commands
        self.db_path, self.runs_dir, self.queue_path = db_path, runs_dir, queue_path
        self.pull_data, self.backup, self.push_enabled = pull_data, backup, push

    # ── The loop ────────────────────────────────────────────────────────────
    def run_forever(self) -> None:
        self._recover()
        while True:
            outcome = self.tick()
            LOGGER.info("%s %s", outcome.action, outcome.detail)
            if outcome.action == "ran":
                continue
            pause = self.config.tick_seconds
            if outcome.wait_until is not None:
                pause = max(5, min(pause, (outcome.wait_until - self.clock()).total_seconds()))
            time.sleep(pause)

    def _recover(self) -> None:
        """A job still marked running when the dispatcher starts crashed with it."""
        for row in self.ledger.all("SELECT id FROM job WHERE status = ?", RUNNING):
            self.ledger.set_job(row["id"], status=QUEUED, pending_prompt=json.dumps(
                {"kind": "resume", "prompt": None}))

    def tick(self) -> Outcome:
        paused = self.ledger.get("paused")
        if paused:
            return Outcome("paused", paused.get("reason", ""))
        try:
            self.housekeeping()
        except FactoryError as exc:
            LOGGER.warning("housekeeping: %s", exc)
        job = self.pick()
        if job is None:
            return Outcome("idle")
        if job["status"] == WAITING_USAGE and job["wait_until"] \
                and not self.ledger.get("override_caps", False):
            until = datetime.fromisoformat(job["wait_until"])
            if until > self.clock():
                return Outcome("waiting", f"job {job['id']} until {job['wait_until']}", until)
        return self.work(job)

    # ── Picking (§3) ────────────────────────────────────────────────────────
    def pick(self) -> Any | None:
        for _ in range(4):
            active = self.ledger.runs(ACTIVE)
            if active:
                run = active[0]
                job = self.ledger.unfinished_job(run["id"])
                if job is not None:
                    return job
                try:
                    self._worktree(run)  # the plan reads the Run's files
                except FactoryError as exc:
                    self._block_run(run, None, f"Can't set up the Run's worktree: {exc}")
                    continue
                nxt = next_job(self.ledger, run,
                               lessons_before_integrate=self.config.lessons_before_integrate)
                if nxt is not None:
                    return self.ledger.job(self.ledger.add_job(run["id"], nxt.stage, nxt.inputs))
                self.ledger.set_run(run["id"], status=IN_REVIEW)
                continue
            if self._activate_answered() or self._activate_pending() or self._start_from_queue():
                continue
            return None
        return None

    def _activate_answered(self) -> bool:
        for run in self.ledger.runs(BLOCKED):
            run_flags = [f for f in self.ledger.flags(run["id"], OPEN, ANSWERED)
                         if f["scope"] == "run"]
            if run_flags:
                continue
            self.ledger.set_run(run["id"], status=ACTIVE, blocked_reason=None)
            return True
        return False

    def _activate_pending(self) -> bool:
        """A ready seed Run, or a follow-up whose Run has merged."""
        for run in self.ledger.runs(PENDING):
            parent = run["follow_up_of"]
            if parent and self.ledger.run(parent)["status"] != MERGED:
                continue
            self.ledger.set_run(run["id"], status=ACTIVE)
            return True
        return False

    def queue(self) -> list[dict[str, Any]]:
        if self.queue_path is not None:
            return json.loads(self.queue_path.read_text(encoding="utf-8")
                              if self.queue_path.exists() else "[]")
        return main_queue(self.repo, self.config.upstream)

    def _start_from_queue(self) -> bool:
        mapped = {r["diocese"] for r in self.ledger.runs() if r["kind"] == MAP}
        for item in self.queue():
            if item["diocese"] not in mapped:
                self.ledger.add_run(diocese=item["diocese"], kind=MAP,
                                    worktrees_dir=self.config.worktrees_dir,
                                    notes=item.get("notes", ""))
                return True
        return False

    # ── One job ─────────────────────────────────────────────────────────────
    def _worktree(self, run: Any) -> Path:
        path = Path(run["worktree"])
        created = git.ensure_worktree(self.repo, path, run["branch"], remote=self.config.remote,
                                      base=self.config.upstream)
        if created:
            if self.db_path.exists():
                (path / "data").mkdir(exist_ok=True)
                shutil.copyfile(self.db_path, path / "data" / self.db_path.name)
            for command in self.config.setup:
                ok, out = self.commands(command, path)
                if not ok:
                    raise FactoryError(f"setup `{command}` failed in {path}: {out[-500:]}")
        return path

    def values(self, run: Any, job: Any) -> dict[str, str]:
        data = json.loads(job["input"])
        approved = self.ledger.get(f"approved:{job['id']}", [])
        return {
            "diocese": run["diocese"], "run": run["id"], "job": job["name"],
            "branch": run["branch"], "parish": data.get("parish", ""),
            "parishes": " ".join(data.get("parishes") or []), "approved": " ".join(approved),
        }

    def work(self, job: Any) -> Outcome:
        run = self.ledger.run(job["run_id"])
        try:
            worktree = self._worktree(run)
        except FactoryError as exc:
            return self._block_run(run, job, f"Can't set up the Run's worktree: {exc}")
        spec = load_stage(job["stage"], worktree)
        if job["status"] == GATING:
            return self._gate(run, self.ledger.job(job["id"]), spec, worktree)
        if job["status"] == QUEUED and not self._attempts(job["id"]):
            merged = self._merge_main(run, job, worktree)
            if merged is not None:
                return merged
        if spec.kind == CODE:
            return self._code(run, job, spec, worktree)
        return self._attempt(run, job, spec, worktree)

    def _attempts(self, job_id: int) -> list[Any]:
        return self.ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", job_id)

    def _merge_main(self, run: Any, job: Any, worktree: Path) -> Outcome | None:
        """At the start of a stage, merge main into the Run branch if it has moved (§10)."""
        if job["stage"] == "pr":
            return None
        done = [j for j in self.ledger.jobs(run["id"]) if j["status"] == DONE]
        if done and done[-1]["stage"] == job["stage"]:
            return None
        git.fetch(worktree, self.config.remote)
        merge = git.merge_upstream(worktree, self.config.upstream)
        if merge.conflicts:
            return self._block_run(run, job, "Merging main into the Run branch conflicts in: "
                                   + ", ".join(merge.conflicts), suggestion="Resolve the merge "
                                   "on the Run branch by hand, push it, then close this issue.")
        if merge.repromote and run["kind"] == MAP:
            ok, out = self.commands(fill(REGENERATE, {"diocese": run["diocese"]}), worktree)
            if not ok:
                return self._block_run(run, job, f"Promoting again after merging main failed:\n"
                                       f"{out[-1500:]}")
            git.commit(worktree, f"{run['diocese']}: promote again after merging main",
                       {"Factory-Run": run["id"]})
        if merge.merged:
            self._push(run, worktree)
        return None

    def _account(self, job: Any) -> tuple[Account | None, Outcome | None]:
        if not self.config.accounts:
            return None, None  # stub runs and tests: no usage to check
        override = self.ledger.get("override_caps", False)
        try:
            rows = standings(self.config, self.fetch_usage, self.clock())
        except UsageError as exc:
            self.ledger.set("paused", {"reason": f"usage check failed: {exc}", "at": now()})
            return None, Outcome("paused", str(exc))
        for s in rows:
            self.ledger.run_sql(
                "INSERT INTO usage (account, at, five_hour, five_hour_resets, seven_day, "
                "seven_day_resets) VALUES (?,?,?,?,?,?)", s.account.name, now(),
                s.usage.five_hour, s.usage.five_hour_resets.isoformat(), s.usage.seven_day,
                s.usage.seven_day_resets.isoformat())
        only = job["account"]
        if override:
            pick = next((s for s in rows if only is None or s.account.name == only), None)
        else:
            pick = choose(rows, only=only)
        if pick is None:
            until = next_eligible(rows, only=only) or self.clock() + timedelta(minutes=30)
            self.ledger.set_job(job["id"], status=WAITING_USAGE, wait_until=until.isoformat())
            return None, Outcome("waiting", f"no account under its caps until {until}", until)
        return pick.account, None

    def _next_prompt(self, run: Any, job: Any, spec: StageSpec,
                     values: dict[str, str]) -> tuple[str, str, str | None]:
        """The attempt's kind, its prompt and the session it resumes."""
        rel = inputs.handoff_rel(run["id"], job["name"])
        pending = json.loads(job["pending_prompt"] or "null")
        if pending is None:
            if job["resumes_job"]:
                original = self.ledger.job(job["resumes_job"])
                data = json.loads(job["input"])
                if original["session_id"] and original["run_id"] == run["id"]:
                    return "answer", inputs.answer_prompt(
                        data.get("question", ""), data.get("answer", ""), rel,
                        data.get("subject", "the parish you set aside")), original["session_id"]
            return "start", inputs.job_input(self.ledger, run, job, spec, values), None
        if not job["session_id"]:
            first = self._attempts(job["id"])
            prompt = first[0]["prompt"] if first else inputs.job_input(
                self.ledger, run, job, spec, values)
            extra = pending.get("prompt")
            return "fresh", prompt + (f"\n\n{extra}" if extra else ""), None
        kind = pending["kind"]
        prompt = pending.get("prompt") or (inputs.continue_prompt(rel) if kind != "resume"
                                           else inputs.resume_prompt(rel))
        return kind, prompt, job["session_id"]

    def _attempt(self, run: Any, job: Any, spec: StageSpec, worktree: Path) -> Outcome:
        if job["resumes_job"] and job["account"] is None:
            original = self.ledger.job(job["resumes_job"])
            if original["account"] and original["run_id"] == run["id"]:
                # Its session can only be resumed from the account that stores it.
                self.ledger.set_job(job["id"], account=original["account"])
                job = self.ledger.job(job["id"])
        account, waiting = self._account(job)
        if waiting is not None:
            return waiting
        job = self.ledger.job(job["id"])
        values = self.values(run, job)
        kind, prompt, session = self._next_prompt(run, job, spec, values)
        commit_sha = git.head(worktree)
        attempt_id = self.ledger.add_attempt(job["id"], kind, prompt,
                                             account.name if account else None, commit_sha)
        self.ledger.set_job(job["id"], status=RUNNING, started_at=job["started_at"] or now(),
                            account=job["account"] or (account.name if account else None),
                            commit_sha=job["commit_sha"] or commit_sha, wait_until=None,
                            session_id=session or job["session_id"])
        steps = iter(range(1, 1_000_000))
        request = WorkerRequest(
            job_id=job["id"], run_id=run["id"], job_name=job["name"], stage=job["stage"],
            spec=spec, worktree=worktree, account=account, prompt=prompt,
            system_append=prompt_body(worktree, spec.prompt), values=values, session_id=session,
            on_step=lambda k, name, detail: self.ledger.add_step(attempt_id, next(steps), k,
                                                                 name, detail),
        )
        result = self.worker.run(request)
        transcript = copy_transcript(result, self.runs_dir / run["id"] / job["name"])
        self.ledger.finish_attempt(attempt_id, outcome=result.outcome, error=result.error,
                                   cost_usd=result.cost_usd, turns=result.turns,
                                   session_id=result.session_id,
                                   transcript=str(transcript) if transcript else None)
        job = self.ledger.job(job["id"])
        self.ledger.set_job(job["id"], cost_usd=job["cost_usd"] + result.cost_usd,
                            turns=job["turns"] + result.turns,
                            session_id=result.session_id or job["session_id"])
        job = self.ledger.job(job["id"])
        if result.outcome == USAGE:
            until = result.resets_at or self.clock() + timedelta(minutes=30)
            self.ledger.set_job(job["id"], status=WAITING_USAGE, wait_until=until.isoformat(),
                                pending_prompt=json.dumps({"kind": "continue", "prompt": None}))
            return Outcome("waiting", f"job {job['id']} hit a usage limit", until)
        if result.outcome == CRASH:
            if session and result.turns == 0:
                # The session couldn't be resumed: a fresh worker gets the files on disk.
                self.ledger.set_job(job["id"], session_id=None)
            crashes = sum(1 for a in self._attempts(job["id"]) if a["outcome"] == CRASH)
            if crashes >= MAX_CRASHES:
                return self._block_run(run, job, f"The worker crashed {crashes} times: "
                                       f"{result.error}")
            self.ledger.set_job(job["id"], status=QUEUED,
                                pending_prompt=json.dumps({"kind": "resume", "prompt": None}))
            return Outcome("ran", f"job {job['id']} crashed; resuming")
        if result.outcome in (PARTIAL, TIMEOUT):
            return self._partial(run, job, f"the session ended early ({result.outcome})")
        assert result.outcome == OK
        self.ledger.set_job(job["id"], status=GATING, pending_prompt=None)
        return self._gate(run, self.ledger.job(job["id"]), spec, worktree)

    def _partial(self, run: Any, job: Any, why: str) -> Outcome:
        if job["continues"] < 1:
            self.ledger.set_job(job["id"], status=SENT_BACK, continues=job["continues"] + 1,
                                pending_prompt=json.dumps({"kind": "continue", "prompt": None}))
            return Outcome("ran", f"job {job['id']} partial; continuing")
        return self._exhausted(run, job, [f"The job stopped partway twice: {why}."])

    # ── Gates ───────────────────────────────────────────────────────────────
    def _gate(self, run: Any, job: Any, spec: StageSpec, worktree: Path) -> Outcome:
        if self.ledger.done_action(job["id"], "gates"):
            handoff, _ = read_handoff(handoff_path(worktree, run["id"], job["name"]), job["stage"])
            assert handoff is not None
            return self._finish(run, job, spec, worktree, handoff)
        values = self.values(run, job)
        problems: list[str] = []
        attempts = self._attempts(job["id"])
        attempt = attempts[-1]["id"] if attempts else None
        start = attempts[-1]["commit_sha"] if attempts else None  # HEAD when it started
        if start and git.head(worktree) != start:
            git.git(worktree, "reset", "--soft", start)
            problems.append("HEAD moved during the job: workers don't commit. Your changes are "
                            "kept, uncommitted.")
        handoff, handoff_problems = read_handoff(
            handoff_path(worktree, run["id"], job["name"]), job["stage"])
        self.ledger.add_gate(job["id"], attempt, "handoff", not handoff_problems,
                             "\n".join(handoff_problems) or "ok")
        problems += handoff_problems
        writes = [fill(w, values) for w in spec.writes]
        outside = [p for p in git.changed_paths(worktree) if not in_scope(p, writes)]
        self.ledger.add_gate(job["id"], attempt, "diff-scope", not outside,
                             "\n".join(outside) or "ok")
        if outside:
            git.revert(worktree, outside)
            problems.append("You changed files outside your write boundaries; they were "
                            "reverted: " + ", ".join(outside))
        if handoff is not None and not problems:
            problems += self._coverage_problems(job, handoff)
        if handoff is not None and not problems and handoff.status == HANDOFF_PARTIAL:
            return self._partial(run, job, "the handoff says partial")
        run_blocked = handoff is not None and any(
            f.severity == BLOCKING and f.scope == "run" for f in handoff.flags)
        if not problems and not run_blocked and job["stage"] != "seed-review":
            problems += self._stage_gates(job, spec, values, worktree, attempt)
        if problems:
            return self._send_back(run, job, problems)
        self.ledger.record_action(job["id"], "gates")
        assert handoff is not None
        return self._finish(run, job, spec, worktree, handoff)

    def _coverage_problems(self, job: Any, handoff: Handoff) -> list[str]:
        """A seed-review gives every parish a verdict or a blocking flag."""
        if not isinstance(handoff, SeedReview):
            return []
        wanted = set(json.loads(job["input"]).get("parishes") or [])
        covered = {v.parish for v in handoff.seeds} | {
            f.subject for f in handoff.flags if f.severity == BLOCKING}
        problems = [f"no verdict or blocking flag for {p}" for p in sorted(wanted - covered)]
        problems += [f"{v.parish} is not one of the seeds to review" for v in handoff.seeds
                     if v.parish not in wanted]
        return problems

    def _stage_gates(self, job: Any, spec: StageSpec, values: dict[str, str], worktree: Path,
                     attempt: int | None) -> list[str]:
        problems = []
        for gate in spec.gates:
            if any(not values.get(name) for name in placeholders(gate)):
                continue  # e.g. no approved seeds to check
            command = fill(gate, values)
            ok, out = self.commands(command, worktree)
            self.ledger.add_gate(job["id"], attempt, command, ok, out)
            if not ok:
                problems.append(f"`{command}` failed:\n{out[-2000:]}")
        return problems

    def _send_back(self, run: Any, job: Any, problems: list[str]) -> Outcome:
        if job["send_backs"] >= self.config.max_send_backs:
            return self._exhausted(run, job, problems)
        rel = inputs.handoff_rel(run["id"], job["name"])
        self.ledger.set_job(job["id"], status=SENT_BACK, send_backs=job["send_backs"] + 1,
                            pending_prompt=json.dumps({
                                "kind": "send_back",
                                "prompt": inputs.send_back_prompt(problems, rel)}))
        return Outcome("ran", f"job {job['id']} sent back: {len(problems)} problems")

    def _exhausted(self, run: Any, job: Any, problems: list[str]) -> Outcome:
        """Past its send-backs: a seed parks its parish; anything else blocks the Run."""
        question = (f"Job {job['name']} ({job['stage']}) still has problems after "
                    f"{job['send_backs']} send-backs:\n\n" + "\n".join(f"- {p}" for p in problems))
        parish = json.loads(job["input"]).get("parish")
        if job["stage"] == "seed" and parish:
            flag = self.ledger.add_flag(run["id"], job["id"], severity=BLOCKING, scope="parish",
                                        subject=parish, question=question,
                                        suggestion="Answer how the drafter should fix it.")
            self._open_issue(run, job, flag)
            self.ledger.set_job(job["id"], status=JOB_BLOCKED, finished_at=now())
            return Outcome("blocked", f"parked {parish}")
        return self._block_run(run, job, question)

    def _block_run(self, run: Any, job: Any | None, question: str, suggestion: str = "") -> Outcome:
        flag = self.ledger.add_flag(run["id"], job["id"] if job else None, severity=BLOCKING,
                                    scope="run", subject=run["id"], question=question,
                                    suggestion=suggestion)
        self._open_issue(run, job, flag)
        if job is not None:
            self.ledger.set_job(job["id"], status=JOB_BLOCKED)
        self.ledger.set_run(run["id"], status=BLOCKED, blocked_reason=question[:500])
        return Outcome("blocked", question[:200])

    def _open_issue(self, run: Any, job: Any | None, flag_id: int) -> None:
        flag = self.ledger.one("SELECT * FROM flag WHERE id = ?", flag_id)
        if flag["issue_number"]:
            return
        stage = job["stage"] if job else "dispatcher"
        title = f"[factory] {run['id']}: {flag['subject']}: {flag['question'].splitlines()[0]}"
        number = self.forge.open_issue(
            title[:120], forge_mod.issue_body(flag, run, job),
            ["factory", f"run:{run['diocese']}", f"stage:{stage}"])
        self.ledger.run_sql("UPDATE flag SET issue_number = ? WHERE id = ?", number, flag_id)

    # ── After the gates: each action once ────────────────────────────────────
    def _once(self, job: Any, name: str, fn: Callable[[], Any]) -> None:
        if self.ledger.done_action(job["id"], name):
            return
        result = fn()
        self.ledger.record_action(job["id"], name, result)

    def _finish(self, run: Any, job: Any, spec: StageSpec, worktree: Path,
                handoff: Handoff) -> Outcome:
        self.ledger.set_job(job["id"], handoff=handoff.model_dump_json())
        job = self.ledger.job(job["id"])
        self._once(job, "verdicts", lambda: self._verdicts(run, job, worktree, handoff))
        if job["stage"] == "seed-review":
            values = self.values(run, job)
            if self.ledger.get(f"approved:{job['id']}"):
                problems = self._stage_gates(job, spec, values, worktree, None)
                if problems:
                    return self._block_run(run, job, "Approved seeds fail their check:\n"
                                           + "\n".join(problems))
        self._once(job, "lessons", lambda: self._lessons(run, job, worktree, handoff))
        self._once(job, "leads", lambda: [self.ledger.run_sql(
            "INSERT INTO lead (run_id, job_id, touches, note) VALUES (?,?,?,?)",
            run["id"], job["id"], lead.touches, lead.note) for lead in handoff.leads] and None)
        self._once(job, "flags", lambda: self._flags(run, job, handoff))
        self._once(job, "commit", lambda: git.commit(
            worktree, self._subject(run, job),
            {"Factory-Job": f"{run['id']}/{job['name']}", "Factory-Stage": job["stage"]}))
        self._once(job, "push", lambda: self._push(run, worktree))
        run_flag = any(f.severity == BLOCKING and f.scope == "run" for f in handoff.flags)
        self.ledger.set_job(job["id"], status=JOB_BLOCKED if run_flag else DONE,
                            finished_at=now())
        if run_flag:
            self.ledger.set_run(run["id"], status=BLOCKED, blocked_reason="a worker's blocking flag")
            return Outcome("blocked", f"job {job['id']} raised a Run-level flag")
        return Outcome("ran", f"job {job['id']} {job['stage']} done")

    def _subject(self, run: Any, job: Any) -> str:
        data = json.loads(job["input"])
        what = data.get("batch") or data.get("parish") or ""
        return f"{run['diocese']}: {job['stage']}{f' {what}' if what else ''} ({run['id']})"

    def _push(self, run: Any, worktree: Path) -> None:
        if self.push_enabled:
            git.push(worktree, self.config.remote, run["branch"])

    def _lessons(self, run: Any, job: Any, worktree: Path, handoff: Handoff) -> list[str]:
        known = {r["text"] for r in self.ledger.all("SELECT text FROM lesson WHERE job_id = ?",
                                                    job["id"])}
        for text in handoff.lessons:
            if text not in known:
                self.ledger.run_sql("INSERT INTO lesson (run_id, job_id, stage, text) VALUES "
                                    "(?,?,?,?)", run["id"], job["id"], job["stage"], text)
        if job["stage"] != "map" or not handoff.lessons:
            return []
        meta = diocese_dir(worktree, run["diocese"]) / "diocese.md"
        return playbook.append(meta, playbook.NEW_LESSONS, handoff.lessons)

    def _flags(self, run: Any, job: Any, handoff: Handoff) -> None:
        existing = {(f["subject"], f["question"]) for f in self.ledger.all(
            "SELECT * FROM flag WHERE job_id = ?", job["id"])}
        for f in handoff.flags:
            if (f.subject, f.question) in existing:
                continue
            self.ledger.add_flag(run["id"], job["id"], severity=f.severity, scope=f.scope,
                                 subject=f.subject, question=f.question, evidence=f.evidence,
                                 suggestion=f.suggestion)
        for row in self.ledger.all("SELECT * FROM flag WHERE job_id = ? AND severity = ? "
                                   "AND issue_number IS NULL", job["id"], BLOCKING):
            self._open_issue(run, job, row["id"])

    # ── Reviewer verdicts (§8) ───────────────────────────────────────────────
    def _verdicts(self, run: Any, job: Any, worktree: Path, handoff: Handoff) -> Any:
        if isinstance(handoff, SurveyReview):
            return self._survey_verdict(run, job, worktree, handoff)
        if isinstance(handoff, SeedReview):
            return self._seed_verdicts(run, job, worktree, handoff)
        return None

    def _verdict_row(self, job: Any, reviewed: int | None, subject: str, verdict: str,
                     problems: list[str]) -> None:
        self.ledger.run_sql("INSERT INTO verdict (job_id, reviewed_job, subject, verdict, "
                            "problems, at) VALUES (?,?,?,?,?,?)", job["id"], reviewed, subject,
                            verdict, json.dumps(problems), now())

    def _survey_verdict(self, run: Any, job: Any, worktree: Path, review: SurveyReview) -> Any:
        survey = int(json.loads(job["input"])["survey_job"])
        self._verdict_row(job, survey, run["diocese"], review.verdict, review.problems)
        if review.verdict == APPROVE:
            meta = diocese_dir(worktree, run["diocese"]) / "diocese.md"
            stamp = f"(accepted by survey-review, {job['name']}, {now()[:10]})"
            return playbook.append(meta, playbook.RULES, [f"{r} {stamp}" for r in review.rules])
        self._send_back_to(run, self.ledger.job(survey), review.problems)
        return None

    def _send_back_to(self, run: Any, reviewed: Any, problems: list[str]) -> None:
        """A reviewer's send-back goes to the session that did the work, and counts there."""
        if reviewed["send_backs"] >= self.config.max_send_backs:
            self._exhausted(run, reviewed, problems)
            return
        rel = inputs.handoff_rel(run["id"], reviewed["name"])
        self.ledger.clear_actions(reviewed["id"])
        self.ledger.set_job(reviewed["id"], status=SENT_BACK, send_backs=reviewed["send_backs"] + 1,
                            pending_prompt=json.dumps({
                                "kind": "send_back",
                                "prompt": "A reviewer sent your work back.\n\n"
                                          + inputs.send_back_prompt(problems, rel)}))

    def _seed_job(self, run: Any, parish: str) -> Any | None:
        jobs = [j for j in self.ledger.jobs(run["id"], "seed")
                if json.loads(j["input"]).get("parish") == parish]
        return jobs[-1] if jobs else None

    def _seed_verdicts(self, run: Any, job: Any, worktree: Path, review: SeedReview) -> Any:
        approved: list[str] = []
        reviewer = f"agent:seed-review@{(job['commit_sha'] or 'unknown')[:12]}"
        scratch = handoff_path(worktree, run["id"], job["name"]).parent
        for verdict in review.seeds:
            drafted = self._seed_job(run, verdict.parish)
            problems = list(verdict.problems)
            if verdict.verdict == APPROVE:
                seed = _read_seed(worktree, verdict.parish)
                answers = [a.model_dump(exclude_none=True) for a in verdict.answers]
                path = scratch / f"answers-{verdict.parish}.json"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(json.dumps(answers, indent=1), encoding="utf-8")
                ok, out = self.commands(
                    f"pnpm seed approve {verdict.parish} --reviewer {reviewer} --answers "
                    f"{path.relative_to(worktree).as_posix()}", worktree)
                if ok:
                    approved.append(verdict.parish)
                    self._verdict_row(job, drafted["id"] if drafted else None, verdict.parish,
                                      APPROVE, [])
                    self._decisions(run, job, worktree, verdict, seed)
                    continue
                problems = [f"`pnpm seed approve` refused the reviewer's answers: {out[-1500:]}"]
            self._verdict_row(job, drafted["id"] if drafted else None, verdict.parish,
                              SEND_BACK, problems)
            if drafted is not None:
                self._send_back_to(run, drafted, problems)
        self.ledger.set(f"approved:{job['id']}", approved)
        return approved

    def _decisions(self, run: Any, job: Any, worktree: Path, verdict: Any,
                   seed: dict[str, Any] | None) -> None:
        slots = {s.get("id"): s for s in (seed or {}).get("slots", [])}
        precedents = []
        for a in verdict.answers:
            slot = slots.get(a.slot, {})
            options = slot.get("options") or []
            lean = next((i for i, o in enumerate(options) if o.get("leaning")), None)
            if isinstance(a.choice, int):
                against = a.choice != lean
                chosen = options[a.choice].get("label", str(a.choice)) \
                    if 0 <= a.choice < len(options) else str(a.choice)
            elif a.choice == "dropped":
                against = lean is None or options[lean].get("entry") is not None
                chosen = "leave it out"
            else:
                against, chosen = True, f"edited entry {json.dumps(a.entry)}"
            lean_label = options[lean].get("label") if lean is not None else None
            question = a.question or slot.get("question") or ""
            self.ledger.run_sql(
                "INSERT INTO decision (run_id, job_id, parish, slot, question, lean, choice, "
                "basis, why, against_lean) VALUES (?,?,?,?,?,?,?,?,?,?)", run["id"], job["id"],
                verdict.parish, a.slot, question, lean_label, chosen, a.basis, a.why, int(against))
            if a.basis == "judgment":
                precedents.append(f"{question} → {chosen}. {a.why} ({verdict.parish} {a.slot}; "
                                  f"{job['name']}, {now()[:10]})")
        if precedents:
            meta = diocese_dir(worktree, run["diocese"]) / "diocese.md"
            playbook.append(meta, playbook.PRECEDENTS, precedents)

    # ── Code stages ─────────────────────────────────────────────────────────
    def _code(self, run: Any, job: Any, spec: StageSpec, worktree: Path) -> Outcome:
        self.ledger.set_job(job["id"], status=RUNNING, started_at=job["started_at"] or now(),
                            commit_sha=job["commit_sha"] or git.head(worktree))
        if job["stage"] == "pr":
            return self._pr(run, job, worktree)
        values = self.values(run, job)
        for gate in spec.gates:
            command = fill(gate, values)
            ok, out = self.commands(command, worktree)
            self.ledger.add_gate(job["id"], None, command, ok, out)
            if not ok:
                return self._block_run(run, job, f"`{command}` failed in {job['stage']}:\n\n"
                                       f"```\n{out[-2500:]}\n```")
        self._once(job, "commit", lambda: git.commit(
            worktree, self._subject(run, job),
            {"Factory-Job": f"{run['id']}/{job['name']}", "Factory-Stage": job["stage"]}))
        self._once(job, "push", lambda: self._push(run, worktree))
        self.ledger.set_job(job["id"], status=DONE, finished_at=now())
        return Outcome("ran", f"job {job['id']} {job['stage']} done")

    def _pr(self, run: Any, job: Any, worktree: Path) -> Outcome:
        self._once(job, "push", lambda: self._push(run, worktree))
        title, body = report.pr_text(self.ledger, run, worktree, self.commands)
        url = self.forge.open_pr(worktree, run["branch"], self.config.base_branch, title, body)
        self.ledger.set_run(run["id"], status=IN_REVIEW, pr_url=url, head_sha=git.head(worktree))
        self.ledger.set_job(job["id"], status=DONE, finished_at=now())
        return Outcome("ran", f"opened {url}")

    # ── Housekeeping: issues, merges, readiness, backups ─────────────────────
    def housekeeping(self) -> None:
        at = self.clock()
        if self._due("issues_polled", timedelta(minutes=self.config.issue_poll_minutes), at):
            git.fetch(self.repo, self.config.remote)
            self.poll_issues()
            self.check_merged()
        if self._due("readiness_checked", timedelta(hours=self.config.readiness_check_hours), at):
            self.check_readiness()
        local = at.astimezone()
        if local.hour >= self.config.backup_hour and self.backup is not None \
                and self.ledger.get("backed_up") != local.date().isoformat():
            self.ledger.set("backup", self.backup())
            self.ledger.set("backed_up", local.date().isoformat())

    def _due(self, key: str, every: timedelta, at: datetime) -> bool:
        last = self.ledger.get(key)
        if last and at - datetime.fromisoformat(last) < every:
            return False
        self.ledger.set(key, at.isoformat())
        return True

    def poll_issues(self) -> None:
        for flag in self.ledger.all("SELECT * FROM flag WHERE status = ? AND issue_number IS "
                                    "NOT NULL ORDER BY id", OPEN):
            issue = self.forge.issue(flag["issue_number"])
            if issue.state.upper() != "CLOSED":
                continue
            text = forge_mod.answer(issue, self.config.owner, flag["suggestion"])
            if text is None:
                self.forge.reopen(flag["issue_number"], "Closed without an answer from the "
                                  "owner, so nothing changed. Comment with the answer (or "
                                  f"`{forge_mod.ACCEPT}`), then close the issue.")
                continue
            self.ledger.run_sql("UPDATE flag SET status = ?, answer = ?, answered_at = ? "
                                "WHERE id = ?", ANSWERED, text, now(), flag["id"])
        for flag in self.ledger.all("SELECT * FROM flag WHERE status = ? ORDER BY id", ANSWERED):
            self.act_on_answer(flag)

    def act_on_answer(self, flag: Any) -> None:
        run = self.ledger.run(flag["run_id"])
        job = self.ledger.job(flag["job_id"]) if flag["job_id"] else None
        if flag["scope"] == "run":
            if job is not None and job["status"] == JOB_BLOCKED:
                self._resume_blocked(run, job, flag)
            self.ledger.run_sql("UPDATE flag SET status = ? WHERE id = ?", SETTLED, flag["id"])
            return
        if job is None:
            self.ledger.run_sql("UPDATE flag SET status = ? WHERE id = ?", SETTLED, flag["id"])
            return
        data = json.loads(job["input"])
        subject = flag["subject"]
        requeued: dict[str, Any] = {"answer": flag["answer"], "question": flag["question"],
                                    "subject": subject, "flag": flag["id"]}
        if job["stage"] == "map":
            requeued |= {"batch": data.get("batch"), "entries": [subject]}
        elif job["stage"] == "seed":
            requeued |= {"parish": subject, "batch": data.get("batch")}
        elif job["stage"] == "seed-review":
            requeued |= {"parishes": [subject], "batch": data.get("batch")}
        else:
            requeued |= {"entries": [subject]}
        target = run
        if run["status"] in (IN_REVIEW, MERGED):
            target = self._follow_up(run, subject)
        self.ledger.add_job(target["id"], job["stage"], requeued, resumes_job=job["id"])
        self.ledger.run_sql("UPDATE flag SET status = ? WHERE id = ?", SETTLED, flag["id"])

    def _resume_blocked(self, run: Any, job: Any, flag: Any) -> None:
        rel = inputs.handoff_rel(run["id"], job["name"])
        prompt = inputs.answer_prompt(flag["question"], flag["answer"], rel, "this job")
        self.ledger.clear_actions(job["id"])
        self.ledger.set_job(job["id"], status=SENT_BACK, send_backs=0, continues=0,
                            pending_prompt=json.dumps({"kind": "answer", "prompt": prompt}))

    def _follow_up(self, run: Any, subject: str) -> Any:
        """The pending follow-up Run of the same kind that takes this parish (§3)."""
        for other in self.ledger.runs(PENDING):
            if other["follow_up_of"] == run["id"]:
                parishes = json.loads(other["parishes"] or "[]")
                if subject not in parishes:
                    self.ledger.set_run(other["id"], parishes=json.dumps(parishes + [subject]))
                return self.ledger.run(other["id"])
        run_id = self.ledger.add_run(diocese=run["diocese"], kind=run["kind"],
                                     worktrees_dir=self.config.worktrees_dir, status=PENDING,
                                     follow_up_of=run["id"], parishes=[subject],
                                     notes=f"Follow-up of {run['id']}")
        return self.ledger.run(run_id)

    def check_merged(self) -> None:
        for run in self.ledger.runs(IN_REVIEW):
            if run["head_sha"] and git.is_merged(self.repo, run["head_sha"], self.config.upstream):
                self.ledger.set_run(run["id"], status=MERGED, merged_at=now())

    def check_readiness(self) -> None:
        dioceses = readiness.dioceses_to_check(self.ledger)
        if not dioceses:
            return
        if self.pull_data is not None:
            self.pull_data()
        for diocese in dioceses:
            result = readiness.assess(self.ledger, self.config, diocese, self.db_path,
                                      self.clock())
            if result is None:
                continue
            if result.start:
                self.ledger.add_run(diocese=diocese, kind=SEED, status=PENDING,
                                    worktrees_dir=self.config.worktrees_dir,
                                    parishes=result.start,
                                    notes=f"{len(result.start)} parishes ready")
            for parish in result.overdue:
                key = f"overdue:{diocese}:{parish}"
                if self.ledger.get(key):
                    continue
                number = self.forge.open_issue(
                    f"[factory] {diocese}: {parish} has too few bulletins to seed",
                    f"{forge_mod.MARKER}\n`{parish}` was mapped with a bulletin source, but "
                    f"{self.config.seed_follow_up_weeks} weeks after the map Run merged the "
                    f"database still has fewer than {self.config.seed_ready_bulletins} of its "
                    "bulletins, so its bulletin source is probably broken. Fix its record "
                    "(`pnpm fetch:check --diocese ...`); it is seeded once it is ready.",
                    ["factory", f"run:{diocese}", "stage:seed"])
                self.ledger.set(key, number)


def _read_seed(worktree: Path, parish: str) -> dict[str, Any] | None:
    try:
        return json.loads((worktree / "data" / "seeds" / f"{parish}.json").read_text("utf-8"))
    except (OSError, ValueError):
        return None

