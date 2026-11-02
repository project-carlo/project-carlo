"""What the ledger shows: `factory status`, `queue`, `inspect <job>`, `prompt`, and the
Run's PR. The measurement reports (`quota`, `cost`, `inspect --stage`) are in
`metrics.report`."""

from __future__ import annotations

import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract.dioceses.records import parse_file
from pdf_extract.factory import git, playbook, render
from pdf_extract.factory.config import Config, FactoryError
from pdf_extract.factory.ledger import (
    ACTIVE,
    ANSWERED,
    LISTED,
    OPEN,
    PENDING,
    QUEUED,
    Ledger,
)
from pdf_extract.factory.ledger import SETTLED as FLAG_SETTLED
from pdf_extract.factory.metrics import report as mreport
from pdf_extract.factory.metrics.quota import WINDOWS, combine
from pdf_extract.factory.plan import diocese_dir, next_job, read_seed
from pdf_extract.factory.spec import load_stage, parse_stage, spec_path
from pdf_extract.factory.workers import strip_frontmatter

Commands = Callable[[str, Path], tuple[bool, str]]


def _flag(row: Any) -> dict[str, Any]:
    return {"id": row["id"], "severity": row["severity"], "scope": row["scope"],
            "subject": row["subject"], "question": row["question"],
            "suggestion": row["suggestion"], "status": row["status"],
            "issue": row["issue_number"], "answer": row["answer"]}


def status(ledger: Ledger) -> dict[str, Any]:
    runs = []
    for run in ledger.runs():
        jobs = ledger.jobs(run["id"])
        current = ledger.unfinished_job(run["id"])
        runs.append({
            "run": run["id"], "status": run["status"], "branch": run["branch"],
            "jobs": len(jobs), "done": sum(j["status"] == "done" for j in jobs),
            "cost_usd": round(sum(j["cost_usd"] for j in jobs), 2),
            "current": None if current is None else {
                "id": current["id"], "name": current["name"], "status": current["status"],
                "wait_until": current["wait_until"]},
            "waiting_on_you": [_flag(f) for f in ledger.flags(run["id"], OPEN)],
            "pr": run["pr_url"], "blocked_reason": run["blocked_reason"],
        })
    usage = [dict(r) for r in ledger.all(
        "SELECT u.* FROM usage u JOIN (SELECT account, MAX(id) AS id FROM usage GROUP BY "
        "account) last ON last.id = u.id ORDER BY u.account")]
    return {"paused": ledger.get("paused"), "usage_cooldown": ledger.get("usage_cooldown"),
            "override_caps": ledger.get("override_caps", False),
            "runs": runs, "usage": usage, "last_backup": ledger.get("backed_up"),
            "workers": ledger.get("worker_backend")}


def text_status(r: dict[str, Any]) -> str:
    lines = []
    if r["paused"]:
        lines.append(f"PAUSED: {r['paused'].get('reason')}")
    if r.get("usage_cooldown"):
        c = r["usage_cooldown"]
        lines.append(f"USAGE CHECK COOLDOWN: {c.get('reason')}; next retry {c['until'][:16]} "
                     f"(since {c.get('since', '')[:16]})")
    if r["override_caps"]:
        lines.append("Caps overridden (`pnpm factory pause` or `resume` to restore)")
    if r.get("workers") == "host":
        lines.append("WORKERS RUN ON THE HOST, not sandboxed (worker_backend: host)")
    for u in r["usage"]:
        lines.append(f"account {u['account']}: 5h {u['five_hour']:.0f}% (resets "
                     f"{u['five_hour_resets'][:16]}), week {u['seven_day']:.0f}% (resets "
                     f"{u['seven_day_resets'][:16]})  [{u['at'][:16]}]")
    for run in r["runs"]:
        head = (f"{run['run']:28} {run['status']:10} {run['done']}/{run['jobs']} jobs  "
                f"${run['cost_usd']:.2f}")
        if run["pr"]:
            head += f"  {run['pr']}"
        lines.append(head)
        if run["current"]:
            c = run["current"]
            lines.append(f"    now: job {c['id']} {c['name']} {c['status']}"
                         + (f" until {c['wait_until'][:16]}" if c["wait_until"] else ""))
        if run["blocked_reason"]:
            lines.append(f"    blocked: {run['blocked_reason'].splitlines()[0][:100]}")
        for f in run["waiting_on_you"]:
            lines.append(f"    issue #{f['issue']}: {f['subject']}: "
                         f"{f['question'].splitlines()[0][:90]}")
    return "\n".join(lines) or "No Runs yet."


def queue(ledger: Ledger, items: list[dict[str, Any]]) -> dict[str, Any]:
    started = {r["diocese"] for r in ledger.runs() if r["kind"] == "map"}
    return {"queue": [{**i, "started": i["diocese"] in started} for i in items],
            "pending_runs": [r["id"] for r in ledger.runs(PENDING)]}


def text_queue(r: dict[str, Any]) -> str:
    lines = [f"{'started ' if i['started'] else 'waiting '} {i['diocese']}"
             + (f": {i['notes']}" if i.get("notes") else "") for i in r["queue"]]
    if r["pending_runs"]:
        lines.append("pending Runs: " + ", ".join(r["pending_runs"]))
    return "\n".join(lines) or "The queue is empty."


def find_job(ledger: Ledger, ref: str) -> Any:
    """A job by its id, or by `<run>/<name>`."""
    if ref.isdigit():
        return ledger.job(int(ref))
    run_id, _, name = ref.partition("/")
    row = ledger.one("SELECT * FROM job WHERE run_id = ? AND name = ?", run_id, name)
    if row is None:
        raise KeyError(ref)
    return row


# ── Inspect ──────────────────────────────────────────────────────────────────
def inspect(ledger: Ledger, job: Any, runs_dir: Path,
            settle_seconds: int = Config.quota_settle_seconds) -> dict[str, Any]:
    """Everything about a job in one place, for a foreman review."""
    an, spans = mreport.analysis(ledger, settle_seconds)
    attempts = []
    rows = ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", job["id"])
    measures = mreport.measures(an, spans, [a["id"] for a in rows])
    for i, a in enumerate(rows):
        steps = ledger.one("SELECT COUNT(*) AS n FROM step WHERE attempt_id = ?", a["id"])["n"]
        attempts.append({
            "n": a["n"], "kind": a["kind"], "account": a["account"], "commit": a["commit_sha"],
            "started": a["started_at"], "finished": a["finished_at"], "outcome": a["outcome"],
            "error": a["error"], "cost_usd": a["cost_usd"], "turns": a["turns"], "steps": steps,
            "session": a["session_id"], "transcript": a["transcript"],
            "prompt": a["prompt"] if a["kind"] not in ("start", "fresh") else
            f"(the job input, {len(a['prompt'])} chars; --prompt prints it)",
            "meta": mreport.attempt_meta(ledger, a["id"]),
            "quota": {w: measures[w][i].as_dict() for w in WINDOWS},
            "rate_limits": mreport.rate_limits(ledger, a["id"]),
        })
    gates = [{"gate": g["name"], "passed": bool(g["passed"]), "output": g["output"][-800:],
              "at": g["at"]} for g in ledger.all("SELECT * FROM gate WHERE job_id = ? ORDER BY id",
                                                job["id"])]
    later = [{"by_job": v["job_id"], "subject": v["subject"], "verdict": v["verdict"],
              "problems": json.loads(v["problems"])}
             for v in ledger.all("SELECT * FROM verdict WHERE reviewed_job = ? ORDER BY id",
                                 job["id"])]
    decisions = [dict(d) for d in ledger.all("SELECT * FROM decision WHERE job_id = ?", job["id"])]
    requeued = [{"job": j["id"], "name": j["name"], "status": j["status"],
                 "answer": json.loads(j["input"]).get("answer")}
                for j in ledger.all("SELECT * FROM job WHERE resumes_job = ?", job["id"])]
    folder = runs_dir / job["run_id"] / job["name"]
    return {
        "job": job["id"], "name": f"{job['run_id']}/{job['name']}", "stage": job["stage"],
        "status": job["status"], "commit": job["commit_sha"], "account": job["account"],
        "input": json.loads(job["input"]), "send_backs": job["send_backs"],
        "continues": job["continues"], "cost_usd": job["cost_usd"], "turns": job["turns"],
        "created": job["created_at"], "started": job["started_at"], "finished": job["finished_at"],
        "handoff": json.loads(job["handoff"] or "null"),
        "gates": gates, "attempts": attempts,
        "quota": {w: combine(measures[w]) for w in WINDOWS},
        "flags": [_flag(f) for f in ledger.all("SELECT * FROM flag WHERE job_id = ?", job["id"])],
        "reviewed_by": later, "decisions": decisions, "answers_requeued": requeued,
        "actions": [a["name"] for a in ledger.all("SELECT name FROM action WHERE job_id = ?",
                                                  job["id"])],
        "transcripts": sorted(str(p) for p in folder.glob("*.jsonl")) if folder.exists() else [],
    }


def text_inspect(r: dict[str, Any]) -> str:
    lines = [f"{r['name']} (job {r['job']}): {r['stage']}, {r['status']}, commit "
             f"{(r['commit'] or '-')[:12]}, account {r['account'] or '-'}",
             f"cost ${r['cost_usd']:.2f}, {r['turns']} turns, {r['send_backs']} send-backs, "
             f"{r['continues']} continues; {r['started'] or '-'} → {r['finished'] or '-'}",
             f"input: {json.dumps(r['input'])}"]
    if r["handoff"]:
        lines.append("handoff: " + json.dumps(r["handoff"]))
    if r.get("quota"):
        lines.append("quota: " + "; ".join(
            f"{mreport.SHORT[w]} {q['label']} {q['text']}" for w, q in r["quota"].items())
            + " (points; dollars are an API-price diagnostic)")
    lines.append("attempts:")
    for a in r["attempts"]:
        lines.append(f"  {a['n']}. {a['kind']:9} {a['outcome'] or 'running':8} ${a['cost_usd']:.2f} "
                     f"{a['turns']} turns {a['steps']} steps  {a['error'] or ''}")
        if a["kind"] not in ("start", "fresh"):
            lines.append("     " + a["prompt"].replace("\n", "\n     ")[:1200])
        lines += ["     " + line for line in mreport.attempt_lines(a)]
    lines.append("gates:")
    lines += [f"  {'pass' if g['passed'] else 'FAIL'} {g['gate']}" + (
        "" if g["passed"] else "\n     " + g["output"].strip().replace("\n", "\n     ")[-600:])
        for g in r["gates"]]
    for f in r["flags"]:
        lines.append(f"flag {f['severity']}/{f['scope']} {f['subject']}: {f['question'][:120]} "
                     f"[{f['status']}{', #' + str(f['issue']) if f['issue'] else ''}]"
                     + (f" answer: {f['answer'][:200]}" if f["answer"] else ""))
    for v in r["reviewed_by"]:
        lines.append(f"reviewed by job {v['by_job']}: {v['subject']} {v['verdict']} "
                     + "; ".join(v["problems"])[:300])
    for d in r["decisions"]:
        lines.append(f"decision {d['parish']} {d['slot']}: {d['choice']} ({d['basis']}"
                     f"{', against the lean' if d['against_lean'] else ''})")
    for q in r["answers_requeued"]:
        lines.append(f"answer requeued as job {q['job']} {q['name']} ({q['status']})")
    lines += [f"transcript: {t}" for t in r["transcripts"]]
    return "\n".join(lines)


# ── The PR ───────────────────────────────────────────────────────────────────
def _diocese_name(worktree: Path, diocese: str) -> str:
    try:
        front, _ = parse_file(diocese_dir(worktree, diocese) / "diocese.md")
        return str(front.get("name") or diocese)
    except Exception:
        return diocese


def _coverage(worktree: Path, diocese: str, commands: Commands) -> list[str]:
    ok, out = commands(f"pnpm --silent diocese coverage {diocese}", worktree)
    try:
        data = json.loads(out[out.index("{"):]) if ok else None
    except ValueError:
        data = None
    if not data:
        return ["- (coverage unavailable)"]
    reps = data.get("rosters") or [v for v in data.values() if isinstance(v, dict)]
    lines = []
    for rep in reps if isinstance(reps, list) else []:
        if isinstance(rep, dict) and rep.get("roster"):
            lines.append(f"- {rep.get('title') or rep['roster']}: {rep.get('accounted_for')} "
                         f"accounted for; modelled {rep.get('modelled')}")
    return lines or ["- (coverage unavailable)"]


def _one_line(text: Any) -> str:
    return " ".join(str(text or "").split())


def _left_open(worktree: Path, diocese: str) -> list[str]:
    """The `open/` records: places with no source yet for Mass or a closure. They need no
    flag; the PR lists them from the files, with what would settle each."""
    lines = []
    for path in sorted((diocese_dir(worktree, diocese) / "open").glob("*.md")):
        try:
            front, _ = parse_file(path)
        except Exception:
            lines.append(f"- `{path.stem}`: (unreadable)")
            continue
        name = f" {_one_line(front.get('name'))}" if front.get("name") else ""
        revisit = (str(front.get("revisit") or "").strip().splitlines() or ["-"])[0]
        after = f" (after {front['revisit_after']})" if front.get("revisit_after") else ""
        lines.append(f"- `{path.stem}`{name}: {revisit}{after}")
    return lines or ["- none"]


def _fetch_gaps(worktree: Path, diocese: str) -> list[str]:
    """Parishes whose bulletin `fetch` can't collect yet, by kind, as `pnpm diocese gaps`
    groups them. Read from the files: that command's JSON outgrows a command's output."""
    groups: dict[str, list[tuple[str, str]]] = {}
    for path in sorted((diocese_dir(worktree, diocese) / "parishes").glob("*.md")):
        try:
            gap = parse_file(path)[0].get("fetch_gap")
        except Exception:
            continue  # the validate gate reports it
        if isinstance(gap, dict):
            groups.setdefault(str(gap.get("kind") or "?"), []).append(
                (path.stem, _one_line(gap.get("note"))))
    lines = []
    for kind, entries in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        parishes = ", ".join(f"`{p}`" for p, _ in entries)
        lines.append(f"- `{kind}` ({len(entries)}): {parishes}. {entries[0][1]}".rstrip())
    return lines or ["- none"]


def _settled_lines(rows: list[Any], names: dict[int, str]) -> list[str]:
    if not rows:
        return []
    return ["", "<details><summary>"
            f"{len(rows)} advisory flag{'s' if len(rows) > 1 else ''} settled during the "
            "Run</summary>", "",
            *[f"- `{f['subject']}`: {f['question'].splitlines()[0]} **Settled"
              f"{' by ' + names[f['settled_by']] if f['settled_by'] in names else ''}:** "
              f"{_one_line(f['answer'])}" for f in rows],
            "", "</details>"]


def _flag_lines(rows: list[Any]) -> list[str]:
    return [f"- `{f['subject']}`: {f['question'].splitlines()[0]}"
            + (f" (#{f['issue_number']})" if f["issue_number"] else "") for f in rows] or ["- none"]


# Past this, the rules integrate changed are cut short, to keep the PR under GitHub's
# 65,536-character limit; the integrate commits' diffs of `diocese.md` have them whole.
RULE_CHANGES_CHARS = 30_000


def _playbook_lines(ledger: Ledger, jobs: list[Any], worktree: Path, diocese: str) -> list[str]:
    """The playbook's sizes as the PR leaves it and after each integrate, and every rule
    integrate merged or reworded, for the owner to check it still decides the same."""
    kb, targets = playbook.kb, playbook.TARGETS
    meta = diocese_dir(worktree, diocese) / "diocese.md"
    final = playbook.sizes(meta.read_text(encoding="utf-8") if meta.exists() else "")
    lines = [f"*Bulletin publishers here* {kb(final['publishers'])} (target "
             f"{kb(targets[playbook.PUBLISHERS])}), *Rules settled* {kb(final['rules'])} "
             f"(target {kb(targets[playbook.RULES])})"
             + (f"; {final['lessons']} new lessons not folded in." if final["lessons"] else ".")]
    integrates = [j for j in jobs if j["stage"] == "integrate" and j["status"] == "done"]
    steps = []
    for j in integrates:
        if sizes := ledger.action_result(j["id"], "playbook"):
            b, a = sizes["before"], sizes["after"]
            steps.append(f"- `{j['name']}`, {b['lessons']} lessons: publishers "
                         f"{kb(b['publishers'])} → {kb(a['publishers'])}, rules "
                         f"{kb(b['rules'])} → {kb(a['rules'])}")
    if steps:
        lines += ["", "Each integrate, before → after:", "", *steps]
    changes = [(j["name"], c) for j in integrates
               for c in json.loads(j["handoff"] or "{}").get("rules_changed") or []]
    if not changes:
        return lines
    cut = sum(len(c["now"]) + sum(map(len, c["was"])) for _, c in changes) > RULE_CHANGES_CHARS

    def text(t: str) -> str:
        t = _one_line(t)
        return t[:300].rstrip() + "…" if cut and len(t) > 300 else t

    lines += ["", "### Rules integrate merged or reworded", "",
              "Each should decide what the rules it replaced did; fix any that doesn't."
              + (" Cut short to fit: the integrate commits' diffs of `diocese.md` have them "
                 "whole." if cut else ""), ""]
    for name, c in changes:
        lines.append(f"- **Now** (`{name}`): {text(c['now'])}")
        lines += [f"  - was: {text(w)}" for w in c["was"]]
    return lines


def _decision_line(d: Any) -> str:
    against = "**against the lean** " if d["against_lean"] else ""
    return (f"- {against}`{d['parish']}` {d['slot']}: {d['question']} Lean: {d['lean'] or '-'}. "
            f"Chose: {d['choice']}. {d['why']}")


def pr_text(ledger: Ledger, run: Any, worktree: Path, commands: Commands) -> tuple[str, str]:
    diocese = run["diocese"]
    name = _diocese_name(worktree, diocese)
    jobs = ledger.jobs(run["id"])
    advisory = ledger.flags(run["id"], LISTED)
    settled = [f for f in ledger.flags(run["id"], FLAG_SETTLED)
               if f["severity"] == "advisory" and f["settled_by"]]
    parked = [f for f in ledger.flags(run["id"], OPEN, ANSWERED) if f["scope"] == "parish"]
    cost_usd = sum(j["cost_usd"] for j in jobs)
    lines = [f"Opened by the onboarding factory (`docs/factory.md`), Run `{run['id']}`: "
             f"{len(jobs)} jobs, ${cost_usd:.2f}."]
    if run["follow_up_of"]:
        lines.append(f"A follow-up of `{run['follow_up_of']}` for parishes answered after its "
                     "PR opened.")
    if run["kind"] == "map":
        title = f"{name}: map and promote ({run['id']})"
        batches = sum(1 for j in jobs if j["stage"] == "map" and j["status"] == "done")
        lessons = ledger.all("SELECT text FROM lesson WHERE run_id = ? AND stage = 'reconcile'",
                             run["id"])
        lines += ["", "## Coverage", "", *_coverage(worktree, diocese, commands),
                  "", f"{batches} map jobs.",
                  "", "## Left open", "",
                  "No source yet shows Mass or a closure; each record says what would "
                  "settle it.", "", *_left_open(worktree, diocese),
                  "", "## Bulletins fetch can't collect yet", "",
                  "Grouped by kind, as `pnpm diocese gaps` lists them for a collector fix.",
                  "", *_fetch_gaps(worktree, diocese),
                  "", "## Advisory flags", "", *_flag_lines(advisory),
                  *_settled_lines(settled, {j["id"]: j["name"] for j in jobs}),
                  "", "## Parked parishes", "", *_flag_lines(parked),
                  "", "## Playbook", "", *_playbook_lines(ledger, jobs, worktree, diocese),
                  "", "## Lessons for every diocese", "",
                  *([f"- {r['text']}" for r in lessons] or ["- none"])]
    else:
        title = f"{name}: seed {len(json.loads(run['parishes'] or '[]'))} parishes ({run['id']})"
        by_status: dict[str, list[str]] = {}
        for parish in json.loads(run["parishes"] or "[]"):
            seed = read_seed(worktree, parish)
            state = seed.get("status", "?") if seed else "no file"
            by_status.setdefault(state, []).append(parish)
        decisions = ledger.all("SELECT * FROM decision WHERE run_id = ? "
                               "ORDER BY against_lean DESC, parish, slot", run["id"])
        lines += ["", "## Seeds", "",
                  *[f"- **{s}** ({len(ps)}): {', '.join(ps)}"
                    + ("" if s == "approved" else " (not approved: left out of this PR)")
                    for s, ps in sorted(by_status.items())],
                  "", "## Decisions by seed-review", "",
                  "Every open question `seed-review` answered, and why; answers against the "
                  "drafter's lean first. Change any that's wrong before merging. A wrong "
                  "judgment may also be a reason to change rules.md.", ""]
        for basis, heading in (("judgment", "By judgment (no rule or precedent)"),
                               ("precedent", "By this diocese's precedents"),
                               ("rule", "By a rule the drafter missed")):
            mine = [d for d in decisions if d["basis"] == basis]
            if mine:
                lines += [f"### {heading}", "", *[_decision_line(d) for d in mine], ""]
        if not decisions:
            lines += ["- none", ""]
        lines += ["## Advisory flags", "", *_flag_lines(advisory),
                  "", "## Parked parishes", "", *_flag_lines(parked)]
    lines += ["", "🤖 Generated by the onboarding factory with [Claude Code]"
                  "(https://claude.com/claude-code)"]
    return title, "\n".join(lines)



# ── What a worker is given: `factory prompt` and `inspect --prompt` ──────────
def _sizes(parts: list[dict[str, Any]]) -> dict[str, Any]:
    return {"parts": parts, "tokens": sum(p["tokens"] for p in parts)}


def preview(ledger: Ledger, stage: str, run_id: str | None, *, repo: Path,
            lessons_before_integrate: int, inputs: dict[str, Any] | None = None
            ) -> dict[str, Any]:
    """What the next attempt of a stage's job would be given, without running anything:
    the Run's unfinished job of that stage, else a new job with the inputs the plan would
    give it (or `inputs`). Reads the ledger and the Run's worktree, and writes neither."""
    runs = [ledger.run(run_id)] if run_id else ledger.runs(ACTIVE)
    if not runs:
        raise FactoryError("no active Run: name one with --run")
    run = dict(runs[0])
    root = Path(run["worktree"])
    if not (root / ".git").exists():  # not set up yet, or retired: main's files instead
        root = repo
        run["worktree"] = str(root)
    spec = load_stage(stage, root)
    if not spec.is_agent:
        raise FactoryError(f"{stage} is a code stage: no worker runs it")
    job: Any = ledger.unfinished_job(run["id"])
    existing = inputs is None and job is not None and job["stage"] == stage
    if not existing:
        if inputs is None:
            nxt = next_job(ledger, run, lessons_before_integrate=lessons_before_integrate)
            if nxt is None or nxt.stage != stage:  # e.g. map while integrate is due first
                nxt = next_job(ledger, run, lessons_before_integrate=sys.maxsize)
            inputs = nxt.inputs if nxt is not None and nxt.stage == stage else {}
        seq = 1 + len(ledger.jobs(run["id"]))
        job = {"id": None, "run_id": run["id"], "name": f"{seq:03d}-{stage}", "stage": stage,
               "input": json.dumps(inputs), "status": QUEUED, "pending_prompt": None,
               "session_id": None, "resumes_job": None}
    values = render.job_values(ledger, run, job)
    kind, prompt, _ = render.next_prompt(ledger, run, job, spec, values)
    try:
        commit = git.head(root)
    except FactoryError:
        commit = None
    text_of = render.worktree_text(root)
    system = text_of(spec.prompt) if spec.prompt else ""
    files = render.input_files(ledger, run, job) if kind in ("start", "fresh") else {}
    return {"run": run["id"], "job": job["name"], "stage": stage, "existing": existing,
            "kind": kind, "input": json.loads(job["input"]), "files": str(root),
            "commit": commit, "deny": list(spec.deny),
            **_sizes(render.given(spec, prompt, text_of, render.message_label(kind), files)),
            "system_prompt": strip_frontmatter(system or ""), "first_message": prompt}


def attempt_prompt(ledger: Ledger, job: Any, n: int,
                   text_at: Callable[[str, str], str | None]) -> dict[str, Any]:
    """What one past attempt was given: its prompt as sent, and the stage's files at the
    commit it ran at (`text_at(commit, path)`), with their sizes."""
    attempt = ledger.one("SELECT * FROM attempt WHERE job_id = ? AND n = ?", job["id"], n)
    if attempt is None:
        return {"job": job["id"], "attempt": n, "prompt": None}
    sha = attempt["commit_sha"]
    spec_text = text_at(sha, spec_path(job["stage"])) if sha else None
    if spec_text is None:
        parts = [{"part": render.message_label(attempt["kind"]), "source": None,
                  "missing": False,
                  "chars": len(attempt["prompt"]), "tokens": render.tokens(attempt["prompt"])}]
    else:
        spec = parse_stage(job["stage"], spec_text, f"{sha[:12]}:{spec_path(job['stage'])}")
        parts = render.given(spec, attempt["prompt"], lambda path: text_at(sha, path),
                             render.message_label(attempt["kind"]))
    return {"job": job["id"], "name": f"{job['run_id']}/{job['name']}", "attempt": n,
            "kind": attempt["kind"], "commit": sha, "stage_files": spec_text is not None,
            **_sizes(parts), "prompt": attempt["prompt"]}


def _size_table(parts: list[dict[str, Any]], total: int) -> list[str]:
    width = max(len(p["part"]) for p in parts)
    lines = [f"  {'~tokens':>8}  {'part':{width}}  source"]
    for p in parts:
        note = " (missing)" if p["missing"] else ""
        lines.append(f"  {p['tokens']:>8,}  {p['part']:{width}}  {p['source'] or ''}{note}"
                     + (f": {p['error']}" if p.get("error") else ""))
    lines.append(f"  {total:>8,}  total (about four characters a token)")
    return lines


def text_preview(r: dict[str, Any]) -> str:
    what = "its next attempt" if r["existing"] else "a new job"
    lines = [f"{r['run']}/{r['job']}: {r['stage']}, {what} ({r['kind']}); files from "
             f"{r['files']} at {(r['commit'] or '-')[:12]}",
             f"input: {json.dumps(r['input'])}", "", *_size_table(r["parts"], r["tokens"])]
    if r.get("deny"):
        lines += ["", "denied besides the workers' own: " + ", ".join(r["deny"])]
    return "\n".join(lines + ["", "## Appended system prompt", "", r["system_prompt"], "",
                              f"## {render.message_label(r['kind']).capitalize()}", "",
                              r["first_message"]])


def text_attempt_prompt(r: dict[str, Any]) -> str:
    if r["prompt"] is None:
        return f"job {r['job']} has no attempt {r['attempt']}"
    head = (f"{r['name']} attempt {r['attempt']} ({r['kind']}), commit "
            f"{(r['commit'] or '-')[:12]}")
    if not r["stage_files"]:
        head += ": its stage files aren't in this checkout, so only the prompt is sized"
    return "\n".join([head, *_size_table(r["parts"], r["tokens"]), "", r["prompt"]])
