"""Probe whether this machine can reach and navigate the parish bulletin sites.

For every parish website in data/parishes.csv, plus the provider hosts the
fetch stage downloads from, report one of:

  ok              page loaded; `bulletin_links` counts anchors mentioning "bulletin"
  egress-blocked  the Claude Code cloud proxy refused the host (session network
                  policy), so no client can reach it from here
  bot-challenge   the site answered with a Cloudflare / WAF challenge page
  http-<code>     the site itself answered with an error status
  error           anything else (DNS, timeout, TLS); the detail column says which

Run from the repo root:

    uv run python .claude/skills/parish-site-access/probe.py [--slug SLUG ...] [--http-only]

The browser is launched the way pdf_extract.browser launches it (stealth
patches, headed unless PLAYWRIGHT_HEADLESS=1), plus the two adjustments a
Claude Code cloud container needs: the pre-installed Chromium when the
bundled one is missing, and trust for the agent proxy's CA.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import os
import ssl
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[3]
PARISHES_CSV = REPO_ROOT / "data" / "parishes.csv"
PROXY_CA = Path("/root/.ccr/agent-proxy-ca.crt")
PREINSTALLED_CHROMIUM = Path("/opt/pw-browsers/chromium")

# Hosts the fetch stage talks to besides the parish websites themselves.
PROVIDER_URLS = [
    "https://parishesonline.com/",
    "https://container.parishesonline.com/",
    "https://files.ecatholic.com/",
    "https://discovermass.com/",
    "https://bulletins.discovermass.com/",
    "https://drive.google.com/",
]

# Same UA as pdf_extract.fetch._http_get_bytes.
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
CHALLENGE_TITLES = ("just a moment", "attention required", "access denied", "security check")
NAV_TIMEOUT_MS = 25_000


def _targets(slugs: set[str]) -> list[tuple[str, str]]:
    with PARISHES_CSV.open(newline="", encoding="utf-8") as f:
        rows = [(r["slug"], r["website"]) for r in csv.DictReader(f)]
    if slugs:
        return [r for r in rows if r[0] in slugs]
    return rows + [(f"provider:{u.split('/')[2]}", u) for u in PROVIDER_URLS]


def _proxy_spki_hash() -> str | None:
    """SHA-256 of the proxy CA's public key, for Chromium's SPKI allowlist.

    Chromium does not read the system trust store the proxy CA was added to,
    so every TLS page fails with ERR_CERT_AUTHORITY_INVALID. Trusting this one
    key keeps verification on for everything else.
    """
    if not PROXY_CA.exists():
        return None
    pubkey = subprocess.run(
        ["openssl", "x509", "-in", str(PROXY_CA), "-pubkey", "-noout"],
        check=True, capture_output=True,
    ).stdout
    der = subprocess.run(
        ["openssl", "pkey", "-pubin", "-outform", "der"],
        input=pubkey, check=True, capture_output=True,
    ).stdout
    return base64.b64encode(hashlib.sha256(der).digest()).decode()


def _classify_error(text: str) -> str:
    lowered = text.lower()
    if "tunnel connection failed: 403" in lowered or "err_tunnel_connection_failed" in lowered:
        return "egress-blocked"
    return "error"


def _ssl_context() -> ssl.SSLContext:
    """Default verification, minus Python 3.13's VERIFY_X509_STRICT.

    The agent proxy's CA has no keyUsage extension, which strict mode rejects
    ("CA cert does not include key usage extension"). The chain is still
    verified against the system store.
    """
    ctx = ssl.create_default_context()
    if PROXY_CA.exists():
        ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return ctx


def probe_http(url: str) -> tuple[str, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    try:
        with urlopen(req, timeout=20, context=_ssl_context()) as resp:
            body = resp.read(200_000).decode("utf-8", "replace").lower()
            if any(t in body for t in CHALLENGE_TITLES) and "cf-" in body:
                return "bot-challenge", f"{resp.status}, challenge markup"
            return "ok", str(resp.status)
    except HTTPError as exc:
        server = exc.headers.get("server", "")
        if exc.code in (403, 503) and "cloudflare" in server.lower():
            return "bot-challenge", f"{exc.code} from {server}"
        return f"http-{exc.code}", server
    except (URLError, OSError) as exc:
        detail = str(getattr(exc, "reason", exc))
        return _classify_error(detail), detail[:90]


def probe_browser(targets: list[tuple[str, str]]) -> dict[str, tuple[str, str]]:
    from playwright.sync_api import sync_playwright
    from playwright_stealth import Stealth

    headless = os.getenv("PLAYWRIGHT_HEADLESS", "0").lower() in {"1", "true", "yes", "on"}
    if not headless and not os.getenv("DISPLAY"):
        headless = True  # no X server; wrap in `xvfb-run -a` to test headed mode
    launch: dict[str, object] = {"headless": headless, "args": []}
    if channel := os.getenv("PLAYWRIGHT_BROWSER_CHANNEL"):
        launch["channel"] = channel
    spki = _proxy_spki_hash()
    if spki:
        launch["args"].append(f"--ignore-certificate-errors-spki-list={spki}")

    results: dict[str, tuple[str, str]] = {}
    with sync_playwright() as pw:
        if "channel" not in launch and not Path(pw.chromium.executable_path).exists():
            # The Python playwright pin can be newer than the browsers baked into
            # the cloud image; the image's Chromium drives fine with it.
            launch["executable_path"] = str(PREINSTALLED_CHROMIUM)
        browser = pw.chromium.launch(**launch)
        context = browser.new_context()
        Stealth().apply_stealth_sync(context)
        page = context.new_page()
        for slug, url in targets:
            try:
                resp = page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT_MS)
                title = (page.title() or "").strip()
                status = resp.status if resp else 0
                if any(t in title.lower() for t in CHALLENGE_TITLES):
                    results[slug] = ("bot-challenge", f"{status} {title!r}")
                elif status >= 400:
                    results[slug] = (f"http-{status}", repr(title[:50]))
                else:
                    n = len(page.query_selector_all("a[href*='ulletin' i], a:has-text('ulletin')"))
                    results[slug] = ("ok", f"{status} bulletin_links={n} {title[:40]!r}")
            except Exception as exc:
                first = str(exc).splitlines()[0]
                results[slug] = (_classify_error(first), first[:90])
        browser.close()
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--slug", action="append", default=[], help="limit to these parish slugs")
    parser.add_argument("--http-only", action="store_true", help="skip the Playwright pass")
    args = parser.parse_args()

    targets = _targets(set(args.slug))
    http = {slug: probe_http(url) for slug, url in targets}
    browser = {} if args.http_only else probe_browser(targets)

    width = max(len(s) for s, _ in targets)
    print(f"{'slug':{width}}  {'http':15} {'browser':15} detail")
    for slug, _url in targets:
        h, hd = http[slug]
        b, bd = browser.get(slug, ("-", ""))
        print(f"{slug:{width}}  {h:15} {b:15} {bd or hd}")

    statuses = [s for s, _ in http.values()] + [s for s, _ in browser.values()]
    print("\nsummary:", {s: statuses.count(s) for s in sorted(set(statuses))})
    return 0


if __name__ == "__main__":
    sys.exit(main())
