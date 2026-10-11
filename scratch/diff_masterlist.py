"""6f(a): diff every masterlist line (parish + worship site) against churches.csv."""
import csv, json, re, sys, unicodedata

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = s.replace("&", " and ")
    s = re.sub(r"\bss\.?\b", "saints", s)
    s = re.sub(r"\bsts\.?\b", "saints", s)
    s = re.sub(r"\bst\.?\b", "saint", s)
    s = re.sub(r"\bmt\.?\b", "mount", s)
    s = s.replace("katherine", "katharine")
    s = re.sub(r"\b(church|parish|the|of|roman|catholic|rc)\b", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(s.split())

# hamlet -> town aliases seen in this diocese (doc 6f(f))
CITY_ALIAS = {
    "eggertsville": "amherst", "harris hill": "williamsville",
    "athol springs": "hamburg", "swormsville": "swormville",
    "silver springs": "silver spring", "tuscarora reservation": "sanborn",
}
def ncity(c):
    c = norm(c)
    return CITY_ALIAS.get(c, c)

churches = list(csv.DictReader(open("data/churches.csv", encoding="utf-8")))
excluded = list(csv.DictReader(open("data/buffalo_excluded_sites.csv", encoding="utf-8")))

have_nc = {(norm(c["name"]), ncity(c["city"])) for c in churches}
have_n  = {}
for c in churches:
    have_n.setdefault(norm(c["name"]), []).append(c["city"])
excl_nc = {(norm(e["site"].split("|")[0]), ncity(e["city"])) for e in excluded}
excl_n  = {norm(e["site"].split("|")[0]) for e in excluded}

fams = json.load(open("scratch/families2.json", encoding="utf-8"))
rows = []
for f in fams:
    for p in f["parishes"]:
        rows.append((f["family"], f["name"], "PARISH", p["parish"], p["city"]))
        for s in p.get("sites", []):
            rows.append((f["family"], f["name"], "site", s["site"], s["city"]))

print(f"masterlist lines: {len(rows)}")
unmatched = []
for fam, famname, kind, name, city in rows:
    # city field can carry spillover from a comma inside the name
    city_last = city.split(",")[-1].strip()
    key = (norm(name), ncity(city_last))
    if key in have_nc:
        continue
    if key in excl_nc:
        continue
    n = norm(name)
    hint = ""
    if n in have_n:
        hint = f"  [name in churches.csv at: {', '.join(have_n[n])}]"
    elif n in excl_n:
        hint = "  [name in excluded.csv, different city]"
    unmatched.append((fam, famname, kind, name, city, hint))

print(f"unmatched: {len(unmatched)}\n")
for fam, famname, kind, name, city, hint in unmatched:
    print(f"#{fam:<3} {famname[:34]:<34} {kind:<6} {name} | {city}{hint}")
