"""Bulletin fetch pipeline: resolve provider links, download PDFs, record bulletins."""

from __future__ import annotations

import hashlib
import logging
import re
import time
from collections.abc import Callable, Collection
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, unquote, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen

from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.browser import AnchorLike, PageLike, launch_stealth_browser
from pdf_extract.pdf_compact import compact_bulletin_pdf
from pdf_extract.runs import (
    FETCH_DOWNLOAD_FAILED,
    FETCH_NEW,
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

# Playwright waits for a matching selector to appear on a page before we scrape
# anchor hrefs from it.
PLAYWRIGHT_SELECTOR_TIMEOUT_MS = 15000
# Short delay between retries when Playwright aborts a navigation because the
# page initiated another one while we were waiting.
PLAYWRIGHT_NAV_RETRY_DELAY_MS = 250
# Per-request timeout for direct PDF downloads over HTTP.
HTTP_DOWNLOAD_TIMEOUT_SECONDS = 60
# eCatholic bulletin pages keep their PDF links in an archive panel that is
# often attached but not visible, and sometimes only populated after the first
# render. When a pass finds nothing, reload once after a short settle.
ECATHOLIC_RESOLVE_ATTEMPTS = 2
ECATHOLIC_SETTLE_DELAY_MS = 2000
# A homepage can link "bulletin" from several places (a menu entry, a news post
# about the bulletin, a Drive folder). When a page has no bulletin, the next is
# tried, up to this many.
OTHER_BULLETIN_PAGES_TO_TRY = 3
# A bulletin dated within this many days of today is taken as the current one.
OTHER_CURRENT_WINDOW_DAYS = 7
# A bulletin found on one of those later links, dated further than this from
# today, is an archive's, not the current one.
OTHER_FALLBACK_MAX_AGE_DAYS = 45
# Wait before the one retry of a download answered 429 (Too Many Requests).
HTTP_429_RETRY_SECONDS = 10
# How _pick_other_candidate's refusal of an old bulletin begins.
OLD_BULLETIN_ONLY = "Only PDF found is dated"
# A date without a year ("March 28", "12-28") is taken as the nearest such day,
# but no further ahead than the coming Sunday: "October 4" read on 27 September
# is in an archive of last year's bulletins, not next week's.
YEARLESS_MAX_DAYS_AHEAD = 6
# A parish whose newest bulletin is older than this is reported at the end of
# the fetch stage: the resolver kept returning a link we already had.
STALE_BULLETIN_AGE_DAYS = 14

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class BulletinLink:
    source_url: str
    fetch_url: str


@dataclass(frozen=True)
class _OtherPdfCandidate:
    source_url: str
    fetch_url: str
    parsed_date: date | None
    # "bulletin" appears in the link's text or address.
    labelled: bool = False
    # The link's whole text names the bulletin ("Bulletin", "Weekly Bulletin").
    titled_bulletin: bool = False


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
            _goto_with_retry(page=p, page_url=bulletins_url)
            # Wait on "attached", not the default "visible": these links live in
            # a collapsed archive panel on most eCatholic themes, so requiring
            # visibility times out on a page that already has what we need.
            _wait_for_selector_quietly(
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
    return _safe_date(int(stem[:4]), int(stem[4:6]), int(stem[6:8]))


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


def _wait_for_selector_quietly(
    *, page: PageLike, selector: str, state: str | None, source_label: str,
) -> None:
    """Wait for `selector`, treating the wait itself as best-effort.

    The wait only lets a fast page resolve in a second instead of blocking for
    the full timeout. When it expires we still scrape whatever the DOM holds,
    so a hidden or late link produces a real "nothing found" error (or a link)
    rather than a Playwright timeout that hides why the parish was skipped.
    """
    try:
        if state is None:
            page.wait_for_selector(selector, timeout=PLAYWRIGHT_SELECTOR_TIMEOUT_MS)
        else:
            page.wait_for_selector(
                selector, timeout=PLAYWRIGHT_SELECTOR_TIMEOUT_MS, state=state,
            )
    except Exception as exc:
        LOGGER.warning(
            "Selector %s did not settle for %s (%s); scraping the page anyway",
            selector, source_label, type(exc).__name__,
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
        _goto_with_retry(page=p, page_url=page_url)
        _wait_for_selector_quietly(
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
) -> BulletinLink:
    source_url, fetch_url = _resolve_other_latest_link(
        provider_id=provider_id, reference_date=reference_date, page=page,
    )
    return BulletinLink(source_url=source_url, fetch_url=fetch_url)


def _resolve_other_latest_link(
    *, provider_id: str, reference_date: date | None = None, page: PageLike | None = None,
) -> tuple[str, str]:
    def _run(p: PageLike) -> tuple[str, str]:
        today = reference_date or date.today()
        _goto_with_retry(page=p, page_url=provider_id)
        _wait_for_selector_quietly(
            page=p, selector="a[href]", state="attached", source_label=provider_id,
        )
        bulletin_page_urls = _find_other_bulletin_page_urls(
            page=p, base_url=provider_id, reference_date=today,
        )
        # Some homepages link this week's bulletin PDF itself, with no page for
        # it: read the homepage as the bulletin page, after any real one.
        if _links_bulletin_pdf(page=p, base_url=p.url or provider_id):
            bulletin_page_urls.append(provider_id)
        if not bulletin_page_urls:
            raise ValueError(f"No bulletin page link found for other provider at {provider_id}")

        # The first "bulletin" link is not always the bulletin: it can be a news
        # post about it, or an old archive. Try the next ones before giving up,
        # and report the first page's problem if none of them has one.
        # A later link is often an archive, so take a bulletin from it only if it
        # is not plainly an old one. The first link's bulletin is taken whatever
        # its age, but only once no later link has a recent one: a site's
        # "Bulletins" page can be a stale 2017 archive beside "2026 Bulletins".
        failures: list[ValueError] = []
        pages_to_try = bulletin_page_urls[:OTHER_BULLETIN_PAGES_TO_TRY]
        for bulletin_page_url in pages_to_try:
            try:
                return _resolve_other_bulletin_page(
                    page=p, bulletin_page_url=bulletin_page_url, reference_date=today,
                    max_age_days=OTHER_FALLBACK_MAX_AGE_DAYS,
                )
            except ValueError as exc:
                LOGGER.info("No recent bulletin on %s: %s", bulletin_page_url, exc)
                failures.append(exc)
        if str(failures[0]).startswith(OLD_BULLETIN_ONLY):
            return _resolve_other_bulletin_page(
                page=p, bulletin_page_url=pages_to_try[0], reference_date=today,
            )
        raise failures[0]

    if page is not None:
        return _run(page)
    with launch_stealth_browser() as p:
        return _run(p)


def _resolve_other_bulletin_page(
    *, page: PageLike, bulletin_page_url: str, reference_date: date,
    max_age_days: int | None = None,
) -> tuple[str, str]:
    _goto_with_retry(page=page, page_url=bulletin_page_url)
    if _google_drive_folder_id(bulletin_page_url):
        candidates = _collect_google_drive_pdf_candidates(
            page=page, folder_url=bulletin_page_url, reference_date=reference_date,
        )
        if not candidates:
            raise ValueError(f"No PDF files found in Google Drive folder: {bulletin_page_url}")
        return _pick_other_candidate(
            candidates, reference_date=reference_date, max_age_days=max_age_days,
        )

    _wait_for_selector_quietly(
        page=page, selector="a[href]", state="attached", source_label=bulletin_page_url,
    )
    current_page_url = page.url or bulletin_page_url
    # A "Bulletin" link can redirect straight to this week's PDF, sometimes by
    # script once the page has loaded.
    if urlparse(current_page_url).path.lower().endswith(".pdf"):
        return current_page_url, current_page_url

    candidates = _collect_other_pdf_candidates(
        page=page, base_url=current_page_url, reference_date=reference_date,
    )
    if not candidates:
        # A page that links no PDF can still hand readers the issue elsewhere: a
        # flipbook it embeds (this week's, while it lists only older ones), or
        # a publisher's listing of dated PDFs.
        issue_page_url = _find_embedded_flipbook_url(
            page=page, base_url=current_page_url,
        ) or _find_publisher_listing_url(page=page, base_url=current_page_url)
        if issue_page_url is not None:
            candidates = _collect_other_post_candidates(
                page=page, post_url=issue_page_url, reference_date=reference_date,
            )
            if not candidates:
                _goto_with_retry(page=page, page_url=bulletin_page_url)

    # Some sites (e.g. WordPress parish blogs) list each weekly bulletin as a
    # dated post that wraps the actual PDF, rather than linking to the PDF
    # directly. If we found no PDFs on the listing page, descend once into
    # the latest dated "bulletin" post and collect PDFs from there. The same
    # goes when its only PDFs are something else (a tour guide in the menu)
    # and a post for this week's bulletin is listed.
    if candidates and not any(
        c.labelled or _is_current(c.parsed_date, reference_date) for c in candidates
    ):
        post = _find_latest_other_bulletin_post(
            page=page, base_url=current_page_url, reference_date=reference_date,
        )
        if post is not None and _is_current(post[0], reference_date):
            post_candidates = _collect_other_post_candidates(
                page=page, post_url=post[1], reference_date=reference_date,
            )
            if post_candidates:
                candidates = post_candidates

    if not candidates:
        post = _find_latest_other_bulletin_post(
            page=page, base_url=current_page_url, reference_date=reference_date,
        )
        if post is None:
            raise ValueError(f"No PDF links found on bulletin page: {bulletin_page_url}")
        post_url = post[1]
        candidates = _collect_other_post_candidates(
            page=page, post_url=post_url, reference_date=reference_date,
        )
        if not candidates:
            raise ValueError(f"No PDF links found on bulletin post page: {post_url}")

    return _pick_other_candidate(
        candidates, reference_date=reference_date, max_age_days=max_age_days,
    )


def _collect_other_post_candidates(
    *, page: PageLike, post_url: str, reference_date: date,
) -> list[_OtherPdfCandidate]:
    _goto_with_retry(page=page, page_url=post_url)
    _wait_for_selector_quietly(
        page=page, selector="a[href]", state="attached", source_label=post_url,
    )
    return _collect_other_pdf_candidates(
        page=page, base_url=page.url or post_url, reference_date=reference_date,
    )


def _is_current(parsed_date: date | None, reference_date: date) -> bool:
    return (
        parsed_date is not None
        and abs((parsed_date - reference_date).days) <= OTHER_CURRENT_WINDOW_DAYS
    )


def _age_days(candidate: _OtherPdfCandidate, reference_date: date) -> int:
    return (reference_date - (candidate.parsed_date or reference_date)).days


def _pick_other_candidate(
    candidates: list[_OtherPdfCandidate], *, reference_date: date,
    max_age_days: int | None = None,
) -> tuple[str, str]:
    """The newest bulletin dated within a week of today, else a fallback.

    With none that current, the first one listed, except:
    - if it is plainly old (dated over OTHER_FALLBACK_MAX_AGE_DAYS ago), the
      newest dated within that, when one is listed: a listing oldest first
      (St. Joseph, Troy) or a parish a few weeks behind;
    - a link whose whole text is "Bulletin" beats a first one that is not
      dated (St. Mary's, Glens Falls lists a Confirmation PDF first).
    With `max_age_days`, a pick dated further than that from today is refused.
    """
    dated_candidates = [c for c in candidates if _is_current(c.parsed_date, reference_date)]
    if dated_candidates:
        best = max(dated_candidates, key=lambda c: c.parsed_date or date.min)
        return best.source_url, best.fetch_url

    first = candidates[0]
    if first.parsed_date is not None and _age_days(first, reference_date) > (
        OTHER_FALLBACK_MAX_AGE_DAYS
    ):
        recent = [
            c for c in candidates
            if c.parsed_date is not None
            and -OTHER_CURRENT_WINDOW_DAYS
            <= _age_days(c, reference_date)
            <= OTHER_FALLBACK_MAX_AGE_DAYS
        ]
        if recent:
            best = max(recent, key=lambda c: c.parsed_date or date.min)
            return best.source_url, best.fetch_url
    if first.parsed_date is None:
        first = next((c for c in candidates if c.titled_bulletin), first)
    if (
        max_age_days is not None
        and first.parsed_date is not None
        and abs((reference_date - first.parsed_date).days) > max_age_days
    ):
        raise ValueError(
            f"{OLD_BULLETIN_ONLY} {first.parsed_date.isoformat()}: {first.source_url}"
        )
    return first.source_url, first.fetch_url


def _find_other_bulletin_page_urls(
    *, page: PageLike, base_url: str, reference_date: date | None = None,
) -> list[str]:
    """Links that look like the bulletin page, best first.

    A link with "bulletin" in both its address and its text comes before one
    with it in only one of them, and within each, an archive ("Bulletin
    Archive", "2024 Bulletins") comes after the rest; otherwise the page's own
    order is kept.
    """
    this_year = (reference_date or date.today()).year
    anchors = page.query_selector_all("a[href]")
    both_matches: list[str] = []
    either_matches: list[str] = []
    archives: set[str] = set()
    for anchor in anchors:
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        text = _anchor_text(anchor)
        href_lower = href.lower()
        text_lower = text.lower()
        has_in_href = "bulletin" in href_lower
        has_in_text = "bulletin" in text_lower
        if not has_in_href and not has_in_text:
            continue
        resolved = urljoin(base_url, href)
        if (
            resolved.lower().endswith(".pdf") and not _is_publisher_listing(resolved)
        ) or _document_download_url(resolved) is not None:
            continue
        if has_in_href and has_in_text:
            both_matches.append(resolved)
        else:
            either_matches.append(resolved)
        if _looks_like_archive(f"{text_lower} {href_lower}", this_year=this_year):
            archives.add(resolved)

    def _ranked(urls: list[str]) -> list[str]:
        return sorted(urls, key=lambda url: url in archives)

    return list(dict.fromkeys(_ranked(both_matches) + _ranked(either_matches)))


def _links_bulletin_pdf(*, page: PageLike, base_url: str) -> bool:
    """Whether the page links a PDF labelled as the bulletin."""
    for anchor in page.query_selector_all("a[href]"):
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        resolved = urljoin(base_url, href)
        is_pdf = resolved.lower().endswith(".pdf") and not _is_publisher_listing(resolved)
        if (
            (is_pdf or _document_download_url(resolved) is not None)
            and "bulletin" in f"{_anchor_text(anchor)} {resolved}".lower()
        ):
            return True
    return False


# John Patrick Publishing's "current bulletin" link names a PDF, but redirects
# to the parish's listing on church-bulletin.org, whose issues are dated PDFs
# (/bulletin/<parish>/2026-09-27.pdf).
_PUBLISHER_LISTING_URL = re.compile(
    r"^https?://(?:www\.)?jppc\.net/onlinebulletins/\d+template\.pdf$", flags=re.IGNORECASE,
)


def _is_publisher_listing(url: str) -> bool:
    return bool(_PUBLISHER_LISTING_URL.match(url))


def _find_publisher_listing_url(*, page: PageLike, base_url: str) -> str | None:
    for anchor in page.query_selector_all("a[href]"):
        href = anchor.get_attribute("href")
        if isinstance(href, str) and _is_publisher_listing(urljoin(base_url, href)):
            return urljoin(base_url, href)
    return None


def _looks_like_archive(text: str, *, this_year: int) -> bool:
    if "archive" in text:
        return True
    return any(int(year) < this_year for year in re.findall(r"(?<!\d)(20\d{2})(?!\d)", text))


# ── Google Drive folders ────────────────────────────────────────────────────

GOOGLE_DRIVE_HOST = "drive.google.com"
GOOGLE_DRIVE_FILE_VIEW_URL_TEMPLATE = "https://drive.google.com/file/d/{file_id}/view"
GOOGLE_DRIVE_FILE_DOWNLOAD_URL_TEMPLATE = (
    "https://drive.google.com/uc?export=download&id={file_id}"
)
# Each file in a shared folder's listing is a row carrying the file's id.
GOOGLE_DRIVE_ITEM_SELECTOR = "[data-id]"
_GOOGLE_DRIVE_FOLDER_PATH = re.compile(r"/folders/(?P<id>[\w-]+)")
_GOOGLE_DRIVE_PDF_NAME = re.compile(r"[^\n]*?\.pdf", flags=re.IGNORECASE)


def _google_drive_folder_id(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc.lower() != GOOGLE_DRIVE_HOST:
        return None
    match = _GOOGLE_DRIVE_FOLDER_PATH.search(parsed.path)
    return match.group("id") if match else None


def _collect_google_drive_pdf_candidates(
    *, page: PageLike, folder_url: str, reference_date: date,
) -> list[_OtherPdfCandidate]:
    """The PDFs a public Drive folder lists, dated by their file names.

    Parishes that keep their bulletins in a shared folder name each file after
    its Sunday ("2026-09-27 Bulletin.pdf"). The folder page is built by script,
    so the files are read from its rendered rows, and each is fetched through
    Drive's direct-download link.
    """
    folder_id = _google_drive_folder_id(folder_url)
    _wait_for_selector_quietly(
        page=page, selector=GOOGLE_DRIVE_ITEM_SELECTOR, state="attached", source_label=folder_url,
    )
    candidates: list[_OtherPdfCandidate] = []
    seen: set[str] = {folder_id} if folder_id else set()
    for item in page.query_selector_all(GOOGLE_DRIVE_ITEM_SELECTOR):
        file_id = item.get_attribute("data-id")
        if not file_id or file_id in seen:
            continue
        name = _GOOGLE_DRIVE_PDF_NAME.search(_anchor_text(item))
        if name is None:
            continue
        seen.add(file_id)
        candidates.append(
            _OtherPdfCandidate(
                source_url=GOOGLE_DRIVE_FILE_VIEW_URL_TEMPLATE.format(file_id=file_id),
                fetch_url=GOOGLE_DRIVE_FILE_DOWNLOAD_URL_TEMPLATE.format(file_id=file_id),
                parsed_date=_parse_relaxed_date(name.group(0).strip(), reference_date),
            )
        )
    return candidates


# Flipbook services a bulletin page can link each week's issue on. Their pages
# name the issue's PDF in a script, which the rendered-HTML scan finds.
FLIPBOOK_HOSTS = frozenset({"designrr.page"})


def _find_embedded_flipbook_url(*, page: PageLike, base_url: str) -> str | None:
    for frame in page.query_selector_all("iframe[src]"):
        src = frame.get_attribute("src")
        if isinstance(src, str) and urlparse(urljoin(base_url, src)).netloc.lower() in FLIPBOOK_HOSTS:
            return urljoin(base_url, src)
    return None


def _find_latest_other_bulletin_post(
    *, page: PageLike, base_url: str, reference_date: date,
) -> tuple[date, str] | None:
    """Find the latest dated non-PDF anchor that looks like a weekly bulletin post.

    Used when a bulletin listing page links to per-week post pages (which wrap
    the actual PDF) instead of linking to PDFs directly.
    """
    anchors = page.query_selector_all("a[href]")
    dated: list[tuple[date, str]] = []
    # A page that is itself the bulletin listing may title its posts by the
    # Sunday alone ("September 27 - Twenty-Sixth Sunday"). Its dated links on
    # the same site (or a flipbook service) count too, if nothing says "bulletin"
    # and they are current.
    unlabelled: list[tuple[date, str]] = []
    listing_is_bulletins = "bulletin" in base_url.lower()
    base_host = urlparse(base_url).netloc.lower()
    post_hosts = {base_host, *FLIPBOOK_HOSTS}
    base_normalized = base_url.rstrip("/").lower()
    for anchor in anchors:
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        resolved = urljoin(base_url, href)
        resolved_lower = resolved.lower()
        if resolved_lower.endswith(".pdf"):
            continue
        if resolved_lower.rstrip("/") == base_normalized:
            continue
        text = _anchor_text(anchor)
        labelled = "bulletin" in href.lower() or "bulletin" in text.lower()
        if not labelled and not (
            listing_is_bulletins and urlparse(resolved).netloc.lower() in post_hosts
        ):
            continue
        parsed_date = _parse_relaxed_date_from_texts([text, href, resolved], reference_date)
        if parsed_date is None:
            continue
        if labelled:
            dated.append((parsed_date, resolved))
        elif abs((parsed_date - reference_date).days) <= OTHER_CURRENT_WINDOW_DAYS:
            unlabelled.append((parsed_date, resolved))

    posts = dated or unlabelled
    if not posts:
        return None
    # A listing keeps its newest post at one end. Of this week's posts, take the
    # one nearest that end: an archive of past years has its own "September 27
    # & 28", read without a year as this week's too.
    current = [post for post in posts if _is_current(post[0], reference_date)]
    if current:
        steps = list(zip(posts, posts[1:]))
        newer_later = sum(later[0] > earlier[0] for earlier, later in steps)
        older_later = sum(later[0] < earlier[0] for earlier, later in steps)
        return current[-1] if newer_later > older_later else current[0]
    return max(posts, key=lambda pair: pair[0])


def _collect_other_pdf_candidates(
    *, page: PageLike, base_url: str, reference_date: date,
) -> list[_OtherPdfCandidate]:
    anchors = page.query_selector_all("a[href]")
    candidates: list[_OtherPdfCandidate] = []
    for anchor in anchors:
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        absolute_href = _unwrap_pdf_viewer_url(urljoin(base_url, href))
        fetch_url: str | None = absolute_href
        if ".pdf" not in absolute_href.lower() or _is_publisher_listing(absolute_href):
            fetch_url = _document_download_url(absolute_href)
            if fetch_url is None:
                continue
        text = _anchor_text(anchor)
        parsed_date = _parse_relaxed_date_from_texts([text, href, absolute_href], reference_date)
        candidates.append(
            _OtherPdfCandidate(
                source_url=absolute_href,
                fetch_url=fetch_url,
                parsed_date=parsed_date,
                labelled="bulletin" in f"{text} {absolute_href}".lower(),
                titled_bulletin=bool(_BULLETIN_TITLE_RE.fullmatch(text.strip().lower())),
            )
        )
    if any(c.labelled or _is_current(c.parsed_date, reference_date) for c in candidates):
        return candidates

    # Fallback: some WordPress parish sites embed PDFs through script-based
    # viewers (e.g. the DFlip / 3D FlipBook plugin on elmiracatholic.org) which
    # inject the PDF URL as JSON inside a <script> tag rather than a plain
    # <a href="..pdf">, or link a whole block to it by script (Divi). Scan the
    # rendered HTML when the page's links are no bulletin, after those links.
    try:
        html = page.content()
    except Exception:
        html = ""
    linked = {c.source_url for c in candidates}
    candidates += [
        c for c in _collect_pdf_urls_from_html(
            html, base_url=base_url, reference_date=reference_date,
        )
        if c.source_url not in linked
    ]
    if candidates or PDF_EMBEDDER_VIEWER_CLASS not in html:
        return candidates

    # The PDF Embedder plugin replaces its <a href="...pdf"> with a viewer once
    # its script runs, leaving the PDF's address only in the page as served.
    try:
        source = page.request.get(page.url or base_url).text()
    except Exception as exc:
        LOGGER.info("Could not read the served page %s: %s", page.url or base_url, exc)
        return []
    return _collect_pdf_urls_from_html(
        source, base_url=base_url, reference_date=reference_date,
    )


_BULLETIN_TITLE_RE = re.compile(
    r"(?:(?:this week'?s|weekly|current|latest|parish|sunday)\s+)?bulletin"
)
# A Google Drive file shared on its own ("/file/d/<id>/view"), as some parishes
# link each week's bulletin, downloads without a browser from this address.
_GOOGLE_DRIVE_FILE_RE = re.compile(r"^https?://drive\.google\.com/file/d/([\w-]+)")
# Concrete CMS (the Diocese of Albany's rcda.org) links files as
# /download_file/view/<file>/<page>, which redirects to the PDF.
_CONCRETE_DOWNLOAD_RE = re.compile(r"^https?://[^/]+/download_file/(?:view/)?\d+(?:/\d+)?/?$")


def _document_download_url(url: str) -> str | None:
    """Where to download a link that is a PDF though its address doesn't say so."""
    match = _GOOGLE_DRIVE_FILE_RE.match(url)
    if match:
        return GOOGLE_DRIVE_FILE_DOWNLOAD_URL_TEMPLATE.format(file_id=match.group(1))
    if _CONCRETE_DOWNLOAD_RE.match(url):
        return url
    return None


# The viewer the PDF Embedder WordPress plugin renders in place of its PDF link.
PDF_EMBEDDER_VIEWER_CLASS = "pdfemb-viewer"

# Up to the ".pdf" that ends the path: WordPress uploads can be named
# "9-20-26.pdf.pdf.pdf", and stopping at the first ".pdf" names a file that 404s.
_HTML_PDF_URL_PATTERN = re.compile(
    r'https?://[^\s"\'<>]+?\.pdf(?![\w.\-/%])', flags=re.IGNORECASE,
)

# Query parameters that online PDF viewers take the document's own URL in:
# Google Docs' `gview?url=` and pdf.js' `viewer.html?file=`.
_PDF_VIEWER_URL_PARAMS = ("url", "file", "src")


def _unwrap_pdf_viewer_url(url: str) -> str:
    """The PDF itself when `url` opens it in an online viewer, else `url`.

    Downloading the viewer gets its HTML page, not the bulletin.
    """
    parsed = urlparse(url)
    if parsed.path.lower().endswith(".pdf"):
        return url
    params = parse_qs(parsed.query)
    for name in _PDF_VIEWER_URL_PARAMS:
        for value in params.get(name, []):
            inner = urlparse(value)
            if inner.scheme in ("http", "https") and inner.path.lower().endswith(".pdf"):
                return value
    return url


def _collect_pdf_urls_from_html(
    html: str, *, base_url: str, reference_date: date,
) -> list[_OtherPdfCandidate]:
    if not html:
        return []

    # Unescape JSON-escaped slashes so URLs like "https:\/\/site\/file.pdf"
    # (as embedded by flipbook/PDF-viewer plugins) match a plain URL regex.
    normalized = html.replace("\\/", "/")

    candidates: list[_OtherPdfCandidate] = []
    seen: set[str] = set()
    for raw in _HTML_PDF_URL_PATTERN.findall(normalized):
        absolute_url = _unwrap_pdf_viewer_url(urljoin(base_url, raw))
        if absolute_url in seen or _is_publisher_listing(absolute_url):
            continue
        seen.add(absolute_url)
        parsed_date = _parse_relaxed_date_from_texts([absolute_url], reference_date)
        candidates.append(
            _OtherPdfCandidate(
                source_url=absolute_url,
                fetch_url=absolute_url,
                parsed_date=parsed_date,
                labelled="bulletin" in absolute_url.lower(),
            )
        )
    return candidates


def _anchor_text(anchor: AnchorLike) -> str:
    try:
        return anchor.inner_text().strip()
    except Exception:
        pass
    try:
        return (anchor.text_content() or "").strip()
    except Exception:
        return ""


# A folder named by the year alone ("/bulletins/2025/September_28.pdf"), not a
# WordPress upload folder ("/2025/12/..."), whose year is the upload's.
_PATH_YEAR_RE = re.compile(r"/(20\d{2})/(?!\d{1,2}/)")


def _parse_relaxed_date_from_texts(texts: list[str], reference_date: date) -> date | None:
    """The first date in texts; a yearless one takes its year from a year folder in them."""
    year = next(
        (int(m.group(1)) for text in texts if (m := _PATH_YEAR_RE.search(text or ""))), None,
    )
    for text in texts:
        parsed = _parse_relaxed_date(text, reference_date, year=year)
        if parsed is not None:
            return parsed
    return None


def _parse_relaxed_date(
    text: str, reference_date: date, *, year: int | None = None,
) -> date | None:
    """A date in text. One without a year is `year`'s if given, else the nearest."""
    if not text:
        return None

    def yearless(month: int, day: int) -> date | None:
        if year is not None:
            return _safe_date(year, month, day)
        return _resolve_yearless_date(month=month, day=day, reference_date=reference_date)

    normalized = text.lower()
    normalized = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", normalized)
    normalized = normalized.replace(",", " ")
    normalized = re.sub(r"\s+", " ", normalized).strip()

    month_name = (
        r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|"
        r"jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t)?(?:ember)?|"
        r"oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
    )
    # A day is never part of a longer number ("October 2026" is not October 20).
    # A weekend can be named by both its days before the year ("September 26 &
    # 27, 2026", "Oct-4-5-2025"); the year is still the issue's.
    month_day_pattern = re.compile(
        rf"(?P<month>{month_name})\s+(?P<day>\d{{1,2}})(?!\d)"
        r"(?:\s*(?:&|and|-|\s)\s*\d{1,2}(?=\s+\d{4}(?!\d)))?"
        r"(?:\s+(?P<year>\d{2,4}))?",
        flags=re.IGNORECASE,
    )
    day_month_pattern = re.compile(
        rf"(?<!\d)(?P<day>\d{{1,2}})\s+(?P<month>{month_name})(?:\s+(?P<year>\d{{2,4}}))?",
        flags=re.IGNORECASE,
    )

    for pattern in (month_day_pattern, day_month_pattern):
        for match in pattern.finditer(normalized):
            month_num = _month_name_to_number(match.group("month"))
            if month_num is None:
                continue
            day = int(match.group("day"))
            raw_year = match.group("year")
            if raw_year:
                parsed = _safe_date(_normalize_year(raw_year, reference_date), month_num, day)
            else:
                parsed = yearless(month_num, day)
            if parsed is not None:
                return parsed

    # Not the tail of a longer number: Weebly's "/38133239/02-12-2017" is no year 3239.
    for match in re.finditer(
        r"(?<!\d)(?P<year>\d{4})[-/.](?P<month>\d{1,2})[-/.](?P<day>\d{1,2})(?!\d)", normalized,
    ):
        parsed = _safe_date(int(match.group("year")), int(match.group("month")), int(match.group("day")))
        if parsed is not None:
            return parsed

    for match in re.finditer(
        r"(?<!\d)(?P<a>\d{1,2})[-/.](?P<b>\d{1,2})[-/.](?P<c>\d{2,4})(?!\d)", normalized,
    ):
        month = int(match.group("a"))
        day = int(match.group("b"))
        year = _normalize_year(match.group("c"), reference_date)
        parsed = _safe_date(year, month, day)
        if parsed is not None:
            return parsed

    for match in re.finditer(r"(?<!\d)(?P<a>\d{1,2})[-/.](?P<b>\d{1,2})(?!\d)", normalized):
        parsed = yearless(int(match.group("a")), int(match.group("b")))
        if parsed is not None:
            return parsed

    # File names often carry the Sunday as one run of digits: "20260927.pdf",
    # "20260927B.pdf". Only this century's years, so ids and timestamps don't
    # read as dates.
    for match in re.finditer(r"(?<!\d)(20\d{2})(\d{2})(\d{2})(?!\d)", normalized):
        parsed = _safe_date(*(int(part) for part in match.groups()))
        if parsed is not None:
            return parsed

    # Slugs and file names join words with hyphens or underscores
    # ("september-27-twenty-sixth-sunday", "Bulletin_Sept_27_2026.pdf"), and
    # abbreviations end in a period ("Sept. 27"), where the month-name
    # patterns above need a space.
    words_split = re.sub(r"[-_]+|(?<=[a-z])\.", " ", normalized)
    if words_split != normalized:
        return _parse_relaxed_date(words_split, reference_date, year=year)
    return None


def _month_name_to_number(month_name: str) -> int | None:
    month_lookup = {
        "jan": 1, "january": 1,
        "feb": 2, "february": 2,
        "mar": 3, "march": 3,
        "apr": 4, "april": 4,
        "may": 5,
        "jun": 6, "june": 6,
        "jul": 7, "july": 7,
        "aug": 8, "august": 8,
        "sep": 9, "sept": 9, "september": 9,
        "oct": 10, "october": 10,
        "nov": 11, "november": 11,
        "dec": 12, "december": 12,
    }
    return month_lookup.get(month_name.lower())


def _normalize_year(raw_year: str | None, reference_date: date) -> int:
    if not raw_year:
        return reference_date.year
    year = int(raw_year)
    if len(raw_year) == 2:
        year = 2000 + year
    return year


def _resolve_yearless_date(*, month: int, day: int, reference_date: date) -> date | None:
    candidates = [
        _safe_date(reference_date.year - 1, month, day),
        _safe_date(reference_date.year, month, day),
        _safe_date(reference_date.year + 1, month, day),
    ]
    valid = [d for d in candidates if d is not None]
    if not valid:
        return None
    not_too_far_ahead = [
        d for d in valid if (d - reference_date).days <= YEARLESS_MAX_DAYS_AHEAD
    ]
    return min(not_too_far_ahead or valid, key=lambda d: abs((d - reference_date).days))


def _safe_date(year: int, month: int, day: int) -> date | None:
    try:
        return datetime(year, month, day).date()
    except ValueError:
        return None


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
    ),
    # A parish that keeps its bulletins in a shared Drive folder links the
    # folder from its homepage, which the "other" resolver follows.
    GOOGLE_DRIVE_TYPE: _ProviderSpec(
        build=build_latest_other_bulletin_links, id_column="homepage_url",
    ),
}

SUPPORTED_BULLETIN_PROVIDERS = frozenset(_PROVIDERS)


def _build_bulletin_link(
    bulletin_provider: str, fetch_provider_id: str, *, page: PageLike | None = None,
) -> BulletinLink:
    spec = _PROVIDERS.get(bulletin_provider)
    if spec is None:
        raise ValueError(f"Unsupported bulletin_provider: {bulletin_provider}")
    return spec.build(provider_id=fetch_provider_id, page=page)


def _resolve_fetch_source(parish) -> tuple[str, str] | None:
    """The provider and provider id to fetch this parish with, or None to skip it."""
    provider = (parish["bulletin_provider"] or "").strip()
    spec = _PROVIDERS.get(provider)
    if spec is None:
        return None
    provider_id = (parish[spec.id_column] or "").strip()
    return (provider, provider_id) if provider_id else None


# ── HTTP helpers ────────────────────────────────────────────────────────────

def _http_get_bytes(
    url: str, *, referer: str | None = None, timeout: int = HTTP_DOWNLOAD_TIMEOUT_SECONDS,
) -> bytes:
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
    req = Request(request_url, headers=headers)
    LOGGER.info("Fetching URL: %s", request_url)
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _normalize_url_for_request(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    path = quote(parsed.path, safe="/%:@+~!$&'()*;,=-._")
    params = quote(parsed.params, safe="%:@+~!$&'()*;,=-._")
    query = quote(parsed.query, safe="=&%:@+~!$'()*;,/-._")
    fragment = quote(parsed.fragment, safe="%:@+~!$&'()*;,=/-._")
    return urlunparse((parsed.scheme, parsed.netloc, path, params, query, fragment))


def _goto_with_retry(*, page: PageLike, page_url: str, max_attempts: int = 3) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            page.goto(page_url, wait_until="domcontentloaded")
            return
        except Exception as exc:
            error_text = str(exc).lower()
            interrupted = "interrupted by another navigation" in error_text
            is_last_attempt = attempt == max_attempts
            if not interrupted or is_last_attempt:
                raise
            LOGGER.warning(
                "Navigation interrupted for %s (attempt %d/%d), retrying",
                page_url, attempt, max_attempts,
            )
            page.wait_for_timeout(PLAYWRIGHT_NAV_RETRY_DELAY_MS)


def _download_pdf(*, fetch_url: str, source_url: str) -> bytes:
    referer = source_url
    try:
        LOGGER.info("Attempting primary fetch URL: %s", fetch_url)
        try:
            return _http_get_bytes(
                fetch_url, referer=referer, timeout=HTTP_DOWNLOAD_TIMEOUT_SECONDS,
            )
        except HTTPError as exc:
            # Weebly and Wix file hosts answer 429 to a few quick requests.
            if exc.code != 429:
                raise
            LOGGER.warning("429 from %s; retrying in %ss", fetch_url, HTTP_429_RETRY_SECONDS)
            time.sleep(HTTP_429_RETRY_SECONDS)
            return _http_get_bytes(
                fetch_url, referer=referer, timeout=HTTP_DOWNLOAD_TIMEOUT_SECONDS,
            )
    except (HTTPError, URLError, OSError) as exc:
        LOGGER.warning("Primary fetch failed (%s), falling back to source URL: %s", exc, source_url)
        return _http_get_bytes(
            source_url, referer=referer, timeout=HTTP_DOWNLOAD_TIMEOUT_SECONDS,
        )


# ── Pipeline: fetch ─────────────────────────────────────────────────────────

def fetch_bulletins(
    *,
    parish_name: str | None = None,
    slugs: Collection[str] | None = None,
    run_id: str | None = None,
) -> dict[str, int]:
    """Download each parish's latest bulletin if it is one we have not seen.

    The PDF goes to the blob store under its content hash and a `bulletin` row
    records where it came from. With `run_id`, each parish's outcome is also
    recorded for the run report. `slugs` limits the run to those parishes.
    """
    LOGGER.info(
        "Starting fetch stage (parish_name=%s, slugs=%s)",
        parish_name or "*all*",
        "*all*" if slugs is None else len(slugs),
    )
    store = get_store()

    fetched = 0
    skipped_existing = 0
    failed = 0
    attempted_slugs: list[str] = []

    conn = connect_db()
    try:
        parishes = _parishes_for_run(conn, parish_name, slugs)
        existing = {
            (row["parish_id"], row["source_url"], row["content_hash"])
            for row in conn.execute("SELECT parish_id, source_url, content_hash FROM bulletin")
        }
        existing_urls = {(parish_id, url) for parish_id, url, _ in existing}

        with launch_stealth_browser() as page:
            for parish in parishes:
                slug = parish["slug"]
                fetch_source = _resolve_fetch_source(parish)
                if fetch_source is None:
                    # Unsupported provider (e.g. no_bulletin): not a
                    # parish we expect to refresh, so keep it out of the stale report.
                    continue
                bulletin_provider, fetch_provider_id = fetch_source
                attempted_slugs.append(slug)

                def record(status: str, **fields) -> None:
                    record_parish_result(conn, run_id, slug, "fetch", status, **fields)

                try:
                    link = _build_bulletin_link(bulletin_provider, fetch_provider_id, page=page)
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

                known_url = (parish["id"], link.source_url) in existing_urls
                if known_url and not _may_be_reissued(link.source_url):
                    skipped_existing += 1
                    record(FETCH_UNCHANGED, source_url=link.source_url)
                    continue

                try:
                    pdf_bytes = _download_pdf(
                        fetch_url=link.fetch_url, source_url=link.source_url,
                    )
                except (HTTPError, URLError, OSError) as exc:
                    LOGGER.warning("Failed downloading bulletin for %s: %s", slug, exc)
                    record(
                        FETCH_DOWNLOAD_FAILED,
                        detail=f"{type(exc).__name__}: {exc}",
                        source_url=link.source_url,
                    )
                    failed += 1
                    continue

                # The hash names the bulletin as published, so it stays the
                # bulletin's identity however the stored copy is compacted.
                content_hash = hashlib.sha256(pdf_bytes).hexdigest()
                if (parish["id"], link.source_url, content_hash) in existing:
                    skipped_existing += 1
                    record(FETCH_UNCHANGED, source_url=link.source_url)
                    continue
                key = bulletin_pdf_key(slug, content_hash)
                try:
                    # Stored before the row that points at it, so a bulletin row
                    # never names a PDF that is not there. Compaction is not
                    # byte-for-byte repeatable, so a bulletin already stored
                    # (the same PDF at a new URL) is left as it is.
                    if not store.exists(key):
                        store.put(
                            key, compact_bulletin_pdf(pdf_bytes), content_type="application/pdf",
                        )
                    insert_bulletin(
                        conn,
                        parish_id=parish["id"],
                        source_url=link.source_url,
                        content_hash=content_hash,
                        fetched_at=utc_now_iso(),
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

                existing.add((parish["id"], link.source_url, content_hash))
                existing_urls.add((parish["id"], link.source_url))
                fetched += 1
                record(FETCH_NEW, source_url=link.source_url, content_hash=content_hash)

        stale_slugs = _report_stale_parishes(
            bulletins=load_bulletins(conn), slugs=attempted_slugs,
        )
    finally:
        conn.close()

    result = {
        "fetched_bulletins": fetched,
        "skipped_existing_urls": skipped_existing,
        "failed_parishes": failed,
        "stale_parishes": len(stale_slugs),
    }
    LOGGER.info("Fetch stage finished: %s", result)
    return result


def _may_be_reissued(url: str) -> bool:
    """Whether a bulletin address we already have may hold a newer issue now.

    An address naming its issue's date ("20260927.pdf") is that issue for good.
    One that names none ("/bulletin.pdf") can be overwritten each week, so it
    is downloaded again and compared by content.
    """
    return _parse_relaxed_date(url, date.today()) is None


def _report_stale_parishes(*, bulletins: list[dict], slugs: list[str]) -> list[str]:
    """Warn about parishes still sitting on an old bulletin after this run.

    A resolver that keeps returning a link we already have leaves no trace
    beyond the `skipped_existing_urls` tally, so a parish can quietly stop
    refreshing for months. Name them instead.
    """
    latest_by_slug: dict[str, str] = {}
    for entry in bulletins:
        slug = entry.get("parish_slug")
        fetched_at = entry.get("fetched_at")
        if not slug or not fetched_at:
            continue
        if fetched_at > latest_by_slug.get(slug, ""):
            latest_by_slug[slug] = fetched_at

    cutoff = (
        (datetime.now(UTC) - timedelta(days=STALE_BULLETIN_AGE_DAYS))
        .replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    stale: list[str] = []
    for slug in slugs:
        latest = latest_by_slug.get(slug)
        if latest is None or latest < cutoff:
            stale.append(slug)
            LOGGER.warning(
                "Parish %s has no bulletin newer than %s days (latest: %s)",
                slug, STALE_BULLETIN_AGE_DAYS, latest or "never fetched",
            )
    return stale


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
