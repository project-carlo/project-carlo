"""The "other" resolver on the site layouts it has to handle.

Each case is a small hand-written site served by `SnapshotPage`; the real
sites these come from are replayed in test_fetch_replay.py.
"""

from __future__ import annotations

import base64
import json
from datetime import date
from urllib.parse import quote

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
        # Nor are Weebly's numbered folders a month and day ("1/3" of
        # "/1/3/1/4/"), or a mistyped five-digit year a year.
        ("/uploads/1/3/1/4/131484079/bulletin_sept_13.pdf", date(2026, 9, 13)),
        ("September 27, 20026", date(2026, 9, 27)),
        ("/var/m_8/8d/8dc/64111/1024614-09-27-2026-aab32.pdf?download", date(2026, 9, 27)),
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
        # An ordinal after a date is the Sunday's number, not a two-digit year
        # (Saint John Bosco, Conyngham).
        ("10/4-27th Sunday in Ordinary Time", date(2025, 10, 4)),
        ("9/20-25th Sunday in Ordinary Time", date(2026, 9, 20)),
        # Weebly's upload folders are no date: "3/4" is not 4 March
        # (Nativity of Our Lord, Duryea).
        ("/uploads/3/4/1/2/34124530/11th__october_2026_bulletin_.pdf", date(2026, 10, 11)),
        # A file name's spaces as "+" (Our Lady of Peace, Hazleton).
        ("/files/uploaded/10+18+26.pdf", date(2026, 10, 18)),
        ("/files/uploaded/9.20.26+bulletin.pdf", date(2026, 9, 20)),
        ("/files/uploaded/August+2-+2026.pdf", date(2026, 8, 2)),
        ("/files/uploaded/Bulletin+for+July+5.pdf", date(2026, 7, 5)),
        # A year before the month is the issue's (St. Michael the Archangel,
        # Scranton lists a 2022 issue among this year's).
        ("/wp-content/uploads/2022/10/bulletin-2022-october-23.pdf", date(2022, 10, 23)),
        ("Bulletin 2026 October 10-11", date(2026, 10, 10)),
        ("Bulletin_October 12_2025", date(2025, 10, 12)),
        # Pilot Bulletins: the issue's YYMMDD names its folder and its file.
        ("https://www.thebostonpilot.com/bcd/Bulletins/260927/32223_260927.pdf", date(2026, 9, 27)),
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


@pytest.mark.parametrize("encoding_layers", [0, 1, 2])
def test_parishes_online_viewer_unwraps_encoded_pdf(encoding_layers: int) -> None:
    pdf = "https://container.parishesonline.com/bulletins/14/1661/20261025B.pdf"
    selected = pdf
    for _ in range(encoding_layers):
        selected = quote(selected, safe="")
    viewer = (
        "https://parishesonline.com/publication-page/st-james-church-15670"
        f"?selectedPublication={selected}"
    )
    assert unwrap_pdf_viewer_url(viewer) == pdf


@pytest.mark.parametrize(
    ("viewer", "selected"),
    [
        (
            "https://example.org/publication-page/st-james",
            "https://container.parishesonline.com/bulletins/14/1661/20261025B.pdf",
        ),
        (
            "https://parishesonline.com/organization/st-james",
            "https://container.parishesonline.com/bulletins/14/1661/20261025B.pdf",
        ),
        (
            "https://parishesonline.com/publication-page/st-james",
            "https://example.org/20261025B.pdf",
        ),
        (
            "https://parishesonline.com/publication-page/st-james",
            "https://container.parishesonline.com.example.org/bulletins/14/1661/20261025B.pdf",
        ),
        (
            "https://parishesonline.com/publication-page/st-james",
            "http://container.parishesonline.com/bulletins/14/1661/20261025B.pdf",
        ),
        (
            "https://parishesonline.com/publication-page/st-james",
            "https://container.parishesonline.com/other/20261025B.pdf",
        ),
        (
            "https://parishesonline.com/publication-page/st-james",
            "https://container.parishesonline.com/bulletins/14/1661/20261025B.html",
        ),
    ],
)
def test_parishes_online_viewer_leaves_unrecognized_links_alone(viewer: str, selected: str) -> None:
    url = f"{viewer}?selectedPublication={quote(selected, safe='')}"
    assert unwrap_pdf_viewer_url(url) == url


def test_parishes_online_widget_recipe_picks_latest_weekly_pdf() -> None:
    widget = "https://parishesonline.com/publicationWidget?type=bulletin&id=0018000000QxC0DAAV"
    container = "https://container.parishesonline.com/bulletins/14/1661"

    def anchor(issue: str, label: str) -> str:
        selected = quote(f"{container}/{issue}.pdf", safe="")
        return (
            '<a href="/publication-page/st-james-church-15670'
            f'?selectedPublication={selected}">{label}</a>'
        )

    link = build_latest_other_bulletin_links(
        provider_id=HOME, reference_date=TODAY,
        recipe=f"page-pdfs {widget} filename=*B.pdf",
        page=_site({widget: (
            anchor("20261004S", "October 4, 2026 Special")
            + anchor("20260920B", "September 20, 2026")
            + anchor("20260927B", "September 27, 2026")
        )}),
    )
    assert link.source_url == f"{container}/20260927B.pdf"
    assert link.fetch_url == link.source_url


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


def _base64_json(value: dict[str, object]) -> str:
    return base64.b64encode(json.dumps(value).encode()).decode()


def test_pilot_bulletins_embed_pages_resolve_to_their_dated_pdfs() -> None:
    # St. Therese, Shavertown: the bulletin page lists Pilot Bulletins embed
    # pages, below the site menu's undated registration form.
    def embed(issue: str) -> str:
        return f"https://www.thebostonpilot.com/bcd/bulletinclick_embed.asp?Id=32223_{issue}.pdf"

    assert _resolve({
        HOME: '<a href="/bulletins/">Weekly Parish Bulletin</a>',
        f"{HOME}/bulletins/": (
            '<a href="/wp-content/uploads/2024/05/Registration-Form.pdf">Registration</a>'
            f'<a href="{embed("260927")}"><img></a><a href="{embed("260920")}"><img></a>'
        ),
    }) == "https://www.thebostonpilot.com/bcd/Bulletins/260927/32223_260927.pdf"


def test_a_script_naming_a_pdf_in_base64_is_kept_in_a_recording() -> None:
    from pdf_extract.fetch_check import _slim_html

    data = _base64_json({"url": "https://parish.example/b.pdf"})
    kept = f"<script>FB3D_CLIENT_DATA.push('{data}');</script>"
    assert _slim_html(f"{kept}<script>var x = 'eyJhbGciOiJIUzI1NiJ9';</script>") == kept


def test_pdf_embedder_iframe_names_its_pdf_in_base64() -> None:
    # Our Lady of Victory, Tannersville: the PDF Embedder iframe's settings,
    # with the PDF's address, are only in its base64 pdfemb-data parameter.
    pdf = "https://parish.example/wp-content/uploads/2026/09/bulletin9-27-2026.pdf"
    data = _base64_json({"pdfID": 11570, "url": pdf, "title": "bulletin9-27-2026"})
    assert _resolve({
        HOME: '<a href="/bulletin/">Bulletin</a>',
        f"{HOME}/bulletin/": (
            '<a href="/wp-content/uploads/2024/01/Annual-Report-2023.pdf">Annual Report</a>'
            f'<iframe class="pdfembed-iframe" src="{HOME}/?pdfemb-data={data}"></iframe>'
        ),
    }) == pdf


def test_3d_flipbook_names_its_pdf_in_base64_client_data() -> None:
    # St. Thomas More, Lake Ariel: 3D FlipBook pushes its books' settings as
    # base64 JSON, with JSON-escaped slashes.
    pdf = "https://parish.example/download/19/bulletin/18800/bul-september-27-2026.pdf"
    settings = '{"posts":{"1":{"data":{"guid":"%s"}}}}' % pdf.replace("/", "\\/")
    data = base64.b64encode(settings.encode()).decode()
    script = (
        "<script>var FB3D_CLIENT_DATA=window.FB3D_CLIENT_DATA||[];"
        f"FB3D_CLIENT_DATA.push('{data}');</script>"
    )
    assert _resolve({
        HOME: '<a href="/bulletin/">Bulletin</a>',
        f"{HOME}/bulletin/": f'<div class="_3d-flip-book"></div>{script}',
    }) == pdf


def test_base64_that_is_not_json_naming_a_pdf_is_ignored() -> None:
    from pdf_extract.parish_sites.links import decoded_base64_json

    no_pdf = _base64_json({"url": "https://parish.example/page"})
    assert decoded_base64_json(f"x={no_pdf} y=eyJ!!notbase64 z=eyJhbGciOiJIUzI1NiJ9xx") == []


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


def test_a_link_titled_this_weeks_bulletin_beats_one_titled_bulletin() -> None:
    # St. Ignatius, Orrtanna: the Wix header links a 2018 issue as "Bulletin".
    assert _resolve({
        HOME: (
            '<a href="/_files/ugd/old.pdf">Bulletin</a>'
            '<a href="/_files/ugd/new.pdf">This Weeks Bulletin</a>'
        ),
    }) == f"{HOME}/_files/ugd/new.pdf"


def test_a_dated_series_beats_an_undated_unlabelled_first_pdf() -> None:
    # Our Lady of Peace, Hazleton lists a "Parish Consolidation" PDF above its
    # weekly issues, the newest of which can be two weeks old.
    assert _resolve({
        HOME: '<a href="/bulletin">Bulletin</a>',
        f"{HOME}/bulletin": (
            '<a href="/files/Parish+Consolidation-1bcc83bd.pdf">Parish Consolidation</a>'
            '<a href="/files/9.13.26.pdf">24th Sunday in Ordinary Time</a>'
            '<a href="/files/9.6.26.pdf">23rd Sunday in Ordinary Time</a>'
        ),
    }) == f"{HOME}/files/9.13.26.pdf"


def test_an_undated_first_pdf_labelled_bulletin_is_kept_over_a_dated_series() -> None:
    # A bulletin overwritten each week under one name is not dated.
    assert _resolve({
        HOME: '<a href="/bulletin">Bulletin</a>',
        f"{HOME}/bulletin": (
            '<a href="/files/current-bulletin.pdf">This week</a>'
            '<a href="/files/festival-9.13.26.pdf">Festival</a>'
            '<a href="/files/picnic-9.6.26.pdf">Picnic</a>'
        ),
    }) == f"{HOME}/files/current-bulletin.pdf"


def test_one_dated_pdf_does_not_make_a_series() -> None:
    assert _resolve({
        HOME: '<a href="/bulletin">Bulletin</a>',
        f"{HOME}/bulletin": (
            '<a href="/files/latest.pdf">Latest</a>'
            '<a href="/files/festival-9.13.26.pdf">Festival</a>'
        ),
    }) == f"{HOME}/files/latest.pdf"


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


def test_dotnetnuke_linkclick_downloads_are_bulletins() -> None:
    # Saints Peter & Paul, Plains: each issue is a DNN file ticket, labelled by date.
    def ticket(t: str) -> str:
        return f"/LinkClick.aspx?fileticket={t}%3d&amp;tabid=2011&amp;portalid=34&amp;mid=3661"

    assert _resolve({
        HOME: '<a href="/Sunday-Bulletin">Sunday Bulletin</a>',
        f"{HOME}/Sunday-Bulletin": (
            f'<a href="{ticket("A")}">September 20, 2026</a><a href="{ticket("A")}">Download</a>'
            f'<a href="{ticket("B")}">September 27, 2026</a><a href="{ticket("B")}">Download</a>'
        ),
    }) == f"{HOME}/LinkClick.aspx?fileticket=B%3d&tabid=2011&portalid=34&mid=3661"


def test_godaddy_nebula_file_links_are_bulletins() -> None:
    # St. Joseph, Matamoras: one hash-named file per Sunday, dated only in the
    # link text, in no particular order.
    def nebula(h: str) -> str:
        return f"https://nebula.wsimg.com/{h * 32}?AccessKeyId=A3711114AD1870F3198A&amp;disposition=0"

    assert _resolve({
        HOME: '<a href="/bulletins-1.html">Bulletins</a>',
        f"{HOME}/bulletins-1.html": (
            f'<a href="{nebula("a")}">September 20, 2026</a>'
            f'<a href="{nebula("b")}">September 27, 2026</a>'
            f'<a href="{nebula("c")}">September 13, 2026</a>'
        ),
    }) == f"https://nebula.wsimg.com/{'b' * 32}?AccessKeyId=A3711114AD1870F3198A&disposition=0"


def test_a_google_doc_is_downloaded_as_a_pdf() -> None:
    # Most Holy Trinity, Susquehanna links each issue as a shared Google Doc.
    doc = "https://docs.google.com/document/d/18ujWxlm2oDDbN16o-_x/edit?usp=sharing"
    page = f"{HOME}/bulletin"
    source_url, fetch_url = _resolve_other(
        provider_id=page, reference_date=TODAY, recipe="page-pdfs",
        page=_site({page: f'<a href="/bulletin">Bulletin</a><a href="{doc}"></a>'}),
    )
    assert source_url == doc
    assert fetch_url == "https://docs.google.com/document/d/18ujWxlm2oDDbN16o-_x/export?format=pdf"


# ── Bulletins posted as images ──────────────────────────────────────────────

CDN = "https://images.squarespace-cdn.com/content/v1/56b2"
_GALLERY = (
    f'<img data-src="{CDN}/a1/2026+BULLETIN+COVER+TEMPLATE.jpg" '
    f'data-image="{CDN}/a1/2026+BULLETIN+COVER+TEMPLATE.jpg">'
    f'<img src="{CDN}/logo.png" alt="St. Mary">'
    f'<img data-src="{CDN}/b2/Bulletin+2026+September+26-27.jpg?format=1500w" '
    f'data-image="{CDN}/b2/Bulletin+2026+September+26-27.jpg">'
    f'<img data-image="{CDN}/c3/Bulletin+2026+September+19-20.jpg">'
)


def test_a_bulletin_posted_as_an_image_is_read_by_recipe() -> None:
    # St. Mary, Waymart: a Squarespace gallery of one image per weekend, after
    # a cover template that is not an issue.
    page = f"{HOME}/newbulletin"
    link = build_latest_other_bulletin_links(
        provider_id=page, reference_date=TODAY, page=_site({page: _GALLERY}),
        recipe="page-images",
    )
    assert link.source_url == f"{CDN}/b2/Bulletin+2026+September+26-27.jpg"
    assert link.how == f"page-images on {page}: current"


def test_images_are_not_read_without_a_recipe() -> None:
    page = f"{HOME}/newbulletin"
    with pytest.raises(ValueError, match="No PDF links found"):
        _resolve({HOME: '<a href="/newbulletin">Bulletin</a>', page: _GALLERY})


def test_a_downloaded_image_is_kept_as_a_pdf(monkeypatch) -> None:
    from io import BytesIO

    from PIL import Image

    from pdf_extract import fetch

    jpeg = BytesIO()
    Image.new("RGB", (300, 150), "white").save(jpeg, format="JPEG")
    monkeypatch.setattr(fetch, "_http_get", lambda url, **_: fetch._Response(jpeg.getvalue()))
    url = f"{CDN}/b2/Bulletin+2026+September+26-27.jpg"
    pdf = fetch._download_pdf(fetch_url=url, source_url=url)
    assert pdf.startswith(b"%PDF-")
    # The same image makes the same PDF, so a re-fetch is seen as a duplicate.
    assert fetch._download_pdf(fetch_url=url, source_url=url) == pdf


def test_a_download_that_is_neither_pdf_nor_image_is_left_as_it_is(monkeypatch) -> None:
    from pdf_extract import fetch

    monkeypatch.setattr(fetch, "_http_get", lambda url, **_: fetch._Response(b"<html>"))
    url = f"{HOME}/bulletin.pdf"
    assert fetch._download_pdf(fetch_url=url, source_url=url) == b"<html>"


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


def test_a_website_that_is_the_bulletin_pdf_is_taken_as_it_is() -> None:
    # No page to read: the diocese hosts the parish's one weekly file.
    pdf = "https://www.rcdony.org/images/Harrisvillebulletin-1.pdf"
    assert _resolve_other(provider_id=pdf, reference_date=TODAY, page=_site({})) == (pdf, pdf)


def test_a_homepage_download_link_dated_this_week_is_the_bulletin() -> None:
    # cathcommsbse.org: "Download File" links, the week's date only in the file name.
    files = f"{HOME}/var/m_8/8d/8dc/64111"
    assert _resolve({
        HOME: (
            f'<a href="{files}/1024129-Registration_for_RE-6512b.pdf?download">Download File</a>'
            f'<a href="{files}/1024614-09-27-2026-aab32.pdf?download">Download File</a>'
        ),
    }) == f"{files}/1024614-09-27-2026-aab32.pdf?download"


def test_a_publishers_listing_beats_pdfs_that_are_not_the_bulletin() -> None:
    # St. Agnes, Lake Placid: a survey report beside "recent bulletins".
    listing = "https://church-bulletin.org/?id=4047"
    assert _resolve({
        HOME: '<a href="/bulletin">Bulletin</a>',
        f"{HOME}/bulletin": (
            f'<a href="{listing}">recent bulletins</a>'
            f'<a href="{HOME}/s/Gallup-ME25-2024.pdf">the complete survey report</a>'
        ),
        listing: LISTING_HTML,
    }) == "https://www.church-bulletin.org/bulletin/saint-joseph-camillus-ny-13031/2026-09-27.pdf"


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


def test_a_bot_check_over_http_is_retried_over_https(monkeypatch) -> None:
    from pdf_extract import fetch

    asked: list[str] = []

    def get(url: str, **_: object) -> fetch._Response:
        asked.append(url)
        if url.startswith("http://"):
            return fetch._Response(b"<html><head><link rel=stylesheet href=/.well-known/sgcaptcha/>")
        return fetch._Response(b"%PDF-1.5")

    monkeypatch.setattr(fetch, "_http_get", get)
    pdf = "http://example.org/wp-content/uploads/10.18.26-bulletin.pdf"
    download = fetch._download_bulletin(fetch_url=pdf, source_url=pdf)
    assert download.pdf == b"%PDF-1.5"
    assert asked == [pdf, "https://example.org/wp-content/uploads/10.18.26-bulletin.pdf"]


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


def test_recipe_filename_filter_round_trips_and_distinguishes_publishers() -> None:
    recipe = Recipe(HOME, "page-pdfs", filename="St-Annes-Bulletin*.pdf")
    text = "page-pdfs filename=St-Annes-Bulletin*.pdf"
    assert recipe.text(website=HOME) == text
    assert Recipe.parse(text, website=HOME) == recipe
    source = FetchSource(OTHER_TYPE, HOME, text)
    assert _same_recipe(f"{text} {HOME}", source)
    assert not _same_recipe("page-pdfs", source)
    assert not _same_recipe("page-pdfs filename=STTHERESESBULLETIN*.pdf", source)
    with pytest.raises(ValueError, match="nonempty glob"):
        Recipe.parse("page-pdfs filename=", website=HOME)
    with pytest.raises(ValueError, match="two filename filters"):
        Recipe.parse(f"{text} filename=other*.pdf", website=HOME)


@pytest.mark.parametrize("prefix", ["St-Annes-Bulletin", "STTHERESESBULLETIN"])
@pytest.mark.parametrize("other_day", [18, 25])
@pytest.mark.parametrize("other_first", [False, True])
@pytest.mark.parametrize("reference_date", [date(2026, 10, 21), date(2026, 10, 26)])
def test_recipe_selects_its_own_parish_on_a_shared_newest_first_page(
    prefix: str, other_day: int, other_first: bool, reference_date: date,
) -> None:
    other = "STTHERESESBULLETIN" if prefix == "St-Annes-Bulletin" else "St-Annes-Bulletin"
    own_link = f'<a href="/{prefix}-Oct-18-2026.pdf">October 18, 2026</a>'
    other_link = f'<a href="/{other}-Oct-{other_day}-2026.pdf">October {other_day}, 2026</a>'
    links = [other_link, own_link] if other_first else [own_link, other_link]
    links.append(f'<a href="/{prefix}-Oct-4-2026.pdf">October 4, 2026</a>')
    page = f"{HOME}/bulletins/"
    recipe = f"page-pdfs {page} filename={prefix}*.pdf"
    link = build_latest_other_bulletin_links(
        provider_id=HOME, reference_date=reference_date, page=_site({page: "".join(links)}),
        recipe=recipe,
    )
    assert link.source_url == f"{HOME}/{prefix}-Oct-18-2026.pdf"
    assert link.recipe == recipe


def test_recipe_filename_filter_decodes_the_name_and_ignores_case_and_query() -> None:
    pdf = f"{HOME}/files/st%2Dannes-bulletin-20260927.PDF?download=1"
    link = build_latest_other_bulletin_links(
        provider_id=HOME, reference_date=TODAY,
        page=_site({HOME: f'<a href="{pdf}">Bulletin September 27</a>'}),
        recipe="page-pdfs filename=St-Annes-Bulletin*.pdf",
    )
    assert link.source_url == pdf


def test_recipe_filename_filter_fails_when_only_the_other_parish_is_available() -> None:
    with pytest.raises(ValueError, match="No PDF links matching filename"):
        build_latest_other_bulletin_links(
            provider_id=HOME, reference_date=TODAY,
            page=_site({HOME: '<a href="/STTHERESESBULLETIN-20260927.pdf">Bulletin</a>'}),
            recipe="page-pdfs filename=St-Annes-Bulletin*.pdf",
        )


def test_recipe_filename_filter_is_applied_to_a_direct_pdf() -> None:
    pdf = f"{HOME}/STTHERESESBULLETIN-20260927.pdf"
    link = build_latest_other_bulletin_links(
        provider_id=pdf, reference_date=TODAY, page=_site({}),
        recipe="filename=STTHERESESBULLETIN*.pdf",
    )
    assert link.source_url == pdf
    assert "filename=STTHERESESBULLETIN*.pdf" in link.recipe
    with pytest.raises(ValueError, match="does not match filename"):
        build_latest_other_bulletin_links(
            provider_id=pdf, reference_date=TODAY, page=_site({}),
            recipe="filename=St-Annes-Bulletin*.pdf",
        )


def _wix_card(day: str, sunday: str, file: str) -> str:
    return (
        f'<div role="listitem"><div><p><span>{day}</span></p></div>'
        f'<div><p>{sunday}</p></div>'
        f'<div><a href="/_files/ugd/{file}.pdf" aria-label="View"><span>View</span></a></div></div>'
    )


def test_a_wix_card_dates_the_hash_named_pdf_it_links() -> None:
    # St. Charles Borromeo, Ashland: a header "Coat of Arms" PDF, then a grid of
    # cards, each a date, the Sunday's name and a "View" link to a hash-named PDF.
    assert _resolve({
        HOME: '<a href="/bulletins">Bulletins</a>',
        f"{HOME}/bulletins": (
            '<a href="/_files/ugd/23b1db_arms.pdf">Coat of Arms</a>'
            '<div role="list">'
            + _wix_card("August 30, 2026", "Twenty-second Sunday in Ordinary Time", "23b1db_aa")
            + _wix_card("September 27, 2026", "Twenty-sixth Sunday in Ordinary Time", "23b1db_bb")
            + _wix_card("September 20, 2026", "Twenty-fifth Sunday in Ordinary Time", "23b1db_cc")
            + "</div>"
        ),
    }) == f"{HOME}/_files/ugd/23b1db_bb.pdf"


def test_a_card_naming_two_dates_does_not_date_its_link() -> None:
    # An events card giving two days is no issue date: the link stays undated,
    # and the PDF titled "Bulletin" wins.
    assert _resolve({
        HOME: (
            '<div role="listitem"><p>Festival</p><p>September 27, 2026</p>'
            '<p>October 4, 2026</p>'
            '<a href="/_files/ugd/flyer.pdf">View</a></div>'
            '<a href="/_files/ugd/c3.pdf">Bulletin</a>'
        ),
    }) == f"{HOME}/_files/ugd/c3.pdf"


def test_a_page_whose_cards_render_late_is_read_again() -> None:
    # St. Joseph the Worker, Frackville: on a busy run the Wix repeater is still
    # empty when the page is first read, which finds only the header PDF.
    bulletins = f"{HOME}/bulletins"
    early = '<a href="/_files/ugd/23b1db_arms.pdf">Coat of Arms</a><div role="list"></div>'
    late = (
        '<a href="/_files/ugd/23b1db_arms.pdf">Coat of Arms</a><div role="list">'
        + _wix_card("September 27, 2026", "Twenty-sixth Sunday in Ordinary Time", "23b1db_bb")
        + "</div>"
    )

    class LatePage(SnapshotPage):
        def wait_for_timeout(self, timeout: int) -> None:
            self._by_url[bulletins] = PageSnapshot(
                requested_url=bulletins, final_url=bulletins, html=late,
            )
            self.goto(bulletins)

    page = LatePage([
        PageSnapshot(requested_url=HOME, final_url=HOME, html='<a href="/bulletins">Bulletins</a>'),
        PageSnapshot(requested_url=bulletins, final_url=bulletins, html=early),
    ])
    source_url, _ = _resolve_other(provider_id=HOME, reference_date=TODAY, page=page)
    assert source_url == f"{HOME}/_files/ugd/23b1db_bb.pdf"


def test_http_get_percent_encodes_a_non_ascii_referer(monkeypatch):
    # A WordPress file name with an en dash used to raise UnicodeEncodeError
    # when it was sent as the Referer of the next request.
    from pdf_extract import fetch

    seen = {}

    class _Resp:
        headers = {}

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b"%PDF"

    def fake_urlopen(req, timeout):
        seen["referer"] = req.get_header("Referer")
        return _Resp()

    monkeypatch.setattr(fetch, "urlopen", fake_urlopen)
    fetch._http_get("https://example.org/b.pdf", referer="https://example.org/Bulletin – October 18.pdf")
    assert seen["referer"] == "https://example.org/Bulletin%20%E2%80%93%20October%2018.pdf"
    seen["referer"].encode("latin-1")


def test_document_base_url_honours_base_href():
    from pdf_extract.parish_sites.collectors import document_base_url

    html = '<html><head><base href="http://stjohneverettpa.org/"></head><body></body></html>'
    page = "http://stjohneverettpa.org/Bulletins/"
    assert document_base_url(html, page) == "http://stjohneverettpa.org/"
    assert document_base_url("<html><body></body></html>", page) == page
    assert document_base_url("<base target='_blank'>", page) == page


def test_parse_date_reads_an_unseparated_month_day_year_near_the_reference():
    ref = date(2026, 10, 21)
    assert parse_date_from_texts(["10112026.jpg"], ref) == date(2026, 10, 11)
    # YYYYMMDD still wins, and an id whose year is far off is no date.
    assert parse_date_from_texts(["20261018.pdf"], ref) == date(2026, 10, 18)
    assert parse_date_from_texts(["photo-12312011.jpg"], ref) is None


@pytest.mark.parametrize("location", ["script", "served-embed", "late-render"])
def test_other_publishers_current_pdf_cannot_hide_a_filtered_issue(location):
    bulletins = f"{HOME}/bulletins/"
    own = f"{HOME}/Anne-Bulletin-20260927.pdf"
    other = '<a href="/Therese-Bulletin-20260927.pdf">September 27, 2026 Bulletin</a>'
    script = f'<script>var diviElementLinkData = [{{"url":"{own}"}}];</script>'
    initial = other + (script if location == "script" else
                       '<div class="pdfemb-viewer"></div>' if location == "served-embed" else "")

    class LatePage(SnapshotPage):
        waited = False

        def wait_for_timeout(self, timeout):
            self.waited = True
            if location == "late-render":
                self._by_url[bulletins.rstrip("/").lower()] = PageSnapshot(
                    bulletins, bulletins, other + script,
                )
                self.goto(bulletins)

    page = LatePage([PageSnapshot(bulletins, bulletins, initial)],
                    {bulletins: other + script})
    link = build_latest_other_bulletin_links(
        provider_id=HOME, reference_date=TODAY, page=page,
        recipe=f"page-pdfs {bulletins} filename=Anne-Bulletin*.pdf",
    )
    assert link.source_url == own
    assert link.fetch_url == own
    assert page.waited is (location == "late-render")
