import sys, ssl, io, hashlib
from urllib.request import Request, urlopen
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
from pypdf import PdfReader
for label, bid in [("ST MARY OF THE ANGELS","gQkxaZsg1lHfQZoLHAa"), ("ST JOHN","JSM2PmS0m7Bol9eNsET")]:
    url = f"https://bulletins.discovermass.com/download.php?bulletin={bid}"
    req = Request(url, headers={"User-Agent": UA})
    try:
        with urlopen(req, timeout=90, context=ctx) as r:
            data = r.read(); final = r.geturl()
    except Exception as e:
        print(f"\n##### {label}: ERROR {e}"); continue
    print(f"\n##### {label}  ({len(data)} bytes)  sha256={hashlib.sha256(data).hexdigest()[:16]}")
    print(f"   final URL: {final}")
    open(f"scratch/bull_{label.split()[1].lower()}.pdf","wb").write(data)
    try:
        rd = PdfReader(io.BytesIO(data))
        print(f"   pages: {len(rd.pages)}")
        for n,p in enumerate(rd.pages[:2],1):
            t=(p.extract_text() or "").strip()
            print(f"   --- page {n} ---\n{t[:1400]}")
    except Exception as e:
        print(f"   pdf error {e}")
