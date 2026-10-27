"""The prompt each job starts from, built in code: a common header, then the stage's input.

The stage spec's prompt file (an agent definition or `factory/prompts/<stage>.md`) is the
system prompt; this is the first user message. Resumed attempts get a short message
instead: the problems a send-back found, your answer to an issue, or "continue".
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pdf_extract.factory import playbook
from pdf_extract.factory.handoff import schema_text
from pdf_extract.factory.ledger import LISTED, Ledger
from pdf_extract.factory.plan import describe_entry, diocese_dir, ordered_batches
from pdf_extract.factory.stages import StageSpec, fill


def handoff_rel(run_id: str, job_name: str) -> str:
    return f"scratch/{run_id}/{job_name}/handoff.json"


def header(run: Any, job: Any, spec: StageSpec, values: dict[str, str]) -> str:
    writes = ", ".join(f"`{fill(w, values)}`" for w in spec.writes) or "nothing"
    gates = "; ".join(f"`{fill(g, values)}`" for g in spec.gates) or "none"
    return f"""\
# Factory job {run['id']}/{job['name']}: {job['stage']}

You are a worker in the onboarding factory (docs/factory-spec.md): one fresh session that
runs one job and ends. Code scheduled you, and no person is watching.

- Diocese: `{run['diocese']}`. This directory is the Run's worktree, on branch `{run['branch']}`.
- Your scratch folder is `scratch/{run['id']}/{job['name']}/`; the Run's shared tools folder
  is `scratch/{run['id']}/tools/` (read its README.md before writing a script).
- You may change only {writes}. Any other change is reverted and the job sent back.
- You can't commit, push, use `gh` or start agents. When you finish, the dispatcher runs
  its gates ({gates}), then commits your work.
- Nobody answers questions during the job. A decision you can't make becomes a flag in
  your handoff, which is all the dispatcher reads.

## Handoff

Before you end, write `{handoff_rel(run['id'], job['name'])}`, about 300 tokens:

```json
{schema_text(job['stage'])}
```

- `status`: `done` when the job is finished; `partial` if you ran out of room and should be
  continued; `blocked` when nothing more can be done without a decision.
- `flags`: `blocking` sets a parish aside (`scope: parish`, subject `roster:id` or the
  parish slug) until the owner answers an issue, while the rest of the Run carries on; a
  blocking flag with `scope: run` stops the Run. `advisory` is listed in the PR: leave
  that parish open or excluded with a reason. Give evidence and what you would do.
- `leads`: something outside your input that later work should know, naming the batch id
  or `roster:id` it touches.
- `lessons`: only what is reusable beyond one parish, one line each.
"""


def _lines(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items) or "- (none)"


def stage_input(ledger: Ledger, run: Any, job: Any, values: dict[str, str]) -> str:
    worktree, diocese, run_id = Path(run["worktree"]), run["diocese"], run["id"]
    inputs = json.loads(job["input"])
    stage = job["stage"]
    tools = f"scratch/{run_id}/tools/"
    if stage == "survey":
        return f"""\
## Your job: survey `{diocese}`

{run['notes'] or 'No notes from the queue.'}

The Run's scratch folder is `scratch/{run_id}/`: write your manifest
`scratch/{run_id}/survey.json` there, and use `{tools}` as the tools folder.
"""
    if stage == "survey-review":
        earlier = [json.loads(r["problems"]) for r in ledger.all(
            "SELECT v.problems FROM verdict v JOIN job j ON j.id = v.job_id WHERE j.run_id = ? "
            "AND j.stage = 'survey-review' AND v.verdict = 'send_back' ORDER BY v.id", run_id)]
        sent = (f"\nAn earlier review sent the survey back for these; check they are fixed:\n"
                f"{_lines(earlier[-1])}\n" if earlier else "")
        return f"""\
## Your job: review the survey of `{diocese}`

The survey was job {inputs.get('survey_job')}. Read `data/dioceses/{diocese}/diocese.md`,
`data/dioceses/{diocese}/batches.json` and `scratch/{run_id}/survey.json`.
`pnpm --silent diocese batches validate {diocese}` passed.
{sent}"""
    if stage == "map":
        return _map_input(ledger, run, job, inputs)
    if stage == "integrate":
        meta = diocese_dir(worktree, diocese) / "diocese.md"
        n = len(playbook.bullets(meta, playbook.NEW_LESSONS))
        return f"""\
## Your job: integrate {n} new lessons

`data/dioceses/{diocese}/diocese.md` has {n} entries under *New lessons*.
"""
    if stage == "reconcile":
        advisory = [f"{f['subject']}: {f['question']} (suggestion: {f['suggestion'] or '-'})"
                    for f in ledger.flags(run_id, LISTED)]
        leads = [f"{r['touches']}: {r['note']}" for r in ledger.all(
            "SELECT * FROM lead WHERE run_id = ? AND used_by IS NULL", run_id)]
        parked = [f"{f['subject']}: {f['question']}" for f in ledger.parked(run_id)]
        return f"""\
## Your job: reconcile `{diocese}`

Every batch is mapped. Use `{tools}` as the tools folder.

Advisory flags from the batches:
{_lines(advisory)}

Leads no batch took:
{_lines(leads)}

Parked parishes (an issue waits for the owner; leave their records alone):
{_lines(parked)}
"""
    if stage == "seed":
        return f"""\
## Your job: seed `{inputs['parish']}`

Draft `data/seeds/{inputs['parish']}.json`, with `scratch/{run_id}/{job['name']}/` as
your scratch folder.
"""
    if stage == "seed-review":
        return _seed_review_input(ledger, run, inputs, values)
    return ""


def _answer(inputs: dict[str, Any]) -> str:
    if not inputs.get("answer"):
        return ""
    return f"""
## The owner's answer

You asked: {inputs.get('question', '')}
They answered: {inputs['answer']}
"""


def _map_input(ledger: Ledger, run: Any, job: Any, inputs: dict[str, Any]) -> str:
    worktree, diocese, run_id = Path(run["worktree"]), run["diocese"], run["id"]
    batch = next((b for b in ordered_batches(worktree, diocese)
                  if b["id"] == inputs.get("batch")), {})
    entries = inputs.get("entries") or batch.get("entries") or []
    touches = {inputs.get("batch"), *entries}
    leads = ledger.all("SELECT * FROM lead WHERE run_id = ? AND (used_by IS NULL OR "
                       "used_by = ?)", run_id, job["id"])  # the same leads for a fresh worker
    mine = [r for r in leads if r["touches"] in touches]
    for r in mine:
        ledger.run_sql("UPDATE lead SET used_by = ? WHERE id = ?", job["id"], r["id"])
    scope = ("only these entries, set aside earlier for a question" if inputs.get("answer")
             else f"batch `{batch.get('id', inputs.get('batch'))}`: {batch.get('name', '')}")
    return f"""\
## Your job: map {scope}

{batch.get('why', '')}

Roster entries:
{_lines([describe_entry(worktree, diocese, e) for e in entries])}

Use `scratch/{run_id}/{job['name']}/` as your scratch folder and `scratch/{run_id}/tools/`
as the tools folder.

Leads from earlier jobs:
{_lines([f"{r['touches']}: {r['note']}" for r in mine])}
"""


def _seed_review_input(ledger: Ledger, run: Any, inputs: dict[str, Any],
                       values: dict[str, str]) -> str:
    worktree, diocese, run_id = Path(run["worktree"]), run["diocese"], run["id"]
    meta = diocese_dir(worktree, diocese) / "diocese.md"
    precedents = playbook.section(meta, playbook.PRECEDENTS) if meta.exists() else ""
    redrafted = []
    for parish in inputs.get("redrafted") or []:
        row = ledger.one("SELECT v.problems FROM verdict v JOIN job j ON j.id = v.job_id "
                         "WHERE j.run_id = ? AND v.subject = ? ORDER BY v.id DESC LIMIT 1",
                         run_id, parish)
        problems = "; ".join(json.loads(row["problems"])) if row else ""
        redrafted.append(f"{parish}, sent back for: {problems}")
    return f"""\
## Your job: review the seeds of batch `{inputs.get('batch')}`

Parishes (`pnpm seed status` shows each one's status and open questions):
{_lines(list(inputs.get('parishes') or []))}

Give every parish above a verdict in `seeds`. Decide every open question yourself, even a
hard one: the owner reads each decision and its `why` in the PR and changes what's wrong.

Redrafted after a send-back:
{_lines(redrafted)}

This diocese's seeding precedents (`diocese.md`, *Seeding precedents*):
{precedents or '(none yet)'}
"""


def job_input(ledger: Ledger, run: Any, job: Any, spec: StageSpec,
              values: dict[str, str]) -> str:
    return (header(run, job, spec, values) + "\n" + stage_input(ledger, run, job, values)
            + _answer(json.loads(job["input"])))


def send_back_prompt(problems: list[str], handoff: str) -> str:
    return ("The dispatcher sent your work back. Fix these problems, then write your handoff "
            f"again at `{handoff}`:\n\n" + _lines(problems))


def continue_prompt(handoff: str) -> str:
    return (f"Continue the job where you left off. Finish it, then write your handoff at "
            f"`{handoff}` with status `done` (or `blocked` with a flag).")


def resume_prompt(handoff: str) -> str:
    return (f"Your session was interrupted. Check what is already on disk, continue the job "
            f"where you left off, and write your handoff at `{handoff}`.")


def answer_prompt(question: str, answer: str, handoff: str, scope: str) -> str:
    return (f"The owner answered the question you raised about {scope}.\n\nYou asked: "
            f"{question}\nThey answered: {answer}\n\nFinish that work now, following the "
            f"answer, and write a new handoff at `{handoff}`.")
