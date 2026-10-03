"""What a link on a parish site points at: a PDF, a viewer around one, a host.

These only read addresses; nothing here opens a page.
"""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

# ── Google Drive ────────────────────────────────────────────────────────────

GOOGLE_DRIVE_HOST = "drive.google.com"
GOOGLE_DRIVE_FILE_VIEW_URL_TEMPLATE = "https://drive.google.com/file/d/{file_id}/view"
GOOGLE_DRIVE_FILE_DOWNLOAD_URL_TEMPLATE = (
    "https://drive.google.com/uc?export=download&id={file_id}"
)
_GOOGLE_DRIVE_FOLDER_PATH = re.compile(r"/folders/(?P<id>[\w-]+)")
# A Google Drive file shared on its own ("/file/d/<id>/view"), as some parishes
# link each week's bulletin, downloads without a browser from this address.
_GOOGLE_DRIVE_FILE_RE = re.compile(r"^https?://drive\.google\.com/file/d/([\w-]+)")


def google_drive_folder_id(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc.lower() != GOOGLE_DRIVE_HOST:
        return None
    match = _GOOGLE_DRIVE_FOLDER_PATH.search(parsed.path)
    return match.group("id") if match else None


# ── Documents behind addresses that don't end in .pdf ───────────────────────

# Concrete CMS (the Diocese of Albany's rcda.org) links files as
# /download_file/view/<file>/<page>, which redirects to the PDF.
_CONCRETE_DOWNLOAD_RE = re.compile(r"^https?://[^/]+/download_file/(?:view/)?\d+(?:/\d+)?/?$")


def document_download_url(url: str) -> str | None:
    """Where to download a link that is a PDF though its address doesn't say so."""
    match = _GOOGLE_DRIVE_FILE_RE.match(url)
    if match:
        return GOOGLE_DRIVE_FILE_DOWNLOAD_URL_TEMPLATE.format(file_id=match.group(1))
    if _CONCRETE_DOWNLOAD_RE.match(url):
        return url
    return None


# Query parameters that online PDF viewers take the document's own URL in:
# Google Docs' `gview?url=` and pdf.js' `viewer.html?file=`.
_PDF_VIEWER_URL_PARAMS = ("url", "file", "src")


def unwrap_pdf_viewer_url(url: str) -> str:
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


# ── Pages that hand readers the issue somewhere else ────────────────────────

# John Patrick Publishing's "current bulletin" link names a PDF, but redirects
# to the parish's listing on church-bulletin.org, whose issues are dated PDFs
# (/bulletin/<parish>/2026-09-27.pdf).
# A church-bulletin.org listing can be linked directly too ("/?id=4047").
_PUBLISHER_LISTING_URL = re.compile(
    r"^https?://(?:www\.)?(?:jppc\.net/onlinebulletins/\d+template\.pdf"
    r"|church-bulletin\.org/(?:\?id=\d+|[\w-]+/?))$",
    flags=re.IGNORECASE,
)


def is_publisher_listing(url: str) -> bool:
    return bool(_PUBLISHER_LISTING_URL.match(url))


def is_pdf_url(url: str) -> bool:
    """An address that names a PDF, query string or not ("bulletin.pdf?download"),
    and is not a publisher's listing named like one."""
    return urlparse(url).path.lower().endswith(".pdf") and not is_publisher_listing(url)


# Flipbook services a bulletin page can link each week's issue on. Their pages
# name the issue's PDF in a script, which the rendered-HTML scan finds.
FLIPBOOK_HOSTS = frozenset({"designrr.page"})


# ── Embedded PDFs ───────────────────────────────────────────────────────────

# The viewer the PDF Embedder WordPress plugin renders in place of its PDF link.
PDF_EMBEDDER_VIEWER_CLASS = "pdfemb-viewer"

# Up to the ".pdf" that ends the path: WordPress uploads can be named
# "9-20-26.pdf.pdf.pdf", and stopping at the first ".pdf" names a file that 404s.
HTML_PDF_URL_PATTERN = re.compile(
    r'https?://[^\s"\'<>]+?\.pdf(?![\w.\-/%])', flags=re.IGNORECASE,
)


def looks_like_archive(text: str, *, this_year: int) -> bool:
    if "archive" in text:
        return True
    return any(int(year) < this_year for year in re.findall(r"(?<!\d)(20\d{2})(?!\d)", text))
