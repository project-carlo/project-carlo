"""Restore provider ids the collapse would otherwise drop.

The rows removed by the §6f(b) collapses carried verified parishes_online
provider_ids. Each surviving family row gets the SHARED org slug its members
actually embed -- the same format as every other parishes_online row
(PARISHES_ONLINE_ORG_URL_TEMPLATE takes the slug). greater-east-buffalo-catholic
is left blank on purpose: its bulletin is eCatholic, whose provider_id is a base
URL rather than the numeric site id (35834), so `detect` should claim it.
"""
import csv
from pathlib import Path

SET = {
    # family #20: this slug is embedded by BOTH st-mark and st-rose-of-lima
    "catholic-community-buffalo-north": ("parishes_online", "holy-spirit-church-14216"),
    # family #28: embedded by BOTH nativity-of-our-lord and st-bernadette
    "eternal-flame-catholic-community": ("parishes_online", "the-eternal-flame-catholic-community"),
    # family #15: the family site's own single BULLETIN link points here
    "st-mary-nativity-sacred-heart": ("parishes_online", "st-mary-nativity-of-the-bvm-sacred-heart"),
}

p = Path("data/parishes.csv")
rows = list(csv.DictReader(p.open(encoding="utf-8")))
fields = list(rows[0].keys())
n = 0
for r in rows:
    if r["slug"] in SET:
        provider, pid = SET[r["slug"]]
        assert r["bulletin_provider"] == "", r
        r["bulletin_provider"], r["provider_id"] = provider, pid
        n += 1
assert n == len(SET), f"set {n} of {len(SET)}"
ids = [r["provider_id"] for r in rows if r["provider_id"]]
assert len(ids) == len(set(ids)), "duplicate provider_id"
with p.open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n"); w.writeheader(); w.writerows(rows)
print(f"set provider on {n} rows; provider_ids unique")
