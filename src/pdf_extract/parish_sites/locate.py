"""Finding a parish's bulletin page from its homepage."""

from __future__ import annotations

from datetime import date
from urllib.parse import urljoin

from pdf_extract.browser import PageLike, anchor_text
from pdf_extract.parish_sites.links import (
    document_download_url,
    is_pdf_url,
    looks_like_archive,
)


def find_bulletin_page_urls(
    *, page: PageLike, base_url: str, reference_date: date | None = None,
) -> list[str]:
    """Links that look like the bulletin page, best first.

    A link with "bulletin" in both its address and its text comes before one
    with it in only one of them, and within each, an archive ("Bulletin
    Archive", "2024 Bulletins") comes after the rest; otherwise the page's own
    order is kept.
    """
    this_year = (reference_date or date.today()).year
    both_matches: list[str] = []
    either_matches: list[str] = []
    archives: set[str] = set()
    for anchor in page.query_selector_all("a[href]"):
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        text_lower = anchor_text(anchor).lower()
        href_lower = href.lower()
        has_in_href = "bulletin" in href_lower
        has_in_text = "bulletin" in text_lower
        if not has_in_href and not has_in_text:
            continue
        resolved = urljoin(base_url, href)
        if is_pdf_url(resolved) or document_download_url(resolved) is not None:
            continue
        if has_in_href and has_in_text:
            both_matches.append(resolved)
        else:
            either_matches.append(resolved)
        if looks_like_archive(f"{text_lower} {href_lower}", this_year=this_year):
            archives.add(resolved)

    def _ranked(urls: list[str]) -> list[str]:
        return sorted(urls, key=lambda url: url in archives)

    return list(dict.fromkeys(_ranked(both_matches) + _ranked(either_matches)))


def links_bulletin_pdf(*, page: PageLike, base_url: str) -> bool:
    """Whether the page links a PDF labelled as the bulletin."""
    for anchor in page.query_selector_all("a[href]"):
        href = anchor.get_attribute("href")
        if not isinstance(href, str):
            continue
        resolved = urljoin(base_url, href)
        if (
            (is_pdf_url(resolved) or document_download_url(resolved) is not None)
            and "bulletin" in f"{anchor_text(anchor)} {resolved}".lower()
        ):
            return True
    return False
