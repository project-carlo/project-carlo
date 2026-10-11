import csv, sys
from pathlib import Path
p = Path("data/buffalo_excluded_sites.csv")
rows = list(csv.DictReader(p.open(encoding="utf-8")))
fields = ["site","city","reason","evidence","decided"]
existing = {(r["site"], r["city"]) for r in rows}

new = [
 {"site":"Queen of Angels","city":"Lackawanna","reason":"closed","decided":"2026-09-12",
  "evidence":(
   "Closed 2026-08-30; 144 Warsaw St. The Mary of Bethlehem family bulletin (ParishesOnline "
   "container 14/0453, whose LPi footer reads \"Our Lady of the Sacred Heart / Queen of Angels, "
   "Orchard Park, NY 14-0453\") announced it and then reported it. The 2026-08-23 issue: \"Please "
   "join us at Queen of Angels on August 29th for the last mass at 4:00pm Saturday and the last "
   "Spanish Mass will be on August 30th at 11:30am\", with both marked \"(Last Mass)\" in its "
   "Mass-intention table. The 2026-08-30 masthead still carries the site but prints \"Last Mass\" "
   "against both remaining times and has already dropped the Sunday 10:00am line. The 2026-09-06 "
   "issue drops the \"Secondary Worship Site (Queen of Angels)\" block altogether and welcomes "
   "\"our parishioners from our Queen of Angels site as we join with each other in one place of "
   "worship\". The Spanish-language community moved to St. Mary's on the Lake (Hamburg), first "
   "Mass 2026-09-06. Never modelled, so there is no church row to delete. NOTE the diocesan "
   "sunday-morning-mass-times page still listed Sun 10:00am and Sun 11:30am (Spanish) on "
   "2026-09-12, thirteen days after the last Mass - including the 10:00am the bulletin had "
   "already dropped; the Saturday and Sunday-afternoon pages carry no Queen of Angels row at all"
  )},
 {"site":"UB North Newman Center","city":"Amherst","reason":"no-bulletin","decided":"2026-09-12",
  "evidence":(
   "Open, and excluded for publishing nothing rather than for closing - the second case of the "
   "Holy Family (Sanborn) kind. The Newman Center at UB, 495 Skinnersville Rd, Amherst 14228, "
   "holds a full public weekend schedule (Sat 5:15pm; Sun 9:15am, 10:45am, and a 6:30pm student "
   "Mass) plus Thu noon, so it is in scope under docs 6f(f). It publishes only a subscribe-only "
   "Flocknote email newsletter (newmancenterub.flocknote.com/Newsletter) with no public archive, "
   "no PDF and no bulletin page; St. Joseph University Parish links to it as a sibling in its "
   "\"Campus Ministry Family\" list rather than covering it in a bulletin, and neither "
   "stjosephbuffalo.org nor ubstjoes.org contains the word \"bulletin\". The diocese names it "
   "only on the \"Campus Ministry Vicariate Family #36\" line of the April 2026 masterlist: it "
   "is absent from the parish finder and from all three weekend Mass-times pages, so no "
   "feed-based tool can see it. Revisit if it ever publishes"
  )},
]
added = [r for r in new if (r["site"], r["city"]) not in existing]
with p.open("a", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    for r in added:
        w.writerow(r)
print(f"appended {len(added)} rows; total now {len(rows)+len(added)}")
