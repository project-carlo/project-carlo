"""`python -m pdf_extract seed ...` (`pnpm seed ...`): the seeding agent's tools.

Batch: choosing parishes, verifying drafts, reviews (the factory, an eval run)
  pick      --eval RUN [--limit N] [--resume]      start or reuse a test run on the labeled parishes
  status                                            every file's status, questions, loaded
  check     <parish>... | --all                     check files against the database
  score     <run>                                   a test run's drafts against the labels
  questions [--open | --answered] [--by agent|person]
                                                    every question, its leaning and answer
  approve   <parish> --reviewer agent:NAME@COMMIT [--answers FILE]
                                                    an agent reviewer's answers and approval

Draft: one parish's file (the drafter)
  start     <parish>                    start a draft, or resume one; prints the brief
  brief     <parish>                    churches, website, bulletins, history, newest PDF
  mark-read <parish> <bulletin>         record a bulletin read, even when no slot cites it
  finalize  <parish>...                 fill in defaults, read marks, as_of, status; check

Write: the draft's slots, checked as they are written (`seed slot --help`: the specs)
  slot list    <parish>                            every slot: id, decision, page, entry
  slot show    <parish> <id>...                    slots in full, their sources numbered
  slot include <parish> ENTRY --src S... --why R   settled inclusions, one per day and time
  slot exclude <parish> [ENTRY] --src S... --why R slots left out (no ENTRY: nothing to record)
  slot ask     <parish> "Q" --option "*L" ENTRY --option L --src S --why R [--group G]
  slot edit    <parish> <id>... [--entry E] [--include|--exclude|--ask Q] [--option ...]
               [--page N] [--src S] [--drop-src N] [--why R] [--group G]
  slot rm      <parish> <id>...                    remove slots (never an answered one)
  slot batch   <parish> [file]                     those writes, one per line (- or none: stdin)
  summary      <parish> "text"                     what a reviewer reads first
  church-issue <parish> "church" "HEAD: said" [--rm]   a church the list lacks (R23)
  block        <parish> "reason" | --clear         R34

Read: the stored bulletins
  bulletins <parish> [--limit N]                      newest first, with pages and flags
  pdf       <parish> <bulletin>                       the PDF the pipeline reads, locally
  text      <parish> <bulletin> [--page N]            its text, page by page
  pages     <parish> <bulletin> [--page N] [--dpi D]  pages as PNGs
  grep      <parish> [pattern] [--bulletins N]        search every stored bulletin's text

Compare: other sources
  history   <parish> [--bulletins N]    extract mode's stored events (free; a hint)
  diff      <parish> [--bulletins N]    history no slot covers, and slots history lacks
  church    <query>                     whose church a name, town or address is
  site      <parish> [path or address] [--fresh] [--no-browser]
                                        a website page as text (never in a test run)

Paid calls: cached, recorded in the file's `calls`, CARLO_SEED_CALL_LIMIT per parish (4)
  ask       <parish> <bulletin> --model M "question"   one question about one bulletin
  extract   <parish> <bulletin> --model M              a full extraction with POLICY

A bulletin is `latest` or a prefix of its content hash; M is gpt-6.1-sol or
gemini-3-flash-preview. Every command but `score` and `approve` takes `--eval RUN`
to work on a test run's drafts (data/seed-evals/RUN/seeds/); one that needs a file
and finds only a test run's draft asks whether you meant `--eval RUN`. Output is
compact text, or the JSON result with `--json`. Drafters run `finalize`,
which checks; the factory's gates and an eval's verification run `check`. `approve`
is the factory's seed-review agent's (docs/factory-spec.md); the owner changes an
answer in the labeler. Workflow: docs/factory-spec.md (seed Runs),
.claude/skills/seed-evals/ (eval runs) and .claude/skills/draft-parish-seed/
(drafting; rules.md holds the decision rules).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract.classifiers.seed_ask import MODELS
from pdf_extract.db import ensure_db
from pdf_extract.schedule.store import parish_churches
from pdf_extract.seeding import queries
from pdf_extract.seeding import slots as slot_writes
from pdf_extract.seeding.calls import call_limit, load_or_start, run_ask, run_extract
from pdf_extract.seeding.checks import check_seed
from pdf_extract.seeding.coverage import diff, event_parts, missing_warning
from pdf_extract.seeding.files import (
    APPROVED,
    BLOCKED,
    NEEDS_HUMAN,
    SeedFileError,
    SeedSummary,
    asked_questions,
    eval_drafts,
    read_seed,
    seed_path,
    seed_slugs,
    write_seed_file,
)
from pdf_extract.seeding.finalize import finalize_seed
from pdf_extract.seeding.loader import is_loaded
from pdf_extract.seeding.queries import SeedContext, SeedError
from pdf_extract.seeding.review import SeedReviewError, approve_seed, is_agent
from pdf_extract.seeding.score import score_run
from pdf_extract.seeding.site import read_site, resolve_url
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db

Result = dict[str, Any]


def _connect():
    ensure_db(DEFAULT_DB_PATH)
    return connect_db(DEFAULT_DB_PATH)


def _ctx(args: argparse.Namespace) -> SeedContext:
    if args.seed_command == "pick":
        # `pick` creates the test run's manifest that other commands require.
        return SeedContext()
    return SeedContext.for_run(getattr(args, "eval", None))


def _with_conn(fn: Callable[[Any, SeedContext, argparse.Namespace], Result]):
    def handler(args: argparse.Namespace) -> Result:
        ctx = _ctx(args)
        conn = _connect()
        try:
            return fn(conn, ctx, args)
        except SeedFileError as exc:
            raise SeedError(str(exc)) from exc
        finally:
            conn.close()
    return handler


# ── Handlers ────────────────────────────────────────────────────────────────
def _pick(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    if not args.eval:
        raise SeedError("pick starts a test run: name it with --eval RUN (production seeds "
                        "come from the factory's seed Runs)")
    return queries.start_eval_run(conn, args.eval, limit=args.limit, resume=args.resume)


def _no_seed_file(ctx: SeedContext, slug: str) -> str:
    """Why a command needing the parish's file can't run: often a forgotten `--eval`."""
    runs = eval_drafts(slug) if ctx.eval_run is None else []
    if runs:
        return (f"no seed file in data/seeds/, but test run {', '.join(runs)} has a draft "
                f"of it: did you mean {' or '.join(f'--eval {r}' for r in runs)}?")
    return f"no seed file: start one with `pnpm seed start {slug}`"


def _start(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    queries.parish_row(conn, args.parish)
    seed = read_seed(args.parish, ctx.seeds_dir)
    resumed = seed is not None
    warnings = []
    if resumed:
        if seed.get("status") == APPROVED:
            raise SeedError("An approved seed belongs to its reviewer; it cannot be resumed")
        ctx.cutoff(args.parish)
        path = seed_path(args.parish, ctx.seeds_dir)
    else:
        runs = eval_drafts(args.parish) if ctx.eval_run is None else []
        if runs:
            # Not an error: a test run's parish can be seeded for real too.
            warnings.append(f"test run {', '.join(runs)} has a draft of {args.parish}; this "
                            "started a production draft (to resume that one, pass --eval RUN)")
        seed = load_or_start(conn, ctx, args.parish)
        path = write_seed_file(seed, ctx.seeds_dir)
    held = queries.stored_pdfs(args.parish)
    stored = [b["content_hash"][:12] for b in seed["bulletins"]
              if held is None or b["content_hash"] in held]
    return {"parish": args.parish, "path": Path(os.path.relpath(path)).as_posix(),
            "bulletins": len(seed["bulletins"]), "stored": stored, "resumed": resumed,
            "status": seed.get("status"), "slots": len(seed.get("slots") or []),
            "calls": len(seed.get("calls") or []), "warnings": warnings,
            "brief": _brief(conn, ctx, args)}


def _mark_read(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    seed = read_seed(args.parish, ctx.seeds_dir)
    if seed is None:
        raise SeedError(f"{args.parish} has {_no_seed_file(ctx, args.parish)}")
    if seed.get("status") == APPROVED:
        raise SeedError("An approved seed belongs to its reviewer; it cannot be changed")
    bulletin = queries.resolve_bulletin(
        conn, args.parish, args.bulletin, cutoff=ctx.cutoff(args.parish),
    )
    listed = next((b for b in seed["bulletins"]
                   if b["content_hash"] == bulletin["content_hash"]), None)
    if listed is None:
        listed = {k: bulletin[k] for k in ("content_hash", "fetched_at", "published_date")}
        seed["bulletins"].append(listed)
        seed["bulletins"].sort(key=lambda b: b["fetched_at"], reverse=True)
    listed["read"] = True
    write_seed_file(seed, ctx.seeds_dir)
    return {"parish": args.parish, "bulletin": bulletin["content_hash"], "read": True}


def _brief(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.brief(conn, args.parish, cutoff=ctx.cutoff(args.parish))


def _bulletins(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.list_bulletins(
        conn, args.parish, cutoff=ctx.cutoff(args.parish), limit=args.limit,
    )


def _pdf(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.export_pdf(conn, args.parish, args.bulletin, cutoff=ctx.cutoff(args.parish))


def _text(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.page_texts(
        conn, args.parish, args.bulletin, page=args.page, cutoff=ctx.cutoff(args.parish),
    )


def _pages(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.render_pages(
        conn, args.parish, args.bulletin, page=args.page, dpi=args.dpi,
        cutoff=ctx.cutoff(args.parish),
    )


def _grep(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.grep_bulletins(
        conn, args.parish, args.pattern, bulletins=args.bulletins,
        cutoff=ctx.cutoff(args.parish),
    )


def _church(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.find_churches(conn, args.query)


def _site(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    if ctx.eval_run is not None:
        raise SeedError("A historical test run may not read live websites: they can show "
                        "changes after its cutoff")
    parish = queries.parish_row(conn, args.parish)
    url = resolve_url(parish["homepage_url"], args.where)
    return read_site(args.parish, url, browser=not args.no_browser, fresh=args.fresh)


def _diff(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    seed = read_seed(args.parish, ctx.seeds_dir)
    if seed is None:
        raise SeedError(f"{args.parish} has {_no_seed_file(ctx, args.parish)}")
    past = queries.recent_history(
        conn, args.parish, bulletins=args.bulletins, cutoff=ctx.cutoff(args.parish),
    )
    return {"parish": args.parish, **diff(seed, past)}


def _history(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    return queries.history(
        conn, args.parish, bulletins=args.bulletins, cutoff=ctx.cutoff(args.parish),
    )


def _extract(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    call = run_extract(conn, ctx, args.parish, args.bulletin, args.model)
    return {"parish": args.parish, "call": call, "limit": call_limit()}


def _ask(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    call = run_ask(conn, ctx, args.parish, args.bulletin, args.model, args.question)
    return {"parish": args.parish, "call": call, "limit": call_limit()}


def _finalize(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    warnings: dict[str, list[str]] = {}
    errors: dict[str, str] = {}
    for slug in args.parish:
        try:
            seed = read_seed(slug, ctx.seeds_dir)
            if seed is None:
                continue  # the check below reports it
            parish = queries.parish_row(conn, slug)
            churches = sorted(parish_churches(conn, parish["id"]))
            past = queries.recent_history(conn, slug, cutoff=ctx.cutoff(slug))
            seed = {**finalize_seed(seed, churches, past), "parish_slug": slug}
            write_seed_file(seed, ctx.seeds_dir)
            if seed.get("status") not in (APPROVED, BLOCKED):
                # History is a hint, so uncovered events are warnings, not failures.
                found = diff(seed, past)
                warnings[slug] = [missing_warning(row, len(found["bulletins"]))
                                  for row in found["missing"]]
        except (SeedFileError, SeedError, ValueError, TypeError, KeyError) as exc:
            errors[slug] = f"could not finalize: {exc}"
            continue
    result = _check(conn, ctx, args)
    for f in result["files"]:
        f["warnings"] = warnings.get(f["parish"], [])
        if f["parish"] in errors:
            f["problems"].append(errors[f["parish"]])
    result["passed"] = all(not f["problems"] for f in result["files"])
    return result


def _check(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    slugs = seed_slugs(ctx.seeds_dir) if getattr(args, "all", False) else args.parish
    if not slugs:
        raise SeedError("Name the parishes to check, or pass --all")
    files = []
    for slug in slugs:
        try:
            seed = read_seed(slug, ctx.seeds_dir)
            cutoff = ctx.cutoff(slug)
        except (SeedFileError, SeedError) as exc:
            files.append({"parish": slug, "status": "invalid", "problems": [str(exc)]})
            continue
        if seed is None:
            files.append({"parish": slug, "status": None,
                          "problems": [_no_seed_file(ctx, slug)]})
            continue
        # An approved file is its reviewer's: newer drafting evidence rules don't apply.
        problems = check_seed(conn, seed, parish_slug=slug, cutoff=cutoff,
                              check_evidence=seed.get("status") != APPROVED)
        summary = SeedSummary.of(slug, seed)
        files.append({
            "parish": slug, "status": summary.status,
            "open_questions": summary.open_questions, "problems": problems,
        })
    return {"passed": all(not f["problems"] for f in files), "files": files}


def _status(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    rows = []
    for slug in seed_slugs(ctx.seeds_dir):
        try:
            seed = read_seed(slug, ctx.seeds_dir)
            summary = SeedSummary.of(slug, seed)
        except SeedFileError as exc:
            seed, summary = None, SeedSummary.of(slug, None, problem=str(exc))
        loaded = None
        if ctx.eval_run is None and seed is not None:
            parish = conn.execute("SELECT id FROM parish WHERE slug = ?", (slug,)).fetchone()
            loaded = parish is not None and is_loaded(conn, parish["id"], seed)
        rows.append({**summary.__dict__, "loaded": loaded})
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {"eval_run": ctx.eval_run, "counts": counts, "seeds": rows}


def _questions(args: argparse.Namespace) -> Result:
    ctx = _ctx(args)
    if args.open and args.by:
        raise SeedError("--by picks answered questions; an open one has no answer yet")
    questions, problems = [], []
    for slug in seed_slugs(ctx.seeds_dir):
        try:
            seed = read_seed(slug, ctx.seeds_dir)
        except SeedFileError as exc:
            problems.append({"parish": slug, "problem": str(exc)})
            continue
        for q in asked_questions(seed or {}):
            # An agent's answers (the factory's seed-review) are kept apart from people's:
            # candidate rules come from people's decisions.
            by = None
            if q["answer"]:
                by = "agent" if is_agent(q["answer"].get("by")) else "person"
            if (args.open and q["status"] != NEEDS_HUMAN or args.answered and not q["answer"]
                    or args.by and by != args.by):
                continue
            questions.append({"parish": slug, **q, "answered_by": by})
    answered = [q for q in questions if q["answer"]]
    return {
        "eval_run": ctx.eval_run, "questions": questions, "problems": problems,
        "totals": {"questions": len(questions), "answered": len(answered),
                   "matched_leaning": sum(1 for q in answered if q["matched"]),
                   "answered_by_person": sum(1 for q in answered
                                             if q["answered_by"] == "person"),
                   "answered_by_agent": sum(1 for q in answered
                                            if q["answered_by"] == "agent")},
    }


def _approve(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    if read_seed(args.parish, ctx.seeds_dir) is None:
        raise SeedError(f"{args.parish} has no seed file to approve")
    answers: Any = []
    if args.answers is not None:
        if args.answers == "-":
            text = sys.stdin.read()
        else:
            try:
                text = Path(args.answers).read_text(encoding="utf-8")
            except OSError as exc:
                raise SeedError(f"can't read the answers {args.answers}: {exc}") from exc
        try:
            answers = json.loads(text)
        except json.JSONDecodeError as exc:
            raise SeedError(f"the answers {args.answers} are not JSON: {exc}") from exc
    try:
        result = approve_seed(conn, args.parish, args.reviewer, answers, ctx.seeds_dir)
    except SeedReviewError as exc:
        raise SeedError(f"can't approve {args.parish}: {exc}") from exc
    path = seed_path(args.parish, ctx.seeds_dir)
    return {**result, "path": Path(os.path.relpath(path)).as_posix()}


def _score(args: argparse.Namespace) -> Result:
    report = score_run(args.run)
    run_dir = SeedContext.for_run(args.run).seeds_dir.parent
    return {
        "eval_run": args.run,
        "totals": report["totals"],
        "not_drafted": report["not_drafted"],
        "report": (run_dir / "report.md").as_posix(),
    }


def _read_for_slots(ctx: SeedContext, slug: str) -> dict[str, Any]:
    seed = read_seed(slug, ctx.seeds_dir)
    if seed is None:
        raise SeedError(f"{slug} has {_no_seed_file(ctx, slug)}")
    if seed.get("parish_slug") != slug:
        raise SeedError(f"the file's parish_slug is {seed.get('parish_slug')!r}, not {slug}")
    return seed


def _file_view(slug: str, seed: dict[str, Any]) -> Result:
    return {
        "parish": slug, "status": seed.get("status"), "summary": seed.get("summary"),
        "blocked_reason": seed.get("blocked_reason"),
        "open_questions": SeedSummary.of(slug, seed).open_questions,
        "church_list_issues": seed.get("church_list_issues") or [],
    }


def _writer(verb: str):
    """A write command (`seed slot include`, `seed summary`, …, or a whole `slot batch`):
    apply it to the file in memory, check the slots it touched, and write the file."""
    def handler(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
        seed = _read_for_slots(ctx, args.parish)
        ctx.cutoff(args.parish)  # a test run's parish must be in the run
        parish = queries.parish_row(conn, args.parish)
        draft = slot_writes.Draft(seed, parish_churches(conn, parish["id"]), ctx.eval_run)
        if verb == "batch":
            if args.file in (None, "-"):
                text = sys.stdin.read()
            else:
                try:
                    text = Path(args.file).read_text(encoding="utf-8")
                except OSError as exc:
                    raise SeedError(f"can't read the batch {args.file}: {exc}") from exc
            slot_writes.run_batch(draft, text)
        else:
            slot_writes.WRITES[verb](draft, args)
        draft.check()
        path = write_seed_file(draft.seed, ctx.seeds_dir)
        return {
            **_file_view(args.parish, draft.seed), "verb": verb,
            "path": Path(os.path.relpath(path)).as_posix(),
            "slots": [draft.slot(i) for i in draft.touched], "removed": draft.removed,
            "total_slots": len(draft.slots), "warnings": draft.warnings,
        }
    return handler


def _slot_list(args: argparse.Namespace) -> Result:
    ctx = _ctx(args)
    seed = _read_for_slots(ctx, args.parish)
    slots = seed.get("slots") if isinstance(seed.get("slots"), list) else []
    return {**_file_view(args.parish, seed), "slots": slots}


def _slot_show(args: argparse.Namespace) -> Result:
    ctx = _ctx(args)
    seed = _read_for_slots(ctx, args.parish)
    by_id = {s.get("id"): s for s in seed.get("slots") or [] if isinstance(s, dict)}
    missing = [i for i in args.ids if i not in by_id]
    if missing:
        raise SeedError(f"no slot {', '.join(missing)} in {args.parish} "
                        f"(`pnpm seed slot list {args.parish}`)")
    return {"parish": args.parish, "slots": [by_id[i] for i in args.ids]}


# ── Text output ─────────────────────────────────────────────────────────────
def _when(value: str | None) -> str:
    return (value or "—")[:16].replace("T", " ")


def _row(ev: dict[str, Any], lead: str = "  ") -> str:
    p = event_parts(ev)
    page = ev.get("page_number")
    return (f"{lead}{p['kind']:13} {p['type']:10} {p['when']:10} {p['time']:11} "
            f"p{page if page else '-':<3} {p['church']}"
            + (f"  {p['extra']}" if p["extra"] else ""))


def _text_pick(r: Result) -> str:
    lines = [f"Test run {r['eval_run']} ({r['manifest']}): {r['drafted']} drafted"]
    lines += [f"  {p['parish']:45} cutoff {_when(p['cutoff'])}  label {p['label_hash'][:12]}"
              for p in r["parishes"]]
    if r["remaining"]:
        lines.append(f"…{r['remaining']} more")
    return "\n".join(lines)


def _text_bulletins(r: Result) -> str:
    lines = [f"{r['parish']}: bulletins, newest fetched first"
             + (f" (test run: none after {r['cutoff']})" if r["cutoff"] else "")]
    for b in r["bulletins"]:
        flags = []
        if b["wrong_bulletin"]:
            flags.append("extract mode: WRONG BULLETIN")
        if b["duplicate_of"]:
            flags.append(f"duplicate of {b['duplicate_of']}")
        if not b["stored"]:
            pages = "no PDF (history only)"
        else:
            pages = "unreadable" if b["pages"] is None else f"{b['pages']:>2} pp"
        lines.append(f"  {b['short']}  fetched {_when(b['fetched_at'])}  issue "
                     f"{b['published_date'] or '—':10}  {pages}" +
                     (f"  {'; '.join(flags)}" if flags else ""))
    if r["not_shown"]:
        lines.append(f"  …{r['not_shown']} older (--limit 0 lists all)")
    return "\n".join(lines)


def _text_pdf(r: Result) -> str:
    return f"{r['path']}  ({r['pages']} pages, fetched {_when(r['fetched_at'])})"


def _text_text(r: Result) -> str:
    lines = [f"{r['bulletin'][:12]}  {r['pages']} pages, fetched {_when(r['fetched_at'])}"]
    for p in r["texts"]:
        lines.append(f"=== page {p['page']}" +
                     (" (only an image: render it with `seed pages`)" if p["image_only"] else ""))
        if p["text"]:
            lines.append(p["text"])
    return "\n".join(lines)


def _text_pages(r: Result) -> str:
    return "\n".join(r["paths"])


def _text_history(r: Result) -> str:
    lines = [f"{r['parish']}: extract mode's stored events (older prompt; a hint, not a vote)"]
    if not r["bulletins"]:
        lines.append("  no processed bulletin")
    for b in r["bulletins"]:
        flag = "  WRONG BULLETIN" if b["wrong_bulletin"] else ""
        lines.append(f"{b['short']}  fetched {_when(b['fetched_at'])}  issue "
                     f"{b['published_date'] or '—'}  {len(b['events'])} events{flag}")
        lines += [_row(ev) for ev in b["events"]]
    return "\n".join(lines)


def _call_head(call: dict[str, Any], limit: int) -> str:
    cost = "—" if call.get("cost_usd") is None else f"${call['cost_usd']:.4f}"
    served = "cache (free)" if call["cached"] else f"API, {cost}"
    return f"{call['id']}: {call['kind']} {call['model']} on {call['bulletin'][:12]} ({served}; " \
        f"limit {limit} paid calls)"


def _text_extract(r: Result) -> str:
    call = r["call"]
    lines = [_call_head(call, r["limit"]),
             f"  issue {call.get('published_date') or '—'}"
             + ("  WRONG BULLETIN" if call.get("wrong_bulletin") else "")]
    lines += [_row(ev) for ev in call["events"]]
    return "\n".join(lines)


def _text_ask(r: Result) -> str:
    call = r["call"]
    return "\n".join([
        _call_head(call, r["limit"]),
        f"  Q: {call['question']}",
        f"  A: {call['answer']}",
        f"  page {call['page'] or '—'}: “{call['quote']}”",
    ])


def _text_check(r: Result) -> str:
    lines = []
    for f in r["files"]:
        head = f"{f['parish']}: {f['status'] or 'missing'}"
        if f.get("open_questions"):
            head += f", {f['open_questions']} open questions"
        lines.append(head + ("" if f["problems"] else "  OK"))
        lines += [f"  - {p}" for p in f["problems"]]
        lines += [f"  ! {w}" for w in f.get("warnings") or []]
    return "\n".join(lines)


def _text_status(r: Result) -> str:
    lines = [", ".join(f"{n} {s}" for s, n in sorted(r["counts"].items())) or "No seed files."]
    for s in r["seeds"]:
        loaded = {True: "loaded", False: "not loaded", None: ""}[s["loaded"]]
        detail = s["problem"] or s["blocked_reason"] or ""
        if s["church_list_issues"] and not detail:
            detail = f"{s['church_list_issues']} for the church list"
        lines.append(f"  {s['parish_slug']:45} {s['status']:12} {s['open_questions']:2} open  "
                     f"{s['included']:3} slots  {loaded:10} {detail}")
    return "\n".join(lines)


def _text_score(r: Result) -> str:
    t = r["totals"]

    def pct(v: float | None) -> str:
        return "—" if v is None else f"{100 * v:.0f}%"

    return "\n".join([
        f"Test run {r['eval_run']}: {t['parishes']} parishes scored"
        + (f", {len(r['not_drafted'])} not drafted" if r["not_drafted"] else ""),
        f"  settled precision {pct(t['settled_precision_strict'])} strict, "
        f"{pct(t['settled_precision_core'])} core; covers {pct(t['settled_recall_core'])} "
        "of label rows",
        f"  open questions {t['open_questions']} ({t['open_questions_per_parish']} per parish); "
        f"leaning matched {pct(t['leaning_matched'])}",
        f"  calls {t['calls']} ({t['paid_calls']} paid), ${t['cost_usd']:.4f}",
        f"  {r['report']}",
    ])


def _text_file_head(r: Result, n_slots: int) -> list[str]:
    head = f"{r['parish']}: {r['status']}, {n_slots} slots"
    if r["open_questions"]:
        head += f", {r['open_questions']} open questions"
    if r.get("blocked_reason"):
        head += f"; blocked: {r['blocked_reason']}"
    return [head]


def _text_issues(r: Result) -> list[str]:
    return [f"church list: {i.get('church')}: {i.get('said')}"
            + (f" ({i['bulletin']}" + (f" p{i['page']}" if i.get("page") else "") + ")"
               if i.get("bulletin") else "")
            for i in r["church_list_issues"] if isinstance(i, dict)]


def _text_slot_list(r: Result) -> str:
    lines = _text_file_head(r, len(r["slots"]))
    lines.append(f"summary: {r['summary'] or '(none yet: `seed summary`)'}")
    for slot in r["slots"]:
        lines += slot_writes.slot_lines(slot)
    return "\n".join(lines + _text_issues(r))


def _text_slot_show(r: Result) -> str:
    return "\n".join(line for slot in r["slots"] for line in slot_writes.slot_lines(slot,
                                                                                    full=True))


def _text_written(r: Result) -> str:
    lines = [f"{r['path']}: written"] + _text_file_head(r, r["total_slots"])
    if r["verb"] in ("summary", "batch") and r["summary"]:
        lines.append(f"summary: {r['summary']}")
    for slot in r["slots"]:
        lines += slot_writes.slot_lines(slot)
    if r["removed"]:
        lines.append(f"removed {', '.join(r['removed'])}")
    if r["verb"] in ("church-issue", "batch"):
        lines += _text_issues(r)
    lines += [f"! {w}" for w in r["warnings"]]
    return "\n".join(lines)


def _text_start(r: Result) -> str:
    if r["resumed"]:
        text = (f"{r['path']}: resumed an existing draft ({r['status']}, {r['slots']} slots, "
                f"{r['calls']} calls) listing {r['bulletins']} bulletins. Read it before "
                "editing; change only what needs correcting")
    else:
        text = f"{r['path']}: a new draft listing {r['bulletins']} bulletins"
    if len(r["stored"]) < r["bulletins"]:
        text += (f"; only {len(r['stored'])} have a stored PDF to read "
                 f"({', '.join(r['stored']) or 'none'}), the rest only history")
    text += "".join(f"\nwarning: {w}" for w in r["warnings"])
    return text + "\n\n" + _text_brief(r["brief"])


def _text_questions(r: Result) -> str:
    lines = []
    # People's answers (and open questions) first, then the agents' apart.
    people = [q for q in r["questions"] if q["answered_by"] != "agent"]
    agents = [q for q in r["questions"] if q["answered_by"] == "agent"]
    for q in people + agents:
        if agents and q is agents[0]:
            lines.append("Answered by agents:")
        where = q["group"] + f" ({', '.join(q['slots'])})" if q["group"] else q["slots"][0]
        lines.append(f"{q['parish']} {where}: {q['question']}")
        for i, o in enumerate(q["options"]):
            lines.append(f"  {'*' if o['leaning'] else ' '}{i} {o['label']}")
        a = q["answer"]
        if a is None:
            got = "open"
        else:
            got = {"leaning": f"answer: {a.get('choice')}, the leaning",
                   "other": f"answer: {a.get('choice')}, not the leaning"}.get(
                q["match"], f"answer: {q['match']}" + (", as leaning" if q["matched"] else ""))
            got += f"; {a.get('by')} {str(a.get('at') or '')[:10]}"
        lines.append(f"  {got}" + (f"  cites {', '.join(q['cites'])}" if q["cites"] else ""))
    lines += [f"{p['parish']}: {p['problem']}" for p in r["problems"]]
    t = r["totals"]
    by = (f" ({t['answered_by_person']} by people, {t['answered_by_agent']} by agents)"
          if t["answered_by_agent"] else "")
    lines.append(f"{t['questions']} questions, {t['answered']} answered{by}, "
                 f"{t['matched_leaning']} matched the leaning (* marks it)")
    return "\n".join(lines)


def _text_approve(r: Result) -> str:
    lines = [f"{r['path']}: {r['status']} by {r['reviewer']} at {_when(r['approved_at'])}"]
    lines += [f"  {', '.join(a['slots'])}: {a['choice']} ({a['decision']})"
              for a in r["answered"]]
    return "\n".join(lines)


def _text_brief(r: Result) -> str:
    lines = [f"{r['parish']}: {r['name']}  {r['website'] or '(no website)'}"]
    lines += [f"  {c['church']:40} {c['name']}, {c['address'] or '(no address)'}"
              for c in r["churches"]]
    lines.append(_text_bulletins(r["bulletins"]))
    week = r.get("newest_week")
    if week:
        held = " · ".join(f"{day[:3]} {'/'.join(w)}" for day, w in week["weeks"].items())
        lines.append(f"newest bulletin's week: {week['from']} to {week['to']}; weeks of the "
                     f"month it holds: {held}")
    n = len(r["history_bulletins"])
    if r["history"] is None:
        lines.append(f"history: {r['history_events']} distinct events in {n} bulletins: "
                     f"`pnpm seed history {r['parish']}`")
    elif not r["history"]:
        lines.append("history: none stored")
    else:
        since = f", dated ones from {r['history_since']}" if r["history_since"] else ""
        lines.append(f"history: events of the last {n} processed bulletins{since}, in how "
                     "many (older prompt; a hint, not a vote)")
        lines += [_row(h["event"], f"  {h['bulletins']}/{n} ") for h in r["history"]]
    pdf = r["pdf"]
    lines.append(f"newest PDF: {_text_pdf(pdf)}" if "path" in pdf
                 else f"newest PDF: none ({pdf['error']})")
    return "\n".join(lines)


def _text_grep(r: Result) -> str:
    what = "schedule words" if r["default_pattern"] else f"/{r['pattern']}/"
    lines = [f"{r['parish']}: {what} in {len(r['bulletins'])} bulletins with a stored PDF, "
             "newest first"]
    for b in r["bulletins"]:
        head = f"{b['short']} (issue {b['published_date'] or '—'})"
        if b["error"]:
            lines.append(f"{head}: unreadable ({b['error']})")
        elif not b["pages"]:
            lines.append(f"{head}: no match")
        for p in b["pages"]:
            where = f"{head} p{p['page']}"
            lines.append(f"{where}: only an image: render it with `seed pages`"
                         if p["image_only"] else where)
            for i, hunk in enumerate(p["hunks"]):
                if i:
                    lines.append("  --")
                lines += [f"  {'>' if line['match'] else ' '} {line['text']}" for line in hunk]
    if r["not_searched"]:
        lines.append(f"…{r['not_searched']} older not searched (no stored PDF, or --bulletins)")
    return "\n".join(lines)


def _text_church(r: Result) -> str:
    if not r["churches"]:
        return f"No church matches {r['query']!r}."
    return "\n".join(f"{c['church']:40} {c['parish']:40} {c['name']}, {c['address']}"
                     for c in r["churches"])


def _text_site(r: Result) -> str:
    when = "read earlier, " if r["cached"] else ""
    lines = [f"{r['final_url']}  ({when}{r['via']} at {r['read_at'][:16].replace('T', ' ')}; "
             f"cite it as {{\"source\": \"website\", \"url\": \"{r['final_url']}\"}})"]
    lines += [f"  note: {n}" for n in r["notes"]]
    if r["links"]:
        lines.append("schedule-like links on this page:")
        lines += [f"  {link['url']}  {link['text']}" for link in r["links"]]
    lines.append("=== text")
    lines.append(r["text"])
    return "\n".join(lines)


def _text_diff(r: Result) -> str:
    n = len(r["bulletins"])
    lines = [f"{r['parish']}: the seed against extract mode's history of {n} bulletins "
             f"({', '.join(r['bulletins']) or 'none'})"]
    lines.append("History events no slot or option covers"
                 + (f" (dated ones before {r['scope_date']} left out)" if r["scope_date"] else "")
                 + ":")
    for row in r["missing"]:
        pages = "/".join(f"p{p}" for p in row["pages"])
        lines.append(f"  {row['said']}  ({len(row['bulletins'])}/{n} bulletins"
                     + (f", {pages}" if pages else "") + ")")
    if not r["missing"]:
        lines.append("  none")
    lines.append("History events that read a slot at another time (confirm the slot's time):")
    lines += [f"  {d['slot']:5} {d['slot_said']}  history: {d['said']}  "
              f"({len(d['bulletins'])}/{n} bulletins)" for d in r["differs"]] or ["  none"]
    lines.append("Included slots history never had:")
    lines += [f"  {u['slot']:5} {u['said']}" for u in r["unseen"]] or ["  none"]
    return "\n".join(lines)


# ── Parser ──────────────────────────────────────────────────────────────────
def add_seed_parser(
    subparsers: argparse._SubParsersAction,
    add_common_args: Callable[[argparse.ArgumentParser], None],
) -> None:
    # argparse has no subcommand groups, so `seed --help` prints this module's
    # docstring, which lists the commands by phase, instead of its own list.
    parser = subparsers.add_parser(
        "seed", help="Draft, check and score parish seeds (docs/seeding-plan.md)",
        description=__doc__, usage="%(prog)s <command> ...",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(help_parser=parser)
    sub = parser.add_subparsers(dest="seed_command", metavar="<command>", help=argparse.SUPPRESS)

    def leaf(name: str, help_text: str, handler, render, *, eval_run: bool = True,
             listed: bool = True, under: Any = None, prog: str | None = None):
        p = (under or sub).add_parser(name, help=help_text if listed else None,
                                      description=help_text,
                                      prog=f"{prog or parser.prog} {name}")
        p.set_defaults(handler=handler, render=render)
        p.add_argument("--json", action="store_true", help="Print the JSON result")
        if eval_run:
            p.add_argument("--eval", metavar="RUN", help="Work on a test run's drafts")
        add_common_args(p)
        return p

    def parish(p: argparse.ArgumentParser) -> None:
        p.add_argument("parish", help="Parish slug")

    def bulletin(p: argparse.ArgumentParser) -> None:
        p.add_argument("bulletin", help="`latest` or a prefix of the content hash")

    # Batch
    p = leaf("pick", "Start or reuse a test run on the labeled parishes (--eval RUN)",
             _with_conn(_pick), _text_pick)
    p.add_argument("--limit", type=int, default=8, help="How many (0: all; default 8)")
    p.add_argument("--resume", action="store_true",
                   help="Also offer unfinished drafts (each resumed with `seed start`)")

    leaf("status", "Every seed file's status, and whether it is loaded", _with_conn(_status),
         _text_status)

    p = leaf("check", "Check seed files against the database", _with_conn(_check), _text_check)
    p.add_argument("parish", nargs="*", help="Parish slugs")
    p.add_argument("--all", action="store_true", help="Every seed file")
    p.set_defaults(fail_on_verification_error=True)

    p = leaf("score", "Score a test run's drafts against the labels", _score, _text_score,
             eval_run=False)
    p.add_argument("run", help="The test run's name")

    p = leaf("questions", "Every question the seed files asked: options, leaning, answer, "
             "and the rules its rationale cites", _questions, _text_questions)
    only = p.add_mutually_exclusive_group()
    only.add_argument("--open", action="store_true", help="Only questions still open")
    only.add_argument("--answered", action="store_true", help="Only answered questions")
    p.add_argument("--by", choices=("agent", "person"),
                   help="Only questions answered by an agent reviewer, or by a person")

    p = leaf("approve", "Answer a seed's open questions and approve it, for an agent reviewer "
             "(people approve in the labeler)", _with_conn(_approve), _text_approve,
             eval_run=False)
    parish(p)
    p.add_argument("--reviewer", required=True, metavar="agent:NAME@COMMIT",
                   help="The agent reviewer, recorded as each answer's `by` and as `reviewer`")
    p.add_argument("--answers", metavar="FILE",
                   help='A JSON list of {"slot", "choice", "entry", "page"} (-: stdin; '
                        "default: none, for a file with no open question)")

    # Draft
    for name in ("start", "init"):  # `init` is the old name, kept for old instructions
        p = leaf(name, "Start a parish's seed file, or resume the existing one, and print "
                 "where it starts from", _with_conn(_start), _text_start,
                 listed=name == "start")
        parish(p)
        if name == "init":
            p.add_argument("--resume", action="store_true", help=argparse.SUPPRESS)

    p = leaf("brief", "A parish's churches, website, bulletins, history and newest PDF",
             _with_conn(_brief), _text_brief)
    parish(p)

    p = leaf("mark-read", "Record a bulletin read, even when no slot cites it",
             _with_conn(_mark_read), lambda r: f"{r['parish']}: {r['bulletin'][:12]} marked read")
    parish(p)
    bulletin(p)

    p = leaf("finalize", "Fill in a draft's defaults, read bulletins, as_of and status; check it",
             _with_conn(_finalize), _text_check)
    p.add_argument("parish", nargs="+", help="Parish slugs")
    p.set_defaults(fail_on_verification_error=True)

    # Write
    slot = sub.add_parser("slot", help="List, add, change and remove a draft's slots",
                          description=slot_writes.USAGE, usage="%(prog)s <command> ...",
                          prog=f"{parser.prog} slot",
                          formatter_class=argparse.RawDescriptionHelpFormatter)
    slot.set_defaults(help_parser=slot)
    slot_sub = slot.add_subparsers(dest="slot_command", metavar="<command>")
    in_slot = {"under": slot_sub, "prog": slot.prog}

    p = leaf("list", "Every slot of a parish's file: id, decision, page, entry or question",
             _slot_list, _text_slot_list, **in_slot)
    parish(p)
    p = leaf("show", "Slots in full: entry, options, numbered sources, rationale, answer",
             _slot_show, _text_slot_show, **in_slot)
    parish(p)
    p.add_argument("ids", nargs="+", metavar="ID", help="Slot ids (s3 s4)")
    for name, help_text in (
        ("include", "Add settled inclusions: one slot per day or date and time"),
        ("exclude", "Add slots left out on purpose, each with its reason"),
        ("ask", "Add an open question (several days: one grouped slot each)"),
        ("edit", "Change slots' entry, decision, question, options, page, sources or "
                 "rationale; ids stay"),
        ("rm", "Remove slots the drafter added (never an answered one)"),
    ):
        p = leaf(name, help_text, _with_conn(_writer(name)), _text_written, **in_slot)
        parish(p)
        slot_writes.add_write_args(name, p)
    p = leaf("batch", "Apply write commands, one per line without `pnpm seed slot` and the "
             "parish (`include mass Sun 08:00,10:30 --src 'latest p2: …' --why 'R1: …'`); "
             "`\\` continues a line, `#` comments. All are written or none",
             _with_conn(_writer("batch")), _text_written, **in_slot)
    parish(p)
    p.add_argument("file", nargs="?", help="The batch file (default, or -: stdin)")

    for name, help_text in (
        ("summary", "Set the file's summary, which a reviewer reads first"),
        ("church-issue", "List a church or chapel the church list lacks, once (R23)"),
        ("block", "Block the parish with its reason (R34), or --clear it"),
    ):
        p = leaf(name, help_text, _with_conn(_writer(name)), _text_written)
        parish(p)
        slot_writes.add_write_args(name, p)

    # Read
    p = leaf("bulletins", "A parish's stored bulletins, newest first", _with_conn(_bulletins),
             _text_bulletins)
    parish(p)
    p.add_argument("--limit", type=int, default=8, help="How many (0: all; default 8)")

    p = leaf("pdf", "Write a bulletin's stored PDF to a local file", _with_conn(_pdf), _text_pdf)
    parish(p)
    bulletin(p)

    p = leaf("text", "A bulletin's text, page by page", _with_conn(_text), _text_text)
    parish(p)
    bulletin(p)
    p.add_argument("--page", type=int, help="Only this page (default: all)")

    p = leaf("pages", "Render a bulletin's pages to PNGs", _with_conn(_pages), _text_pages)
    parish(p)
    bulletin(p)
    p.add_argument("--page", type=int, help="Only this page (default: all)")
    p.add_argument("--dpi", type=int, default=150, help="Resolution (default 150)")

    p = leaf("grep", "Search the text of every bulletin with a stored PDF", _with_conn(_grep),
             _text_grep)
    parish(p)
    p.add_argument("pattern", nargs="?",
                   help="A regular expression, any case (default: schedule words)")
    p.add_argument("--bulletins", type=int, default=0,
                   help="Only the newest N (default 0: all)")

    # Compare
    p = leaf("history", "Extract mode's stored events for recent bulletins",
             _with_conn(_history), _text_history)
    parish(p)
    p.add_argument("--bulletins", type=int, default=queries.HISTORY_BULLETINS,
                   help=f"How many bulletins (default {queries.HISTORY_BULLETINS})")

    p = leaf("diff", "History events no slot covers, and included slots history never had",
             _with_conn(_diff), _text_diff)
    parish(p)
    p.add_argument("--bulletins", type=int,
                   help="The newest N processed bulletins (default: those with a stored PDF)")

    p = leaf("church", "Look a church up by slug, name, town or address", _with_conn(_church),
             _text_church)
    p.add_argument("query", help="Any part of a slug, name, town or address")

    p = leaf("site", "A page of the parish's website as text, with its schedule links",
             _with_conn(_site), _text_site)
    parish(p)
    p.add_argument("where", nargs="?",
                   help="A path on the parish's site (/mass-times) or a full address "
                        "(default: its homepage)")
    p.add_argument("--fresh", action="store_true", help="Read it again, not from today's copy")
    p.add_argument("--no-browser", action="store_true",
                   help="Only a plain request: never fall back to the stealth browser")

    # Paid calls
    p = leaf("ask", "One question about one bulletin (cached, recorded)", _with_conn(_ask),
             _text_ask)
    parish(p)
    bulletin(p)
    p.add_argument("--model", required=True, choices=MODELS)
    p.add_argument("question", help="The question, naming the page if you know it")

    p = leaf("extract", "A full extraction by an external model (cached, recorded)",
             _with_conn(_extract), _text_extract)
    parish(p)
    bulletin(p)
    p.add_argument("--model", required=True, choices=MODELS)
