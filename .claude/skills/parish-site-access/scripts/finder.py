"""Turn an eCatholic parish-finder map into a list `roster import` takes.

Many dioceses on eCatholic publish their parish directory as a "parish finder" /
Mass-times map (for example syracusediocese.org/parishfinder). The page is
behind Cloudflare like every eCatholic site, and it is not WP Store Locator, so
`pnpm diocese roster fetch ... wpsl` can't read it. Each site on the map is an
`<li class="site" data-latitude=... data-longitude=...>` holding its name,
address, mailing address, phone and website; closed parishes stay on the map as
"<Name> (Closed)" with no address.

Usage (from the repo root):
  uv run python .claude/skills/parish-site-access/scripts/finder.py URL --out list.json
  uv run python .claude/skills/parish-site-access/scripts/finder.py --html saved.html --out list.json
  pnpm diocese roster import <d> directory list.json --title "..." --url URL --notes "..."

Each entry: id (the finder's site id), name, kind ("closed" when the name says
"(Closed)", else ""), line1, city, state, postal_code, latitude, longitude
(coordinates_from diocese-directory), website, url, address (verbatim, for the
evidence quote), phone, mailing. With URL, the page is loaded in the stealth
browser the way visit.py loads it (run setup_browser.sh first).
"""

from __future__ import annotations

import argparse
import html as htmllib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE_SPLIT = re.compile(r'<li[^>]*\bid="(\d+)"[^>]*class="site"[^>]*>')


def _field(pattern: str, chunk: str) -> str:
    m = re.search(pattern, chunk, re.S)
    if not m:
        return ""
    return " ".join(htmllib.unescape(re.sub(r"<.*?>", " ", m.group(1))).split())


def _float(pattern: str, chunk: str) -> float | None:
    m = re.search(pattern, chunk)
    try:
        return float(m.group(1)) if m else None
    except ValueError:
        return None


def parse(html: str, source_url: str) -> list[dict]:
    parts = SITE_SPLIT.split(html)
    # parts[0] is everything before the first site's <li>; after it, the id and
    # its chunk alternate. The opening tag itself is consumed by the split, so
    # the coordinates are read back from it.
    tags = SITE_SPLIT.finditer(html)
    entries = []
    for (site_id, chunk), tag in zip(zip(parts[1::2], parts[2::2]), tags):
        name = _field(r'<div class="name">(.*?)</div>', chunk)
        address = _field(r'<a class="address"[^>]*>(.*?)</a>', chunk)
        pieces = [p.strip() for p in address.split(",")]
        line1 = city = state = postal = ""
        if len(pieces) >= 4:
            line1, city, state, postal = ", ".join(pieces[:-3]), *pieces[-3:]
        elif len(pieces) == 2:
            city, state = pieces
        web = re.search(r'class="website">[^<]*<a[^>]*href="([^"]+)"', chunk)
        entries.append({
            "id": site_id,
            "name": name,
            "group": "",
            "kind": "closed" if "(closed)" in name.lower() else "",
            "line1": line1,
            "city": city or _field(r'<div class="city">(.*?)</div>', chunk),
            "state": state or "",
            "postal_code": postal,
            "latitude": _float(r'data-latitude="([^"]*)"', tag.group(0)),
            "longitude": _float(r'data-longitude="([^"]*)"', tag.group(0)),
            "website": htmllib.unescape(web.group(1)) if web else "",
            "url": source_url,
            "address": address,
            "phone": _field(r'class="phoneLink"[^>]*>(.*?)</a>', chunk),
            "mailing": _field(r'class="mailAddress">(.*?)</div>', chunk).removeprefix("Mailing: "),
        })
    return entries


def _load(url: str) -> str:
    sys.path.insert(0, str(HERE))
    import visit  # the browser loader, with its Cloudflare retries

    visit._reexec_under_xvfb()
    import os
    import shutil

    sys.path.insert(0, str(visit.REPO / "src"))
    from pdf_extract.browser import launch_stealth_browser

    channel = os.getenv("PLAYWRIGHT_BROWSER_CHANNEL") or (
        "chrome" if shutil.which("google-chrome") else None
    )
    with launch_stealth_browser(channel=channel) as page:
        visit.goto(page, url, 8)
        if visit._challenged(page):
            raise SystemExit(f"Cloudflare challenged every load of {url}; retry in a minute")
        return page.content()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("url", nargs="?", help="the finder page (loaded in the browser)")
    parser.add_argument("--html", type=Path, help="parse a saved page instead of loading URL")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if not args.url and not args.html:
        parser.error("give the finder URL or --html")
    html = args.html.read_text(encoding="utf-8") if args.html else _load(args.url)
    entries = parse(html, args.url or "")
    if not entries:
        print("no <li class=\"site\"> entries found: not an eCatholic finder page?",
              file=sys.stderr)
        return 1
    args.out.write_text(json.dumps(entries, indent=1, ensure_ascii=False), encoding="utf-8")
    closed = sum(e["kind"] == "closed" for e in entries)
    print(json.dumps({"out": str(args.out), "entries": len(entries), "closed": closed,
                      "without_address": sum(not e["line1"] for e in entries)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
