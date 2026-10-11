import sys, ssl, re, gzip, io
from urllib.request import Request, urlopen
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
def get(url):
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*",
                                "Accept-Language": "en-US,en;q=0.9"})
    with urlopen(req, timeout=60, context=ctx) as r:
        raw = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return r.geturl(), r.status, raw.decode("utf-8", "replace")
for url in sys.argv[1:]:
    try:
        final, status, body = get(url)
        print(f"\n===== {url}\n  -> {final}  HTTP {status}  {len(body)} bytes")
        for pat, label in [
            (r'publicationWidget[^"\'<>]{0,80}', "LPi publicationWidget"),
            (r'parishesonline\.com[^"\'\s<>]{0,80}', "parishesonline"),
            (r'discovermass\.com[^"\'\s<>]{0,60}', "discovermass"),
            (r'ecatholic[^"\'\s<>]{0,40}', "ecatholic"),
            (r'[\w./-]*bulletin[\w./?=-]{0,60}', "bulletin-ish"),
            (r'seek\.catholic|myparishapp', "other"),
        ]:
            hits = sorted(set(re.findall(pat, body, re.I)))[:8]
            if hits:
                print(f"  [{label}]")
                for h in hits: print(f"      {h}")
    except Exception as e:
        print(f"\n===== {url}\n  ERROR {type(e).__name__}: {e}")
