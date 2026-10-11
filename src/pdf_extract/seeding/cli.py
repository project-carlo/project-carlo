"""`python -m pdf_extract seed ...` (`pnpm seed ...`): the seeding agent's tools.

    seed pick      [--limit N] [--diocese D] [--labeled --eval RUN] [--resume]
    seed init      <parish> [--resume]
    seed mark-read <parish> <bulletin>
    seed brief     <parish>
    seed bulletins <parish> [--limit N]
    seed pdf       <parish> <bulletin>
    seed text      <parish> <bulletin> [--page N]
    seed pages     <parish> <bulletin> [--page N] [--dpi D]
    seed grep      <parish> [pattern] [--bulletins N]
    seed history   <parish> [--bulletins N]
    seed diff      <parish> [--bulletins N]
    seed church    <query>
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
from pdf_extract.seeding.coverage import diff, event_parts, missing_warning
from pdf_extract.seeding.files import (
    APPROVED,
    BLOCKED,
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
    if args.seed_command == "pick":
        # `pick --labeled` creates the manifest that other commands require.
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
    if args.labeled:
        if not args.eval:
            raise SeedError("--labeled starts a test run: name it with --eval RUN")
        return queries.start_eval_run(conn, args.eval, limit=args.limit, resume=args.resume)
    if args.eval:
        raise SeedError("--eval with pick needs --labeled")
    return queries.pick(conn, limit=args.limit, diocese=args.diocese, seeds_dir=ctx.seeds_dir,
                        resume=args.resume)


def _init(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    queries.parish_row(conn, args.parish)
    seed = read_seed(args.parish, ctx.seeds_dir)
    resumed = seed is not None
    if resumed and not args.resume:
        raise SeedError(f"{seed_path(args.parish, ctx.seeds_dir)} exists already "
                        f"(use `pnpm seed init {args.parish} --resume` to continue, or "
                        f"`pnpm seed brief {args.parish}` to inspect it)")
    if resumed:
        if seed.get("status") == APPROVED:
            raise SeedError("An approved seed belongs to its reviewer; it cannot be resumed")
        ctx.cutoff(args.parish)
        path = seed_path(args.parish, ctx.seeds_dir)
    else:
        seed = load_or_start(conn, ctx, args.parish)
        path = write_seed_file(seed, ctx.seeds_dir)
    held = queries.stored_pdfs(args.parish)
    stored = [b["content_hash"][:12] for b in seed["bulletins"]
              if held is None or b["content_hash"] in held]
    return {"parish": args.parish, "path": Path(os.path.relpath(path)).as_posix(),
            "bulletins": len(seed["bulletins"]), "stored": stored,
            "resumed": resumed, "brief": _brief(conn, ctx, args)}


def _mark_read(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    seed = read_seed(args.parish, ctx.seeds_dir)
    if seed is None:
        raise SeedError(f"{args.parish} has no seed file: start one with `pnpm seed init`")
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


def _diff(conn, ctx: SeedContext, args: argparse.Namespace) -> Result:
    seed = read_seed(args.parish, ctx.seeds_dir)
    if seed is None:
        raise SeedError(f"{args.parish} has no seed file: start one with `pnpm seed init`")
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
            files.append({"parish": slug, "status": None, "problems": ["no seed file"]})
            continue
        problems = check_seed(conn, seed, parish_slug=slug, cutoff=cutoff)
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


def _row(ev: dict[str, Any], lead: str = "  ") -> str:
    p = event_parts(ev)
    page = ev.get("page_number")
    return (f"{lead}{p['kind']:13} {p['type']:10} {p['when']:10} {p['time']:11} "
            f"p{page if page else '-':<3} {p['church']}"
            + (f"  {p['extra']}" if p["extra"] else ""))


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
        lines += [f"  ! {w}" for w in f.get("warnings") or []]
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
    state = "resumed draft" if r["resumed"] else "a draft"
    text = f"{r['path']}: {state} listing {r['bulletins']} bulletins"
    if len(r["stored"]) < r["bulletins"]:
        text += (f"; only {len(r['stored'])} have a stored PDF to read "
                 f"({', '.join(r['stored']) or 'none'}), the rest only history")
    return text + "\n\n" + _text_brief(r["brief"])


def _text_brief(r: Result) -> str:
    lines = [f"{r['parish']}: {r['name']}  {r['website'] or '(no website)'}"]
    lines += [f"  {c['church']:40} {c['name']}, {c['address'] or '(no address)'}"
              for c in r["churches"]]
    lines.append(_text_bulletins(r["bulletins"]))
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
    lines.append("Included slots history never had:")
    lines += [f"  {u['slot']:5} {u['said']}" for u in r["unseen"]] or ["  none"]
    return "\n".join(lines)


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
    p.add_argument("--resume", action="store_true", help="Also offer unfinished drafts")

    p = leaf("init", "Start a parish's seed file, and print where it starts from",
             _with_conn(_init), _text_init)
    parish(p)
    p.add_argument("--resume", action="store_true",
                   help="Continue an existing draft, preserving its decisions and calls")

    p = leaf("mark-read", "Record a bulletin read, even when no slot cites it",
             _with_conn(_mark_read), lambda r: f"{r['parish']}: {r['bulletin'][:12]} marked read")
    parish(p)
    bulletin(p)

    p = leaf("brief", "A parish's churches, website, bulletins, history and newest PDF",
             _with_conn(_brief), _text_brief)
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

    p = leaf("grep", "Search the text of every bulletin with a stored PDF", _with_conn(_grep),
             _text_grep)
    parish(p)
    p.add_argument("pattern", nargs="?",
                   help="A regular expression, any case (default: schedule words)")
    p.add_argument("--bulletins", type=int, default=0,
                   help="Only the newest N (default 0: all)")

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
