"""The labeler's API: finding bulletins, Gemini sources, label files and path safety."""

from __future__ import annotations

import copy
import http.client
import json
import threading
from pathlib import Path

import pytest

from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, set_store
from pdf_extract.labeling.bulletins import (
    bulletin_detail,
    gemini_rows,
    list_bulletins,
    next_bulletin,
    progress,
)
from pdf_extract.labeling.demo import OLD_CLASSIFIER_VERSION, build_demo, make_pdf
from pdf_extract.labeling.labels import (
    LabelError,
    empty_label,
    label_path,
    label_statuses,
    read_label,
    validate_label,
    write_label,
)
from pdf_extract.labeling.server import LabelerApp, make_server
from pdf_extract.storage import connect_db

HASH = "a" * 64


@pytest.fixture
def demo(tmp_path: Path) -> dict[str, Path]:
    paths = build_demo(tmp_path / "demo")
    set_store(CachedBlobStore(LocalBlobStore(paths["root"])))
    return paths


@pytest.fixture
def conn(demo: dict[str, Path]):
    c = connect_db(demo["db_path"])
    yield c
    c.close()


def _queue_key(conn, parish: str, rank: int = 0) -> tuple[str, str]:
    for b in list_bulletins(conn, Path("unused-labels")):
        if b["parish_slug"] == parish and b["rank"] == rank:
            return parish, b["content_hash"]
    raise AssertionError(f"no bulletin for {parish} rank {rank}")


def _event(**overrides) -> dict:
    event = {
        "church_slug": "holy-family-demo-rochester",
        "event_type": "mass",
        "event_kind": "weekly",
        "day_of_week": "Sunday",
        "date": None,
        "start_time": "10:30",
        "end_time": None,
        "cancelled": False,
        "weeks_of_month": [],
        "season": None,
        "page_number": 2,
        "note": None,
        "origin": "human",
    }
    event.update(overrides)
    return event


def _label(parish: str = "holy-family-demo", content_hash: str = HASH, **overrides) -> dict:
    label = empty_label(parish, content_hash, "https://example.org/b.pdf")
    label["events"] = [_event()]
    label.update(overrides)
    return label


# ── Finding bulletins ───────────────────────────────────────────────────────
def test_queue_takes_each_parishs_latest_bulletin_first(conn, demo):
    queue = list_bulletins(conn, demo["labels_dir"])
    assert [(b["parish_slug"], b["rank"]) for b in queue] == [
        ("holy-family-demo", 0),
        ("our-lady-demo", 0),
        ("st-anne-demo", 0),
        ("holy-family-demo", 1),
    ]
    assert queue[0]["published_date"] == "2026-09-27"
    assert queue[3]["published_date"] == "2026-09-20"
    assert {b["status"] for b in queue} == {"unlabeled"}


def test_queue_counts_a_pdf_fetched_twice_once(conn, demo):
    parish, content_hash = _queue_key(conn, "st-anne-demo")
    with conn:
        conn.execute(
            "INSERT INTO bulletin(parish_id, source_url, content_hash, fetched_at)"
            " SELECT parish_id, 'https://example.org/other-url.pdf', content_hash, fetched_at"
            " FROM bulletin WHERE content_hash = ?",
            (content_hash,),
        )
    queue = list_bulletins(conn, demo["labels_dir"])
    assert sum(1 for b in queue if b["content_hash"] == content_hash) == 1


def test_statuses_next_and_progress_follow_label_files(conn, demo):
    labels_dir = demo["labels_dir"]
    first = _queue_key(conn, "holy-family-demo")
    second = _queue_key(conn, "our-lady-demo")
    write_label(_label(*first, status="done"), parish_slug=first[0], content_hash=first[1],
                source_url="u", labels_dir=labels_dir)
    write_label(_label(*second), parish_slug=second[0], content_hash=second[1],
                source_url="u", labels_dir=labels_dir)

    queue = list_bulletins(conn, labels_dir)
    statuses = {(b["parish_slug"], b["content_hash"]): b["status"] for b in queue}
    assert statuses[first] == "done"
    assert statuses[second] == "in_progress"

    # Unlabeled bulletins come before ones left in progress, and "next" moves on.
    nxt = next_bulletin(queue)
    assert (nxt["parish_slug"], nxt["rank"]) == ("st-anne-demo", 0)
    nxt = next_bulletin(queue, after=(nxt["parish_slug"], nxt["content_hash"]))
    assert (nxt["parish_slug"], nxt["rank"]) == ("holy-family-demo", 1)
    assert next_bulletin(queue, parish_slug="our-lady-demo")["status"] == "in_progress"
    assert next_bulletin(queue, after=second, parish_slug="our-lady-demo") is None

    counts = progress(queue)
    assert counts["latest_total"] == 3
    assert counts["latest_done"] == 1
    assert counts["done"] == 1 and counts["in_progress"] == 1 and counts["unlabeled"] == 2


# ── Gemini sources ──────────────────────────────────────────────────────────
def test_gemini_from_the_current_cache_version(conn):
    detail = bulletin_detail(conn, *_queue_key(conn, "holy-family-demo"))
    gemini = detail["gemini"]
    assert gemini["source"]["kind"] == "cache"
    assert gemini["source"]["is_current_version"] is True
    assert gemini["source"]["church_list_matches"] is True
    assert gemini["source"]["model"] == "gemini-3-flash-preview"
    assert gemini["published_date"] == "2026-09-27"
    assert len(gemini["events"]) == 15
    saturday = gemini["events"][0]
    assert saturday["start_time"] == "16:00"
    assert saturday["raw"]["start_time"] == "4:00 PM"
    cancelled = [e for e in gemini["events"] if e["cancelled"]]
    assert cancelled[0]["event_kind"] == "specific_date"
    assert cancelled[0]["date"] == "2026-10-05"
    assert [c["slug"] for c in detail["churches"]] == [
        "holy-family-demo-rochester", "st-joseph-demo-penfield",
    ]


def test_gemini_from_an_older_cache_version(conn):
    gemini = bulletin_detail(conn, *_queue_key(conn, "st-anne-demo"))["gemini"]
    source = gemini["source"]
    assert source["kind"] == "cache"
    assert source["is_current_version"] is False
    assert source["church_list_matches"] is True
    old_model, _, old_prompt = OLD_CLASSIFIER_VERSION.partition("+prompt-")
    assert (source["model"], source["prompt_version"]) == (old_model, old_prompt)
    tuesday = next(e for e in gemini["events"] if e["day_of_week"] == "Tuesday")
    assert tuesday["start_time"] == "12:10"
    adoration = next(e for e in gemini["events"] if e["event_type"] == "adoration")
    assert adoration["end_time"] is None
    assert adoration["problems"] == ["unreadable end time 'after Mass'"]


def test_gemini_cached_against_an_older_church_list_is_still_found(conn):
    parish, content_hash = _queue_key(conn, "holy-family-demo")
    with conn:
        conn.execute("UPDATE church SET name = 'Holy Family (renamed)' "
                     "WHERE slug = 'holy-family-demo-rochester'")
    source = bulletin_detail(conn, parish, content_hash)["gemini"]["source"]
    assert source["kind"] == "cache"
    assert source["is_current_version"] is True
    assert source["church_list_matches"] is False


def test_gemini_falls_back_to_the_event_table(conn):
    gemini = bulletin_detail(conn, *_queue_key(conn, "holy-family-demo", rank=1))["gemini"]
    assert gemini["source"]["kind"] == "post-processing"
    assert gemini["source"]["model"] is None
    assert gemini["published_date"] == "2026-09-20"
    spanish = next(e for e in gemini["events"] if e["note"] == "Spanish")
    assert (spanish["day_of_week"], spanish["start_time"]) == ("Wednesday", "19:00")
    assert spanish["church_slug"] == "st-joseph-demo-penfield"


def test_gemini_none_for_an_unprocessed_bulletin(conn):
    gemini = bulletin_detail(conn, *_queue_key(conn, "our-lady-demo"))["gemini"]
    assert gemini["source"]["kind"] == "none"
    assert gemini["events"] == []


def test_unknown_bulletin_has_no_detail(conn):
    assert bulletin_detail(conn, "holy-family-demo", HASH) is None


def test_gemini_rows_carry_schema_v2_qualifiers_and_problems():
    rows = gemini_rows([
        {"church_slug": "c", "type": "confession", "kind": "weekly", "day_of_week": "fri",
         "start_time": "noon", "end_time": None, "weeks_of_month": ["First", "last", "x"],
         "season_start_month": 9, "season_end_month": 5},
        {"church_slug": "c", "type": "vespers", "kind": "specific_date", "date": "sometime",
         "start_time": "later"},
    ])
    assert rows[0]["day_of_week"] == "Friday"
    assert rows[0]["start_time"] == "12:00"
    assert rows[0]["weeks_of_month"] == ["first", "last"]
    assert rows[0]["season"] == {"start_month": 9, "start_day": None, "end_month": 5,
                                 "end_day": None}
    assert rows[0]["problems"] == []
    assert rows[1]["problems"] == [
        "unknown type 'vespers'", "unreadable date 'sometime'", "unreadable start time 'later'",
    ]


# ── Label validation ────────────────────────────────────────────────────────
def test_a_complete_label_is_valid():
    label = _label(events=[
        _event(weeks_of_month=["first", "third"],
               season={"start_month": 9, "start_day": None, "end_month": 5, "end_day": 31}),
        _event(event_kind="specific_date", day_of_week=None, date="2026-10-05",
               cancelled=True, origin="gemini-edited", end_time="09:00"),
    ])
    label["published_date"] = "2026-09-27"
    assert validate_label(label) == []


@pytest.mark.parametrize("change, message", [
    ({"day_of_week": None}, "day_of_week must be a weekday name"),
    ({"date": "2026-10-05"}, "date must be null for a weekly event"),
    ({"event_kind": "specific_date", "day_of_week": None, "date": "2026-02-30"},
     "date must be YYYY-MM-DD"),
    ({"event_kind": "specific_date", "day_of_week": None, "date": "2026-10-05",
      "weeks_of_month": ["first"]}, "weeks_of_month applies to weekly events only"),
    ({"event_kind": "specific_date", "day_of_week": None, "date": "2026-10-05",
      "season": {"start_month": 9, "start_day": None, "end_month": 5, "end_day": None}},
     "season applies to weekly events only"),
    ({"start_time": "5:30 PM"}, "start_time must be HH:MM"),
    ({"start_time": "24:00"}, "start_time must be HH:MM"),
    ({"end_time": "7pm"}, "end_time must be null or HH:MM"),
    ({"weeks_of_month": ["first", "first"]}, "weeks_of_month has duplicates"),
    ({"weeks_of_month": ["1st"]}, "weeks_of_month must be a list"),
    ({"season": {"start_month": 13, "start_day": None, "end_month": 5, "end_day": None}},
     "season.start_month must be 1-12"),
    ({"season": {"start_month": 2, "start_day": 30, "end_month": 5, "end_day": None}},
     "season.start_day must be null or a day of month 2"),
    ({"season": {"start_month": 9, "end_month": 5}}, "season: missing start_day, end_day"),
    ({"origin": "model"}, "origin must be one of"),
    ({"cancelled": "no"}, "cancelled must be true or false"),
    ({"page_number": 0}, "page_number must be null or a positive integer"),
    ({"church_slug": "../x"}, "church_slug must be a church slug"),
    ({"extra": 1}, "unknown extra"),
])
def test_invalid_events_are_rejected(change, message):
    errors = validate_label(_label(events=[_event(**change)]))
    assert any(message in e for e in errors), errors


@pytest.mark.parametrize("change, message", [
    ({"schema_version": 2}, "schema_version must be 1"),
    ({"status": "finished"}, "status must be one of"),
    ({"flags": {"wrong_bulletin": True}}, "flags: missing"),
    ({"flags": {"wrong_bulletin": 1, "unreadable": False, "no_schedule": False,
                "church_missing": False}}, "flags.wrong_bulletin must be true or false"),
    ({"published_date": "Sept 27"}, "published_date must be null or YYYY-MM-DD"),
    ({"seconds_spent": -1}, "seconds_spent must be a non-negative integer"),
    ({"seconds_spent": 1.5}, "seconds_spent must be a non-negative integer"),
    ({"events": {}}, "events must be a list"),
])
def test_invalid_labels_are_rejected(change, message):
    errors = validate_label(_label(**change))
    assert any(message in e for e in errors), errors


# ── Writing labels and path safety ──────────────────────────────────────────
def test_write_label_saves_one_file_per_bulletin(tmp_path: Path):
    labels_dir = tmp_path / "labels"
    saved = write_label(_label(source_url="https://attacker.example/"),
                        parish_slug="holy-family-demo", content_hash=HASH,
                        source_url="https://example.org/real.pdf", labels_dir=labels_dir)
    path = labels_dir / "holy-family-demo" / f"{HASH}.json"
    on_disk = json.loads(path.read_text(encoding="utf-8"))
    assert on_disk == saved
    assert saved["source_url"] == "https://example.org/real.pdf"
    assert saved["updated_at"].endswith("Z")
    assert list(saved) == list(empty_label("p", HASH, "u"))
    assert read_label("holy-family-demo", HASH, labels_dir) == saved
    assert label_statuses(labels_dir) == {("holy-family-demo", HASH): "in_progress"}


def test_write_label_rejects_invalid_labels_without_writing(tmp_path: Path):
    labels_dir = tmp_path / "labels"
    bad = _label(events=[_event(start_time="")])
    with pytest.raises(LabelError, match="start_time"):
        write_label(bad, parish_slug="holy-family-demo", content_hash=HASH, source_url="u",
                    labels_dir=labels_dir)
    with pytest.raises(LabelError, match="unknown sneaky"):
        write_label({**_label(), "sneaky": True}, parish_slug="holy-family-demo",
                    content_hash=HASH, source_url="u", labels_dir=labels_dir)
    with pytest.raises(LabelError, match="do not match"):
        write_label(_label(parish="other-parish"), parish_slug="holy-family-demo",
                    content_hash=HASH, source_url="u", labels_dir=labels_dir)
    assert not labels_dir.exists() or not any(labels_dir.rglob("*.json"))


@pytest.mark.parametrize("parish, content_hash", [
    ("..", HASH),
    ("../etc", HASH),
    ("a/b", HASH),
    ("Holy-Family", HASH),
    ("", HASH),
    ("parish", "../" + "a" * 61),
    ("parish", "A" * 64),
    ("parish", "a" * 63),
    ("parish", HASH + ".json"),
    ("parish", "/" + "a" * 63),
])
def test_label_path_refuses_anything_that_could_escape(tmp_path: Path, parish, content_hash):
    with pytest.raises(LabelError):
        label_path(parish, content_hash, tmp_path / "labels")


def test_label_path_stays_inside_the_labels_dir(tmp_path: Path):
    path = label_path("st-anne", HASH, tmp_path / "labels")
    assert path == (tmp_path / "labels" / "st-anne" / f"{HASH}.json").resolve()


def test_label_statuses_ignores_stray_files(tmp_path: Path):
    labels_dir = tmp_path / "labels"
    (labels_dir / "parish").mkdir(parents=True)
    (labels_dir / "parish" / "notes.json").write_text("{}")
    (labels_dir / "parish" / f"{HASH}.json").write_text("not json")
    (labels_dir / "parish" / f"{'b' * 64}.json").write_text('{"status": "done"}')
    assert label_statuses(labels_dir) == {("parish", "b" * 64): "done"}


# ── Demo data ───────────────────────────────────────────────────────────────
def test_demo_pdfs_are_readable_and_rebuilds_keep_labels(demo):
    from pypdf import PdfReader

    pdfs = sorted((demo["root"] / "bulletins").rglob("*.pdf"))
    assert len(pdfs) == 4
    reader = PdfReader(str(next(p for p in pdfs if "holy-family" in str(p))))
    text = "".join(page.extract_text() for page in reader.pages)
    assert "Mass" in text or "MASS" in text

    (demo["labels_dir"] / "keep.txt").write_text("kept")
    build_demo(demo["root"])
    assert (demo["labels_dir"] / "keep.txt").read_text() == "kept"
    assert make_pdf([[(12, "x")]]) == make_pdf([[(12, "x")]])


# ── HTTP ────────────────────────────────────────────────────────────────────
@pytest.fixture
def server(demo, tmp_path: Path):
    static = tmp_path / "dist"
    static.mkdir()
    (static / "index.html").write_text("<!doctype html><title>labeler</title>")
    (static / "assets").mkdir()
    (static / "assets" / "app.js").write_text("console.log(1)")
    app = LabelerApp(db_path=demo["db_path"], labels_dir=demo["labels_dir"], static_dir=static,
                     mode="demo")
    srv = make_server(app, port=0)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()
    srv.server_close()


def _request(srv, method: str, path: str, body=None, headers=None):
    conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1], timeout=10)
    all_headers = {"Host": f"localhost:{srv.server_address[1]}"}
    data = None
    if body is not None:
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        all_headers["Content-Type"] = "application/json"
    all_headers.update(headers or {})
    conn.request(method, path, body=data, headers=all_headers)
    resp = conn.getresponse()
    payload = resp.read()
    conn.close()
    ctype = resp.getheader("Content-Type") or ""
    return resp.status, json.loads(payload) if "json" in ctype else payload


def test_http_queue_detail_pdf_and_save(server, demo):
    status, queue = _request(server, "GET", "/api/bulletins")
    assert status == 200
    first = queue["bulletins"][0]
    key = f"{first['parish_slug']}/{first['content_hash']}"
    assert queue["progress"]["latest_total"] == 3

    status, detail = _request(server, "GET", f"/api/bulletins/{key}")
    assert status == 200
    assert detail["label"] is None
    assert detail["gemini"]["source"]["kind"] == "cache"

    status, pdf = _request(server, "GET", f"/api/bulletins/{key}/pdf")
    assert status == 200 and pdf.startswith(b"%PDF")

    label = _label(first["parish_slug"], first["content_hash"], status="done")
    status, saved = _request(server, "PUT", f"/api/labels/{key}", label)
    assert status == 200
    assert saved["label"]["source_url"] == first["source_url"]
    path = demo["labels_dir"] / first["parish_slug"] / f"{first['content_hash']}.json"
    assert json.loads(path.read_text())["status"] == "done"

    status, nxt = _request(server, "GET", f"/api/next?after={key}")
    assert status == 200
    assert nxt["bulletin"]["parish_slug"] == "our-lady-demo"
    assert nxt["progress"]["latest_done"] == 1

    status, config = _request(server, "GET", "/api/config")
    assert config["mode"] == "demo" and config["classifier"] == "gemini-flash"


def test_http_rejects_bad_labels_and_unsafe_paths(server, demo):
    _, queue = _request(server, "GET", "/api/bulletins")
    first = queue["bulletins"][0]
    key = f"{first['parish_slug']}/{first['content_hash']}"
    label = _label(first["parish_slug"], first["content_hash"])

    status, err = _request(server, "PUT", f"/api/labels/{key}",
                           {**label, "events": [_event(start_time="noon")]})
    assert status == 400 and "start_time" in err["error"]
    status, _ = _request(server, "PUT", f"/api/labels/{key}", b"{not json")
    assert status == 400
    status, _ = _request(server, "PUT", f"/api/labels/holy-family-demo/{HASH}",
                         _label("holy-family-demo", HASH))
    assert status == 404
    for path in (
        f"/api/labels/..%2F..%2Ftmp/{HASH}",
        f"/api/labels/%2E%2E/{HASH}",
        "/api/labels/holy-family-demo/..%2F..%2Fescape",
        f"/api/bulletins/..%2Fx/{HASH}/pdf",
    ):
        method = "GET" if path.endswith("/pdf") else "PUT"
        status, _ = _request(server, method, path, label if method == "PUT" else None)
        assert status in (400, 404), path
    assert list(demo["labels_dir"].rglob("*.json")) == []


def test_http_refuses_non_local_hosts_and_origins(server):
    status, _ = _request(server, "GET", "/api/config", headers={"Host": "evil.example"})
    assert status == 403
    status, _ = _request(server, "PUT", f"/api/labels/holy-family-demo/{HASH}",
                         _label(), headers={"Origin": "https://evil.example"})
    assert status == 403
    status, _ = _request(server, "GET", "/api/config",
                         headers={"Origin": "http://localhost:5174"})
    assert status == 200


def test_http_serves_the_built_ui_without_leaving_it(server):
    status, body = _request(server, "GET", "/assets/app.js")
    assert status == 200 and body == b"console.log(1)"
    status, body = _request(server, "GET", "/")
    assert status == 200 and b"labeler" in body
    status, body = _request(server, "GET", "/..%2F..%2Fpyproject.toml")
    assert status == 200 and b"labeler" in body
    status, err = _request(server, "GET", "/api/nope")
    assert status == 404 and "No such endpoint" in err["error"]


def test_label_round_trip_keeps_event_order(tmp_path: Path):
    labels_dir = tmp_path / "labels"
    events = [_event(start_time=t) for t in ("17:00", "08:00", "12:00")]
    label = _label(events=copy.deepcopy(events))
    saved = write_label(label, parish_slug="holy-family-demo", content_hash=HASH,
                        source_url="u", labels_dir=labels_dir)
    assert [e["start_time"] for e in saved["events"]] == ["17:00", "08:00", "12:00"]
