"""Check what the fetch stage resolves for each parish, live or from recorded pages.

`fetch` only learns a parish failed when a weekly run reports it, and a change
to a resolver can fix one site and quietly break another. This module makes
the resolvers testable against real sites without a network or a browser:

- `check_fetch` runs each parish's resolver in the real browser, downloads
  what it resolves to, and reports per parish whether a PDF came back. With a
  record directory it also saves every page the resolver read.
- `SnapshotPage` replays those saved pages: a `PageLike` whose `goto` serves
  the recorded HTML, so tests can run a resolver offline and check it still
  picks the same bulletin it picked when the pages were recorded.

Nothing here touches the database or the blob store.
"""

from __future__ import annotations

import csv
import gzip
import json
import logging
import re
from collections import Counter
from collections.abc import Collection, Iterable
from dataclasses import dataclass, field
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError

from pdf_extract import fetch
from pdf_extract.browser import PageLike, launch_stealth_browser
from pdf_extract.parish_sites import Recipe
from pdf_extract.parish_sites.dates import parse_date
from pdf_extract.parish_sites.links import decoded_base64_json
from pdf_extract.storage import PARISHES_CSV_PATH

LOGGER = logging.getLogger(__name__)

SNAPSHOT_SUFFIX = ".json.gz"


# ── Replaying recorded pages ────────────────────────────────────────────────

class SnapshotMissing(Exception):
    """The resolver asked for a page that was not recorded."""


_VOID_TAGS = frozenset({
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
    "param", "source", "track", "wbr",
})
_TEXTLESS_TAGS = frozenset({"script", "style", "noscript", "template"})


@dataclass
class SnapshotElement:
    """An element of a recorded page: enough of Playwright's ElementHandle for the resolvers."""

    tag: str
    attrs: dict[str, str]
    _text: list[str] = field(default_factory=list)

    def get_attribute(self, name: str) -> str | None:
        return self.attrs.get(name)

    def inner_text(self) -> str:
        return re.sub(r"\s+", " ", "".join(self._text)).strip()

    def text_content(self) -> str | None:
        return "".join(self._text)


class _ElementCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[SnapshotElement] = []
        self._open: list[SnapshotElement] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        element = SnapshotElement(tag=tag, attrs={k: v or "" for k, v in attrs})
        self.elements.append(element)
        if tag not in _VOID_TAGS:
            self._open.append(element)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.elements.append(SnapshotElement(tag=tag, attrs={k: v or "" for k, v in attrs}))

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self._open) - 1, -1, -1):
            if self._open[i].tag == tag:
                del self._open[i:]
                return

    def handle_data(self, data: str) -> None:
        if any(e.tag in _TEXTLESS_TAGS for e in self._open):
            return
        for element in self._open:
            element._text.append(data)


# One compound selector: an optional tag, an optional #id, then [attr] tests.
_COMPOUND = re.compile(
    r"^(?P<tag>[a-zA-Z][\w-]*|\*)?(?:#(?P<id>[\w-]+))?(?P<attrs>(?:\[[^\]]+\])*)$"
)
_ATTR_TEST = re.compile(
    r"\[\s*(?P<name>[\w:-]+)\s*"
    r"(?:(?P<op>[*^$]?=)\s*(?P<quote>['\"]?)(?P<value>.*?)(?P=quote))?\s*\]"
)


def _selector_matches(selector: str, element: SnapshotElement) -> bool:
    for part in selector.split(","):
        match = _COMPOUND.match(part.strip())
        if match is None:
            raise ValueError(f"SnapshotPage cannot evaluate selector {selector!r}")
        tag = match.group("tag")
        if tag and tag != "*" and tag.lower() != element.tag:
            continue
        if match.group("id") and element.attrs.get("id") != match.group("id"):
            continue
        if all(_attr_matches(t, element) for t in _ATTR_TEST.finditer(match.group("attrs"))):
            return True
    return False


def _attr_matches(test: re.Match[str], element: SnapshotElement) -> bool:
    actual = element.attrs.get(test.group("name").lower())
    if actual is None:
        return False
    op, value = test.group("op"), test.group("value")
    if op is None:
        return True
    return {
        "=": actual == value,
        "*=": value in actual,
        "^=": actual.startswith(value),
        "$=": actual.endswith(value),
    }[op]


@dataclass(frozen=True)
class PageSnapshot:
    requested_url: str
    final_url: str
    html: str


def _url_key(url: str) -> str:
    return url.rstrip("/").lower()


@dataclass(frozen=True)
class _SourceResponse:
    body: str

    def text(self) -> str:
        return self.body


class _SnapshotRequest:
    def __init__(self, sources: dict[str, str]) -> None:
        self._sources = {_url_key(url): html for url, html in sources.items()}

    def get(self, url: str) -> _SourceResponse:
        html = self._sources.get(_url_key(url))
        if html is None:
            raise SnapshotMissing(f"No recorded source for {url}; re-record this parish")
        return _SourceResponse(html)


class SnapshotPage:
    """A `PageLike` that serves recorded pages instead of the network.

    `sources` are pages as the server sent them, before any script ran, for
    resolvers that read one through `page.request`.
    """

    def __init__(
        self, snapshots: Iterable[PageSnapshot], sources: dict[str, str] | None = None,
    ) -> None:
        self.request = _SnapshotRequest(sources or {})
        self._by_url = {_url_key(s.requested_url): s for s in snapshots}
        self._current: PageSnapshot | None = None
        self._elements: list[SnapshotElement] = []

    def goto(self, url: str, wait_until: str = "load", timeout: float = 0) -> None:
        snapshot = self._by_url.get(_url_key(url))
        if snapshot is None:
            raise SnapshotMissing(f"No recorded page for {url}; re-record this parish")
        self._current = snapshot
        collector = _ElementCollector()
        collector.feed(snapshot.html)
        collector.close()
        self._elements = collector.elements

    def wait_for_selector(self, selector: str, timeout: int, state: str | None = None) -> None:
        if not self.query_selector_all(selector):
            raise TimeoutError(f"Timeout {timeout}ms waiting for {selector!r}")

    def query_selector_all(self, selector: str) -> list[SnapshotElement]:
        return [e for e in self._elements if _selector_matches(selector, e)]

    def content(self) -> str:
        return self._current.html if self._current else ""

    def wait_for_timeout(self, timeout: int) -> None:
        return None

    @property
    def url(self) -> str:
        return self._current.final_url if self._current else ""


# ── Recording pages ─────────────────────────────────────────────────────────

# Recorded pages keep what a resolver could read (links, iframes, scripts that
# embed a PDF viewer's settings) and drop the bulk that no resolver looks at.
_STRIP_PATTERNS = [
    re.compile(r"<style\b.*?</style>", re.IGNORECASE | re.DOTALL),
    re.compile(r"<svg\b.*?</svg>", re.IGNORECASE | re.DOTALL),
    re.compile(r"<!--.*?-->", re.DOTALL),
    re.compile(r"<(?:link|meta)\b[^>]*>", re.IGNORECASE),
]
_SCRIPT = re.compile(r"<script\b.*?</script\b[^>]*>", re.IGNORECASE | re.DOTALL)


def _slim_html(html: str) -> str:
    for pattern in _STRIP_PATTERNS:
        html = pattern.sub("", html)
    # A script can hold a PDF URL (flipbook viewers), in plain sight or in
    # base64 JSON (3D FlipBook); any other is dead weight.
    return _SCRIPT.sub(
        lambda m: m.group(0)
        if ".pdf" in m.group(0).lower() or decoded_base64_json(m.group(0)) else "",
        html,
    )


class _RecordingRequest:
    def __init__(self, page: PageLike, sources: dict[str, str]) -> None:
        self._page = page
        self._sources = sources

    def get(self, url: str) -> _SourceResponse:
        html = self._page.request.get(url).text()
        self._sources[url] = _slim_html(html)
        return _SourceResponse(html)


class RecordingPage:
    """Wraps a live page and keeps what the resolver saw on each page it opened."""

    def __init__(self, page: PageLike) -> None:
        self._page = page
        self._requested: str | None = None
        self.snapshots: dict[str, PageSnapshot] = {}
        self.sources: dict[str, str] = {}
        self.request = _RecordingRequest(page, self.sources)

    def _record(self) -> None:
        if self._requested is None:
            return
        try:
            html = self._page.content()
        except Exception:
            return
        self.snapshots[_url_key(self._requested)] = PageSnapshot(
            requested_url=self._requested, final_url=self._page.url, html=_slim_html(html),
        )

    def goto(self, url: str, wait_until: str = "load", timeout: float = 30000) -> None:
        self._requested = url
        self._page.goto(url, wait_until=wait_until)
        self._record()

    def wait_for_selector(self, selector: str, timeout: int, state: str | None = None) -> None:
        try:
            if state is None:
                self._page.wait_for_selector(selector, timeout=timeout)
            else:
                self._page.wait_for_selector(selector, timeout=timeout, state=state)
        finally:
            self._record()

    def query_selector_all(self, selector: str):  # type: ignore[no-untyped-def]
        self._record()
        return self._page.query_selector_all(selector)

    def content(self) -> str:
        self._record()
        return self._page.content()

    def wait_for_timeout(self, timeout: int) -> None:
        self._page.wait_for_timeout(timeout)

    @property
    def url(self) -> str:
        return self._page.url


def save_recording(
    path: Path, *, slug: str, provider: str, provider_id: str, reference_date: date,
    snapshots: Iterable[PageSnapshot], sources: dict[str, str] | None = None,
    recipe: str = "",
) -> None:
    payload: dict[str, object] = {
        "slug": slug,
        "provider": provider,
        "provider_id": provider_id,
        "reference_date": reference_date.isoformat(),
        "pages": [
            {"requested_url": s.requested_url, "final_url": s.final_url, "html": s.html}
            for s in snapshots
        ],
    }
    if sources:
        payload["sources"] = sources
    if recipe:
        payload["recipe"] = recipe
    path.parent.mkdir(parents=True, exist_ok=True)
    # mtime=0 keeps a re-recording of unchanged pages byte-identical.
    with open(path, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
        gz.write(json.dumps(payload, indent=1, sort_keys=True).encode())


@dataclass(frozen=True)
class Recording:
    slug: str
    provider: str
    provider_id: str
    reference_date: date
    snapshots: list[PageSnapshot]
    sources: dict[str, str] = field(default_factory=dict)
    # The parish's recipe when it was recorded. A recipe added since is read
    # from parishes.csv by the replay test.
    recipe: str = ""

    def page(self) -> SnapshotPage:
        return SnapshotPage(self.snapshots, self.sources)

    def resolve(self, *, recipe: str | None = None) -> fetch.BulletinLink:
        """Run today's resolver for this parish against the recorded pages."""
        return _resolve(
            fetch.FetchSource(
                self.provider, self.provider_id, self.recipe if recipe is None else recipe,
            ),
            page=self.page(), reference_date=self.reference_date,
        )


def _resolve(
    source: fetch.FetchSource, *, page: PageLike, reference_date: date,
) -> fetch.BulletinLink:
    return fetch._build_bulletin_link(
        source.provider, source.provider_id, page=page, recipe=source.recipe,
        reference_date=reference_date,
    )


def load_recording(path: Path) -> Recording:
    with gzip.open(path, "rt") as fh:
        payload = json.load(fh)
    return Recording(
        slug=payload["slug"],
        provider=payload["provider"],
        provider_id=payload["provider_id"],
        reference_date=date.fromisoformat(payload["reference_date"]),
        snapshots=[PageSnapshot(**p) for p in payload["pages"]],
        sources=payload.get("sources", {}),
        recipe=payload.get("recipe", ""),
    )


# ── Live check ──────────────────────────────────────────────────────────────

OK = "ok"
RESOLVE_FAILED = "resolve_failed"
DOWNLOAD_FAILED = "download_failed"
NOT_PDF = "not_pdf"
# Cloudflare challenged the browser instead of serving the site. The weekly
# run's browser usually gets through, so this says nothing about the resolver.
BLOCKED = "blocked"

_CHALLENGE_TITLE = re.compile(r"<title>\s*Just a moment", re.IGNORECASE)


def _challenged(page: PageLike) -> bool:
    try:
        return bool(_CHALLENGE_TITLE.search(page.content()))
    except Exception:
        return False


def _fetch_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Rows in the parishes.csv layout, keyed the way the fetch stage reads the parish table."""
    return [{**row, "homepage_url": row["website"]} for row in rows]


def _read_parishes(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as fh:
        return _fetch_rows(csv.DictReader(fh))


def _same_recipe(recipe: str, source: fetch.FetchSource) -> bool:
    """Whether `recipe` reads the parish's site the way its recorded one does."""
    try:
        recorded = Recipe.parse(source.recipe, website=source.provider_id)
    except ValueError:
        return False
    return Recipe.parse(recipe, website=source.provider_id) == recorded


def _check_one(
    slug: str, source: fetch.FetchSource, page: PageLike, *,
    reference_date: date, download: bool,
) -> dict[str, object]:
    result: dict[str, object] = {"slug": slug, "provider": source.provider}
    try:
        link = _resolve(source, page=page, reference_date=reference_date)
    except Exception as exc:
        status = BLOCKED if _challenged(page) else RESOLVE_FAILED
        result.update(status=status, detail=f"{type(exc).__name__}: {exc}")
        return result
    result["source_url"] = link.source_url
    if link.how:
        result["how"] = link.how
    # A recipe that would pin what the resolver guessed: copy it into the
    # parish's provider_id once the pick is right.
    if link.recipe and not _same_recipe(link.recipe, source):
        result["recipe"] = link.recipe
    if link.fetch_url != link.source_url:
        result["fetch_url"] = link.fetch_url
    url_date = parse_date(link.source_url, reference_date)
    if url_date is not None:
        result["url_date"] = url_date.isoformat()
    if not download:
        result["status"] = OK
        return result
    try:
        pdf = fetch._download_pdf(fetch_url=link.fetch_url, source_url=link.source_url)
    except (HTTPError, URLError, OSError) as exc:
        result.update(status=DOWNLOAD_FAILED, detail=f"{type(exc).__name__}: {exc}")
        return result
    result["bytes"] = len(pdf)
    result["status"] = OK if pdf[:5] == b"%PDF-" else NOT_PDF
    return result


def check_fetch(
    *,
    slugs: Collection[str] | None = None,
    providers: Collection[str] | None = None,
    record_dir: Path | None = None,
    download: bool = True,
    reference_date: date | None = None,
    parishes: Iterable[dict[str, str]] | None = None,
) -> dict[str, object]:
    """Resolve (and download) each parish's latest bulletin without saving it.

    Returns one row per parish with its status, so a resolver change can be
    compared site by site with the run before it. With `record_dir`, the pages
    each resolver read are saved there as `<slug>.json.gz` for `SnapshotPage`.
    `parishes` (rows in the parishes.csv layout, such as a diocese's records
    before promotion) defaults to data/parishes.csv.
    """
    today = reference_date or date.today()
    all_parishes = (
        _read_parishes(PARISHES_CSV_PATH) if parishes is None else _fetch_rows(parishes)
    )
    missing = sorted(set(slugs or ()) - {p["slug"] for p in all_parishes})
    if missing:
        raise ValueError(f"Parish not found: {', '.join(missing)}")
    to_check = [
        p for p in all_parishes
        if fetch._resolve_fetch_source(p) is not None
        and (slugs is None or p["slug"] in slugs)
        and (providers is None or p["bulletin_provider"] in providers)
    ]

    rows: list[dict[str, object]] = []
    with launch_stealth_browser() as live_page:
        for parish in to_check:
            slug = parish["slug"]
            source = fetch._resolve_fetch_source(parish)
            assert source is not None
            page = RecordingPage(live_page) if record_dir else None
            row = _check_one(
                slug, source, page or live_page, reference_date=today, download=download,
            )
            LOGGER.info("%s: %s %s", slug, row["status"], row.get("source_url", row.get("detail")))
            rows.append(row)
            # A challenge page is not the site: keep any earlier recording instead.
            if record_dir and page is not None and row["status"] != BLOCKED:
                save_recording(
                    record_dir / f"{slug}{SNAPSHOT_SUFFIX}",
                    slug=slug, provider=source.provider, provider_id=source.provider_id,
                    reference_date=today, snapshots=page.snapshots.values(),
                    sources=page.sources, recipe=source.recipe,
                )

    counts = Counter(str(row["status"]) for row in rows)
    return {"reference_date": today.isoformat(), "counts": dict(counts), "parishes": rows}
