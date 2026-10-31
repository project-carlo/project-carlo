"""`seed site`: a page of a parish's website as plain text, for a drafter to read and quote.

WebFetch hands a drafter a small model's summary of a page, not the page: it
misses what a script draws, and it once offered confession times it had worked
out itself. This returns the page's own text, so a website source's `said` can
quote it, and the links on it that look like schedules, so the drafter can open
the right page next.

A plain request comes first. When it is refused (Cloudflare's "Just a moment…"
page, an HTTP error) or comes back with almost no text (a page a script
draws), the pipeline's stealth browser (`browser.launch_stealth_browser`) loads
it instead. `PLAYWRIGHT_HEADLESS` decides whether that browser shows a window, as
everywhere else; Cloudflare passes a headed one more often.

Each page's text is kept under `data/seed-work/<parish>/site/` for a day, so
reading it again costs nothing.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

from pdf_extract.dioceses.web import fetch, html_text
from pdf_extract.parish_sites.links import registrable_domain, url_host
from pdf_extract.seeding.files import WORK_DIR
from pdf_extract.seeding.queries import SeedError

# Less text than this is a page a script draws, or a challenge page.
MIN_TEXT_CHARS = 400
CACHE_HOURS = 24
BLOCKED_MARKERS = ("just a moment", "enable javascript and cookies", "attention required",
                   "checking your browser")
SCHEDULE_WORDS = re.compile(
    r"mass|confession|reconciliation|penance|adoration|schedule|times|bulletin|"
    r"sacrament|liturg|worship|holy hour|eucharist", re.I,
)
MAX_LINKS = 25
# The browser waits for a challenge page to clear, or a script to draw, in steps
# of this long, up to this many (Cloudflare's check takes 5-15 seconds).
BROWSER_SETTLE_MS = 5000
BROWSER_SETTLE_STEPS = 5


def resolve_url(homepage: str | None, where: str | None) -> str:
    """The address `where` names: the parish's homepage by default, a path on its site,
    or a full address."""
    if where and re.match(r"https?://", where, re.I):
        return where
    if not homepage:
        raise SeedError("The parish has no website in data/parishes.csv: give a full address")
    return urljoin(homepage if homepage.endswith("/") else homepage + "/", where or "")


def _blocked(text: str) -> bool:
    head = text[:2000].lower()
    return any(marker in head for marker in BLOCKED_MARKERS)


def schedule_links(page: str, base: str) -> list[dict[str, str]]:
    """The links on `page` within its site whose address or words look like schedules."""
    domain = registrable_domain(url_host(base) or "")
    found: dict[str, dict[str, str]] = {}
    for href, label in re.findall(
        r"""<a\b[^>]*href=["']([^"'#]+)["'][^>]*>(.*?)</a>""", page, flags=re.I | re.S,
    ):
        url = urljoin(base, href.strip())
        if urlsplit(url).scheme not in ("http", "https"):
            continue
        words = " ".join(html_text(label).split())
        if not SCHEDULE_WORDS.search(f"{url} {words}"):
            continue
        if domain and registrable_domain(url_host(url) or "") != domain:
            continue
        found.setdefault(url, {"url": url, "text": words[:80]})
    return list(found.values())[:MAX_LINKS]


def _browser_html(url: str) -> tuple[str, str]:
    """The page as the stealth browser renders it, and the address it ended at: in
    Chrome, which Cloudflare passes more often, or Playwright's Chromium without it."""
    from pdf_extract.browser import goto_with_retry, launch_stealth_browser

    for channel in ("chrome", None):
        try:
            with launch_stealth_browser(channel=channel) as page:
                goto_with_retry(page=page, page_url=url)
                for _ in range(BROWSER_SETTLE_STEPS):
                    page.wait_for_timeout(BROWSER_SETTLE_MS)
                    if not _blocked(html_text(page.content())):
                        break
                return page.content(), page.url
        except Exception as exc:
            if channel is None or "is not found" not in str(exc):
                raise
    raise AssertionError("unreachable")


def read_site(
    parish_slug: str, url: str, *, browser: bool = True, fresh: bool = False,
    work_dir: Path = WORK_DIR, now: datetime | None = None,
) -> dict[str, Any]:
    """`url`'s text and schedule links: from the cache when read within a day."""
    now = now or datetime.now(UTC)
    cache = work_dir / parish_slug / "site" / (hashlib.sha256(url.encode()).hexdigest()[:16]
                                               + ".json")
    if not fresh and cache.is_file():
        kept = json.loads(cache.read_text(encoding="utf-8"))
        read_at = datetime.fromisoformat(kept["read_at"])
        if now - read_at < timedelta(hours=CACHE_HOURS):
            return {**kept, "cached": True}

    notes: list[str] = []
    resp = fetch(url)
    page, final, how = "", resp.final_url or url, "http"
    if resp.ok:
        page = resp.text()
    else:
        notes.append(f"plain request: {resp.error or resp.status}")
    text = html_text(page) if page else ""
    if browser and (not text or _blocked(text) or len(text) < MIN_TEXT_CHARS):
        if text:
            notes.append("plain request: "
                         + ("a challenge page" if _blocked(text) else f"only {len(text)} chars"))
        try:
            page, final = _browser_html(url)
            text, how = html_text(page), "browser"
        except Exception as exc:  # noqa: BLE001 - say why and keep the plain result
            first = (str(exc).splitlines() or [""])[0][:200]
            hint = (" (no display: run it under xvfb-run)"
                    if "display" in str(exc).lower() or "x server" in str(exc).lower() else "")
            notes.append(f"browser: {type(exc).__name__}: {first}{hint}")
    if not text or _blocked(text):
        raise SeedError(f"Could not read {url}: " + ("; ".join(notes) or "no text")
                        + ". Rely on the bulletins, or note the website was unreadable.")
    result = {
        "parish": parish_slug,
        "url": url,
        "final_url": final,
        "via": how,
        "read_at": now.isoformat(timespec="seconds"),
        "notes": notes,
        "links": schedule_links(page, final),
        "text": text,
    }
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return {**result, "cached": False}
