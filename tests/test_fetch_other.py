"""The "other" resolver on the site layouts it has to handle.

Each case is a small hand-written site served by `SnapshotPage`; the real
sites these come from are replayed in test_fetch_replay.py.
"""

from __future__ import annotations

from datetime import date

import pytest

from pdf_extract.fetch import (
    _find_other_bulletin_page_urls,
    _parse_relaxed_date,
    _resolve_other_latest_link,
    _unwrap_pdf_viewer_url,
)
from pdf_extract.fetch_check import PageSnapshot, SnapshotPage

TODAY = date(2026, 9, 26)
HOME = "https://parish.example"


def _site(pages: dict[str, str]) -> SnapshotPage:
    return SnapshotPage(
        PageSnapshot(requested_url=url, final_url=url, html=html) for url, html in pages.items()
    )


def _resolve(pages: dict[str, str]) -> str:
    source_url, _ = _resolve_other_latest_link(
        provider_id=HOME, reference_date=TODAY, page=_site(pages),
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
        # Ids and timestamps are not dates.
        ("/bulletins/1790326230.pdf", None),
        ("/_files/ugd/cea846_00334ad9684947469dd533a9f70fcc50.pdf", None),
    ],
)
def test_parse_relaxed_date_reads_file_name_and_abbreviated_dates(text, expected) -> None:
    assert _parse_relaxed_date(text, TODAY) == expected


def test_unwrap_pdf_viewer_url() -> None:
    pdf = "https://cniffamily.org/wp-content/uploads/2026/09/Bulletin-September-27-2026.pdf"
    assert _unwrap_pdf_viewer_url(f"https://docs.google.com/gview?url={pdf}&embedded=true") == pdf
    assert _unwrap_pdf_viewer_url(f"{HOME}/pdfjs/web/viewer.html?file={pdf}") == pdf
    # Already a PDF, or no absolute PDF address inside: left alone.
    direct = f"{HOME}/b.pdf?url=https://x.org/a.pdf"
    assert _unwrap_pdf_viewer_url(direct) == direct
    relative = f"{HOME}/page?url=/relative.pdf"
    assert _unwrap_pdf_viewer_url(relative) == relative


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
    assert _find_other_bulletin_page_urls(page=page, base_url=HOME, reference_date=TODAY) == [
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
    source_url, fetch_url = _resolve_other_latest_link(
        provider_id=HOME,
        reference_date=TODAY,
        page=_site({
            HOME: f'<a href="{folder}">Bulletins</a>',
            folder: f'<div data-id="FOLDER">Bulletins</div><table>{rows}</table>',
        }),
    )
    assert source_url == "https://drive.google.com/file/d/id-0927/view"
    assert fetch_url == "https://drive.google.com/uc?export=download&id=id-0927"
