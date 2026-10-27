"""Apply the reviewed October 25 corrections to the recorded source state only."""

import json
from pathlib import Path

from pdf_extract.schedule.repairs import apply_review


def migrate(conn):
    spec = Path(__file__).resolve().parents[1] / "update-evals/2026-10-25/repairs.json"
    apply_review(conn, json.loads(spec.read_text(encoding="utf-8")))
