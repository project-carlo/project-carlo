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
import os
import sys
from pathlib import Path
from typing import Any

from pdf_extract.apply import (
    apply_detect_results,
    apply_geocode_results,
    apply_verify_results,
)
from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, remote_from_env, set_store
from pdf_extract.classifiers import ClassifierOptionError, available_classifiers
from pdf_extract.classifiers.openai_responses import IMAGE_DETAILS, REASONING_EFFORTS
from pdf_extract.compare import compare
from pdf_extract.datasync import (
    DEFAULT_KEEP_MONTHLY,
    DEFAULT_KEEP_RECENT,
    build_deploy_snapshot,
    promote,
    pull,
    push_candidate,
)
from pdf_extract.datasync import prune as data_prune
from pdf_extract.datasync import status as data_status
from pdf_extract.db import create_db, ensure_db
from pdf_extract.detect import run_detection
from pdf_extract.dioceses import DioceseError
from pdf_extract.dioceses.cli import add_diocese_parser
from pdf_extract.evals.report import write_report as write_eval_report
from pdf_extract.evals.run import DEFAULT_STATUSES as EVAL_DEFAULT_STATUSES
from pdf_extract.evals.run import run as run_eval
from pdf_extract.extract_frontend_db import extract as extract_frontend_db
from pdf_extract.extract_run import run as run_extract
from pdf_extract.fetch import fetch_bulletins
from pdf_extract.fetch_check import check_fetch
from pdf_extract.geocode import run_backfill
from pdf_extract.labeling.demo import build_demo
from pdf_extract.labeling.labels import LABELS_DIR
from pdf_extract.labeling.server import DEFAULT_PORT as LABELER_PORT
from pdf_extract.labeling.server import LabelerApp
from pdf_extract.labeling.server import serve as serve_labeler
from pdf_extract.paths import DATA_DIR
from pdf_extract.process import process_bulletins
from pdf_extract.recurrence import apply_recurrence
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db, delete_db, utc_now_iso
from pdf_extract.verify import verify_churches
from pdf_extract.verify_frontend_snapshot import verify_frontend_snapshot
from pdf_extract.weekly import RunScopeError, run_weekly

LOGGER = logging.getLogger(__name__)

Result = dict[str, Any]

# Exit code of `weekly` when the run finished but a publishing check failed.
EXIT_HELD = 10

# `label serve --demo` builds its generated dataset here (gitignored).
DEMO_DIR = DATA_DIR / "labeler-demo"


def _configure_logging(level_name: str) -> None:
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def _load_dotenv(path: Path = Path(".env")) -> None:
    """Read KEY=VALUE lines from .env into the environment, without overriding.

    So GEMINI_API_KEY and the R2_* credentials can live in one local file for
    every command, however it is launched.
    """
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(key, value)


def _add_common_args(parser: argparse.ArgumentParser, default_level: str = "INFO") -> None:
    parser.add_argument(
        "--log-level",
        default=default_level,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help=f"Logging verbosity (default: {default_level})",
    )


def _add_eval_model_args(parser: argparse.ArgumentParser) -> None:
    """Model settings for `eval run`; `eval report` takes the same ones to find that run."""
    parser.add_argument(
        "--model",
        help=(
            "Model to run in place of the classifier's own, from the same provider: "
            "e.g. gpt-6.1-sol for gpt-6-luna (output under data/runs/<model>/), or a "
            "Gemini model for gemini-flash-qualified (under data/runs/<model>-qualified/)"
        ),
    )
    parser.add_argument(
        "--reasoning", choices=REASONING_EFFORTS,
        help="Reasoning effort (default: the classifier's, medium for gpt-6-luna)",
    )
    parser.add_argument(
        "--image-detail", choices=IMAGE_DETAILS,
        help=(
            "Detail level the bulletin is read at (default: the classifier's, low for "
            "gpt-6-luna). `original` needs --pdf-as-images"
        ),
    )
    parser.add_argument(
        "--pdf-as-images", action="store_true",
        help="Render every PDF page to an image and send those instead of the PDF",
    )


def _ensure_db() -> None:
    """Migrate the DB and re-seed parishes/churches from the CSVs before a command."""
    ensure_db(DEFAULT_DB_PATH)


# ── Command handlers ────────────────────────────────────────────────────────
def _cmd_fetch(args: argparse.Namespace) -> Result:
    _ensure_db()
    return fetch_bulletins(parish_name=args.parish)


def _cmd_fetch_check(args: argparse.Namespace) -> Result:
    return check_fetch(
        slugs=_split_csv(args.parish),
        providers=_split_csv(args.provider),
        record_dir=args.record,
        download=not args.no_download,
    )


def _split_csv(values: list[str] | None) -> set[str] | None:
    if not values:
        return None
    return {v.strip() for value in values for v in value.split(",") if v.strip()}


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


def _eval_classifier_options(args: argparse.Namespace) -> dict[str, Any]:
    """The model settings given on the command line; unset ones keep the classifier's default."""
    return {
        "model": args.model,
        "reasoning_effort": args.reasoning,
        "file_detail": args.image_detail,
        "pdf_as_images": True if args.pdf_as_images else None,
    }


def _cmd_eval_run(args: argparse.Namespace) -> Result:
    _ensure_db()
    return run_eval(
        classifier_name=args.classifier,
        statuses=args.status or EVAL_DEFAULT_STATUSES,
        parish_slug=args.parish,
        limit=args.limit,
        concurrency=args.concurrency,
        refresh=args.refresh,
        classifier_options=_eval_classifier_options(args),
    )


def _cmd_eval_report(args: argparse.Namespace) -> Result:
    return write_eval_report(
        classifier_name=args.classifier,
        version=args.version,
        classifier_options=_eval_classifier_options(args),
        statuses=args.status or EVAL_DEFAULT_STATUSES,
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
    _ensure_db()
    conn = connect_db()
    try:
        return apply_recurrence(conn)
    finally:
        conn.close()


def _cmd_weekly(args: argparse.Namespace) -> Result:
    run_id = args.run_id or "local-" + utc_now_iso().replace(":", "").replace("-", "")
    return run_weekly(
        run_id=run_id,
        model=args.model,
        concurrency=args.concurrency,
        git_sha=args.git_sha,
        trigger=args.trigger,
        parishes=args.parish,
        dioceses=args.diocese,
    )


def _cmd_data_pull(args: argparse.Namespace) -> Result:
    return pull(
        run_id=args.run_id,
        db=not args.snapshot_only,
        snapshot=not args.no_snapshot,
        public_fallback=args.public_fallback,
    )


def _cmd_data_snapshot(_args: argparse.Namespace) -> Result:
    return build_deploy_snapshot()


def _cmd_data_push(args: argparse.Namespace) -> Result:
    return push_candidate(args.run_id, git_sha=args.git_sha)


def _cmd_data_promote(args: argparse.Namespace) -> Result:
    return promote(args.run_id, rollback=args.rollback)


def _cmd_data_status(args: argparse.Namespace) -> Result:
    return data_status(limit=args.limit)


def _cmd_data_prune(args: argparse.Namespace) -> Result:
    return data_prune(
        keep_recent=args.keep_recent, keep_monthly=args.keep_monthly, apply=args.apply,
    )


def _cmd_db_create(args: argparse.Namespace) -> Result:
    if DEFAULT_DB_PATH.exists() and not args.force:
        raise FileExistsError(
            f"{DEFAULT_DB_PATH} exists and holds pipeline data; pass --force to replace "
            "it with an empty database (or `pnpm data:pull` to reset to the published data)"
        )
    return create_db(DEFAULT_DB_PATH)


def _cmd_db_drop(_args: argparse.Namespace) -> Result:
    return {"deleted": delete_db(DEFAULT_DB_PATH), "db_path": str(DEFAULT_DB_PATH)}


def _cmd_label_serve(args: argparse.Namespace) -> Result:
    # Built here rather than with get_store(): the labeler only ever reads from
    # R2, whatever CARLO_REMOTE_WRITE says.
    if args.demo:
        paths = build_demo(Path(args.demo_dir))
        set_store(CachedBlobStore(LocalBlobStore(paths["root"])))
        app = LabelerApp(db_path=paths["db_path"], labels_dir=paths["labels_dir"], mode="demo")
    else:
        _ensure_db()
        set_store(CachedBlobStore(LocalBlobStore(DATA_DIR), remote_from_env(), remote_write=False))
        app = LabelerApp(db_path=DEFAULT_DB_PATH, labels_dir=LABELS_DIR)
    return serve_labeler(app, port=args.port)


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

    # -- fetch-check --
    fetch_check_parser = subparsers.add_parser(
        "fetch-check",
        help="Resolve and download each parish's latest bulletin without saving it",
    )
    fetch_check_parser.add_argument(
        "--parish", action="append", help="Only these slugs (repeat, or comma-separate)",
    )
    fetch_check_parser.add_argument(
        "--provider", action="append",
        help="Only parishes with these bulletin providers (e.g. other)",
    )
    fetch_check_parser.add_argument(
        "--record", type=Path, default=None,
        help="Save the pages each resolver read here, for tests/test_fetch_replay.py",
    )
    fetch_check_parser.add_argument(
        "--no-download", action="store_true", help="Resolve links only; skip the PDF download",
    )
    fetch_check_parser.set_defaults(handler=_cmd_fetch_check)
    _add_common_args(fetch_check_parser)

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

    # -- eval (run a classifier over the ground-truth labeled bulletins) --
    eval_parser = subparsers.add_parser(
        "eval", help="Run classifiers over the labeled bulletins in data/labels/",
    )
    eval_parser.set_defaults(help_parser=eval_parser)
    eval_subparsers = eval_parser.add_subparsers(dest="eval_command")

    eval_run_parser = eval_subparsers.add_parser(
        "run",
        help="Classify the labeled bulletins; writes data/runs/<classifier>/eval/<version>/",
    )
    eval_run_parser.add_argument(
        "--classifier", required=True, choices=available_classifiers(),
        help="Name of the registered classifier",
    )
    eval_run_parser.add_argument(
        "--status", action="append", choices=["done", "in_progress", "skipped"],
        help="Label statuses to include; repeatable (default: done)",
    )
    eval_run_parser.add_argument("--parish", help="Only this parish slug")
    eval_run_parser.add_argument(
        "--limit", type=int, help="Only the first N selected bulletins (a cheap smoke test)",
    )
    eval_run_parser.add_argument(
        "--concurrency", type=int, default=5,
        help="Number of parallel classifier calls (default: 5)",
    )
    eval_run_parser.add_argument(
        "--refresh", action="store_true",
        help="Ignore cached results and call the classifier again",
    )
    _add_eval_model_args(eval_run_parser)
    eval_run_parser.set_defaults(handler=_cmd_eval_run)
    _add_common_args(eval_run_parser)

    eval_report_parser = eval_subparsers.add_parser(
        "report",
        help="Score an eval run against the labels; writes report.md and report.json",
    )
    eval_report_parser.add_argument(
        "--classifier", required=True, choices=available_classifiers(),
        help="Name of the registered classifier",
    )
    eval_report_parser.add_argument(
        "--version", help="Classifier version to score (default: its current version)",
    )
    eval_report_parser.add_argument(
        "--status", action="append", choices=["done", "in_progress"],
        help="Label statuses to score; repeatable (default: done). Skipped labels never are",
    )
    _add_eval_model_args(eval_report_parser)
    eval_report_parser.set_defaults(handler=_cmd_eval_report)
    _add_common_args(eval_report_parser)

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
        help="Re-run weekly promotion over each parish's current events",
    )
    recurrence_apply_parser.set_defaults(handler=_cmd_recurrence_apply)
    _add_common_args(recurrence_apply_parser)

    # -- weekly --
    weekly_parser = subparsers.add_parser(
        "weekly",
        help="Run the weekly pipeline (fetch, process, snapshot, checks, report)",
    )
    weekly_parser.add_argument("--run-id", help="Run id (default: local-<timestamp>)")
    weekly_parser.add_argument(
        "--model", default=DEFAULT_GEMINI_MODEL,
        help=f"Gemini model (default: {DEFAULT_GEMINI_MODEL})",
    )
    weekly_parser.add_argument("--concurrency", type=int, default=5)
    weekly_parser.add_argument("--git-sha", default=None)
    weekly_parser.add_argument("--trigger", default=None)
    weekly_parser.add_argument(
        "--parish",
        action="append",
        default=None,
        metavar="PARISH",
        help=(
            "Parish slug or name to refresh (repeatable, or several slugs "
            "separated by commas). Default: every parish."
        ),
    )
    weekly_parser.add_argument(
        "--diocese",
        action="append",
        default=None,
        metavar="DIOCESE",
        help=(
            "Diocese slug (data/dioceses/<slug>) whose live parishes to refresh "
            "(repeatable, or comma-separated). Combines with --parish."
        ),
    )
    weekly_parser.set_defaults(handler=_cmd_weekly, exit_code_from_status=True)
    _add_common_args(weekly_parser)

    # -- data --
    data_parser = subparsers.add_parser("data", help="Pull and publish the pipeline database")
    data_parser.set_defaults(help_parser=data_parser)
    data_subparsers = data_parser.add_subparsers(dest="data_command")

    data_pull_parser = data_subparsers.add_parser(
        "pull", help="Download the published database and frontend snapshot",
    )
    data_pull_parser.add_argument("--run-id", help="A specific run instead of the published one")
    data_pull_parser.add_argument("--snapshot-only", action="store_true")
    data_pull_parser.add_argument("--no-snapshot", action="store_true")
    data_pull_parser.add_argument(
        "--public-fallback", action="store_true",
        help="With --snapshot-only: use the live site's snapshot when there are no R2 credentials",
    )
    data_pull_parser.set_defaults(handler=_cmd_data_pull)
    _add_common_args(data_pull_parser)

    data_snapshot_parser = data_subparsers.add_parser(
        "snapshot",
        help="Build the frontend snapshot from the published database with this code",
    )
    data_snapshot_parser.set_defaults(handler=_cmd_data_snapshot)
    _add_common_args(data_snapshot_parser)

    data_push_parser = data_subparsers.add_parser(
        "push", help="Upload a run's database, snapshot and report without publishing",
    )
    data_push_parser.add_argument("--run-id", required=True)
    data_push_parser.add_argument("--git-sha", default=None)
    data_push_parser.set_defaults(handler=_cmd_data_push)
    _add_common_args(data_push_parser)

    data_promote_parser = data_subparsers.add_parser(
        "promote", help="Publish an uploaded run (also how to roll back)",
    )
    data_promote_parser.add_argument("--run-id", required=True)
    data_promote_parser.add_argument(
        "--rollback", action="store_true",
        help="Allow publishing a run older than the published one",
    )
    data_promote_parser.set_defaults(handler=_cmd_data_promote)
    _add_common_args(data_promote_parser)

    data_status_parser = data_subparsers.add_parser(
        "status", help="Show the published run and recent uploaded runs",
    )
    data_status_parser.add_argument("--limit", type=int, default=10)
    data_status_parser.set_defaults(handler=_cmd_data_status)
    _add_common_args(data_status_parser)

    data_prune_parser = data_subparsers.add_parser(
        "prune",
        help="Delete old uploaded runs, keeping recent weeks and one run a month",
    )
    data_prune_parser.add_argument(
        "--keep-recent", type=int, default=DEFAULT_KEEP_RECENT,
        help=f"Most recent runs to keep (default {DEFAULT_KEEP_RECENT})",
    )
    data_prune_parser.add_argument(
        "--keep-monthly", type=int, default=DEFAULT_KEEP_MONTHLY,
        help=f"Months for which to keep that month's last run (default {DEFAULT_KEEP_MONTHLY})",
    )
    data_prune_parser.add_argument(
        "--apply", action="store_true", help="Delete; without it, only report what would go",
    )
    data_prune_parser.set_defaults(handler=_cmd_data_prune)
    _add_common_args(data_prune_parser)

    # -- diocese (exploring new dioceses; quiet by default, the JSON is the output) --
    add_diocese_parser(
        subparsers, lambda p: _add_common_args(p, default_level="WARNING"),
    )

    # -- db --
    db_parser = subparsers.add_parser("db", help="Database management commands")
    db_parser.set_defaults(help_parser=db_parser)
    db_subparsers = db_parser.add_subparsers(dest="db_command")

    db_create_parser = db_subparsers.add_parser(
        "create", help="Create an empty DB (schema + parishes/churches, no bulletins)",
    )
    db_create_parser.add_argument("--force", action="store_true")
    db_create_parser.set_defaults(handler=_cmd_db_create)
    _add_common_args(db_create_parser)

    db_drop_parser = db_subparsers.add_parser("drop", help="Delete the SQLite DB file")
    db_drop_parser.set_defaults(handler=_cmd_db_drop)
    _add_common_args(db_drop_parser)

    # -- label (local ground-truth labeling app) --
    label_parser = subparsers.add_parser("label", help="Label bulletins with ground truth")
    label_parser.set_defaults(help_parser=label_parser)
    label_subparsers = label_parser.add_subparsers(dest="label_command")

    label_serve_parser = label_subparsers.add_parser(
        "serve", help="Serve the labeling app on localhost",
    )
    label_serve_parser.add_argument("--port", type=int, default=LABELER_PORT)
    label_serve_parser.add_argument(
        "--demo", action="store_true",
        help="Use a generated demo dataset instead of data/ (no R2 needed)",
    )
    label_serve_parser.add_argument(
        "--demo-dir", default=str(DEMO_DIR),
        help=f"Where --demo builds its dataset and keeps its labels (default: {DEMO_DIR})",
    )
    label_serve_parser.set_defaults(handler=_cmd_label_serve)
    _add_common_args(label_serve_parser)

    # -- extract frontend db --
    extract_frontend_db_parser = subparsers.add_parser(
        "extract-frontend-db",
        help="Write apps/web/public/frontend.json.gz from the DB",
    )
    extract_frontend_db_parser.set_defaults(handler=_cmd_extract_frontend_db)
    _add_common_args(extract_frontend_db_parser)

    # -- verify frontend snapshot --
    verify_frontend_snapshot_parser = subparsers.add_parser(
        "verify-frontend-snapshot",
        help="Verify frontend snapshot similarity against frontend.json.gz.previous",
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
    _load_dotenv()

    try:
        result = handler(args)
    except (DioceseError, RunScopeError, ClassifierOptionError) as e:
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
    if getattr(args, "exit_code_from_status", False):
        # Distinct from 1 (a crash) and 2 (what argparse and uv use for usage
        # errors), so a caller can trust that "held" really means held.
        return {"passed": 0, "held": EXIT_HELD}.get(result.get("status"), 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
