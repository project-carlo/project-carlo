"""`python -m pdf_extract diocese ...` (`pnpm diocese ...`): the command-line face of this package.

Every handler returns the JSON-serialisable dict that `__main__.main` prints.
Records are meant to be edited directly as files; the commands here create
them, check them, and do what touches several files at once.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract.dioceses import records, report, rosters, web
from pdf_extract.dioceses.records import EXCLUSION_REASONS, KINDS, PARISH, DioceseError

Handler = Callable[[argparse.Namespace], dict[str, Any]]


# ── New records ─────────────────────────────────────────────────────────────
def _from_roster(diocese: str, refs: list[str]) -> dict[str, Any]:
    """Fields, roster links and evidence for a record prefilled from roster entries.

    The first entry supplies the name, address and coordinates; every entry
    becomes a roster link and an evidence item dated to when its roster was
    fetched.
    """
    fields: dict[str, Any] = {"roster": [], "evidence": []}
    for ref in refs:
        roster, entry = rosters.get_entry(diocese, ref)
        fields["roster"].append(ref)
        address = ", ".join(str(entry[k]) for k in ("line1", "city", "state", "postal_code")
                            if entry.get(k))
        fields["evidence"].append({
            "url": entry.get("url") or roster.get("url") or "",
            "seen": roster.get("fetched") or records.today(),
            **({"quote": entry["address"]} if entry.get("address") else {}),
            "note": f"Listed in {roster.get('title') or roster['name']} as "
                    f"{entry.get('name', '')!r}" + (f", {address}" if address else "")
                    + "".join(f"; {k}: {entry[k]}" for k in ("kind", "group", "rite")
                              if entry.get(k)),
        })
        if "name" in fields:
            continue
        fields["name"] = entry.get("name", "")
        for f in ("line1", "city", "state", "postal_code"):
            fields[f] = str(entry.get(f) or "")
        if entry.get("latitude") is not None and entry.get("longitude") is not None:
            fields["latitude"], fields["longitude"] = entry["latitude"], entry["longitude"]
            fields["coordinates_from"] = ("gcatholic-plus-code" if entry.get("plus_code")
                                          else "diocese-directory")
    return fields


_NEW_FLAGS: dict[str, dict[str, str]] = {
    "parish": {
        "name": "name", "website": "website (where the bulletin can be found)",
        "bulletin-provider": f"one of {', '.join(sorted(records.KNOWN_BULLETIN_PROVIDERS))}",
        "provider-id": "account id for parishes_online (org slug) or discover_mass (church slug)",
        "group": "the diocese's grouping, e.g. 'Family #31' or a cluster name",
    },
    "church": {
        "parish": "slug of the parish (bulletin publisher) it belongs to",
        "name": "name", "line1": "street address", "line2": "", "city": "", "state": "",
        "postal-code": "", "latitude": "", "longitude": "",
        "coordinates-from": ", ".join(records.COORDINATE_SOURCES),
    },
    "excluded": {
        "name": "name", "reason": "; ".join(f"{k}: {v}" for k, v in EXCLUSION_REASONS.items()),
        "parish": "related parish slug, if any", "line1": "", "city": "", "state": "",
        "postal-code": "", "last-mass": "date of the last Mass, if closed",
    },
    "open": {
        "name": "name of the place, or a short title for the question",
        "revisit": "the next thing to check", "revisit-after": "date to check it after",
        "parish": "related parish slug, if any", "line1": "", "city": "", "state": "",
        "postal-code": "",
    },
}


def _cmd_new(kind_name: str) -> Handler:
    def run(args: argparse.Namespace) -> dict[str, Any]:
        fields: dict[str, Any] = {}
        if getattr(args, "from_", None):
            # Only what this kind records: an exclusion has no coordinates.
            allowed = records.KINDS[kind_name].fields
            fields.update({k: v for k, v in _from_roster(args.diocese, args.from_).items()
                           if k in allowed})
        for flag in _NEW_FLAGS[kind_name]:
            value = getattr(args, flag.replace("-", "_"))
            if value is not None:
                fields[flag.replace("-", "_")] = value
        if kind_name == "parish" and args.publication:
            fields["publication"] = args.publication
        if not fields.get("name"):
            raise DioceseError("--name is required (or --from a roster entry)")
        body = Path(args.body_file).read_text(encoding="utf-8") if args.body_file else None
        result = records.new_record(args.diocese, kind_name, fields, slug=args.slug, body=body)
        result["next"] = (f"edit data/dioceses/{args.diocese}/{result['created']}: replace the "
                          "TODOs with the explanation and add evidence (see the README)")
        return result
    return run


# ── Handlers ────────────────────────────────────────────────────────────────
def _probe_sites(args: argparse.Namespace) -> dict[str, Any]:
    d = records.load(args.diocese)
    parishes = d.of(PARISH)
    urls = {slug: r.get("website", "") for slug, r in parishes.items() if r.get("website")}
    probes = dict(zip(urls, web.probe_urls(list(urls.values()))))
    found_by: dict[str, list[str]] = {}
    results = []
    for slug, probe in probes.items():
        recorded = set(parishes[slug].get("publication") or [])
        found = set(probe.get("publications") or [])
        for pub in found:
            found_by.setdefault(pub, []).append(slug)
        results.append({"parish": slug, **probe,
                        "recorded_not_on_site": sorted(recorded - found),
                        "on_site_not_recorded": sorted(found - recorded)})
    order = ["DEAD-DNS", "SPAM-SQUAT", "REDIRECT-OFFSITE", "UNREACHABLE", "HTTP5XX", "HTTP4XX",
             "NO-PARISH-WORDS", "ok"]
    results.sort(key=lambda r: order.index(r["verdict"]) if r["verdict"] in order else 0)
    if not args.all:
        results = [r for r in results if r["verdict"] != "ok" or r["on_site_not_recorded"]]
    summary: dict[str, int] = {}
    for probe in probes.values():
        summary[probe["verdict"]] = summary.get(probe["verdict"], 0) + 1
    return {
        "diocese": args.diocese, "summary": summary,
        "shared_on_sites": {p: s for p, s in found_by.items() if len(s) > 1},
        "results": results,
        "note": "a flag is a question, not an answer: re-probe DEAD-DNS, read REDIRECT-OFFSITE "
                "targets, and expect JS-rendered sites to show NO-PARISH-WORDS",
    }


def _recheck(args: argparse.Namespace) -> dict[str, Any]:
    d = records.load(args.diocese)
    kinds = [KINDS[k] for k in args.kind] if args.kind else list(KINDS.values())
    items = []
    for kind in kinds:
        for slug, r in d.of(kind).items():
            if args.slug and slug not in args.slug:
                continue
            for e in r.get("evidence") or []:
                if isinstance(e, dict):
                    items.append((f"{kind.dir}/{slug}", e))
    results = web.recheck_evidence(items)
    summary: dict[str, int] = {}
    for r in results:
        summary[r["result"]] = summary.get(r["result"], 0) + 1
    shown = results if args.all else [r for r in results if r["result"] not in ("found",
                                                                                   "no-quote")]
    return {"diocese": args.diocese, "summary": summary, "results": shown,
            "note": "a quote missing from a dated bulletin PDF is a real problem; missing from a "
                    "homepage it usually means the page changed, so look again"}


def _roster_show(args: argparse.Namespace) -> dict[str, Any]:
    roster, entry = rosters.get_entry(args.diocese, args.ref)
    return {"roster": {k: roster.get(k) for k in ("name", "title", "url", "fetched")},
            "entry": entry}


def _date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a date like 2026-09-06: {value!r}") from None


def _write_record(args: argparse.Namespace) -> dict[str, Any]:
    def invalid_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON value {value!r}")

    try:
        text = sys.stdin.read() if args.file == "-" else Path(args.file).read_text(encoding="utf-8")
        payload = json.loads(text, parse_constant=invalid_constant)
    except (OSError, ValueError) as exc:
        raise DioceseError(f"cannot read record JSON: {exc}") from None
    return records.write_record(args.diocese, args.kind, args.slug, payload, create=args.create)


HANDLERS: dict[str, Handler] = {
    "list": lambda a: records.list_dioceses(),
    "init": lambda a: records.init_diocese(a.diocese, name=a.name, state=a.state or "",
                                           website=a.website or "", gcatholic=a.gcatholic or ""),
    "show": lambda a: records.show_diocese(a.diocese),
    "todo": lambda a: report.todo(a.diocese),
    "validate": lambda a: records.validate(a.diocese),
    "write": _write_record,
    "search": lambda a: records.search(" ".join(a.query), diocese=a.diocese, kinds=a.kind,
                                       limit=a.limit),
    "merge": lambda a: records.merge_parishes(a.diocese, a.parishes, a.into, note=a.note or ""),
    "rename": lambda a: records.rename_record(a.diocese, a.kind, a.old, a.new),
    "exclude": lambda a: records.exclude_church(a.diocese, a.church, reason=a.reason,
                                                last_mass=a.last_mass or ""),
    "question": lambda a: records.question_church(a.diocese, a.church, revisit=a.revisit,
                                                  revisit_after=a.revisit_after or ""),
    "coverage": lambda a: report.coverage(a.diocese, a.roster, link=a.link,
                                          show_matched=a.show_matched),
    "audit": lambda a: report.audit(a.diocese, fetch=a.fetch),
    "roster-list": lambda a: rosters.list_rosters(a.diocese),
    "roster-fetch": lambda a: rosters.fetch_roster(a.diocese, a.source, a.target or "",
                                                   name=a.name or "", limit=a.limit),
    "roster-import": lambda a: rosters.import_roster(a.diocese, a.name, Path(a.file),
                                                     title=a.title or "", url=a.url or "",
                                                     notes=a.notes or ""),
    "roster-show": _roster_show,
    "probe-url": lambda a: {"results": web.probe_urls(a.urls)},
    "probe-sites": _probe_sites,
    "probe-container": lambda a: web.probe_container(
        a.container, weeks=a.weeks, start=a.start, step=a.step, all_issues=a.all,
        pages=a.pages, chars=a.chars),
    "probe-po": lambda a: {"results": [web.parishes_online_org(k, issues=a.issues)
                                       for k in a.keys]},
    "probe-pdf": lambda a: web.pdf_text(a.url, pages=a.pages, chars=a.chars, grep=a.grep or ()),
    "recheck": _recheck,
    "export": lambda a: records.export_csv(a.diocese, Path(a.out_dir)),
    "promote": lambda a: records.promote(a.diocese, dry_run=a.dry_run),
}


# ── Parser ──────────────────────────────────────────────────────────────────
def add_diocese_parser(
    subparsers: argparse._SubParsersAction,
    add_common_args: Callable[[argparse.ArgumentParser], None],
) -> None:
    """Register `diocese` and its subcommands on the top-level parser."""
    parser = subparsers.add_parser(
        "diocese",
        help="Explore new dioceses: record parishes, churches and exclusions in data/dioceses/",
        description="Work on data/dioceses/<diocese>/. See data/dioceses/README.md.",
    )
    parser.set_defaults(help_parser=parser)
    sub = parser.add_subparsers(dest="diocese_command", metavar="<command>")

    def leaf(name: str, key: str, help_text: str, parent=sub) -> argparse.ArgumentParser:
        p = parent.add_parser(name, help=help_text, description=help_text)
        p.set_defaults(handler=HANDLERS[key])
        add_common_args(p)
        return p

    def group(name: str, help_text: str) -> argparse._SubParsersAction:
        g = sub.add_parser(name, help=help_text, description=help_text)
        g.set_defaults(help_parser=g)
        return g.add_subparsers(dest=f"{name}_command", metavar="<command>")

    leaf("list", "list", "Dioceses being explored, with record counts")

    p = leaf("init", "init", "Create data/dioceses/<diocese>/")
    p.add_argument("diocese", help="folder slug, e.g. 'syracuse'")
    p.add_argument("--name", required=True, help="e.g. 'Roman Catholic Diocese of Syracuse'")
    p.add_argument("--state", help="two-letter state code")
    p.add_argument("--website", help="diocese homepage")
    p.add_argument("--gcatholic", help="GCatholic key, as in gcatholic.org/dioceses/diocese/<key>")

    p = leaf("show", "show", "Parishes with their churches, exclusions by reason, open questions")
    p.add_argument("diocese")

    p = leaf("todo", "todo", "What is left: errors, revisits due, coverage gaps, incomplete records")
    p.add_argument("diocese")

    p = leaf("validate", "validate", "Check one diocese (or all); exits 1 on errors")
    p.add_argument("diocese", nargs="?")
    p.set_defaults(fail_on_verification_error=True)

    p = leaf("write", "write", "Patch a record from JSON, validate, then atomically write it")
    p.add_argument("diocese")
    p.add_argument("kind", choices=list(KINDS))
    p.add_argument("slug")
    p.add_argument("--file", required=True, help="JSON fields plus optional body; '-' reads stdin")
    p.add_argument("--create", action="store_true", help="create a new record; refuse overwrites")

    p = leaf("search", "search",
             "Search every diocese and the live CSVs (diocese 'live'); run it before adding")
    p.add_argument("query", nargs="+", help="all words must match; St./Saint are treated alike")
    p.add_argument("--diocese", help="one diocese, or 'live' for data/*.csv")
    p.add_argument("--kind", action="append", choices=list(KINDS), help="repeatable")
    p.add_argument("--limit", type=int, default=50)

    new = group("new", "Create a record file, with an explanation template to fill in")
    for kind_name, flags in _NEW_FLAGS.items():
        kind = KINDS[kind_name]
        p = new.add_parser(kind_name, help=f"a new {kind.dir}/<slug>.md",
                           description=f"Create {kind.dir}/<slug>.md.")
        p.set_defaults(handler=_cmd_new(kind_name))
        add_common_args(p)
        p.add_argument("diocese")
        p.add_argument("--slug", help="file name; defaults to the name (and town, for places)")
        for flag, help_text in flags.items():
            p.add_argument(f"--{flag}", help=help_text or None, type=str)
        if kind_name == "parish":
            p.add_argument("--publication", action="append",
                           help="publication id, e.g. po-container:14/0434; repeatable")
        else:
            p.add_argument("--from", dest="from_", action="append", metavar="ROSTER:ID",
                           help="prefill from a roster entry (name, address, coordinates, "
                                "evidence) and link it; repeatable")
        p.add_argument("--body-file", help="use this file as the explanation instead of the "
                                           "template")

    p = leaf("merge", "merge",
             "Fold parish rows that share one bulletin into one; their churches move with them")
    p.add_argument("diocese")
    p.add_argument("parishes", nargs="+", help="parish slugs to fold in")
    p.add_argument("--into", required=True, help="the parish row that remains")
    p.add_argument("--note", help="why, with the evidence; added above the merged explanations")

    p = leaf("rename", "rename", "Change a record's slug and every reference to it")
    p.add_argument("diocese")
    p.add_argument("kind", choices=list(KINDS))
    p.add_argument("old")
    p.add_argument("new")

    p = leaf("exclude", "exclude", "Turn a church into an exclusion (it closed, or is not one)")
    p.add_argument("diocese")
    p.add_argument("church", help="church slug")
    p.add_argument("--reason", required=True, choices=list(EXCLUSION_REASONS))
    p.add_argument("--last-mass", help="date of the last Mass, if known")

    p = leaf("question", "question",
             "Turn a church into an open question (no current Mass found, not known closed)")
    p.add_argument("diocese")
    p.add_argument("church", help="church slug")
    p.add_argument("--revisit", required=True, help="the next thing to check")
    p.add_argument("--revisit-after", help="date to check it on")

    roster = group("roster", "Outside lists to measure the diocese against (rosters/*.json)")
    p = leaf("list", "roster-list", "Rosters of a diocese", roster)
    p.add_argument("diocese")
    p = leaf("fetch", "roster-fetch", "Fetch a roster: gcatholic <key> or wpsl <finder URL>",
             roster)
    p.add_argument("diocese")
    p.add_argument("source", choices=list(rosters.FETCHERS))
    p.add_argument("target", nargs="?", help="GCatholic key (default: diocese.md gcatholic) or "
                                             "the parish-finder page URL")
    p.add_argument("--name", help="roster name (default: the source)")
    p.add_argument("--limit", type=int, help="gcatholic: only the first N churches (a test)")
    p = leaf("import", "roster-import",
             "Save a list you built (JSON list or CSV) as a roster, e.g. a family list or "
             "Mass-times page", roster)
    p.add_argument("diocese")
    p.add_argument("name", help="roster name, e.g. 'families' or 'mass-times'")
    p.add_argument("file")
    p.add_argument("--title")
    p.add_argument("--url", help="where the list came from")
    p.add_argument("--notes", help="how it was built, and how far to trust it")
    p = leaf("show", "roster-show", "One roster entry in full", roster)
    p.add_argument("diocese")
    p.add_argument("ref", help="<roster>:<id>")

    p = leaf("coverage", "coverage",
             "Account for every roster entry: church, excluded, open, or unmatched")
    p.add_argument("diocese")
    p.add_argument("--roster", help="one roster (default: all)")
    p.add_argument("--link", action="store_true",
                   help="save unambiguous automatic matches on their records")
    p.add_argument("--show-matched", action="store_true", help="list the automatic matches too")

    p = leaf("audit", "audit", "Parish rows the diocese groups together: one bulletin or several?")
    p.add_argument("diocese")
    p.add_argument("--fetch", action="store_true",
                   help="also read each undecided row's website for the publication ids it embeds")

    probe = group("probe", "Look things up on the web (nothing is written)")
    p = leaf("url", "probe-url",
             "Is a website alive, whose is it now, which bulletin does it embed?", probe)
    p.add_argument("urls", nargs="+")
    p = leaf("sites", "probe-sites", "probe url over every parish website of a diocese", probe)
    p.add_argument("diocese")
    p.add_argument("--all", action="store_true", help="include sites with nothing to report")
    p = leaf("container", "probe-container",
             "Walk back through a ParishesOnline bulletin container (e.g. 14/0434)", probe)
    p.add_argument("container")
    p.add_argument("--weeks", type=int, default=12, help="Sundays to look back over")
    p.add_argument("--from", dest="start", type=_date, help="start from this date, not today")
    p.add_argument("--step", type=int, default=1, help="probe every n-th Sunday (4 = monthly)")
    p.add_argument("--all", action="store_true", help="every issue in range, not just the latest")
    p.add_argument("--pages", type=int, default=0,
                   help="include the text of the first N readable pages of each issue found")
    p.add_argument("--chars", type=int, default=2500)
    p = leaf("po", "probe-po",
             "A ParishesOnline organization (org slug or LPi widget id): its address, "
             "publication ids and latest bulletins", probe)
    p.add_argument("keys", nargs="+", help="org slug, LPi publicationWidget id, or org URL")
    p.add_argument("--issues", type=int, default=6, help="how many recent issues to list")
    p = leaf("pdf", "probe-pdf", "Text of a bulletin PDF, and where given words occur", probe)
    p.add_argument("url")
    p.add_argument("--pages", type=int, default=3, help="readable pages to include")
    p.add_argument("--chars", type=int, default=3000, help="characters per page")
    p.add_argument("--grep", action="append", help="count and quote lines with this; repeatable")

    p = leaf("recheck", "recheck", "Check that the quotes recorded as evidence are still there")
    p.add_argument("diocese")
    p.add_argument("slug", nargs="*", help="only these records")
    p.add_argument("--kind", action="append", choices=list(KINDS))
    p.add_argument("--all", action="store_true", help="list the quotes that were found too")

    p = leaf("export", "export", "Write parishes.csv and churches.csv in the live layout")
    p.add_argument("diocese")
    p.add_argument("--out-dir", required=True)

    p = leaf("promote", "promote",
             "Apply the diocese to data/parishes.csv and data/churches.csv")
    p.add_argument("diocese")
    p.add_argument("--dry-run", action="store_true", help="report the changes, write nothing")
