"""Replay each parish's recorded pages through today's resolver.

`tests/fixtures/fetch/<slug>.json.gz` holds the pages a resolver read on a real
site (`pnpm fetch:check --record tests/fixtures/fetch`), and `expected.json`
what it should resolve from them: the bulletin, or the error for a site the
fetch stage cannot read yet. A resolver change that picks a different bulletin
on any recorded site fails here, before a weekly run finds out.

When a change fixes a site, or a site is re-recorded, update its entry in
`expected.json`: the diff is the coverage change.

Each site is replayed with the parish's recipe in data/parishes.csv as it is
now, so pinning a recipe is checked against the pages too.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import replace
from datetime import date
from pathlib import Path

import pytest

from pdf_extract.bulletin_week import nearest_sunday
from pdf_extract.fetch import (
    _PROVIDERS,
    PARISHES_ONLINE_ORG_URL_TEMPLATE,
    PARISHES_ONLINE_TYPE,
    FetchSource,
    _extract_parishes_online_pdf_url_from_href,
    _predict_parishes_online_link,
)
from pdf_extract.fetch_check import (
    SNAPSHOT_SUFFIX,
    PageSnapshot,
    SnapshotPage,
    load_recording,
)

FIXTURES = Path(__file__).parent / "fixtures" / "fetch"
EXPECTED: dict[str, dict[str, str]] = json.loads((FIXTURES / "expected.json").read_text())
RECORDINGS = sorted(FIXTURES.glob(f"*{SNAPSHOT_SUFFIX}"))
PARISHES_CSV = Path(__file__).parents[1] / "data" / "parishes.csv"
PARISHES = {row["slug"]: row for row in csv.DictReader(PARISHES_CSV.open(encoding="utf-8"))}


def _slug(path: Path) -> str:
    return path.name.removesuffix(SNAPSHOT_SUFFIX)


def _current_recipe(slug: str, provider: str) -> str | None:
    column = _PROVIDERS[provider].recipe_column
    parish = PARISHES.get(slug)
    if column is None or parish is None:
        return None
    return parish[column].strip()


def test_every_recording_has_an_expectation() -> None:
    recorded = {_slug(p) for p in RECORDINGS}
    assert sorted(recorded - EXPECTED.keys()) == []
    assert sorted(EXPECTED.keys() - recorded) == []


@pytest.mark.parametrize("path", RECORDINGS, ids=_slug)
def test_resolver_replays_recorded_site(path: Path) -> None:
    recording = load_recording(path)
    expected = EXPECTED[recording.slug]
    recipe = _current_recipe(recording.slug, recording.provider)
    if "error" in expected:
        with pytest.raises(ValueError, match=re.escape(expected["error"])):
            recording.resolve(recipe=recipe)
        return
    link = recording.resolve(recipe=recipe)
    assert link.source_url == expected["source_url"]
    assert link.fetch_url == expected.get("fetch_url", expected["source_url"])


@pytest.mark.parametrize("slug", [
    "saint-anne-johnstown", "saint-therese-of-the-child-jesus-johnstown",
])
def test_johnstown_recipes_keep_the_latest_own_issue_after_the_current_window(slug: str) -> None:
    recording = load_recording(FIXTURES / f"{slug}{SNAPSHOT_SUFFIX}")
    delayed = replace(recording, reference_date=date(2026, 10, 26))
    link = delayed.resolve(recipe=_current_recipe(slug, recording.provider))
    assert link.source_url == EXPECTED[slug]["source_url"]


PARISHES_ONLINE_RECORDINGS = [
    path for path in RECORDINGS if load_recording(path).provider == PARISHES_ONLINE_TYPE
]


def _listed_parishes_online_issues(recording) -> list[tuple[str, str]]:
    """Every issue the recorded organization page links, as (page, PDF)."""
    org_url = PARISHES_ONLINE_ORG_URL_TEMPLATE.format(provider_id=recording.provider_id)
    page = recording.page()
    page.goto(org_url)
    return [
        urls for anchor in page.query_selector_all("a[href*='selectedPublication=']")
        if (urls := _extract_parishes_online_pdf_url_from_href(
            href=anchor.get_attribute("href") or "", provider_id=recording.provider_id,
            base_url=org_url,
        ))
    ]


def test_parishes_online_predicted_address_leads_to_the_pages_bulletin() -> None:
    """On each recorded organization page, with the file host holding exactly
    the issues listed and the oldest of them stored, a predicted bulletin
    taken directly is the one the page resolves to."""
    predicted_count = hits = 0
    for path in PARISHES_ONLINE_RECORDINGS:
        recording = load_recording(path)
        listed = _listed_parishes_online_issues(recording)
        on_host = {pdf for _, pdf in listed}
        oldest = min(listed, key=lambda urls: urls[1].rsplit("/", 1)[-1])
        stored = [{
            "id": 1, "source_url": oldest[0], "content_hash": "h", "published_date": None,
            "fetched_at": f"{recording.reference_date.isoformat()}T09:00:00Z",
            "wrong_bulletin": 0,
        }]
        sunday = nearest_sunday(recording.reference_date)
        predicted = _predict_parishes_online_link(
            FetchSource(PARISHES_ONLINE_TYPE, recording.provider_id), stored, sunday,
            recording.reference_date,
        )
        # Recorded on a Saturday and a Friday, before the run's Sunday.
        assert (predicted is None) == (recording.reference_date < sunday), recording.slug
        if predicted is None:
            continue
        predicted_count += 1
        if any(url in on_host for url in predicted.later):
            continue
        if predicted.link.fetch_url not in on_host:
            continue
        hits += 1
        resolved = recording.resolve()
        assert (predicted.link.source_url, predicted.link.fetch_url) == (
            resolved.source_url, resolved.fetch_url,
        ), recording.slug
    assert len(PARISHES_ONLINE_RECORDINGS) >= 90
    # Recorded on a Monday and a Wednesday: most pages had the weekend's
    # bulletin, so the comparison is not empty.
    assert predicted_count >= 30
    assert hits >= predicted_count * 3 // 4, (hits, predicted_count)


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
