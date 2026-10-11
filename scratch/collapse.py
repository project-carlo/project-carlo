"""Collapse families whose members share one bulletin (docs 1 + 4b).
Each entry verified: family container live this week, members' own containers dead."""
import csv, sys
from pathlib import Path

GROUPS = [
    {"old": ["assumption-buffalo","holy-spirit-buffalo","st-mark-buffalo","st-rose-of-lima-buffalo"],
     "slug": "catholic-community-buffalo-north",
     "name": "Catholic Community of Buffalo, North",
     "website": "https://catholiccbn.com"},
    {"old": ["nativity-of-our-lord-orchard-park","ss-peter-and-paul-hamburg",
             "st-bernadette-orchard-park","st-john-the-baptist-boston"],
     "slug": "eternal-flame-catholic-community",
     "name": "The Eternal Flame Catholic Community",
     "website": "https://eternalflamecc.com"},
]

pp, cp = Path("data/parishes.csv"), Path("data/churches.csv")
rows = list(csv.DictReader(pp.open(encoding="utf-8")))
pfields = list(rows[0].keys())
crows = list(csv.DictReader(cp.open(encoding="utf-8")))
cfields = list(crows[0].keys())

for g in GROUPS:
    missing = [s for s in g["old"] if s not in {r["slug"] for r in rows}]
    assert not missing, f"missing parish rows: {missing}"
    idx = min(i for i, r in enumerate(rows) if r["slug"] in g["old"])
    rows = [r for r in rows if r["slug"] not in g["old"]]
    rows.insert(idx, {"slug": g["slug"], "name": g["name"], "website": g["website"],
                      "bulletin_provider": "", "provider_id": ""})
    n = 0
    for r in crows:
        if r["parish_id"] in g["old"]:
            r["parish_id"] = g["slug"]; n += 1
    print(f"{g['slug']:<34} {len(g['old'])} parish rows -> 1, {n} church rows re-pointed")

with pp.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=pfields, lineterminator="\n"); w.writeheader(); w.writerows(rows)
with cp.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cfields, lineterminator="\n"); w.writeheader(); w.writerows(crows)

slugs = [r["slug"] for r in rows]
assert len(slugs) == len(set(slugs)), "duplicate parish slug"
sites = [r["website"] for r in rows]
assert len(sites) == len(set(sites)), "duplicate website"
orphan = {r["parish_id"] for r in crows} - set(slugs)
assert not orphan, f"orphan church parish_id: {orphan}"
print(f"parishes: {len(rows)}  churches: {len(crows)}  (slug+website unique, no orphans)")
