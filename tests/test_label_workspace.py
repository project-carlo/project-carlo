"""Queue ordering and progress for a labeling session."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from labelapp import corpus, store
from labelapp.workspace import Workspace

URLS = [f"https://example.org/b{index}.pdf" for index in range(3)]


def _ev(url: str, **overrides):
    base = {
        "church_slug": "st-mary",
        "bulletin_source_url": url,
        "event_type": "mass",
        "event_kind": "weekly",
        "day_of_week": "Sunday",
        "date": None,
        "start_time": "9:00 AM",
        "end_time": None,
        "cancelled": False,
        "page_number": 1,
        "note": None,
    }
    base.update(overrides)
    return base


def _write_run(root: Path, name: str, events: list[dict], urls: list[str]) -> None:
    run_dir = root / "runs" / name
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "events.json").write_text(json.dumps(events), encoding="utf-8")
    (run_dir / "bulletins.json").write_text(
        json.dumps([{"bulletin_source_url": url} for url in urls]), encoding="utf-8"
    )


@pytest.fixture
def corpus_dir(tmp_path, monkeypatch):
    """A three-bulletin corpus with a different amount of disagreement in each."""
    monkeypatch.setattr(corpus, "RUNS_DIR", tmp_path / "runs")
    monkeypatch.setattr(corpus, "BULLETINS_METADATA_PATH", tmp_path / "metadata.json")
    monkeypatch.setattr(corpus, "CHURCHES_CSV_PATH", tmp_path / "churches.csv")
    monkeypatch.setattr(corpus, "PARISHES_CSV_PATH", tmp_path / "parishes.csv")
    monkeypatch.setattr(store, "LABELS_PATH", tmp_path / "labels.json")

    (tmp_path / "metadata.json").write_text(
        json.dumps(
            [
                {
                    "source_url": url,
                    "parish_slug": f"parish-{index}",
                    "content_hash": f"hash{index}",
                    "pdf_path": f"data\\bulletins\\parish-{index}\\x.pdf",
                    "published_date": f"2026-03-0{index + 1}",
                    "fetched_at": f"2026-03-0{index + 1}T00:00:00Z",
                }
                for index, url in enumerate(URLS)
            ]
        ),
        encoding="utf-8",
    )

    shared = [_ev(url) for url in URLS]
    # b0: no disagreement. b1: one. b2: three.
    a_only = [_ev(URLS[1], start_time="11:00 AM")]
    a_only += [_ev(URLS[2], start_time=f"{hour}:00 PM") for hour in (1, 2, 3)]

    _write_run(tmp_path, "a", shared + a_only, URLS)
    _write_run(tmp_path, "b", list(shared), URLS)
    return tmp_path


def test_queue_leads_with_the_most_disagreement(corpus_dir):
    workspace = Workspace(["a", "b"])
    order = [row["bulletin_source_url"] for row in workspace.queue(sort="disagreement")]
    assert order == [URLS[2], URLS[1], URLS[0]]


def test_quickest_ordering_leads_with_the_smallest_open_job(corpus_dir):
    workspace = Workspace(["a", "b"])
    rows = workspace.queue(sort="quickest")
    assert rows[0]["bulletin_source_url"] == URLS[1]
    assert rows[0]["undecided_count"] == 1


def test_completed_bulletins_sink_and_stop_counting_as_work(corpus_dir):
    workspace = Workspace(["a", "b"])
    store.put_label(
        {
            "bulletin_source_url": URLS[2],
            "parish_slug": "parish-2",
            "status": store.STATUS_COMPLETE,
            "events": [_ev(URLS[2])],
            "rejected": [_ev(URLS[2], start_time=f"{hour}:00 PM") for hour in (1, 2, 3)],
        },
        store.LABELS_PATH,
    )
    workspace.reload_labels()

    order = [row["bulletin_source_url"] for row in workspace.queue(sort="disagreement")]
    assert order[-1] == URLS[2]
    assert workspace.progress()["complete"] == 1
    assert workspace.progress()["disputed_undecided"] == 1


def test_todo_filter_hides_finished_bulletins(corpus_dir):
    workspace = Workspace(["a", "b"])
    store.put_label(
        {
            "bulletin_source_url": URLS[0],
            "parish_slug": "parish-0",
            "status": store.STATUS_COMPLETE,
            "events": [_ev(URLS[0])],
        },
        store.LABELS_PATH,
    )
    workspace.reload_labels()

    remaining = [row["bulletin_source_url"] for row in workspace.queue(which="todo")]
    assert URLS[0] not in remaining
    assert len(remaining) == 2


def test_next_url_wraps_around_the_queue(corpus_dir):
    workspace = Workspace(["a", "b"])
    order = [row["bulletin_source_url"] for row in workspace.queue(sort="parish")]
    assert workspace.next_url(order[0], sort="parish") == order[1]
    assert workspace.next_url(order[-1], sort="parish") == order[0]


def test_windows_pdf_paths_resolve_on_this_platform(corpus_dir):
    """metadata.json records whatever separator the fetching machine used."""
    assert corpus.normalize_pdf_path("data\\bulletins\\p\\x.pdf") == Path(
        "data/bulletins/p/x.pdf"
    )
    workspace = Workspace(["a", "b"])
    review = workspace.review(URLS[0])
    assert review["has_pdf"] is False  # normalized, and correctly reported missing
