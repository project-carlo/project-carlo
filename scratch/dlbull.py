import sys, ssl, re, io, hashlib
from urllib.request import Request, urlopen
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
from pypdf import PdfReader
def fetch(url):
    with urlopen(Request(url, headers={"User-Agent":UA}), timeout=90, context=ctx) as r:
        return r.read()
for label, page in [("sma","https://discovermass.com/church/st-mary-of-the-angels-olean-ny/"),
                    ("stjohn","https://discovermass.com/church/st-john-olean-ny/")]:
    body = fetch(page).decode("utf-8","replace")
    ids = re.findall(r'bulletins\.discovermass\.com/download\.php\?bulletin=([^"\'&<>\s]+)', body)
    ids = sorted(set(ids), key=len, reverse=True)
    print(f"\n##### {label}: {len(ids)} ids, longest={len(ids[0]) if ids else 0}")
    got = False
    for bid in ids[:4]:
        data = fetch(f"https://bulletins.discovermass.com/download.php?bulletin={bid}")
        if data[:4] != b"%PDF":
            print(f"   id {bid[:24]}... -> not a pdf ({len(data)}b)"); continue
        open(f"scratch/bull_{label}.pdf","wb").write(data)
        rd = PdfReader(io.BytesIO(data))
        print(f"   OK id {bid[:24]}...  {len(data)}b  sha256={hashlib.sha256(data).hexdigest()[:16]}  pages={len(rd.pages)}")
        for n,p in enumerate(rd.pages[:2],1):
            t=(p.extract_text() or "").strip()
            print(f"   --- page {n} ---\n{t[:1500]}\n")
        got = True; break
    if not got: print("   no pdf retrieved")
