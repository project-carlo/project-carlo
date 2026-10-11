"""6f(b) screen, corrected: LPi publicationWidget ids are 15-18 char Salesforce
ids, so a \d+ pattern truncates every one of them to the shared prefix 00180000
and makes unrelated parishes look identical. Match the whole id."""
import csv, json, re, ssl, sys, gzip
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
sys.stdout.reconfigure(encoding="utf-8")
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
PATS = [
    ("lpi",       r"publicationWidget\?type=bulletin&id=([A-Za-z0-9]{15,18})"),
    ("lpi2",      r"[?&]id=([A-Za-z0-9]{18})"),
    ("ecatholic", r"files\.ecatholic\.com/(\d{3,8})/"),
    ("po-org",    r"parishesonline\.com/organization/([a-z0-9-]{4,90})"),
    ("po-cont",   r"container\.parishesonline\.com/bulletins/(\d+/\d+)"),
]
par={r["slug"]:r for r in csv.DictReader(open("data/parishes.csv",encoding="utf-8"))}
fams=json.load(open("scratch/multi.json",encoding="utf-8"))
def probe(url):
    try:
        with urlopen(Request(url, headers={"User-Agent":UA,"Accept":"text/html,*/*"}),
                     timeout=45, context=ctx) as r:
            raw=r.read()
            if r.headers.get("Content-Encoding")=="gzip": raw=gzip.decompress(raw)
            body=raw.decode("utf-8","replace")
            ids=[]
            for label,pat in PATS:
                for m in sorted(set(re.findall(pat, body, re.I)))[:3]:
                    ids.append(f"{label}:{m}")
            return f"HTTP{r.status}", ids
    except Exception as e:
        return type(e).__name__, []
targets=[(f["family"],f["name"],pid,par[pid]["website"])
         for f in fams for pid in f["pids"] if pid in par and par[pid].get("website")]
with ThreadPoolExecutor(max_workers=8) as ex:
    res=list(ex.map(lambda t: probe(t[3]), targets))
cur=None
for (fam,name,pid,url),(st,ids) in zip(targets,res):
    if fam!=cur: print(f"\n=== Family #{fam} {name}"); cur=fam
    print(f"   {pid:<48} {st:<11} {', '.join(ids) if ids else '-'}")
