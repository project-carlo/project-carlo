"""Structured edits preserve evidence, reject invalid changes, and remain pipeable."""

from __future__ import annotations

import io
import json
from datetime import date
from pathlib import Path

import pytest

from pdf_extract import storage
from pdf_extract.__main__ import main
from pdf_extract.dioceses import cli, records, report
from pdf_extract.dioceses.records import DioceseError

EVIDENCE = [{"url": "https://example.org/issue.pdf", "seen": "2026-10-21",
             "quote": "Masthead: St. Anne’s & St. Mary's", "note": "Page 2: both members."}]


@pytest.fixture()
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DIOCESES_DIR", tmp_path / "dioceses")
    monkeypatch.setattr(storage, "PARISHES_CSV_PATH", tmp_path / "parishes.csv")
    monkeypatch.setattr(storage, "CHURCHES_CSV_PATH", tmp_path / "churches.csv")
    monkeypatch.setattr(records, "today", lambda: "2026-10-22")
    records.init_diocese("test", name="Test", state="PA")
    return tmp_path / "dioceses" / "test"


def _payload(name="St. Anne"):
    return {"name": name, "website": f"https://example.org/{records.slugify(name)}",
            "bulletin_provider": "no_bulletin", "evidence": EVIDENCE,
            "body": "## Publisher\n\nNo file found. A colon: and a quote ‘stay intact’."}


def _attempt(**changes):
    return {"method": "parish-site", "url": "https://example.org/bulletins",
            "checked": "2026-10-21", "outcome": "unsupported-format",
            "next_action": "Read the existing Word bulletin after format support is added.",
            "retry_when": "The pipeline supports docx.", **changes}


def _write(slug="anne", payload=None, **kwargs):
    return records.write_record("test", "parish", slug, payload or _payload(), **kwargs)


def test_writer_roundtrips_colons_unicode_and_multiline_evidence(root):
    payload = {**_payload(), "research": [_attempt()], "bulletin_status": "unsupported-format"}
    payload["evidence"] = [{**EVIDENCE[0], "note": "Page 2: members\nPage 3: Mass schedule"}]
    result = _write(payload=payload, create=True)
    record = records.load("test").of(records.PARISH)["anne"]
    assert {key: record[key] for key in payload} == payload
    assert result["path"] == "parishes/anne.md" and result["slug"] == "anne"
    assert result["validation"]["errors"] == 0
    assert sorted(p.name for p in (root / "parishes").iterdir()) == [".gitkeep", "anne.md"]


def test_writer_patches_fields_and_replaces_lists_without_losing_evidence(root):
    _write(create=True)
    result = _write(payload={"publication": ["url:https://example.org/one"],
                             "research": [_attempt()]})
    _write(payload={"publication": []})
    record = records.load("test").of(records.PARISH)["anne"]
    assert record["evidence"] == EVIDENCE
    assert record["research"] == [_attempt()]
    assert record["publication"] == []
    assert result["written"] == ["parishes/anne.md"]


@pytest.mark.parametrize("patch", [
    {"website": "bad-url"}, {"publication": 123}, {"provider_id": {}},
    {"evidence": ["a quote"]}, {"evidence": [{"url": "bad", "seen": "2026-10-21"}]},
    {"research": [_attempt(checked="2026-02-30")]},
    {"research": [_attempt(outcome="no-bulletin")]},
    {"research": [_attempt(next_action="")]}, {"research": [_attempt(retry_when="")]},
    {"research": [_attempt(revisit_after=False)]},
    {"research": [_attempt(revisit_after=0)]},
    {"research": [_attempt(revisit_after="")]},
    {"bulletin_status": "absent"}, {"body": 7}, {"invented": "field"},
    {"fetch_gap": "solutio"}, {"fetch_gap": {"kind": "Solutio 403", "seen": "2026-10-21",
                                            "note": "403"}},
    {"fetch_gap": {"kind": "solutio-file-403", "seen": "2026-10-21"}},
    {"fetch_gap": {"kind": "solutio-file-403", "seen": "2026-10-21", "note": "403",
                   "url": "ftp://example.org"}},
    {"fetch_gap": {"kind": "solutio-file-403", "seen": "2026-10-21", "note": "403",
                   "invented": 1}},
    {"publication_reviews": [{"parish": "missing", "decision": "separate",
                              "evidence": EVIDENCE}]},
])
def test_bad_patch_is_rejected_before_file_replacement(root, patch):
    _write(create=True)
    path = root / "parishes/anne.md"
    before = path.read_bytes()
    with pytest.raises(DioceseError):
        _write(payload=patch)
    assert path.read_bytes() == before


def test_creation_and_identity_must_be_explicit(root):
    with pytest.raises(DioceseError, match="no parish"):
        _write()
    _write(create=True)
    with pytest.raises(DioceseError, match="already exists"):
        _write(create=True)
    with pytest.raises(DioceseError, match="slug"):
        _write(slug="../outside", create=True)
    assert not (root / "outside.md").exists()


def test_atomic_replace_failure_leaves_old_file_and_cleans_temp(root, monkeypatch):
    _write(create=True)
    path = root / "parishes/anne.md"
    before = path.read_bytes()

    def fail(*_):
        raise OSError("disk refused replace")

    monkeypatch.setattr(Path, "replace", fail)
    with pytest.raises(OSError, match="disk refused"):
        _write(payload={"name": "New name"})
    assert path.read_bytes() == before
    assert sorted(p.name for p in path.parent.iterdir()) == [".gitkeep", "anne.md"]


def test_cli_prints_one_json_document_and_diagnostics_on_stderr(root, monkeypatch, capsys):
    handler = cli.HANDLERS["write"]

    def noisy(args):
        print("browser diagnostic")
        return handler(args)

    monkeypatch.setitem(cli.HANDLERS, "write", noisy)
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(_payload())))
    assert main(["diocese", "write", "test", "parish", "anne", "--file", "-", "--create"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["slug"] == "anne"
    assert "browser diagnostic" in captured.err


@pytest.mark.parametrize("text", ['{broken', '[]', '{"name": NaN}'])
def test_cli_rejects_bad_json_without_output_or_changes(root, monkeypatch, capsys, text):
    monkeypatch.setattr("sys.stdin", io.StringIO(text))
    assert main(["diocese", "write", "test", "parish", "anne", "--file", "-", "--create"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and "Error:" in captured.err and "Traceback" not in captured.err
    assert not list((root / "parishes").glob("*.md"))


def test_todo_separates_dependency_triggers_and_scheduled_research(root):
    _write(payload={**_payload(), "bulletin_status": "unsupported-format", "research": [
        _attempt(),
        _attempt(method="publisher", outcome="not-published", revisit_after="2026-11-22"),
        _attempt(method="search", outcome="not-found", revisit_after="2026-10-22"),
    ]}, create=True)
    result = report.todo("test")
    assert result["research_summary"] == {"due": 1, "scheduled": 1, "waiting-for-trigger": 1}
    assert not result["revisit_now"]  # a format dependency is not another immediate crawl
    attempts = records.load("test").of(records.PARISH)["anne"]["research"]
    _write(payload={"research": [*attempts, _attempt(checked="2026-10-22", outcome="found")]})
    result = report.todo("test")
    assert len(result["research_pending"]) == 2
    _write(payload={"bulletin_status": "available"})
    assert not report.todo("test")["research_pending"]


def test_rename_and_merge_preserve_research_and_peer_reviews(root):
    _write(create=True)
    _write("bede", {**_payload("St. Bede"), "research": [_attempt()]}, create=True)
    _write("cyr", _payload("St. Cyr"), create=True)
    _write("cyr", {"publication_reviews": [
        {"parish": "bede", "decision": "separate", "evidence": EVIDENCE},
    ]})
    records.rename_record("test", "parish", "bede", "bede-town")
    records.merge_parishes("test", ["bede-town"], "anne")
    d = records.load("test")
    assert d.of(records.PARISH)["anne"]["research"] == [_attempt()]
    assert d.of(records.PARISH)["cyr"]["publication_reviews"][0]["parish"] == "anne"


def test_merge_archives_evidence_of_retired_peer_review(root):
    _write(create=True)
    _write("bede", _payload("St. Bede"), create=True)
    unique = [{**EVIDENCE[0], "note": "Masthead names Anne and Bede together on page 2."}]
    _write(payload={"publication_reviews": [
        {"parish": "bede", "decision": "shared", "evidence": unique},
    ]})
    records.merge_parishes("test", ["bede"], "anne")
    record = records.load("test").of(records.PARISH)["anne"]
    assert unique[0] in record["evidence"]
    assert not record.get("publication_reviews")
    assert "Peer bede: shared" in record["body"]


def test_writer_can_clear_required_nullable_open_date(root):
    records.write_record("test", "open", "chapel", {
        "name": "Chapel", "revisit": "Confirm public access", "revisit_after": "2026-11-01",
        "evidence": EVIDENCE, "body": "Public access remains unknown.",
    }, create=True)
    records.write_record("test", "open", "chapel", {"revisit_after": None})
    assert records.load("test").of(records.OPEN)["chapel"]["revisit_after"] is None


def test_fetch_cli_passes_explicit_verification_options(monkeypatch, capsys):
    import pdf_extract.__main__ as entrypoint

    received = {}

    def check(**kwargs):
        received.update(kwargs)
        return {"counts": {}, "parishes": [], "verification_counts": {}}

    monkeypatch.setattr(entrypoint, "check_fetch", check)
    assert main(["fetch-check", "--parish", "anne", "--expected-identity", "St. Anne",
                 "--expected-issue-date", "2026-10-18", "--reference-date", "2026-10-21",
                 "--max-issue-age-days", "10", "--no-download"]) == 0
    assert received["expected_identity"] == "St. Anne"
    assert received["expected_issue_date"] == date(2026, 10, 18)
    assert received["reference_date"] == date(2026, 10, 21)
    assert received["max_issue_age_days"] == 10 and received["download"] is False
    assert json.loads(capsys.readouterr().out)["parishes"] == []


@pytest.mark.parametrize("option,value", [
    ("--max-issue-age-days", "-1"), ("--expected-identity", "..."),
])
def test_fetch_cli_bad_expectations_are_input_errors(option, value, capsys):
    assert main(["fetch-check", option, value]) == 1
    captured = capsys.readouterr()
    assert captured.out == "" and "Traceback" not in captured.err


def _gap(kind="solutio-file-403", **changes):
    return {"kind": kind, "seen": "2026-10-21", "url": "https://example.org/bulletin/7/file",
            "note": "Solutio /file links answer 403 to the fetcher.", **changes}


def test_fetch_gaps_are_written_listed_by_kind_and_cleared(root):
    _write("anne", {**_payload("St. Anne"), "fetch_gap": _gap()}, create=True)
    _write("bede", {**_payload("St. Bede"), "fetch_gap": _gap()}, create=True)
    _write("clare", {**_payload("St. Clare"), "fetch_gap": _gap("joomla-weblink-redirect")},
           create=True)
    _write("dunstan", _payload("St. Dunstan"), create=True)
    assert "fetch_gap" not in (root / "parishes/dunstan.md").read_text()

    out = report.gaps()
    assert out["total"] == 3
    assert [(k["kind"], k["parishes"]) for k in out["kinds"]] == [
        ("solutio-file-403", 2), ("joomla-weblink-redirect", 1)]
    assert [e["parish"] for e in out["kinds"][0]["entries"]] == ["anne", "bede"]
    assert report.gaps("test", "joomla-weblink-redirect")["total"] == 1
    assert [g["parish"] for g in report.todo("test")["fetch_gaps"]] == ["anne", "bede", "clare"]

    _write("anne", {"fetch_gap": None})
    assert "fetch_gap" not in (root / "parishes/anne.md").read_text()
    assert report.gaps("test", "solutio-file-403")["total"] == 1
    with pytest.raises(DioceseError):
        report.gaps("missing")

    # new_record (scripts, bulk adds) keeps the object rather than turning it into text
    records.new_record("test", "parish", {"name": "St. Edith", "fetch_gap": _gap(),
                                          "website": "https://example.org/edith"})
    assert records.load("test").of(records.PARISH)["st-edith"]["fetch_gap"] == _gap()
