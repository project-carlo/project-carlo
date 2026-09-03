"""Entry point for the bulletin labeling app.

    uv run python apps/label/cli.py serve     # label bulletins in a browser
    uv run python apps/label/cli.py score     # score classifier runs against the labels
    uv run python apps/label/cli.py export    # dump ground truth as flat event rows

Or through pnpm: `pnpm label`, `pnpm label:score`, `pnpm label:export`.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Running this file directly puts apps/label on sys.path, which is what makes
# `labelapp` importable. Keep it explicit so the imports below survive being
# invoked from another working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from labelapp import corpus, score as scoring, store  # noqa: E402
from labelapp.server import serve  # noqa: E402

LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 8765


def _resolve_runs(requested: list[str] | None) -> list[str]:
    """Which classifier runs to work with, defaulting to every one on disk."""
    available = corpus.available_runs()
    if not available:
        raise SystemExit(
            "No classifier runs found under data/runs/.\n"
            "Produce one first, e.g. `pnpm extract -- --classifier gemini-flash`."
        )
    if not requested:
        return available
    missing = [name for name in requested if name not in available]
    if missing:
        raise SystemExit(
            f"No run on disk for: {', '.join(missing)}.\n"
            f"Available: {', '.join(available)}"
        )
    return list(requested)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python apps/label/cli.py",
        description="Collect and use human ground truth for bulletin event extraction.",
    )
    subparsers = parser.add_subparsers(dest="command")

    def add_common(target: argparse.ArgumentParser) -> None:
        target.add_argument(
            "--log-level",
            default="INFO",
            choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            help="Logging verbosity (default: INFO)",
        )

    serve_parser = subparsers.add_parser("serve", help="Start the labeling UI")
    serve_parser.add_argument(
        "--classifier",
        action="append",
        dest="classifiers",
        help="Classifier run to review (repeatable; default: every run in data/runs/)",
    )
    serve_parser.add_argument("--host", default="127.0.0.1", help="Bind address (loopback only)")
    serve_parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    serve_parser.add_argument(
        "--no-open", action="store_true", help="Do not open a browser on start"
    )
    add_common(serve_parser)

    score_parser = subparsers.add_parser(
        "score", help="Score classifier runs against data/labels.json"
    )
    score_parser.add_argument(
        "classifiers",
        nargs="*",
        help="Runs to score (default: every run in data/runs/)",
    )
    score_parser.add_argument("--out", default=None, help="Path for the JSON report")
    score_parser.add_argument(
        "--json", action="store_true", help="Print the full JSON report instead of a summary"
    )
    add_common(score_parser)

    export_parser = subparsers.add_parser(
        "export", help="Write accepted ground-truth events as flat rows"
    )
    export_parser.add_argument(
        "--out", default="data/labels_events.json", help="Output path"
    )
    export_parser.add_argument(
        "--include-partial",
        action="store_true",
        help="Also export bulletins that are labeled but not marked complete",
    )
    add_common(export_parser)
    return parser


def _export(out_path: Path, *, include_partial: bool) -> dict[str, int]:
    """Flatten accepted events into the same row shape as data/events.json."""
    labels = store.load_labels()
    rows = []
    exported_bulletins = 0
    for source_url, label in sorted(labels.items()):
        if not include_partial and label.get("status") != store.STATUS_COMPLETE:
            continue
        exported_bulletins += 1
        for event in label.get("events") or []:
            rows.append(
                {
                    "church_slug": event["church_slug"],
                    "bulletin_source_url": source_url,
                    "event_type": event["event_type"],
                    "event_kind": event["event_kind"],
                    "day_of_week": event["day_of_week"],
                    "date": event["date"],
                    "start_time": event["start_time"],
                    "end_time": event["end_time"],
                    "cancelled": event["cancelled"],
                    "page_number": event.get("page_number"),
                    "note": event.get("note"),
                }
            )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return {"bulletins": exported_bulletins, "events": len(rows), "path": str(out_path)}


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(sys.argv[1:] if argv is None else argv))
    if not args.command:
        parser.print_help()
        return 1

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )

    if args.command == "serve":
        serve(
            _resolve_runs(args.classifiers),
            host=args.host,
            port=args.port,
            open_browser=not args.no_open,
        )
        return 0

    if args.command == "score":
        try:
            report = scoring.score(
                _resolve_runs(args.classifiers or None),
                out_path=Path(args.out) if args.out else None,
            )
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(scoring.format_markdown(report))
            print(f"\nFull JSON report: {report['report_path']}")
        return 0

    if args.command == "export":
        result = _export(Path(args.out), include_partial=args.include_partial)
        print(json.dumps(result, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
