"""Tests for the diocese exploration files and the `diocese` CLI."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from pdf_extract import dioceses
from pdf_extract.__main__ import main
from pdf_extract.dioceses import DioceseError
from pdf_extract.fetch import SUPPORTED_BULLETIN_PROVIDERS


@pytest.fixture()
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty dioceses dir next to a two-parish live dataset."""
    parishes = tmp_path / "parishes.csv"
    parishes.write_text(
        "slug,name,website,bulletin_provider,provider_id\n"
        "live-parish,Live Parish,https://live.org,ecatholic,\n",
        encoding="utf-8",
    )
    churches = tmp_path / "churches.csv"
    churches.write_text(
        "parish_id,slug,name,line1,line2,city,state,postal_code\n"
        "live-parish,st-live,St. Live Church,1 Main St,,Town,NY,14000\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(dioceses, "PARISHES_CSV_PATH", parishes)
    monkeypatch.setattr(dioceses, "CHURCHES_CSV_PATH", churches)
    monkeypatch.setattr(dioceses, "DIOCESES_DIR", tmp_path / "dioceses")
    dioceses.init_diocese("test", name="Diocese of Test", state="NY")
    return tmp_path / "dioceses"


def _add_parish(slug: str = "st-ann", **fields) -> dict:
    return dioceses.add_record("test", "parish", {
        "slug": slug, "name": "St. Ann Parish", "website": f"https://{slug}.org",
        "bulletin_provider": "ecatholic", "explanation": "Listed in the diocese directory.",
        "sources": ["https://diocese.example/parishes"], **fields,
    })


def _add_church(slug: str = "st-ann-church", parish: str = "st-ann", **fields) -> dict:
    return dioceses.add_record("test", "church", {
        "parish_id": parish, "slug": slug, "name": "St. Ann Church", "line1": "5 Elm St",
        "city": "Town", "state": "NY", "postal_code": "14001",
        "explanation": "Address from the parish site.", "sources": ["https://st-ann.org"],
        **fields,
    })


def test_init_creates_every_file(root: Path) -> None:
    files = sorted(p.name for p in (root / "test").iterdir())
    assert files == [
        "churches.json", "diocese.json", "not-churches.md", "not-parishes.md", "parishes.json",
    ]
    assert json.loads((root / "test" / "parishes.json").read_text()) == []
    with pytest.raises(DioceseError, match="already exists"):
        dioceses.init_diocese("test", name="Again")


def test_add_writes_typed_json_and_warns_about_gaps(root: Path) -> None:
    result = _add_parish()
    assert result["warnings"] == ["parish 'st-ann': no churches recorded"]

    result = _add_church(latitude="43.1", longitude="-77.5", name_verified="true")
    assert result["warnings"] == []
    stored = json.loads((root / "test" / "churches.json").read_text())
    assert stored[0]["latitude"] == 43.1
    assert stored[0]["name_verified"] is True
    assert stored[0]["address_verified"] is False
    assert list(stored[0]) == list(dioceses.CHURCH.fields)


def test_slug_defaults_to_slugified_name(root: Path) -> None:
    result = _add_parish(slug=None, name="St. Mary's / St. Joseph")
    assert result["parish"]["slug"] == "st-marys-st-joseph"


def test_add_refuses_new_errors_and_writes_nothing(root: Path) -> None:
    before = (root / "test" / "churches.json").read_text()
    with pytest.raises(DioceseError) as e:
        _add_church(slug="st-live", parish="missing", state="New York")
    message = str(e.value)
    assert "slug already used in" in message and "churches.csv" in message
    assert "parish_id 'missing' is not in parishes.json" in message
    assert "state must be a two-letter code" in message
    assert (root / "test" / "churches.json").read_text() == before


def test_explanation_is_required(root: Path) -> None:
    with pytest.raises(DioceseError, match="explanation is required"):
        _add_parish(explanation="  ")


def test_website_must_be_unique_across_live_data_and_dioceses(root: Path) -> None:
    with pytest.raises(DioceseError, match="already used by data"):
        _add_parish(website="http://www.live.org/")

    dioceses.init_diocese("other", name="Other Diocese")
    dioceses.add_record("other", "parish", {
        "slug": "elsewhere", "name": "Elsewhere", "website": "https://st-ann.org",
        "explanation": "x",
    })
    with pytest.raises(DioceseError, match="diocese 'other'"):
        _add_parish()


def test_unknown_bulletin_provider_is_refused(root: Path) -> None:
    with pytest.raises(DioceseError, match="bulletin_provider 'wordpress'"):
        _add_parish(bulletin_provider="wordpress")


def test_known_providers_cover_everything_fetch_supports() -> None:
    assert SUPPORTED_BULLETIN_PROVIDERS <= dioceses.KNOWN_BULLETIN_PROVIDERS


def test_edit_changes_only_given_fields(root: Path) -> None:
    _add_parish()
    result = dioceses.edit_record(
        "test", "parish", "st-ann", {"name": "Saint Ann", "website": None},
        append_explanation="Bulletin confirmed on eCatholic.",
        add_sources=["https://st-ann.org/bulletins"],
    )
    parish = result["parish"]
    assert parish["name"] == "Saint Ann"
    assert parish["website"] == "https://st-ann.org"
    assert parish["explanation"] == (
        "Listed in the diocese directory.\n\nBulletin confirmed on eCatholic."
    )
    assert parish["sources"] == [
        "https://diocese.example/parishes", "https://st-ann.org/bulletins",
    ]


def test_editing_is_not_blocked_by_an_unrelated_existing_error(root: Path) -> None:
    _add_parish()
    _add_church()
    # A hand edit leaves a broken church behind...
    path = root / "test" / "churches.json"
    rows = json.loads(path.read_text())
    rows.append({**rows[0], "slug": "orphan", "parish_id": "gone"})
    path.write_text(json.dumps(rows))
    # ...which does not stop an unrelated change, but still fails validation.
    dioceses.edit_record("test", "parish", "st-ann", {"name": "Saint Ann"})
    report = dioceses.validate("test")
    assert report["passed"] is False
    assert report["dioceses"]["test"]["errors"] == [
        "church 'orphan': parish_id 'gone' is not in parishes.json",
    ]


def test_renaming_a_parish_moves_its_churches(root: Path) -> None:
    _add_parish()
    _add_church()
    dioceses.edit_record("test", "parish", "st-ann", {}, new_slug="st-ann-town")
    churches = dioceses.list_records("test", "church")["records"]
    assert [c["parish_id"] for c in churches] == ["st-ann-town"]


def test_remove_parish_needs_cascade_when_it_has_churches(root: Path) -> None:
    _add_parish()
    _add_church()
    with pytest.raises(DioceseError, match="still has churches"):
        dioceses.remove_record("test", "parish", "st-ann")
    result = dioceses.remove_record("test", "parish", "st-ann", cascade=True)
    assert result["removed_churches"] == ["st-ann-church"]
    assert dioceses.list_records("test", "church")["count"] == 0


def test_exclusions_round_trip_through_markdown(root: Path) -> None:
    dioceses.add_record("test", "not-parish", {
        "name": "Campus Ministry Center", "website": "https://campus.example",
        "sources": ["https://a.example", "https://b.example"],
        "explanation": "Campus ministry, not a parish.\n\nSecond paragraph.",
    })
    path = root / "test" / "not-parishes.md"
    text = path.read_text()
    assert text.startswith("# Not parishes: Diocese of Test\n")
    assert "## Campus Ministry Center\n- **Slug:** campus-ministry-center\n" in text

    # A hand-edited preamble survives the next write.
    path.write_text(text.replace("Places found", "Hand-written intro. Places found"))
    dioceses.edit_record("test", "not-parish", "campus-ministry-center", {"address": "1 Quad"})
    text = path.read_text()
    assert "Hand-written intro." in text

    entry = dioceses.get_record("test", "not-parish", "campus-ministry-center")["not-parish"]
    assert entry["address"] == "1 Quad"
    assert entry["sources"] == ["https://a.example", "https://b.example"]
    assert entry["explanation"] == "Campus ministry, not a parish.\n\nSecond paragraph."
    assert entry["added"]


def test_a_slug_cannot_be_both_kept_and_excluded(root: Path) -> None:
    _add_parish()
    with pytest.raises(DioceseError, match="also listed in parishes.json"):
        dioceses.add_record("test", "not-parish", {
            "slug": "st-ann", "name": "St. Ann", "explanation": "Closed.",
        })


def test_adding_a_record_named_like_an_exclusion_warns(root: Path) -> None:
    dioceses.add_record("test", "not-parish", {
        "slug": "st-ann-old", "name": "St. Ann Parish", "explanation": "Merged away in 2010.",
    })
    warnings = _add_parish()["warnings"]
    assert any("same name as not-parish 'st-ann-old'" in w for w in warnings)


def test_search_spans_live_data_and_dioceses_and_normalizes_saint(root: Path) -> None:
    _add_parish()
    _add_church()
    dioceses.add_record("test", "not-church", {
        "name": "Old St. Ann Chapel", "explanation": "Closed in 2008.",
    })
    hits = dioceses.search("saint ann")["results"]
    assert [(h["diocese"], h["kind"], h["slug"]) for h in hits] == [
        ("test", "parish", "st-ann"),
        ("test", "church", "st-ann-church"),
        ("test", "not-church", "old-st-ann-chapel"),
    ]
    live = dioceses.search("St Live")["results"]
    assert [(h["diocese"], h["slug"]) for h in live] == [("live", "st-live")]
    only_excluded = dioceses.search("ann", kinds=["not-church"])["results"]
    assert [h["slug"] for h in only_excluded] == ["old-st-ann-chapel"]
    assert dioceses.search("ann", diocese="live")["count"] == 0


def test_export_writes_live_csv_columns(root: Path, tmp_path: Path) -> None:
    _add_parish()
    _add_church(latitude="43.1", longitude="-77.5")
    out = tmp_path / "out"
    dioceses.export_csv("test", out)
    with open(out / "parishes.csv", encoding="utf-8") as f:
        parishes = list(csv.DictReader(f))
    with open(out / "churches.csv", encoding="utf-8") as f:
        churches = list(csv.DictReader(f))
    assert list(parishes[0]) == ["slug", "name", "website", "bulletin_provider", "provider_id"]
    assert churches[0]["latitude"] == "43.1"
    assert churches[0]["name_verified"] == "false"
    assert "explanation" not in churches[0]


def test_export_refuses_a_diocese_with_errors(root: Path, tmp_path: Path) -> None:
    path = root / "test" / "parishes.json"
    path.write_text(json.dumps([{"slug": "Bad Slug", "name": "x", "website": "https://x.org"}]))
    with pytest.raises(DioceseError, match="fix these first"):
        dioceses.export_csv("test", tmp_path / "out")


def test_cli_add_then_validate(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([
        "diocese", "parish", "add", "test", "--name", "St. Ann Parish",
        "--website", "https://st-ann.org", "--explanation", "In the directory.",
        "--source", "https://diocese.example",
    ]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["parish"]["slug"] == "st-ann-parish"

    # Validation failures exit non-zero, bad input prints no traceback.
    assert main(["diocese", "church", "add", "test", "--name", "X", "--parish", "nope",
                 "--explanation", "x"]) == 1
    err = capsys.readouterr().err
    assert err.startswith("Error: refused") and "Traceback" not in err
    assert main(["diocese", "validate", "test"]) == 0


def test_committed_dioceses_validate() -> None:
    """Hand edits to data/dioceses/ must still pass `diocese validate`."""
    report = dioceses.validate()
    errors = {slug: r["errors"] for slug, r in report["dioceses"].items() if r["errors"]}
    assert not errors
