from dataclasses import replace
from datetime import date

import pytest

from pdf_extract.browser import goto_with_retry
from pdf_extract.fetch import (
    _PROVIDERS,
    DISCOVER_MASS_TYPE,
    ECATHOLIC_TYPE,
    OTHER_TYPE,
    PARISHES_ONLINE_TYPE,
    BulletinLink,
    FetchSource,
    _build_bulletin_link,
    _extract_discover_mass_pdf_url_from_href,
    _extract_ecatholic_pdf_url_from_href,
    _extract_parishes_online_pdf_url_from_href,
    _normalize_url_for_request,
    _parse_ecatholic_pdf_date,
    _pick_latest_ecatholic_pdf_url,
    _report_stale_parishes,
    _resolve_ecatholic_latest_link,
    _resolve_fetch_source,
    _resolve_latest_anchor_link_with_playwright,
    build_latest_discover_mass_bulletin_links,
    build_latest_ecatholic_bulletin_links,
    build_latest_other_bulletin_links,
    build_latest_parishes_online_bulletin_links,
)
from pdf_extract.parish_sites import Resolution
from pdf_extract.parish_sites.choose import CURRENT, Candidate
from pdf_extract.parish_sites.dates import parse_date
from pdf_extract.parish_sites.locate import find_bulletin_page_urls
from pdf_extract.storage import utc_now_iso


def _resolve_other(**kwargs) -> tuple[str, str]:
    link = build_latest_other_bulletin_links(**kwargs)
    return link.source_url, link.fetch_url


def test_build_latest_ecatholic_bulletin_links(monkeypatch) -> None:
    def fake_resolve(*, provider_id: str, page=None) -> tuple[str, str]:
        assert provider_id == "https://southeastrochestercatholics.org"
        return (
            "https://files.ecatholic.com/19887/bulletins/20260222.pdf",
            "https://files.ecatholic.com/19887/bulletins/20260222.pdf",
        )

    monkeypatch.setattr("pdf_extract.fetch._resolve_ecatholic_latest_link", fake_resolve)
    link = build_latest_ecatholic_bulletin_links(
        provider_id="https://southeastrochestercatholics.org",
        reference_date=date(2026, 2, 19),  # should be ignored
    )
    assert link.source_url == "https://files.ecatholic.com/19887/bulletins/20260222.pdf"
    assert link.fetch_url == "https://files.ecatholic.com/19887/bulletins/20260222.pdf"


def test_extract_ecatholic_pdf_url_from_href() -> None:
    urls = _extract_ecatholic_pdf_url_from_href(
        href="/19887/bulletins/20260222.pdf",
        base_url="https://files.ecatholic.com",
    )
    assert urls == (
        "https://files.ecatholic.com/19887/bulletins/20260222.pdf",
        "https://files.ecatholic.com/19887/bulletins/20260222.pdf",
    )


def test_build_latest_parishes_online_bulletin_links(monkeypatch) -> None:
    def fake_resolve(*, provider_id: str, page=None) -> tuple[str, str]:
        assert provider_id == "123"
        return (
            "https://parishesonline.com/publication-page/123?selectedPublication=https://container.parishesonline.com/path/latest.pdf",
            "https://container.parishesonline.com/path/latest.pdf",
        )

    monkeypatch.setattr("pdf_extract.fetch._resolve_parishes_online_latest_link", fake_resolve)
    link = build_latest_parishes_online_bulletin_links(
        provider_id="123",
        reference_date=date(2026, 2, 19),
    )
    assert link.fetch_url == "https://container.parishesonline.com/path/latest.pdf"


def test_build_latest_discover_mass_bulletin_links() -> None:
    class FakePage:
        def goto(self, url: str, wait_until: str) -> None:
            assert url == "https://discovermass.com/church/st-joseph-rush/"
            assert wait_until == "domcontentloaded"

        def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
            assert selector == "a#bulletin-current[href]"
            assert timeout == 15000
            assert state == "attached"

        def query_selector_all(self, selector: str):
            assert selector == "a#bulletin-current[href]"

            class _Anchor:
                def __init__(self, href):
                    self._href = href

                def get_attribute(self, name: str):
                    if name == "href":
                        return self._href
                    return None

            return [
                _Anchor("/church/st-joseph-rush/"),
                _Anchor("https://bulletins.discovermass.com/download.php?bulletin=abc123"),
            ]

    link = build_latest_discover_mass_bulletin_links(
        provider_id="/st-joseph-rush/",
        page=FakePage(),
    )
    assert link.source_url == "https://bulletins.discovermass.com/download.php?bulletin=abc123"
    assert link.fetch_url == "https://bulletins.discovermass.com/download.php?bulletin=abc123"


def test_build_latest_discover_mass_bulletin_links_raises_when_bulletin_anchor_missing() -> None:
    class FakePage:
        def goto(self, url: str, wait_until: str) -> None:
            assert url == "https://discovermass.com/church/st-joseph-rush/"
            assert wait_until == "domcontentloaded"

        def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
            assert selector == "a#bulletin-current[href]"
            assert timeout == 15000
            assert state == "attached"

        def query_selector_all(self, selector: str):
            assert selector == "a#bulletin-current[href]"
            return []

    try:
        build_latest_discover_mass_bulletin_links(
            provider_id="st-joseph-rush",
            page=FakePage(),
        )
    except ValueError as exc:
        assert "No matching anchor link found for discover-mass provider_id=st-joseph-rush" in str(exc)
    else:
        raise AssertionError("Expected ValueError when Discover Mass bulletin anchor is missing")


def test_extract_discover_mass_pdf_url_from_href() -> None:
    urls = _extract_discover_mass_pdf_url_from_href(
        href="https://bulletins.discovermass.com/download.php?bulletin=abc123",
        base_url="https://discovermass.com/church/st-joseph-rush/",
    )
    assert urls == (
        "https://bulletins.discovermass.com/download.php?bulletin=abc123",
        "https://bulletins.discovermass.com/download.php?bulletin=abc123",
    )


def test_extract_discover_mass_pdf_url_from_href_rejects_non_download_urls() -> None:
    urls = _extract_discover_mass_pdf_url_from_href(
        href="https://bulletins.discovermass.com/image.php?bulletin=abc123",
        base_url="https://discovermass.com/church/st-joseph-rush/",
    )
    assert urls is None


def test_extract_parishes_online_pdf_url_from_absolute_href() -> None:
    href = (
        "https://parishesonline.com/publication-page/abc-123?"
        "selectedPublication=https%3A%2F%2Fcontainer.parishesonline.com%2Fpath%2Flatest.pdf"
    )
    urls = _extract_parishes_online_pdf_url_from_href(
        href=href,
        provider_id="abc-123",
        base_url="https://parishesonline.com/organization/abc-123",
    )
    assert urls == (
        "https://parishesonline.com/publication-page/abc-123?"
        "selectedPublication=https%3A%2F%2Fcontainer.parishesonline.com%2Fpath%2Flatest.pdf",
        "https://container.parishesonline.com/path/latest.pdf",
    )


def test_extract_parishes_online_pdf_url_from_relative_href() -> None:
    href = (
        "/publication-page/our-lady-of-lourdes-saint-anne-church?"
        "selectedPublication=https%3A%2F%2Fcontainer.parishesonline.com%2Fbulletins%2Fweekly.pdf"
    )
    urls = _extract_parishes_online_pdf_url_from_href(
        href=href,
        provider_id="our-lady-of-lourdes-saint-anne-church",
        base_url="https://parishesonline.com/organization/our-lady-of-lourdes-saint-anne-church",
    )
    assert urls == (
        "https://parishesonline.com/publication-page/our-lady-of-lourdes-saint-anne-church?"
        "selectedPublication=https%3A%2F%2Fcontainer.parishesonline.com%2Fbulletins%2Fweekly.pdf",
        "https://container.parishesonline.com/bulletins/weekly.pdf",
    )


def test_resolve_latest_anchor_link_with_playwright_uses_first_valid_anchor() -> None:
    class FakeAnchor:
        def __init__(self, href):
            self._href = href

        def get_attribute(self, name: str):
            if name == "href":
                return self._href
            return None

    class FakePage:
        def goto(self, url: str, wait_until: str) -> None:
            assert url == "https://example.org/bulletins"
            assert wait_until == "domcontentloaded"

        def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
            assert selector == "a[href*='bulletins']"
            assert timeout == 15000

        def query_selector_all(self, selector: str):
            assert selector == "a[href*='bulletins']"
            return [
                FakeAnchor(None),
                FakeAnchor("/ignore-this"),
                FakeAnchor("/good.pdf"),
                FakeAnchor("/later.pdf"),
            ]

    fake_page = FakePage()
    seen_hrefs: list[str] = []

    def href_to_urls(href: str):
        seen_hrefs.append(href)
        if href == "/good.pdf":
            return ("https://example.org/source", "https://example.org/good.pdf")
        return None

    source_url, fetch_url = _resolve_latest_anchor_link_with_playwright(
        page_url="https://example.org/bulletins",
        anchor_selector="a[href*='bulletins']",
        source_label="test-provider",
        href_to_urls=href_to_urls,
        page=fake_page,
    )
    assert seen_hrefs == ["/ignore-this", "/good.pdf"]
    assert source_url == "https://example.org/source"
    assert fetch_url == "https://example.org/good.pdf"


@pytest.mark.parametrize(
    ("provider", "provider_id", "builder"),
    [
        (ECATHOLIC_TYPE, "https://test.org", build_latest_ecatholic_bulletin_links),
        (PARISHES_ONLINE_TYPE, "123", build_latest_parishes_online_bulletin_links),
        (DISCOVER_MASS_TYPE, "st-joseph-rush", build_latest_discover_mass_bulletin_links),
        (OTHER_TYPE, "https://example.org", build_latest_other_bulletin_links),
    ],
)
def test_build_bulletin_link_dispatches_to_the_registered_builder(
    monkeypatch, provider: str, provider_id: str, builder
) -> None:
    assert _PROVIDERS[provider].build is builder

    seen: dict[str, object] = {}

    def fake_build(*, provider_id, reference_date=None, page=None, **recipe):
        seen["provider_id"] = provider_id
        seen.update(recipe)
        return BulletinLink(source_url="https://example.org/b.pdf", fetch_url="https://example.org/b.pdf")

    monkeypatch.setitem(
        _PROVIDERS, provider, replace(_PROVIDERS[provider], build=fake_build),
    )
    link = _build_bulletin_link(provider, provider_id, recipe="page-pdfs")
    assert seen["provider_id"] == provider_id
    # Only a provider that reads the parish's own site takes a recipe.
    assert seen.get("recipe") == ("page-pdfs" if provider == OTHER_TYPE else None)
    assert link.fetch_url == "https://example.org/b.pdf"


def test_build_bulletin_link_rejects_an_unregistered_provider() -> None:
    with pytest.raises(ValueError, match="Unsupported bulletin_provider"):
        _build_bulletin_link("no_bulletin", "https://example.org")


def test_build_latest_other_bulletin_links(monkeypatch) -> None:
    pdf = "https://example.org/bulletins/2026-02-16.pdf"

    def fake_resolve(*, homepage_url: str, reference_date, page, recipe=None) -> Resolution:
        assert homepage_url == "https://example.org"
        assert reference_date == date(2026, 2, 19)
        return Resolution(
            candidate=Candidate(source_url=pdf, fetch_url=pdf, parsed_date=date(2026, 2, 16)),
            page_url="https://example.org/bulletins", collector="page-pdfs", reason=CURRENT,
        )

    monkeypatch.setattr("pdf_extract.fetch.resolve_parish_site", fake_resolve)
    link = build_latest_other_bulletin_links(
        provider_id="https://example.org",
        reference_date=date(2026, 2, 19),
        page=object(),
    )
    assert link.source_url == pdf
    assert link.fetch_url == pdf
    assert link.how == "page-pdfs on https://example.org/bulletins: current"


def test_find_other_bulletin_page_url_prefers_href_and_text_match() -> None:
    class FakeAnchor:
        def __init__(self, href: str, text: str):
            self._href = href
            self._text = text

        def get_attribute(self, name: str):
            if name == "href":
                return self._href
            return None

        def inner_text(self):
            return self._text

    class FakePage:
        def query_selector_all(self, selector: str):
            assert selector == "a[href]"
            return [
                FakeAnchor("/news", "Parish News"),
                FakeAnchor("/weekly", "Weekly Bulletin"),
                FakeAnchor("/bulletins", "Read Bulletins"),
            ]

    resolved = find_bulletin_page_urls(page=FakePage(), base_url="https://example.org")[0]
    assert resolved == "https://example.org/bulletins"


def test_resolve_other_latest_link_prefers_latest_parseable_within_plus_minus_week() -> None:
    class FakeAnchor:
        def __init__(self, href: str, text: str):
            self._href = href
            self._text = text

        def get_attribute(self, name: str):
            if name == "href":
                return self._href
            return None

        def inner_text(self):
            return self._text

    class FakePage:
        def __init__(self):
            self.url = ""

        def goto(self, url: str, wait_until: str) -> None:
            assert wait_until == "domcontentloaded"
            self.url = url

        def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
            assert selector == "a[href]"
            assert timeout == 15000

        def query_selector_all(self, selector: str):
            assert selector == "a[href]"
            if self.url == "https://example.org":
                return [
                    FakeAnchor("/weekly", "Weekly"),
                    FakeAnchor("/bulletins", "Bulletin Archive"),
                ]
            assert self.url == "https://example.org/bulletins"
            return [
                FakeAnchor("/pdfs/old-2026-01-10.pdf", "Jan 10, 2026 Bulletin"),
                FakeAnchor("/pdfs/new-2026-02-18.pdf", "Feb 18, 2026 Bulletin"),
                FakeAnchor("/pdfs/future-2026-03-10.pdf", "Mar 10, 2026 Bulletin"),
            ]

    source_url, fetch_url = _resolve_other(
        provider_id="https://example.org",
        reference_date=date(2026, 2, 19),
        page=FakePage(),
    )
    assert source_url == "https://example.org/pdfs/new-2026-02-18.pdf"
    assert fetch_url == "https://example.org/pdfs/new-2026-02-18.pdf"


def test_resolve_other_latest_link_falls_back_to_first_pdf_when_no_date_match() -> None:
    class FakeAnchor:
        def __init__(self, href: str, text: str):
            self._href = href
            self._text = text

        def get_attribute(self, name: str):
            if name == "href":
                return self._href
            return None

        def inner_text(self):
            return self._text

    class FakePage:
        def __init__(self):
            self.url = ""

        def goto(self, url: str, wait_until: str) -> None:
            self.url = url

        def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
            assert selector == "a[href]"
            assert timeout == 15000

        def query_selector_all(self, selector: str):
            assert selector == "a[href]"
            if self.url == "https://example.org":
                return [FakeAnchor("/bulletins", "Bulletin Archive")]
            return [
                FakeAnchor("/pdfs/no-date-1.pdf", "This Week"),
                FakeAnchor("/pdfs/no-date-2.pdf", "Latest PDF"),
            ]

    source_url, fetch_url = _resolve_other(
        provider_id="https://example.org",
        reference_date=date(2026, 2, 19),
        page=FakePage(),
    )
    assert source_url == "https://example.org/pdfs/no-date-1.pdf"
    assert fetch_url == "https://example.org/pdfs/no-date-1.pdf"


def test_resolve_other_latest_link_finds_pdf_embedded_in_script_on_post_page() -> None:
    """Mirrors the elmiracatholic.org layout: the per-week post page does not
    expose the bulletin PDF as an <a> or <iframe>; it is embedded as a JSON
    string (JSON-escaped slashes) inside a WordPress dflip / 3D FlipBook script.
    The resolver should still pick it up via the rendered HTML.
    """

    class FakeAnchor:
        def __init__(self, href: str, text: str):
            self._href = href
            self._text = text

        def get_attribute(self, name: str):
            if name == "href":
                return self._href
            return None

        def inner_text(self):
            return self._text

    listing_url = "https://elmiracatholic.org/news-bulletins/"
    latest_post_url = "https://elmiracatholic.org/2026/04/16/april-19-2026-bulletin/"
    expected_pdf_url = (
        "https://elmiracatholic.org/wp-content/uploads/2026/04/"
        "ElmiraCatholicChurchesBulletin-4-19-2026.pdf"
    )
    dflip_script = (
        '<div class="_df_book" id="df_10896"></div>'
        '<script class="df-shortcode-script" type="application/javascript">'
        'window.option_df_10896 = {"source":'
        '"https:\\/\\/elmiracatholic.org\\/wp-content\\/uploads\\/2026\\/04\\/'
        'ElmiraCatholicChurchesBulletin-4-19-2026.pdf","wpOptions":"true"};'
        '</script>'
    )

    class FakePage:
        def __init__(self):
            self.url = ""

        def goto(self, url: str, wait_until: str) -> None:
            assert wait_until == "domcontentloaded"
            self.url = url

        def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
            assert selector == "a[href]"
            assert timeout == 15000

        def query_selector_all(self, selector: str):
            if selector == "iframe[src]":
                return []
            assert selector == "a[href]"
            if self.url == "https://elmiracatholic.org":
                return [FakeAnchor("/news-bulletins/", "News/Bulletins")]
            if self.url == listing_url:
                return [
                    FakeAnchor(latest_post_url, "April 19, 2026 Bulletin"),
                ]
            assert self.url == latest_post_url
            return [FakeAnchor("https://elmiracatholic.org/", "Home")]

        def content(self) -> str:
            if self.url == latest_post_url:
                return f"<html><body>{dflip_script}</body></html>"
            return "<html><body></body></html>"

    source_url, fetch_url = _resolve_other(
        provider_id="https://elmiracatholic.org",
        reference_date=date(2026, 4, 17),
        page=FakePage(),
    )
    assert source_url == expected_pdf_url
    assert fetch_url == expected_pdf_url


def test_resolve_other_latest_link_descends_into_latest_bulletin_post_when_no_pdfs() -> None:
    """Listing pages that link to dated bulletin *posts* (not PDFs) should resolve
    by navigating into the latest-dated post and collecting the PDF there.

    Mirrors the elmiracatholic.org WordPress-style layout where /news-bulletins/
    lists permalink posts like /2026/04/16/april-192026-bulletin/ which wrap
    the actual PDF.
    """

    class FakeAnchor:
        def __init__(self, href: str, text: str):
            self._href = href
            self._text = text

        def get_attribute(self, name: str):
            if name == "href":
                return self._href
            return None

        def inner_text(self):
            return self._text

    listing_url = "https://elmiracatholic.org/news-bulletins/"
    latest_post_url = "https://elmiracatholic.org/2026/04/16/april-19-2026-bulletin/"
    older_post_url = "https://elmiracatholic.org/2026/04/09/april-12-2026-bulletin/"
    latest_pdf_url = (
        "https://elmiracatholic.org/wp-content/uploads/2026/04/"
        "ElmiraCatholicChurchesBulletin-4-19-2026.pdf"
    )

    class FakePage:
        def __init__(self):
            self.url = ""

        def goto(self, url: str, wait_until: str) -> None:
            assert wait_until == "domcontentloaded"
            self.url = url

        def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
            assert selector == "a[href]"
            assert timeout == 15000

        def query_selector_all(self, selector: str):
            if selector == "iframe[src]":
                return []
            assert selector == "a[href]"
            if self.url == "https://elmiracatholic.org":
                return [FakeAnchor("/news-bulletins/", "News/Bulletins")]
            if self.url == listing_url:
                return [
                    FakeAnchor(listing_url, "News/Bulletins"),
                    FakeAnchor(latest_post_url, "April 19, 2026 Bulletin"),
                    FakeAnchor(older_post_url, "April 12, 2026 Bulletin"),
                    FakeAnchor("/category/bulletin/", "Bulletin"),
                ]
            assert self.url == latest_post_url
            return [FakeAnchor(latest_pdf_url, "Download Bulletin")]

    source_url, fetch_url = _resolve_other(
        provider_id="https://elmiracatholic.org",
        reference_date=date(2026, 4, 17),
        page=FakePage(),
    )
    assert source_url == latest_pdf_url
    assert fetch_url == latest_pdf_url


def test_parse_relaxed_date_handles_multiple_formats() -> None:
    ref = date(2026, 2, 19)
    assert parse_date("Bulletin Feb 18, 2026", ref) == date(2026, 2, 18)
    assert parse_date("Bulletin 02/18/26", ref) == date(2026, 2, 18)
    assert parse_date("Bulletin 2026-02-18", ref) == date(2026, 2, 18)


def test_normalize_url_for_request_encodes_spaces() -> None:
    raw = "https://s3-us-west-2.amazonaws.com/classrooms.stritawebster.org/Bulletins/2026/March 22.pdf"
    normalized = _normalize_url_for_request(raw)
    assert normalized.endswith("/March%2022.pdf")


def test_goto_with_retry_on_interrupted_navigation() -> None:
    class FakePage:
        def __init__(self) -> None:
            self.calls = 0
            self.waits = 0

        def goto(self, page_url: str, wait_until: str) -> None:
            self.calls += 1
            assert page_url == "https://example.org/page"
            assert wait_until == "domcontentloaded"
            if self.calls == 1:
                raise Exception(
                    'Page.goto: Navigation to "https://example.org/page" is interrupted by another navigation'
                )

        def wait_for_timeout(self, ms: int) -> None:
            assert ms == 250
            self.waits += 1

    page = FakePage()
    goto_with_retry(page=page, page_url="https://example.org/page")
    assert page.calls == 2
    assert page.waits == 1


def test_resolve_fetch_source_discover_mass_uses_provider_id() -> None:
    parish = {
        "bulletin_provider": DISCOVER_MASS_TYPE,
        "provider_id": "st-joseph-rush",
        "homepage_url": "https://stjoseph.example.org",
    }
    assert _resolve_fetch_source(parish) == FetchSource(DISCOVER_MASS_TYPE, "st-joseph-rush")


def test_resolve_fetch_source_discover_mass_without_provider_id_returns_none() -> None:
    parish = {
        "bulletin_provider": DISCOVER_MASS_TYPE,
        "provider_id": "",
        "homepage_url": "https://stjoseph.example.org",
    }
    assert _resolve_fetch_source(parish) is None


class _EcatholicFakePage:
    """Page whose bulletin anchors exist but never become visible."""

    def __init__(self, *, hrefs, html="", raise_on_wait=True):
        self._hrefs = hrefs
        self._html = html
        self._raise_on_wait = raise_on_wait
        self.goto_calls = 0
        self.settle_waits = 0
        self.wait_states: list[str | None] = []

    def goto(self, url: str, wait_until: str) -> None:
        assert url == "https://stjeromerochester.org/bulletins"
        assert wait_until == "domcontentloaded"
        self.goto_calls += 1

    def wait_for_selector(self, selector: str, timeout: int, state=None) -> None:
        self.wait_states.append(state)
        if self._raise_on_wait:
            raise TimeoutError("Timeout 15000ms exceeded")

    def query_selector_all(self, selector: str):
        assert selector == "a[href*='files.ecatholic.com']"

        class _Anchor:
            def __init__(self, href):
                self._href = href

            def get_attribute(self, name: str):
                return self._href if name == "href" else None

        return [_Anchor(href) for href in self._hrefs]

    def content(self) -> str:
        return self._html

    def wait_for_timeout(self, timeout: int) -> None:
        self.settle_waits += 1


def test_resolve_ecatholic_latest_link_uses_hidden_anchors() -> None:
    page = _EcatholicFakePage(
        hrefs=[
            "https://files.ecatholic.com/22370/bulletins/20260809.pdf?t=1",
            "https://files.ecatholic.com/22370/bulletins/20260823.pdf?t=3",
            "https://files.ecatholic.com/22370/bulletins/20260816.pdf?t=2",
            "/about-us",
        ],
    )

    source_url, fetch_url = _resolve_ecatholic_latest_link(
        provider_id="https://stjeromerochester.org",
        page=page,
    )

    # A visibility timeout must not stop us reading anchors that are attached.
    assert page.wait_states == ["attached"]
    assert page.goto_calls == 1
    assert source_url == "https://files.ecatholic.com/22370/bulletins/20260823.pdf?t=3"
    assert fetch_url == source_url


def test_resolve_ecatholic_latest_link_falls_back_to_page_html() -> None:
    page = _EcatholicFakePage(
        hrefs=[],
        html=(
            '<script>window.viewer = {"file":'
            '"https:\\/\\/files.ecatholic.com\\/22370\\/bulletins\\/20260823.pdf?t=9"};'
            "</script>"
        ),
    )

    source_url, _ = _resolve_ecatholic_latest_link(
        provider_id="https://stjeromerochester.org",
        page=page,
    )
    assert source_url == "https://files.ecatholic.com/22370/bulletins/20260823.pdf?t=9"


def test_resolve_ecatholic_latest_link_reloads_then_raises_when_page_is_empty() -> None:
    page = _EcatholicFakePage(hrefs=[], html="<html><body>No bulletins yet</body></html>")

    try:
        _resolve_ecatholic_latest_link(
            provider_id="https://stjeromerochester.org",
            page=page,
        )
    except ValueError as exc:
        assert "ecatholic provider_id=https://stjeromerochester.org" in str(exc)
    else:
        raise AssertionError("Expected ValueError when no bulletin PDF is found")

    assert page.goto_calls == 2
    assert page.settle_waits == 1


def test_pick_latest_ecatholic_pdf_url_prefers_newest_date() -> None:
    urls = [
        "https://files.ecatholic.com/1/bulletins/20260705.pdf",
        "https://files.ecatholic.com/1/bulletins/20260823.pdf?t=5",
        "https://files.ecatholic.com/1/bulletins/20260816.pdf",
    ]
    assert _pick_latest_ecatholic_pdf_url(urls) == urls[1]

    undated = ["https://files.ecatholic.com/1/bulletins/weekly.pdf", "https://x/2.pdf"]
    assert _pick_latest_ecatholic_pdf_url(undated) == undated[0]


def test_parse_ecatholic_pdf_date() -> None:
    assert _parse_ecatholic_pdf_date(
        "https://files.ecatholic.com/1/bulletins/20260823.pdf?t=1"
    ) == date(2026, 8, 23)
    assert _parse_ecatholic_pdf_date("https://files.ecatholic.com/1/bulletins/latest.pdf") is None
    assert _parse_ecatholic_pdf_date("https://files.ecatholic.com/1/bulletins/20261332.pdf") is None


def test_report_stale_parishes_names_parishes_stuck_on_old_bulletins() -> None:
    fresh = utc_now_iso()
    bulletins = [
        {"parish_slug": "fresh-parish", "fetched_at": fresh},
        {"parish_slug": "stale-parish", "fetched_at": "2026-01-01T00:00:00Z"},
    ]
    stale = _report_stale_parishes(
        bulletins=bulletins,
        slugs=["fresh-parish", "stale-parish", "never-fetched-parish"],
    )
    assert stale == ["stale-parish", "never-fetched-parish"]
