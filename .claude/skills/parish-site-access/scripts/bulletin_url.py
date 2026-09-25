"""Find a parish's latest bulletin PDF without a browser.

Uses the provider routes that are not behind Cloudflare challenges, so it works
from sandboxes (and WebFetch) where the parish websites themselves return 403:

  parishes_online  JSON API behind parishesonline.com (slug -> org id -> publications)
  ecatholic        files.ecatholic.com/{site_id}/bulletins/{YYYYMMDD}.pdf, site id
                   taken from past data/metadata.json rows, newest Sunday probed first
  discover_mass    discovermass.com church page (server-rendered, needs a browser UA)

Anything else prints the website so you can look at it by hand.

Usage (from the repo root):
  python .claude/skills/parish-site-access/scripts/bulletin_url.py SLUG [SLUG ...]
  python .claude/skills/parish-site-access/scripts/bulletin_url.py --all
"""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

REPO = Path(__file__).resolve().parents[4]
PARISHES_CSV = REPO / "data" / "parishes.csv"
METADATA_JSON = REPO / "data" / "metadata.json"

# discovermass.com 403s Python's default "Python-urllib" agent.
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
PARISHES_ONLINE_API = "https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/organizations"
ECATHOLIC_WEEKS_BACK = 6


def _get(url: str, *, method: str = "GET") -> bytes:
    req = Request(url, method=method, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return resp.read()


def parishes_online(provider_id: str) -> tuple[str, str]:
    org = json.loads(_get(f"{PARISHES_ONLINE_API}/slug/{provider_id}"))["data"]
    pubs = json.loads(
        _get(f"{PARISHES_ONLINE_API}/{org['salesforce_id']}/publications?limit=5&type=Church")
    )["data"]
    bulletins = [p for p in pubs if p.get("type") == "Bulletin"] or pubs
    latest = max(bulletins, key=lambda p: p["publishDate"])
    return latest["publishDate"][:10], latest["fileUrl"]


def _ecatholic_site_id(slug: str) -> str | None:
    if not METADATA_JSON.exists():
        return None
    for row in reversed(json.loads(METADATA_JSON.read_text(encoding="utf-8"))):
        if row.get("parish_slug") != slug:
            continue
        match = re.match(r"https://files\.ecatholic\.com/(\d+)/", row.get("source_url", ""))
        if match:
            return match.group(1)
    return None


def ecatholic(slug: str) -> tuple[str, str]:
    site_id = _ecatholic_site_id(slug)
    if site_id is None:
        raise LookupError(
            "no files.ecatholic.com site id in data/metadata.json; find one by opening "
            "the parish's /bulletins page in a real browser (it is Cloudflare-challenged)"
        )
    today = date.today()
    next_sunday = today + timedelta(days=(6 - today.weekday()) % 7)
    for weeks in range(ECATHOLIC_WEEKS_BACK + 1):
        sunday = next_sunday - timedelta(weeks=weeks)
        url = f"https://files.ecatholic.com/{site_id}/bulletins/{sunday:%Y%m%d}.pdf"
        try:
            _get(url, method="HEAD")
        except HTTPError:  # missing files are 403 AccessDenied (S3), not 404
            continue
        return sunday.isoformat(), url
    raise LookupError(f"no bulletin for site {site_id} in the last {ECATHOLIC_WEEKS_BACK} weeks")


def discover_mass(provider_id: str) -> tuple[str, str]:
    html = _get(f"https://discovermass.com/church/{provider_id}/").decode("utf-8", "replace")
    match = re.search(
        r"href='(https://bulletins\.discovermass\.com/download\.php\?bulletin=[^']+)'"
        r"[^>]*><img[^>]*class='bulletin-cover X-\|(\d{4}-\d{2}-\d{2})\|",
        html,
    )
    if not match:
        raise LookupError("no current bulletin link on the discovermass page")
    return match.group(2), match.group(1)


def resolve(row: dict[str, str]) -> tuple[str, str]:
    provider, provider_id = row["bulletin_provider"], row["provider_id"]
    if provider == "parishes_online":
        return parishes_online(provider_id)
    if provider == "ecatholic":
        return ecatholic(row["slug"])
    if provider == "discover_mass":
        return discover_mass(provider_id)
    raise LookupError(f"provider {provider!r}: no API route, inspect {row['website']} by hand")


def main(argv: list[str]) -> int:
    with PARISHES_CSV.open(encoding="utf-8") as fh:
        rows = {r["slug"]: r for r in csv.DictReader(fh)}
    slugs = list(rows) if argv == ["--all"] else argv
    if not slugs:
        print(__doc__)
        return 2
    failed = 0
    for slug in slugs:
        row = rows.get(slug)
        if row is None:
            print(f"{slug}\tERROR\tunknown slug")
            failed += 1
            continue
        try:
            published, url = resolve(row)
            print(f"{slug}\t{published}\t{url}")
        except Exception as exc:  # report and keep going over the other parishes
            print(f"{slug}\tERROR\t{type(exc).__name__}: {exc}")
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
