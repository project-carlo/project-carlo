"""Looking things up on the web while exploring a diocese.

Everything here answers one of the questions the model turns on, cheaply and
without a browser:

- `probe_url`: is this parish website alive, whose is it now, and which
  bulletin does it embed? (A lapsed parish domain is often bought by a spam
  network; a redirect into a family site often means the parish folded in.)
- `probe_container`: is this ParishesOnline bulletin container still
  publishing, and what does its latest masthead say?
- `pdf_text`: what does this bulletin say? (Mastheads, Mass schedules, closing
  announcements.)
- `recheck`: do the quotes recorded as evidence still appear at their URLs?

Nothing here writes to the records; the caller decides what the answer means.
"""

from __future__ import annotations

import datetime as dt
import gzip
import html
import io
import re
import socket
import unicodedata
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
TIMEOUT = 30
# Scanned bulletins run past 30 MB (Spirit of Hope, Oneida: 31 MB in 2026),
# and LPi family bulletins past 180 MB. A truncated PDF does not parse at all.
MAX_BYTES = 250_000_000

PO_CONTAINER_BASE = "https://container.parishesonline.com/bulletins"


@dataclass
class Response:
    url: str
    status: int | None = None
    final_url: str = ""
    content_type: str = ""
    body: bytes = b""
    error: str = ""
    truncated: bool = False  # the body stopped at max_bytes

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300

    def text(self) -> str:
        return self.body.decode("utf-8", "replace")


def fetch(url: str, *, method: str = "GET", timeout: int = TIMEOUT,
          max_bytes: int = MAX_BYTES) -> Response:
    """GET (or HEAD) a URL; failures come back as `error`, never as an exception."""
    req = Request(url, method=method, headers={
        "User-Agent": USER_AGENT, "Accept": "text/html,application/pdf,*/*",
        "Accept-Encoding": "gzip",
    })
    for attempt in (1, 2):
        try:
            with urlopen(req, timeout=timeout) as resp:
                body = resp.read(max_bytes + 1) if method != "HEAD" else b""
                truncated = len(body) > max_bytes
                body = body[:max_bytes]
                if resp.headers.get("Content-Encoding") == "gzip" and body and not truncated:
                    body = gzip.decompress(body)
                return Response(url, resp.status, resp.geturl(),
                                resp.headers.get("Content-Type", ""), body, truncated=truncated)
        except HTTPError as e:
            return Response(url, e.code, e.geturl() or url, error=f"HTTP {e.code}")
        except (URLError, OSError, ValueError) as e:
            reason = getattr(e, "reason", e)
            # A reset or dropped connection mid-transfer is usually transient
            # (Discover Mass downloads do it); try once more before reporting.
            if attempt == 1 and isinstance(reason, (ConnectionError, TimeoutError)):
                continue
            return Response(url, error=f"{type(reason).__name__}: {reason}")
    raise AssertionError("unreachable")


# ── Text ────────────────────────────────────────────────────────────────────
def html_text(page: str) -> str:
    page = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", page, flags=re.S | re.I)
    page = re.sub(r"<br\s*/?>|</(p|div|li|tr|h\d)>", "\n", page, flags=re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", page))
    return "\n".join(" ".join(line.split()) for line in text.splitlines() if line.strip())


def pdf_pages(data: bytes) -> list[str]:
    """Text of each page; an empty string for a page that is a scanned image."""
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    pages = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
            # Some LPi PDFs separate words with control characters (\x03):
            # show them as spaces so a quote copied from here is what recheck finds.
            pages.append(re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", text).strip())
        except Exception:  # noqa: BLE001 - one bad page should not lose the rest
            pages.append("")
    return pages


def _is_pdf(resp: Response) -> bool:
    return "pdf" in resp.content_type.lower() or resp.body[:5] == b"%PDF-"


def page_text(resp: Response) -> str:
    if _is_pdf(resp):
        return "\n\n".join(pdf_pages(resp.body))
    return html_text(resp.text())


def pdf_text(url: str, *, pages: int = 3, chars: int = 3000,
             grep: Iterable[str] = ()) -> dict[str, Any]:
    """The first readable pages of a bulletin PDF, and where given words occur in it.

    The masthead (the list of parishes a bulletin serves) is often not on page
    1: LPi wraps many bulletins in a generic cover reflection. Ask for a few
    pages. `grep` counts each term on every page and quotes the matching
    lines, which is how to date a closure: find the issue where a church's
    Mass-schedule code stops appearing, or the one announcing its last Mass.
    """
    resp = fetch(url)
    if not resp.ok:
        return {"url": url, "error": resp.error or f"HTTP {resp.status}"}
    if not _is_pdf(resp):
        return {"url": url, "error": f"not a PDF ({resp.content_type or 'unknown type'})"}
    if resp.truncated:
        return {"url": url, "error": f"larger than {MAX_BYTES // 1_000_000} MB: not read"}
    try:
        texts = pdf_pages(resp.body)
    except Exception as exc:  # noqa: BLE001 - a broken issue should not stop a container walk
        return {"url": url, "error": f"could not read the PDF: {exc}"}
    readable = [(n, t) for n, t in enumerate(texts, 1) if t]
    out: dict[str, Any] = {
        "url": url, "page_count": len(texts), "readable_pages": len(readable),
        "pages": [{"page": n, "text": t[:chars]} for n, t in readable[:pages]],
    }
    if not readable:
        out["note"] = ("no extractable text: the issue is scanned images. Try an older issue "
                       "from the same source, which is often text and has the same masthead.")
    elif len(readable) < len(texts):
        # A masthead or Mass schedule on an image-only page is silently absent
        # from `pages` and `grep`; say which pages those are.
        out["pages_without_text"] = [n for n, t in enumerate(texts, 1) if not t]
        out["note"] = ("some pages are images with no text layer (pages_without_text): "
                       "a masthead or schedule there is invisible to pages and grep")
    terms = [t for t in grep if t]
    if terms:
        out["grep"] = {}
        for term in terms:
            pattern = re.compile(re.escape(term), re.I)
            hits = []
            for n, t in enumerate(texts, 1):
                lines = [line.strip() for line in t.splitlines() if pattern.search(line)]
                if lines:
                    hits.append({"page": n, "count": len(pattern.findall(t)), "lines": lines[:8]})
            out["grep"][term] = {"total": sum(h["count"] for h in hits), "pages": hits}
    return out


# ── Publishers ──────────────────────────────────────────────────────────────
# Each pattern must capture the id IN FULL. An LPi publicationWidget id is an
# 18-character Salesforce id: matched as digits it truncates to the prefix
# every LPi parish shares (00180000), and unrelated parishes look like one
# bulletin.
PUBLICATION_PATTERNS = [
    ("lpi", r"publicationWidget\?[^\"'<>]*?\bid=([A-Za-z0-9]{18}|[A-Za-z0-9]{15})\b"),
    ("po-container", r"container\.parishesonline\.com/bulletins/(\d+/\d+)/"),
    # The same container's issues linked through the org's /find/ page, e.g.
    # parishesonline.com/find/<slug>/bulletin/file/03-1424-20260927B.pdf is 03/1424.
    ("po-container", r"parishesonline\.com/find/[a-z0-9-]+/bulletin/file/(\d+-\d+)-\d{8}"),
    ("po-org", r"parishesonline\.com/organization/([a-z0-9-]{3,120})"),
    ("ecatholic", r"files\.ecatholic\.com/(\d{3,8})/"),
    ("discovermass", r"discovermass\.com/church/([a-z0-9-]{3,120})"),
]


def find_publications(page: str) -> list[str]:
    """Bulletin-publisher ids embedded in a page, as `scheme:value` publication ids."""
    found: list[str] = []
    for scheme, pattern in PUBLICATION_PATTERNS:
        for value in re.findall(pattern, page, flags=re.I):
            if scheme == "po-container":
                value = value.replace("-", "/")
            pub = f"{scheme}:{value if scheme == 'lpi' else value.lower()}"
            if pub not in found:
                found.append(pub)
    return found


def bulletin_links(page: str, base: str, limit: int = 15) -> list[str]:
    links = []
    for href in re.findall(r"""href=["']([^"'#]+)["']""", page, flags=re.I):
        low = href.lower()
        if "bulletin" in low or low.split("?")[0].endswith(".pdf"):
            full = urljoin(base, html.unescape(href))
            if full not in links:
                links.append(full)
    return links[:limit]


# ── Parish websites ─────────────────────────────────────────────────────────
# Lapsed parish domains get bought by spam networks. Two Buffalo parish domains
# fell to one online-slots network whose vocabulary was not in the first
# version of this list, and were reported as redirects "into a family site",
# which is the label that means "collapse this row". Multi-word where the one
# word has an innocent parish use (time slots, lotteries, direct deposit).
# Matched as whole words: Wix pages carry config keys like `forExpressButtons`,
# and "judicial" is common on parish sites.
SPAM_TERMS = [
    "casino", "roulette", "betting", "sportsbook", "viagra", "cialis", "escort", "porn",
    "payday", "forex", "judi", "togel", "gacor", "maxwin", "slot online", "situs slot",
    "slot gacor", "slot terpercaya", "pragmatic play",
]
# Whole words only: Wix pages carry config keys like
# "DisplayCheckoutErrorModalsForExpressButtons", which contain "forex".
_SPAM_RE = re.compile(r"\b(?:" + "|".join(re.escape(t) for t in SPAM_TERMS) + r")\b")


def spam_terms(text: str) -> list[str]:
    """The SPAM_TERMS found in text as whole words (case-insensitive)."""
    found = set(_SPAM_RE.findall(text.lower()))
    return [t for t in SPAM_TERMS if t in found]


PARISH_WORDS = [
    "parish", "church", "catholic", "mass", "bulletin", "diocese", "gospel", "liturgy",
    "sacrament", "worship", "rosary",
]


def looks_squatted(text: str) -> bool:
    """Spam vocabulary that means a squatter, not a passing mention.

    A squat page repeats its terms; a live parish page can name one in its news (a
    Schenectady parish announced a dinner "at Rivers Casino & Resort"). One term, at most
    twice, on a page that still has parish vocabulary is not a squat.
    """
    low = text.lower()
    hits = _SPAM_RE.findall(low)
    if not hits:
        return False
    if len(set(hits)) >= 2 or len(hits) >= 3:
        return True
    return not any(w in low for w in PARISH_WORDS)

VERDICT_NOTES = {
    "DEAD-DNS": "the domain does not resolve (checked twice, with and without www.)",
    "UNREACHABLE": "resolves but did not answer: often an IPv6-only host; check in a browser",
    "SPAM-SQUAT": "the domain has been taken over by spam; the parish has moved or folded in",
    "REDIRECT-OFFSITE": "redirects to another site: read the target. A family site means the "
                        "parish may have folded in; anything else may be a squat",
    "HTTP4XX": "the server refused: bot-blocking (403) is common and usually harmless",
    "HTTP5XX": "server error: retry later",
    "NO-PARISH-WORDS": "no parish vocabulary in the HTML: usually a JavaScript-rendered site",
    "ok": "",
}


def _host(url: str) -> str:
    return (urlsplit(url).hostname or "").lower()


def _registrable(host: str) -> str:
    return ".".join(host.removeprefix("www.").split(".")[-2:])


def _resolves(host: str) -> bool:
    for _ in range(2):  # a single resolver failure has been wrong before
        try:
            socket.getaddrinfo(host, 443)
            return True
        except OSError:
            continue
    return False


def probe_url(url: str) -> dict[str, Any]:
    """What is at a parish website now, and which bulletin does it embed?"""
    out: dict[str, Any] = {"url": url}
    host = _host(url)
    if not host:
        return {**out, "verdict": "BAD-URL"}
    if not _resolves(host):
        alt = host[4:] if host.startswith("www.") else f"www.{host}"
        if _resolves(alt):
            out["note"] = f"{host} does not resolve but {alt} does; use that"
            url = url.replace(host, alt, 1)
            out["url_tried"] = url
        else:
            return {**out, "verdict": "DEAD-DNS", "detail": VERDICT_NOTES["DEAD-DNS"]}
    resp = fetch(url, max_bytes=3_000_000)
    out["status"] = resp.status
    if resp.final_url and resp.final_url.rstrip("/") != url.rstrip("/"):
        out["final_url"] = resp.final_url
    if resp.status is None:
        return {**out, "verdict": "UNREACHABLE", "detail": f"{resp.error}; "
                f"{VERDICT_NOTES['UNREACHABLE']}"}
    page = resp.text()
    low = page.lower()
    title = re.search(r"<title[^>]*>(.*?)</title>", page, flags=re.S | re.I)
    if title:
        out["title"] = " ".join(html.unescape(title.group(1)).split())[:160]
    spam = spam_terms(page)
    words = [w for w in PARISH_WORDS if w in low]
    out["publications"] = find_publications(page)
    out["bulletin_links"] = bulletin_links(page, resp.final_url or url)
    if spam:
        out["spam_terms"] = spam
    if spam and looks_squatted(page):
        verdict = "SPAM-SQUAT"
    elif resp.final_url and _registrable(_host(resp.final_url)) != _registrable(host):
        verdict = "REDIRECT-OFFSITE"
    elif resp.status >= 500:
        verdict = "HTTP5XX"
    elif resp.status >= 400:
        verdict = "HTTP4XX"
    elif not words:
        verdict = "NO-PARISH-WORDS"
    else:
        verdict = "ok"
    return {**out, "verdict": verdict, "detail": VERDICT_NOTES.get(verdict, "")}


def probe_urls(urls: list[str], workers: int = 8) -> list[dict[str, Any]]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(probe_url, urls))


# ── ParishesOnline containers ───────────────────────────────────────────────
def _last_sunday(on: dt.date) -> dt.date:
    return on - dt.timedelta(days=(on.weekday() + 1) % 7)


def container_issue_url(container: str, sunday: dt.date) -> str:
    return f"{PO_CONTAINER_BASE}/{container.strip('/')}/{sunday:%Y%m%d}B.pdf"


def probe_container(container: str, *, weeks: int = 12, start: dt.date | None = None,
                    step: int = 1, all_issues: bool = False, pages: int = 0,
                    chars: int = 2500) -> dict[str, Any]:
    """Walk back Sunday by Sunday through a ParishesOnline bulletin container.

    Containers serve one PDF per Sunday at a fixed, unauthenticated path. The
    family bulletin publishing this week while a member parish's own former
    container has gone silent is the evidence that the member folded in; a
    silent container with no live one to fold into only means the publisher
    changed. A missing issue answers 403, not 404, so "403 every week" is the
    dead signal; confirm the prober against a container you know is live.

    `step` > 1 samples every n-th Sunday (4 is monthly), and `all_issues`
    keeps going after the first hit: reading two mastheads months apart shows
    who joined and who left. `pages` > 0 includes the text of each issue found.
    """
    container = container.strip().strip("/")
    if not re.fullmatch(r"\d+/\d+", container):
        raise ValueError(f"a container looks like 14/0434, got {container!r}")
    # Without a start, begin at the coming Sunday: its issue is usually up by
    # mid-week, and starting at the last one missed it on a Saturday.
    sunday = _last_sunday(start or dt.date.today() + dt.timedelta(days=6))
    issues, found = [], []
    for i in range(0, weeks, max(1, step)):
        day = sunday - dt.timedelta(weeks=i)
        url = container_issue_url(container, day)
        resp = fetch(url, method="HEAD")
        issues.append({"date": day.isoformat(), "status": resp.status or resp.error})
        if resp.ok:
            found.append(url)
            if not all_issues:
                break
    out: dict[str, Any] = {
        "container": container, "latest": found[0] if found else None,
        "found": len(found), "probed": issues,
    }
    if not found:
        out["note"] = (f"no issue in {len(issues)} Sundays probed. A missing issue answers 403; "
                       "check the prober against a live container before calling this dead.")
    if pages and found:
        out["issues"] = [pdf_text(url, pages=pages, chars=chars) for url in found]
    return out


# ── ParishesOnline organizations ────────────────────────────────────────────
# The API behind parishesonline.com. An organization's `salesforce_id` is the
# same id LPi parish sites embed as publicationWidget?id=, so a widget found on
# a parish site leads to the organization and its bulletin container in two
# requests, and so does an org slug found in a "Bulletin" link.
PO_API = "https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod"
_SFID_RE = re.compile(r"^[A-Za-z0-9]{15}(?:[A-Za-z0-9]{3})?$")


def _po_json(path: str) -> Any:
    import json

    resp = fetch(f"{PO_API}/{path}")
    if not resp.ok:
        return None
    try:
        return json.loads(resp.body).get("data")
    except (ValueError, AttributeError):
        return None


def parishes_online_org(key: str, *, issues: int = 6) -> dict[str, Any]:
    """A ParishesOnline organization by org slug or LPi/Salesforce id, with its latest issues.

    Returns the organization's own address and website, its publication ids in
    every form they turn up in (po-org, lpi, po-container), and its most
    recent bulletins. An organization whose newest issue is months old has
    stopped publishing there.
    """
    key = key.strip().rstrip("/").rsplit("/", 1)[-1]
    org = _po_json(f"organizations/{key}" if _SFID_RE.match(key) and any(
        c.isdigit() for c in key) else f"organizations/slug/{key}")
    if not org:
        return {"key": key, "error": "no such organization (check the slug or id)"}
    sfid = org.get("salesforce_id", "")
    pubs = _po_json(f"organizations/{sfid}/publications") or []
    containers = sorted({m.group(1) for p in pubs if (m := re.search(
        r"/bulletins/(\d+/\d+)/", p.get("fileUrl") or ""))})
    address = ", ".join(str(org[k]) for k in ("physical_street", "physical_city",
                                                "physical_state", "physical_postal_code")
                        if org.get(k))
    latest = pubs[0].get("publishDate", "")[:10] if pubs else ""
    out = {
        "slug": org.get("slug"), "lpi_id": sfid, "title": org.get("physical_title"),
        "website": org.get("website"), "address": address,
        "latitude": org.get("latitude"), "longitude": org.get("longitude"),
        "org_url": f"https://parishesonline.com/organization/{org.get('slug')}",
        "publication_ids": [f"po-org:{org.get('slug')}", f"lpi:{sfid}",
                            *(f"po-container:{c}" for c in containers)],
        "latest_issue": latest,
        "issues": [{"date": p.get("publishDate", "")[:10], "type": p.get("type"),
                    "url": p.get("fileUrl")} for p in pubs[:issues]],
    }
    if not pubs:
        out["note"] = "no publications: this organization does not publish a bulletin here now"
    elif latest < (dt.date.today() - dt.timedelta(days=45)).isoformat():
        out["note"] = f"newest issue is {latest}: publishing here has stopped"
    return out


# ── Evidence recheck ────────────────────────────────────────────────────────
_QUOTE_CHARS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-",
                              " ": " "})


def _squash(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(_QUOTE_CHARS).lower()
    text = " ".join(re.sub(r"[^\w'\"&@:/.,-]+", " ", text).split())
    # PDF extraction spaces punctuation unpredictably ("Fr.Zach (CTK)" in one
    # tool, "Fr. Zach ( CTK )" in another), so spacing around it doesn't count.
    return re.sub(r" ?([&@:/.,-]) ?", r"\1", text)


def quote_found(quote: str, text: str) -> bool:
    """Whether every part of `quote` (split at … or ...) appears in `text`, in order."""
    haystack = _squash(text)
    pos = 0
    for part in re.split(r"…|\.\.\.|\[\.\.\.\]", quote):
        part = _squash(part).strip(" .,")
        if not part:
            continue
        at = haystack.find(part, pos)
        if at < 0:
            return False
        pos = at + len(part)
    return True


# A Discover Mass church page lists its recent issues behind download links
# whose token changes on every load, so evidence cites the church page and
# quotes an issue; recheck reads the listed issues along with the page.
DISCOVER_MASS_CHURCH_RE = re.compile(r"discovermass\.com/church/[a-z0-9-]+/?$")
_DISCOVER_MASS_ISSUE_RE = re.compile(
    r"href='(https://bulletins\.discovermass\.com/download\.php\?bulletin=[^']+)'")


def _discover_mass_issue_texts(page: str) -> str:
    texts = []
    for link in dict.fromkeys(_DISCOVER_MASS_ISSUE_RE.findall(page)):
        resp = fetch(html.unescape(link))
        if resp.ok and _is_pdf(resp) and not resp.truncated:
            try:
                texts.append("\n\n".join(pdf_pages(resp.body)))
            except Exception:  # noqa: BLE001 - an unreadable issue just isn't searched
                continue
    return "\n\n".join(texts)


def recheck_evidence(items: list[tuple[str, dict[str, Any]]], workers: int = 6
                     ) -> list[dict[str, Any]]:
    """Fetch each evidence URL once and look for its recorded quote.

    `items` pairs a record label with one evidence item. Bulletin PDFs at dated
    URLs do not change, so a missing quote there is a real problem; a parish
    homepage changing is normal, and a missing quote there means "go and look
    again", not "the record is wrong".
    """
    urls = sorted({str(e.get("url")) for _, e in items if e.get("quote")})

    def load(url: str) -> tuple[str, str | None, str]:
        resp = fetch(url)
        if not resp.ok:
            return url, None, resp.error or f"HTTP {resp.status}"
        try:
            text = page_text(resp)
            if DISCOVER_MASS_CHURCH_RE.search(url):
                text += "\n\n" + _discover_mass_issue_texts(resp.text())
            return url, text, ""
        except Exception as e:  # noqa: BLE001 - reported per item
            return url, None, f"could not read: {e}"

    with ThreadPoolExecutor(max_workers=workers) as pool:
        pages = {url: (text, err) for url, text, err in pool.map(load, urls)}
    out = []
    for label, e in items:
        entry = {"record": label, "url": e.get("url"), "seen": e.get("seen")}
        quote = e.get("quote")
        if not quote:
            out.append({**entry, "result": "no-quote"})
            continue
        text, err = pages[str(e.get("url"))]
        if text is None:
            out.append({**entry, "result": "unreachable", "detail": err})
        elif not text.strip():
            out.append({**entry, "result": "no-text", "detail": "scanned PDF or empty page"})
        else:
            out.append({**entry, "result": "found" if quote_found(str(quote), text)
                        else "missing", "quote": quote})
    return out
