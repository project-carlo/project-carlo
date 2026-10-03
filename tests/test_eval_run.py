"""`eval run`: classify the labeled bulletins and write label-shaped predictions."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import classifiers, runner
from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, set_store
from pdf_extract.classifiers.qualified_schedule import flatten_events
from pdf_extract.evals.run import labeled_bulletins, prediction_path, run, version_dir_name
from pdf_extract.labeling.demo import build_demo
from pdf_extract.labeling.labels import empty_label, write_label
from pdf_extract.storage import connect_db


class _FakeClassifier:
    name = "fake"
    version = "fake-v1"

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def extract(self, pdf_bytes: bytes, *, churches: list[dict], today: date) -> dict:
        self.calls.append({"churches": churches, "today": today})
        slot = {
            "church_slug": churches[0]["slug"], "day_of_week": "Friday",
            "start_time": "7:00 PM", "end_time": "8:30 PM", "weeks_of_month": ["first"],
            "season": {"start_month": "October", "start_day": None,
                       "end_month": "June", "end_day": None},
            "page_number": 1, "note": None,
        }
        result = flatten_events({"weekly_schedule": {"adorations": [slot]}})
        result["usage"] = {"input_tokens": 100, "output_tokens": 10}
        return result


@pytest.fixture
def demo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    paths = build_demo(tmp_path / "demo")
    set_store(CachedBlobStore(LocalBlobStore(paths["root"])))
    monkeypatch.setattr(runner, "RUNS_DIR", tmp_path / "runs")
    fake = _FakeClassifier()
    monkeypatch.setitem(classifiers.REGISTRY, "fake", lambda: fake)
    conn = connect_db(paths["db_path"])
    bulletins = conn.execute(
        """SELECT p.slug, b.source_url, b.content_hash, b.fetched_at
           FROM bulletin b JOIN parish p ON p.id = b.parish_id ORDER BY b.id"""
    ).fetchall()
    conn.close()
    return paths, fake, bulletins


def _label(labels_dir: Path, bulletin, status: str) -> None:
    slug, url, content_hash = bulletin["slug"], bulletin["source_url"], bulletin["content_hash"]
    label = empty_label(slug, content_hash, url) | {"status": status}
    write_label(label, parish_slug=slug, content_hash=content_hash, source_url=url,
                labels_dir=labels_dir)


def test_runs_done_labels_as_of_fetch_date_and_caches(demo):
    paths, fake, bulletins = demo
    done, in_progress = bulletins[0], bulletins[1]
    _label(paths["labels_dir"], done, "done")
    _label(paths["labels_dir"], in_progress, "in_progress")

    summary = run(classifier_name="fake", labels_dir=paths["labels_dir"],
                  db_path=paths["db_path"])

    assert summary["bulletins_selected"] == 1
    assert summary["classifier_calls"] == 1 and summary["cache_hits"] == 0
    assert summary["errors"] == [] and summary["skipped"] == []
    assert summary["usage_new_calls"] == {"input_tokens": 100, "output_tokens": 10}
    assert fake.calls[0]["today"] == date.fromisoformat(done["fetched_at"][:10])

    out = Path(summary["out_dir"])
    pred = json.loads(
        (out / "predictions" / done["slug"] / f"{done['content_hash'][:12]}.json").read_text()
    )
    assert pred["classifier_version"] == "fake-v1" and pred["from_cache"] is False
    [event] = pred["events"]
    assert {k: event[k] for k in (
        "event_type", "event_kind", "day_of_week", "start_time", "end_time",
        "weeks_of_month", "season",
    )} == {
        "event_type": "adoration", "event_kind": "weekly", "day_of_week": "Friday",
        "start_time": "19:00", "end_time": "20:30", "weeks_of_month": ["first"],
        "season": {"start_month": 10, "start_day": None, "end_month": 6, "end_day": None},
    }
    assert json.loads((out / "run.json").read_text())["events_written"] == 1

    again = run(classifier_name="fake", labels_dir=paths["labels_dir"],
                db_path=paths["db_path"])
    assert again["cache_hits"] == 1 and again["classifier_calls"] == 0
    assert again["usage_all_served"] == {"input_tokens": 100, "output_tokens": 10}
    assert len(fake.calls) == 1

    refreshed = run(classifier_name="fake", labels_dir=paths["labels_dir"],
                    db_path=paths["db_path"], refresh=True,
                    statuses=("done", "in_progress"))
    assert refreshed["classifier_calls"] == 2


def test_label_for_unknown_bulletin_is_skipped(demo):
    paths, fake, _ = demo
    labels_dir = paths["labels_dir"]
    _label(labels_dir, {"slug": "holy-family-demo", "source_url": "https://x/y.pdf",
                        "content_hash": "b" * 64}, "done")
    assert [b["content_hash"] for b in labeled_bulletins(labels_dir)] == ["b" * 64]

    summary = run(classifier_name="fake", labels_dir=labels_dir, db_path=paths["db_path"])
    assert summary["skipped"][0]["reason"] == "bulletin not in database"
    assert fake.calls == []


def test_prediction_paths_fit_windows_path_limit():
    # The longest parish slug, a long model name, and every setting on: from a
    # checkout at C:\\Users\\<user>\\Documents\\GitHub\\project-carlo\\ the path
    # must stay inside MAX_PATH (260), or git on Windows cannot commit it.
    checkout = "C:/Users/someuser/Documents/GitHub/project-carlo/"
    classifier = classifiers.get_classifier(
        "gpt-6-luna-nonstrict", model="gpt-6.1-sol", reasoning_effort="minimal",
        pdf_as_images=True, file_detail="original",
    )
    name = version_dir_name(classifier.name, classifier.version)
    assert name.startswith("nonstrict_reasoning-minimal_detail-original_pages-200dpi-")
    out_dir = Path("data/runs") / classifier.name / "eval" / name
    path = prediction_path(out_dir, "holy-mother-and-child-st-joseph-st-paul-greenfield-center",
                           "a" * 64)
    assert len(checkout + path.as_posix()) <= 245
    assert version_dir_name("gemini-flash", "gemini-2.5-flash+prompt-abc123").startswith(
        "gemini-2.5-flash-"
    )
