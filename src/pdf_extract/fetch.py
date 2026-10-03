"""Bulletin fetch pipeline: resolve provider links, download PDFs, record bulletins."""

from __future__ import annotations

import logging
import re
import time
from collections.abc import Callable, Collection
from dataclasses import dataclass
from datetime import date
from http import HTTPStatus
from typing import NamedTuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.browser import (
    PageLike,
    goto_with_retry,
    launch_stealth_browser,
    wait_for_selector_quietly,
)
from pdf_extract.bulletin_week import (
    STALE_BULLETIN_AGE_DAYS,
    bulletin_reference_date,
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


class FetchSource(NamedTuple):
    """What the fetch stage reads one parish's bulletin with."""

    provider: str
    provider_id: str
    recipe: str = ""


def _build_bulletin_link(
    bulletin_provider: str, fetch_provider_id: str, *, page: PageLike | None = None,
    recipe: str = "",
) -> BulletinLink:
    spec = _PROVIDERS.get(bulletin_provider)
    if spec is None:
        raise ValueError(f"Unsupported bulletin_provider: {bulletin_provider}")
    if spec.recipe_column is None:
        return spec.build(provider_id=fetch_provider_id, page=page)
    return spec.build(provider_id=fetch_provider_id, page=page, recipe=recipe)


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

def fetch_bulletins(
    *,
    parish_name: str | None = None,
    slugs: Collection[str] | None = None,
    run_id: str | None = None,
    today: date | None = None,
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
    """
    LOGGER.info(
        "Starting fetch stage (parish_name=%s, slugs=%s)",
        parish_name or "*all*",
        "*all*" if slugs is None else len(slugs),
    )
    store = get_store()
    sunday = nearest_sunday(today or date.today())

    fetched = 0
    current = 0
    unchanged = 0
    recheck_failed = 0
    failed = 0
    attempted_slugs: list[str] = []

    conn = connect_db()
    try:
        parishes = _parishes_for_run(conn, parish_name, slugs)
        by_slug: dict[str, list[dict]] = {}
        for entry in load_bulletins(conn):
            by_slug.setdefault(entry["parish_slug"], []).append(entry)

        with launch_stealth_browser() as page:
            for parish in parishes:
                slug = parish["slug"]
                fetch_source = _resolve_fetch_source(parish)
                if fetch_source is None:
                    # Unsupported provider (e.g. no_bulletin): not a
                    # parish we expect to refresh, so keep it out of the stale report.
                    continue
                attempted_slugs.append(slug)
                stored = by_slug.setdefault(slug, [])

                def record(status: str, **fields) -> None:
                    record_parish_result(conn, run_id, slug, "fetch", status, **fields)

                newest = newest_bulletin(stored)
                if has_bulletin_for(newest, sunday):
                    current += 1
                    record(
                        FETCH_CURRENT, source_url=newest["source_url"],
                        content_hash=newest["content_hash"],
                        detail=f"already have the bulletin for {sunday.isoformat()}",
                    )
                    continue

                try:
                    link = _build_bulletin_link(
                        fetch_source.provider, fetch_source.provider_id, page=page,
                        recipe=fetch_source.recipe,
                    )
                except ValueError as exc:
                    LOGGER.warning("Skipping parish %s: %s", slug, exc)
                    record(FETCH_RESOLVE_FAILED, detail=str(exc))
                    failed += 1
                    continue
                except Exception as exc:
                    LOGGER.warning(
                        "Failed resolving bulletin link for parish %s: %s", slug, exc,
                        exc_info=True,
                    )
                    record(FETCH_RESOLVE_FAILED, detail=f"{type(exc).__name__}: {exc}")
                    failed += 1
                    continue

                # The address is never taken to mean we have the bulletin: one
                # address can carry a new issue each week, and one issue can
                # come from a new address each time. It only lets the server
                # say the copy we have from it is current.
                known = validators_for(link.source_url, stored)
                try:
                    download = _download_bulletin(
                        fetch_url=link.fetch_url, source_url=link.source_url,
                        validators=None if known is None else Validators(
                            known.bulletin.get("etag"), known.bulletin.get("last_modified"),
                        ),
                    )
                except (HTTPError, URLError, OSError) as exc:
                    LOGGER.warning("Failed downloading bulletin for %s: %s", slug, exc)
                    detail = f"{type(exc).__name__}: {exc}"
                    if any(entry["source_url"] == link.source_url for entry in stored):
                        # A re-check of a bulletin we already have: the parish
                        # still has it, so this is not a failure to fetch.
                        recheck_failed += 1
                        record(FETCH_RECHECK_FAILED, detail=detail, source_url=link.source_url)
                    else:
                        failed += 1
                        record(FETCH_DOWNLOAD_FAILED, detail=detail, source_url=link.source_url)
                    continue

                seen_at = utc_now_iso()
                if download.pdf is None:
                    duplicate = known
                    content_hash = None
                else:
                    content_hash = bulletin_hash(download.pdf)
                    duplicate = find_duplicate(content_hash, stored)
                if duplicate is not None:
                    _record_seen_again(
                        conn, duplicate, download=download, source_url=link.source_url,
                        seen_at=seen_at,
                    )
                    unchanged += 1
                    record(
                        FETCH_UNCHANGED, source_url=link.source_url,
                        content_hash=duplicate.bulletin["content_hash"],
                        detail=_join(link.how, duplicate.describe()),
                    )
                    continue
                assert download.pdf is not None and content_hash is not None

                key = bulletin_pdf_key(slug, content_hash)
                try:
                    # Stored before the row that points at it, so a bulletin row
                    # never names a PDF that is not there. Compaction is not
                    # byte-for-byte repeatable, so a PDF already stored (by a
                    # run whose database was not published) is left as it is.
                    if not store.exists(key):
                        store.put(
                            key, compact_bulletin_pdf(download.pdf),
                            content_type="application/pdf",
                        )
                    bulletin_id = insert_bulletin(
                        conn,
                        parish_id=parish["id"],
                        source_url=link.source_url,
                        content_hash=content_hash,
                        fetched_at=seen_at,
                        etag=download.etag,
                        last_modified=download.last_modified,
                    )
                except Exception as exc:
                    LOGGER.warning(
                        "Failed saving bulletin for parish %s: %s", slug, exc, exc_info=True,
                    )
                    record(
                        FETCH_SAVE_FAILED,
                        detail=f"{type(exc).__name__}: {exc}",
                        source_url=link.source_url,
                    )
                    failed += 1
                    continue

                stored.append({
                    "id": bulletin_id, "parish_slug": slug, "source_url": link.source_url,
                    "content_hash": content_hash, "published_date": None,
                    "fetched_at": seen_at, "processed_at": None, "wrong_bulletin": 0,
                    "etag": download.etag, "last_modified": download.last_modified,
                    "last_seen_at": seen_at,
                })
                fetched += 1
                record(
                    FETCH_NEW, source_url=link.source_url, content_hash=content_hash,
                    detail=link.how or None,
                )
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
        "fetched_bulletins": fetched,
        "already_current": current,
        "unchanged_bulletins": unchanged,
        "recheck_failed": recheck_failed,
        "failed_parishes": failed,
        "stale_parishes": len(stale),
    }
    LOGGER.info("Fetch stage finished: %s", result)
    return result


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


def _join(*parts: str | None) -> str | None:
    return "; ".join(part for part in parts if part) or None


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
