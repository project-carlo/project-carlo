"""The "other" resolver on the site layouts it has to handle.

Each case is a small hand-written site served by `SnapshotPage`; the real
sites these come from are replayed in test_fetch_replay.py.
"""

from __future__ import annotations

from datetime import date

import pytest

from pdf_extract.fetch import OTHER_TYPE, FetchSource, build_latest_other_bulletin_links
from pdf_extract.fetch_check import PageSnapshot, SnapshotPage, _same_recipe
from pdf_extract.parish_sites import Recipe
from pdf_extract.parish_sites.dates import parse_date_from_texts
from pdf_extract.parish_sites.links import unwrap_pdf_viewer_url
from pdf_extract.parish_sites.locate import find_bulletin_page_urls

TODAY = date(2026, 9, 26)
HOME = "https://parish.example"


def _resolve_other(**kwargs) -> tuple[str, str]:
    link = build_latest_other_bulletin_links(**kwargs)
    return link.source_url, link.fetch_url


def _site(
    pages: dict[str, str], *, redirects: dict[str, str] | None = None,
    sources: dict[str, str] | None = None,
) -> SnapshotPage:
    """Pages by address; `redirects` sends an address on to another (its page is
    served under the address asked for), and `sources` are pages as served."""
    redirects = redirects or {}
    return SnapshotPage(
        (
            PageSnapshot(requested_url=url, final_url=redirects.get(url, url), html=html)
            for url, html in pages.items()
        ),
        sources,
    )


def _resolve(
    pages: dict[str, str], *, today: date = TODAY, **site: dict[str, str],
) -> str:
    source_url, _ = _resolve_other(
        provider_id=HOME, reference_date=today, page=_site(pages, **site),
    )
    return source_url


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Sept. 27, 2026", date(2026, 9, 27)),
        ("Apr. 5, 2026", date(2026, 4, 5)),
        ("september-27-twenty-sixth-sunday-in-ordinary-time", date(2026, 9, 27)),
        ("Bulletin-September-27-2026.pdf", date(2026, 9, 27)),
        ("/wp-content/uploads/20260927.pdf", date(2026, 9, 27)),
        ("/wp-content/uploads/20260920B.pdf", date(2026, 9, 20)),
        # A day is not the start of the year, and a weekend's second day
        # doesn't hide its year.
        ("Bulletin 04 October 2026", date(2026, 10, 4)),
        ("27-September-2026.pdf", date(2026, 9, 27)),
        ("October 4 & 5, 2025", date(2025, 10, 4)),
        # Without a year: the nearest such day, but not past the coming Sunday.
        ("Bulletin September 27", date(2026, 9, 27)),
        ("Bulletin October 4 & 5", date(2025, 10, 4)),
        ("Bulletin March 28 & 29", date(2026, 3, 28)),
        ("/12-28-bulletin-pdf/", date(2025, 12, 28)),
        # A year folder gives a yearless date its year; a WordPress upload
        # folder (year, then month) does not.
        ("/bulletins/2025/September_28.pdf", date(2025, 9, 28)),
        ("/wp-content/uploads/2025/12/January-4.pdf", date(2026, 1, 4)),
        # Weebly's numeric folder is no year: "3239/02-12" is not a date.
        ("/uploads/3/8/1/3/38133239/02-12-2017_6th_sun.pdf", date(2017, 2, 12)),
        # A ParishesOnline container number is no month and day.
        ("/bulletins/03/0408/20260927B.pdf", date(2026, 9, 27)),
        # Ids and timestamps are not dates.
        ("/bulletins/1790326230.pdf", None),
        ("/_files/ugd/cea846_00334ad9684947469dd533a9f70fcc50.pdf", None),
        # Nor is "e2-4a" inside a Wix file host's id (St. Patrick, Ravena).
        (
            "https://66067635-7ce2-4a3b-8ee4-2d7aacecd675.filesusr.com/ugd/"
            "eb6be9_047b24e2076843a4a39cc7e2d47bd9ab.pdf",
            None,
        ),
        # A WordPress upload folder that runs into a dated file name is the
        # folder's year and month, then the file's date (Sacred Heart, Margaretville).
        ("/wp-content/uploads/2026/10/10-04-2026-1.pdf", date(2026, 10, 4)),
        # An ordinal is a day, not a month or a year (St. John Vianney, Bath).
        ("/wp-content/uploads/Sept.-27th-26th-Sun-in-OT.pdf", date(2026, 9, 27)),
        ("/wp-content/uploads/Sept.-20th-25th-Sun-in-OT.pdf", date(2026, 9, 20)),
        ("September 27th, 2026", date(2026, 9, 27)),
        # A run of digits that is no month-day-year gives a later yearless
        # date no year.
        ("scan 13-45-19 bulletin 9-27", date(2026, 9, 27)),
    ],
)
def test_parse_relaxed_date_reads_file_name_and_abbreviated_dates(text, expected) -> None:
    assert parse_date_from_texts([text], TODAY) == expected


def testunwrap_pdf_viewer_url() -> None:
    pdf = "https://cniffamily.org/wp-content/uploads/2026/09/Bulletin-September-27-2026.pdf"
    assert unwrap_pdf_viewer_url(f"https://docs.google.com/gview?url={pdf}&embedded=true") == pdf
    assert unwrap_pdf_viewer_url(f"{HOME}/pdfjs/web/viewer.html?file={pdf}") == pdf
    # Already a PDF, or no absolute PDF address inside: left alone.
    direct = f"{HOME}/b.pdf?url=https://x.org/a.pdf"
    assert unwrap_pdf_viewer_url(direct) == direct
    relative = f"{HOME}/page?url=/relative.pdf"
    assert unwrap_pdf_viewer_url(relative) == relative


def test_flipbook_pdf_named_with_repeated_extension_is_read_whole() -> None:
    script = (
        '<script>window.option_df_1 = {"source":"https:\\/\\/parish.example\\/wp-content'
        '\\/uploads\\/2026\\/09\\/9-20-26.pdf.pdf.pdf"};</script>'
    )
    assert _resolve({
        HOME: '<a href="/news-bulletins/">News/Bulletins</a>',
        f"{HOME}/news-bulletins/": '<a href="/2026/09/18/september-20-2026-bulletin/">Sept 20</a>',
        f"{HOME}/2026/09/18/september-20-2026-bulletin/": f'<a href="/">Home</a>{script}',
    }) == f"{HOME}/wp-content/uploads/2026/09/9-20-26.pdf.pdf.pdf"


def test_pdf_opened_in_an_online_viewer_resolves_to_the_pdf() -> None:
    pdf = f"{HOME}/wp-content/uploads/2026/09/Bulletin-September-27-2026.pdf"
    assert _resolve({
        HOME: '<a href="/bulletin/">Bulletin</a>',
        f"{HOME}/bulletin/": f'<iframe src="https://docs.google.com/gview?url={pdf}"></iframe>',
    }) == pdf


def test_next_bulletin_link_is_tried_when_the_first_has_no_bulletin() -> None:
    assert _resolve({
        HOME: (
            '<a href="/post/read-the-church-bulletin-online">Read the bulletin</a>'
            '<a href="/bulletins">Bulletins</a>'
        ),
        f"{HOME}/post/read-the-church-bulletin-online": '<a href="/bulletins">here</a>',
        f"{HOME}/bulletins": '<a href="/files/a.pdf">SMDP Bulletin 9.13.26</a>',
    }) == f"{HOME}/files/a.pdf"


def test_a_later_bulletin_link_is_not_trusted_for_an_old_bulletin() -> None:
    with pytest.raises(ValueError, match="No PDF links found on bulletin page"):
        _resolve({
            HOME: '<a href="/bulletin/">Bulletin</a><a href="/bulletin-archive/">Archive</a>',
            f"{HOME}/bulletin/": '<a href="/about/">About</a>',
            f"{HOME}/bulletin-archive/": '<a href="/uploads/2024/04/20230101.pdf">Jan 1</a>',
        })


def test_archive_links_are_tried_after_the_current_bulletin_page() -> None:
    page = _site({
        HOME: (
            '<a href="/copy-of-2021-bulletins">2024 bulletins</a>'
            '<a href="/bulletin-archive">Bulletin Archive</a>'
            '<a href="/copy-of-bulletins">Bulletins</a>'
        ),
    })
    page.goto(HOME)
    assert find_bulletin_page_urls(page=page, base_url=HOME, reference_date=TODAY) == [
        f"{HOME}/copy-of-bulletins",
        f"{HOME}/copy-of-2021-bulletins",
        f"{HOME}/bulletin-archive",
    ]


def test_bulletin_listing_posts_titled_by_their_sunday_are_followed() -> None:
    assert _resolve({
        HOME: '<a href="/category/bulletin/">Weekly Bulletin</a>',
        f"{HOME}/category/bulletin/": (
            '<a href="/september-27-twenty-sixth-sunday-in-ordinary-time/">READ MORE</a>'
            '<a href="/september-20-twenty-fifth-sunday-in-ordinary-time/">READ MORE</a>'
            '<a href="/events/october-18-fall-festival/">Fall Festival</a>'
        ),
        f"{HOME}/september-27-twenty-sixth-sunday-in-ordinary-time/": (
            '<a href="/wp-content/uploads/2026/09/146c_2026_09_27.pdf">Download PDF File</a>'
        ),
    }) == f"{HOME}/wp-content/uploads/2026/09/146c_2026_09_27.pdf"


def test_this_weeks_bulletin_post_wins_over_an_unrelated_pdf() -> None:
    tour = '<a href="/wp-content/uploads/2020/05/SELF-GUIDED-TOUR.pdf">Self-Guided Tour</a>'
    assert _resolve({
        HOME: f'{tour}<a href="/bulletins/">Bulletins</a>',
        f"{HOME}/bulletins/": (
            f'{tour}<a href="/bulletin-09-27-26-26th-sunday/">Bulletin 09.27.26</a>'
            '<a href="/bulletin-09-20-26-25th-sunday/">Bulletin 09.20.26</a>'
        ),
        f"{HOME}/bulletin-09-27-26-26th-sunday/": (
            f'{tour}<a href="/wp-content/uploads/2026/09/Bulletin-09.27.26.pdf">Bulletin</a>'
        ),
    }) == f"{HOME}/wp-content/uploads/2026/09/Bulletin-09.27.26.pdf"


def test_undated_pdf_labelled_bulletin_is_kept_without_visiting_posts() -> None:
    assert _resolve({
        HOME: '<a href="/bulletins/">Bulletins</a>',
        f"{HOME}/bulletins/": (
            '<a href="/_files/ugd/abc.pdf">This week\'s bulletin</a>'
            '<a href="/bulletin-09-27-26/">Bulletin 09.27.26 announcements</a>'
        ),
    }) == f"{HOME}/_files/ugd/abc.pdf"


def test_this_weeks_post_beats_last_weeks_pdf_listed_beside_it() -> None:
    # Sacred Heart, Stamford lists each week's post with its PDF, but names this
    # week's PDF "output.pdf"; read on Saturday, last Sunday's is still current.
    assert _resolve({
        HOME: '<a href="/weekly-bulletin/">Weekly Bulletin</a>',
        f"{HOME}/weekly-bulletin/": (
            '<a href="/10-04-26/">10-04-26</a>'
            '<a href="/wp-content/uploads/2026/10/output.pdf">Download</a>'
            '<a href="/09-27-26/">09-27-26</a>'
            '<a href="/wp-content/uploads/2026/09/09-27-26Web.pdf">Download</a>'
        ),
        f"{HOME}/10-04-26/": '<a href="/wp-content/uploads/2026/10/output.pdf">Download</a>',
    }, today=date(2026, 10, 3)) == f"{HOME}/wp-content/uploads/2026/10/output.pdf"


def test_google_drive_folder_resolves_its_newest_pdf() -> None:
    folder = "https://drive.google.com/drive/folders/FOLDER?usp=sharing"
    rows = "".join(
        f'<tr data-id="{file_id}"><td><div data-id="{file_id}"></div>{name}</td>'
        f"<td>Shared</td><td>Sep 23</td><td>1.2 MB</td></tr>"
        for file_id, name in [
            ("id-0913", "2026-09-13.BULLETIN.pdf"),
            ("id-0927", "2026-09-27.BULLETIN &amp;Insert.pdf"),
            ("id-0920", "2026-09-20.BULLETIN &amp;Insert.pdf"),
            ("id-notes", "Parish notes.docx"),
        ]
    )
    source_url, fetch_url = _resolve_other(
        provider_id=HOME,
        reference_date=TODAY,
        page=_site({
            HOME: f'<a href="{folder}">Bulletins</a>',
            folder: f'<div data-id="FOLDER">Bulletins</div><table>{rows}</table>',
        }),
    )
    assert source_url == "https://drive.google.com/file/d/id-0927/view"
    assert fetch_url == "https://drive.google.com/uc?export=download&id=id-0927"


def test_bulletin_pdf_linked_from_the_homepage_itself() -> None:
    assert _resolve({
        HOME: (
            '<a href="bulletin.pdf">Bulletin</a>'
            '<a href="images/registration.pdf">Download</a>'
        ),
    }) == f"{HOME}/bulletin.pdf"


def test_bulletin_link_that_redirects_to_the_pdf() -> None:
    pdf = f"{HOME}/resources/bulletin.pdf"
    assert _resolve(
        {
            HOME: '<a href="announcements.html">Church Bulletin</a>',
            f"{HOME}/announcements.html": '<embed type="application/pdf">',
        },
        redirects={f"{HOME}/announcements.html": pdf},
    ) == pdf


LISTING = "https://www.church-bulletin.org/saint-joseph-camillus-ny-13031"
TEMPLATE = "https://www.jppc.net/onlinebulletins/4038template.pdf"
LISTING_HTML = "".join(
    f'<a href="https://www.church-bulletin.org/bulletin/saint-joseph-camillus-ny-13031/{day}.pdf">'
    f"{label}</a>"
    for day, label in [("2026-09-27", "View Current Bulletin"), ("2026-09-20", "Sep 20 2026")]
)


@pytest.mark.parametrize(
    "pages",
    [
        {HOME: f'<a href="{TEMPLATE}">Current Bulletin</a>'},
        {
            HOME: '<a href="/bulletins/">Bulletins</a>',
            f"{HOME}/bulletins/": f'<a href="{TEMPLATE}">This Week\'s Bulletin</a>',
        },
    ],
    ids=["from-homepage", "from-bulletin-page"],
)
def test_publisher_template_link_opens_the_publishers_listing(pages) -> None:
    assert _resolve({**pages, TEMPLATE: LISTING_HTML}, redirects={TEMPLATE: LISTING}) == (
        "https://www.church-bulletin.org/bulletin/saint-joseph-camillus-ny-13031/2026-09-27.pdf"
    )


def _flipbook(pdf_name: str) -> str:
    return (
        '<script>FLIPBOOK.options = {"pdfUrl": '
        f'"https:\\/\\/designrr.s3.amazonaws.com\\/parish\\/{pdf_name}"}};</script>'
    )


def test_flipbook_links_on_a_bulletin_page_are_followed() -> None:
    assert _resolve({
        HOME: '<a href="/weekly-bulletin.html">Weekly Bulletin</a>',
        f"{HOME}/weekly-bulletin.html": (
            '<a href="https://designrr.page/?id=1">September 20, 2026</a>'
            '<a href="https://designrr.page/?id=2">September 27, 2026</a>'
        ),
        "https://designrr.page/?id=2": _flipbook("27September2026.pdf"),
    }) == "https://designrr.s3.amazonaws.com/parish/27September2026.pdf"


def test_flipbook_embedded_in_the_bulletin_page_is_this_weeks() -> None:
    assert _resolve({
        HOME: '<a href="/weekly-bulletin.html">Weekly Bulletin</a>',
        f"{HOME}/weekly-bulletin.html": (
            "<p>Week of: September 27, 2026</p>"
            '<iframe src="https://designrr.page/?id=2"></iframe>'
            '<a href="https://designrr.page/?id=1">September 20, 2026</a>'
        ),
        "https://designrr.page/?id=2": _flipbook("27September2026.pdf"),
    }) == "https://designrr.s3.amazonaws.com/parish/27September2026.pdf"


def test_pdf_embedder_post_is_read_as_served() -> None:
    post = f"{HOME}/bulletin-9-27-2/"
    pdf = f"{HOME}/wp-content/uploads/09.27.26.pdf"
    assert _resolve(
        {
            HOME: '<a href="/category/bulletins/">Bulletins</a>',
            f"{HOME}/category/bulletins/": f'<a href="{post}">Bulletin 9/27</a>',
            post: '<div class="pdfemb-viewer"><canvas class="pdfemb-the-canvas"></canvas></div>',
        },
        sources={post: f'<a href="{pdf}" class="pdfemb-viewer">09.27.26</a>'},
    ) == pdf


def test_pdf_linked_by_script_wins_over_an_unrelated_footer_pdf() -> None:
    post = f"{HOME}/bulletin-27-september-2026/"
    pdf = f"{HOME}/wp-content/uploads/09-27-2026-Bulletin.pdf"
    footer = '<a href="/wp-content/uploads/Terms-and-Conditions-2022-1.pdf">Terms</a>'
    assert _resolve({
        HOME: '<a href="/category/bulletins/">Bulletins</a>',
        f"{HOME}/category/bulletins/": f'{footer}<a href="{post}">Bulletin 27 September 2026</a>',
        post: f'{footer}<script>var diviElementLinkData = [{{"url":"{pdf}"}}];</script>',
    }) == pdf


def test_this_years_post_wins_over_last_years_with_the_same_day() -> None:
    # Newest first, without years: last year's "September 27 & 28" reads as
    # this week's too.
    assert _resolve({
        HOME: '<a href="/newsletters">Bulletins</a>',
        f"{HOME}/newsletters": (
            '<a href="/s/PRIVACY-POLICY.pdf">Our Privacy Statement</a>'
            '<a href="/b/bulletin-september-26-amp-27">Bulletin September 26 &amp; 27</a>'
            '<a href="/b/bulletin-september-19-amp-20">Bulletin September 19 &amp; 20</a>'
            '<a href="/b/bulletin-october-4-amp-5">Bulletin October 4 &amp; 5</a>'
            '<a href="/b/bulletin-september-27-amp-28">Bulletin September 27 &amp; 28</a>'
        ),
        f"{HOME}/b/bulletin-september-26-amp-27": (
            '<a href="/s/Bulletin-for-9-2627FINAL.pdf">Bulletin</a>'
        ),
    }) == f"{HOME}/s/Bulletin-for-9-2627FINAL.pdf"


def test_last_years_issue_in_a_year_folder_is_not_this_weeks() -> None:
    # parishes.rcda.org (St. Joseph, Worcester) names files by the day alone.
    assert _resolve({
        HOME: '<a href="/Bulletin.php">Bulletin</a>',
        f"{HOME}/Bulletin.php": (
            '<a href="/bulletins/2025/September_28.pdf">September 28</a>'
            '<a href="/bulletins/2026/September_20.pdf">September 20</a>'
        ),
    }) == f"{HOME}/bulletins/2026/September_20.pdf"


def test_a_listing_oldest_first_gives_its_newest_recent_issue() -> None:
    # St. Joseph, Troy: January first, the newest two weeks old at the end.
    assert _resolve({
        HOME: '<a href="/bulletins">Bulletins</a>',
        f"{HOME}/bulletins": (
            '<a href="/docs/2026_01_04.pdf">Jan. 4, 2026</a>'
            '<a href="/docs/2026_09_06.pdf">September 6, 2026</a>'
            '<a href="/docs/2026_09_13.pdf">September 13, 2026</a>'
        ),
    }) == f"{HOME}/docs/2026_09_13.pdf"


def test_a_link_titled_bulletin_beats_an_undated_first_pdf() -> None:
    # St. Mary's, Glens Falls: its homepage lists a Confirmation PDF first.
    assert _resolve({
        HOME: (
            '<a href="/_files/ugd/a1.pdf">Confirmation</a>'
            '<a href="/_files/ugd/b2.pdf">Community Resources</a>'
            '<a href="/_files/ugd/c3.pdf">Bulletin</a>'
        ),
    }) == f"{HOME}/_files/ugd/c3.pdf"


def test_drive_files_listed_on_the_website_itself_are_read_there() -> None:
    # St. John the Baptist, Walton: its schedule page lists each week's Drive file,
    # and its "Bulletins" link goes to an empty page.
    drive = "https://drive.google.com/file/d/ID-0920/view?usp=drivesdk"
    assert _resolve({
        HOME: (
            '<a href="/bulletins/">Bulletins</a>'
            f'<a href="{drive}">September 20, 2026 Bulletin.pdf</a>'
        ),
        f"{HOME}/bulletins/": '<a href="/bulletins/">Bulletins</a>',
    }) == drive


def test_a_stale_first_bulletin_page_gives_way_to_this_years() -> None:
    # Northern Points: "Bulletins" is a 2017 page beside "2026 Bulletins".
    assert _resolve({
        HOME: (
            '<a href="/bulletins.html">Bulletins</a>'
            '<a href="/2026-bulletins.html">2026 Bulletins</a>'
        ),
        f"{HOME}/bulletins.html": '<a href="/uploads/02-12-2017_6th_sun.pdf">Download File</a>',
        f"{HOME}/2026-bulletins.html": (
            '<a href="/uploads/09-27-26_26th_sun.pdf">Download File</a>'
            '<a href="/uploads/09-20-26_25th_sun.pdf">Download File</a>'
        ),
    }) == f"{HOME}/uploads/09-27-26_26th_sun.pdf"


def test_a_stale_first_bulletin_page_is_still_read_when_nothing_is_newer() -> None:
    assert _resolve({
        HOME: '<a href="/bulletins.html">Bulletins</a>',
        f"{HOME}/bulletins.html": '<a href="/uploads/02-12-2017_6th_sun.pdf">Download File</a>',
    }) == f"{HOME}/uploads/02-12-2017_6th_sun.pdf"


def test_a_stale_first_bulletin_page_is_read_once() -> None:
    site = _site({
        HOME: '<a href="/bulletins.html">Bulletins</a>',
        f"{HOME}/bulletins.html": '<a href="/uploads/02-12-2017_6th_sun.pdf">Download File</a>',
    })
    visited: list[str] = []
    goto = site.goto

    def counting_goto(url: str, **kwargs) -> None:
        visited.append(url)
        goto(url, **kwargs)

    site.goto = counting_goto  # type: ignore[method-assign]
    source_url, _ = _resolve_other(provider_id=HOME, reference_date=TODAY, page=site)
    assert source_url == f"{HOME}/uploads/02-12-2017_6th_sun.pdf"
    assert visited.count(f"{HOME}/bulletins.html") == 1


def test_bulletin_links_are_read_relative_to_where_the_homepage_landed() -> None:
    landing = f"{HOME}/en/home/"
    assert _resolve(
        {
            HOME: '<a href="bulletin/">Bulletin</a>',
            f"{landing}bulletin/": '<a href="/uploads/09-27-26_26th_sun.pdf">Download</a>',
        },
        redirects={HOME: landing},
    ) == f"{HOME}/uploads/09-27-26_26th_sun.pdf"


def test_google_drive_file_links_are_bulletins() -> None:
    # St. Lucy/St. Bernadette, Altamont links one Drive file per Sunday.
    source_url, fetch_url = _resolve_other(
        provider_id=HOME, reference_date=TODAY, page=_site({
            HOME: '<a href="/bulletin">Bulletin</a>',
            f"{HOME}/bulletin": (
                '<a href="https://drive.google.com/file/d/ID-0920/view?usp=sharing">'
                "September 20, 2026</a>"
                '<a href="https://drive.google.com/file/d/ID-0913/view?usp=sharing">'
                "September 13, 2026</a>"
            ),
        }),
    )
    assert source_url == "https://drive.google.com/file/d/ID-0920/view?usp=sharing"
    assert fetch_url == "https://drive.google.com/uc?export=download&id=ID-0920"


def test_concrete_cms_download_links_are_bulletins() -> None:
    # rcda.org lists St. Joan of Arc's issues as /download_file/view/<file>/<page>,
    # beside unrelated PDFs in its menus.
    site = "https://www.rcda.org"
    source_url, _ = _resolve_other(
        provider_id=f"{site}/bulletins", reference_date=TODAY, page=_site({
            f"{site}/bulletins": (
                f'<a href="{site}/application/files/1/Oikoumene_November_2024.pdf">'
                "Oikoumene Newsletter</a>"
                f'<a href="{site}/download_file/view/4445/2079">September 27, 2026</a>'
                f'<a href="{site}/download_file/view/4430/2079">September 20, 2026</a>'
                f'<a href="{site}/bulletins">Bulletins</a>'
            ),
        }),
    )
    assert source_url == f"{site}/download_file/view/4445/2079"


def test_a_download_answered_429_is_retried_once(monkeypatch) -> None:
    # Weebly's file host (St. Michael's, Cohoes) answers 429 to quick requests.
    from urllib.error import HTTPError

    from pdf_extract import fetch

    calls: list[str] = []

    def get(url: str, **_: object) -> fetch._Response:
        calls.append(url)
        if len(calls) == 1:
            raise HTTPError(url, 429, "Too Many Requests", {}, None)  # type: ignore[arg-type]
        return fetch._Response(b"%PDF-1.7")

    monkeypatch.setattr(fetch, "_http_get", get)
    monkeypatch.setattr(fetch.time, "sleep", lambda _: None)
    pdf = f"{HOME}/uploads/bulletin-2026-09-27.pdf"
    assert fetch._download_pdf(fetch_url=pdf, source_url=pdf) == b"%PDF-1.7"
    assert calls == [pdf, pdf]


def test_a_conditional_download_answered_304_brings_back_no_pdf(monkeypatch) -> None:
    from urllib.error import HTTPError

    from pdf_extract import fetch
    from pdf_extract.duplicates import Validators

    sent: list[dict[str, str]] = []

    def get(url: str, *, extra_headers=None, **_: object) -> fetch._Response:
        sent.append(dict(extra_headers or {}))
        if extra_headers:
            raise HTTPError(url, 304, "Not Modified", {}, None)  # type: ignore[arg-type]
        return fetch._Response(b"%PDF-1.7", etag='"v2"', last_modified="Sun, 27 Sep 2026")

    monkeypatch.setattr(fetch, "_http_get", get)
    pdf = f"{HOME}/uploads/bulletin.pdf"

    download = fetch._download_bulletin(
        fetch_url=pdf, source_url=pdf, validators=Validators('"v1"', "Sat, 26 Sep 2026"),
    )
    assert download == fetch.Download(pdf=None)
    assert sent == [{"If-None-Match": '"v1"', "If-Modified-Since": "Sat, 26 Sep 2026"}]

    download = fetch._download_bulletin(fetch_url=pdf, source_url=pdf)
    assert download == fetch.Download(b"%PDF-1.7", etag='"v2"', last_modified="Sun, 27 Sep 2026")


def test_a_304_to_an_unconditional_download_is_a_failure(monkeypatch) -> None:
    from urllib.error import HTTPError

    from pdf_extract import fetch

    def get(url: str, **_: object) -> fetch._Response:
        raise HTTPError(url, 304, "Not Modified", {}, None)  # type: ignore[arg-type]

    monkeypatch.setattr(fetch, "_http_get", get)
    pdf = f"{HOME}/uploads/bulletin.pdf"
    with pytest.raises(HTTPError):
        fetch._download_bulletin(fetch_url=pdf, source_url=pdf)


# ── Recipes ─────────────────────────────────────────────────────────────────

def test_recipe_reads_collector_page_or_both() -> None:
    page = f"{HOME}/bulletins"
    assert Recipe.parse("", website=HOME) == Recipe()
    assert Recipe.parse(page, website=HOME) == Recipe(page=page)
    assert Recipe.parse(f"dated-post {page}", website=HOME) == Recipe(page, "dated-post")
    # A collector alone reads the website as the bulletin page.
    assert Recipe.parse("page-pdfs", website=page) == Recipe(page, "page-pdfs")
    assert Recipe(page, "page-pdfs").text(website=page) == "page-pdfs"
    assert Recipe(page, "page-pdfs").text(website=HOME) == f"page-pdfs {page}"
    with pytest.raises(ValueError, match="Unknown collector 'pdfs'"):
        Recipe.parse("pdfs", website=HOME)
    with pytest.raises(ValueError, match="two pages"):
        Recipe.parse(f"{page} {HOME}", website=HOME)
    # A page with spaces in its URL is written so that parse reads it back.
    spaced = f"{HOME}/documents/Parish Bulletin - October 18 2026.pdf"
    text = Recipe(spaced, "redirected-pdf").text(website=HOME)
    assert Recipe.parse(text, website=HOME) == Recipe(spaced.replace(" ", "%20"), "redirected-pdf")


def test_a_recipe_skips_the_homepage_and_runs_only_its_collector() -> None:
    # The homepage is not recorded: a pinned page is read without it. The page
    # lists this week's post, which dated-post would follow, and an older PDF.
    pages = {
        f"{HOME}/bulletins": (
            '<a href="/files/bulletin-2026-09-20.pdf">Bulletin</a>'
            '<a href="/2026/09/25/bulletin-september-27/">Bulletin for September 27</a>'
        ),
        f"{HOME}/2026/09/25/bulletin-september-27/": '<a href="/files/0927.pdf">Read it</a>',
    }
    link = build_latest_other_bulletin_links(
        provider_id=HOME, reference_date=TODAY, page=_site(pages),
        recipe=f"page-pdfs {HOME}/bulletins",
    )
    assert link.source_url == f"{HOME}/files/bulletin-2026-09-20.pdf"
    assert link.how == f"page-pdfs on {HOME}/bulletins: current"
    assert link.recipe == f"page-pdfs {HOME}/bulletins"


def test_a_recipe_whose_collector_finds_nothing_fails_rather_than_guessing() -> None:
    pages = {f"{HOME}/bulletins": '<iframe src="https://designrr.page/?id=1"></iframe>'}
    with pytest.raises(ValueError, match="No PDF links found on bulletin page"):
        _resolve_other(
            provider_id=HOME, reference_date=TODAY, page=_site(pages),
            recipe=f"page-pdfs {HOME}/bulletins",
        )


def test_a_recipe_written_differently_is_the_same_recipe() -> None:
    source = FetchSource(OTHER_TYPE, HOME, f"page-pdfs {HOME}")
    assert _same_recipe("page-pdfs", source)
    assert _same_recipe(f"{HOME}/b page-pdfs", source._replace(recipe=f"page-pdfs {HOME}/b"))
    assert not _same_recipe(f"page-pdfs {HOME}/b", source)
    assert not _same_recipe("page-pdfs", source._replace(recipe=""))
