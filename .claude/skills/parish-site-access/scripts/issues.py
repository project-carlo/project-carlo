"""`probe container` for the other two bulletin publishers: eCatholic and Discover Mass.

`pnpm diocese probe container` walks a ParishesOnline container back Sunday by
Sunday; nothing in the CLI does the same for eCatholic or Discover Mass. Both
serve their bulletins from hosts that are NOT behind Cloudflare, so this needs
no browser even when the parish's own eCatholic site is challenged:

  ecatholic     files.ecatholic.com/{site id}/bulletins/{YYYYMMDD}.pdf, one per Sunday.
                Like ParishesOnline, a missing issue answers 403 (S3 AccessDenied),
                not 404, and there is no directory listing.
  discovermass  discovermass.com/church/{slug}/ is server-rendered and lists the
                current issue plus an archive of about 12, each a download.php link.

Takes the publication id as `probe url`/visit.py report it (ecatholic:20434,
discovermass:st-patrick-victor-ny), the bare id/slug, or any URL containing it.

Usage (from the repo root):
  uv run python .claude/skills/parish-site-access/scripts/issues.py ecatholic <id> \
      [--weeks 12] [--from DATE] [--step N] [--all] [--day fri] [--pages N] [--grep TEXT ...]
  uv run python .claude/skills/parish-site-access/scripts/issues.py discovermass <slug> \
      [--issues 6] [--pages N] [--grep TEXT ...]

--pages N adds the text of the first N readable pages of each issue found (the
masthead is often on page 2 or 3), and --grep counts and quotes a term per page,
exactly as `probe pdf` does (--grep alone reads 3 pages). Prints JSON.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "src"))

from pdf_extract.dioceses import web  # noqa: E402

ECATHOLIC_FILES = "https://files.ecatholic.com"
DISCOVER_MASS_CHURCH = "https://discovermass.com/church/{slug}/"
_DM_ISSUE_RE = re.compile(
    r"href='(https://bulletins\.discovermass\.com/download\.php\?bulletin=[^']+)'[^>]*>"
    r"([A-Z][a-z]{2} \d{1,2}, \d{4})<"
)


def _key(raw: str, scheme: str, pattern: str) -> str:
    raw = raw.strip()
    if raw.startswith(f"{scheme}:"):
        return raw.split(":", 1)[1].strip("/").lower()
    match = re.search(pattern, raw, flags=re.I)
    return match.group(1).lower() if match else raw.strip("/").lower()


def _with_text(urls: list[str], pages: int, grep: list[str]) -> list[dict[str, Any]]:
    return [web.pdf_text(url, pages=pages, grep=grep) for url in urls]


WEEKDAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")


def _ecatholic_url(site: str, day: dt.date) -> str:
    return f"{ECATHOLIC_FILES}/{site}/bulletins/{day:%Y%m%d}.pdf"


def ecatholic(args: argparse.Namespace) -> dict[str, Any]:
    site = _key(args.id, "ecatholic", r"files\.ecatholic\.com/(\d+)")
    if not site.isdigit():
        raise SystemExit(f"an eCatholic site id is a number, got {site!r}")
    if args.from_date:
        try:
            start = dt.date.fromisoformat(args.from_date)
        except ValueError:
            raise SystemExit(f"--from takes a date as YYYY-MM-DD, got {args.from_date!r}")
        # the Sunday on or before it, as probe container --from does
        sunday = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    else:
        # Parishes post the coming Sunday's issue mid-week, so start from the next Sunday.
        today = dt.date.today()
        sunday = today + dt.timedelta(days=(6 - today.weekday()) % 7)
    probed, found = [], []
    # Some parishes date the file by another day of the week (Holy Spirit,
    # Hamilton: the Friday before); --day shifts every probe back to it.
    before_sunday = (6 - WEEKDAYS.index(args.day)) % 7
    for i in range(0, args.weeks, max(1, args.step)):
        day = sunday - dt.timedelta(weeks=i, days=before_sunday)
        url = _ecatholic_url(site, day)
        resp = web.fetch(url, method="HEAD")
        probed.append({"date": day.isoformat(), "status": resp.status or resp.error})
        if resp.ok:
            found.append(url)
            if not args.all:
                break
    out: dict[str, Any] = {
        "publication": f"ecatholic:{site}",
        "latest": found[0] if found else None,
        "found": len(found),
        "probed": probed,
    }
    if not found:
        out["note"] = (
            f"no Sunday-dated issue in {len(probed)} Sundays probed (a missing issue answers "
            "403). Some parishes date files by another weekday (try --day fri or --day sat) or "
            "name them differently: open the site's /bulletins page with "
            "visit.py --links --match 'files.ecatholic|discovermass' and read the real file "
            "names. An eCatholic site may post its bulletin on Discover Mass instead "
            "(bulletins.discovermass.com links): then use issues.py discovermass."
        )
    elif not args.from_date and found[0] < _ecatholic_url(
        site, dt.date.today() - dt.timedelta(days=45)
    ):
        out["note"] = (
            f"newest issue is {found[0].rsplit('/', 1)[-1][:8]}: publishing here has stopped"
        )
    if (args.pages or args.grep) and found:
        out["issues"] = _with_text(found, args.pages or 3, args.grep)
    return out


def discovermass(args: argparse.Namespace) -> dict[str, Any]:
    slug = _key(args.slug, "discovermass", r"discovermass\.com/church/([a-z0-9-]+)")
    url = DISCOVER_MASS_CHURCH.format(slug=slug)
    resp = web.fetch(url)
    if not resp.ok:
        return {
            "publication": f"discovermass:{slug}",
            "url": url,
            "error": resp.error or f"HTTP {resp.status}",
        }
    page = resp.text()
    title = re.search(r"<title[^>]*>(.*?)</title>", page, flags=re.S | re.I)
    issues, seen = [], set()
    for link, label in _DM_ISSUE_RE.findall(page):
        if link in seen:
            continue
        seen.add(link)
        date = dt.datetime.strptime(label, "%b %d, %Y").date().isoformat()
        issues.append({"date": date, "url": html.unescape(link)})
    out: dict[str, Any] = {
        "publication": f"discovermass:{slug}",
        "url": url,
        "title": " ".join(html.unescape(title.group(1)).split()) if title else None,
        "latest_issue": issues[0]["date"] if issues else None,
        "issues": issues[: args.issues],
    }
    if not issues:
        out["note"] = "no bulletins listed: this church does not publish through Discover Mass now"
    elif issues[0]["date"] < (dt.date.today() - dt.timedelta(days=45)).isoformat():
        out["note"] = f"newest issue is {issues[0]['date']}: publishing here has stopped"
    if (args.pages or args.grep) and issues:
        out["text"] = _with_text(
            [i["url"] for i in issues[: args.issues]], args.pages or 3, args.grep
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="publisher", required=True)
    ec = sub.add_parser("ecatholic", help="walk back an eCatholic site's Sunday bulletins")
    ec.add_argument("id", help="ecatholic:<id>, the site id, or a files.ecatholic.com URL")
    ec.add_argument("--weeks", type=int, default=12)
    ec.add_argument("--from", dest="from_date", help="start from this date (YYYY-MM-DD)")
    ec.add_argument("--step", type=int, default=1, help="probe every n-th Sunday (4 = monthly)")
    ec.add_argument("--all", action="store_true", help="keep going after the first issue")
    ec.add_argument("--day", choices=WEEKDAYS, default="sun",
                    help="the weekday files are dated by, if not the Sunday (e.g. fri)")
    dm = sub.add_parser("discovermass", help="a Discover Mass church's listed bulletins")
    dm.add_argument("slug", help="discovermass:<slug>, the slug, or the church page URL")
    dm.add_argument("--issues", type=int, default=6)
    for p in (ec, dm):
        p.add_argument("--pages", type=int, default=0)
        p.add_argument("--grep", action="append", default=[])
    args = parser.parse_args()
    result = ecatholic(args) if args.publisher == "ecatholic" else discovermass(args)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result.get("error"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
