"""Find this week's bulletin on a parish's own website.

Three stages, each in its own module:

1. locate: the bulletin page, from the parish's recipe or by following the
   homepage's "bulletin" links (`locate.py`);
2. collect: the PDFs that page offers, by the collectors in order
   (`collectors.py`);
3. choose: this week's issue among them (`choose.py`).

A parish's `Recipe` can pin the first two stages: the page to read, and the
one collector that reads it. Then nothing is guessed for that parish, and a
change made for another site cannot change what it picks.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date

from pdf_extract.browser import PageLike, goto_with_retry, wait_for_selector_quietly
from pdf_extract.parish_sites.choose import (
    CURRENT,
    FALLBACK_MAX_AGE_DAYS,
    Choice,
    OldBulletinOnly,
    choose,
)
from pdf_extract.parish_sites.collectors import (
    COLLECTORS,
    BulletinPage,
    Candidate,
    Collector,
    NoBulletin,
)
from pdf_extract.parish_sites.locate import find_bulletin_page_urls, links_bulletin_pdf

LOGGER = logging.getLogger(__name__)

# A homepage can link "bulletin" from several places (a menu entry, a news post
# about the bulletin, a Drive folder). When a page has no bulletin, the next is
# tried, up to this many.
BULLETIN_PAGES_TO_TRY = 3


@dataclass(frozen=True)
class Recipe:
    """How to read one parish's site, as recorded when it was explored.

    It is kept in the parish's `provider_id` as text: the collector's name, the
    bulletin page's address, or both ("page-pdfs https://example.org/bulletins").
    A collector alone reads the parish's website as the bulletin page.
    """

    page: str | None = None
    """The bulletin page; without it, found from the homepage."""
    collector: str | None = None
    """The one collector that reads `page`; without it, each is tried in turn."""

    def __post_init__(self) -> None:
        if self.collector is not None and self.collector not in COLLECTORS:
            raise ValueError(
                f"Unknown collector {self.collector!r}; expected one of "
                f"{', '.join(COLLECTORS)}"
            )

    @classmethod
    def parse(cls, text: str, *, website: str) -> Recipe:
        page: str | None = None
        collector: str | None = None
        for token in text.split():
            if token.startswith(("http://", "https://")):
                if page is not None:
                    raise ValueError(f"Recipe {text!r} names two pages")
                page = token
            elif collector is None:
                collector = token
            else:
                raise ValueError(f"Recipe {text!r} names two collectors")
        if collector is not None and page is None:
            page = website
        return cls(page=page, collector=collector)

    def text(self, *, website: str) -> str:
        """The recipe as `parse` reads it, leaving out a page that is the website."""
        page = None if self.page == website and self.collector else self.page
        # parse splits on whitespace, so a page whose URL has spaces (eCatholic
        # file names do) is written with them encoded.
        page = page.replace(" ", "%20") if page else page
        return " ".join(part for part in (self.collector, page) if part)


@dataclass(frozen=True)
class Resolution:
    """This week's bulletin, and how the resolver came to it."""

    candidate: Candidate
    page_url: str
    """The bulletin page as linked, before any redirect."""
    collector: str
    reason: str

    @property
    def recipe(self) -> Recipe:
        """The recipe that reads this bulletin the way it was found here."""
        return Recipe(page=self.page_url, collector=self.collector)

    def describe(self) -> str:
        """One line for the run report: "page-pdfs on <page>: current".

        A pick the site dated, but not this week, ends in OLD_PICK_MARK and
        its date, so the report can point it out.
        """
        text = f"{self.collector} on {self.page_url}: {self.reason}"
        dated = self.candidate.parsed_date
        if dated is not None and self.reason != CURRENT:
            text += f"{OLD_PICK_MARK}{dated.isoformat()}"
        return text


# How `Resolution.describe` marks a pick dated before (or after) this week.
OLD_PICK_MARK = ", dated "


def resolve_parish_site(
    *, homepage_url: str, reference_date: date, page: PageLike, recipe: Recipe | None = None,
) -> Resolution:
    recipe = recipe or Recipe()
    collectors = (
        [COLLECTORS[recipe.collector]] if recipe.collector else list(COLLECTORS.values())
    )
    if recipe.page:
        return _resolve_bulletin_page(
            page=page, url=recipe.page, reference_date=reference_date, collectors=collectors,
        )

    bulletin_page_urls = _locate_bulletin_pages(
        page=page, homepage_url=homepage_url, reference_date=reference_date,
    )
    # The first "bulletin" link is not always the bulletin: it can be a news
    # post about it, or an old archive. Try the next ones before giving up,
    # and report the first page's problem if none of them has one.
    # A later link is often an archive, so take a bulletin from it only if it
    # is not plainly an old one. The first link's bulletin is taken whatever
    # its age, but only once no later link has a recent one: a site's
    # "Bulletins" page can be a stale 2017 archive beside "2026 Bulletins".
    failures: list[ValueError] = []
    # What the first page offered, to take its old bulletin from without
    # reading the page again.
    first_page: _Collected | None = None
    pages_to_try = bulletin_page_urls[:BULLETIN_PAGES_TO_TRY]
    for index, url in enumerate(pages_to_try):
        try:
            collected = _collect_bulletin_page(
                page=page, url=url, reference_date=reference_date, collectors=collectors,
            )
            if index == 0:
                first_page = collected
            return collected.resolve(
                reference_date=reference_date, max_age_days=FALLBACK_MAX_AGE_DAYS,
            )
        except ValueError as exc:
            LOGGER.info("No recent bulletin on %s: %s", url, exc)
            failures.append(exc)
    if isinstance(failures[0], OldBulletinOnly) and first_page is not None:
        return first_page.resolve(reference_date=reference_date)
    raise failures[0]


def _locate_bulletin_pages(
    *, page: PageLike, homepage_url: str, reference_date: date,
) -> list[str]:
    goto_with_retry(page=page, page_url=homepage_url)
    wait_for_selector_quietly(
        page=page, selector="a[href]", state="attached", source_label=homepage_url,
    )
    # Links are relative to where the homepage landed, after any redirect.
    base_url = page.url or homepage_url
    urls = find_bulletin_page_urls(page=page, base_url=base_url, reference_date=reference_date)
    # Some homepages link this week's bulletin PDF itself, with no page for
    # it: read the homepage as the bulletin page, after any real one.
    if links_bulletin_pdf(page=page, base_url=base_url):
        urls.append(homepage_url)
    if not urls:
        raise NoBulletin(f"No bulletin page link found for other provider at {homepage_url}")
    return urls


@dataclass(frozen=True)
class _Collected:
    """The PDFs one bulletin page offers, and the collector that found them."""

    url: str
    candidates: list[Candidate]
    collector: Collector

    def resolve(self, *, reference_date: date, max_age_days: int | None = None) -> Resolution:
        choice: Choice = choose(
            self.candidates, reference_date=reference_date, max_age_days=max_age_days,
        )
        return Resolution(
            candidate=choice.candidate, page_url=self.url, collector=self.collector.name,
            reason=choice.reason,
        )


def _resolve_bulletin_page(
    *, page: PageLike, url: str, reference_date: date, collectors: list[Collector],
) -> Resolution:
    collected = _collect_bulletin_page(
        page=page, url=url, reference_date=reference_date, collectors=collectors,
    )
    return collected.resolve(reference_date=reference_date)


def _collect_bulletin_page(
    *, page: PageLike, url: str, reference_date: date, collectors: list[Collector],
) -> _Collected:
    site = BulletinPage(page=page, requested_url=url, reference_date=reference_date)
    site.load()
    found: list[Candidate] = []
    used: Collector | None = None
    for collector in collectors:
        if used is not None and used.final:
            break
        site.return_here()
        more = collector.collect(site, found)
        if more:
            found, used = more, collector
    if used is None:
        raise NoBulletin(f"No PDF links found on bulletin page: {url}")
    return _Collected(url=url, candidates=found, collector=used)
