"""What the ledger shows: `factory status`, `inspect`, `cost`, and the PR summary (§10)."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract.dioceses.records import parse_file
from pdf_extract.factory.ledger import (
    ANSWERED,
    LISTED,
    OPEN,
    PENDING,
    Ledger,
)
from pdf_extract.factory.plan import diocese_dir

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
    return {"paused": ledger.get("paused"), "override_caps": ledger.get("override_caps", False),
            "runs": runs, "usage": usage, "last_backup": ledger.get("backed_up")}


def text_status(r: dict[str, Any]) -> str:
    lines = []
    if r["paused"]:
        lines.append(f"PAUSED: {r['paused'].get('reason')}")
    if r["override_caps"]:
        lines.append("Caps overridden (`pnpm factory pause` or `resume` to restore)")
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


def inspect(ledger: Ledger, job: Any, runs_dir: Path) -> dict[str, Any]:
    """Everything about a job in one place, for a foreman review (§9)."""
    attempts = []
    for a in ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", job["id"]):
        steps = ledger.one("SELECT COUNT(*) AS n FROM step WHERE attempt_id = ?", a["id"])["n"]
        attempts.append({
            "n": a["n"], "kind": a["kind"], "account": a["account"], "commit": a["commit_sha"],
            "started": a["started_at"], "finished": a["finished_at"], "outcome": a["outcome"],
            "error": a["error"], "cost_usd": a["cost_usd"], "turns": a["turns"], "steps": steps,
            "session": a["session_id"], "transcript": a["transcript"],
            "prompt": a["prompt"] if a["kind"] not in ("start", "fresh") else
            f"(the job input, {len(a['prompt'])} chars; --prompt prints it)",
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
    lines.append("attempts:")
    for a in r["attempts"]:
        lines.append(f"  {a['n']}. {a['kind']:9} {a['outcome'] or 'running':8} ${a['cost_usd']:.2f} "
                     f"{a['turns']} turns {a['steps']} steps  {a['error'] or ''}")
        if a["kind"] not in ("start", "fresh"):
            lines.append("     " + a["prompt"].replace("\n", "\n     ")[:1200])
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


def recent(ledger: Ledger, stage: str, last: int) -> dict[str, Any]:
    rows = ledger.all("SELECT * FROM job WHERE stage = ? ORDER BY id DESC LIMIT ?", stage, last)
    return {"stage": stage, "jobs": [{
        "job": j["id"], "name": f"{j['run_id']}/{j['name']}", "status": j["status"],
        "send_backs": j["send_backs"], "cost_usd": j["cost_usd"], "turns": j["turns"],
        "finished": j["finished_at"]} for j in rows]}


def text_recent(r: dict[str, Any]) -> str:
    return "\n".join(f"{j['job']:5} {j['name']:40} {j['status']:13} {j['send_backs']} sb  "
                     f"${j['cost_usd']:.2f} {j['turns']} turns" for j in r["jobs"]) or "No jobs."


def cost(ledger: Ledger, by_stage: bool) -> dict[str, Any]:
    key = "stage" if by_stage else "run_id"
    rows = ledger.all(f"SELECT {key} AS k, COUNT(*) AS jobs, SUM(cost_usd) AS cost, "
                      f"SUM(turns) AS turns FROM job GROUP BY {key} ORDER BY cost DESC")
    items = [{"key": r["k"], "jobs": r["jobs"], "cost_usd": round(r["cost"] or 0, 2),
              "turns": r["turns"] or 0} for r in rows]
    return {"by": "stage" if by_stage else "run", "rows": items,
            "total_usd": round(sum(i["cost_usd"] for i in items), 2)}


def text_cost(r: dict[str, Any]) -> str:
    lines = [f"{i['key']:30} {i['jobs']:4} jobs  ${i['cost_usd']:8.2f}  {i['turns']} turns"
             for i in r["rows"]]
    return "\n".join(lines + [f"{'total':30}            ${r['total_usd']:8.2f}"])


# ── The PR (§10) ─────────────────────────────────────────────────────────────
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


def _flag_lines(rows: list[Any]) -> list[str]:
    return [f"- `{f['subject']}`: {f['question'].splitlines()[0]}"
            + (f" (#{f['issue_number']})" if f["issue_number"] else "") for f in rows] or ["- none"]


def pr_text(ledger: Ledger, run: Any, worktree: Path, commands: Commands) -> tuple[str, str]:
    diocese = run["diocese"]
    name = _diocese_name(worktree, diocese)
    jobs = ledger.jobs(run["id"])
    advisory = ledger.flags(run["id"], LISTED)
    parked = [f for f in ledger.flags(run["id"], OPEN, ANSWERED) if f["scope"] == "parish"]
    cost_usd = sum(j["cost_usd"] for j in jobs)
    lines = [f"Opened by the onboarding factory (`docs/factory-spec.md`), Run `{run['id']}`: "
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
                  "", "## Advisory flags", "", *_flag_lines(advisory),
                  "", "## Parked parishes", "", *_flag_lines(parked),
                  "", "## Lessons for every diocese", "",
                  *([f"- {r['text']}" for r in lessons] or ["- none"])]
    else:
        title = f"{name}: seed {len(json.loads(run['parishes'] or '[]'))} parishes ({run['id']})"
        by_status: dict[str, list[str]] = {}
        for parish in json.loads(run["parishes"] or "[]"):
            path = worktree / "data" / "seeds" / f"{parish}.json"
            try:
                state = json.loads(path.read_text(encoding="utf-8")).get("status", "?")
            except (OSError, ValueError):
                state = "no file"
            by_status.setdefault(state, []).append(parish)
        decisions = ledger.all("SELECT * FROM decision WHERE run_id = ? AND basis = 'judgment' "
                               "ORDER BY against_lean DESC, parish, slot", run["id"])
        lines += ["", "## Seeds", "",
                  *[f"- **{s}** ({len(ps)}): {', '.join(ps)}" for s, ps in sorted(by_status.items())],
                  "", "## Decisions without a rule", "",
                  "Every question `seed-review` settled by judgment; answers against the "
                  "drafter's lean first. A wrong one is a reason to change the policy.", "",
                  *([f"- {'**against the lean** ' if d['against_lean'] else ''}`{d['parish']}` "
                     f"{d['slot']}: {d['question']} Lean: {d['lean'] or '-'}. Chose: "
                     f"{d['choice']}. {d['why']}" for d in decisions] or ["- none"]),
                  "", "## Advisory flags", "", *_flag_lines(advisory),
                  "", "## Parked parishes", "", *_flag_lines(parked)]
    lines += ["", "🤖 Generated by the onboarding factory with [Claude Code]"
                  "(https://claude.com/claude-code)"]
    return title, "\n".join(lines)

