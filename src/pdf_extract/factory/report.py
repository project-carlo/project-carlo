"""What the ledger shows: `factory status`, `inspect`, `quota`, `cost`, and the PR summary
(§10)."""

from __future__ import annotations

import json
import statistics
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pdf_extract.dioceses.records import parse_file
from pdf_extract.factory.config import QUOTA_SETTLE_SECONDS, FactoryError
from pdf_extract.factory.ledger import (
    ANSWERED,
    DONE,
    FAILED,
    JOB_BLOCKED,
    LISTED,
    OPEN,
    PENDING,
    UNFINISHED,
    Ledger,
)
from pdf_extract.factory.plan import diocese_dir, read_seed
from pdf_extract.factory.quota import (
    SETTLED,
    WINDOWS,
    Analysis,
    Measure,
    Reading,
    Span,
    combine,
    range_text,
    work_units,
)

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


# ── Quota ────────────────────────────────────────────────────────────────────
SHORT = {"five_hour": "5h", "seven_day": "week"}
META_JSON = ("models", "per_model", "gaps")


def analysis(ledger: Ledger,
             settle_seconds: int = QUOTA_SETTLE_SECONDS) -> tuple[Analysis, dict[int, Span]]:
    spans = {s.id: s for s in map(Span.from_row, ledger.all(
        "SELECT id, job_id, account, started_at, finished_at FROM attempt"))}
    readings = [Reading.from_row(r) for r in ledger.all("SELECT * FROM usage")]
    approx = {r["attempt_id"] for r in ledger.all(
        "SELECT attempt_id FROM attempt_meta WHERE approximate = 1")}
    return Analysis(list(spans.values()), readings, timedelta(seconds=settle_seconds),
                    approximate=approx), spans


def attempt_meta(ledger: Ledger, attempt_id: int) -> dict[str, Any] | None:
    row = ledger.one("SELECT * FROM attempt_meta WHERE attempt_id = ?", attempt_id)
    if row is None:
        return None
    meta = dict(row)
    for k in META_JSON:
        meta[k] = json.loads(meta[k]) if meta[k] else ([] if k != "per_model" else {})
    return meta


def _rate_limits(ledger: Ledger, attempt_id: int) -> dict[str, Any]:
    events = ledger.all("SELECT * FROM rate_limit_event WHERE attempt_id = ? ORDER BY id",
                        attempt_id)
    steps = ledger.one("SELECT COUNT(*) AS n FROM step WHERE attempt_id = ? AND "
                       "kind = 'rate_limit'", attempt_id)["n"]
    last = events[-1] if events else None
    return {"events": len(events), "steps": steps,
            "last_type": last["type"] if last else None,
            "last_status": last["status"] if last else None,
            "last_utilization": last["utilization"] if last else None}


def _measures(an: Analysis, spans: dict[int, Span], ids: list[int]) -> dict[str, list[Measure]]:
    return {w: [an.measure(spans[i], w) for i in ids] for w in WINDOWS}


def inspect(ledger: Ledger, job: Any, runs_dir: Path,
            settle_seconds: int = QUOTA_SETTLE_SECONDS) -> dict[str, Any]:
    """Everything about a job in one place, for a foreman review (§9)."""
    an, spans = analysis(ledger, settle_seconds)
    attempts = []
    rows = ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", job["id"])
    measures = _measures(an, spans, [a["id"] for a in rows])
    for i, a in enumerate(rows):
        steps = ledger.one("SELECT COUNT(*) AS n FROM step WHERE attempt_id = ?", a["id"])["n"]
        attempts.append({
            "n": a["n"], "kind": a["kind"], "account": a["account"], "commit": a["commit_sha"],
            "started": a["started_at"], "finished": a["finished_at"], "outcome": a["outcome"],
            "error": a["error"], "cost_usd": a["cost_usd"], "turns": a["turns"], "steps": steps,
            "session": a["session_id"], "transcript": a["transcript"],
            "prompt": a["prompt"] if a["kind"] not in ("start", "fresh") else
            f"(the job input, {len(a['prompt'])} chars; --prompt prints it)",
            "meta": attempt_meta(ledger, a["id"]),
            "quota": {w: measures[w][i].as_dict() for w in WINDOWS},
            "rate_limits": _rate_limits(ledger, a["id"]),
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
            f"{SHORT[w]} {q['label']} {q['text']}" for w, q in r["quota"].items())
            + " (points; dollars are an API-price diagnostic)")
    lines.append("attempts:")
    for a in r["attempts"]:
        lines.append(f"  {a['n']}. {a['kind']:9} {a['outcome'] or 'running':8} ${a['cost_usd']:.2f} "
                     f"{a['turns']} turns {a['steps']} steps  {a['error'] or ''}")
        if a["kind"] not in ("start", "fresh"):
            lines.append("     " + a["prompt"].replace("\n", "\n     ")[:1200])
        lines += ["     " + line for line in _attempt_quota_lines(a)]
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


def _attempt_quota_lines(a: dict[str, Any]) -> list[str]:
    lines, m = [], a.get("meta")
    if m:
        lines.append(
            f"model {m['model'] or '-'} (asked {m['requested_model'] or '-'}, effort "
            f"{m['effort'] or '-'}), cli {m['cli_version'] or '-'}, sdk {m['sdk_version'] or '-'}"
            f", {m['entrypoint'] or '-'}, plan {m['plan'] or '-'}, config {m['config_hash'] or '-'}"
            + (f", resumes attempt {m['resumed_from']}" if m["resumed_from"] else "")
            + f" [{m['source']}{', approximate' if m['approximate'] else ''}]")
        lines.append(
            f"tokens in {m['input_tokens'] or 0:,} out {m['output_tokens'] or 0:,} (thinking "
            f"{m['thinking_tokens'] or 0:,}) cache read {m['cache_read_tokens'] or 0:,} write "
            f"5m {m['cache_write_5m_tokens'] or 0:,} 1h {m['cache_write_1h_tokens'] or 0:,}; "
            f"{m['messages'] or 0} messages ({m['duplicate_records'] or 0} repeated records); "
            f"models {', '.join(m['models']) or '-'}; units {m['work_units'] or '-'}")
        lines += [f"gap: {g}" for g in m["gaps"]]
    for w, q in (a.get("quota") or {}).items():
        used = " → ".join(f"{x['value']:g}% @{x['at'][11:19]} ({x['source']} #{x['id']})"
                          for x in (q["before"], q["after"]) if x)
        group = (f" (group of attempts {','.join(map(str, q['group']))}: "
                 f"{range_text(q['group_low'], q['group_high'])})" if q["group"] else "")
        lines.append(f"{SHORT[w]:4} {q['label']} {q['text']}{group}"
                     + (" outside use?" if q["outside_use"] else "")
                     + (" approximate" if q["approximate"] else "")
                     + (f"  [{used}]" if used else "") + (f"  {q['note']}" if q["note"] else ""))
    rl = a.get("rate_limits") or {}
    if rl.get("events") or rl.get("steps"):
        lines.append(f"rate limits: {rl['events']} events ({rl['steps']} steps)"
                     + (f", last {rl['last_type']} {rl['last_status']} utilization "
                        f"{rl['last_utilization']}" if rl["events"] else ""))
    return lines


def recent(ledger: Ledger, stage: str, last: int,
           settle_seconds: int = QUOTA_SETTLE_SECONDS) -> dict[str, Any]:
    an, spans = analysis(ledger, settle_seconds)
    rows = ledger.all("SELECT * FROM job WHERE stage = ? ORDER BY id DESC LIMIT ?", stage, last)
    out = []
    for j in rows:
        ids = [a["id"] for a in ledger.all("SELECT id FROM attempt WHERE job_id = ?", j["id"])]
        ms = _measures(an, spans, ids)
        out.append({
            "job": j["id"], "name": f"{j['run_id']}/{j['name']}", "status": j["status"],
            "send_backs": j["send_backs"], "cost_usd": j["cost_usd"], "turns": j["turns"],
            "finished": j["finished_at"], **{w: combine(ms[w]) for w in WINDOWS}})
    return {"stage": stage, "jobs": out}


def text_recent(r: dict[str, Any]) -> str:
    return "\n".join(f"{j['job']:5} {j['name']:40} {j['status']:13} {j['send_backs']} sb  "
                     f"5h {j['five_hour']['label']} {j['five_hour']['text']:8} "
                     f"week {j['seven_day']['label']} {j['seven_day']['text']:6}  "
                     f"{j['turns']} turns  ${j['cost_usd']:.2f}"
                     for j in r["jobs"]) or "No jobs."


BY = ("stage", "model", "effort", "mode", "account", "plan", "date", "hour")


def _key(by: str, job: Any, meta: dict[str, Any] | None, tz: Any) -> str:
    meta = meta or {}
    if by == "stage":
        return job["stage"]
    if by in ("date", "hour"):
        started = job["started_at"] or job["created_at"]
        local = datetime.fromisoformat(started).astimezone(tz)
        value = local.date().isoformat() if by == "date" else f"{local.hour:02d}h"
    else:
        value = {"model": meta.get("model") or meta.get("requested_model"),
                 "effort": meta.get("effort"), "mode": meta.get("entrypoint"),
                 "account": job["account"], "plan": meta.get("plan")}[by]
    return f"{job['stage']} / {value or '?'}"  # similar work: always within a stage


def _per_unit(values: list[float]) -> dict[str, Any]:
    return {"median": round(statistics.median(values), 2), "low": round(min(values), 2),
            "high": round(max(values), 2)} if values else {}


def quota(ledger: Ledger, by: str = "stage", tz: str | None = None,
          settle_seconds: int = QUOTA_SETTLE_SECONDS) -> dict[str, Any]:
    """Points per unit of completed work, by stage (or within stages by model, effort,
    mode, account, plan, date or hour), with outcomes, sample sizes and coverage."""
    try:
        zone = ZoneInfo(tz) if tz else datetime.now().astimezone().tzinfo
    except (ZoneInfoNotFoundError, ValueError):
        raise FactoryError(f"unknown time zone {tz!r} (an IANA name, e.g. "
                           "America/New_York)") from None
    an, spans = analysis(ledger, settle_seconds)
    groups: dict[str, dict[str, Any]] = {}
    for job in ledger.all("SELECT * FROM job ORDER BY id"):
        attempts = ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", job["id"])
        if not attempts:
            continue
        metas = [attempt_meta(ledger, a["id"]) for a in attempts]
        g = groups.setdefault(_key(by, job, metas[0], zone), {
            "jobs": 0, "done": 0, "units": 0, "units_unknown": 0, "first_try": 0,
            "retries": 0, "send_backs": 0, "crashes_partials": 0, "unresolved": 0,
            "parked": 0, "cost_usd": 0.0,
            **{w: {"settled": [], "uncertain": [], "outside_use": 0} for w in WINDOWS}})
        g["jobs"] += 1
        g["retries"] += len(attempts) - 1
        g["send_backs"] += job["send_backs"]
        g["crashes_partials"] += sum(a["outcome"] in ("crash", "timeout", "partial")
                                     for a in attempts)
        g["cost_usd"] += job["cost_usd"]
        gates = ledger.all("SELECT passed FROM gate WHERE attempt_id = ?", attempts[0]["id"])
        g["first_try"] += bool(gates) and all(x["passed"] for x in gates)
        if job["status"] in (JOB_BLOCKED, FAILED, *UNFINISHED):
            g["unresolved"] += 1
        g["parked"] += ledger.one("SELECT COUNT(*) AS n FROM flag WHERE job_id = ? AND "
                                  "severity = 'blocking' AND scope = 'parish' AND status IN "
                                  "(?, ?)", job["id"], OPEN, ANSWERED)["n"]
        if job["status"] != DONE:
            continue
        g["done"] += 1
        units = next((m["work_units"] for m in reversed(metas) if m and m["work_units"]),
                     None) or work_units(job["stage"], json.loads(job["input"]))
        if not units:
            g["units_unknown"] += 1
            continue
        g["units"] += units
        ms = _measures(an, spans, [a["id"] for a in attempts])
        for w in WINDOWS:
            q = combine(ms[w])
            g[w]["outside_use"] += bool(q["outside_use"])
            if q["label"] == SETTLED and q["high"] is not None:
                g[w]["settled"].append(((q["low"] + q["high"]) / 2 / units,
                                        q["low"] / units, q["high"] / units))
            else:
                g[w]["uncertain"].append((q["low"] / units if q["low"] is not None else None,
                                          q["high"] / units if q["high"] is not None else None))
    rows = []
    for key in sorted(groups):
        g = groups[key]
        row: dict[str, Any] = {"key": key, **{k: g[k] for k in (
            "jobs", "done", "units", "units_unknown", "first_try", "retries", "send_backs",
            "crashes_partials", "unresolved", "parked")}}
        for w in WINDOWS:
            settled, uncertain = g[w]["settled"], g[w]["uncertain"]
            lows = [x[0] for x in uncertain if x[0] is not None]
            highs = [x[1] for x in uncertain]
            row[w] = {
                "samples": len(settled),
                "coverage": round(len(settled) / g["done"], 2) if g["done"] else None,
                "per_unit": _per_unit([x[0] for x in settled]),
                "settled_range": [round(min(x[1] for x in settled), 2),
                                  round(max(x[2] for x in settled), 2)] if settled else None,
                "uncertain": {"jobs": len(uncertain),
                              "low": round(min(lows), 2) if lows else None,
                              "high": None if not highs or any(h is None for h in highs)
                              else round(max(h for h in highs if h is not None), 2)},
                "outside_use": g[w]["outside_use"]}
        row["cost_usd_diagnostic"] = round(g["cost_usd"], 2)
        rows.append(row)
    return {"by": by, "timezone": str(zone), "settle_seconds": settle_seconds, "rows": rows,
            "note": "Points per unit of completed work from settled samples only (median and "
                    "the range of their ±1 bounds); uncertain jobs' ranges apart. Dollars are an "
                    "API-price diagnostic, not quota."}


def _window_text(q: dict[str, Any]) -> str:
    out = f"n={q['samples']}"
    if q["per_unit"]:
        p = q["per_unit"]
        lo, hi = q["settled_range"]
        out = f"{p['median']:g}/unit ({lo:g}–{hi:g}) " + out
    if q["coverage"] is not None:
        out += f" cov {q['coverage']:.0%}"
    u = q["uncertain"]
    if u["jobs"]:
        rng = "?" if u["low"] is None else (f"≥{u['low']:g}" if u["high"] is None
                                            else f"{u['low']:g}–{u['high']:g}")
        out += f"; {u['jobs']} uncertain {rng}/unit"
    if q["outside_use"]:
        out += f"; {q['outside_use']} near outside use"
    return out


def text_quota(r: dict[str, Any]) -> str:
    lines = [f"by {r['by']} ({r['timezone']}); a reading settles {r['settle_seconds']}s after "
             "an attempt"]
    for row in r["rows"]:
        lines.append(f"{row['key']}: {row['jobs']} jobs, {row['done']} done, {row['units']} "
                     f"units" + (f" ({row['units_unknown']} unknown)" if row["units_unknown"]
                                 else ""))
        for w in WINDOWS:
            lines.append(f"    {SHORT[w]:4} {_window_text(row[w])}")
        lines.append(f"    first-try passes {row['first_try']}, retries {row['retries']}, "
                     f"send-backs {row['send_backs']}, crashes/partials "
                     f"{row['crashes_partials']}, unresolved {row['unresolved']}, parked "
                     f"{row['parked']}; ${row['cost_usd_diagnostic']:.2f} (diagnostic)")
    lines.append(r["note"])
    return "\n".join(lines) if r["rows"] else "No attempts yet."


def windows(ledger: Ledger, settle_seconds: int = QUOTA_SETTLE_SECONDS) -> dict[str, Any]:
    """Per account and window instance: points used, and how much the factory's measured
    attempts explain (settled, shared, uncertain); the rest is unexplained."""
    an, _ = analysis(ledger, settle_seconds)
    rises = [{**r, "from": r["from"].isoformat(), "to": r["to"].isoformat()} for r in an.rises]
    return {"windows": an.window_totals(), "idle_rises": rises}


def text_windows(r: dict[str, Any]) -> str:
    lines = [f"{w['account']:10} {SHORT[w['window']]:4} resets {(w['resets'] or '-')[:16]}  "
             f"{w['readings']:3} readings  total {w['total']:g}: settled {w['settled']:g}, "
             f"shared {w['shared']:g}, uncertain {w['uncertain']:g}, unexplained "
             f"{w['unexplained']:g} (rose {w['idle_rises']:g} while idle)"
             for w in r["windows"]]
    lines += [f"idle rise: {x['account']} {SHORT[x['window']]} +{x['points']:g} "
              f"{x['from'][:16]} → {x['to'][:16]}" for x in r["idle_rises"]]
    return "\n".join(lines) or "No readings."


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


def _decision_line(d: Any) -> str:
    against = "**against the lean** " if d["against_lean"] else ""
    return (f"- {against}`{d['parish']}` {d['slot']}: {d['question']} Lean: {d['lean'] or '-'}. "
            f"Chose: {d['choice']}. {d['why']}")


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

