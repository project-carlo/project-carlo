"""Source seeds (docs/source-schedules-plan.md): a `website_schedule` parish, with no
bulletin, seeded from captures of its own website or Facebook page."""

from __future__ import annotations

import csv
import http.client
import io
import json
import threading
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from PIL import Image

from pdf_extract import fetch
from pdf_extract.__main__ import main
from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, get_store, set_store
from pdf_extract.db import migrate, seed_reference_data
from pdf_extract.extract_frontend_db import checked_on, extract, read_snapshot
from pdf_extract.labeling.server import LabelerApp, make_server
from pdf_extract.model import facebook_page, sha256_text
from pdf_extract.report import render_seeds, render_source_due
from pdf_extract.seeding import captures as seed_captures
from pdf_extract.seeding import cli as seed_cli
from pdf_extract.seeding.captures import capture_page, linked_facebook_pages, screenshot_key
from pdf_extract.seeding.checks import check_seed
from pdf_extract.seeding.files import (
    APPROVED,
    READY,
    add_months,
    capture_text_path,
    new_seed,
    parse_capture_document,
    read_seed,
    screenshot_path,
    seed_digest,
    seed_path,
    validate_seed,
    write_seed_file,
)
from pdf_extract.seeding.finalize import finalize_seed
from pdf_extract.seeding.loader import due_source_seeds, load_approved_seeds
from pdf_extract.seeding.page_images import fits
from pdf_extract.seeding.queries import SeedContext, SeedError
from pdf_extract.seeding.review import save_reviewed_seed
from pdf_extract.seeding.slots import parse_source
from pdf_extract.storage import connect_db, insert_bulletin, save_processed_bulletin

PARISH = "st-rita-web"
CHURCH = "st-rita-web-webster"
BULLETIN_PARISH = "st-luke-bulletin"
SITE = "https://stritaweb.org"
PAGE = "https://stritaweb.org/mass-times"
FACEBOOK_PAGE = "https://www.facebook.com/stritaweb"
MASS_TIMES = (
    "<html><body><h1>Mass Times</h1><p>Saturday Vigil 4:00 PM</p>"
    "<p>Sunday 8:00 AM &amp; 10:30 AM</p><p>Confessions Saturday 3:00 – 3:45 PM</p>"
    "<p>Advent 2026 · Fr. John Smith, Pastor</p>"
    '<p><a href="https://www.facebook.com/StRitaWeb/">Follow us</a></p></body></html>'
)
# A page that is only a picture: its text is the site's menu, the same on every page.
PICTURE = "<html><body><nav>Home · About · Contact</nav></body></html>"
FACEBOOK = (
    "<html><body><div>St. Rita Parish</div><div>Holy Day Mass Tuesday December 8 at "
    "7:00 PM</div><div>Log in to Facebook to see more</div></body></html>"
)

BATCH = """\
include "mass Sat 16:00 note=Vigil" --src "cap primary: Saturday Vigil 4:00 PM" \\
    --why "R43: the parish's Mass times page."
include "mass Sun 08:00,10:30" --src "cap primary: Sunday 8:00 AM & 10:30 AM" \\
    --why "R43: the parish's Mass times page."
include "confession Sat 15:00-15:45" --src "cap primary: Confessions Saturday 3:00 - 3:45 PM" \\
    --why "R43: the parish's Mass times page."
"""


def _png(width: int, height: int, color: str = "white") -> bytes:
    out = io.BytesIO()
    Image.new("RGB", (width, height), color).save(out, format="PNG")
    return out.getvalue()


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


@pytest.fixture
def env(tmp_path: Path, monkeypatch) -> dict[str, Any]:
    """A database with a website_schedule parish and a bulletin parish; the CLI on it."""
    monkeypatch.chdir(tmp_path)
    _write_csv(tmp_path / "parishes.csv", [
        {"slug": PARISH, "name": "St. Rita Parish", "website": SITE,
         "bulletin_provider": "website_schedule", "provider_id": ""},
        {"slug": BULLETIN_PARISH, "name": "St. Luke Parish", "website": "https://stluke.org",
         "bulletin_provider": "parishes_online", "provider_id": "st-luke"},
    ])
    _write_csv(tmp_path / "churches.csv", [
        {"parish_id": PARISH, "slug": CHURCH, "name": "St. Rita Church", "line1": "1 Ridge Rd",
         "city": "Webster", "state": "NY", "postal_code": "14580"},
        {"parish_id": BULLETIN_PARISH, "slug": "st-luke-bulletin-greece",
         "name": "St. Luke Church", "line1": "2 Lake Ave", "city": "Greece", "state": "NY",
         "postal_code": "14612"},
    ])
    db = tmp_path / "parish_events.db"
    conn = connect_db(db)
    migrate(conn)
    seed_reference_data(conn, parishes_csv=tmp_path / "parishes.csv",
                        churches_csv=tmp_path / "churches.csv")
    conn.close()
    set_store(CachedBlobStore(LocalBlobStore(tmp_path / "blobs")))
    seeds = tmp_path / "seeds"
    pages = {PAGE: (MASS_TIMES, PAGE, _png(1280, 4500)),
             FACEBOOK_PAGE: (FACEBOOK, FACEBOOK_PAGE, _png(1280, 900))}
    monkeypatch.setattr(seed_captures, "browser_grab", lambda url: pages[url])
    monkeypatch.setattr(seed_cli, "_connect", lambda: connect_db(db))
    monkeypatch.setattr(seed_cli, "_ctx", lambda args: SeedContext(seeds_dir=seeds))
    yield {"db": db, "seeds": seeds, "root": tmp_path, "pages": pages}
    set_store(None)


@pytest.fixture
def conn(env):
    c = connect_db(env["db"])
    yield c
    c.close()


def _draft(env, capsys, *, current: bool = True) -> dict[str, Any]:
    """St. Rita drafted from its Mass times page, finalized."""
    assert main(["seed", "start", PARISH]) == 0
    assert main(["seed", "capture", PARISH, "/mass-times"]) == 0
    plan = env["root"] / "plan.txt"
    plan.write_text(BATCH)
    assert main(["seed", "slot", "batch", PARISH, str(plan)]) == 0
    assert main(["seed", "summary", PARISH, "Three weekend times from the Mass times page."]) == 0
    if current:
        assert main(["seed", "current", PARISH,
                     "The page names Advent 2026 and the current pastor."]) == 0
    main(["seed", "finalize", PARISH])
    capsys.readouterr()
    seed = read_seed(PARISH, env["seeds"])
    assert seed is not None
    return seed


def _approve(conn, env, seed: dict[str, Any]) -> dict[str, Any]:
    save_reviewed_seed(conn, PARISH, {**seed, "status": APPROVED, "reviewer": "Reviewer"},
                       env["seeds"])
    approved = read_seed(PARISH, env["seeds"])
    assert approved is not None and approved["status"] == APPROVED
    return approved


# ── Starting and capturing ──────────────────────────────────────────────────
def test_a_website_schedule_parish_starts_a_source_seed(env, capsys):
    assert main(["seed", "start", PARISH]) == 0
    out = capsys.readouterr().out
    assert "a new source draft (no bulletins)" in out
    assert "website_schedule: no bulletin" in out and "no captures yet" in out
    seed = read_seed(PARISH, env["seeds"])
    assert seed["kind"] == "source" and seed["bulletins"] == [] and seed["captures"] == []
    assert validate_seed(seed, parish_slug=PARISH) == []
    # A parish with a bulletin starts a bulletin seed, which captures nothing.
    assert main(["seed", "start", BULLETIN_PARISH]) == 0
    assert "kind" not in read_seed(BULLETIN_PARISH, env["seeds"])
    assert main(["seed", "capture", BULLETIN_PARISH, "https://stluke.org"]) == 1
    assert "Only a source seed captures pages" in capsys.readouterr().err


def test_a_capture_keeps_the_pages_text_and_screenshot(env, capsys):
    assert main(["seed", "start", PARISH]) == 0
    assert main(["seed", "capture", PARISH, "/mass-times"]) == 0
    out = capsys.readouterr().out
    seed = read_seed(PARISH, env["seeds"])
    [capture] = seed["captures"]
    assert capture["url"] == PAGE and capture["platform"] == "website" and capture["primary"]
    text = capture_text_path(PARISH, capture["content_hash"], env["seeds"]).read_text()
    assert sha256_text(text) == capture["content_hash"]
    assert "Saturday Vigil 4:00 PM" in text and "Saturday Vigil 4:00 PM" in out
    # Its text says what page it is of, and the Facebook pages the page links.
    header, body = parse_capture_document(text)
    assert header == {"url": PAGE, "final_url": None,
                      "facebook_pages": ["https://www.facebook.com/stritaweb"]}
    assert body.startswith("Mass Times")
    shot = get_store().get(screenshot_key(PARISH, capture["screenshot_hash"]))
    assert shot is not None and shot[8:12] == b"WEBP"
    # The blob store's copy isn't committed: only a quoted screenshot is (finalize).
    assert not list(env["seeds"].rglob("*.webp"))
    tiles = sorted((env["root"] / "data" / "seed-work" / PARISH / "captures").glob("*.png"))
    assert len(tiles) == 3  # 4500 px tall, in tiles Read takes whole
    assert all(fits(*Image.open(t).size) for t in tiles)
    assert f"cap {capture['content_hash'][:8]}" in out and "(primary)" in out

    # The same text again is the same capture, read again now.
    assert main(["seed", "capture", PARISH, PAGE]) == 0
    assert "the same text as before" in capsys.readouterr().out
    assert len(read_seed(PARISH, env["seeds"])["captures"]) == 1

    # A Facebook page asks to log in, and can be made the primary page.
    assert main(["seed", "capture", PARISH, FACEBOOK_PAGE, "--primary"]) == 0
    out = capsys.readouterr().out
    assert "Facebook asked to log in" in out
    captures = read_seed(PARISH, env["seeds"])["captures"]
    assert [(c["platform"], c["primary"]) for c in captures] == [
        ("website", False), ("facebook", True)]


def test_a_challenge_page_is_not_captured(env, capsys):
    env["pages"][PAGE] = ("<html><body>Just a moment...</body></html>", PAGE, None)
    assert main(["seed", "start", PARISH]) == 0
    assert main(["seed", "capture", PARISH, "/mass-times"]) == 1
    assert "a challenge page" in capsys.readouterr().err
    assert read_seed(PARISH, env["seeds"])["captures"] == []


# ── Drafting and checking ───────────────────────────────────────────────────
def test_a_source_seed_drafts_from_its_captures_and_checks(env, conn, capsys):
    seed = _draft(env, capsys)
    assert seed["status"] == READY
    [capture] = seed["captures"]
    assert seed["as_of"] == capture["captured_at"]
    as_of = seed["as_of"][:10]
    assert seed["recheck_after"] == add_months(date.fromisoformat(as_of), 3).isoformat()
    first = seed["slots"][0]
    assert first["page"] is None
    assert first["sources"] == [{"source": "website", "capture": capture["content_hash"][:8],
                                 "url": PAGE, "said": "Saturday Vigil 4:00 PM"}]
    assert check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"]) == []
    assert main(["seed", "check", PARISH]) == 0
    assert main(["seed", "slot", "show", PARISH, "s1"]) == 0
    assert f"cap {capture['content_hash'][:8]}: Saturday Vigil 4:00 PM" in capsys.readouterr().out


def test_a_source_seeds_quote_must_be_in_its_capture(env, conn, capsys):
    seed = _draft(env, capsys)
    seed["slots"][0]["sources"][0]["said"] = "Saturday Vigil 5:00 PM"
    problems = check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"])
    assert any("s1.sources[0].said is not in capture" in p for p in problems)
    # The header isn't the page: a quote of it isn't found.
    seed["slots"][0]["sources"][0]["said"] = "Captured from"
    problems = check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"])
    assert any("s1.sources[0].said is not in capture" in p for p in problems)
    seed["slots"][0]["sources"][0]["said"] = "Saturday Vigil 4:00 PM"
    # The committed text is the evidence: missing or edited, it fails.
    path = capture_text_path(PARISH, seed["captures"][0]["content_hash"], env["seeds"])
    path.write_text(path.read_text() + "edited\n")
    assert any("has changed since it was captured" in p
               for p in check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"]))
    path.unlink()
    assert any("text is missing" in p
               for p in check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"]))


def test_a_source_seed_needs_the_parishs_own_pages_and_no_bulletin(env, conn, capsys):
    seed = _draft(env, capsys)
    off_site = json.loads(json.dumps(seed))
    off_site["captures"][0]["url"] = "https://masstimes.example/st-rita"
    for slot in off_site["slots"]:
        slot["sources"][0]["url"] = "https://masstimes.example/st-rita"
    problems = check_seed(conn, off_site, parish_slug=PARISH, seeds_dir=env["seeds"])
    assert any("is not on the parish's own website" in p for p in problems)
    # The committed text says which page it is of, so the file can't be pointed elsewhere.
    assert any("must be those its text was captured from" in p for p in problems)

    conn.execute("UPDATE parish SET bulletin_provider = 'parishes_online' WHERE slug = ?",
                 (PARISH,))
    problems = check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"])
    assert any("a parish with a bulletin is seeded from it" in p for p in problems)
    # An approved seed's evidence isn't checked again, so it still loads.
    assert check_seed(conn, seed, parish_slug=PARISH, check_evidence=False,
                      seeds_dir=env["seeds"]) == []


def test_a_source_seeds_shape(env, capsys):
    seed = _draft(env, capsys)
    assert validate_seed(seed) == []

    def problems(**changes: Any) -> list[str]:
        changed = json.loads(json.dumps(seed))
        for path, value in changes.items():
            *keys, last = path.split("__")
            target = changed
            for key in keys:
                target = target[int(key)] if key.isdigit() else target[key]
            target[last] = value
        return validate_seed(changed)

    assert any("page must be null" in p for p in problems(slots__0__page=2))
    assert any("names one of the file's captures" in p or "must name one of the file's captures"
               in p for p in problems(slots__0__sources__0__capture="ffffffff"))
    assert any("must be website or facebook" in p
               for p in problems(slots__0__sources__0__source="agent"))
    assert any("must be its capture's" in p
               for p in problems(slots__0__sources__0__url="https://stritaweb.org/other"))
    assert any("needs a capture with a screenshot" in p for p in problems(
        captures__0__screenshot_hash=None, slots__0__sources__0__from_image=True))
    assert any("bulletins must be empty" in p for p in problems(bulletins=[
        {"content_hash": "a" * 64, "fetched_at": "2026-11-01T00:00:00Z",
         "published_date": None, "read": True}]))
    assert any("platform must be facebook" in p
               for p in problems(captures__0__url="https://www.facebook.com/x"))
    assert any("current_because is required" in p for p in problems(current_because=None))
    assert any("must be after as_of" in p for p in problems(recheck_after="2020-01-01"))
    assert any("exactly one must be primary" in p for p in problems(captures__0__primary=False))
    # A bulletin seed has none of a source seed's keys.
    bulletin = new_seed("st-luke-bulletin", [])
    assert validate_seed({**bulletin, "captures": []}) == [
        "captures: only a source seed has these"]
    assert validate_seed({**bulletin, "kind": "web"}) == ["kind must be one of bulletin, source"]


def test_a_source_seed_gets_no_history_and_only_a_source_seed_says_why_it_is_current(
        env, capsys):
    seed = _draft(env, capsys)
    assert seed["calls"] == []
    # finalize attaches no history sources to a source seed, whatever it is given.
    history = [{"short": "1ab3e7c2", "content_hash": "1ab3e7c2" + "0" * 56,
                "wrong_bulletin": False, "events": []}]
    finalized = finalize_seed(seed, [CHURCH], history)
    assert [s["source"] for slot in finalized["slots"] for s in slot["sources"]] == [
        "website"] * 4
    assert main(["seed", "start", BULLETIN_PARISH]) == 0
    capsys.readouterr()
    assert main(["seed", "current", BULLETIN_PARISH, "why"]) == 1
    assert "current_because is a source seed's" in capsys.readouterr().err


def test_current_and_recheck_after(env, capsys):
    _draft(env, capsys, current=False)
    seed = read_seed(PARISH, env["seeds"])
    assert seed["status"] == READY  # finalize doesn't check; check does
    assert main(["seed", "check", PARISH]) == 1
    assert "current_because is required" in capsys.readouterr().out
    assert main(["seed", "current", PARISH, "Dated post of 2026-11-10",
                 "--recheck-after", "2027-01-15"]) == 0
    assert main(["seed", "check", PARISH]) == 0
    assert read_seed(PARISH, env["seeds"])["recheck_after"] == "2027-01-15"
    # Any ISO form is stored as YYYY-MM-DD, which the file requires.
    assert main(["seed", "current", PARISH, "Dated post", "--recheck-after", "20270116"]) == 0
    assert read_seed(PARISH, env["seeds"])["recheck_after"] == "2027-01-16"
    assert main(["seed", "check", PARISH]) == 0
    assert main(["seed", "current", PARISH, "x", "--recheck-after", "soon"]) == 1


# ── What a capture is, and whose ────────────────────────────────────────────
def test_two_pages_with_the_same_text_are_two_captures(env, capsys):
    env["pages"].update({
        f"{SITE}/mass": (PICTURE, f"{SITE}/mass", _png(1280, 900, "red")),
        f"{SITE}/confession": (PICTURE, f"{SITE}/confession", _png(1280, 900, "blue")),
    })
    assert main(["seed", "start", PARISH]) == 0
    assert main(["seed", "capture", PARISH, "/mass"]) == 0
    assert main(["seed", "capture", PARISH, "/confession", "--primary"]) == 0
    out = capsys.readouterr().out
    assert "almost no text" in out and "the same text as before" not in out
    captures = read_seed(PARISH, env["seeds"])["captures"]
    assert [(c["url"], c["primary"]) for c in captures] == [
        (f"{SITE}/mass", False), (f"{SITE}/confession", True)]
    assert len({c["content_hash"] for c in captures}) == 2
    assert len({c["screenshot_hash"] for c in captures}) == 2


def test_a_quote_read_from_a_screenshot_is_committed_and_read_again_when_it_changes(
        env, conn, capsys):
    seed = _draft(env, capsys)
    [capture] = seed["captures"]
    [source] = parse_source(seed, "cap primary image: Sat Vigil 4 PM")
    assert source["from_image"] == capture["screenshot_hash"]
    seed["slots"][0]["sources"].append(source)
    write_seed_file(seed, env["seeds"])
    # Nothing matches it to the text, so the reviewer must be able to see the picture.
    problems = check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"])
    assert any("which isn't committed" in p for p in problems)
    assert main(["seed", "finalize", PARISH]) == 0
    committed = screenshot_path(PARISH, capture["screenshot_hash"], env["seeds"])
    assert committed.read_bytes() == get_store().get(
        screenshot_key(PARISH, capture["screenshot_hash"]))

    # The page's picture changes under the same text: the quote must be read again.
    env["pages"][PAGE] = (MASS_TIMES, PAGE, _png(1280, 4500, "yellow"))
    assert main(["seed", "capture", PARISH, PAGE]) == 0
    assert "s1 quote the old one" in capsys.readouterr().out
    seed = read_seed(PARISH, env["seeds"])
    assert any("a screenshot the capture no longer has" in p
               for p in check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"]))
    # Without the quote, finalize removes the screenshot nothing quotes.
    seed["slots"][0]["sources"].pop()
    write_seed_file(seed, env["seeds"])
    assert main(["seed", "finalize", PARISH]) == 0
    assert not committed.exists()


def test_a_facebook_capture_must_be_the_parishs_own_page(env, conn, capsys):
    other = "https://www.facebook.com/stbernard"
    env["pages"][other] = (FACEBOOK, other, _png(1280, 900))
    _draft(env, capsys)
    # The parish's Mass times page links its Facebook page.
    assert main(["seed", "capture", PARISH, FACEBOOK_PAGE]) == 0
    main(["seed", "finalize", PARISH])
    capsys.readouterr()
    assert check_seed(conn, read_seed(PARISH, env["seeds"]), parish_slug=PARISH,
                      seeds_dir=env["seeds"]) == []
    # Another page, with the same text, is not the parish's.
    assert main(["seed", "capture", PARISH, other]) == 0
    main(["seed", "finalize", PARISH])
    capsys.readouterr()
    problems = check_seed(conn, read_seed(PARISH, env["seeds"]), parish_slug=PARISH,
                          seeds_dir=env["seeds"])
    assert [p for p in problems if "not the parish's own Facebook page" in p] == [
        f"capture {read_seed(PARISH, env['seeds'])['captures'][2]['content_hash'][:12]} "
        f"({other}) is not the parish's own Facebook page: capture the page of its website "
        "that links it (its website links https://www.facebook.com/stritaweb)"]


def test_a_website_capture_must_not_end_on_another_site(env, conn, capsys):
    env["pages"][PAGE] = (MASS_TIMES, "https://parked.example/", _png(1280, 900))
    seed = _draft(env, capsys)
    assert seed["captures"][0]["final_url"] == "https://parked.example/"
    problems = check_seed(conn, seed, parish_slug=PARISH, seeds_dir=env["seeds"])
    assert any("ended on another site, https://parked.example/" in p for p in problems)


def test_facebook_pages_are_named_alike():
    page = "https://www.facebook.com/stritaweb"
    assert facebook_page("https://m.facebook.com/StRitaWeb/posts/123") == page
    assert facebook_page("https://www.facebook.com/pg/StRitaWeb/about/") == page
    assert facebook_page("https://www.facebook.com/profile.php?id=1000&sk=about") == (
        "https://www.facebook.com/profile.php?id=1000")
    assert facebook_page("https://www.facebook.com/people/St-Rita/1000/") == (
        "https://www.facebook.com/profile.php?id=1000")
    assert facebook_page("https://www.facebook.com/sharer/sharer.php?u=x") is None
    assert facebook_page(SITE) is None
    plugin = ("https://www.facebook.com/plugins/page.php?href=https%3A%2F%2Fwww.facebook.com"
              "%2FStRitaWeb&amp;tabs=timeline")
    html = (f'<iframe src="{plugin}"></iframe>'
            '<a href="https://facebook.com/sharer.php?u=1">Share</a>')
    assert linked_facebook_pages(html, SITE) == [page]


# ── Loading, the snapshot and the report ────────────────────────────────────
def test_an_approved_source_seed_loads_with_its_page_and_reaches_the_snapshot(env, conn, capsys):
    approved = _approve(conn, env, _draft(env, capsys))
    result = load_approved_seeds(conn, env["seeds"])
    [loaded] = result["loaded"]
    assert loaded["kind"] == "source" and loaded["source_url"] == PAGE
    assert loaded["entries"] == 4 and loaded["sightings"] == 0
    row = conn.execute(
        "SELECT schedule_source, schedule_source_url, as_of FROM schedule_revision r "
        "JOIN parish p ON p.id = r.parish_id WHERE p.slug = ?", (PARISH,)).fetchone()
    assert tuple(row)[:2] == ("website", PAGE)
    assert any("from https://stritaweb.org/mass-times" in line
               for line in render_seeds(result))

    dest = env["root"] / "frontend.json.gz"
    extract(env["db"], dest, keep_previous=False)
    churches = {c["slug"]: c for c in read_snapshot(dest.read_bytes())["churches"]}
    assert churches[CHURCH]["schedule_source"] == "website"
    assert churches[CHURCH]["source_url"] == PAGE
    assert churches[CHURCH]["checked_on"] == checked_on(approved["as_of"])
    assert churches[CHURCH]["bulletin_url"] is None

    # A bulletin the parish once published is no longer its current one.
    parish_id = conn.execute("SELECT id FROM parish WHERE slug = ?", (PARISH,)).fetchone()[0]
    old = "https://stritaweb.org/bulletin-2025-01-05.pdf"
    bulletin_id = insert_bulletin(conn, parish_id=parish_id, source_url=old,
                                  content_hash="b" * 64, fetched_at="2025-01-02T00:00:00Z")
    save_processed_bulletin(conn, bulletin_id, [], processed_at="2025-01-02T01:00:00Z",
                            published_date="2025-01-05")
    conn.commit()
    extract(env["db"], dest, keep_previous=False)
    churches = {c["slug"]: c for c in read_snapshot(dest.read_bytes())["churches"]}
    assert churches[CHURCH]["schedule_source"] == "website"
    assert churches[CHURCH]["bulletin_url"] is None
    assert churches[CHURCH]["bulletin_week"] is None

    # A parish that has found a bulletin is shown as a bulletin parish.
    conn.execute("UPDATE parish SET bulletin_provider = 'parishes_online' WHERE slug = ?",
                 (PARISH,))
    conn.commit()
    extract(env["db"], dest, keep_previous=False)
    churches = {c["slug"]: c for c in read_snapshot(dest.read_bytes())["churches"]}
    assert churches[CHURCH]["schedule_source"] is None
    assert churches[CHURCH]["bulletin_url"] == old


def test_checked_on_is_the_date_in_the_parishes_time_zone():
    # 9 PM in New York on November 16 is already November 17 in UTC.
    assert checked_on("2026-11-17T02:00:00+00:00") == "2026-11-16"
    assert checked_on("2026-07-01T12:00:00Z") == "2026-07-01"
    assert checked_on(None) is None


def test_a_source_seeds_digest_covers_its_primary_page(env, conn, capsys):
    seed = _draft(env, capsys)
    moved = json.loads(json.dumps(seed))
    moved["captures"][0]["url"] = "https://stritaweb.org/schedule"
    assert seed_digest(moved) != seed_digest(seed)


def test_source_schedules_due_are_a_warning_in_the_report(env, conn, capsys):
    approved = _approve(conn, env, _draft(env, capsys))
    recheck = approved["recheck_after"]
    assert due_source_seeds(conn, "2026-01-01", env["seeds"]) == []
    [due] = due_source_seeds(conn, recheck, env["seeds"])
    assert due["parish"] == PARISH and due["source_url"] == PAGE
    lines = render_source_due([due])
    assert lines[1] == "### Source schedules due" and "They stay on the site." in lines[3]
    assert f"**{PARISH}**: recheck after {recheck}" in lines[4]
    # A parish that has found a bulletin is no longer due.
    conn.execute("UPDATE parish SET bulletin_provider = 'parishes_online' WHERE slug = ?",
                 (PARISH,))
    assert due_source_seeds(conn, recheck, env["seeds"]) == []


def test_an_approved_source_seed_cannot_be_captured_into(env, conn, capsys):
    approved = _approve(conn, env, _draft(env, capsys))
    before = seed_path(PARISH, env["seeds"]).read_bytes()
    with pytest.raises(SeedError, match="belongs to its reviewer"):
        capture_page(approved, PAGE, grab=lambda url: env["pages"][url], seeds_dir=env["seeds"])
    assert main(["seed", "capture", PARISH, "/mass-times"]) == 1
    assert seed_path(PARISH, env["seeds"]).read_bytes() == before


# ── The labeler, and fetch ──────────────────────────────────────────────────
def test_the_labeler_serves_a_source_seeds_captures(env, capsys, tmp_path):
    seed = _draft(env, capsys)
    [capture] = seed["captures"]
    static = tmp_path / "dist"
    static.mkdir()
    (static / "index.html").write_text("<!doctype html>")
    app = LabelerApp(db_path=env["db"], labels_dir=tmp_path / "labels", static_dir=static,
                     seeds_dir=env["seeds"])
    srv = make_server(app, port=0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()

    def get(path: str) -> tuple[int, str, bytes]:
        conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1], timeout=10)
        conn.request("GET", path, headers={"Host": f"localhost:{srv.server_address[1]}"})
        resp = conn.getresponse()
        return resp.status, resp.getheader("Content-Type") or "", resp.read()

    try:
        base = f"/api/seeds/{PARISH}/captures"
        status, kind, body = get(f"{base}/{capture['content_hash']}/text")
        assert status == 200 and kind.startswith("text/plain")
        assert "Saturday Vigil 4:00 PM" in body.decode()
        status, kind, body = get(f"{base}/{capture['content_hash']}/image")
        assert status == 200 and kind == "image/webp" and body[8:12] == b"WEBP"
        # A committed screenshot is served without the blob store.
        set_store(CachedBlobStore(LocalBlobStore(tmp_path / "empty")))
        assert get(f"{base}/{capture['content_hash']}/image")[0] == 404
        committed = screenshot_path(PARISH, capture["screenshot_hash"], env["seeds"])
        committed.parent.mkdir(parents=True, exist_ok=True)
        committed.write_bytes(body)
        assert get(f"{base}/{capture['content_hash']}/image")[2] == body
        # Only a capture the parish's seed lists.
        assert get(f"{base}/{'0' * 64}/text")[0] == 404
        assert get(f"/api/seeds/{BULLETIN_PARISH}/captures/{capture['content_hash']}/text")[
            0] == 404
        assert get(f"{base}/not-a-hash/text")[0] == 400
        status, _, body = get(f"/api/seeds/{PARISH}")
        assert status == 200 and json.loads(body)["problems"] == []
    finally:
        srv.shutdown()
        srv.server_close()


def test_fetch_skips_a_website_schedule_parish():
    assert fetch._resolve_fetch_source(
        {"bulletin_provider": "website_schedule", "provider_id": "", "homepage_url": SITE}
    ) is None
