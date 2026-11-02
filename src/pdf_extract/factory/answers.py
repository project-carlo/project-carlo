"""Blocking flags become GitHub issues; the owner's answers come back as work.

An answer to a Run-level flag, or to a flag of a job that isn't parked, resumes the job
with the answer. An answer to a parked parish requeues it as a new job, in a follow-up
Run if its own Run is already in review or merged.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from pdf_extract.factory import forge as forge_mod
from pdf_extract.factory import render
from pdf_extract.factory.config import Config, FactoryError
from pdf_extract.factory.forge import Forge
from pdf_extract.factory.handoff import BLOCKING, PARKING_STAGES
from pdf_extract.factory.ledger import (
    ANSWERED,
    IN_REVIEW,
    JOB_BLOCKED,
    MERGED,
    OPEN,
    PENDING,
    SENT_BACK,
    SETTLED,
    Ledger,
    now,
    pending,
)

LOGGER = logging.getLogger(__name__)


class Answers:
    def __init__(self, ledger: Ledger, config: Config, forge: Forge) -> None:
        self.ledger, self.config, self.forge = ledger, config, forge

    def open_issue(self, run: Any, job: Any | None, flag_id: int) -> None:
        """The flag's issue. If GitHub refuses, the flag stays open without one and
        `poll_issues` opens it on a later poll."""
        flag = self.ledger.one("SELECT * FROM flag WHERE id = ?", flag_id)
        if flag["issue_number"]:
            return
        stage = job["stage"] if job else "dispatcher"
        title = f"[factory] {run['id']}: {flag['subject']}: {flag['question'].splitlines()[0]}"
        try:
            number = self.forge.open_issue(
                title[:120], forge_mod.issue_body(flag, run, job),
                ["factory", f"run:{run['diocese']}", f"stage:{stage}"])
        except FactoryError as exc:
            LOGGER.warning("couldn't open the issue for flag %s: %s", flag_id, exc)
            return
        self.ledger.run_sql("UPDATE flag SET issue_number = ? WHERE id = ?", number, flag_id)

    def poll_issues(self) -> None:
        for flag in self.ledger.all("SELECT * FROM flag WHERE status = ? AND severity = ? AND "
                                    "issue_number IS NULL ORDER BY id", OPEN, BLOCKING):
            self.open_issue(self.ledger.run(flag["run_id"]),
                            self.ledger.job(flag["job_id"]) if flag["job_id"] else None,
                            flag["id"])
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
        if flag["scope"] == "run" or job is None or job["stage"] not in PARKING_STAGES:
            # Only map and seed jobs park a parish to be requeued on its own (the handoff
            # check refuses parish flags from other stages).
            if job is not None and job["status"] in (JOB_BLOCKED, SENT_BACK):
                self._resume_blocked(run, job, flag)
            self.ledger.run_sql("UPDATE flag SET status = ? WHERE id = ?", SETTLED, flag["id"])
            return
        data = json.loads(job["input"])
        subject = flag["subject"]
        requeued: dict[str, Any] = {"answer": flag["answer"], "question": flag["question"],
                                    "subject": subject, "flag": flag["id"]}
        if job["stage"] == "map":
            requeued |= {"batch": data.get("batch"), "entries": [subject]}
        else:
            requeued |= {"parish": subject, "batch": data.get("batch")}
        target = run
        if run["status"] in (IN_REVIEW, MERGED):
            target = self._follow_up(run, subject)
        self.ledger.add_job(target["id"], job["stage"], requeued, resumes_job=job["id"])
        self.ledger.run_sql("UPDATE flag SET status = ? WHERE id = ?", SETTLED, flag["id"])

    def _resume_blocked(self, run: Any, job: Any, flag: Any) -> None:
        rel = render.handoff_rel(run["id"], job["name"])
        prompt = render.answer_prompt(flag["question"], flag["answer"], rel, "this job")
        before = json.loads(job["pending_prompt"] or "null")
        if job["status"] == SENT_BACK and before:
            # Another of its flags was answered first: the job gets both answers.
            prompt = f"{before.get('prompt') or ''}\n\n{prompt}".strip()
        self.ledger.clear_actions(job["id"])
        self.ledger.set_job(job["id"], status=SENT_BACK, send_backs=0, continues=0, crashes=0,
                            pending_prompt=pending("answer", prompt))

    def _follow_up(self, run: Any, subject: str) -> Any:
        """The pending follow-up Run of the same kind that takes this parish."""
        for other in self.ledger.runs(PENDING):
            if other["follow_up_of"] == run["id"]:
                parishes = json.loads(other["parishes"] or "[]")
                if subject not in parishes:
                    self.ledger.set_run(other["id"], parishes=json.dumps(parishes + [subject]))
                return self.ledger.run(other["id"])
        run_id = self.ledger.add_run(diocese=run["diocese"], kind=run["kind"],
                                     worktrees_dir=self.config.worktrees_dir,
                                     branch_prefix=self.config.branch_prefix, status=PENDING,
                                     follow_up_of=run["id"], parishes=[subject],
                                     notes=f"Follow-up of {run['id']}")
        return self.ledger.run(run_id)
