import sys, ssl, re
from urllib.request import Request, urlopen
sys.stdout.reconfigure(encoding="utf-8")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
for url in sys.argv[1:]:
    with urlopen(Request(url, headers={"User-Agent":UA}), timeout=60, context=ctx) as r:
        body = r.read().decode("utf-8","replace")
    print(f"\n===== {url}")
    for m in sorted(set(re.findall(r'bulletins\.discovermass\.com/[a-z]+\.php\?bulletin=[A-Za-z0-9]+', body))):
        print("   ", m)
    # also the bulletin date text and archive
    for m in sorted(set(re.findall(r'(?:Sep|Aug|Jul)\s+\d{1,2},\s*20\d\d', body)))[:6]:
        print("    date:", m)
