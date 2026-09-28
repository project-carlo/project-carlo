"""`probe url` with a real browser: see a parish website the way a person does.

`pnpm diocese probe url` fetches pages without a browser, so it reports
HTTP4XX for sites behind Cloudflare (every eCatholic site, many others),
NO-PARISH-WORDS for sites built in JavaScript (Wix, Squarespace, "Redirecting..."
shells), and no publications for bulletins that sit in an iframe widget or one
click deep. This opens the page in the pipeline's own stealth browser
(pdf_extract.browser.launch_stealth_browser) with real Chrome, headed under
xvfb, and reports the same fields `probe url` does, read from the rendered page
and its iframes. Run scripts/setup_browser.sh once per sandbox first.

Cloudflare decides per request whether to challenge, and in a Claude Code sandbox
the challenge can never be solved (brunhild.challenges.cloudflare.com is denied
by the egress policy), so a challenged load is simply retried with backoff.

Usage (from the repo root; re-runs itself under xvfb-run when there is no display):
  uv run python .claude/skills/parish-site-access/scripts/visit.py URL [URL ...] [options]

  --bulletin        when a page embeds no publication id, open its bulletin links
                    (up to 5) until one does, the way detect.py does; bulletin PDFs
                    with no publisher are reported as self-hosted (url:<page>)
  --follow TEXT     after loading, follow the first link whose text or href contains
                    TEXT (case-insensitive); repeat to walk deeper (single URL only)
  --text            include the visible text of the final page (--chars N, default 4000)
  --links           include the final page's links as [text, href] (--match REGEX filters)
  --screenshot PATH full-page screenshot of the final page (look at it with Read);
                    with several URLs, -0, -1, ... is added to the name
  --html PATH       save the final page's HTML, iframes included (numbered like --screenshot)
  --retries N       loads per navigation while Cloudflare challenges (default 8)

Prints JSON: {"results": [{url, verdict, status, final_url, title, loads,
publications, bulletin_links, pdf_links, ...}]}, describing the site's own page.
verdict is one of probe url's (ok, SPAM-SQUAT, REDIRECT-OFFSITE, HTTP4XX, HTTP5XX,
NO-PARISH-WORDS) judged on the rendered page, or BLOCKED (Cloudflare challenged
every load: wait a minute and retry) or ERROR (the browser could not load it,
which includes domains that don't resolve: probe url tells DEAD-DNS apart).
With --follow, the page it ends on is described under "followed", and --text,
--links, --screenshot and --html read that page.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urljoin

REPO = Path(__file__).resolve().parents[4]
CF_TITLE = "just a moment"
# SiteGround's "Robot Challenge Screen" (/.well-known/sgcaptcha/) clears by itself
# after 5-10 s in a headed browser, then goes back to the page.
SG_TITLE = "robot challenge"
SG_PATH = "/.well-known/sgcaptcha"
# How long one load waits for a passive challenge to clear before reloading.
CF_SETTLE_MS = 5000
SG_SETTLE_MS = 20000
# Pause before each reload. Challenged loads come in streaks lasting tens of
# seconds, so back off instead of hammering: 2s, 4s, 8s, then 15s.
RETRY_PAUSES_MS = (2000, 4000, 8000, 15000)
BULLETIN_PAGES_TO_TRY = 5


def _reexec_under_xvfb() -> None:
    headless = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes", "on"}
    if os.getenv("DISPLAY") or headless or not shutil.which("xvfb-run"):
        return
    # xvfb-run -a probes upward from display 99, so runs started together (parallel agents)
    # race for the same display. Start each run's search at a random number instead.
    os.execvp(
        "xvfb-run",
        ["xvfb-run", "-a", "-n", str(random.randint(100, 60000)), "-s", "-screen 0 1366x900x24",
         sys.executable, *sys.argv],
    )


def _challenged(page) -> bool:  # type: ignore[no-untyped-def]
    try:
        title = (page.title() or "").lower()
        return CF_TITLE in title or SG_TITLE in title or SG_PATH in (page.url or "")
    except Exception:  # title() during a navigation
        return True


def _settle_ms(page) -> int:  # type: ignore[no-untyped-def]
    try:
        return SG_SETTLE_MS if SG_PATH in (page.url or "") else CF_SETTLE_MS
    except Exception:
        return CF_SETTLE_MS


def goto(page, url: str, retries: int) -> tuple[int | None, int]:  # type: ignore[no-untyped-def]
    """Load url, reloading while Cloudflare (or SiteGround) challenges. Returns (status, loads)."""
    status = None
    for attempt in range(1, retries + 1):
        status = None  # a challenged attempt's 403 must not describe a later load
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
            status = resp.status if resp else None
        except Exception as exc:
            # A site's own JavaScript redirect (http -> https, "Redirecting...")
            # interrupts the navigation; the page it went to is the answer.
            if "interrupted by another navigation" not in str(exc):
                raise
            page.wait_for_load_state("domcontentloaded", timeout=30000)
        waited = 0
        while _challenged(page) and waited < _settle_ms(page):
            page.wait_for_timeout(500)
            waited += 500
        if not _challenged(page):
            # let client-rendered content (Wix, ParishesOnline widgets) populate
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            return status, attempt
        if attempt < retries:
            page.wait_for_timeout(RETRY_PAUSES_MS[min(attempt, len(RETRY_PAUSES_MS)) - 1])
    return status, retries


def _frames(page):  # type: ignore[no-untyped-def]
    return [page.main_frame] + [
        f for f in page.frames if f != page.main_frame and not f.is_detached()
    ]


def _html(page) -> str:  # type: ignore[no-untyped-def]
    """The page's HTML followed by each iframe's, plus each iframe's own URL."""
    parts = []
    for frame in _frames(page):
        try:
            parts.append(f"<!-- frame {frame.url} -->\n{frame.content()}")
        except Exception:
            continue
    return "\n".join(parts)


def _links(page) -> list[tuple[str, str]]:  # type: ignore[no-untyped-def]
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for frame in _frames(page):
        try:
            anchors = frame.eval_on_selector_all(
                "a[href]",
                "els => els.map(a => [(a.innerText || a.title || '').trim(), a.href])",
            )
        except Exception:
            continue
        for text, href in anchors:
            href = urljoin(frame.url, href)
            if href in seen or href.startswith(("javascript:", "mailto:", "tel:")):
                continue
            seen.add(href)
            out.append((" ".join(text.split())[:80], href))
    return out


def _text(page) -> str:  # type: ignore[no-untyped-def]
    parts = []
    for frame in _frames(page):
        try:
            parts.append(frame.inner_text("body"))
        except Exception:
            continue
    return "\n".join(parts)


def _is_pdf(url: str) -> bool:
    return url.lower().split("?")[0].endswith(".pdf")


def _observe(page, web) -> dict:  # type: ignore[no-untyped-def]
    publications: list[str] = []
    bulletin_links: list[str] = []
    for frame in _frames(page):
        try:
            html = frame.content()
        except Exception:
            continue
        publications += [p for p in web.find_publications(html) if p not in publications]
        # each frame's relative links resolve against that frame, not the page
        bulletin_links += [
            u for u in web.bulletin_links(html, frame.url) if u not in bulletin_links
        ]
    return {
        "publications": publications,
        "bulletin_links": bulletin_links[:15],
        # bulletin_links stops at 15, and WordPress pages spend that on feeds and
        # embeds before reaching the PDF, so list PDFs on their own.
        "pdf_links": [h for _, h in _links(page) if _is_pdf(h)][:15],
    }


def _verdict(url: str, status: int | None, page, web) -> str:  # type: ignore[no-untyped-def]
    """probe url's verdicts, judged on the rendered HTML instead of the raw HTML."""
    html = _html(page).lower()
    status = status or 0
    if web.looks_squatted(html):
        return "SPAM-SQUAT"
    if web._registrable(web._host(page.url)) != web._registrable(web._host(url)):
        return "REDIRECT-OFFSITE"
    if status >= 500:
        return "HTTP5XX"
    if status >= 400:
        return "HTTP4XX"
    if not any(w in html for w in web.PARISH_WORDS):
        return "NO-PARISH-WORDS"
    return "ok"


def _self_hosted(page_url: str, pdfs: list[str], pdfs_on: str) -> dict:
    return {
        "page": page_url,
        "publications": [f"url:{page_url}"],
        "pdfs_on": pdfs_on,
        "pdf_links": pdfs,
        "note": "bulletin PDFs but no publisher id: looks self-hosted",
    }


def _bulletin_search(page, web, home: dict, retries: int) -> dict:  # type: ignore[no-untyped-def]
    """Open the home page's bulletin links until one embeds a publication id.

    Returns what was found (`found`) and every page tried. Bulletin PDFs with no
    publisher id are a self-hosted bulletin, recorded as url:<the page listing
    them>: the bulletin page that links to the page holding the PDFs (a WordPress
    index linking one post per issue), else the page holding them.
    """
    home_url = page.url
    pages = [u for u in home["bulletin_links"] if not _is_pdf(u)]
    tried, self_hosted = [], None
    hrefs_by_page: dict[str, set[str]] = {}
    for link in pages[:BULLETIN_PAGES_TO_TRY]:
        try:
            status, loads = goto(page, link, retries)
            seen = _observe(page, web)
            hrefs = {h for _, h in _links(page)}
        except Exception as exc:
            tried.append({"url": link, "error": f"{type(exc).__name__}: {exc}".splitlines()[0]})
            continue
        blocked = _challenged(page)
        tried.append(
            {
                "url": link,
                "final_url": page.url,
                "status": status,
                "loads": loads,
                "blocked": blocked,
                **seen,
            }
        )
        if blocked:
            continue
        hrefs_by_page[page.url] = hrefs
        if seen["publications"]:
            return {
                "found": {"page": page.url, "publications": seen["publications"]},
                "tried": tried,
            }
        if seen["pdf_links"] and self_hosted is None:
            listing = next(
                (p for p, links in hrefs_by_page.items() if p != page.url and link in links),
                page.url,
            )
            self_hosted = _self_hosted(listing, seen["pdf_links"], page.url)
    if self_hosted is None:
        # Bulletin PDFs linked straight from the home page.
        pdfs = [u for u in home["bulletin_links"] if _is_pdf(u)]
        if pdfs:
            self_hosted = _self_hosted(home_url, pdfs, home_url)
    return {"found": self_hosted, "tried": tried}


def _numbered(path: Path, index: int, many: bool) -> Path:
    return path.with_name(f"{path.stem}-{index}{path.suffix}") if many else path


def visit(page, web, url: str, index: int, args) -> dict:  # type: ignore[no-untyped-def]
    out: dict = {"url": url}
    try:
        status, loads = goto(page, url, args.retries)
        out.update(status=status, final_url=page.url, title=page.title(), loads=loads)
        if _challenged(page):
            return {
                **out,
                "verdict": "BLOCKED",
                "detail": "Cloudflare challenged every load; wait a minute or two and retry",
            }
        out["verdict"] = _verdict(url, status, page, web)
        if out["verdict"] != "ok":
            out["detail"] = web.VERDICT_NOTES.get(out["verdict"], "")
        out.update(_observe(page, web))
        home = dict(out)

        target = out
        for needle in args.follow:
            match = next(
                (
                    h
                    for t, h in _links(page)
                    if needle.lower() in t.lower() or needle.lower() in h.lower()
                ),
                None,
            )
            if match is None:
                out["follow_error"] = f"no link matching {needle!r} on {page.url}"
                break
            status, more = goto(page, match, args.retries)
            target = out["followed"] = {
                "url": match,
                "status": status,
                "final_url": page.url,
                "title": page.title(),
                "loads": more,
            }
            if _challenged(page):
                target["blocked"] = True
                break
            target.update(_observe(page, web))

        if args.text:
            target["text"] = _text(page)[: args.chars]
        if args.links:
            pattern = re.compile(args.match, re.IGNORECASE) if args.match else None
            target["links"] = [
                [t, h]
                for t, h in _links(page)
                if pattern is None or pattern.search(t) or pattern.search(h)
            ]
        many = len(args.urls) > 1
        if args.screenshot:
            path = _numbered(args.screenshot, index, many)
            path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(path), full_page=True)
            target["screenshot"] = str(path)
        if args.html:
            path = _numbered(args.html, index, many)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(_html(page), encoding="utf-8")
            target["html"] = str(path)
        if args.bulletin and not args.follow and not out["publications"] and out["bulletin_links"]:
            out["bulletin_search"] = _bulletin_search(page, web, home, args.retries)
    except Exception as exc:
        # Keep what was learnt before the failure; one bad site must not lose the batch.
        out.setdefault("verdict", "ERROR")
        out["error"] = f"{type(exc).__name__}: {exc}".splitlines()[0]
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--bulletin", action="store_true")
    parser.add_argument("--follow", action="append", default=[])
    parser.add_argument("--text", action="store_true")
    parser.add_argument("--chars", type=int, default=4000)
    parser.add_argument("--links", action="store_true")
    parser.add_argument("--match", help="regex: only links whose text or href matches")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--retries", type=int, default=8)
    args = parser.parse_args()
    if args.follow and len(args.urls) > 1:
        parser.error("--follow takes a single URL")
    if args.follow and args.bulletin:
        parser.error("--bulletin searches from the site's own page; drop --follow")
    args.retries = max(1, args.retries)

    sys.path.insert(0, str(REPO / "src"))
    from pdf_extract.browser import launch_stealth_browser
    from pdf_extract.dioceses import web

    channel = os.getenv("PLAYWRIGHT_BROWSER_CHANNEL") or (
        "chrome" if shutil.which("google-chrome") else None
    )
    results = []
    with launch_stealth_browser(channel=channel) as first_page:
        context = first_page.context
        for index, url in enumerate(args.urls):
            if not re.match(r"https?://", url):
                url = f"https://{url}"
            # A fresh tab per site: a failed navigation can leave the old one
            # mid-load, and it would interrupt the next site's.
            page = context.new_page()
            try:
                results.append(visit(page, web, url, index, args))
            finally:
                page.close()
    print(json.dumps({"results": results}, indent=2, ensure_ascii=False))
    return 2 if any(r["verdict"] in {"BLOCKED", "ERROR"} for r in results) else 0


if __name__ == "__main__":
    _reexec_under_xvfb()
    sys.exit(main())
