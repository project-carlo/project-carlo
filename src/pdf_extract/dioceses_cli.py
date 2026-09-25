"""`python -m pdf_extract diocese ...`: the command-line face of `pdf_extract.dioceses`.

Kept apart from `__main__` because the group is large: four record kinds, each
with list/get/add/edit/remove and its own field flags. Every handler returns
the JSON-serialisable dict that `__main__.main` prints.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract import dioceses
from pdf_extract.dioceses import KINDS

# Flags for each kind's fields: flag name -> field name. `--slug` and
# `--source` are shared and handled separately.
_FIELD_FLAGS: dict[str, dict[str, str]] = {
    "parish": {
        "name": "name",
        "website": "website",
        "bulletin-provider": "bulletin_provider",
        "provider-id": "provider_id",
        "explanation": "explanation",
    },
    "church": {
        "parish": "parish_id",
        "name": "name",
        "line1": "line1",
        "line2": "line2",
        "city": "city",
        "state": "state",
        "postal-code": "postal_code",
        "latitude": "latitude",
        "longitude": "longitude",
        "name-verified": "name_verified",
        "address-verified": "address_verified",
        "explanation": "explanation",
    },
    "not-parish": {
        "name": "name",
        "website": "website",
        "address": "address",
        "parish": "parish",
        "explanation": "explanation",
    },
}
_FIELD_FLAGS["not-church"] = _FIELD_FLAGS["not-parish"]

_FLAG_HELP = {
    "bulletin-provider": f"one of: {', '.join(sorted(dioceses.KNOWN_BULLETIN_PROVIDERS))}",
    "provider-id": "account id for parishes_online / discover_mass",
    "parish": "slug of the parish it belongs to (for not-* entries: the related parish, if any)",
    "name-verified": "true or false",
    "address-verified": "true or false",
    "explanation": "why this record is right (or, for not-* entries, why it is excluded)",
    "latitude": "decimal degrees; pass '' to clear",
    "longitude": "decimal degrees; pass '' to clear",
}

_KIND_HELP = {
    "parish": "parishes.json: parishes to add to the pipeline",
    "church": "churches.json: worship sites of those parishes",
    "not-parish": "not-parishes.md: places that looked like parishes but are not",
    "not-church": "not-churches.md: places that looked like churches but are not",
}


def _fields(kind: str, args: argparse.Namespace) -> dict[str, Any]:
    return {field: getattr(args, flag.replace("-", "_")) for flag, field in _FIELD_FLAGS[kind].items()}


# ── Handlers ────────────────────────────────────────────────────────────────
def _cmd_list(_args: argparse.Namespace) -> dict[str, Any]:
    return dioceses.list_dioceses()


def _cmd_init(args: argparse.Namespace) -> dict[str, Any]:
    return dioceses.init_diocese(
        args.diocese, name=args.name, state=args.state or "", website=args.website or "",
        parish_directory_url=args.directory_url or "", notes=args.notes or "",
    )


def _cmd_edit_meta(args: argparse.Namespace) -> dict[str, Any]:
    return dioceses.edit_diocese(args.diocese, {
        "name": args.name, "state": args.state, "website": args.website,
        "parish_directory_url": args.directory_url, "notes": args.notes,
    })


def _cmd_show(args: argparse.Namespace) -> dict[str, Any]:
    return dioceses.show_diocese(args.diocese)


def _cmd_search(args: argparse.Namespace) -> dict[str, Any]:
    return dioceses.search(
        " ".join(args.query), diocese=args.diocese, kinds=args.kind, limit=args.limit,
    )


def _cmd_validate(args: argparse.Namespace) -> dict[str, Any]:
    return dioceses.validate(args.diocese)


def _cmd_export(args: argparse.Namespace) -> dict[str, Any]:
    return dioceses.export_csv(args.diocese, Path(args.out_dir))


def _record_handlers(kind: str) -> dict[str, Callable[[argparse.Namespace], dict[str, Any]]]:
    def list_(args):
        return dioceses.list_records(args.diocese, kind, parish=args.parish)

    def get(args):
        return dioceses.get_record(args.diocese, kind, args.slug)

    def add(args):
        return dioceses.add_record(
            args.diocese, kind, {**_fields(kind, args), "slug": args.slug, "sources": args.source},
        )

    def edit(args):
        return dioceses.edit_record(
            args.diocese, kind, args.slug, _fields(kind, args),
            new_slug=args.new_slug, append_explanation=args.append_explanation,
            add_sources=args.source or (), clear_sources=args.clear_sources,
        )

    def remove(args):
        return dioceses.remove_record(
            args.diocese, kind, args.slug, cascade=getattr(args, "cascade", False),
        )

    return {"list": list_, "get": get, "add": add, "edit": edit, "remove": remove}


# ── Parser ──────────────────────────────────────────────────────────────────
def add_diocese_parser(
    subparsers: argparse._SubParsersAction,
    add_common_args: Callable[[argparse.ArgumentParser], None],
) -> None:
    """Register `diocese` and its subcommands on the top-level parser."""
    parser = subparsers.add_parser(
        "diocese",
        help="Explore new dioceses: record parishes, churches and exclusions in data/dioceses/",
        description=(
            "Manage data/dioceses/<diocese>/. Writes are checked and refused if they would add "
            "a validation error. See data/dioceses/README.md."
        ),
    )
    parser.set_defaults(help_parser=parser)
    sub = parser.add_subparsers(dest="diocese_command")

    def leaf(name: str, handler, help_text: str, parent=sub) -> argparse.ArgumentParser:
        p = parent.add_parser(name, help=help_text, description=help_text)
        p.set_defaults(handler=handler)
        add_common_args(p)
        return p

    leaf("list", _cmd_list, "List dioceses with record counts")

    def meta_flags(p: argparse.ArgumentParser, *, required_name: bool) -> None:
        p.add_argument("--name", required=required_name, help="e.g. 'Roman Catholic Diocese of Syracuse'")
        p.add_argument("--state", help="two-letter state code")
        p.add_argument("--website", help="diocese homepage")
        p.add_argument("--directory-url", help="where the diocese lists its parishes")
        p.add_argument("--notes", help="exploration notes: coverage so far, quirks, next steps")

    p = leaf("init", _cmd_init, "Create data/dioceses/<diocese>/ with empty files")
    p.add_argument("diocese", help="slug for the folder, e.g. 'syracuse'")
    meta_flags(p, required_name=True)

    p = leaf("edit", _cmd_edit_meta, "Change diocese.json fields")
    p.add_argument("diocese")
    meta_flags(p, required_name=False)

    p = leaf("show", _cmd_show, "Overview: parishes with their churches, and exclusions")
    p.add_argument("diocese")

    p = leaf(
        "search", _cmd_search,
        "Search every diocese and the live CSVs (diocese 'live'); use before adding anything",
    )
    p.add_argument("query", nargs="+", help="all words must match; St./Saint are treated alike")
    p.add_argument("--diocese", help="limit to one diocese, or 'live' for data/*.csv")
    p.add_argument("--kind", action="append", choices=list(KINDS), help="repeatable")
    p.add_argument("--limit", type=int, default=50)

    p = leaf("validate", _cmd_validate, "Check one diocese (or all); exits 1 on errors")
    p.add_argument("diocese", nargs="?")
    p.set_defaults(fail_on_verification_error=True)

    p = leaf("export", _cmd_export, "Write parishes.csv and churches.csv in the live data/ format")
    p.add_argument("diocese")
    p.add_argument("--out-dir", required=True, help="directory to write the two CSVs into")

    for kind in KINDS:
        group = sub.add_parser(kind, help=_KIND_HELP[kind], description=_KIND_HELP[kind])
        group.set_defaults(help_parser=group)
        actions = group.add_subparsers(dest=f"{kind}_command")
        handlers = _record_handlers(kind)

        p = leaf("list", handlers["list"], f"List every {kind}", actions)
        p.add_argument("diocese")
        p.add_argument("--parish", help="only records belonging to this parish slug")

        p = leaf("get", handlers["get"], f"Show one {kind} in full", actions)
        p.add_argument("diocese")
        p.add_argument("slug")

        p = leaf("add", handlers["add"], f"Add a {kind}", actions)
        p.add_argument("diocese")
        p.add_argument("--slug", help="defaults to the name, slugified")
        _add_field_flags(p, kind)

        p = leaf("edit", handlers["edit"], f"Change fields of a {kind}; omitted flags stay", actions)
        p.add_argument("diocese")
        p.add_argument("slug")
        p.add_argument("--new-slug", help="rename (a parish's churches follow it)")
        p.add_argument("--append-explanation", help="add a paragraph to the explanation")
        p.add_argument("--clear-sources", action="store_true", help="drop sources before adding --source")
        _add_field_flags(p, kind)

        p = leaf("remove", handlers["remove"], f"Remove a {kind}", actions)
        p.add_argument("diocese")
        p.add_argument("slug")
        if kind == "parish":
            p.add_argument("--cascade", action="store_true", help="also remove its churches")


def _add_field_flags(p: argparse.ArgumentParser, kind: str) -> None:
    for flag in _FIELD_FLAGS[kind]:
        p.add_argument(f"--{flag}", help=_FLAG_HELP.get(flag))
    p.add_argument("--source", action="append", help="URL backing this record; repeatable")
