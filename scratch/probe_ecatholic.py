import sys, ssl, datetime as dt, io
from urllib.request import Request, urlopen
from urllib.error import HTTPError
sys.stdout.reconfigure(encoding="utf-8")
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA="Mozilla/5.0 (project-carlo bulletin probe)"
site=sys.argv[1]
d=dt.date.today()
d -= dt.timedelta(days=(d.weekday()+1) % 7)   # most recent Sunday
for i in range(8):
    day=d - dt.timedelta(weeks=i)
    url=f"https://files.ecatholic.com/{site}/bulletins/{day:%Y%m%d}.pdf"
    try:
        with urlopen(Request(url, headers={"User-Agent":UA}), timeout=45, context=ctx) as r:
            data=r.read()
        print(f"{day}  FOUND  {len(data)} bytes  {url}")
        open("scratch/ecath.pdf","wb").write(data)
        from pypdf import PdfReader
        rd=PdfReader(io.BytesIO(data))
        print(f"  pages={len(rd.pages)}")
        for n,p in enumerate(rd.pages[:2],1):
            print(f"  --- page {n} ---\n{(p.extract_text() or '')[:1300]}\n")
        break
    except HTTPError as e:
        print(f"{day}  {e.code}")
    except Exception as e:
        print(f"{day}  {type(e).__name__}")
