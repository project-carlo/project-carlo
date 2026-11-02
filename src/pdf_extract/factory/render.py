"""Every piece of worker-facing text the factory builds in code.

The stage spec's prompt file (an agent definition or `factory/prompts/<stage>.md`) is the
system prompt; a job's first message is a common header, then the stage's input. Resumed
attempts get a short message instead: the problems a send-back found, your answer to an
issue, or "continue".

Rendering is pure: it reads the ledger and the Run's files and writes nothing, so
`pnpm factory prompt` can preview a job that hasn't run. The dispatcher does the writing
when the attempt starts: it claims the leads a map input shows (`leads_shown`), and puts
the sections the stage reads (`read_files`) and any bulky input (`input_files`) in the
job's scratch folder, where the first message points.
"""

from __future__ import annotations

import hashlib
import json
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


def scratch_rel(run_id: str, job_name: str) -> str:
    return f"scratch/{run_id}/{job_name}/"


def handoff_rel(run_id: str, job_name: str) -> str:
    return f"{scratch_rel(run_id, job_name)}handoff.json"


def reads_rel(run_id: str, job_name: str, path: str) -> str:
    """Where the dispatcher writes the sections a job reads of `path`."""
    return f"{scratch_rel(run_id, job_name)}reads/{path}"


def flags_rel(run_id: str, job_name: str) -> str:
    """Reconcile's list of the flags and leads it may settle."""
    return f"{scratch_rel(run_id, job_name)}flags.md"


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

You are a worker in the onboarding factory: one fresh session that runs one job and ends.
Code scheduled you, and no person is watching.

- Diocese: `{run['diocese']}`. This directory is the Run's worktree, on branch `{run['branch']}`.
- Your scratch folder is `{scratch_rel(run['id'], job['name'])}`; the Run's shared tools
  folder is `scratch/{run['id']}/tools/` (read its README.md before writing a script).
- You may change only {writes}. Any other change is reverted and the job sent back.
- You can't commit, push, use `gh` or start agents. When you finish, the dispatcher runs
  its gates ({gates}), then commits your work.
- Nobody answers questions during the job. A decision you can't make becomes a flag in
  your handoff, which is all the dispatcher reads.
- Keep your context small: everything you read is read again on every later step. Send
  long output to a file in your scratch folder and read only the part you need (`jq`,
  `grep`, `head`); grep a long document before reading it.
{_reads_list(run['id'], job['name'], spec)}
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


def _reads_list(run_id: str, job_name: str, spec: StageSpec) -> str:
    """What the stage's `reads:` asks for: a whole file by its own path, a file's sections
    by the copy the dispatcher writes in the job's scratch folder."""
    if not spec.reads:
        return ""
    items = []
    for path, headings in _reads_by_file(spec).items():
        if headings is None:
            items.append(f"- `{path}`")
        else:
            names = ", ".join(f"*{h}*" for h in headings)
            items.append(f"- `{reads_rel(run_id, job_name, path)}`: {names} from `{path}`")
    return ("\n## Read first\n\nRead these in full before you start; they are the rules "
            "this job is held to.\n\n" + "\n".join(items) + "\n")


def _flags_help(stage: str) -> str:
    if stage in PARKING_STAGES:
        return """\
- `flags`: a `blocking` flag with `scope: parish` (subject `roster:id` or the parish slug)
  sets that parish aside until the owner answers an issue, while the rest of the Run
  carries on; with `scope: run` it stops the Run. An `advisory` flag is listed in the PR.
  Give evidence and what you would do."""
    return """\
- `flags`: a `blocking` flag (`scope: run`) stops the Run until the owner answers an
  issue; this stage can't set a single parish aside. An `advisory` flag is listed in the
  PR. Give evidence and what you would do."""


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
    if stage == "integrate":
        base |= {"rules_changed": [{"was": ["each rule it replaces, word for word"],
                                    "now": "the rule that replaces them"}]}
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
    # One line a field: the shape is what matters, and it stays valid JSON.
    return "{\n" + ",\n".join(f" {json.dumps(k)}: {json.dumps(v)}"
                               for k, v in base.items()) + "\n}"


def _lines(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items) or "- (none)"


def stage_input(ledger: Ledger, run: Any, job: Any, values: dict[str, str]) -> str:
    worktree, diocese, run_id = Path(run["worktree"]), run["diocese"], run["id"]
    inputs = json.loads(job["input"])
    stage = job["stage"]
    if stage == "survey":
        return f"""\
## Your job: survey `{diocese}`

{run['notes'] or 'No notes from the queue.'}

Write your manifest to `scratch/{run_id}/survey.json`.
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
        return _integrate_input(worktree, diocese)
    if stage == "reconcile":
        advisory, leads = _reconcile_lists(ledger, run, job)
        parked = [f"{f['subject']}: {f['question']}" for f in ledger.parked(run_id)]
        return f"""\
## Your job: reconcile `{diocese}`

Every batch is mapped. `{flags_rel(run_id, job['name'])}` lists, one a line, the
{len(advisory)} advisory flags earlier jobs raised and the {len(leads)} leads no batch took.
Put each flag you settle in your handoff's `settled`, by its `[#id]`; the PR lists the
rest as still open.

Parked parishes (an issue waits for the owner; leave their records alone):
{_lines(parked)}
"""
    if stage == "seed":
        return f"""\
## Your job: seed `{inputs['parish']}`

Draft `data/seeds/{inputs['parish']}.json`.
"""
    if stage == "seed-review":
        return _seed_review_input(ledger, run, inputs, values)
    return ""


def _integrate_input(worktree: Path, diocese: str) -> str:
    meta = diocese_dir(worktree, diocese) / "diocese.md"
    text = meta.read_text(encoding="utf-8") if meta.exists() else ""
    n = playbook.sizes(text)["lessons"]
    rows = []
    for heading, target in playbook.TARGETS.items():
        now = playbook.size(text, heading)
        over = f", {playbook.kb(now - target)} over" if now > target else ""
        rows.append(f"*{heading.lstrip('# ')}*: {playbook.kb(now)} (target "
                    f"{playbook.kb(target)}{over})")
    rows.append(f"*New lessons*: {n} entries, "
                f"{playbook.kb(playbook.size(text, playbook.NEW_LESSONS))}, all to fold in or drop")
    return f"""\
## Your job: integrate {n} new lessons

The playbook in `data/dioceses/{diocese}/diocese.md` now, by section (bytes of the text
under each heading, as `wc -c` counts them), and the size to keep each near:

{_lines(rows)}
"""


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


def _reconcile_lists(ledger: Ledger, run: Any, job: Any) -> tuple[list[str], list[str]]:
    """The advisory flags reconcile may settle and the leads no batch took, one line each."""
    raised_by = {j["id"]: j["name"] for j in ledger.jobs(run["id"])}
    # Not its own: a fresh input after a resume or retry can't settle what it raised.
    advisory = [f"[#{f['id']}] {f['subject']} ({raised_by.get(f['job_id'], '?')}): "
                f"{_one_line(f['question'])} (suggestion: {_one_line(f['suggestion']) or '-'})"
                for f in ledger.flags(run["id"], LISTED) if f["job_id"] != job["id"]]
    leads = [f"{r['touches']}: {_one_line(r['note'])}" for r in ledger.all(
        "SELECT * FROM lead WHERE run_id = ? AND used_by IS NULL ORDER BY id", run["id"])]
    return advisory, leads


def _one_line(text: str | None) -> str:
    return " ".join((text or "").split())


def input_files(ledger: Ledger, run: Any, job: Any) -> dict[str, str]:
    """Bulky input the dispatcher writes to the job's scratch folder instead of the first
    message, by repo-relative path. Only reconcile has any."""
    if job["stage"] != "reconcile":
        return {}
    advisory, leads = _reconcile_lists(ledger, run, job)
    return {flags_rel(run["id"], job["name"]): f"""\
# Advisory flags and leads for {run['id']}/{job['name']}

## Advisory flags from earlier jobs, mostly the batches

{_lines(advisory)}

## Leads no batch took

{_lines(leads)}
"""}


PLAYBOOK = (playbook.PUBLISHERS, playbook.RULES, playbook.NEW_LESSONS)


def _playbook(worktree: Path, diocese: str) -> str:
    """The sections of `diocese.md` every map job follows, as they stand."""
    meta = diocese_dir(worktree, diocese) / "diocese.md"
    parts = []
    for heading in PLAYBOOK:
        body = playbook.section(meta, heading) if meta.exists() else ""
        if heading == playbook.NEW_LESSONS:
            # From the first bullet, so without the section's intro; a lesson that wraps,
            # or has sub-bullets, stays whole.
            lines = body.splitlines()
            first = next((i for i, line in enumerate(lines) if line.startswith("- ")),
                         len(lines))
            body = "\n".join(lines[first:])
        parts.append(f"### {heading.lstrip('# ')}\n\n{body or '(none yet)'}\n")
    return "\n".join(parts)


def _map_input(ledger: Ledger, run: Any, job: Any, inputs: dict[str, Any]) -> str:
    worktree, diocese = Path(run["worktree"]), run["diocese"]
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

Leads from earlier jobs:
{_lines([f"{r['touches']}: {r['note']}" for r in mine])}

## The playbook

From `data/dioceses/{diocese}/diocese.md`, as earlier jobs of this Run left it. Its other
sections (the intro, *Sources*, the *Log*) describe the diocese and its lists; grep them
when you need one.

{_playbook(worktree, diocese)}"""


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
    headings = playbook.headings(lines)
    start = next((i for i, (_, title) in headings.items() if title == heading.strip()), None)
    if start is None:
        raise FactoryError(f"reads: {path} has no heading {heading!r}")
    level = headings[start][0]
    end = next((i for i, (lv, _) in headings.items() if i > start and lv <= level), len(lines))
    return "\n".join(lines[start:end]).strip() + "\n"


def _reads_by_file(spec: StageSpec) -> dict[str, list[str] | None]:
    """The stage's reads by file, in order: the headings it names, or None for the whole
    file (which a section of the same file adds nothing to)."""
    files: dict[str, list[str] | None] = {}
    for entry in spec.reads:
        path, _, heading = entry.partition("#")
        if not heading:
            files[path] = None
        elif (headings := files.setdefault(path, [])) is not None:
            headings.append(heading.strip())
    return files


def read_files(spec: StageSpec, text_of: TextOf, run_id: str,
               job_name: str) -> dict[str, str]:
    """The files the dispatcher writes in the job's scratch folder before its worker starts:
    for each file the stage reads sections of, those sections in order. Raises FactoryError
    when a file or heading is missing, so the job fails before its worker starts."""
    out = {}
    for path, headings in _reads_by_file(spec).items():
        if headings is None:
            read_entry(text_of, path)  # it must exist
            continue
        out[reads_rel(run_id, job_name, path)] = "\n".join(
            read_entry(text_of, f"{path}#{h}") for h in headings)
    return out


def message_label(kind: str) -> str:
    """What an attempt's prompt is: a job's first message, or a resumed session's next."""
    return "first message" if kind in ("start", "fresh") else f"{kind} message"


def given(spec: StageSpec, message: str, text_of: TextOf, label: str = "first message",
          files: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """Each part of what a worker is given, with its size: the appended system prompt, the
    attempt's message, each skill it may load, each file it must read, and the input
    files its message points to (`input_files`)."""
    def part(kind: str, source: str | None, text: str | None, **extra: Any) -> dict[str, Any]:
        return {"part": kind, "source": source, "missing": text is None,
                "chars": len(text or ""), "tokens": tokens(text or ""), **extra}

    prompt = text_of(spec.prompt) if spec.prompt else ""
    parts = [part("system prompt", spec.prompt,
                  strip_frontmatter(prompt) if prompt is not None else None),
             part(label, None, message)]
    for name in spec.skills:
        parts.append(part("skill", skill_path(name), text_of(skill_path(name)), name=name))
    # As the worker is given them: a section of a file it reads whole adds nothing.
    whole = {path for path, headings in _reads_by_file(spec).items() if headings is None}
    for entry in dict.fromkeys(spec.reads):
        path, _, heading = entry.partition("#")
        if heading and path in whole:
            continue
        try:
            parts.append(part("read", entry, read_entry(text_of, entry)))
        except FactoryError as exc:
            parts.append(part("read", entry, None, error=str(exc)))
    for path, text in (files or {}).items():
        parts.append(part("input file", path, text))
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
