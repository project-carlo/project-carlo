"""Family #30: one bulletin (masthead read on two hosts) -> one parish row (docs 1)."""
import csv
from pathlib import Path

OLD = ["corpus-christi-buffalo", "st-stanislaus-buffalo", "st-katharine-drexel-buffalo"]
NEW_SLUG = "greater-east-buffalo-catholic"
NEW = {"slug": NEW_SLUG,
       "name": "Greater East Buffalo Family of Parishes",
       "website": "https://eastbuffalocatholic.org",
       "bulletin_provider": "", "provider_id": ""}

pp = Path("data/parishes.csv")
rows = list(csv.DictReader(pp.open(encoding="utf-8")))
fields = list(rows[0].keys())
assert fields == ["slug","name","website","bulletin_provider","provider_id"], fields
idx = min(i for i, r in enumerate(rows) if r["slug"] in OLD)   # keep position in file
kept = [r for r in rows if r["slug"] not in OLD]
kept.insert(idx, NEW)
with pp.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(kept)
print(f"parishes.csv: {len(rows)} -> {len(kept)}")

cp = Path("data/churches.csv")
crows = list(csv.DictReader(cp.open(encoding="utf-8")))
cfields = list(crows[0].keys())
moved = 0
for r in crows:
    if r["parish_id"] in OLD:
        r["parish_id"] = NEW_SLUG; moved += 1
with cp.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cfields, lineterminator="\n"); w.writeheader(); w.writerows(crows)
print(f"churches.csv: re-pointed {moved} church rows to {NEW_SLUG}")
