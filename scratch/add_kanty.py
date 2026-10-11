import csv
from pathlib import Path
p = Path("data/buffalo_excluded_sites.csv")
rows = list(csv.DictReader(p.open(encoding="utf-8")))
fields = ["site","city","reason","evidence","decided"]
if any(r["site"] == "St. John Kanty" for r in rows):
    print("already present"); raise SystemExit
row = {"site":"St. John Kanty","city":"Buffalo","reason":"closed","decided":"2026-09-12",
 "evidence":(
  "101 Swinburne St. Last Mass 2025-05-18 at 10:15 am after a concert of Polish hymns, announced "
  "by the parish itself: its own bulletin for that Sunday is headed \"OUR LAST MASS AS SAINT JOHN "
  "KANTY CHURCH IS THIS SUNDAY, MAY 18\", and stjohnkantychurchbuffalo.wordpress.com now titles "
  "itself \"(1892-2025) - Closed\" with no issue since. The Sunday Mass moved to St. Stanislaus at "
  "10:15 and the community is served by the Greater East Buffalo family, now modelled as "
  "greater-east-buffalo-catholic. The diocese's own sacramental-records index gives \"St. John "
  "Kanty (1892-2025) | St. Stanislaus\". Absent from the parish finder, from the April 2026 "
  "masterlist and from all three weekend Mass-times pages. RECORDED WITH A CAVEAT: the Vatican "
  "suspended the merger decree in September 2025 and accepted the parishioners' recourse for "
  "examination, and the recourse group said it would begin scheduling Masses - so the CANONICAL "
  "status is unsettled. This row asserts only what every source agrees on, that the building has "
  "hosted no scheduled Mass since 2025-05-18 and publishes nothing. Per docs 4b the bulletin is "
  "what we model, and its bulletin ended. Revisit if Mass resumes or the appeal restores the "
  "parish. Never modelled, so no church row was deleted. Its former domain saintjohnkanty.com is "
  "now an online-slots squat (see 6e)"
 )}
with p.open("a", encoding="utf-8", newline="") as f:
    csv.DictWriter(f, fieldnames=fields, lineterminator="\n").writerow(row)
print("appended St. John Kanty")
