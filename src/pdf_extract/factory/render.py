"""Every piece of worker-facing text the factory builds in code.

The stage spec's prompt file (an agent definition or `factory/prompts/<stage>.md`) is the
system prompt; a job's first message is a common header, then the stage's input. Resumed
attempts get a short message instead: the problems a send-back found, your answer to an
issue, or "continue".

Rendering is pure: it reads the ledger and the Run's files and writes nothing, so
`pnpm factory prompt` can preview a job that hasn't run. The leads a map input shows are
claimed by the dispatcher when the attempt starts (`leads_shown`).
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract.factory import playbook
from pdf_extract.factory.config import FactoryError
from pdf_extract.factory.handoff import PARKING_STAGES
from pdf_extract.factory.ledger import LISTED, Ledger
from pdf_extract.factory.plan import describe_entry, diocese_dir, ordered_batches
from pdf_extract.factory.stages import StageSpec, fill
from pdf_extract.factory.workers import strip_frontmatter

SKILLS_DIR = Path(".claude") / "skills"


def handoff_rel(run_id: str, job_name: str) -> str:
    return f"scratch/{run_id}/{job_name}/handoff.json"


def job_values(ledger: Ledger, run: Any, job: Any) -> dict[str, str]:
    """The placeholders a stage spec's `writes` and `gates` may use."""
    data = json.loads(job["input"])
    approved = ledger.get(f"approved:{job['id']}", [])
    return {
        "diocese": run["diocese"], "run": run["id"], "job": job["name"],
        "branch": run["branch"], "parish": data.get("parish", ""),
        "parishes": " ".join(data.get("parishes") or []), "approved": " ".join(approved),
    }


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
{_flags_help(job['stage'])}
- `leads`: something outside your input that later work should know, naming the batch id
  or `roster:id` it touches.
- `lessons`: only what is reusable beyond one parish, one line each.
"""


def _flags_help(stage: str) -> str:
    if stage in PARKING_STAGES:
        return """\
- `flags`: `blocking` sets a parish aside (`scope: parish`, subject `roster:id` or the
  parish slug) until the owner answers an issue, while the rest of the Run carries on; a
  blocking flag with `scope: run` stops the Run. `advisory` is listed in the PR: leave
  that parish open or excluded with a reason. Give evidence and what you would do. Don't
  flag what the records already carry (README, *What to flag*): a church left in `open/`,
  a bulletin `fetch` can't collect (`fetch_gap`), a check blocked for now (`research`
  with a retry trigger), or an address you chose between sources."""
    return """\
- `flags`: a `blocking` flag (`scope: run`) stops the Run until the owner answers an
  issue; this stage can't set a single parish aside. `advisory` is listed in the PR.
  Give evidence and what you would do. Don't flag what the records already carry
  (README, *What to flag*): a church left in `open/`, a bulletin `fetch` can't collect
  (`fetch_gap`), a check blocked for now (`research` with a retry trigger), or an address
  you chose between sources."""


def schema_text(stage: str) -> str:
    """The handoff format, as the job input shows it to a worker."""
    base = {
        "status": "done | partial | blocked",
        "summary": "one or two sentences",
        "flags": [{
            "severity": "blocking | advisory", "scope": "parish | run",
            "subject": "roster:id or parish slug", "question": "what needs deciding",
            "evidence": ["path#section or URL with date"],
            "suggestion": "what you would do",
        }],
        "leads": [{"touches": "batch id or roster:id", "note": "..."}],
        "lessons": ["reusable publisher or rule lesson"],
    }
    if stage == "survey-review":
        base |= {"verdict": "approve | send_back", "problems": ["..."],
                 "rules": ["each proposed rule you accept, as written"]}
    if stage == "reconcile":
        base |= {"settled": [{"flag": "the id from your input, e.g. 12",
                              "how": "what you did, or what settled it, in one line"}]}
    if stage == "seed-review":
        base |= {"seeds": [{
            "parish": "slug", "verdict": "approve | send_back",
            "answers": [{"slot": "slot id", "question": "...",
                         "choice": "option index | dropped | edited",
                         "entry": "only for edited", "basis": "rule | precedent | judgment",
                         "why": "..."}],
            "problems": ["..."],
        }]}
    return json.dumps(base, indent=1)


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
        raised_by = {j["id"]: j["name"] for j in ledger.jobs(run_id)}
        # Not its own: a fresh input after a resume or retry can't settle what it raised.
        advisory = [f"[#{f['id']}] {f['subject']} ({raised_by.get(f['job_id'], '?')}): "
                    f"{f['question']} (suggestion: {f['suggestion'] or '-'})"
                    for f in ledger.flags(run_id, LISTED) if f["job_id"] != job["id"]]
        leads = [f"{r['touches']}: {r['note']}" for r in ledger.all(
            "SELECT * FROM lead WHERE run_id = ? AND used_by IS NULL", run_id)]
        parked = [f"{f['subject']}: {f['question']}" for f in ledger.parked(run_id)]
        return f"""\
## Your job: reconcile `{diocese}`

Every batch is mapped. Use `{tools}` as the tools folder.

Advisory flags from earlier jobs, mostly the batches. Put each one you settle in your
handoff's `settled`, by its `[#id]`; the PR lists the rest as still open:
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


def leads_shown(ledger: Ledger, run: Any, job: Any) -> list[Any]:
    """The leads a map job's input shows: those about its batch or entries that no other
    job has claimed. A fresh attempt gets the leads its first attempt claimed again, plus
    any added since. Other stages show none."""
    if job["stage"] != "map":
        return []
    inputs = json.loads(job["input"])
    entries = inputs.get("entries") or next(
        (b.get("entries") or [] for b in ordered_batches(Path(run["worktree"]), run["diocese"])
         if b["id"] == inputs.get("batch")), [])
    touches = {inputs.get("batch"), *entries}
    leads = ledger.all("SELECT * FROM lead WHERE run_id = ? AND (used_by IS NULL OR "
                       "used_by = ?) ORDER BY id", run["id"], job["id"])
    return [r for r in leads if r["touches"] in touches]


def _map_input(ledger: Ledger, run: Any, job: Any, inputs: dict[str, Any]) -> str:
    worktree, diocese, run_id = Path(run["worktree"]), run["diocese"], run["id"]
    batch = next((b for b in ordered_batches(worktree, diocese)
                  if b["id"] == inputs.get("batch")), {})
    entries = inputs.get("entries") or batch.get("entries") or []
    mine = leads_shown(ledger, run, job)
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


def reviewer_send_back_prompt(problems: list[str], handoff: str) -> str:
    return "A reviewer sent your work back.\n\n" + send_back_prompt(problems, handoff)


def next_prompt(ledger: Ledger, run: Any, job: Any, spec: StageSpec,
                values: dict[str, str]) -> tuple[str, str, str | None]:
    """The next attempt's kind, its prompt and the session it resumes."""
    rel = handoff_rel(run["id"], job["name"])
    pending = json.loads(job["pending_prompt"] or "null")
    if pending is None:
        if job["resumes_job"]:
            original = ledger.job(job["resumes_job"])
            data = json.loads(job["input"])
            if original["session_id"] and original["run_id"] == run["id"]:
                return "answer", answer_prompt(
                    data.get("question", ""), data.get("answer", ""), rel,
                    data.get("subject", "the parish you set aside")), original["session_id"]
        return "start", job_input(ledger, run, job, spec, values), None
    if not job["session_id"]:
        # A fresh worker needs the whole job input, whatever the last attempt was told.
        prompt = job_input(ledger, run, job, spec, values)
        extra = pending.get("prompt")
        return "fresh", prompt + (f"\n\n{extra}" if extra else ""), None
    kind = pending["kind"]
    prompt = pending.get("prompt") or (continue_prompt(rel) if kind != "resume"
                                       else resume_prompt(rel))
    return kind, prompt, job["session_id"]


# ── What a worker is given, and its size ────────────────────────────────────
TextOf = Callable[[str], str | None]  # a repo-relative path's text, None if it's missing


def tokens(text: str) -> int:
    """A rough token count (about four characters a token), for comparing sizes."""
    return round(len(text) / 4)


def skill_path(name: str) -> str:
    return (SKILLS_DIR / name / "SKILL.md").as_posix()


def read_entry(text_of: TextOf, entry: str) -> str:
    """A `reads:` entry's text: a whole file (`path`), or one section (`path#Heading`), from
    its heading to the next heading of its level or above."""
    path, _, heading = entry.partition("#")
    text = text_of(path)
    if text is None:
        raise FactoryError(f"reads: no file {path}")
    if not heading:
        return text
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.fullmatch(r"#+\s+" + re.escape(heading.strip()) + r"\s*", line)), None)
    if start is None:
        raise FactoryError(f"reads: {path} has no heading {heading!r}")
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    end = next((i for i in range(start + 1, len(lines))
                if (m := re.match(r"(#+)\s", lines[i])) and len(m.group(1)) <= level),
               len(lines))
    return "\n".join(lines[start:end]).strip() + "\n"


def message_label(kind: str) -> str:
    """What an attempt's prompt is: a job's first message, or a resumed session's next."""
    return "first message" if kind in ("start", "fresh") else f"{kind} message"


def given(spec: StageSpec, message: str, text_of: TextOf,
          label: str = "first message") -> list[dict[str, Any]]:
    """Each part of what a worker is given, with its size: the appended system prompt, the
    attempt's message, each skill it may load and each file it must read."""
    def part(kind: str, source: str | None, text: str | None, **extra: Any) -> dict[str, Any]:
        return {"part": kind, "source": source, "missing": text is None,
                "chars": len(text or ""), "tokens": tokens(text or ""), **extra}

    prompt = text_of(spec.prompt) if spec.prompt else ""
    parts = [part("system prompt", spec.prompt,
                  strip_frontmatter(prompt) if prompt is not None else None),
             part(label, None, message)]
    for name in spec.skills:
        parts.append(part("skill", skill_path(name), text_of(skill_path(name)), name=name))
    for entry in spec.reads:
        try:
            parts.append(part("read", entry, read_entry(text_of, entry)))
        except FactoryError as exc:
            parts.append(part("read", entry, None, error=str(exc)))
    return parts


def _digest(*parts: bytes | str) -> str:
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode() if isinstance(p, str) else p)
        h.update(b"\0")
    return h.hexdigest()[:12]


def context_hashes(worktree: Path, spec: StageSpec) -> dict[str, Any]:
    """For the attempt's config fingerprint, what the spec and prompt file don't show: the
    code that builds the first message (this module), the skills' contents and the reads'."""
    def skill(name: str) -> str:
        folder = worktree / SKILLS_DIR / name
        files = sorted(p for p in folder.rglob("*") if p.is_file()
                       and "__pycache__" not in p.parts and p.suffix != ".pyc")
        return _digest(*[x for p in files for x in (p.relative_to(folder).as_posix(),
                                                    p.read_bytes())]) if files else "missing"

    def read(entry: str) -> str:
        try:
            return _digest(read_entry(lambda p: _text(worktree / p), entry))
        except FactoryError:
            return "missing"

    return {"render": _digest(Path(__file__).read_bytes()),
            "skills": {name: skill(name) for name in spec.skills},
            "reads": {entry: read(entry) for entry in spec.reads}}


def _text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def worktree_text(worktree: Path) -> TextOf:
    return lambda rel: _text(worktree / rel)
