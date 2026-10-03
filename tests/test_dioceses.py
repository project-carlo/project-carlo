"""Tests for the diocese exploration files and the `diocese` command."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from pdf_extract import storage
from pdf_extract.__main__ import main
from pdf_extract.dioceses import records, report, rosters, web
from pdf_extract.dioceses.records import DioceseError
from pdf_extract.fetch import SUPPORTED_BULLETIN_PROVIDERS

EVIDENCE = [{"url": "https://example.org/bulletin.pdf", "seen": "2026-09-06",
             "quote": "St. Ann", "note": "masthead"}]


@pytest.fixture()
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """An empty diocese 'test' next to a one-parish live dataset."""
    parishes = tmp_path / "parishes.csv"
    parishes.write_text(
        "slug,name,website,bulletin_provider,provider_id\n"
        "live-parish,Live Parish,https://live.org,ecatholic,\n",
        encoding="utf-8",
    )
    churches = tmp_path / "churches.csv"
    churches.write_text(
        ",".join(records.CHURCH_CSV_FIELDS) + "\n"
        "live-parish,st-live,St. Live Church,1 Main St,,Town,NY,14000,true,true,43.1,-77.1\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(storage, "PARISHES_CSV_PATH", parishes)
    monkeypatch.setattr(storage, "CHURCHES_CSV_PATH", churches)
    monkeypatch.setattr(storage, "DEFAULT_DB_PATH", tmp_path / "parish_events.db")
    monkeypatch.setattr(storage, "DIOCESES_DIR", tmp_path / "dioceses")
    records.init_diocese("test", name="Diocese of Test", state="NY")
    return tmp_path / "dioceses" / "test"


def _parish(slug: str = "st-ann", **fields) -> dict:
    return records.new_record("test", "parish", {
        "name": "St. Ann Parish", "website": f"https://{slug}.org",
        "bulletin_provider": "ecatholic", "evidence": EVIDENCE, **fields,
    }, slug=slug, body="## Publisher\n\nThe masthead names St. Ann alone.")


def _church(slug: str = "st-ann-town", parish: str = "st-ann", **fields) -> dict:
    return records.new_record("test", "church", {
        "parish": parish, "name": "St. Ann Church", "line1": "5 Elm Street", "city": "Town",
        "state": "NY", "postal_code": "14001", "evidence": EVIDENCE, **fields,
    }, slug=slug, body="## Holds Mass\n\nSunday 9 am in the 2026-09-06 bulletin.")


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _live(name: str) -> list[dict[str, str]]:
    with open(getattr(storage, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ── Files ───────────────────────────────────────────────────────────────────
def test_init_creates_the_layout(root: Path) -> None:
    assert sorted(p.name for p in root.iterdir()) == [
        "churches", "diocese.md", "excluded", "open", "parishes", "rosters",
    ]
    assert records.load_meta("test")["status"] == "exploring"
    with pytest.raises(DioceseError, match="already exists"):
        records.init_diocese("test", name="Again")


def test_new_record_writes_frontmatter_and_the_template(root: Path) -> None:
    result = records.new_record("test", "parish", {"name": "St. Ann Parish",
                                                   "website": "https://st-ann.org"})
    assert result["created"] == "parishes/st-ann-parish.md"
    text = (root / "parishes" / "st-ann-parish.md").read_text()
    assert text.startswith("---\nname: St. Ann Parish\nwebsite: https://st-ann.org\n")
    assert "## Publisher\n\nTODO:" in text
    assert any("TODO placeholders" in w for w in result["warnings"])
    assert any("no evidence" in w for w in result["warnings"])


def test_church_slug_is_dedication_and_town(root: Path) -> None:
    _parish()
    result = records.new_record("test", "church", {
        "parish": "st-ann", "name": "St. Mary's Church", "city": "East Aurora"})
    assert result["slug"] == "st-marys-east-aurora"
    assert records.church_slug("Our Lady of Victory Basilica", "Lackawanna") == (
        "our-lady-of-victory-basilica-lackawanna")


def test_hand_written_files_load_with_dates_as_text(root: Path) -> None:
    _parish()
    _write(root / "churches" / "st-ann-town.md", """---
parish: st-ann
name: St. Ann Church
line1: 5 Elm Street
city: Town
state: NY
postal_code: '14001'
latitude: 43.2
longitude: -77.2
coordinates_from: osm-node
evidence:
- url: https://example.org/b.pdf
  seen: 2026-09-06
  quote: 'Sat. 4:00 pm'
my_note: kept
---

## Holds Mass

Sunday 9 am.
""")
    d = records.load("test")
    church = d.of(records.CHURCH)["st-ann-town"]
    assert church["evidence"][0]["seen"] == "2026-09-06"
    assert church["body"].startswith("## Holds Mass")
    rendered = records.render(records.CHURCH, church)
    assert "seen: 2026-09-06\n" in rendered and "my_note: kept" in rendered
    p = records.problems(d)
    assert not p.errors
    assert "church 'st-ann-town': unknown field 'my_note'" in p.warnings


def test_an_unquoted_zip_and_a_broken_file_are_reported_not_fatal(root: Path) -> None:
    _parish()
    _write(root / "churches" / "a-town.md",
           "---\nparish: st-ann\nname: A\npostal_code: 01234\n---\n\nText\n")
    _write(root / "churches" / "b-town.md", "---\nname: [unclosed\n---\n\nText\n")
    result = records.validate("test")
    errors = result["dioceses"]["test"]["errors"]
    assert not result["passed"]
    assert any("postal_code must be text" in e and "quote it" in e for e in errors)
    assert any("b-town.md: frontmatter is not valid YAML" in e for e in errors)
    # a new file can't miss references, so it goes ahead and names the broken one
    created = _church()
    assert any("b-town.md" in w for w in created["warnings"])
    with pytest.raises(DioceseError, match="already exists"):
        _church(slug="b-town")
    # moving references around could miss the ones in the broken file
    with pytest.raises(DioceseError, match="do not parse"):
        records.exclude_church("test", "st-ann-town", reason="closed")


# ── Checks ──────────────────────────────────────────────────────────────────
def test_collisions_with_live_data_and_other_dioceses_are_refused(root: Path) -> None:
    records.init_diocese("other", name="Other Diocese")
    records.new_record("other", "parish", {"name": "X", "website": "https://x.org"}, slug="x")
    with pytest.raises(DioceseError, match="data/parishes.csv"):
        _parish(slug="live-parish")
    with pytest.raises(DioceseError, match="website already used by data/parishes.csv"):
        _parish(website="https://www.live.org/")
    with pytest.raises(DioceseError, match="diocese 'other'"):
        _parish(slug="x")
    _parish()
    with pytest.raises(DioceseError, match="data/churches.csv"):
        _church(slug="st-live")
    assert not (root / "churches" / "st-live.md").exists()


def test_two_parishes_publishing_one_bulletin_is_an_error(root: Path) -> None:
    _parish(publication=["po-container:14/0434"])
    with pytest.raises(DioceseError, match="both publish po-container:14/0434"):
        _parish(slug="st-bede", publication=["po-container:14/0434"])


def test_a_truncated_lpi_id_is_rejected() -> None:
    assert records.publication_problem("lpi:0018000000Qbyz4AAB") is None
    assert "truncated" in records.publication_problem("lpi:00180000")
    assert "scheme" in records.publication_problem("bulletin:1")


def test_bulletin_provider_values_cover_what_fetch_supports() -> None:
    assert SUPPORTED_BULLETIN_PROVIDERS <= records.KNOWN_BULLETIN_PROVIDERS


def test_an_other_parish_provider_id_must_be_a_fetch_recipe(root: Path) -> None:
    _parish("st-ann", bulletin_provider="other", provider_id="page-pdfs https://st-ann.org/b")
    assert not records.validate("test")["dioceses"]["test"]["errors"]
    with pytest.raises(DioceseError, match=(
        r"parish 'st-bede': provider_id is not a fetch recipe: "
        r"Unknown collector 'newest-pdf'; expected one of drive-folder, "
    )):
        _parish("st-bede", bulletin_provider="other", provider_id="newest-pdf")


# ── Operations ──────────────────────────────────────────────────────────────
def test_merge_folds_rows_into_one_and_keeps_what_was_known(root: Path) -> None:
    _parish("family", publication=["po-container:14/0948"])
    _church("a-town", parish="family")
    _parish("st-bede", bulletin_provider="parishes_online", provider_id="st-bede-org",
            publication=["po-org:st-bede-org"])
    _church("b-town", parish="st-bede")
    result = records.merge_parishes("test", ["st-bede"], "family", note="One masthead.")
    assert result["moved_churches"] == ["b-town"]
    assert not (root / "parishes" / "st-bede.md").exists()
    d = records.load("test")
    family = d.of(records.PARISH)["family"]
    assert family["replaces"] == ["st-bede"]
    assert family["publication"] == ["po-container:14/0948", "po-org:st-bede-org"]
    assert family["provider_id"] == "st-bede-org"
    assert "## Merged in: st-bede" in family["body"] and "One masthead." in family["body"]
    assert "### Publisher" in family["body"]  # the old explanation, one heading level down
    assert d.of(records.CHURCH)["b-town"]["parish"] == "family"


def test_rename_moves_references(root: Path) -> None:
    _parish()
    _church()
    records.rename_record("test", "parish", "st-ann", "st-ann-town")
    d = records.load("test")
    assert d.of(records.CHURCH)["st-ann-town"]["parish"] == "st-ann-town"
    assert "replaces" not in d.of(records.PARISH)["st-ann-town"]  # never promoted


def test_exclude_turns_a_church_into_an_exclusion(root: Path) -> None:
    _parish()
    _church(roster=["gcatholic:1"])
    records.exclude_church("test", "st-ann-town", reason="closed", last_mass="2025-05-18")
    excluded = records.load("test").of(records.EXCLUDED)["st-ann-town"]
    assert excluded["reason"] == "closed" and excluded["last_mass"] == "2025-05-18"
    assert excluded["line1"] == "5 Elm Street" and excluded["roster"] == ["gcatholic:1"]
    assert "## When it was a church row" in excluded["body"]
    assert not (root / "churches" / "st-ann-town.md").exists()


def test_search_spans_dioceses_and_live_rows(root: Path) -> None:
    _parish()
    _church()
    hits = records.search("saint ann")["results"]
    assert {(h["diocese"], h["kind"], h["slug"]) for h in hits} == {
        ("test", "parish", "st-ann"), ("test", "church", "st-ann-town")}
    assert records.search("st live", diocese="live")["results"][0]["slug"] == "st-live"


# ── Rosters and coverage ────────────────────────────────────────────────────
def _roster(entries: list[dict]) -> None:
    rosters.save_roster("test", "feed", entries, title="Feed", url="https://d.org/finder",
                        command="test")


def test_coverage_matches_links_and_reports(root: Path) -> None:
    _parish()
    _church()                                                     # 5 Elm Street, Town
    _church("st-joseph-town", name="St. Joseph", line1="9 Oak Road")
    records.new_record("test", "excluded", {"name": "St. Hedwig", "reason": "closed",
                                            "city": "Village", "evidence": EVIDENCE},
                       slug="st-hedwig-village", body="Closed.")
    _roster([
        {"id": "1", "name": "Saint Ann", "line1": "5 Elm St.", "city": "Town"},       # address
        {"id": "2", "name": "Saint Joseph Church", "line1": "", "city": "Town"},       # name
        {"id": "3", "name": "St. Hedwig", "city": "Village"},                          # excluded
        {"id": "4", "name": "St. Hedwig", "city": "Village"},                          # repeat
        {"id": "5", "name": "Holy Cross", "line1": "1 New Rd", "city": "Elsewhere",
         "group": "Family #1"},
        {"id": "6", "name": "Other", "line1": "9 Oak Rd", "city": "Hamlet"},          # street
    ])
    cov = report.coverage("test")["rosters"][0]
    assert cov["counts"] == {"church": 3, "excluded": 1, "open": 0, "repeat": 1,
                             "unmatched": 1}
    assert cov["accounted_for"] == "4/5 (80%)"
    assert cov["unmatched"] == {"Family #1": [
        {"ref": "feed:5", "name": "Holy Cross", "address": "1 New Rd, Elsewhere"}]}
    assert cov["street_only_matches"][0]["ref"] == "feed:6"

    linked = report.coverage("test", link=True)["linked"]
    assert sorted(linked["written"]) == ["churches/st-ann-town.md", "churches/st-joseph-town.md",
                                         "excluded/st-hedwig-village.md"]
    d = records.load("test")
    assert d.of(records.CHURCH)["st-ann-town"]["roster"] == ["feed:1"]
    assert d.of(records.CHURCH)["st-joseph-town"]["roster"] == ["feed:2"]  # not feed:6


def test_city_aliases_catch_hamlet_names(root: Path) -> None:
    _parish()
    _church()
    meta = root / "diocese.md"
    _write(meta, meta.read_text().replace("status: exploring",
                                          "status: exploring\ncity_aliases:\n  Hamlet: Town"))
    _roster([{"id": "1", "name": "St. Ann", "city": "Hamlet"}])
    assert report.coverage("test")["rosters"][0]["counts"]["church"] == 1


def test_roster_refetch_reports_changes(root: Path) -> None:
    _roster([{"id": "1", "name": "A", "city": "X"}, {"id": "2", "name": "B", "city": "Y"}])
    result = rosters.save_roster("test", "feed", [{"id": "2", "name": "B", "city": "Y"},
                                                  {"id": "3", "name": "C", "city": "Z"}],
                                 title="Feed", url="", command="test")
    assert result["changes"]["added"] == ["3: C (Z)"]
    assert result["changes"]["removed"] == ["1: A (X)"]


def test_import_roster_accepts_loose_keys(root: Path, tmp_path: Path) -> None:
    src = tmp_path / "families.json"
    src.write_text(json.dumps([{"Site": "St. Mary", "Town": "Pavilion", "Family": "#14"}]))
    rosters.import_roster("test", "families", src)
    entry = rosters.load_roster("test", "families")["entries"][0]
    assert (entry["name"], entry["city"], entry["group"], entry["id"]) == (
        "St. Mary", "Pavilion", "#14", "st-mary-pavilion")


def test_audit_sorts_groups_by_what_is_recorded(root: Path) -> None:
    _parish("a", group="Family #1", publication=["po-container:1/1"])
    _parish("b", group="Family #1", publication=["po-container:1/2"])
    _parish("c", group="Family #2", publication=["po-container:1/3"])
    _parish("d", group="Family #2")
    groups = {g["group"]: g["verdict"] for g in report.audit("test")["groups_spanning_rows"]}
    assert groups["group: Family #1"].startswith("separate")
    assert groups["group: Family #2"].startswith("unknown")


def test_todo_lists_revisits_and_gaps(root: Path) -> None:
    _parish(revisit="Read the bulletin", revisit_after="2000-01-01")
    todo = report.todo("test")
    assert todo["revisit_now"][0]["record"] == "parishes/st-ann.md"
    assert "parish 'st-ann': no churches" in todo["incomplete"]


# ── Export and promote ──────────────────────────────────────────────────────
def test_export_refuses_incomplete_records(root: Path, tmp_path: Path) -> None:
    records.new_record("test", "parish", {"name": "Draft", "website": "https://d.org"})
    with pytest.raises(DioceseError, match="TODO placeholders"):
        records.export_csv("test", tmp_path / "out")


def test_promote_adds_updates_and_retires_live_rows(root: Path) -> None:
    _parish()
    _church()
    report_ = records.promote("test", dry_run=True)
    assert report_["parishes"]["added"] == ["st-ann"]
    assert [r["slug"] for r in _live("PARISHES_CSV_PATH")] == ["live-parish"]

    records.promote("test")
    assert [r["slug"] for r in _live("PARISHES_CSV_PATH")] == ["live-parish", "st-ann"]
    d = records.load("test")
    assert d.of(records.PARISH)["st-ann"]["promoted"] == records.today()
    assert records.load_meta("test")["status"] == "promoted"
    assert not records.validate("test")["dioceses"]["test"]["errors"]  # owns its live rows

    # The geocode stage fills coordinates in the live CSV; promote keeps them.
    rows = _live("CHURCHES_CSV_PATH")
    rows[1].update(latitude="43.5", longitude="-77.5")
    with open(storage.CHURCHES_CSV_PATH, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=records.CHURCH_CSV_FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    result = records.promote("test")
    assert result["churches"]["kept_live_values"] == {"st-ann-town": ["latitude", "longitude"]}
    church = records.load("test").of(records.CHURCH)["st-ann-town"]
    assert (church["latitude"], church["coordinates_from"]) == (43.5, "geocode-stage")

    # A later merge and a closure retire live rows.
    _parish("family", publication=["po-container:1/9"])
    records.merge_parishes("test", ["st-ann"], "family")
    records.exclude_church("test", "st-ann-town", reason="closed",
                           explanation="## Why it is excluded\n\nLast Mass announced.")
    _church("st-bede-town", parish="family")
    result = records.promote("test")
    assert result["parishes"]["removed"] == ["st-ann"]
    assert result["churches"]["removed"] == ["st-ann-town"]
    assert [r["slug"] for r in _live("PARISHES_CSV_PATH")] == ["live-parish", "family"]
    assert [r["slug"] for r in _live("CHURCHES_CSV_PATH")] == ["st-live", "st-bede-town"]


# ── Web helpers (no network) ────────────────────────────────────────────────
def test_decode_plus_code_matches_the_reference() -> None:
    lat, lng = rosters.decode_plus_code("849VCWC8+R9")
    assert abs(lat - 37.4219) < 0.0002 and abs(lng + 122.0841) < 0.0002
    assert rosters.decode_plus_code("CWC8+R9") is None


def test_gcatholic_pages_parse() -> None:
    index = (
        '<tr id="L1"><td><span class="znote">Forestport</span></td><td>'
        '<a href="../usa-02/17930" title="Mission of St. Patrick"><img></a> '
        '<a href="../usa-02/17930" class="chw">St. Patrick</a><br>'
        '<span class="znote">Christ our Hope Parish</span></td></tr>'
        '<tr id="L2"><td><span class="znote">Utica</span></td><td>'
        '<a href="../usa-02/16547" title="Church of St. Basil"></a> '
        '<a href="../usa-02/16547" class="che">St. Basil</a><span class="zrite"> (</span>'
        '<a href="../../dioceses/rite-GM" class="zrite">Greek-Melkite</a></td></tr>'
    )
    rows = rosters.parse_gcatholic_index(index)
    assert rows[0] | {} == {"id": "17930", "path": "usa-02/17930", "name": "St. Patrick",
                            "index_city": "Forestport", "group": "Christ our Hope Parish",
                            "kind": "Mission"}
    assert rows[1]["rite"] == "Greek-Melkite"
    detail = rosters.parse_gcatholic_detail(
        "<div>Type: Church Rite: Roman (Latin) History: 1914 Location: 87J67GR9+RC "
        "Address: 34 S Main St., Bainbridge, New York 13733-1215 Country: USA "
        "Telephone: +1 (607) 967-4481 GCatholic Church ID: 18006</div>")
    assert detail["line1"] == "34 S Main St." and detail["state"] == "NY"
    assert detail["postal_code"] == "13733" and detail["latitude"] == pytest.approx(42.292, 1e-3)


def test_parse_address_ignores_direction_marks() -> None:
    # Albany's GCatholic pages end some addresses with U+200E.
    assert rosters.parse_address("NY 23A, Hunter, New York 12450 \u200e") == {
        "line1": "NY 23A", "city": "Hunter", "state": "NY", "postal_code": "12450"}
    assert rosters.parse_address("27 Harper St., Stamford, New York 1890") == {
        "line1": "27 Harper St.", "city": "Stamford", "state": "NY", "postal_code": ""}


def test_find_publications_keeps_lpi_ids_whole() -> None:
    page = ('<iframe src="https://parishesonline.com/publicationWidget?type=bulletin&'
            'id=0018000000Qbyz4AAB"></iframe>'
            '<a href="https://container.parishesonline.com/bulletins/14/0434/20260906B.pdf">'
            '<a href="https://files.ecatholic.com/35834/bulletins/20260906.pdf">')
    assert web.find_publications(page) == [
        "lpi:0018000000Qbyz4AAB", "po-container:14/0434", "ecatholic:35834"]


def test_find_publications_reads_containers_from_find_links() -> None:
    page = ('<a href="https://parishesonline.com/find/catholic-community-of-st-stephen-st-patrick'
            '/bulletin/file/03-1424-20260927B.pdf">'
            '<a href="https://container.parishesonline.com/bulletins/03/1424/20260920B.pdf">')
    assert web.find_publications(page) == ["po-container:03/1424"]


def test_spam_terms_match_whole_words_only() -> None:
    wix = '{"specs.DisplayCheckoutErrorModalsForExpressButtons": true} St. Mary Parish'
    assert web.spam_terms(wix) == []
    assert web.spam_terms("Best Slot Gacor and casino bonuses") == ["casino", "slot gacor"]
    wix = '{"specs.stores.displayCheckoutErrorModalsForExpressButtons":"true"}'
    assert web.spam_terms(wix + " Judicial Conference policy prohibits it") == []
    assert web.spam_terms("Situs judi slot online terpercaya") == ["judi", "slot online"]


def test_one_passing_spam_term_on_a_parish_page_is_not_a_squat() -> None:
    news = "Parish news: the Hall of Fame dinner is at Rivers Casino & Resort. Mass times"
    assert web.spam_terms(news) == ["casino"] and not web.looks_squatted(news)
    assert web.looks_squatted("Casino bonus! Best casino games, casino online")
    assert web.looks_squatted("Situs judi slot online terpercaya, parish")
    assert web.looks_squatted("Play at our casino tonight")


def test_a_pdf_that_does_not_parse_is_an_error_not_a_crash(monkeypatch) -> None:
    broken = web.Response("u", 200, "u", "application/pdf", b"%PDF-1.7\n1 0 obj")
    monkeypatch.setattr(web, "fetch", lambda url, **kw: broken)
    assert web.pdf_text("https://example.org/x.pdf")["error"].startswith("could not read")


def test_quote_found_tolerates_layout_and_elisions() -> None:
    text = "Mass Schedule\n  Weekend: Sat. 5:10 pm\n   Sun. 7:30 am, 9:45 am\nSt. Bernard’s"
    assert web.quote_found("Weekend: Sat. 5:10 pm … Sun. 7:30 am", text)
    assert web.quote_found("St. Bernard's", text)
    assert not web.quote_found("Sun. 7:30 am … Weekend", text)
    # spacing around punctuation differs between PDF extractions
    assert web.quote_found("Mass- Fr.Zach(CTK)", "8:30 AM Mass - Fr. Zach (CTK)")


def test_new_exclusion_from_a_roster_drops_coordinates(root: Path, tmp_path: Path) -> None:
    src = tmp_path / "directory.json"
    src.write_text(json.dumps([{"id": "7", "name": "St. Paul (Closed)", "city": "Fabius",
                                "state": "NY", "latitude": 42.8, "longitude": -75.9,
                                "url": "https://example.org/finder"}]))
    rosters.import_roster("test", "directory", src)
    assert main(["diocese", "new", "excluded", "test", "--reason", "closed",
                 "--from", "directory:7"]) == 0
    [path] = (root / "excluded").glob("*.md")
    text = path.read_text(encoding="utf-8")
    assert "directory:7" in text and "latitude" not in text


# ── CLI and the committed data ──────────────────────────────────────────────
def test_cli_prints_errors_without_a_traceback(root: Path, capsys) -> None:
    assert main(["diocese", "new", "church", "test", "--name", "X", "--parish", "nope"]) == 1
    err = capsys.readouterr().err
    assert "refused, nothing was written" in err and "Traceback" not in err
    assert main(["diocese", "validate", "test"]) == 0


def test_committed_dioceses_have_no_errors() -> None:
    result = records.validate()
    assert result["passed"], json.dumps(
        {d: r["errors"] for d, r in result["dioceses"].items()}, indent=2)


def test_rows_losing_events_come_from_the_database(root: Path, tmp_path: Path) -> None:
    import sqlite3

    conn = sqlite3.connect(tmp_path / "parish_events.db")
    conn.executescript(
        "CREATE TABLE parish (id INTEGER PRIMARY KEY, slug TEXT);"
        "CREATE TABLE bulletin (id INTEGER PRIMARY KEY, parish_id INTEGER);"
        "CREATE TABLE church (id INTEGER PRIMARY KEY, slug TEXT);"
        "CREATE TABLE event (id INTEGER PRIMARY KEY, church_id INTEGER, bulletin_id INTEGER);"
        "INSERT INTO parish VALUES (1, 'kept'), (2, 'retired');"
        "INSERT INTO bulletin VALUES (10, 1), (20, 2);"
        "INSERT INTO church VALUES (1, 'st-live'), (2, 'st-quiet'), (3, 'st-moved');"
        # st-moved's events come from the retired parish's bulletin: they go with it.
        "INSERT INTO event VALUES (1, 1, 10), (2, 3, 20);"
    )
    conn.close()

    assert records._referenced_by_events(["st-live", "st-quiet", "st-gone"]) == ["st-live"]
    assert records._referenced_by_events([], ["retired"]) == ["st-moved"]
    assert records._referenced_by_events([], []) == []
