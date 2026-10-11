import sys
sys.stdout.reconfigure(encoding="utf-8")
lines = open("docs/buffalo-expansion.md", encoding="utf-8").read().splitlines()
blocks, cur = [], []
for i, l in enumerate(lines, 1):
    if l.lstrip().startswith("|"):
        cur.append((i, l))
    elif cur:
        blocks.append(cur); cur = []
if cur:
    blocks.append(cur)
BS = chr(92)
for b in blocks:
    counts = set()
    for _, l in b:
        n, prev = 0, ""
        for ch in l:
            if ch == "|" and prev != BS:
                n += 1
            prev = ch
        counts.add(n)
    status = "OK      " if len(counts) == 1 else "MISMATCH"
    print(f"{status} lines {b[0][0]}-{b[-1][0]}  rows={len(b)}  pipes={sorted(counts)}")
