"""CLI entry point for pdf_extract.

Each subparser carries its own handler (`set_defaults(handler=...)`), so a
command's arguments and the call they feed sit next to each other and `main`
stays a dispatcher. Handlers return the JSON-serialisable result dict that gets
printed; returning None means "no subcommand given", which prints help and
exits non-zero.

Imports are eager on purpose: `pdf_extract/__init__.py` re-exports the pipeline
stages, so importing anything from this package already pulls in playwright,
google-genai and openai. Deferring them inside the handlers would defer nothing.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from pdf_extract.apply import (
    apply_detect_results,
    apply_geocode_results,
    apply_verify_results,
)
from pdf_extract.classifiers import available_classifiers
from pdf_extract.compare import compare
from pdf_extract.db import create_db
from pdf_extract.detect import run_detection
from pdf_extract.dioceses import DioceseError
from pdf_extract.dioceses_cli import add_diocese_parser
from pdf_extract.extract_frontend_db import extract as extract_frontend_db
from pdf_extract.extract_run import run as run_extract
from pdf_extract.fetch import fetch_bulletins
from pdf_extract.geocode import run_backfill
from pdf_extract.process import process_bulletins
from pdf_extract.recurrence import apply_recurrence, backfill_history_from_git
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL
from pdf_extract.storage import DEFAULT_DB_PATH, delete_db
from pdf_extract.verify import verify_churches
from pdf_extract.verify_frontend_snapshot import verify_frontend_snapshot

LOGGER = logging.getLogger(__name__)

Result = dict[str, Any]


def _configure_logging(level_name: str) -> None:
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def _add_common_args(parser: argparse.ArgumentParser, default_level: str = "INFO") -> None:
    parser.add_argument(
        "--log-level",
        default=default_level,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help=f"Logging verbosity (default: {default_level})",
    )


def _ensure_db() -> None:
    """Rebuild the DB from data files before running a pipeline command."""
    create_db(DEFAULT_DB_PATH)


# ── Command handlers ────────────────────────────────────────────────────────
def _cmd_fetch(args: argparse.Namespace) -> Result:
    _ensure_db()
    return fetch_bulletins(parish_name=args.parish)


def _cmd_process(args: argparse.Namespace) -> Result:
    _ensure_db()
    return process_bulletins(
        parish_name=args.parish, model=args.model, concurrency=args.concurrency,
    )


def _cmd_extract(args: argparse.Namespace) -> Result:
    _ensure_db()
    return run_extract(
        classifier_name=args.classifier,
        parish_name=args.parish,
        concurrency=args.concurrency,
    )


def _cmd_compare(args: argparse.Namespace) -> Result:
    return compare(args.classifiers, out_path=Path(args.out) if args.out else None)


def _cmd_detect_run(args: argparse.Namespace) -> Result:
    _ensure_db()
    return run_detection(
        db_path=DEFAULT_DB_PATH,
        dry_run=args.dry_run,
        limit=args.limit,
        pause_seconds=args.pause_seconds,
    )


def _cmd_detect_apply(_args: argparse.Namespace) -> Result:
    return apply_detect_results()


def _cmd_verify_run(args: argparse.Namespace) -> Result:
    _ensure_db()
    return verify_churches(parish_name=args.parish, model=args.model)


def _cmd_verify_apply(_args: argparse.Namespace) -> Result:
    return apply_verify_results()


def _cmd_geocode_run(args: argparse.Namespace) -> Result:
    _ensure_db()
    return run_backfill(
        dry_run=args.dry_run,
        limit=args.limit,
        pause_seconds=args.pause_seconds,
        email=args.email,
    )


def _cmd_geocode_apply(_args: argparse.Namespace) -> Result:
    return apply_geocode_results()


def _cmd_recurrence_apply(_args: argparse.Namespace) -> Result:
    return apply_recurrence()


def _cmd_recurrence_backfill(args: argparse.Namespace) -> Result:
    return backfill_history_from_git(limit=args.limit)


def _cmd_db_create(_args: argparse.Namespace) -> Result:
    return create_db(DEFAULT_DB_PATH)


def _cmd_db_drop(_args: argparse.Namespace) -> Result:
    return {"deleted": delete_db(DEFAULT_DB_PATH), "db_path": str(DEFAULT_DB_PATH)}


def _cmd_extract_frontend_db(_args: argparse.Namespace) -> Result:
    _ensure_db()
    return extract_frontend_db()


def _cmd_verify_frontend_snapshot(_args: argparse.Namespace) -> Result:
    return verify_frontend_snapshot()


# ── Parser ──────────────────────────────────────────────────────────────────
def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m pdf_extract",
        description="Fetch bulletin PDFs, process events, and manage parish data.",
    )
    subparsers = parser.add_subparsers(dest="command")

    # -- fetch --
    fetch_parser = subparsers.add_parser("fetch", help="Fetch latest PDFs and save to disk")
    fetch_parser.add_argument("--parish", help="Parish name (omit to run for all)")
    fetch_parser.set_defaults(handler=_cmd_fetch)
    _add_common_args(fetch_parser)

    # -- process --
    process_parser = subparsers.add_parser("process", help="Process fetched PDFs with Gemini")
    process_parser.add_argument("--parish", help="Parish name (omit to run for all)")
    process_parser.add_argument(
        "--model", default=DEFAULT_GEMINI_MODEL,
        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})",
    )
    process_parser.add_argument(
        "--concurrency", type=int, default=5,
        help="Number of parallel Gemini calls (default: 5)",
    )
    process_parser.set_defaults(handler=_cmd_process)
    _add_common_args(process_parser)

    # -- extract (experimental: run a registered classifier into data/runs/) --
    extract_parser = subparsers.add_parser(
        "extract",
        help="Run an experimental classifier and write to data/runs/<name>/",
    )
    extract_parser.add_argument(
        "--classifier", required=True, choices=available_classifiers(),
        help="Name of the registered classifier",
    )
    extract_parser.add_argument("--parish", help="Parish name (omit to run for all)")
    extract_parser.add_argument(
        "--concurrency", type=int, default=5,
        help="Number of parallel classifier calls (default: 5)",
    )
    extract_parser.set_defaults(handler=_cmd_extract)
    _add_common_args(extract_parser)

    # -- compare (experimental: pairwise metrics over previous extract runs) --
    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare two or more classifier runs from data/runs/",
    )
    compare_parser.add_argument(
        "classifiers", nargs="+",
        help="Two or more classifier names to compare (must each have a run dir)",
    )
    compare_parser.add_argument(
        "--out", type=str, default=None,
        help="Optional path for the JSON report (default: data/runs/compare/compare_<ts>.json)",
    )
    compare_parser.set_defaults(handler=_cmd_compare)
    _add_common_args(compare_parser)

    # -- detect --
    detect_parser = subparsers.add_parser("detect", help="Detect bulletin provider for parish websites")
    detect_parser.set_defaults(help_parser=detect_parser)
    detect_subparsers = detect_parser.add_subparsers(dest="detect_command")

    detect_run_parser = detect_subparsers.add_parser("run", help="Run provider detection")
    detect_run_parser.add_argument("--dry-run", action="store_true")
    detect_run_parser.add_argument("--limit", type=int, default=None)
    detect_run_parser.add_argument("--pause-seconds", type=float, default=0.5)
    detect_run_parser.set_defaults(handler=_cmd_detect_run)
    _add_common_args(detect_run_parser)

    detect_apply_parser = detect_subparsers.add_parser("apply", help="Write detect results into parishes.csv")
    detect_apply_parser.set_defaults(handler=_cmd_detect_apply)
    _add_common_args(detect_apply_parser)

    # -- verify --
    verify_parser = subparsers.add_parser("verify", help="Verify church data against latest bulletin")
    verify_parser.set_defaults(help_parser=verify_parser)
    verify_subparsers = verify_parser.add_subparsers(dest="verify_command")

    verify_run_parser = verify_subparsers.add_parser("run", help="Run church verification")
    verify_run_parser.add_argument("--parish", help="Parish name (omit for all)")
    verify_run_parser.add_argument(
        "--model", default=DEFAULT_GEMINI_MODEL,
        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})",
    )
    verify_run_parser.set_defaults(handler=_cmd_verify_run)
    _add_common_args(verify_run_parser)

    verify_apply_parser = verify_subparsers.add_parser("apply", help="Write verify results into churches.csv")
    verify_apply_parser.set_defaults(handler=_cmd_verify_apply)
    _add_common_args(verify_apply_parser)

    # -- geocode --
    geocode_parser = subparsers.add_parser("geocode", help="Backfill church lat/lng from address")
    geocode_parser.set_defaults(help_parser=geocode_parser)
    geocode_subparsers = geocode_parser.add_subparsers(dest="geocode_command")

    geocode_run_parser = geocode_subparsers.add_parser("run", help="Run geocoding via Nominatim")
    geocode_run_parser.add_argument("--dry-run", action="store_true")
    geocode_run_parser.add_argument("--limit", type=int, default=None)
    geocode_run_parser.add_argument("--pause-seconds", type=float, default=1.0)
    geocode_run_parser.add_argument("--email", type=str, default=None, help="Email for Nominatim usage policy")
    geocode_run_parser.set_defaults(handler=_cmd_geocode_run)
    _add_common_args(geocode_run_parser)

    geocode_apply_parser = geocode_subparsers.add_parser("apply", help="Write geocode results into churches.csv")
    geocode_apply_parser.set_defaults(handler=_cmd_geocode_apply)
    _add_common_args(geocode_apply_parser)

    # -- recurrence --
    recurrence_parser = subparsers.add_parser(
        "recurrence",
        help="Detect dated events that repeat weekly and promote them",
    )
    recurrence_parser.set_defaults(help_parser=recurrence_parser)
    recurrence_subparsers = recurrence_parser.add_subparsers(dest="recurrence_command")

    recurrence_apply_parser = recurrence_subparsers.add_parser(
        "apply",
        help="Re-run weekly promotion over data/events.json using the recorded history",
    )
    recurrence_apply_parser.set_defaults(handler=_cmd_recurrence_apply)
    _add_common_args(recurrence_apply_parser)

    recurrence_backfill_parser = recurrence_subparsers.add_parser(
        "backfill",
        help="Seed data/event_history.json from past committed revisions of data/events.json",
    )
    recurrence_backfill_parser.add_argument(
        "--limit", type=int, default=None,
        help="Only scan the N most recent revisions (default: all)",
    )
    recurrence_backfill_parser.set_defaults(handler=_cmd_recurrence_backfill)
    _add_common_args(recurrence_backfill_parser)

    # -- diocese (exploring new dioceses; quiet by default, the JSON is the output) --
    add_diocese_parser(
        subparsers, lambda p: _add_common_args(p, default_level="WARNING"),
    )

    # -- db --
    db_parser = subparsers.add_parser("db", help="Database management commands")
    db_parser.set_defaults(help_parser=db_parser)
    db_subparsers = db_parser.add_subparsers(dest="db_command")

    db_create_parser = db_subparsers.add_parser("create", help="Drop and recreate DB from schema + data files")
    db_create_parser.set_defaults(handler=_cmd_db_create)
    _add_common_args(db_create_parser)

    db_drop_parser = db_subparsers.add_parser("drop", help="Delete the SQLite DB file")
    db_drop_parser.set_defaults(handler=_cmd_db_drop)
    _add_common_args(db_drop_parser)

    # -- extract frontend db --
    extract_frontend_db_parser = subparsers.add_parser(
        "extract-frontend-db",
        help="Rebuild the DB and write apps/web/public/frontend.snapshot",
    )
    extract_frontend_db_parser.set_defaults(handler=_cmd_extract_frontend_db)
    _add_common_args(extract_frontend_db_parser)

    # -- verify frontend snapshot --
    verify_frontend_snapshot_parser = subparsers.add_parser(
        "verify-frontend-snapshot",
        help="Verify frontend snapshot similarity against frontend.snapshot.previous",
    )
    verify_frontend_snapshot_parser.set_defaults(
        handler=_cmd_verify_frontend_snapshot, fail_on_verification_error=True,
    )
    _add_common_args(verify_frontend_snapshot_parser)

    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = _build_parser()
    args = parser.parse_args(argv)

    # No command, or a command group invoked without its subcommand: only leaf
    # parsers set a handler, so there is nothing to run. `help_parser` is the
    # group's own parser, so `detect` alone prints the detect help.
    handler = getattr(args, "handler", None)
    if handler is None:
        getattr(args, "help_parser", parser).print_help()
        return 1

    _configure_logging(args.log_level)

    try:
        result = handler(args)
    except DioceseError as e:
        # Bad input, not a crash: the message says what to fix, a traceback would bury it.
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        LOGGER.exception("Command failed")
        print(f"Error: {e}", file=sys.stderr)
        return 1

    LOGGER.info("Command completed: %s", result)
    print(json.dumps(result, indent=2))
    if getattr(args, "fail_on_verification_error", False) and not result.get("passed", False):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
