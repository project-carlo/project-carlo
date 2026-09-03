"""Persisting human labels: normalization, identity, and durability."""

from __future__ import annotations

import json

import pytest

from labelapp import events as ev
from labelapp import store

URL = "https://example.org/bulletin.pdf"


def _event(**overrides):
    base = {
        "church_slug": "st-mary",
        "event_type": "mass",
        "event_kind": "weekly",
        "day_of_week": "Sunday",
        "date": None,
        "start_time": "9:00 AM",
        "end_time": None,
        "cancelled": False,
    }
    base.update(overrides)
    return base


def _payload(**overrides):
    base = {
        "bulletin_source_url": URL,
        "parish_slug": "st-mary-parish",
        "content_hash": "abc123",
        "status": store.STATUS_COMPLETE,
        "events": [_event()],
        "rejected": [],
    }
    base.update(overrides)
    return base


def test_round_trip_through_disk(tmp_path):
    path = tmp_path / "labels.json"
    store.put_label(_payload(), path)

    reloaded = store.load_labels(path)
    assert list(reloaded) == [URL]
    assert reloaded[URL]["status"] == store.STATUS_COMPLETE
    assert reloaded[URL]["events"][0]["start_time"] == "9:00 AM"
    assert reloaded[URL]["labeled_at"].endswith("Z")


def test_missing_file_reads_as_no_labels(tmp_path):
    assert store.load_labels(tmp_path / "nothing.json") == {}


def test_key_id_is_recomputed_rather_than_trusted(tmp_path):
    """A stale or hand-edited payload must not be able to store an event whose
    recorded id disagrees with its own fields — scoring keys off that id."""
    path = tmp_path / "labels.json"
    store.put_label(_payload(events=[_event(key_id="not-a-real-id")]), path)

    stored = store.load_labels(path)[URL]["events"][0]
    assert stored["key_id"] == ev.event_id(_event())


def test_acceptance_wins_over_rejection(tmp_path):
    """The same event cannot be both ground truth and a confirmed error."""
    path = tmp_path / "labels.json"
    store.put_label(_payload(events=[_event()], rejected=[_event()]), path)

    label = store.load_labels(path)[URL]
    assert len(label["events"]) == 1
    assert label["rejected"] == []


def test_duplicate_events_collapse(tmp_path):
    path = tmp_path / "labels.json"
    store.put_label(_payload(events=[_event(), _event(), _event()]), path)
    assert len(store.load_labels(path)[URL]["events"]) == 1


def test_unusable_events_are_dropped(tmp_path):
    path = tmp_path / "labels.json"
    store.put_label(
        _payload(
            events=[
                _event(),
                _event(church_slug=""),          # no church
                _event(start_time=""),           # no time
                _event(event_kind="sometimes"),  # not a recurrence the schema allows
                "not an event",
            ]
        ),
        path,
    )
    assert len(store.load_labels(path)[URL]["events"]) == 1


def test_unknown_status_falls_back_to_in_progress(tmp_path):
    path = tmp_path / "labels.json"
    store.put_label(_payload(status="finished-ish"), path)
    assert store.load_labels(path)[URL]["status"] == store.STATUS_IN_PROGRESS


def test_a_label_without_a_bulletin_is_refused(tmp_path):
    with pytest.raises(ValueError, match="bulletin_source_url"):
        store.normalize_label({"events": [_event()]})


def test_hand_added_events_keep_their_origin(tmp_path):
    path = tmp_path / "labels.json"
    store.put_label(
        _payload(events=[_event(origin="human", start_time="6:45 PM")]), path
    )
    stored = store.load_labels(path)[URL]["events"][0]
    assert stored["origin"] == "human"


def test_decided_ids_covers_both_verdicts():
    label = {
        "events": [{"key_id": "a"}],
        "rejected": [{"key_id": "b"}],
    }
    assert store.decided_ids(label) == {"a", "b"}
    assert store.decided_ids(None) == set()


def test_delete_removes_only_that_bulletin(tmp_path):
    path = tmp_path / "labels.json"
    store.put_label(_payload(), path)
    store.put_label(_payload(bulletin_source_url="https://example.org/other.pdf"), path)

    assert store.delete_label(URL, path) is True
    assert store.delete_label(URL, path) is False
    assert list(store.load_labels(path)) == ["https://example.org/other.pdf"]


def test_existing_labels_survive_a_failed_write(tmp_path, monkeypatch):
    """Ground truth is the one artifact that cannot be regenerated, so a crash
    mid-write must not truncate the file."""
    path = tmp_path / "labels.json"
    store.put_label(_payload(), path)
    before = path.read_text(encoding="utf-8")

    def explode(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(store.os, "replace", explode)
    with pytest.raises(OSError):
        store.put_label(_payload(bulletin_source_url="https://example.org/2.pdf"), path)

    assert path.read_text(encoding="utf-8") == before
    assert not list(tmp_path.glob("*.tmp"))


def test_corrupt_labels_file_is_reported_not_silently_dropped(tmp_path):
    path = tmp_path / "labels.json"
    path.write_text("{ this is not json", encoding="utf-8")
    with pytest.raises(ValueError, match="not valid JSON"):
        store.load_labels(path)


def test_labels_are_written_sorted_for_a_readable_diff(tmp_path):
    path = tmp_path / "labels.json"
    for url in ("https://example.org/c.pdf", "https://example.org/a.pdf"):
        store.put_label(_payload(bulletin_source_url=url), path)

    assert list(json.loads(path.read_text(encoding="utf-8"))) == [
        "https://example.org/a.pdf",
        "https://example.org/c.pdf",
    ]
