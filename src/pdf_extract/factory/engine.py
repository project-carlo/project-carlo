"""The engine: one job, from picking it to its gates and what follows them.

One Run is active at a time, and one job runs at a time within it. Everything after a
job's gates is recorded in the ledger as it completes, so a dispatcher restarted partway
through skips what's done instead of committing or appending twice.

The stage-specific branches (seed parking, reviewer verdicts, integrate's rules check, the
code stages) are here until each stage gets its own module.
"""

from __future__ import annotations

import json
import logging
import subprocess
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.factory import git, playbook, render, report
from pdf_extract.factory.answers import Answers
from pdf_extract.factory.attempts import Attempts, Ended
from pdf_extract.factory.backup import copy_database
from pdf_extract.factory.config import QUEUE_PATH, Config, FactoryError
from pdf_extract.factory.forge import Forge
from pdf_extract.factory.handoff import (
    APPROVE,
    BLOCKING,
    SEND_BACK,
    Handoff,
    Integrate,
    Reconcile,
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
    LISTED,
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
    pending,
)
from pdf_extract.factory.outcome import Outcome
from pdf_extract.factory.plan import diocese_dir, next_job, read_seed, seed_status
from pdf_extract.factory.secrets import Secrets, pick
from pdf_extract.factory.spec import CODE, StageSpec, fill, in_scope, load_stage, placeholders
from pdf_extract.factory.workers import CRASH, OK, PARTIAL, SANDBOX, TIMEOUT

LOGGER = logging.getLogger(__name__)
# What a git, gh or command call raises when it fails; a job's tick waits and tries again.
TRANSIENT = (FactoryError, OSError, subprocess.SubprocessError)
REGENERATE = "pnpm --silent diocese promote {diocese}"


def main_queue(repo: Path, upstream: str) -> list[dict[str, Any]]:
    """The queue as main has it (a PR edits it), else this checkout's copy."""
    try:
        text = git.git(repo, "show", f"{upstream}:{QUEUE_PATH.as_posix()}")
    except FactoryError:
        text = QUEUE_PATH.read_text(encoding="utf-8") if QUEUE_PATH.exists() else "[]"
    return json.loads(text)


class Engine:
    def __init__(self, ledger: Ledger, config: Config, *, repo: Path, forge: Forge,
                 attempts: Attempts, answers: Answers, clock: Callable[[], datetime],
                 commands: Callable[..., tuple[bool, str]], secrets: Secrets,
                 db_path: Path, queue_path: Path | None, push: bool) -> None:
        self.ledger, self.config, self.repo, self.forge = ledger, config, repo, forge
        self.attempts, self.answers = attempts, answers
        self.clock, self.commands = clock, commands
        self.secrets = secrets  # the dispatcher's .env; a stage's `gate_secrets:` pick
        self.db_path, self.queue_path, self.push_enabled = db_path, queue_path, push

    def run_job(self, job: Any) -> Outcome:
        """Take the job one step on: a job waiting on usage or a sandbox retry waits, and a
        git or GitHub failure is retried after `failure_retry_minutes`."""
        # A usage wait (which --override-caps skips), or a sandbox retry.
        if job["wait_until"] and (job["status"] == QUEUED or (
                job["status"] == WAITING_USAGE and not self.ledger.get("override_caps", False))):
            until = datetime.fromisoformat(job["wait_until"])
            if until > self.clock():
                return Outcome("waiting", f"job {job['id']} until {job['wait_until']}", until)
        key = f"failures:{job['id']}"
        try:
            outcome = self.work(job)
        except TRANSIENT as exc:
            return self._work_failed(job, key, exc)
        if self.ledger.get(key):
            self.ledger.set(key, 0)
        return outcome

    def _work_failed(self, job: Any, key: str, exc: Exception) -> Outcome:
        """git or GitHub failed partway through a job (a network blip, an expired login), or a
        file the stage reads is missing. Each step after the gates runs once, so trying the
        job again picks up where it stopped; after a few failures in a row the Run blocks on
        an issue instead."""
        LOGGER.warning("job %s failed: %s", job["id"], exc)
        failures = (self.ledger.get(key) or 0) + 1
        self.ledger.set(key, failures)
        job = self.ledger.job(job["id"])
        if job["status"] == RUNNING:
            # Its worker's result, if any, is lost: resume the session.
            self.ledger.set_job(job["id"], status=QUEUED, pending_prompt=pending("resume")
                                if job["session_id"] else job["pending_prompt"])
        if failures >= self.config.max_failures:
            # The Run blocks, not the job: once the issue is closed, the job carries on
            # from the step that failed instead of starting its worker again.
            self.ledger.set(key, 0)
            return self._block_run(self.ledger.run(job["run_id"]), None,
                                   f"Job {job['name']} ({job['stage']}) failed {failures} "
                                   f"times in a row: {exc}",
                                   suggestion="Fix what failed (git, GitHub, the network, or "
                                   "a stage spec's `reads:` on main), then close this issue "
                                   "to try the job again.")
        until = self.clock() + timedelta(minutes=self.config.failure_retry_minutes)
        return Outcome("waiting", f"job {job['id']} failed ({exc}); trying again", until)

    # ── Picking ─────────────────────────────────────────────────────────────
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
                                    branch_prefix=self.config.branch_prefix,
                                    notes=item.get("notes", ""))
                return True
        return False

    # ── One job ─────────────────────────────────────────────────────────────
    def _worktree(self, run: Any) -> Path:
        """The Run's worktree, set up: until its setup has passed once, a new or recreated
        worktree gets the database and the setup commands again."""
        path = Path(run["worktree"])
        created = git.ensure_worktree(self.repo, path, run["branch"], remote=self.config.remote,
                                      base=self.config.upstream)
        key = f"set_up:{run['id']}"
        if created or not self.ledger.get(key):
            self.ledger.set(key, False)
            if self.db_path.exists():
                (path / "data").mkdir(exist_ok=True)
                copy_database(self.db_path, path / "data" / self.db_path.name)
            for command in self.config.setup:
                ok, out = self.commands(command, path)
                if not ok:
                    raise FactoryError(f"setup `{command}` failed in {path}: {out[-500:]}")
            self.ledger.set(key, True)
        return path

    def values(self, run: Any, job: Any) -> dict[str, str]:
        return render.job_values(self.ledger, run, job)

    def work(self, job: Any) -> Outcome:
        run = self.ledger.run(job["run_id"])
        try:
            worktree = self._worktree(run)
        except FactoryError as exc:
            return self._block_run(run, job, f"Can't set up the Run's worktree: {exc}")
        # Merge first, so the job runs with the stage spec and prompt of the same commit.
        if job["status"] in (QUEUED, WAITING_USAGE) and not self._attempts(job["id"]):
            merged = self._merge_main(run, job, worktree)
            if merged is not None:
                return merged
        spec = load_stage(job["stage"], worktree)
        if job["status"] == GATING:
            return self._gate(run, self.ledger.job(job["id"]), spec, worktree)
        if spec.kind == CODE:
            return self._code(run, job, spec, worktree)
        return self._attempt(run, job, spec, worktree)

    def _attempts(self, job_id: int) -> list[Any]:
        return self.ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", job_id)

    def _attempt(self, run: Any, job: Any, spec: StageSpec, worktree: Path) -> Outcome:
        ended = self.attempts.run(run, job, spec, worktree)
        if not isinstance(ended, Ended):
            return ended
        job = ended.job
        if ended.outcome == CRASH:
            return self._block_run(run, job, ended.why)
        if ended.outcome == SANDBOX:
            return self._block_run(run, job, ended.why, suggestion="Fix the sandbox (Podman, "
                                   "the worker image or the egress proxy; see "
                                   "docs/factory.md), then close this issue. Workers never "
                                   "run on the host instead.")
        if ended.outcome in (PARTIAL, TIMEOUT):
            return self._partial(run, job, ended.why)
        assert ended.outcome == OK
        self.ledger.set_job(job["id"], status=GATING, pending_prompt=None)
        return self._gate(run, self.ledger.job(job["id"]), spec, worktree)

    def _merge_main(self, run: Any, job: Any, worktree: Path) -> Outcome | None:
        """At the start of a stage, merge main into the Run branch if it has moved."""
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

    def _partial(self, run: Any, job: Any, why: str) -> Outcome:
        if job["continues"] < self.config.max_continues:
            self.ledger.set_job(job["id"], status=SENT_BACK, continues=job["continues"] + 1,
                                pending_prompt=pending("continue"))
            return Outcome("ran", f"job {job['id']} partial; continuing")
        return self._exhausted(run, job, [f"The job stopped partway {job['continues'] + 1} "
                                          f"times: {why}."])

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
        outside = self._revert_outside(worktree, spec, values)
        # A sandboxed worker's changes that were never brought back (workspace.py).
        refused = json.loads(attempts[-1]["refused"] or "[]") if attempts else []
        self.ledger.add_gate(job["id"], attempt, "diff-scope", not outside and not refused,
                             "\n".join(outside + refused) or "ok")
        if outside:
            problems.append("You changed files outside your write boundaries; they were "
                            "reverted: " + ", ".join(outside))
        if refused:
            problems.append("Some of your changes were not kept: " + ", ".join(refused))
        if handoff is not None and not problems:
            problems += self._coverage_problems(job, handoff)
            problems += self._settled_problems(run, job, handoff)
            problems += self._rules_problems(run, worktree, handoff)
        if handoff is not None and not problems and handoff.status == HANDOFF_PARTIAL:
            return self._partial(run, job, "the handoff says partial")
        run_blocked = handoff is not None and any(
            f.severity == BLOCKING and f.scope == "run" for f in handoff.flags)
        parks_itself = job["stage"] == "seed" and handoff is not None and any(
            f.severity == BLOCKING and f.subject == values["parish"] for f in handoff.flags)
        if not problems and not run_blocked and not parks_itself \
                and job["stage"] != "seed-review":
            problems += self._stage_gates(job, spec, values, worktree, attempt)
        if problems:
            return self._send_back(run, job, problems)
        self.ledger.record_action(job["id"], "gates")
        assert handoff is not None
        return self._finish(run, job, spec, worktree, handoff)

    def _coverage_problems(self, job: Any, handoff: Handoff) -> list[str]:
        """A seed-review gives every parish a verdict."""
        if not isinstance(handoff, SeedReview):
            return []
        wanted = set(json.loads(job["input"]).get("parishes") or [])
        covered = {v.parish for v in handoff.seeds}
        problems = [f"no verdict for {p}" for p in sorted(wanted - covered)]
        problems += [f"{v.parish} is not one of the seeds to review" for v in handoff.seeds
                     if v.parish not in wanted]
        return problems

    def _settled_problems(self, run: Any, job: Any, handoff: Handoff) -> list[str]:
        """Reconcile settles only advisory flags other jobs of its Run raised."""
        if not isinstance(handoff, Reconcile):
            return []
        problems = []
        for s in handoff.settled:
            row = self.ledger.one("SELECT * FROM flag WHERE id = ?", s.flag)
            if (row is None or row["run_id"] != run["id"] or row["severity"] == BLOCKING
                    or row["job_id"] == job["id"]):
                problems.append(f"settled: flag {s.flag} is not one of the advisory flags in "
                                "your input; use the ids shown there, as in `[#12]`")
        return problems

    def _playbooks(self, run: Any, worktree: Path) -> tuple[str, str]:
        """`diocese.md` before the job (HEAD: the dispatcher hasn't committed it yet) and now."""
        rel = f"data/dioceses/{run['diocese']}/diocese.md"
        now = worktree / rel
        return (git.git(worktree, "show", f"HEAD:{rel}", check=False),
                now.read_text(encoding="utf-8") if now.exists() else "")

    def _rules_problems(self, run: Any, worktree: Path, handoff: Handoff) -> list[str]:
        """Integrate lists every *Rules settled* rule it merged or reworded, word for word,
        so the PR shows the owner each change; a rule can't leave the section unlisted."""
        if not isinstance(handoff, Integrate):
            return []
        before, after = ({playbook.rule_key(r): r for r in
                          playbook.items(playbook.section_of(text, playbook.RULES))}
                         for text in self._playbooks(run, worktree))
        listed = {playbook.rule_key(w) for c in handoff.rules_changed for w in c.was}
        problems = [f"rules_changed: this rule is gone from *Rules settled*, but no `was` lists "
                    f"it. List it word for word with the rule that replaces it, or put it "
                    f"back: {_clip(rule)}" for key, rule in before.items()
                    if key not in after and key not in listed]
        problems += [f"rules_changed: each `was` quotes a rule as *Rules settled* had it before "
                     f"your job, word for word; this matches none: {_clip(w)}"
                     for c in handoff.rules_changed for w in c.was
                     if playbook.rule_key(w) not in before]
        problems += [f"rules_changed: this `now` isn't a rule in *Rules settled*; copy it as you "
                     f"wrote it there: {_clip(c.now)}" for c in handoff.rules_changed
                     if playbook.rule_key(c.now) not in after]
        return problems

    def _revert_outside(self, worktree: Path, spec: StageSpec,
                        values: dict[str, str]) -> list[str]:
        """Revert every change outside the stage's write boundaries; returns those paths."""
        writes = [fill(w, values) for w in spec.writes]
        outside = [p for p in git.changed_paths(worktree) if not in_scope(p, writes)]
        if outside:
            git.revert(worktree, outside)
        return outside

    def _stage_gates(self, job: Any, spec: StageSpec, values: dict[str, str], worktree: Path,
                     attempt: int | None, *, first_failure: bool = False) -> list[str]:
        """Run the stage's gate commands; `first_failure` stops at the first that fails."""
        problems = []
        for gate in spec.gates:
            if any(not values.get(name) for name in placeholders(gate)):
                continue  # e.g. no approved seeds to check
            command = fill(gate, values)
            ok, out = self.commands(command, worktree,
                                    secrets=pick(self.secrets, spec.gate_secrets))
            self.ledger.add_gate(job["id"], attempt, command, ok, out)
            if not ok:
                problems.append(f"`{command}` failed:\n\n```\n{out[-2500:]}\n```")
                if first_failure:
                    break
        return problems

    def _send_back(self, run: Any, job: Any, problems: list[str]) -> Outcome:
        if job["send_backs"] >= self.config.max_send_backs:
            return self._exhausted(run, job, problems)
        rel = render.handoff_rel(run["id"], job["name"])
        self.ledger.set_job(job["id"], status=SENT_BACK, send_backs=job["send_backs"] + 1,
                            pending_prompt=pending(
                                "send_back", render.send_back_prompt(problems, rel)))
        return Outcome("ran", f"job {job['id']} sent back: {len(problems)} problems")

    def _exhausted(self, run: Any, job: Any, problems: list[str], *,
                   own_work: bool = True) -> Outcome:
        """Past its send-backs: a seed parks its parish; anything else blocks the Run.

        `own_work` is false when a reviewer's verdict exhausts a job that finished earlier,
        whose work is already committed (the tree holds the reviewer's approvals instead).
        """
        question = (f"Job {job['name']} ({job['stage']}) still has problems after "
                    f"{job['send_backs']} send-backs:\n\n" + "\n".join(f"- {p}" for p in problems))
        parish = json.loads(job["input"]).get("parish")
        if job["stage"] == "seed" and parish:
            if own_work:
                self._commit_parked(run, job, parish)
            flag = self.ledger.add_flag(run["id"], job["id"], severity=BLOCKING, scope="parish",
                                        subject=parish, question=question,
                                        suggestion="Answer how the drafter should fix it.")
            self.answers.open_issue(run, job, flag)
            self.ledger.set_job(job["id"], status=JOB_BLOCKED, finished_at=now())
            return Outcome("blocked", f"parked {parish}")
        return self._block_run(run, job, question)

    def _commit_parked(self, run: Any, job: Any, parish: str) -> None:
        """Commit a parked seed's draft as it stands, so the next job's diff is only its own
        and the job resumed with the owner's answer finds the draft on disk."""
        worktree = Path(run["worktree"])
        self._revert_outside(worktree, load_stage(job["stage"], worktree), self.values(run, job))
        git.commit(worktree, f"{run['diocese']}: seed {parish}, parked ({run['id']})",
                   _trailers(run, job))
        self._push(run, worktree)

    def _block_run(self, run: Any, job: Any | None, question: str, suggestion: str = "") -> Outcome:
        flag = self.ledger.add_flag(run["id"], job["id"] if job else None, severity=BLOCKING,
                                    scope="run", subject=run["id"], question=question,
                                    suggestion=suggestion)
        self.answers.open_issue(run, job, flag)
        if job is not None:
            self.ledger.set_job(job["id"], status=JOB_BLOCKED)
        self.ledger.set_run(run["id"], status=BLOCKED, blocked_reason=question[:500])
        return Outcome("blocked", question[:200])

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
        if isinstance(handoff, Integrate):
            # Before the commit, so HEAD is still the playbook the job started from.
            self._once(job, "playbook", lambda: dict(zip(
                ("before", "after"), map(playbook.sizes, self._playbooks(run, worktree)),
                strict=True)))
        self._once(job, "verdicts", lambda: self._verdicts(run, job, worktree, handoff))
        if job["stage"] == "seed-review":
            values = self.values(run, job)
            if self.ledger.get(f"approved:{job['id']}"):
                problems = self._stage_gates(job, spec, values, worktree, None)
                if problems:
                    # Commit the approvals and precedents already written, so they aren't
                    # taken for the reviewer's out-of-scope edits when it resumes. Once
                    # fixed, the check passes on the next try.
                    self._once(job, "approvals", lambda: git.commit(
                        worktree, f"{self._subject(run, job)}: approvals, check failing",
                        _trailers(run, job)))
                    self._push(run, worktree)
                    return self._block_run(run, job, "Approved seeds fail their check:\n"
                                           + "\n".join(problems), suggestion="Fix the seeds "
                                           "on the Run branch, or answer how the reviewer "
                                           "should fix them, then close this issue.")
        self._once(job, "lessons", lambda: self._lessons(run, job, worktree, handoff))
        self._once(job, "leads", lambda: [self.ledger.run_sql(
            "INSERT INTO lead (run_id, job_id, touches, note) VALUES (?,?,?,?)",
            run["id"], job["id"], lead.touches, lead.note) for lead in handoff.leads] and None)
        self._once(job, "settled", lambda: self._settle(job, handoff))
        self._once(job, "flags", lambda: self._flags(run, job, handoff))
        self._once(job, "commit", lambda: git.commit(
            worktree, self._subject(run, job), _trailers(run, job)))
        self._once(job, "push", lambda: self._push(run, worktree))
        run_flag = self.ledger.one("SELECT id FROM flag WHERE job_id = ? AND scope = 'run' AND "
                                   "status = ?", job["id"], OPEN) is not None
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

    def _settle(self, job: Any, handoff: Handoff) -> None:
        """Mark the earlier advisory flags reconcile settled, so the PR stops listing them
        as open and shows how each was settled instead."""
        for s in handoff.settled if isinstance(handoff, Reconcile) else []:
            self.ledger.run_sql("UPDATE flag SET status = ?, answer = ?, answered_at = ?, "
                                "settled_by = ? WHERE id = ? AND status = ?", SETTLED, s.how,
                                now(), job["id"], s.flag, LISTED)

    def _flags(self, run: Any, job: Any, handoff: Handoff) -> None:
        """Record the handoff's flags. One this job raised and the owner already settled is
        a new question when raised again; only a flag still open (a restart partway through
        this step) or listed is skipped."""
        existing = {(f["subject"], f["question"]) for f in self.ledger.all(
            "SELECT * FROM flag WHERE job_id = ? AND status != ?", job["id"], SETTLED)}
        for f in handoff.flags:
            if (f.subject, f.question) in existing:
                continue
            self.ledger.add_flag(run["id"], job["id"], severity=f.severity, scope=f.scope,
                                 subject=f.subject, question=f.question, evidence=f.evidence,
                                 suggestion=f.suggestion)
        for row in self.ledger.all("SELECT * FROM flag WHERE job_id = ? AND severity = ? "
                                   "AND issue_number IS NULL", job["id"], BLOCKING):
            self.answers.open_issue(run, job, row["id"])

    # ── Reviewer verdicts ────────────────────────────────────────────────────
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
            self._exhausted(run, reviewed, problems, own_work=False)
            return
        rel = render.handoff_rel(run["id"], reviewed["name"])
        self.ledger.clear_actions(reviewed["id"])
        self.ledger.set_job(reviewed["id"], status=SENT_BACK, send_backs=reviewed["send_backs"] + 1,
                            pending_prompt=pending(
                                "send_back", render.reviewer_send_back_prompt(problems, rel)))

    def _seed_job(self, run: Any, parish: str) -> Any | None:
        jobs = [j for j in self.ledger.jobs(run["id"], "seed")
                if json.loads(j["input"]).get("parish") == parish]
        return jobs[-1] if jobs else None

    def _seed_verdicts(self, run: Any, job: Any, worktree: Path, review: SeedReview) -> Any:
        """Approve or send back each seed. Safe to repeat (a resumed or retried review, a
        restart partway): a parish this job already gave a verdict keeps it."""
        approved: list[str] = []
        reviewer = f"agent:seed-review@{(job['commit_sha'] or 'unknown')[:12]}"
        scratch = handoff_path(worktree, run["id"], job["name"]).parent
        given = {r["subject"]: r["verdict"] for r in self.ledger.all(
            "SELECT subject, verdict FROM verdict WHERE job_id = ?", job["id"])}
        for verdict in review.seeds:
            if verdict.parish in given:
                if given[verdict.parish] == APPROVE:
                    approved.append(verdict.parish)
                continue
            drafted = self._seed_job(run, verdict.parish)
            problems = list(verdict.problems)
            if verdict.verdict == APPROVE:
                seed = read_seed(worktree, verdict.parish)
                ok, out = True, ""
                if (seed or {}).get("status") != "approved":  # approved before a restart
                    answers = [a.model_dump(exclude_none=True) for a in verdict.answers]
                    path = scratch / f"answers-{verdict.parish}.json"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(answers, indent=1), encoding="utf-8")
                    # It checks the seed as the stage's gates do, with their secrets.
                    ok, out = self.commands(
                        f"pnpm seed approve {verdict.parish} --reviewer {reviewer} --answers "
                        f"{path.relative_to(worktree).as_posix()}", worktree,
                        secrets=pick(self.secrets,
                                     load_stage(job["stage"], worktree).gate_secrets))
                if ok:
                    approved.append(verdict.parish)
                    self._decisions(run, job, worktree, verdict, seed)
                    self._verdict_row(job, drafted["id"] if drafted else None, verdict.parish,
                                      APPROVE, [])
                    continue
                problems = [f"`pnpm seed approve` refused the reviewer's answers: {out[-1500:]}"]
            if drafted is not None:
                self._send_back_to(run, drafted, problems)
            self._verdict_row(job, drafted["id"] if drafted else None, verdict.parish,
                              SEND_BACK, problems)
        self.ledger.set(f"approved:{job['id']}", approved)
        return approved

    def _decisions(self, run: Any, job: Any, worktree: Path, verdict: Any,
                   seed: dict[str, Any] | None) -> None:
        slots = {s.get("id"): s for s in (seed or {}).get("slots", [])}
        self.ledger.run_sql("DELETE FROM decision WHERE job_id = ? AND parish = ?", job["id"],
                            verdict.parish)  # a restart before its verdict row
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
        problems = self._stage_gates(job, spec, self.values(run, job), worktree, None,
                                     first_failure=True)
        if problems:
            return self._block_run(run, job, f"{job['stage']}: {problems[0]}")
        self._once(job, "commit", lambda: git.commit(
            worktree, self._subject(run, job), _trailers(run, job)))
        self._once(job, "push", lambda: self._push(run, worktree))
        self.ledger.set_job(job["id"], status=DONE, finished_at=now())
        return Outcome("ran", f"job {job['id']} {job['stage']} done")

    def _pr(self, run: Any, job: Any, worktree: Path) -> Outcome:
        self._once(job, "text", lambda: report.pr_text(self.ledger, run, worktree, self.commands))
        title, body = self.ledger.action_result(job["id"], "text")
        if run["kind"] == SEED:
            self._once(job, "drop drafts", lambda: self._drop_unapproved(run, job, worktree))
        self._once(job, "push", lambda: self._push(run, worktree))
        url = self.forge.open_pr(worktree, run["branch"], self.config.base_branch, title, body)
        self.ledger.set_run(run["id"], status=IN_REVIEW, pr_url=url, head_sha=git.head(worktree))
        self.ledger.set_job(job["id"], status=DONE, finished_at=now())
        return Outcome("ran", f"opened {url}")

    def _drop_unapproved(self, run: Any, job: Any, worktree: Path) -> list[str]:
        """Only approved seeds go to main: a parked parish's draft is left out of the PR.

        Its answer goes to a follow-up Run, whose drafter starts again with the answer.
        """
        dropped = []
        for parish in json.loads(run["parishes"] or "[]"):
            if seed_status(worktree, parish) not in (None, "approved"):
                git.revert(worktree, [f"data/seeds/{parish}.json"], source=self.config.upstream)
                dropped.append(parish)
        if dropped:
            git.commit(worktree, f"{run['diocese']}: leave out seeds not approved ({run['id']})",
                       _trailers(run, job))
        return dropped


def _trailers(run: Any, job: Any) -> dict[str, str]:
    return {"Factory-Job": f"{run['id']}/{job['name']}", "Factory-Stage": job["stage"]}


def _clip(text: str, n: int = 160) -> str:
    return text if len(text) <= n else text[:n].rstrip() + "…"
