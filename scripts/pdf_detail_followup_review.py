"""Prepare disjoint visual-review packets without using Gemini as ground truth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pdf_detail_followup import DEFAULT_OUTPUT, ident, pred_path
from pdf_detail_study import write_json


def packets(output: Path, batch_size: int) -> None:
    source = output / "initial/comparison.json"
    if not source.exists():
        source = output / "initial/partial_comparison.json"
    comparison = json.loads(source.read_text(encoding="utf-8"))
    cohort = {
        ident(row): row for row in json.loads((output / "cohort.json").read_text())["bulletins"]
    }
    assigned = set()
    root = output / "review_packets"
    for packet in root.glob("*.json"):
        assigned.update(ident(row["comparison"]) for row in json.loads(packet.read_text())["cases"])
    pending = [row for row in comparison if row["review_needed"] and ident(row) not in assigned]
    count = len(list(root.glob("*.json")))
    for start in range(0, len(pending), batch_size):
        cases = []
        for row in pending[start : start + batch_size]:
            entry = cohort[ident(row)]
            cases.append(
                {
                    "cohort": entry,
                    "comparison": row,
                    "low": json.loads(pred_path(output / "initial/low", entry).read_text()),
                    "high": json.loads(pred_path(output / "initial/high", entry).read_text()),
                    "gemini": json.loads(pred_path(output / "gemini", entry).read_text()),
                }
            )
        write_json(root / f"batch-{count:03d}.json", {"cases": cases})
        count += 1
    print(json.dumps({"new_cases": len(pending), "total_batches": count}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--batch-size", type=int, default=10)
    args = parser.parse_args()
    packets(args.output, args.batch_size)


if __name__ == "__main__":
    main()
