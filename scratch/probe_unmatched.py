import csv, re, unicodedata
def norm(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = s.replace("&"," and ")
    s = re.sub(r"\bss\.?\b","saints",s); s = re.sub(r"\bsts\.?\b","saints",s)
    s = re.sub(r"\bst\.?\b","saint",s); s = re.sub(r"\bmt\.?\b","mount",s)
    s = re.sub(r"[^a-z0-9 ]"," ",s)
    return " ".join(s.split())
ch = list(csv.DictReader(open("data/churches.csv",encoding="utf-8")))
CITIES = ["Belmont","Alfred","Fredonia","Dunkirk","Jamestown","Mayville","Bemus Point",
          "French Creek","Westfield","Newfane","Olcott","Wilson","Barker","Medina","Batavia",
          "Strykersville","Attica","Swormville","Buffalo","Olean","Lackawanna","North Collins",
          "Langford","Niagara Falls","Sherman","Clymer"]
for city in CITIES:
    rows = [c for c in ch if norm(c["city"]) == norm(city)]
    print(f"\n== {city} ({len(rows)}) ==")
    for c in rows:
        print(f"   {c['parish_id']:<38} {c['slug']:<34} {c['name']} | {c['line1']}")
