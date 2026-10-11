import sys, io
sys.path.insert(0, "scripts")
from fetch_diocese_family_list import fetch_text, DEFAULT_URL, FAMILY_RE
txt = fetch_text(DEFAULT_URL)
open("scratch/masterlist.txt","w",encoding="utf-8").write(txt)
lines = [l.strip() for l in txt.splitlines() if l.strip()]
print(f"{len(lines)} non-blank lines")
# show every line the family regex matches, and every line that mentions Family
for i,l in enumerate(lines):
    if "Family" in l or "Campus" in l or "Newman" in l:
        mark = "MATCH" if FAMILY_RE.match(l) else "     "
        print(f"{i:4} {mark} {l[:100]}")
