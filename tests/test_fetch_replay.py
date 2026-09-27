"""Replay each parish's recorded pages through today's resolver.

`tests/fixtures/fetch/<slug>.json.gz` holds the pages a resolver read on a real
site (`pnpm fetch:check --record tests/fixtures/fetch`), and `expected.json`
what it should resolve from them: the bulletin, or the error for a site the
fetch stage cannot read yet. A resolver change that picks a different bulletin
on any recorded site fails here, before a weekly run finds out.

When a change fixes a site, or a site is re-recorded, update its entry in
`expected.json`: the diff is the coverage change.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from pdf_extract.fetch_check import (
    SNAPSHOT_SUFFIX,
    PageSnapshot,
    SnapshotPage,
    load_recording,
)

FIXTURES = Path(__file__).parent / "fixtures" / "fetch"
EXPECTED: dict[str, dict[str, str]] = json.loads((FIXTURES / "expected.json").read_text())
RECORDINGS = sorted(FIXTURES.glob(f"*{SNAPSHOT_SUFFIX}"))


def _slug(path: Path) -> str:
    return path.name.removesuffix(SNAPSHOT_SUFFIX)


def test_every_recording_has_an_expectation() -> None:
    recorded = {_slug(p) for p in RECORDINGS}
    assert sorted(recorded - EXPECTED.keys()) == []
    assert sorted(EXPECTED.keys() - recorded) == []


@pytest.mark.parametrize("path", RECORDINGS, ids=_slug)
def test_resolver_replays_recorded_site(path: Path) -> None:
    recording = load_recording(path)
    expected = EXPECTED[recording.slug]
    if "error" in expected:
        with pytest.raises(ValueError, match=re.escape(expected["error"])):
            recording.resolve()
        return
    link = recording.resolve()
    assert link.source_url == expected["source_url"]
    assert link.fetch_url == expected.get("fetch_url", expected["source_url"])


def test_snapshot_page_matches_the_selectors_resolvers_use() -> None:
    page = SnapshotPage([
        PageSnapshot(
            requested_url="https://example.org/",
            final_url="https://example.org/home",
            html=(
                '<a id="bulletin-current" href="https://bulletins.discovermass.com/x">Now</a>'
                '<a href="/b.pdf"><span>Bulletin</span> Sept 27</a>'
                '<a name="top">no href</a><iframe src="https://e.org/v"></iframe>'
            ),
        ),
    ])
    page.goto("https://example.org")
    assert page.url == "https://example.org/home"
    assert len(page.query_selector_all("a[href]")) == 2
    assert [a.inner_text() for a in page.query_selector_all("a[href$='.pdf']")] == [
        "Bulletin Sept 27",
    ]
    assert len(page.query_selector_all("a#bulletin-current[href]")) == 1
    assert len(page.query_selector_all("a[href*='discovermass']")) == 1
    assert len(page.query_selector_all("iframe[src], a[name]")) == 2
    with pytest.raises(TimeoutError):
        page.wait_for_selector("img", timeout=10)
