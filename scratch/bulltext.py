import sys, io, re
sys.stdout.reconfigure(encoding="utf-8")
from pypdf import PdfReader
path = sys.argv[1]
rd = PdfReader(path)
full = "\n".join((p.extract_text() or "") for p in rd.pages)
# the PDF has letter-spacing artefacts; collapse them for searching
flat = re.sub(r"\s+", "", full).lower()
open(path+".txt","w",encoding="utf-8").write(full)
for term in ["portville","sacredheart","bonaventure","allegany","stjohn","basilica","masschedule","massschedule"]:
    print(f"{term:18} -> {flat.count(term)}")
print("\n--- pages mentioning portville/sacred heart ---")
for n,p in enumerate(rd.pages,1):
    t = (p.extract_text() or "")
    f = re.sub(r"\s+","",t).lower()
    if "portville" in f or "sacredheart" in f:
        print(f"\n=== page {n} ===\n{t[:2200]}")
