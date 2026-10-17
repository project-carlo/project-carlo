"""Ways a bulletin page offers its PDFs, each a named collector.

A collector reads the bulletin page (or one page it links) and returns the
PDFs it finds there as candidates. The resolver runs them in COLLECTORS order,
handing each what the ones before it found; a collector returns nothing
unless it has something better, so each only matters on the sites the ones
before it could not read. A `final` collector's find ends the search. A
parish's fetch recipe can name the one collector its site needs.

To teach the resolver a new kind of site, add a collector here, rather than a
branch inside another one, and record the site for tests/test_fetch_replay.py.
"""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from urllib.parse import urljoin, urlparse

from pdf_extract.browser import (
    PageLike,
    anchor_text,
    goto_with_retry,
    wait_for_selector_quietly,
)
from pdf_extract.parish_sites.choose import Candidate, is_convincing, is_current
from pdf_extract.parish_sites.dates import parse_date, parse_date_from_texts
from pdf_extract.parish_sites.links import (
    FLIPBOOK_HOSTS,
    GOOGLE_DRIVE_FILE_DOWNLOAD_URL_TEMPLATE,
    GOOGLE_DRIVE_FILE_VIEW_URL_TEMPLATE,
    HTML_PDF_URL_PATTERN,
    PDF_EMBEDDER_VIEWER_CLASS,
    decoded_base64_json,
    document_download_url,
    google_drive_folder_id,
    is_image_url,
    is_publisher_listing,
    unwrap_pdf_viewer_url,
)

LOGGER = logging.getLogger(__name__)


class NoBulletin(ValueError):
    """The page offers no bulletin a collector can read."""


@dataclass
class BulletinPage:
    """The bulletin page a resolver is reading, and the browser tab it is in.

    Collectors that open another page (a post, a flipbook) leave the tab
    there; `return_here` brings it back before the next collector reads.
    """

    page: PageLike
    requested_url: str
    reference_date: date
    url: str = field(init=False, default="")

    def load(self) -> None:
        goto_with_retry(page=self.page, page_url=self.requested_url)
        # A Drive folder is built by script; its collector waits for its rows.
        if google_drive_folder_id(self.requested_url) is None:
            wait_for_selector_quietly(
                page=self.page, selector="a[href]", state="attached",
                source_label=self.requested_url,
            )
        self.url = self.page.url or self.requested_url

    def return_here(self) -> None:
        if (self.page.url or self.requested_url) != self.url:
            goto_with_retry(page=self.page, page_url=self.requested_url)


@dataclass(frozen=True)
class Collector:
    name: str
    collect: Callable[[BulletinPage, list[Candidate]], list[Candidate]]
    """Candidates on the page, given those the collectors before it found."""
    final: bool = False
    """When it finds anything, no later collector runs."""
    automatic: bool = True
    """Tried on a site without a recipe. One that is not runs only when a
    parish's recipe names it: it reads what most sites have for other uses."""


# ── Shared reading ──────────────────────────────────────────────────────────

_BULLETIN_TITLE_RE = re.compile(
    r"(?:(?:this week'?s|weekly|current|latest|parish|sunday)\s+)?bulletin"
)


def page_pdf_candidates(
    *, page: PageLike, base_url: str, reference_date: date,
) -> list[Candidate]:
    """Every PDF the page in the tab offers: its links, else its markup."""
    candidates: list[Candidate] = []
    for anchor in page.query_selector_all("a[href]"):
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        absolute_href = unwrap_pdf_viewer_url(urljoin(base_url, href))
        fetch_url: str | None = absolute_href
        if ".pdf" not in absolute_href.lower() or is_publisher_listing(absolute_href):
            fetch_url = document_download_url(absolute_href)
            if fetch_url is None:
                continue
        text = anchor_text(anchor)
        candidates.append(
            Candidate(
                source_url=absolute_href,
                fetch_url=fetch_url,
                parsed_date=parse_date_from_texts([text, href, absolute_href], reference_date),
                labelled="bulletin" in f"{text} {absolute_href}".lower(),
                titled_bulletin=bool(_BULLETIN_TITLE_RE.fullmatch(text.strip().lower())),
            )
        )
    if is_convincing(candidates, reference_date):
        return candidates

    # Some WordPress parish sites embed PDFs through script-based viewers (e.g.
    # the DFlip / 3D FlipBook plugin on elmiracatholic.org) which inject the
    # PDF URL as JSON inside a <script> tag rather than a plain <a href="..pdf">,
    # or link a whole block to it by script (Divi). Scan the rendered HTML when
    # the page's links are no bulletin, after those links.
    try:
        html = page.content()
    except Exception:
        html = ""
    linked = {c.source_url for c in candidates}
    candidates += [
        c for c in _pdf_candidates_in_html(html, base_url=base_url, reference_date=reference_date)
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
    return _pdf_candidates_in_html(source, base_url=base_url, reference_date=reference_date)


def _pdf_candidates_in_html(
    html: str, *, base_url: str, reference_date: date,
) -> list[Candidate]:
    if not html:
        return []
    # Unescape JSON-escaped slashes so URLs like "https:\/\/site\/file.pdf"
    # (as embedded by flipbook/PDF-viewer plugins) match a plain URL regex. A
    # viewer's settings can be base64 JSON; their PDFs come after the page's own.
    normalized = "\n".join([html, *decoded_base64_json(html)]).replace("\\/", "/")
    candidates: list[Candidate] = []
    seen: set[str] = set()
    for raw in HTML_PDF_URL_PATTERN.findall(normalized):
        absolute_url = unwrap_pdf_viewer_url(urljoin(base_url, raw))
        if absolute_url in seen or is_publisher_listing(absolute_url):
            continue
        seen.add(absolute_url)
        candidates.append(
            Candidate(
                source_url=absolute_url,
                fetch_url=absolute_url,
                parsed_date=parse_date_from_texts([absolute_url], reference_date),
                labelled="bulletin" in absolute_url.lower(),
            )
        )
    return candidates


def _candidates_on(site: BulletinPage, url: str) -> list[Candidate]:
    """Open `url` in the tab and read its PDFs."""
    goto_with_retry(page=site.page, page_url=url)
    wait_for_selector_quietly(page=site.page, selector="a[href]", state="attached", source_label=url)
    return page_pdf_candidates(
        page=site.page, base_url=site.page.url or url, reference_date=site.reference_date,
    )


# ── Collectors ──────────────────────────────────────────────────────────────

# Each file in a shared folder's listing is a row carrying the file's id.
GOOGLE_DRIVE_ITEM_SELECTOR = "[data-id]"
_GOOGLE_DRIVE_PDF_NAME = re.compile(r"[^\n]*?\.pdf", flags=re.IGNORECASE)


def collect_drive_folder(site: BulletinPage, found: list[Candidate]) -> list[Candidate]:
    """The PDFs a public Drive folder lists, dated by their file names.

    Parishes that keep their bulletins in a shared folder name each file after
    its Sunday ("2026-09-27 Bulletin.pdf"). The folder page is built by script,
    so the files are read from its rendered rows, and each is fetched through
    Drive's direct-download link.
    """
    folder_id = google_drive_folder_id(site.requested_url)
    if folder_id is None:
        return []
    wait_for_selector_quietly(
        page=site.page, selector=GOOGLE_DRIVE_ITEM_SELECTOR, state="attached",
        source_label=site.requested_url,
    )
    candidates: list[Candidate] = []
    seen = {folder_id}
    for item in site.page.query_selector_all(GOOGLE_DRIVE_ITEM_SELECTOR):
        file_id = item.get_attribute("data-id")
        if not file_id or file_id in seen:
            continue
        name = _GOOGLE_DRIVE_PDF_NAME.search(anchor_text(item))
        if name is None:
            continue
        seen.add(file_id)
        candidates.append(
            Candidate(
                source_url=GOOGLE_DRIVE_FILE_VIEW_URL_TEMPLATE.format(file_id=file_id),
                fetch_url=GOOGLE_DRIVE_FILE_DOWNLOAD_URL_TEMPLATE.format(file_id=file_id),
                parsed_date=parse_date(name.group(0).strip(), site.reference_date),
            )
        )
    if not candidates:
        raise NoBulletin(f"No PDF files found in Google Drive folder: {site.requested_url}")
    return candidates


def collect_redirected_pdf(site: BulletinPage, found: list[Candidate]) -> list[Candidate]:
    """A "Bulletin" link that redirects straight to this week's PDF, sometimes by
    script once the page has loaded."""
    if not urlparse(site.url).path.lower().endswith(".pdf"):
        return []
    return [Candidate(source_url=site.url, fetch_url=site.url, parsed_date=None)]


def collect_page_pdfs(site: BulletinPage, found: list[Candidate]) -> list[Candidate]:
    """The PDFs the bulletin page links, or names in its markup."""
    if found:
        return []
    return page_pdf_candidates(
        page=site.page, base_url=site.url, reference_date=site.reference_date,
    )


def collect_linked_issue_page(site: BulletinPage, found: list[Candidate]) -> list[Candidate]:
    """A page that links no PDF can still hand readers the issue elsewhere: a
    flipbook it embeds (this week's, while it lists only older ones), or a
    publisher's listing of dated PDFs."""
    if found:
        return []
    issue_page_url = _embedded_flipbook_url(site) or _publisher_listing_url(site)
    if issue_page_url is None:
        return []
    return _candidates_on(site, issue_page_url)


def _embedded_flipbook_url(site: BulletinPage) -> str | None:
    for frame in site.page.query_selector_all("iframe[src]"):
        src = frame.get_attribute("src")
        if isinstance(src, str) and urlparse(urljoin(site.url, src)).netloc.lower() in FLIPBOOK_HOSTS:
            return urljoin(site.url, src)
    return None


def _publisher_listing_url(site: BulletinPage) -> str | None:
    for anchor in site.page.query_selector_all("a[href]"):
        href = anchor.get_attribute("href")
        if isinstance(href, str) and is_publisher_listing(urljoin(site.url, href)):
            return urljoin(site.url, href)
    return None


def collect_dated_post(site: BulletinPage, found: list[Candidate]) -> list[Candidate]:
    """The PDFs in the latest dated bulletin post the page lists.

    Some sites (e.g. WordPress parish blogs) list each weekly bulletin as a
    dated post that wraps the actual PDF, rather than linking to the PDF
    directly. With PDFs already found, only a post for this week's bulletin
    replaces them, and only if they are something else (a tour guide in the
    menu) or older than it: Sacred Heart, Stamford lists each week's post with
    its PDF, but names this week's PDF "output.pdf".
    """
    post = latest_bulletin_post(site)
    if found:
        if post is None or not is_current(post[0], site.reference_date):
            return []
        newest = max((c.parsed_date for c in found if c.parsed_date), default=None)
        if is_convincing(found, site.reference_date) and (newest is None or newest >= post[0]):
            return []
        return _candidates_on(site, post[1])
    if post is None:
        raise NoBulletin(f"No PDF links found on bulletin page: {site.requested_url}")
    candidates = _candidates_on(site, post[1])
    if not candidates:
        raise NoBulletin(f"No PDF links found on bulletin post page: {post[1]}")
    return candidates


def latest_bulletin_post(site: BulletinPage) -> tuple[date, str] | None:
    """The latest dated non-PDF link that looks like a weekly bulletin post."""
    base_url = site.url
    reference_date = site.reference_date
    dated: list[tuple[date, str]] = []
    # A page that is itself the bulletin listing may title its posts by the
    # Sunday alone ("September 27 - Twenty-Sixth Sunday"). Its dated links on
    # the same site (or a flipbook service) count too, if nothing says "bulletin"
    # and they are current.
    unlabelled: list[tuple[date, str]] = []
    listing_is_bulletins = "bulletin" in base_url.lower()
    post_hosts = {urlparse(base_url).netloc.lower(), *FLIPBOOK_HOSTS}
    base_normalized = base_url.rstrip("/").lower()
    for anchor in site.page.query_selector_all("a[href]"):
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        resolved = urljoin(base_url, href)
        resolved_lower = resolved.lower()
        if resolved_lower.endswith(".pdf") or resolved_lower.rstrip("/") == base_normalized:
            continue
        text = anchor_text(anchor)
        labelled = "bulletin" in href.lower() or "bulletin" in text.lower()
        if not labelled and not (
            listing_is_bulletins and urlparse(resolved).netloc.lower() in post_hosts
        ):
            continue
        parsed_date = parse_date_from_texts([text, href, resolved], reference_date)
        if parsed_date is None:
            continue
        if labelled:
            dated.append((parsed_date, resolved))
        elif is_current(parsed_date, reference_date):
            unlabelled.append((parsed_date, resolved))

    posts = dated or unlabelled
    if not posts:
        return None
    # A listing keeps its newest post at one end. Of this week's posts, take the
    # one nearest that end: an archive of past years has its own "September 27
    # & 28", read without a year as this week's too.
    current = [post for post in posts if is_current(post[0], reference_date)]
    if current:
        steps = list(zip(posts, posts[1:]))
        newer_later = sum(later[0] > earlier[0] for earlier, later in steps)
        older_later = sum(later[0] < earlier[0] for earlier, later in steps)
        return current[-1] if newer_later > older_later else current[0]
    return max(posts, key=lambda pair: pair[0])


# Where an <img> keeps its picture: Squarespace galleries load the full-size
# file from data-image or data-src, after the page's script has run.
_IMAGE_SOURCE_ATTRIBUTES = ("data-image", "data-src", "src")


def collect_page_images(site: BulletinPage, found: list[Candidate]) -> list[Candidate]:
    """Each issue posted as an image, not a PDF: St. Mary, Waymart's Squarespace
    gallery shows each weekend's bulletin as one JPEG ("Bulletin 2026 October
    10-11.jpg"). The download is wrapped in a PDF.

    Only for a parish whose recipe names it: every site has images, and one
    labelled "bulletin" (an icon) is no issue. A picture counts if its address
    or text says "bulletin" or a date; once some are dated, the undated ones
    (a cover template, a logo) are dropped.
    """
    if found:
        return []
    candidates: list[Candidate] = []
    seen: set[str] = set()
    for element in site.page.query_selector_all("img, a[href]"):
        if element.get_attribute("href") is not None:
            sources = [element.get_attribute("href")]
            text = anchor_text(element)
        else:
            sources = [element.get_attribute(name) for name in _IMAGE_SOURCE_ATTRIBUTES]
            text = element.get_attribute("alt") or ""
        for source in sources:
            if not source:
                continue
            url = urljoin(site.url, source)
            if not is_image_url(url) or url in seen:
                continue
            seen.add(url)
            parsed_date = parse_date_from_texts([text, url], site.reference_date)
            labelled = "bulletin" in f"{text} {url}".lower()
            if parsed_date is None and not labelled:
                continue
            candidates.append(
                Candidate(
                    source_url=url, fetch_url=url, parsed_date=parsed_date, labelled=labelled,
                )
            )
    dated = [c for c in candidates if c.parsed_date is not None]
    return dated or candidates


COLLECTORS: dict[str, Collector] = {
    c.name: c
    for c in (
        Collector("drive-folder", collect_drive_folder, final=True),
        Collector("redirected-pdf", collect_redirected_pdf, final=True),
        Collector("page-pdfs", collect_page_pdfs),
        Collector("linked-issue-page", collect_linked_issue_page, final=True),
        Collector("dated-post", collect_dated_post),
        Collector("page-images", collect_page_images, automatic=False),
    )
}
