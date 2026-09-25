"""Open a parish website in the pipeline's browser and show what it sees.

Uses pdf_extract.browser.launch_stealth_browser (stealth-patched, headed) with
real Chrome, the same setup detect.py uses, so what you see here is what the
pipeline sees. Run scripts/setup_browser.sh once per sandbox first.

Cloudflare decides per request whether to challenge, and in this sandbox the
challenge can never be solved (its brunhild.challenges.cloudflare.com endpoint
is denied by the egress policy). So every navigation that lands on
"Just a moment..." is simply loaded again, up to --retries times.

Usage (from the repo root; re-runs itself under xvfb-run when there is no display):
  uv run python .claude/skills/parish-site-access/scripts/visit.py TARGET [options]

TARGET is a URL or a slug from data/parishes.csv (its website is opened).
  --follow TEXT     then follow the first link whose text or href contains TEXT
                    (case-insensitive); repeat to walk several pages deep
  --text [N]        print the page's visible text (first N chars, default 4000)
  --links [PATTERN] print links (text -> href), optionally only those matching PATTERN
  --frames          include iframe content in --text/--links/--html (parishesonline widgets)
  --screenshot PATH save a full-page screenshot of the final page (view it with Read)
  --html PATH       save the final page's HTML (plus frames with --frames)
  --retries N       loads per navigation while Cloudflare challenges (default 8)
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

REPO = Path(__file__).resolve().parents[4]
CF_TITLE = "just a moment"
# How long one load waits for a passive challenge to clear before reloading.
CF_SETTLE_MS = 5000
# Pause before each reload. Challenged loads come in streaks lasting tens of
# seconds, so back off instead of hammering: 2s, 4s, 8s, then 15s.
RETRY_PAUSES_MS = (2000, 4000, 8000, 15000)


def _reexec_under_xvfb() -> None:
    headless = os.getenv("PLAYWRIGHT_HEADLESS", "").lower() in {"1", "true", "yes", "on"}
    if os.getenv("DISPLAY") or headless or not shutil.which("xvfb-run"):
        return
    os.execvp(
        "xvfb-run",
        ["xvfb-run", "-a", "-s", "-screen 0 1366x900x24", sys.executable, *sys.argv],
    )


def _resolve_target(target: str) -> str:
    if re.match(r"https?://", target):
        return target
    with (REPO / "data" / "parishes.csv").open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["slug"] == target:
                return row["website"]
    sys.exit(f"{target!r} is neither a URL nor a slug in data/parishes.csv")


def _challenged(page) -> bool:  # type: ignore[no-untyped-def]
    try:
        return CF_TITLE in (page.title() or "").lower()
    except Exception:  # title() during a navigation
        return True


def goto_past_cloudflare(page, url: str, retries: int) -> tuple[int | None, int]:  # type: ignore[no-untyped-def]
    """Load url, reloading while Cloudflare challenges. Returns (status, attempts)."""
    status = None
    for attempt in range(1, retries + 1):
        resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
        status = resp.status if resp else None
        waited = 0
        while _challenged(page) and waited < CF_SETTLE_MS:
            page.wait_for_timeout(500)
            waited += 500
        if not _challenged(page):
            # let client-rendered content (parishesonline, Wix) populate
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            return status, attempt
        if attempt < retries:
            page.wait_for_timeout(RETRY_PAUSES_MS[min(attempt, len(RETRY_PAUSES_MS)) - 1])
    return status, retries


def _frames(page, include: bool):  # type: ignore[no-untyped-def]
    frames = [page.main_frame]
    if include:
        frames += [f for f in page.frames if f != page.main_frame and not f.is_detached()]
    return frames


def _links(page, include_frames: bool) -> list[tuple[str, str]]:  # type: ignore[no-untyped-def]
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for frame in _frames(page, include_frames):
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


def _text(page, include_frames: bool) -> str:  # type: ignore[no-untyped-def]
    parts = []
    for frame in _frames(page, include_frames):
        try:
            parts.append(frame.inner_text("body"))
        except Exception:
            continue
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("target")
    parser.add_argument("--follow", action="append", default=[])
    parser.add_argument("--text", nargs="?", type=int, const=4000)
    parser.add_argument("--links", nargs="?", const="")
    parser.add_argument("--frames", action="store_true")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--html", type=Path)
    parser.add_argument("--retries", type=int, default=8)
    args = parser.parse_args()

    sys.path.insert(0, str(REPO / "src"))
    from pdf_extract.browser import launch_stealth_browser

    url = _resolve_target(args.target)
    channel = os.getenv("PLAYWRIGHT_BROWSER_CHANNEL") or (
        "chrome" if shutil.which("google-chrome") else None
    )
    with launch_stealth_browser(channel=channel) as page:
        steps = [url, *args.follow]
        for i, step in enumerate(steps):
            if i > 0:
                needle = step.lower()
                match = next(
                    (
                        href
                        for text, href in _links(page, args.frames)
                        if needle in text.lower() or needle in href.lower()
                    ),
                    None,
                )
                if match is None:
                    print(f"FOLLOW  no link matching {step!r} on {page.url}")
                    return 1
                url = match
            started = time.time()
            status, attempts = goto_past_cloudflare(page, url, args.retries)
            state = "BLOCKED" if _challenged(page) else "OK"
            print(
                f"{state:7} {status} {page.url}\n        title={page.title()!r} "
                f"loads={attempts} {time.time() - started:.1f}s"
            )
            if state == "BLOCKED":
                print(
                    "        Cloudflare challenged every load; retry later or with more "
                    "--retries (see SKILL.md)"
                )
                return 2

        if args.text is not None:
            print("\n--- text ---")
            print(_text(page, args.frames)[: args.text])
        if args.links is not None:
            pattern = re.compile(args.links, re.IGNORECASE) if args.links else None
            links = [
                (t, h)
                for t, h in _links(page, args.frames)
                if pattern is None or pattern.search(t) or pattern.search(h)
            ]
            print(f"\n--- links ({len(links)}) ---")
            for text, href in links:
                print(f"{text or '(no text)'} -> {href}")
        if args.screenshot:
            args.screenshot.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(args.screenshot), full_page=True)
            print(f"\nscreenshot: {args.screenshot}")
        if args.html:
            args.html.parent.mkdir(parents=True, exist_ok=True)
            html = [page.content()]
            if args.frames:
                html += [f.content() for f in _frames(page, True)[1:]]
            args.html.write_text("\n".join(html), encoding="utf-8")
            print(f"html: {args.html}")
    return 0


if __name__ == "__main__":
    _reexec_under_xvfb()
    sys.exit(main())
