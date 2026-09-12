#!/usr/bin/env python
"""Find families we model as several parish rows but which publish ONE bulletin.

This is the check for the one §1 violation that has **no observable symptom**
anywhere else in the repo. `reconcile_diocese_roster.py` measures buildings, so
does the §6f(a) masterlist diff, and `db create`/`pytest` never look at family
structure at all. A family carried as four `parish` rows instead of one is
therefore invisible: every one of its worship sites is already modelled, so
coverage is 100% and nothing is flagged. Buffalo's §6f(b) was declared "every
family has been read" twice while three such families sat in the data.

    uv run python scripts/fetch_diocese_family_list.py -o scratch/families.json
    uv run python scripts/audit_family_parish_rows.py scratch/families.json

Two passes:

1. **Structure.** For each masterlist family, map its parishes and worship sites
   onto `churches.csv` and count the distinct `parish_id`s they span. More than
   one is a *candidate*: either a genuinely multi-bulletin family (plenty exist
   -- Buffalo #7 and #16) or a missed collapse.
2. **Publisher.** One GET per member parish website, extracting whatever
   bulletin-publisher id it embeds. Members sharing an id share a bulletin, and
   under docs §1 that is one `parish` row.

A shared id is a LEAD, never a licence to delete a row. Confirm by reading the
masthead (`probe_bulletin_container.py`), and apply the Fourteen Holy Helpers
rule from docs §4c: a member that still publishes its own bulletin keeps its own
row no matter what the diocese's structure says. The signal that a collapse is
safe is the family container publishing *this week* while each member's own
container has gone silent.

Two traps this script exists to avoid, both of which produced confident nonsense
when done by hand:

* An LPi `publicationWidget` id is an 18-character Salesforce id, **not** a
  number. Extracting it with `(\\d+)` truncates every id to the shared prefix
  `00180000` and makes unrelated parishes look identical -- which nearly
  collapsed three correct rows in Buffalo Family #7.
* Do **not** compare bytes or hashes to decide "same bulletin". A parish that
  self-hosts its family's bulletin serves a different file -- different size,
  different SHA-256, even a different page count -- of the same issue.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import re
import ssl
import sys
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

DATA = Path(__file__).resolve().parent.parent / "data"
PARISHES_CSV = DATA / "parishes.csv"
CHURCHES_CSV = DATA / "churches.csv"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

_CTX = ssl.create_default_context()
_CTX.check_hostname = False
_CTX.verify_mode = ssl.CERT_NONE

# Publisher fingerprints. Each must capture the id IN FULL -- see the docstring.
PUBLISHER_PATTERNS = [
    ("lpi", r"publicationWidget\?type=bulletin&id=([A-Za-z0-9]{15,18})"),
    ("ecatholic", r"files\.ecatholic\.com/(\d{3,8})/"),
    ("po-org", r"parishesonline\.com/organization/([a-z0-9-]{4,90})"),
    ("po-container", r"container\.parishesonline\.com/bulletins/(\d+/\d+)"),
    ("discovermass", r"discovermass\.com/church/([a-z0-9-]{4,70})"),
]

# The masterlist names hamlets where the feed names towns (docs §4e).
CITY_ALIAS = {
    "eggertsville": "amherst", "harris hill": "williamsville",
    "athol springs": "hamburg", "swormsville": "swormville",
    "silver springs": "silver spring", "tuscarora reservation": "sanborn",
}

# Stripped before matching: the masterlist names the PARISH where churches.csv
# names the BUILDING, and the honorific is not part of the dedication.
_NOISE = (r"\b(church|parish|the|of|roman|catholic|rc|basilica|oratory|chapel"
          r"|shrine|national)\b")


def norm(value: str) -> str:
    s = unicodedata.normalize("NFKD", value or "").lower()
    s = s.replace("&", " and ")
    # "St. Mary's Church (Swormville)" must reduce to the same key as the
    # masterlist's bare "St. Mary", or this audit silently skips the row --
    # which is exactly how st-mary-swormville hid inside Family #15.
    s = re.sub(r"\([^)]*\)", " ", s)            # drop a disambiguating parenthetical
    s = re.sub(r"\b(\w+)['’]s\b", r"\1", s)  # possessive: mary's -> mary
    s = re.sub(r"\bss\.?\b", "saints", s)
    s = re.sub(r"\bsts\.?\b", "saints", s)
    s = re.sub(r"\bst\.?\b", "saint", s)
    s = re.sub(r"\bmt\.?\b", "mount", s)
    s = s.replace("katherine", "katharine")
    s = re.sub(_NOISE, " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(s.split())


def norm_city(value: str) -> str:
    city = norm(value)
    return CITY_ALIAS.get(city, city)


def family_entries(family: dict) -> list[tuple[str, str]]:
    """Every (dedication, city) the family names, parishes and worship sites."""
    out = []
    for parish in family["parishes"]:
        # A few entries list several towns ("Newfane, Olcott, Wilson") and a few
        # dedications contain a comma ("Holy Family of Jesus, Mary, and Joseph"),
        # which `split_place` splits on -- the town is the last field either way.
        out.append((parish["parish"], parish["city"].split(",")[-1].strip()))
        for site in parish.get("sites", []):
            out.append((site["site"], site["city"].split(",")[-1].strip()))
    return out


def fetch_ids(url: str) -> tuple[str, list[str]]:
    try:
        req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
        with urlopen(req, timeout=45, context=_CTX) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            body = raw.decode("utf-8", "replace")
        ids = []
        for label, pattern in PUBLISHER_PATTERNS:
            for found in sorted(set(re.findall(pattern, body, re.I)))[:3]:
                ids.append(f"{label}:{found}")
        return f"HTTP{resp.status}", ids
    except Exception as exc:                        # noqa: BLE001 - reported, not raised
        return type(exc).__name__, []


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("families", type=Path,
                    help="JSON from fetch_diocese_family_list.py")
    ap.add_argument("--no-fetch", action="store_true",
                    help="structure pass only; skip the one-GET-per-site screen")
    args = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):          # mastheads are full of typographic quotes
        sys.stdout.reconfigure(encoding="utf-8")

    parishes = {r["slug"]: r for r in csv.DictReader(
        PARISHES_CSV.open(encoding="utf-8"))}
    churches = list(csv.DictReader(CHURCHES_CSV.open(encoding="utf-8")))

    by_name_city: dict[tuple[str, str], list[dict]] = {}
    by_name: dict[str, list[dict]] = {}
    for church in churches:
        by_name_city.setdefault(
            (norm(church["name"]), norm_city(church["city"])), []).append(church)
        by_name.setdefault(norm(church["name"]), []).append(church)

    families = json.loads(args.families.read_text(encoding="utf-8"))

    candidates = []
    for family in families:
        pids: set[str] = set()
        for name, city in family_entries(family):
            hits = by_name_city.get((norm(name), norm_city(city)))
            if not hits:
                # dedication we carry with a suffix the masterlist drops
                hits = [c for c in by_name.get(norm(name), [])
                        if norm_city(c["city"]) == norm_city(city)]
            for church in hits or []:
                pids.add(church["parish_id"])
        if len(pids) > 1:
            candidates.append((family, sorted(pids)))

    print(f"{len(families)} families; {len(candidates)} span more than one parish row\n")
    if not candidates:
        return

    targets = [(fam["family"], fam["name"], pid, parishes[pid]["website"])
               for fam, pids in candidates for pid in pids
               if pid in parishes and parishes[pid].get("website")]

    if args.no_fetch:
        results = [("(not fetched)", []) for _ in targets]
    else:
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(lambda t: fetch_ids(t[3]), targets))

    shared_any = False
    current = None
    for (number, name, pid, _url), (status, ids) in zip(targets, results):
        if number != current:
            print(f"=== Family #{number} {name}")
            current = number
            seen: dict[str, list[str]] = {}
            for (n2, _nm, p2, _u2), (_s2, ids2) in zip(targets, results):
                if n2 == number:
                    for i in ids2:
                        seen.setdefault(i, []).append(p2)
            shared = {i: rows for i, rows in seen.items() if len(rows) > 1}
            if shared:
                shared_any = True
                for i, rows in shared.items():
                    print(f"    *** SHARED {i} across {len(rows)} rows: {', '.join(rows)}")
        print(f"    {pid:<48} {status:<12} {', '.join(ids) if ids else '-'}")
    print()
    if shared_any:
        print("A SHARED line is a lead, not a verdict: read the masthead and check that each")
        print("member's own former container has gone silent before collapsing any row.")


if __name__ == "__main__":
    main()
