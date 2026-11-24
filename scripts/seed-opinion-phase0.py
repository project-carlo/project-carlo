"""Phase 0 of docs/seed-second-opinion-plan.md: the blind luna reading against approved seeds.

For each approved seed in data/seeds/, gives gpt-6-luna the newest 2-4 of the
seed's bulletins (one per issue week, PDF still stored, fetched on or before
its `as_of`), with "today" at the newest one's fetch date, and compares its
schedule with the approved slots (`seeding.opinion.compare`).

Replies are cached under data/runs/seed-opinion/cache/, so a rerun pays only
for parishes not yet asked. Spending stops at --cap dollars: a call starts only
while what is spent, plus what the calls in flight may cost, stays under it.

Differences are counted as production will count them: a resolved one (a
settled R22-R26 exclusion, a slot the website settled, one resting only on
bulletins luna wasn't given; `seeding.opinion`) needs no answer and isn't.

    uv run python scripts/seed-opinion-phase0.py --limit 5
    uv run python scripts/seed-opinion-phase0.py --cap 1.2 --workers 24 --name prompt-v1
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Any

from pdf_extract.classifiers import pricing
from pdf_extract.classifiers.seed_opinion import (
    SeedOpinionCaller,
    bulletin_reads,
    opinion_entries,
    parse_reply,
    render_context,
)
from pdf_extract.dotenv import read_dotenv
from pdf_extract.seeding import opinion
from pdf_extract.seeding.files import SEEDS_DIR, read_seed, seed_slugs
from pdf_extract.seeding.queries import bulletin_pdf, pdf_stored
from pdf_extract.storage import DEFAULT_DB_PATH, churches_for_parish, connect_db

LOGGER = logging.getLogger("seed-opinion-phase0")
ROOT = Path("data/runs/seed-opinion")
CACHE = ROOT / "cache"


def pick_bulletins(seed: dict[str, Any], most: int) -> list[dict[str, Any]]:
    as_of = seed.get("as_of") or "9999"
    out, weeks = [], set()
    for b in sorted(seed.get("bulletins") or [], key=lambda b: b["fetched_at"], reverse=True):
        if b["fetched_at"] > as_of:
            continue
        week = b.get("published_date") or b["content_hash"]
        if week in weeks or not pdf_stored(seed["parish_slug"], b["content_hash"]):
            continue
        weeks.add(week)
        out.append(b)
        if len(out) == most:
            break
    return out


def cache_path(version: str, parish: str, bulletins, churches, today) -> Path:
    asked = json.dumps({
        "version": version,
        "bulletins": [b["content_hash"] for b in bulletins],
        "churches": sorted(churches, key=lambda c: str(c.get("slug"))),
        "today": today.isoformat(),
    }, sort_keys=True)
    return CACHE / f"{parish}-{sha256(asked.encode()).hexdigest()[:16]}.json"


class Budget:
    def __init__(self, cap: float, estimate: float) -> None:
        self.cap, self.estimate = cap, estimate
        self.spent, self.reserved, self.largest = 0.0, 0.0, 0.0
        self.lock = threading.Lock()

    def reserve(self) -> float | None:
        with self.lock:
            hold = max(self.estimate, self.largest * 1.5)
            if self.spent + self.reserved + hold > self.cap:
                return None
            self.reserved += hold
            return hold

    def settle(self, hold: float, cost: float) -> None:
        with self.lock:
            self.reserved -= hold
            self.spent += cost
            self.largest = max(self.largest, cost)


def ask(caller, parish, bulletins, churches, budget, replay: str | None = None) -> dict[str, Any]:
    if len(bulletins) < 2:
        return {"parish": parish, "skipped": f"{len(bulletins)} bulletin(s) with a stored PDF"}
    today = date.fromisoformat(bulletins[0]["fetched_at"][:10])
    path = cache_path(replay or caller.version, parish, bulletins, churches, today)
    if path.exists():
        record = json.loads(path.read_text())
        record["cached"] = True
        return record
    if replay:
        return {"parish": parish, "skipped": "not cached for the replayed version"}
    hold = budget.reserve()
    if hold is None:
        return {"parish": parish, "skipped": "budget"}
    cost = 0.0
    try:
        pdfs = [bulletin_pdf(parish, b["content_hash"]) for b in bulletins]
        reply = caller.opinion(pdfs, render_context(churches, today, bulletins))
        cost = pricing.call_cost(caller.model, reply.usage, service_tier=reply.service_tier) or 0.0
    finally:
        budget.settle(hold, cost)
    record = {
        "parish": parish, "version": caller.version, "today": today.isoformat(),
        "bulletins": [{k: b.get(k) for k in ("content_hash", "fetched_at", "published_date")}
                      for b in bulletins],
        "text": reply.text, "usage": reply.usage, "service_tier": reply.service_tier,
        "latency_ms": reply.latency_ms, "cost_usd": round(cost, 6),
    }
    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=1, ensure_ascii=False) + "\n")
    record["cached"] = False
    return record


def evaluate(
    record: dict[str, Any], seed: dict[str, Any], churches: list[dict[str, Any]],
) -> dict[str, Any]:
    payload, status = parse_reply(record["text"])
    if payload is None:
        return {"parish": record["parish"], "status": status}
    entries = opinion_entries(payload)
    slugs_fixed = opinion.fix_church_slugs(entries, [str(c.get("slug")) for c in churches])
    seen = [b["content_hash"] for b in record["bulletins"]]
    result = opinion.compare(seed, entries, record["today"], seen_bulletins=seen)
    return {
        "parish": record["parish"], "status": status,
        "bulletins": len(record["bulletins"]), "cost_usd": record["cost_usd"],
        "usage": record["usage"], "reads": bulletin_reads(payload),
        "church_list_needs_review": payload.get("church_list_needs_review") is True,
        "opinion_entries": len(entries), "seed_included": result["included"],
        "agree": len(result["agree"]), "out_of_scope": result["out_of_scope"],
        "slugs_fixed": slugs_fixed,
        "dropped": [{"why": d["why"], "slot": d.get("slot"),
                     "opinion": opinion.describe(d.get("opinion"))} for d in result["dropped"]],
        "differences": [
            {"kind": d["kind"], "slot": d.get("slot"), "fields": d.get("fields"),
             "opinion": opinion.describe(d.get("opinion")),
             "evidence": (d.get("opinion") or {}).get("evidence"),
             "seed": opinion.describe(d.get("seed")),
             "policy_exclusion": d.get("policy_exclusion"), "resolved": d.get("resolved")}
            for d in result["differences"]
        ],
        "groups": [
            {"kind": g[0]["kind"], "size": len(g),
             "opinion": [opinion.describe(d.get("opinion")) for d in g],
             "seed": [opinion.describe(d.get("seed")) for d in g],
             "slots": [d.get("slot") for d in g],
             "fields": g[0].get("fields"),
             "policy_exclusion": g[0].get("policy_exclusion"), "resolved": g[0].get("resolved")}
            for g in result["groups"]
        ],
    }


def median(values: list[float]) -> float:
    values = sorted(values)
    if not values:
        return 0.0
    mid = len(values) // 2
    return values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2


def counted(r: dict[str, Any], kinds: tuple[str, ...] = opinion.KINDS) -> int:
    """A parish's grouped differences that need an answer (resolved ones excluded)."""
    return sum(1 for g in r["groups"] if g["kind"] in kinds and not g.get("resolved"))


def report(results: list[dict[str, Any]], skipped: list[dict[str, Any]], spent: float) -> str:
    done = [r for r in results if "groups" in r]
    lines = ["# Seed second opinion", "",
             "gpt-6-luna read each approved seed's newest 2-4 bulletins blind; its schedule "
             "is compared with the approved slots (`seeding/opinion.py`). See "
             "docs/seed-second-opinion-plan.md.", ""]
    cost = sum(r.get("cost_usd") or 0 for r in done)
    out_tokens = [r["usage"].get("output_tokens") or 0 for r in done]
    reasoning = [r["usage"].get("reasoning_tokens") or 0 for r in done]
    lines += [f"- Parishes compared: {len(done)}; skipped: {len(skipped)} "
              f"({', '.join(f'{k}: {v}' for k, v in Counter(s['skipped'] for s in skipped).items()) or 'none'}); "
              f"unparseable: {sum(1 for r in results if 'groups' not in r)}",
              f"- Cost of these replies: ${cost:.3f} (median ${median([r['cost_usd'] for r in done]):.4f}, "
              f"mean ${cost / max(len(done), 1):.4f} a parish); spent this run: ${spent:.4f}",
              f"- Output tokens a parish: median {median(out_tokens):.0f}, mean "
              f"{sum(out_tokens) / max(len(done), 1):.0f} (reasoning: median {median(reasoning):.0f})",
              f"- Luna entries: {sum(r['opinion_entries'] for r in done)}; church slugs mapped "
              f"to a listed one: {sum(r.get('slugs_fixed') or 0 for r in done)}", ""]

    values = [counted(r) for r in done]
    agree = sum(r["agree"] for r in done)
    included = sum(r["seed_included"] for r in done)
    lines += ["## Counted differences (grouped: a Mon-Fri difference is one; resolved excluded)", "",
              "| measure | total | median | parishes with none | parishes with 3 or fewer |",
              "|---|---:|---:|---:|---:|"]
    for name, vals in (("all kinds", values),
                       *((k, [counted(r, (k,)) for r in done]) for k in opinion.KINDS)):
        lines.append(f"| {name} | {sum(vals)} | {median(vals):g} | "
                     f"{sum(1 for v in vals if v == 0)} | {sum(1 for v in vals if v <= 3)} |")
    resolved = Counter(g["resolved"] for r in done for g in r["groups"] if g.get("resolved"))
    dropped = Counter(d["why"] for r in done for d in r.get("dropped") or [])
    raw = sum(1 for r in done for d in r["differences"] if not d.get("resolved"))
    lines += ["", f"- Agreements: {agree} of luna's entries agree with a slot "
              f"({included} included slots in all).",
              f"- Ungrouped counted differences: {raw}.",
              "- Resolved groups (not counted): "
              + (", ".join(f"{k} {v}" for k, v in sorted(resolved.items())) or "none") + ".",
              "- Dropped as no difference: "
              + (", ".join(f"{k} {v}" for k, v in sorted(dropped.items())) or "none") + ".",
              "", "Distribution of counted differences:", ""]
    dist = Counter(min(v, 10) for v in values)
    lines += [f"- {'10+' if k == 10 else k}: {dist[k]} parishes" for k in sorted(dist)]
    lines += ["", "## Every parish (counted differences)", "", "| parish | bulletins | seed slots | agree | "
              + " | ".join(opinion.KINDS) + " | resolved | cost |",
              "|---|---:|---:|---:|" + "---:|" * len(opinion.KINDS) + "---:|---:|"]
    for r in sorted(done, key=lambda r: (-counted(r), r["parish"])):
        kinds = Counter(g["kind"] for g in r["groups"] if not g.get("resolved"))
        lines.append(f"| {r['parish']} | {r['bulletins']} | {r['seed_included']} | {r['agree']} | "
                     + " | ".join(str(kinds[k]) for k in opinion.KINDS)
                     + f" | {sum(1 for g in r['groups'] if g.get('resolved'))}"
                     + f" | ${r['cost_usd']:.4f} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--cap", type=float, default=2.0, help="dollars, all calls together")
    parser.add_argument("--limit", type=int, help="the first N approved seeds")
    parser.add_argument("--parish", action="append", help="only these (repeatable)")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--max-bulletins", type=int, default=4)
    parser.add_argument("--effort", default="high")
    parser.add_argument("--estimate", type=float, default=0.02,
                        help="what to hold for a call before any has been priced")
    parser.add_argument("--out", type=Path, help="the output folder (default: eval/phase0-<today>)")
    parser.add_argument("--name", help="write to data/runs/seed-opinion/eval/<name>/ instead")
    parser.add_argument("--replay", metavar="VERSION",
                        help="compare the cached replies of this caller version; make no calls")
    args = parser.parse_args()
    if args.out and args.name:
        parser.error("give --out or --name, not both")
    args.out = args.out or ROOT / "eval" / (args.name or f"phase0-{date.today()}")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    for k, v in read_dotenv().items():
        os.environ.setdefault(k, v)

    seeds = {}
    for slug in args.parish or seed_slugs(SEEDS_DIR):
        seed = read_seed(slug, SEEDS_DIR)
        if seed and seed.get("status") == "approved":
            seeds[slug] = seed
    slugs = sorted(seeds)[: args.limit] if args.limit else sorted(seeds)
    caller = SeedOpinionCaller(reasoning_effort=args.effort)
    budget = Budget(args.cap, args.estimate)
    conn = connect_db(DEFAULT_DB_PATH)
    # The database and the store lookups stay on this thread; workers only call.
    inputs = {s: (pick_bulletins(seeds[s], args.max_bulletins), churches_for_parish(conn, s))
              for s in slugs}
    records, skipped = [], []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(ask, caller, s, *inputs[s], budget, args.replay): s for s in slugs}
        for future in as_completed(futures):
            slug = futures[future]
            try:
                record = future.result()
            except Exception as exc:  # one parish failing doesn't stop the rest
                LOGGER.exception("%s failed", slug)
                skipped.append({"parish": slug, "skipped": f"error: {type(exc).__name__}"})
                continue
            if "skipped" in record:
                skipped.append(record)
            else:
                records.append(record)
            LOGGER.info("%s: %s; spent $%.4f", slug, record.get("skipped") or (
                "cached" if record.get("cached") else f"${record['cost_usd']:.4f}"), budget.spent)
    results = [evaluate(r, seeds[r["parish"]], inputs[r["parish"]][1]) for r in records]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(json.dumps(
        {"results": sorted(results, key=lambda r: r["parish"]), "skipped": skipped,
         "spent_this_run": round(budget.spent, 4), "version": args.replay or caller.version},
        indent=1, ensure_ascii=False) + "\n")
    (args.out / "report.md").write_text(report(results, skipped, budget.spent))
    print(f"spent ${budget.spent:.4f} this run; {len(results)} compared, {len(skipped)} skipped")
    print(args.out / "report.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
