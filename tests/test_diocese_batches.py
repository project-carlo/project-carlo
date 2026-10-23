"""Scout plans account for every local roster entry exactly once, including exclusions."""

import copy
import json

import pytest

from pdf_extract import storage
from pdf_extract.__main__ import main
from pdf_extract.dioceses import batches, records, rosters, web


@pytest.fixture
def plan(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DIOCESES_DIR", tmp_path / "dioceses")
    records.init_diocese("test", name="Test")
    for name, ids in (("directory", ["anne", "bede"]), ("gcatholic", ["123", "999"])):
        rosters.save_roster("test", name, [{"id": i, "name": i} for i in ids],
                           title=name, url="https://example.org", command="fixture")
    monkeypatch.setattr(web, "fetch", lambda *a, **k: pytest.fail("must stay offline"))
    return {"version": 1, "diocese": "test", "first_batch": "town",
            "batches": [{"id": "town", "name": "Town", "why": "One shared pastor",
                         "entries": ["directory:anne", "directory:bede", "gcatholic:123"]}],
            "excluded": [{"ref": "gcatholic:999", "reason": "Outside the diocese"}]}


def save(plan, path=None):
    path = path or records.diocese_dir("test") / "batches.json"
    path.write_text(json.dumps(plan), encoding="utf-8")
    return path


def test_complete_plan_passes_cli_and_is_read_only(plan, capsys):
    path = save(plan)
    before = {p: p.read_bytes() for p in path.parent.rglob("*") if p.is_file()}
    assert main(["diocese", "batches", "validate", "test"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["passed"]
    assert result["counts"] == {"roster_entries": 4, "assigned": 3, "excluded": 1, "batches": 1}
    assert result["first_batch"] == "town"
    assert {p: p.read_bytes() for p in path.parent.rglob("*") if p.is_file()} == before


def test_missing_unknown_and_duplicate_refs_fail_with_locations(plan, tmp_path, capsys):
    plan["batches"][0]["entries"] = ["directory:anne", "directory:anne", "gcatholic:missing"]
    plan["excluded"].append({"ref": "directory:anne", "reason": "Duplicate of another roster"})
    path = save(plan, tmp_path / "custom.json")
    assert main(["diocese", "batches", "validate", "test", "--file", str(path)]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["missing"] == ["directory:bede", "gcatholic:123"]
    assert result["unknown"] == ["gcatholic:missing"]
    assert result["duplicates"] == {"directory:anne": [
        "batches[1].entries[1]", "batches[1].entries[2]", "excluded[2].ref",
    ]}


@pytest.mark.parametrize("change,expected", [
    ({"version": True}, "version must be 1"),
    ({"diocese": "other"}, "diocese must be 'test'"),
    ({"first_batch": "missing"}, "first_batch must name"),
    ({"batches": []}, "batches must be a nonempty list"),
    ({"batches": [None]}, "batches[1] must be an object"),
    ({"excluded": [{"ref": "gcatholic:999", "reason": " "}]}, "reason must be nonempty"),
    ({"excluded": [{"ref": "gcatholic:999", "reason": "Outside", "typo": True}]}, "unknown field"),
    ({"excluded": None}, "excluded must be a list"),
])
def test_invalid_manifest_shapes_are_diagnostics(plan, change, expected):
    plan.update(change)
    result = batches.validate("test", save(plan))
    assert not result["passed"]
    assert any(expected in error for error in result["errors"])


def test_batch_ids_and_exclusions_are_unique_and_batches_need_a_reason(plan):
    second = copy.deepcopy(plan["batches"][0])
    second["why"] = ""
    plan["batches"].append(second)
    plan["excluded"] *= 2
    result = batches.validate("test", save(plan))
    assert any("duplicate batch id" in error for error in result["errors"])
    assert any("why must be nonempty" in error for error in result["errors"])
    assert "gcatholic:999" in result["duplicates"]


def test_refreshing_roster_invalidates_a_previously_complete_plan(plan):
    path = save(plan)
    assert batches.validate("test", path)["passed"]
    rosters.save_roster("test", "missions", [{"id": "new", "name": "New mission"}],
                       title="Missions", url="https://example.org", command="fixture")
    assert batches.validate("test", path)["missing"] == ["missions:new"]


@pytest.mark.parametrize("contents", ["{broken", "null", "[]"])
def test_bad_json_or_top_level_type_is_a_clean_cli_failure(plan, capsys, contents):
    path = save(plan)
    path.write_text(contents)
    assert main(["diocese", "batches", "validate", "test"]) == 1
    output = capsys.readouterr()
    assert "Traceback" not in output.err
    if contents != "{broken":
        assert not json.loads(output.out)["passed"]


def test_no_rosters_and_malformed_roster_entries_cannot_pass(plan):
    path = save(plan)
    folder = records.diocese_dir("test") / "rosters"
    for roster in folder.glob("*.json"):
        roster.unlink()
    assert any("no roster entries" in error for error in batches.validate("test", path)["errors"])
    (folder / "bad.json").write_text(json.dumps({"entries": [None, {"id": ""},
                                                              {"id": "1"}, {"id": "1"}]}))
    errors = batches.validate("test", path)["errors"]
    assert sum("nonempty id is required" in error for error in errors) == 2
    assert any("duplicate id" in error for error in errors)
