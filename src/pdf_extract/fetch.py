"""Bulletin fetch pipeline: resolve provider links, download PDFs, record bulletins."""

from __future__ import annotations

import logging
import queue
import re
import threading
import time
from collections import Counter, deque
from collections.abc import Callable, Collection, Iterator
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import dataclass
from datetime import date
from http import HTTPStatus
from typing import Any, NamedTuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

from pdf_extract.blobstore import CachedBlobStore, bulletin_pdf_key, get_store
from pdf_extract.browser import (
    PageLike,
    goto_with_retry,
    launch_stealth_browser,
    wait_for_selector_quietly,
)
from pdf_extract.bulletin_week import (
    STALE_BULLETIN_AGE_DAYS,
    bulletin_reference_date,
    bulletin_week,
    has_bulletin_for,
    nearest_sunday,
    newest_bulletin,
    stale_parishes,
)
from pdf_extract.duplicates import (
    Duplicate,
    Validators,
    bulletin_hash,
    find_duplicate,
    validators_for,
)
from pdf_extract.parish_sites import Recipe, resolve_parish_site
from pdf_extract.parish_sites.dates import safe_date
from pdf_extract.pdf_compact import compact_bulletin_pdf
from pdf_extract.runs import (
    FETCH_CURRENT,
    FETCH_DOWNLOAD_FAILED,
    FETCH_NEW,
    FETCH_RECHECK_FAILED,
    FETCH_RESOLVE_FAILED,
    FETCH_SAVE_FAILED,
    FETCH_UNCHANGED,
    join_details,
    record_parish_result,
)
from pdf_extract.storage import (
    connect_db,
    get_parish_by_name,
    insert_bulletin,
    list_parishes,
    load_bulletins,
    mark_bulletin_seen,
    utc_now_iso,
)

ECATHOLIC_BULLETINS_PATH = "/bulletins"
ECATHOLIC_FILES_HOST = "files.ecatholic.com"
ECATHOLIC_ANCHOR_SELECTOR = f"a[href*='{ECATHOLIC_FILES_HOST}']"
ECATHOLIC_TYPE = "ecatholic"
PARISHES_ONLINE_TYPE = "parishes_online"
DISCOVER_MASS_TYPE = "discover_mass"
OTHER_TYPE = "other"
GOOGLE_DRIVE_TYPE = "google_drive"
PARISHES_ONLINE_ORG_URL_TEMPLATE = "https://parishesonline.com/organization/{provider_id}"
DISCOVER_MASS_BULLETIN_URL_TEMPLATE = "https://discovermass.com/church/{provider_id}/"

# Per-request timeout for direct PDF downloads over HTTP.
HTTP_DOWNLOAD_TIMEOUT_SECONDS = 60
# eCatholic bulletin pages keep their PDF links in an archive panel that is
# often attached but not visible, and sometimes only populated after the first
# render. When a pass finds nothing, reload once after a short settle.
ECATHOLIC_RESOLVE_ATTEMPTS = 2
ECATHOLIC_SETTLE_DELAY_MS = 2000
# Wait before the one retry of a download answered 429 (Too Many Requests).
HTTP_429_RETRY_SECONDS = 10

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class BulletinLink:
    source_url: str
    fetch_url: str
    # How the resolver came to this link, for the run report; empty when the
    # provider has only one way.
    how: str = ""
    # For a resolver that can guess: the recipe that pins the way it found
    # this link (see parish_sites.Recipe).
    recipe: str = ""


# ── eCatholic bulletin resolution ───────────────────────────────────────────

def build_latest_ecatholic_bulletin_links(
    *, provider_id: str, reference_date: date | None = None, page: PageLike | None = None,
) -> BulletinLink:
    _ = reference_date
    source_url, fetch_url = _resolve_ecatholic_latest_link(provider_id=provider_id, page=page)
    return BulletinLink(source_url=source_url, fetch_url=fetch_url)


def _ecatholic_bulletins_url(site_url: str) -> str:
    """The site's bulletins page; a website recorded as that page already is kept."""
    base = site_url.rstrip("/")
    if base.lower().endswith(ECATHOLIC_BULLETINS_PATH):
        return base
    return urljoin(base + "/", ECATHOLIC_BULLETINS_PATH.lstrip("/"))


def _resolve_ecatholic_latest_link(
    *, provider_id: str, page: PageLike | None = None,
) -> tuple[str, str]:
    bulletins_url = _ecatholic_bulletins_url(provider_id)
    source_label = f"ecatholic provider_id={provider_id}"

    def _run(p: PageLike) -> tuple[str, str]:
        LOGGER.info("Resolving latest anchor link (%s)", source_label)
        LOGGER.info("Visiting page URL: %s", bulletins_url)
        for attempt in range(1, ECATHOLIC_RESOLVE_ATTEMPTS + 1):
            goto_with_retry(page=p, page_url=bulletins_url)
            # Wait on "attached", not the default "visible": these links live in
            # a collapsed archive panel on most eCatholic themes, so requiring
            # visibility times out on a page that already has what we need.
            wait_for_selector_quietly(
                page=p,
                selector=ECATHOLIC_ANCHOR_SELECTOR,
                state="attached",
                source_label=source_label,
            )
            pdf_urls = _collect_ecatholic_pdf_urls(page=p, base_url=bulletins_url)
            if pdf_urls:
                latest = _pick_latest_ecatholic_pdf_url(pdf_urls)
                LOGGER.info("Resolved latest anchor link (%s)", source_label)
                return latest, latest
            if attempt < ECATHOLIC_RESOLVE_ATTEMPTS:
                LOGGER.warning(
                    "No eCatholic bulletin PDF on %s (attempt %d/%d), reloading",
                    bulletins_url, attempt, ECATHOLIC_RESOLVE_ATTEMPTS,
                )
                p.wait_for_timeout(ECATHOLIC_SETTLE_DELAY_MS)
        raise ValueError(f"No matching anchor link found for {source_label} at {bulletins_url}")

    if page is not None:
        return _run(page)
    with launch_stealth_browser() as p:
        return _run(p)


def _collect_ecatholic_pdf_urls(*, page: PageLike, base_url: str) -> list[str]:
    """Collect every eCatholic bulletin PDF URL the page exposes, in DOM order."""
    urls: list[str] = []
    seen: set[str] = set()

    def _add(raw_href: str) -> None:
        extracted = _extract_ecatholic_pdf_url_from_href(href=raw_href, base_url=base_url)
        if extracted is None:
            return
        url = extracted[0]
        if url in seen:
            return
        seen.add(url)
        urls.append(url)

    for anchor in page.query_selector_all(ECATHOLIC_ANCHOR_SELECTOR):
        href = anchor.get_attribute("href")
        if isinstance(href, str):
            _add(href)
    if urls:
        return urls

    # Some eCatholic themes hand the bulletin to a script-driven viewer instead
    # of a plain anchor, leaving the PDF URL only in the rendered markup.
    for raw in _find_ecatholic_pdf_urls_in_html(page=page):
        _add(raw)
    return urls


_ECATHOLIC_HTML_PDF_URL_PATTERN = re.compile(
    rf"https?://{re.escape(ECATHOLIC_FILES_HOST)}/[^\s\"'<>\\]+?\.pdf(?:\?[^\s\"'<>\\]*)?",
    flags=re.IGNORECASE,
)


def _find_ecatholic_pdf_urls_in_html(*, page: PageLike) -> list[str]:
    try:
        html = page.content()
    except Exception:
        return []
    if not html:
        return []
    # Unescape JSON-escaped slashes so URLs embedded as "https:\/\/host\/f.pdf"
    # match a plain URL regex.
    return _ECATHOLIC_HTML_PDF_URL_PATTERN.findall(html.replace("\\/", "/"))


def _pick_latest_ecatholic_pdf_url(urls: list[str]) -> str:
    """Pick the newest bulletin rather than trusting the page's anchor order."""
    dated = [(parsed, url) for url in urls if (parsed := _parse_ecatholic_pdf_date(url))]
    if dated:
        return max(dated)[1]
    return urls[0]


def _parse_ecatholic_pdf_date(url: str) -> date | None:
    """eCatholic names every bulletin PDF after its Sunday: `YYYYMMDD.pdf`."""
    filename = urlparse(url).path.rsplit("/", 1)[-1]
    if not filename.lower().endswith(".pdf"):
        return None
    stem = filename[: -len(".pdf")]
    if len(stem) != 8 or not stem.isdigit():
        return None
    return safe_date(int(stem[:4]), int(stem[4:6]), int(stem[6:8]))


def _resolve_parishes_online_latest_link(
    *, provider_id: str, page: PageLike | None = None,
) -> tuple[str, str]:
    org_url = PARISHES_ONLINE_ORG_URL_TEMPLATE.format(provider_id=provider_id)
    return _resolve_latest_anchor_link_with_playwright(
        page_url=org_url,
        anchor_selector="a[href*='selectedPublication=']",
        source_label=f"parishes-online provider_id={provider_id}",
        href_to_urls=lambda href: _extract_parishes_online_pdf_url_from_href(
            href=href,
            provider_id=provider_id,
            base_url=org_url,
        ),
        page=page,
    )


def _resolve_latest_anchor_link_with_playwright(
    *,
    page_url: str,
    anchor_selector: str,
    source_label: str,
    href_to_urls: Callable[[str], tuple[str, str] | None],
    wait_for_state: str | None = None,
    page: PageLike | None = None,
) -> tuple[str, str]:
    def _run(p: PageLike) -> tuple[str, str]:
        LOGGER.info("Resolving latest anchor link (%s)", source_label)
        LOGGER.info("Visiting page URL: %s", page_url)
        goto_with_retry(page=p, page_url=page_url)
        wait_for_selector_quietly(
            page=p,
            selector=anchor_selector,
            state=wait_for_state,
            source_label=source_label,
        )
        anchors = p.query_selector_all(anchor_selector)
        for anchor in anchors:
            href = anchor.get_attribute("href")
            if not isinstance(href, str):
                continue
            urls = href_to_urls(href)
            if urls is None:
                continue
            LOGGER.info("Resolved latest anchor link (%s)", source_label)
            return urls
        raise ValueError(f"No matching anchor link found for {source_label} at {page_url}")

    if page is not None:
        return _run(page)
    with launch_stealth_browser() as p:
        return _run(p)


def _extract_ecatholic_pdf_url_from_href(*, href: str, base_url: str) -> tuple[str, str] | None:
    absolute_href = urljoin(base_url, href)
    parsed = urlparse(absolute_href)
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    if host != ECATHOLIC_FILES_HOST:
        return None
    if "bulletins" not in path:
        return None
    if not path.endswith(".pdf"):
        return None
    return absolute_href, absolute_href


def build_latest_parishes_online_bulletin_links(
    *, provider_id: str, reference_date: date | None = None, page: PageLike | None = None,
) -> BulletinLink:
    source_url, fetch_url = _resolve_parishes_online_latest_link(provider_id=provider_id, page=page)
    _ = reference_date
    return BulletinLink(source_url=source_url, fetch_url=fetch_url)


def build_latest_discover_mass_bulletin_links(
    *, provider_id: str, reference_date: date | None = None, page: PageLike | None = None,
) -> BulletinLink:
    _ = reference_date
    source_url, fetch_url = _resolve_discover_mass_latest_link(provider_id=provider_id, page=page)
    return BulletinLink(source_url=source_url, fetch_url=fetch_url)


def _resolve_discover_mass_latest_link(
    *, provider_id: str, page: PageLike | None = None,
) -> tuple[str, str]:
    bulletin_url = DISCOVER_MASS_BULLETIN_URL_TEMPLATE.format(provider_id=provider_id.strip("/"))
    return _resolve_latest_anchor_link_with_playwright(
        page_url=bulletin_url,
        anchor_selector="a#bulletin-current[href]",
        source_label=f"discover-mass provider_id={provider_id}",
        wait_for_state="attached",
        href_to_urls=lambda href: _extract_discover_mass_pdf_url_from_href(
            href=href,
            base_url=bulletin_url,
        ),
        page=page,
    )


def _extract_discover_mass_pdf_url_from_href(*, href: str, base_url: str) -> tuple[str, str] | None:
    absolute_href = urljoin(base_url, href)
    parsed = urlparse(absolute_href)
    if parsed.netloc.lower() != "bulletins.discovermass.com":
        return None
    if parsed.path.lower() != "/download.php":
        return None
    bulletin_values = parse_qs(parsed.query).get("bulletin")
    if not bulletin_values or not bulletin_values[0].strip():
        return None
    return absolute_href, absolute_href


def build_latest_other_bulletin_links(
    *, provider_id: str, reference_date: date | None = None, page: PageLike | None = None,
    recipe: str = "",
) -> BulletinLink:
    """This week's bulletin on the parish's own site.

    `provider_id` is the parish's website, and `recipe` how to read it, if one
    was recorded (see parish_sites.Recipe).
    """
    pinned = Recipe.parse(recipe, website=provider_id)

    def _run(p: PageLike) -> BulletinLink:
        resolution = resolve_parish_site(
            homepage_url=provider_id, reference_date=reference_date or date.today(), page=p,
            recipe=pinned,
        )
        LOGGER.info("Resolved %s: %s", provider_id, resolution.describe())
        return BulletinLink(
            source_url=resolution.candidate.source_url,
            fetch_url=resolution.candidate.fetch_url,
            how=resolution.describe(),
            recipe=resolution.recipe.text(website=provider_id),
        )

    if page is not None:
        return _run(page)
    with launch_stealth_browser() as p:
        return _run(p)


def _extract_parishes_online_pdf_url_from_href(
    *, href: str, provider_id: str, base_url: str
) -> tuple[str, str] | None:
    absolute_href = urljoin(base_url, href)
    parsed = urlparse(absolute_href)
    expected_path = f"/publication-page/{provider_id}"
    if parsed.netloc != "parishesonline.com" or parsed.path != expected_path:
        return None
    selected_values = parse_qs(parsed.query).get("selectedPublication")
    if not selected_values:
        return None
    selected = selected_values[0]
    for _ in range(2):
        selected = unquote(selected)
    if not selected.lower().startswith("https://container.parishesonline.com/"):
        return None
    if not selected.lower().endswith(".pdf"):
        return None
    return absolute_href, selected


# ── Bulletin link resolution ────────────────────────────────────────────────

BulletinLinkBuilder = Callable[..., BulletinLink]


@dataclass(frozen=True)
class _ProviderSpec:
    """Everything the fetch stage needs to know about one bulletin provider."""

    build: BulletinLinkBuilder
    """Resolves the parish's latest bulletin link."""

    id_column: str
    """The parishes.csv column `build` takes as its provider_id."""

    recipe_column: str | None = None
    """The column `build` takes as its recipe, for a provider that reads a
    parish's own site."""


# Adding a provider means writing its builder and adding one row here: this
# table is what the fetch stage supports, and where each provider's id comes
# from. Providers with a stable directory listing (parishesonline, discovermass)
# are keyed by an account id; the rest start from the parish's own homepage.
_PROVIDERS: dict[str, _ProviderSpec] = {
    ECATHOLIC_TYPE: _ProviderSpec(
        build=build_latest_ecatholic_bulletin_links, id_column="homepage_url",
    ),
    PARISHES_ONLINE_TYPE: _ProviderSpec(
        build=build_latest_parishes_online_bulletin_links, id_column="provider_id",
    ),
    DISCOVER_MASS_TYPE: _ProviderSpec(
        build=build_latest_discover_mass_bulletin_links, id_column="provider_id",
    ),
    OTHER_TYPE: _ProviderSpec(
        build=build_latest_other_bulletin_links, id_column="homepage_url",
        recipe_column="provider_id",
    ),
    # A parish that keeps its bulletins in a shared Drive folder links the
    # folder from its homepage, which the "other" resolver follows.
    GOOGLE_DRIVE_TYPE: _ProviderSpec(
        build=build_latest_other_bulletin_links, id_column="homepage_url",
        recipe_column="provider_id",
    ),
}

SUPPORTED_BULLETIN_PROVIDERS = frozenset(_PROVIDERS)
# Providers that read the parish's own site, whose provider_id is an optional
# recipe pinning how (see parish_sites.Recipe).
PROVIDERS_TAKING_RECIPE = frozenset(
    name for name, spec in _PROVIDERS.items() if spec.recipe_column is not None
)


class FetchSource(NamedTuple):
    """What the fetch stage reads one parish's bulletin with."""

    provider: str
    provider_id: str
    recipe: str = ""


def _build_bulletin_link(
    bulletin_provider: str, fetch_provider_id: str, *, page: PageLike | None = None,
    recipe: str = "", reference_date: date | None = None,
) -> BulletinLink:
    """The parish's latest bulletin link, judging "latest" by `reference_date` (today)."""
    spec = _PROVIDERS.get(bulletin_provider)
    if spec is None:
        raise ValueError(f"Unsupported bulletin_provider: {bulletin_provider}")
    if spec.recipe_column is None:
        return spec.build(
            provider_id=fetch_provider_id, reference_date=reference_date, page=page,
        )
    return spec.build(
        provider_id=fetch_provider_id, reference_date=reference_date, page=page, recipe=recipe,
    )


def _resolve_fetch_source(parish) -> FetchSource | None:
    """The provider, provider id and recipe to fetch this parish with, or None to skip it."""
    provider = (parish["bulletin_provider"] or "").strip()
    spec = _PROVIDERS.get(provider)
    if spec is None:
        return None
    provider_id = (parish[spec.id_column] or "").strip()
    if not provider_id:
        return None
    recipe = (parish[spec.recipe_column] or "").strip() if spec.recipe_column else ""
    return FetchSource(provider, provider_id, recipe)


# ── HTTP helpers ────────────────────────────────────────────────────────────

class _Response(NamedTuple):
    body: bytes
    etag: str | None = None
    last_modified: str | None = None


def _http_get(
    url: str,
    *,
    referer: str | None = None,
    extra_headers: dict[str, str] | None = None,
    timeout: int = HTTP_DOWNLOAD_TIMEOUT_SECONDS,
) -> _Response:
    request_url = _normalize_url_for_request(url)
    headers = {
        # WordPress.com's CDN answers 403 to a Chrome much older than the
        # current one (122 was refused in September 2026), so keep this recent.
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
    }
    if referer:
        headers["Referer"] = referer
    headers.update(extra_headers or {})
    req = Request(request_url, headers=headers)
    LOGGER.info("Fetching URL: %s", request_url)
    with urlopen(req, timeout=timeout) as resp:
        return _Response(resp.read(), resp.headers.get("ETag"), resp.headers.get("Last-Modified"))


def _normalize_url_for_request(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    path = quote(parsed.path, safe="/%:@+~!$&'()*;,=-._")
    params = quote(parsed.params, safe="%:@+~!$&'()*;,=-._")
    query = quote(parsed.query, safe="=&%:@+~!$'()*;,/-._")
    fragment = quote(parsed.fragment, safe="%:@+~!$&'()*;,=/-._")
    return urlunparse((parsed.scheme, parsed.netloc, path, params, query, fragment))


@dataclass(frozen=True)
class Download:
    """What a bulletin download brought back."""

    pdf: bytes | None
    """The PDF, or None when the server said the copy we have is current (304)."""

    etag: str | None = None
    last_modified: str | None = None
    """The server's validators for the fetch URL, for a conditional GET next time."""


def _download_bulletin(
    *, fetch_url: str, source_url: str, validators: Validators | None = None,
) -> Download:
    """Download a bulletin, asking first whether `validators` still name it."""
    conditional = validators.request_headers() if validators else {}

    def get() -> _Response:
        return _http_get(fetch_url, referer=source_url, extra_headers=conditional)

    try:
        LOGGER.info("Attempting primary fetch URL: %s", fetch_url)
        try:
            response = get()
        except HTTPError as exc:
            # Weebly and Wix file hosts answer 429 to a few quick requests.
            if exc.code != HTTPStatus.TOO_MANY_REQUESTS:
                raise
            LOGGER.warning("429 from %s; retrying in %ss", fetch_url, HTTP_429_RETRY_SECONDS)
            time.sleep(HTTP_429_RETRY_SECONDS)
            response = get()
    except (HTTPError, URLError, OSError) as exc:
        # urllib raises a 304 like any other non-2xx answer.
        if conditional and isinstance(exc, HTTPError) and exc.code == HTTPStatus.NOT_MODIFIED:
            LOGGER.info("Not modified since the copy we have: %s", fetch_url)
            return Download(pdf=None)
        LOGGER.warning("Primary fetch failed (%s), falling back to source URL: %s", exc, source_url)
        # The validators belong to the fetch URL, so none are kept from here.
        return Download(pdf=_http_get(source_url, referer=source_url).body)
    return Download(pdf=response.body, etag=response.etag, last_modified=response.last_modified)


def _download_pdf(*, fetch_url: str, source_url: str) -> bytes:
    """Download a bulletin unconditionally."""
    pdf = _download_bulletin(fetch_url=fetch_url, source_url=source_url).pdf
    assert pdf is not None, "only a conditional download can come back empty"
    return pdf


# ── Pipeline: fetch ─────────────────────────────────────────────────────────

# Parishes fetched at once, each worker with its own browser. However many
# there are, a site never has more than one of our requests in flight (see
# `_SiteLanes`); the workers only overlap different sites, and the PDF
# compaction that follows a download.
FETCH_WORKERS = 6

# Domains that serve many parishes' pages and bulletins, mapped to the
# provider they belong to. A provider's own directory and its PDF host
# (parishesonline.com, container.parishesonline.com) are one site.
_PROVIDER_DOMAINS: dict[str, str] = {
    "parishesonline.com": PARISHES_ONLINE_TYPE,
    "ecatholic.com": ECATHOLIC_TYPE,
    "discovermass.com": DISCOVER_MASS_TYPE,
}
# Providers whose parish pages all come from the provider's servers, whatever
# domain the parish uses (an eCatholic parish's /bulletins is eCatholic's).
_HOSTED_PROVIDERS = frozenset({ECATHOLIC_TYPE, PARISHES_ONLINE_TYPE, DISCOVER_MASS_TYPE})


def _site_for_url(url: str) -> str:
    """The site a request to `url` lands on: its provider, else its domain.

    The domain is the host's last two labels, so a diocese's shared parish
    host (parishes.rcda.org) and its main site (www.rcda.org) are one site.
    """
    host = (urlparse(url if "//" in url else f"//{url}").hostname or "").lower()
    domain = ".".join(host.split(".")[-2:])
    return _PROVIDER_DOMAINS.get(domain, domain)


def _site_for_source(source: FetchSource) -> str:
    """The site resolving this parish's bulletin link visits."""
    if source.provider in _HOSTED_PROVIDERS:
        return source.provider
    return _site_for_url(source.provider_id)


@dataclass(frozen=True)
class _FetchJob:
    """One parish to fetch, and what the fetch compares its download with."""

    parish: Any
    source: FetchSource
    stored: list[dict]
    """The parish's stored bulletins. Read-only until the job is recorded."""


@dataclass(frozen=True)
class _Fetched:
    """What a worker brought back for one parish, for the main thread to record."""

    job: _FetchJob
    status: str
    detail: str | None = None
    link: BulletinLink | None = None
    download: Download | None = None
    content_hash: str | None = None
    """The downloaded PDF's hash, for a new bulletin (already in the blob store)."""
    duplicate: Duplicate | None = None
    """The stored bulletin the download turned out to be."""
    seen_at: str | None = None


class _SiteLanes:
    """Hands parishes to workers so that a site has one request in flight at most.

    A worker holds a parish's site while it resolves the bulletin link, then
    moves to the site the PDF comes from for the download (`switch`), and
    lets go before compacting it. A free worker takes a parish from the site
    with the most parishes still waiting, so the longest queue (one provider
    can have half the parishes) never sits idle; each site's parishes go in
    their given order.
    """

    def __init__(self, jobs: list[tuple[str, _FetchJob]]) -> None:
        self._pending: dict[str, deque[_FetchJob]] = {}
        for site, job in jobs:
            self._pending.setdefault(site, deque()).append(job)
        self._busy: set[str] = set()
        # Sites a worker is waiting to download from: they go to that worker
        # before any new parish.
        self._wanted: Counter[str] = Counter()
        self._cond = threading.Condition()

    def take(self) -> tuple[str, _FetchJob] | None:
        """The next parish and its site, now held; None when none are left."""
        with self._cond:
            while self._pending:
                free = [
                    site for site in self._pending
                    if site not in self._busy and not self._wanted[site]
                ]
                if free:
                    site = max(free, key=lambda s: len(self._pending[s]))
                    queue = self._pending[site]
                    job = queue.popleft()
                    if not queue:
                        del self._pending[site]
                    self._busy.add(site)
                    return site, job
                self._cond.wait()
            return None

    def switch(self, held: str, site: str) -> None:
        """Let go of `held` and hold `site`, waiting until it is free."""
        if site == held:
            return
        with self._cond:
            self._busy.discard(held)
            self._cond.notify_all()
            self._wanted[site] += 1
            try:
                while site in self._busy:
                    self._cond.wait()
            finally:
                self._wanted[site] -= 1
            self._busy.add(site)

    def release(self, site: str) -> None:
        with self._cond:
            self._busy.discard(site)
            self._cond.notify_all()

    def close(self) -> None:
        """Hand out no more parishes (the ones in flight finish)."""
        with self._cond:
            self._pending.clear()
            self._cond.notify_all()


def fetch_bulletins(
    *,
    parish_name: str | None = None,
    slugs: Collection[str] | None = None,
    run_id: str | None = None,
    today: date | None = None,
    workers: int = FETCH_WORKERS,
) -> dict[str, int]:
    """Download each parish's latest bulletin if it is one we have not seen.

    A parish whose newest bulletin is, by the date the extractor read off it,
    already this weekend's (see `bulletin_week.has_bulletin_for`) is not
    fetched at all. For the rest, the download is compared with what the
    parish already has (see `duplicates`): a bulletin seen before is recorded
    as seen again, not stored twice. A new one goes to the blob store under
    its content hash, and a `bulletin` row records where it came from. With
    `run_id`, each parish's outcome is also recorded for the run report.
    `slugs` limits the run to those parishes.

    Up to `workers` parishes are fetched at once, never two from one site
    (see `_SiteLanes`). Only this thread touches the database.
    """
    LOGGER.info(
        "Starting fetch stage (parish_name=%s, slugs=%s, workers=%s)",
        parish_name or "*all*",
        "*all*" if slugs is None else len(slugs),
        workers,
    )
    store = get_store()
    sunday = nearest_sunday(today or date.today())

    tally: Counter[str] = Counter()
    attempted_slugs: list[str] = []

    conn = connect_db()
    try:
        parishes = _parishes_for_run(conn, parish_name, slugs)
        by_slug: dict[str, list[dict]] = {}
        for entry in load_bulletins(conn):
            by_slug.setdefault(entry["parish_slug"], []).append(entry)

        jobs: list[tuple[str, _FetchJob]] = []
        for parish in parishes:
            slug = parish["slug"]
            fetch_source = _resolve_fetch_source(parish)
            if fetch_source is None:
                # Unsupported provider (e.g. no_bulletin): not a
                # parish we expect to refresh, so keep it out of the stale report.
                continue
            attempted_slugs.append(slug)
            stored = by_slug.setdefault(slug, [])

            newest = newest_bulletin(stored)
            if has_bulletin_for(newest, sunday):
                tally[FETCH_CURRENT] += 1
                record_parish_result(
                    conn, run_id, slug, "fetch", FETCH_CURRENT,
                    source_url=newest["source_url"], content_hash=newest["content_hash"],
                    detail=f"already have the bulletin for {sunday.isoformat()}",
                )
                continue
            jobs.append((
                _site_for_source(fetch_source),
                _FetchJob(parish=parish, source=fetch_source, stored=stored),
            ))

        # Closed on the way out, so a failure here stops the workers too.
        with closing(_fetch_in_parallel(
            jobs, workers=workers, store=store, sunday=sunday, today=today,
        )) as results:
            for fetched in results:
                tally[_record_fetched(conn, run_id, fetched)] += 1
    finally:
        conn.close()

    stale = stale_parishes(
        (entry for entries in by_slug.values() for entry in entries),
        attempted_slugs, today=today,
    )
    for slug, newest in stale.items():
        LOGGER.warning(
            "Parish %s has no bulletin from the last %s days (newest: %s)",
            slug, STALE_BULLETIN_AGE_DAYS,
            "none" if newest is None else bulletin_reference_date(newest),
        )

    result = {
        "fetched_bulletins": tally[FETCH_NEW],
        "already_current": tally[FETCH_CURRENT],
        "unchanged_bulletins": tally[FETCH_UNCHANGED],
        "recheck_failed": tally[FETCH_RECHECK_FAILED],
        "failed_parishes": (
            tally[FETCH_RESOLVE_FAILED] + tally[FETCH_DOWNLOAD_FAILED] + tally[FETCH_SAVE_FAILED]
        ),
        "stale_parishes": len(stale),
    }
    LOGGER.info("Fetch stage finished: %s", result)
    return result


def _fetch_in_parallel(
    jobs: list[tuple[str, _FetchJob]],
    *,
    workers: int,
    store: CachedBlobStore,
    sunday: date,
    today: date | None,
) -> Iterator[_Fetched]:
    """Fetch `jobs` on worker threads, yielding each result as it lands.

    A worker that crashes (anything `_fetch_one` does not turn into a
    result) stops the others taking new parishes, and its error is raised
    here once they have finished the ones in flight.
    """
    if not jobs:
        return
    lanes = _SiteLanes(jobs)
    results: queue.SimpleQueue[_Fetched | None] = queue.SimpleQueue()

    def work() -> None:
        try:
            with launch_stealth_browser() as page:
                while (taken := lanes.take()) is not None:
                    site, job = taken
                    results.put(_fetch_one(
                        job, site=site, lanes=lanes, page=page, store=store,
                        sunday=sunday, today=today,
                    ))
        except BaseException:
            lanes.close()
            raise
        finally:
            results.put(None)

    count = max(1, min(workers, len(jobs)))
    with ThreadPoolExecutor(max_workers=count, thread_name_prefix="fetch") as pool:
        futures = [pool.submit(work) for _ in range(count)]
        try:
            finished = 0
            while finished < count:
                fetched = results.get()
                if fetched is None:
                    finished += 1
                else:
                    yield fetched
        finally:
            lanes.close()
    for future in futures:
        future.result()


def _fetch_one(
    job: _FetchJob,
    *,
    site: str,
    lanes: _SiteLanes,
    page: PageLike,
    store: CachedBlobStore,
    sunday: date,
    today: date | None,
) -> _Fetched:
    """Resolve, download and store one parish's bulletin; no database access.

    Holds `site` (taken from `lanes`) until the download is done.
    """
    slug = job.parish["slug"]
    try:
        LOGGER.info("Fetching parish %s (%s)", slug, job.source.provider)
        try:
            link = _build_bulletin_link(
                job.source.provider, job.source.provider_id, page=page,
                recipe=job.source.recipe, reference_date=today,
            )
        except ValueError as exc:
            LOGGER.warning("Skipping parish %s: %s", slug, exc)
            return _Fetched(job, FETCH_RESOLVE_FAILED, detail=str(exc))
        except Exception as exc:
            LOGGER.warning(
                "Failed resolving bulletin link for parish %s: %s", slug, exc, exc_info=True,
            )
            return _Fetched(job, FETCH_RESOLVE_FAILED, detail=f"{type(exc).__name__}: {exc}")

        pdf_site = _site_for_url(link.fetch_url)
        lanes.switch(site, pdf_site)
        site = pdf_site

        # The address is never taken to mean we have the bulletin: one
        # address can carry a new issue each week, and one issue can
        # come from a new address each time. It only lets the server
        # say the copy we have from it is current.
        known = validators_for(link.source_url, job.stored)
        try:
            download = _download_bulletin(
                fetch_url=link.fetch_url, source_url=link.source_url,
                validators=None if known is None else Validators(
                    known.bulletin.get("etag"), known.bulletin.get("last_modified"),
                ),
            )
        except (HTTPError, URLError, OSError) as exc:
            LOGGER.warning("Failed downloading bulletin for %s: %s", slug, exc)
            # A re-check of this week's bulletin, which we already have from
            # this address but could not trust the date of, is not a failure
            # to fetch. A bulletin from an earlier week at the same address is
            # no such thing: the site may have this week's issue there now.
            status = (
                FETCH_RECHECK_FAILED
                if _rechecks_this_weeks_bulletin(job.stored, link.source_url, sunday)
                else FETCH_DOWNLOAD_FAILED
            )
            return _Fetched(job, status, detail=f"{type(exc).__name__}: {exc}", link=link)
    finally:
        lanes.release(site)

    seen_at = utc_now_iso()
    if download.pdf is None:
        duplicate = known
        content_hash = None
    else:
        content_hash = bulletin_hash(download.pdf)
        duplicate = find_duplicate(content_hash, job.stored)
    if duplicate is not None:
        return _Fetched(
            job, FETCH_UNCHANGED, link=link, download=download, duplicate=duplicate,
            seen_at=seen_at,
        )
    assert download.pdf is not None and content_hash is not None

    key = bulletin_pdf_key(slug, content_hash)
    try:
        # Stored before the row that points at it, so a bulletin row never
        # names a PDF that is not there. Compaction is not byte-for-byte
        # repeatable, so a PDF already stored (by a run whose database was not
        # published) is left as it is.
        if not store.exists(key):
            store.put(key, compact_bulletin_pdf(download.pdf), content_type="application/pdf")
    except Exception as exc:
        LOGGER.warning("Failed saving bulletin for parish %s: %s", slug, exc, exc_info=True)
        return _Fetched(
            job, FETCH_SAVE_FAILED, detail=f"{type(exc).__name__}: {exc}", link=link,
        )
    return _Fetched(
        job, FETCH_NEW, link=link, download=download, content_hash=content_hash,
        seen_at=seen_at,
    )


def _record_fetched(conn, run_id: str | None, fetched: _Fetched) -> str:
    """Record one parish's fetch in the database; returns its final status."""
    job, link = fetched.job, fetched.link
    slug = job.parish["slug"]
    source_url = None if link is None else link.source_url

    def record(status: str, **fields) -> str:
        record_parish_result(conn, run_id, slug, "fetch", status, **fields)
        return status

    if fetched.status == FETCH_UNCHANGED:
        duplicate, download = fetched.duplicate, fetched.download
        assert duplicate is not None and download is not None and fetched.seen_at is not None
        _record_seen_again(
            conn, duplicate, download=download, source_url=link.source_url,
            seen_at=fetched.seen_at,
        )
        return record(
            FETCH_UNCHANGED, source_url=source_url,
            content_hash=duplicate.bulletin["content_hash"],
            detail=join_details(link.how, duplicate.describe()),
        )
    if fetched.status != FETCH_NEW:
        if source_url is None:
            return record(fetched.status, detail=fetched.detail)
        return record(fetched.status, detail=fetched.detail, source_url=source_url)

    download = fetched.download
    assert download is not None and fetched.content_hash is not None
    try:
        bulletin_id = insert_bulletin(
            conn,
            parish_id=job.parish["id"],
            source_url=link.source_url,
            content_hash=fetched.content_hash,
            fetched_at=fetched.seen_at,
            etag=download.etag,
            last_modified=download.last_modified,
        )
    except Exception as exc:
        LOGGER.warning("Failed saving bulletin for parish %s: %s", slug, exc, exc_info=True)
        return record(
            FETCH_SAVE_FAILED, detail=f"{type(exc).__name__}: {exc}", source_url=source_url,
        )

    job.stored.append({
        "id": bulletin_id, "parish_slug": slug, "source_url": link.source_url,
        "content_hash": fetched.content_hash, "published_date": None,
        "fetched_at": fetched.seen_at, "processed_at": None, "wrong_bulletin": 0,
        "etag": download.etag, "last_modified": download.last_modified,
        "last_seen_at": fetched.seen_at,
    })
    return record(
        FETCH_NEW, source_url=source_url, content_hash=fetched.content_hash,
        detail=link.how or None,
    )


def _rechecks_this_weeks_bulletin(
    stored: list[dict], source_url: str, sunday: date,
) -> bool:
    """Whether a bulletin for `sunday`'s week was already fetched from `source_url`."""
    return any(
        entry["source_url"] == source_url and not entry.get("wrong_bulletin")
        and bulletin_week(entry) == sunday
        for entry in stored
    )


def _record_seen_again(
    conn, duplicate: Duplicate, *, download: Download, source_url: str, seen_at: str,
) -> None:
    """Note on a stored bulletin that the site served it again.

    The server's validators are kept only when it served the bulletin from the
    address the bulletin was stored under: they name that address's copy.
    """
    same_address = duplicate.bulletin["source_url"] == source_url
    etag = download.etag if same_address else None
    last_modified = download.last_modified if same_address else None
    mark_bulletin_seen(
        conn, duplicate.bulletin["id"], seen_at=seen_at, etag=etag, last_modified=last_modified,
    )
    duplicate.bulletin["last_seen_at"] = seen_at
    if etag:
        duplicate.bulletin["etag"] = etag
    if last_modified:
        duplicate.bulletin["last_modified"] = last_modified


# ── Helpers ─────────────────────────────────────────────────────────────────

def _parishes_for_run(conn, parish_name: str | None, slugs: Collection[str] | None) -> list:
    if parish_name:
        row = get_parish_by_name(conn, parish_name)
        if row is None:
            raise ValueError(f"Parish not found: {parish_name}")
        return [row]
    rows = list(list_parishes(conn))
    if slugs is None:
        return rows
    wanted = set(slugs)
    missing = sorted(wanted - {row["slug"] for row in rows})
    if missing:
        raise ValueError(f"Parish not found: {', '.join(missing)}")
    return [row for row in rows if row["slug"] in wanted]
