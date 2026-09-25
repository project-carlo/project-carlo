"""Open parish pages in the pipeline's stealth Chromium and report what loaded.

Mirrors src/pdf_extract/browser.py (playwright-stealth, headed by default) and
adds the two fixes a Claude Code cloud sandbox needs before Chromium can load
anything:

  * executable_path: the venv's Playwright wants a newer Chromium build than
    the one preinstalled under /opt/pw-browsers, and `playwright install`
    is blocked by the egress policy.
  * --ignore-certificate-errors-spki-list: trusts exactly the agent proxy's CA
    (read from /root/.ccr/agent-proxy-ca.crt), which re-terminates TLS. TLS is
    still verified for everything else.

Run headed under xvfb (headed gets past more Cloudflare checks than headless):
  xvfb-run -a uv run python .claude/skills/parish-site-access/scripts/probe_browser.py URL [URL ...]
Options: --headless, --screenshot DIR, --wait SECONDS (default 6).
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

PROXY_CA = Path("/root/.ccr/agent-proxy-ca.crt")
SANDBOX_CHROMIUM = Path("/opt/pw-browsers/chromium")
LINK_SELECTOR = (
    "a[href$='.pdf'], a[href*='.pdf?'], a[href*='files.ecatholic.com'], "
    "a[href*='selectedPublication='], a[href*='download.php?bulletin=']"
)


def _proxy_ca_spki() -> str | None:
    """Base64 SHA-256 of the proxy CA's public key, the form Chromium's flag wants."""
    if not PROXY_CA.exists():
        return None
    pubkey = subprocess.run(
        ["openssl", "x509", "-in", str(PROXY_CA), "-pubkey", "-noout"],
        check=True,
        capture_output=True,
    ).stdout
    der = subprocess.run(
        ["openssl", "pkey", "-pubin", "-outform", "der"],
        input=pubkey,
        check=True,
        capture_output=True,
    ).stdout
    return base64.b64encode(hashlib.sha256(der).digest()).decode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--screenshot", type=Path)
    parser.add_argument("--wait", type=float, default=6.0)
    args = parser.parse_args()

    launch: dict[str, object] = {"headless": args.headless, "args": []}
    if SANDBOX_CHROMIUM.exists():
        launch["executable_path"] = str(SANDBOX_CHROMIUM)
    if spki := _proxy_ca_spki():
        launch["args"] = [f"--ignore-certificate-errors-spki-list={spki}"]
    if args.screenshot:
        args.screenshot.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(**launch)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        Stealth().apply_stealth_sync(context)
        page = context.new_page()
        for i, url in enumerate(args.urls):
            try:
                resp = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                # A passive Cloudflare check swaps the title once it clears; an
                # interactive one ("Verify you are human") never does here.
                deadline = args.wait * 1000
                while deadline > 0 and "just a moment" in page.title().lower():
                    page.wait_for_timeout(1000)
                    deadline -= 1000
                page.wait_for_timeout(max(deadline, 2000))
                title = page.title()
                links = [a.get_attribute("href") for a in page.query_selector_all(LINK_SELECTOR)]
                blocked = "just a moment" in title.lower()
                print(
                    f"{'BLOCKED' if blocked else 'OK':7} {resp.status if resp else '-'} "
                    f"{url}  title={title[:60]!r}  bulletin_links={len(links)}"
                )
                for href in links[:5]:
                    print(f"          {href}")
                if args.screenshot:
                    page.screenshot(path=str(args.screenshot / f"{i:02d}.png"))
            except Exception as exc:
                print(f"ERROR   {url}  {type(exc).__name__}: {str(exc).splitlines()[0]}")
        browser.close()


if __name__ == "__main__":
    os.environ.setdefault("PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD", "1")
    main()
