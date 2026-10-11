"""For each masterlist family, how many of OUR parish rows do its buildings span?
>1 means either a genuinely multi-bulletin family or a missed collapse (docs 6f(b))."""
import csv, json, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")

def norm(s):
    s = unicodedata.normalize("NFKD", s or "").lower()
    s = s.replace("&"," and ")
    s = re.sub(r"\bss\.?\b","saints",s); s = re.sub(r"\bsts\.?\b","saints",s)
    s = re.sub(r"\bst\.?\b","saint",s); s = re.sub(r"\bmt\.?\b","mount",s)
    s = s.replace("katherine","katharine")
    s = re.sub(r"\b(church|parish|the|of|roman|catholic|rc|basilica|oratory|chapel|shrine|national)\b"," ",s)
    s = re.sub(r"[^a-z0-9 ]"," ",s)
    return " ".join(s.split())

CITY_ALIAS={"eggertsville":"amherst","harris hill":"williamsville","athol springs":"hamburg",
            "swormsville":"swormville","silver springs":"silver spring"}
def ncity(c):
    c=norm(c); return CITY_ALIAS.get(c,c)

ch=list(csv.DictReader(open("data/churches.csv",encoding="utf-8")))
par={r["slug"]:r for r in csv.DictReader(open("data/parishes.csv",encoding="utf-8"))}
by_nc={}
for c in ch:
    by_nc.setdefault((norm(c["name"]), ncity(c["city"])), []).append(c)
by_n={}
for c in ch:
    by_n.setdefault(norm(c["name"]), []).append(c)

fams=json.load(open("scratch/families2.json",encoding="utf-8"))
print(f"{'fam':>4} {'rows':>4}  family / our parish rows")
print("-"*100)
for f in fams:
    entries=[]
    for p in f["parishes"]:
        entries.append((p["parish"], p["city"].split(",")[-1].strip()))
        for s in p.get("sites",[]):
            entries.append((s["site"], s["city"].split(",")[-1].strip()))
    pids=set()
    for name, city in entries:
        hits = by_nc.get((norm(name), ncity(city)))
        if not hits:
            cand = by_n.get(norm(name)) or []
            hits = [c for c in cand if ncity(c["city"]) == ncity(city)]
        for c in hits or []:
            pids.add(c["parish_id"])
    if len(pids) > 1:
        print(f"{f['family']:>4} {len(pids):>4}  {f['name']}")
        for pid in sorted(pids):
            row = par.get(pid, {})
            print(f"            -> {pid:<42} {row.get('website','?')}")
