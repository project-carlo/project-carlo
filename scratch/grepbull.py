import sys, ssl, io, re
from urllib.request import Request, urlopen
sys.stdout.reconfigure(encoding="utf-8")
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
from pypdf import PdfReader
url=sys.argv[1]; terms=sys.argv[2:]
with urlopen(Request(url, headers={"User-Agent":"Mozilla/5.0 (project-carlo)"}), timeout=90, context=ctx) as r:
    data=r.read()
rd=PdfReader(io.BytesIO(data))
print(f"{url}\n{len(data)} bytes, {len(rd.pages)} pages\n")
pages=[(n,(p.extract_text() or "")) for n,p in enumerate(rd.pages,1)]
full="\n".join(t for _,t in pages)
open("scratch/last_bull.txt","w",encoding="utf-8").write(full)
flat=re.sub(r"\s+","",full).lower()
for t in terms:
    key=re.sub(r"\s+","",t).lower()
    print(f"  {t!r:34} -> {flat.count(key)}")
print()
for t in terms:
    key=re.sub(r"\s+","",t).lower()
    for n,txt in pages:
        if key in re.sub(r"\s+","",txt).lower():
            # print surrounding context from the raw page
            idx=re.sub(r"\s+"," ",txt)
            m=re.search(re.sub(r"\s+",r"\s*",re.escape(t)), idx, re.I)
            ctxs = idx[max(0,m.start()-300):m.end()+400] if m else idx[:400]
            print(f"=== {t!r} on page {n} ===\n{ctxs}\n")
