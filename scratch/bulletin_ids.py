"""6f(b), made checkable: fetch every multi-row family's member sites once and
extract whatever bulletin-publisher id they embed. Members sharing an id share a
bulletin (docs 4b) -> under docs 1 they are ONE parish row."""
import csv, json, re, ssl, sys, gzip
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
sys.stdout.reconfigure(encoding="utf-8")
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

FAMILIES = json.loads(open(sys.argv[1], encoding="utf-8").read())
par={r["slug"]:r for r in csv.DictReader(open("data/parishes.csv",encoding="utf-8"))}

PATS = [
    ("lpi",        r'publicationWidget[^0-9]{0,40}(\d{3,8})'),
    ("lpi-alt",    r'4lpi\.com[^"\'\s]*?(\d{4,8})'),
    ("ecatholic",  r'files\.ecatholic\.com/(\d{3,8})/'),
    ("po-org",     r'parishesonline\.com/organization/([a-z0-9-]{4,90})'),
    ("po-cont",    r'container\.parishesonline\.com/bulletins/(\d+/\d+)'),
    ("discmass",   r'discovermass\.com/church/([a-z0-9-]{4,70})'),
    ("seekandfind",r'seekandfind\.com[^"\'\s]{0,60}'),
]

def probe(url):
    try:
        req=Request(url, headers={"User-Agent":UA,"Accept":"text/html,*/*"})
        with urlopen(req, timeout=45, context=ctx) as r:
            raw=r.read()
            if r.headers.get("Content-Encoding")=="gzip": raw=gzip.decompress(raw)
            body=raw.decode("utf-8","replace")
            ids=[]
            for label,pat in PATS:
                for m in sorted(set(re.findall(pat, body, re.I)))[:3]:
                    ids.append(f"{label}:{m}")
            return f"HTTP{r.status}", ids
    except Exception as e:
        return f"{type(e).__name__}", []

targets=[]
for f in FAMILIES:
    for pid in f["pids"]:
        w=par.get(pid,{}).get("website")
        if w: targets.append((f["family"], f["name"], pid, w))

with ThreadPoolExecutor(max_workers=8) as ex:
    results=list(ex.map(lambda t: probe(t[3]), targets))

cur=None
for (fam,name,pid,url),(status,ids) in zip(targets,results):
    if fam!=cur:
        print(f"\n=== Family #{fam} {name}"); cur=fam
    print(f"   {pid:<44} {status:<12} {', '.join(ids) if ids else '-'}")
