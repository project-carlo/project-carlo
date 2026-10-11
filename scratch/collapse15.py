"""Family #15: the family's single BULLETIN link, the bulletin's own Mass schedule,
and the org slug on Nativity's site all name the SAME three parishes. Our Lady of
Peace (Clarence) and St. Teresa of Avila (Akron) are in the family but not in that
bulletin, and are deliberately left as their own rows (docs 6f(b))."""
import csv
from pathlib import Path

OLD = ["st-mary-swormville",
       "nativity-of-the-blessed-virgin-mary-williamsville",
       "sacred-heart-of-jesus-bowmansville"]
NEW = {"slug": "st-mary-nativity-sacred-heart",
       "name": "St. Mary, Nativity of the BVM & Sacred Heart of Jesus",
       "website": "https://togetherinchristfamily.org",
       "bulletin_provider": "", "provider_id": ""}

pp, cp = Path("data/parishes.csv"), Path("data/churches.csv")
rows = list(csv.DictReader(pp.open(encoding="utf-8")))
pf = list(rows[0].keys())
have = {r["slug"] for r in rows}
assert all(s in have for s in OLD), [s for s in OLD if s not in have]
idx = min(i for i, r in enumerate(rows) if r["slug"] in OLD)
rows = [r for r in rows if r["slug"] not in OLD]
rows.insert(idx, NEW)

crows = list(csv.DictReader(cp.open(encoding="utf-8")))
cf = list(crows[0].keys())
n = 0
for r in crows:
    if r["parish_id"] in OLD:
        r["parish_id"] = NEW["slug"]; n += 1

with pp.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=pf, lineterminator="\n"); w.writeheader(); w.writerows(rows)
with cp.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cf, lineterminator="\n"); w.writeheader(); w.writerows(crows)

slugs=[r["slug"] for r in rows]; sites=[r["website"] for r in rows]
assert len(slugs)==len(set(slugs)), "duplicate slug"
assert len(sites)==len(set(sites)), "duplicate website"
assert not ({r["parish_id"] for r in crows} - set(slugs)), "orphan church row"
print(f"{NEW['slug']}: 3 parish rows -> 1, {n} church rows re-pointed")
print(f"parishes: {len(rows)}  churches: {len(crows)}  (slug+website unique, no orphans)")
