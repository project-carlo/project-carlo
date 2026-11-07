"""What the dispatcher does between jobs: quota readings, issues and answers, merged Runs,
seed readiness, the nightly backup.

Each step on its own: one failing (GitHub down, R2 keys wrong) is logged and tried again
on its next turn, without stopping the others or the jobs.
"""

from __future__ import annotations

import logging
import shutil
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.factory import forge as forge_mod
from pdf_extract.factory import git, readiness, workspace
from pdf_extract.factory.answers import Answers
from pdf_extract.factory.config import Config, FactoryError
from pdf_extract.factory.forge import Forge
from pdf_extract.factory.ledger import IN_REVIEW, MERGED, PENDING, SEED, Ledger, now
from pdf_extract.factory.metrics.readings import Readings

LOGGER = logging.getLogger(__name__)


class Housekeeping:
    def __init__(self, ledger: Ledger, config: Config, *, repo: Path, forge: Forge,
                 readings: Readings, answers: Answers, clock: Callable[[], datetime],
                 db_path: Path, runs_dir: Path, pull_data: Callable[[], None] | None,
                 backup: Callable[[], str] | None, sandbox_dir: Path | None = None) -> None:
        self.ledger, self.config, self.repo, self.forge = ledger, config, repo, forge
        self.readings, self.answers, self.clock = readings, answers, clock
        self.db_path, self.runs_dir = db_path, runs_dir
        self.pull_data, self.backup = pull_data, backup
        self.sandbox_dir = sandbox_dir  # sandboxed workers' workspaces, one per Run

    def run(self) -> None:
        at = self.clock()
        self._safely("quota", self.readings.sample)  # skips accounts cooling down
        if self.ledger.due("issues_polled", timedelta(minutes=self.config.issue_poll_minutes),
                           at):
            self._safely("issues", lambda: (git.fetch(self.repo, self.config.remote),
                                            self.answers.poll_issues(), self.check_merged()))
        if self.ledger.due("readiness_checked",
                           timedelta(hours=self.config.readiness_check_hours), at):
            self._safely("readiness", self.check_readiness)
        local = at.astimezone()
        if local.hour >= self.config.backup_hour and self.backup is not None \
                and self.ledger.get("backed_up") != local.date().isoformat():
            # Marked first, so a failing backup is tried again tomorrow, not every tick.
            self.ledger.set("backed_up", local.date().isoformat())
            backup = self.backup
            self._safely("backup", lambda: self.ledger.set("backup", backup()))

    def _safely(self, name: str, fn: Callable[[], Any]) -> None:
        try:
            fn()
        except Exception:  # housekeeping never stops the dispatcher
            LOGGER.exception("housekeeping %s failed", name)

    def check_merged(self) -> None:
        """Its last commit in main, or (squashed or rebased, so it isn't) its PR merged."""
        for run in self.ledger.runs(IN_REVIEW):
            merged = run["head_sha"] and git.is_merged(self.repo, run["head_sha"],
                                                       self.config.upstream)
            if not merged and run["pr_url"]:
                merged = self.forge.pr_merged(run["pr_url"])
            if merged:
                self.ledger.set_run(run["id"], status=MERGED, merged_at=now())
                self.retire(self.ledger.run(run["id"]))

    def retire(self, run: Any) -> None:
        """A merged Run's worktree is no longer needed: answers after the merge go to a
        follow-up Run with its own worktree, and readiness reads main. Its scratch (handoffs,
        manifests, tools) is kept in data/factory/runs/<run>/scratch/ for foreman reviews."""
        path = Path(run["worktree"])
        scratch = path / "scratch" / run["id"]
        if scratch.is_dir():
            shutil.copytree(scratch, self.runs_dir / run["id"] / "scratch", dirs_exist_ok=True)
        try:
            git.remove_worktree(self.repo, path, run["branch"])
        except FactoryError as exc:
            LOGGER.warning("couldn't remove %s: %s", path, exc)
        if self.sandbox_dir is not None:
            workspace.remove(self.sandbox_dir, run["id"])

    def check_readiness(self) -> None:
        dioceses = readiness.dioceses_to_check(self.ledger)
        if not dioceses:
            return
        if self.pull_data is not None:
            self.pull_data()
        for diocese in dioceses:
            result = readiness.assess(self.ledger, self.config, diocese, self.db_path,
                                      self.clock(), repo=self.repo)
            if result is None:
                continue
            if result.start:
                self.ledger.add_run(diocese=diocese, kind=SEED, status=PENDING,
                                    worktrees_dir=self.config.worktrees_dir,
                                    branch_prefix=self.config.branch_prefix,
                                    parishes=result.start,
                                    notes=f"{len(result.start)} parishes ready"
                                    + (f"; {len(result.fetch_gaps)} wait on a collector "
                                       f"(`pnpm diocese gaps --diocese {diocese}`)"
                                       if result.fetch_gaps else ""))
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
