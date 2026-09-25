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
                    (up to 5) until one does, the way detect.py does; a bulletin page
                    with PDFs and no publisher is reported as self-hosted (url:<page>)
  --follow TEXT     after loading, follow the first link whose text or href contains
                    TEXT (case-insensitive); repeat to walk deeper (single URL only)
  --text [N]        include the page's visible text (first N chars, default 4000)
  --links [REGEX]   include every link (text, href), optionally only those matching
  --screenshot PATH full-page screenshot of the final page (look at it with Read)
  --html PATH       save the final page's HTML, iframes included
  --retries N       loads per navigation while Cloudflare challenges (default 8)

Prints JSON: {"results": [{url, verdict, status, final_url, title, loads,
publications, bulletin_links, pdf_links, ...}]}. verdict is one of probe url's
(ok, SPAM-SQUAT, REDIRECT-OFFSITE, HTTP4XX, HTTP5XX, NO-PARISH-WORDS) judged on the
rendered page, or BLOCKED (Cloudflare challenged every load: wait a minute and
retry) or ERROR (the browser could not load it at all).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import urljoin

REPO = Path(__file__).resolve().parents[4]
CF_TITLE = "just a moment"
# How long one load waits for a passive challenge to clear before reloading.
CF_SETTLE_MS = 5000
# Pause before each reload. Challenged loads come in streaks lasting tens of
# seconds, so back off instead of hammering: 2s, 4s, 8s, then 15s.
RETRY_PAUSES_MS = (2000, 4000, 8000, 15000)
BULLETIN_PAGES_TO_TRY = 5


def _reexec_under_xvfb() -> None:
    headless = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes", "on"}
    if os.getenv("DISPLAY") or headless or not shutil.which("xvfb-run"):
        return
    os.execvp(
        "xvfb-run",
        ["xvfb-run", "-a", "-s", "-screen 0 1366x900x24", sys.executable, *sys.argv],
    )


def _challenged(page) -> bool:  # type: ignore[no-untyped-def]
    try:
        return CF_TITLE in (page.title() or "").lower()
    except Exception:  # title() during a navigation
        return True


def goto(page, url: str, retries: int) -> tuple[int | None, int]:  # type: ignore[no-untyped-def]
    """Load url, reloading while Cloudflare challenges. Returns (status, loads)."""
    status = None
    for attempt in range(1, retries + 1):
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
        while _challenged(page) and waited < CF_SETTLE_MS:
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


def _observe(page, web) -> dict:  # type: ignore[no-untyped-def]
    html = _html(page)
    publications = web.find_publications(html)
    return {
        "publications": publications,
        "bulletin_links": web.bulletin_links(html, page.url),
        # bulletin_links stops at 15, and WordPress pages spend that on feeds and
        # embeds before reaching the PDF, so list PDFs on their own.
        "pdf_links": [h for _, h in _links(page) if h.lower().split("?")[0].endswith(".pdf")][:15],
    }


def _verdict(out: dict, page, web) -> str:  # type: ignore[no-untyped-def]
    """probe url's verdicts, judged on the rendered page instead of the raw HTML."""
    html = _html(page).lower()
    status = out.get("status") or 0
    if any(t in html for t in web.SPAM_TERMS):
        return "SPAM-SQUAT"
    if web._registrable(web._host(page.url)) != web._registrable(web._host(out["url"])):
        return "REDIRECT-OFFSITE"
    if status >= 500:
        return "HTTP5XX"
    if status >= 400:
        return "HTTP4XX"
    if not any(w in _text(page).lower() for w in web.PARISH_WORDS):
        return "NO-PARISH-WORDS"
    return "ok"


def _bulletin_search(page, web, links: list[str], retries: int) -> dict:  # type: ignore[no-untyped-def]
    """Open the page's bulletin links until one embeds a publication id.

    Returns what was found (`found`) and every page tried. A bulletin page with
    PDFs but no publisher id is a self-hosted bulletin: record it as url:<page>.
    """
    pages = [u for u in links if not u.lower().split("?")[0].endswith(".pdf")]
    tried, self_hosted, listing = [], None, None
    for link in pages[:BULLETIN_PAGES_TO_TRY]:
        try:
            status, loads = goto(page, link, retries)
            seen = _observe(page, web)
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
        # The first bulletin page that loads is where issues are listed; a later
        # one may be a single issue's post (WordPress) holding the PDF.
        listing = listing or page.url
        if seen["publications"]:
            return {
                "found": {"page": page.url, "publications": seen["publications"]},
                "tried": tried,
            }
        if seen["pdf_links"] and self_hosted is None:
            self_hosted = {
                "page": listing,
                "publications": [f"url:{listing}"],
                "pdfs_on": page.url,
                "pdf_links": seen["pdf_links"],
                "note": "PDFs but no publisher id: looks self-hosted",
            }
    return {"found": self_hosted, "tried": tried}


def visit(page, web, url: str, args) -> dict:  # type: ignore[no-untyped-def]
    out: dict = {"url": url}
    try:
        status, loads = goto(page, url, args.retries)
        for needle in args.follow:
            if _challenged(page):
                break
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
            loads += more
    except Exception as exc:
        return {**out, "verdict": "ERROR", "error": f"{type(exc).__name__}: {exc}".splitlines()[0]}

    out.update(status=status, final_url=page.url, title=page.title(), loads=loads)
    if _challenged(page):
        return {
            **out,
            "verdict": "BLOCKED",
            "detail": "Cloudflare challenged every load; wait a minute or two and retry",
        }
    out["verdict"] = _verdict(out, page, web)
    if out["verdict"] != "ok":
        out["detail"] = web.VERDICT_NOTES.get(out["verdict"], "")
    out.update(_observe(page, web))

    if args.text is not None:
        out["text"] = _text(page)[: args.text]
    if args.links is not None:
        pattern = re.compile(args.links, re.IGNORECASE) if args.links else None
        out["links"] = [
            [t, h]
            for t, h in _links(page)
            if pattern is None or pattern.search(t) or pattern.search(h)
        ]
    if args.screenshot:
        path = args.screenshot
        if len(args.urls) > 1:
            path = path.with_name(f"{path.stem}-{len(args.done)}{path.suffix}")
        path.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(path), full_page=True)
        out["screenshot"] = str(path)
    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(_html(page), encoding="utf-8")
        out["html"] = str(args.html)
    if args.bulletin and not out["publications"] and out["bulletin_links"]:
        out["bulletin_search"] = _bulletin_search(page, web, out["bulletin_links"], args.retries)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--bulletin", action="store_true")
    parser.add_argument("--follow", action="append", default=[])
    parser.add_argument("--text", nargs="?", type=int, const=4000)
    parser.add_argument("--links", nargs="?", const="")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--retries", type=int, default=8)
    args = parser.parse_args()
    if args.follow and len(args.urls) > 1:
        parser.error("--follow takes a single URL")

    sys.path.insert(0, str(REPO / "src"))
    from pdf_extract.browser import launch_stealth_browser
    from pdf_extract.dioceses import web

    channel = os.getenv("PLAYWRIGHT_BROWSER_CHANNEL") or (
        "chrome" if shutil.which("google-chrome") else None
    )
    args.done = []
    with launch_stealth_browser(channel=channel) as first_page:
        context = first_page.context
        for url in args.urls:
            if not re.match(r"https?://", url):
                url = f"https://{url}"
            # A fresh tab per site: a failed navigation can leave the old one
            # mid-load, and it would interrupt the next site's.
            page = context.new_page()
            args.done.append(visit(page, web, url, args))
            page.close()
    print(json.dumps({"results": args.done}, indent=2, ensure_ascii=False))
    return 2 if any(r["verdict"] in {"BLOCKED", "ERROR"} for r in args.done) else 0


if __name__ == "__main__":
    _reexec_under_xvfb()
    sys.exit(main())
