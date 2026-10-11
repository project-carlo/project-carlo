"""`python -m pdf_extract seed ...` (`pnpm seed ...`): the seeding agent's tools.

    seed pick      [--limit N] [--diocese D] [--labeled --eval RUN]
    seed init      <parish>
    seed bulletins <parish> [--limit N]
    seed pdf       <parish> <bulletin>
    seed text      <parish> <bulletin> [--page N]
    seed pages     <parish> <bulletin> [--page N] [--dpi D]
    seed history   <parish> [--bulletins N]
    seed extract   <parish> <bulletin> --model M
    seed ask       <parish> <bulletin> --model M "question"
    seed finalize  <parish>...
    seed check     <parish>... | --all
    seed status
    seed score     <run>

A bulletin is `latest` or a prefix of its content hash. Every command but
`score` takes `--eval RUN` to work on a test run's drafts
(docs/seeding-plan.md, "Testing it first"). Output is compact text, or the
JSON result with `--json`. The workflow around these is the
`seed-parishes` skill (.claude/skills/seed-parishes/SKILL.md).
"""

from __future__ import annotations

import argparse
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract.classifiers.seed_ask import MODELS
from pdf_extract.db import ensure_db
from pdf_extract.schedule.store import parish_churches
from pdf_extract.seeding import queries
from pdf_extract.seeding.calls import call_limit, load_or_start, run_ask, run_extract
from pdf_extract.seeding.checks import check_seed
from pdf_extract.seeding.files import (
    SeedFileError,
    SeedSummary,
    read_seed,
    seed_path,
    seed_slugs,
    write_seed_file,
)
from pdf_extract.seeding.finalize import finalize_seed
from pdf_extract.seeding.loader import is_loaded
from pdf_extract.seeding.queries import SeedContext, SeedError
from pdf_extract.seeding.score import score_run
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db

Result = dict[str, Any]


def _connect():
    ensure_db(DEFAULT_DB_PATH)
    return connect_db(DEFAULT_DB_PATH)


def _ctx(args: argparse.Namespace) -> SeedContext:
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
    if args.labeled:
        if not args.eval:
            raise SeedError("--labeled starts a test run: name it with --eval RUN")
        return queries.start_eval_run(conn, args.eval, limit=args.limit)
    if args.eval:
        raise SeedError("--eval with pick needs --labeled")
    return queries.pick(conn, limit=args.limit, diocese=args.diocese, seeds_dir=ctx.seeds_dir)


def _init(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    queries.parish_row(conn, args.parish)
    if read_seed(args.parish, ctx.seeds_dir) is not None:
        raise SeedError(f"{seed_path(args.parish, ctx.seeds_dir)} exists already")
    seed = load_or_start(conn, ctx, args.parish)
    path = write_seed_file(seed, ctx.seeds_dir)
    held = queries.stored_pdfs(args.parish)
    stored = [b["content_hash"][:12] for b in seed["bulletins"]
              if held is None or b["content_hash"] in held]
    return {"parish": args.parish, "path": Path(os.path.relpath(path)).as_posix(),
            "bulletins": len(seed["bulletins"]), "stored": stored}


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
    for slug in args.parish:
        seed = read_seed(slug, ctx.seeds_dir)
        if seed is None:
            continue  # the check below reports it
        parish = queries.parish_row(conn, slug)
        churches = sorted(parish_churches(conn, parish["id"]))
        write_seed_file({**finalize_seed(seed, churches), "parish_slug": slug}, ctx.seeds_dir)
    return _check(conn, ctx, args)


def _check(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    slugs = seed_slugs(ctx.seeds_dir) if getattr(args, "all", False) else args.parish
    if not slugs:
        raise SeedError("Name the parishes to check, or pass --all")
    files = []
    for slug in slugs:
        seed = read_seed(slug, ctx.seeds_dir)
        if seed is None:
            files.append({"parish": slug, "status": None, "problems": ["no seed file"]})
            continue
        problems = check_seed(conn, seed, parish_slug=slug, cutoff=ctx.cutoff(slug))
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


def _score(args: argparse.Namespace) -> Result:
    report = score_run(args.run)
    run_dir = SeedContext.for_run(args.run).seeds_dir.parent
    return {
        "eval_run": args.run,
        "totals": report["totals"],
        "not_drafted": report["not_drafted"],
        "report": (run_dir / "report.md").as_posix(),
    }


# ── Text output ─────────────────────────────────────────────────────────────
def _when(value: str | None) -> str:
    return (value or "—")[:16].replace("T", " ")


def _row(ev: dict[str, Any]) -> str:
    when = ev.get("day_of_week") or ev.get("date") or "?"
    end = f"–{ev['end_time']}" if ev.get("end_time") else ""
    extra = []
    if ev.get("weeks_of_month"):
        excluded = "except " if ev.get("exclude_weeks") else ""
        extra.append(f"weeks {excluded}" + "/".join(ev["weeks_of_month"]))
    if ev.get("season"):
        s = ev["season"]
        extra.append(f"season {s['start_month']}/{s.get('start_day') or ''}–"
                     f"{s['end_month']}/{s.get('end_day') or ''}")
    if ev.get("cancelled"):
        extra.append("CANCELLED")
    if ev.get("note"):
        extra.append(f"“{ev['note']}”")
    page = ev.get("page_number")
    kind = ev.get("event_kind") or "?"
    return (f"  {kind:13} {ev.get('event_type') or '?':10} {when:10} "
            f"{(ev.get('start_time') or '?') + end:11} p{page if page else '-':<3} "
            f"{ev.get('church_slug') or '?'}" + (f"  {'; '.join(extra)}" if extra else ""))


def _text_pick(r: Result) -> str:
    if "eval_run" in r:
        lines = [f"Test run {r['eval_run']} ({r['manifest']}): {r['drafted']} drafted"]
        lines += [f"  {p['parish']:45} cutoff {_when(p['cutoff'])}  label {p['label_hash'][:12]}"
                  for p in r["parishes"]]
    else:
        lines = ["parish                                        churches newest           "
                 "age  stable"]
        for p in r["parishes"]:
            stable = "—" if p["stability"] is None else f"{p['stability']:.2f}"
            age = "—" if p["newest_age_days"] is None else f"{p['newest_age_days']}d"
            lines.append(f"{p['parish']:45} {p['churches']:8} {_when(p['newest_fetched_at']):16} "
                         f"{age:>4} {stable:>7}")
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
    return "\n".join(lines)


def _text_status(r: Result) -> str:
    lines = [", ".join(f"{n} {s}" for s, n in sorted(r["counts"].items())) or "No seed files."]
    for s in r["seeds"]:
        loaded = {True: "loaded", False: "not loaded", None: ""}[s["loaded"]]
        detail = s["problem"] or s["blocked_reason"] or ""
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


def _text_init(r: Result) -> str:
    text = f"{r['path']}: a draft listing {r['bulletins']} bulletins"
    if len(r["stored"]) < r["bulletins"]:
        text += (f"; only {len(r['stored'])} have a stored PDF to read "
                 f"({', '.join(r['stored']) or 'none'}), the rest only history")
    return text


# ── Parser ──────────────────────────────────────────────────────────────────
def add_seed_parser(
    subparsers: argparse._SubParsersAction,
    add_common_args: Callable[[argparse.ArgumentParser], None],
) -> None:
    parser = subparsers.add_parser(
        "seed", help="Draft, check and score parish seeds (docs/seeding-plan.md)",
    )
    parser.set_defaults(help_parser=parser)
    sub = parser.add_subparsers(dest="seed_command")

    def leaf(name: str, help_text: str, handler, render, *, eval_run: bool = True):
        p = sub.add_parser(name, help=help_text)
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

    p = leaf("pick", "Parishes to seed next, easiest first", _with_conn(_pick), _text_pick)
    p.add_argument("--limit", type=int, default=8, help="How many (0: all; default 8)")
    p.add_argument("--diocese", help="Only this diocese's parishes")
    p.add_argument("--labeled", action="store_true",
                   help="The labeled parishes instead, for a test run (with --eval RUN)")

    p = leaf("init", "Start a parish's seed file", _with_conn(_init), _text_init)
    parish(p)

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

    p = leaf("history", "Extract mode's stored events for recent bulletins",
             _with_conn(_history), _text_history)
    parish(p)
    p.add_argument("--bulletins", type=int, default=4, help="How many bulletins (default 4)")

    p = leaf("extract", "A full extraction by an external model (cached, recorded)",
             _with_conn(_extract), _text_extract)
    parish(p)
    bulletin(p)
    p.add_argument("--model", required=True, choices=MODELS)

    p = leaf("ask", "One question about one bulletin (cached, recorded)", _with_conn(_ask),
             _text_ask)
    parish(p)
    bulletin(p)
    p.add_argument("--model", required=True, choices=MODELS)
    p.add_argument("question", help="The question, naming the page if you know it")

    p = leaf("finalize", "Fill in a draft's defaults, read bulletins, as_of and status; check it",
             _with_conn(_finalize), _text_check)
    p.add_argument("parish", nargs="+", help="Parish slugs")
    p.set_defaults(fail_on_verification_error=True)

    p = leaf("check", "Check seed files against the database", _with_conn(_check), _text_check)
    p.add_argument("parish", nargs="*", help="Parish slugs")
    p.add_argument("--all", action="store_true", help="Every seed file")
    p.set_defaults(fail_on_verification_error=True)

    leaf("status", "Every seed file's status, and whether it is loaded", _with_conn(_status),
         _text_status)

    p = leaf("score", "Score a test run's drafts against the labels", _score, _text_score,
             eval_run=False)
    p.add_argument("run", help="The test run's name")
