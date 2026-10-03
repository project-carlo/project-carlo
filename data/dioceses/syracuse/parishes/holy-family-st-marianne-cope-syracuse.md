---
name: Holy Family Church & St. Marianne Cope Parish
website: https://holyfamilysyr.org
bulletin_provider: other
provider_id: page-pdfs https://holyfamilysyr.org/bulletin
publication: ['url:https://holyfamilysyr.org/bulletin']
group: Holy Family, Fairmount + St. Marianne Cope, Solvay/Lakeland (shared pastor)
evidence:
- url: https://holyfamilysyr.org/s/HF-Bulletin-September-27-2026.pdf
  seen: 2026-09-26
  quote: Holy Family Church , Fairmount & St. Marianne Cope Parish Our Lady of Peace Church, Lakeland
    St. Cecilia’s Church, Solvay
  note: Masthead, page 1 of the 27 September 2026 issue. One bulletin for Holy Family and for St. Marianne
    Cope Parish's two churches.
- url: https://holyfamilysyr.org/s/HF-Bulletin-September-27-2026.pdf
  seen: 2026-09-26
  quote: 'HF: Holy Family • SC: St. Cecilia’s • OLOP: Our Lady of Peace'
  note: Legend of the page-9 "Mass schedule and intentions", which lists weekend Masses at all three (e.g.
    Sunday 9:30 AM SC, Saturday 4 PM OLOP, Saturday 4 PM and Sunday 7:30, 11 AM and 4 PM HF).
- url: https://holyfamilysyr.org/bulletin
  seen: 2026-09-26
  note: Holy Family's bulletin page, one PDF per week (HF-Bulletin-<Month>-<day>-<year>.pdf), newest 27
    September 2026. stmariannecope.org's own bulletin link points to this page (visit.py --bulletin on
    stmariannecope.org, 2026-09-26).
promoted: 2026-09-26
---

## Publisher

Holy Family Church (Fairmount) and St. Marianne Cope Parish (Solvay/Lakeland) share a
pastor, Rev. John D. Manno, and publish **one** weekly bulletin. I read the 27 September
2026 issue (holyfamilysyr.org/s/HF-Bulletin-September-27-2026.pdf, 10 pages): the page-1
masthead names "Holy Family Church, Fairmount & St. Marianne Cope Parish, Our Lady of Peace
Church, Lakeland, St. Cecilia's Church, Solvay" with the three church addresses, every page
header carries both parishes' phones and websites, and the page-9 Mass schedule uses the
codes HF, SC and OLOP for Masses at all three churches. Page 10 lists both parish offices
and both staffs.

## Worship sites

Three, all with weekend Mass in the 27 September issue: Holy Family, 127 Chapel Drive
(`holy-family-syracuse`); St. Cecilia, 1001 Woods Road, Solvay (`st-cecilia-solvay`); Our
Lady of Peace, 203 Halcomb Street, Lakeland (`our-lady-of-peace-lakeland`). St. Marianne
Cope Parish is the 2010s merger of St. Cecilia and Our Lady of Peace; the diocese lists
both former parishes as "(See St. Marianne Cope Parish, Solvay/Lakeland)", not closed, and
both still hold Mass. No other building appears in the bulletin.

## Website and bulletin provider

holyfamilysyr.org/bulletin lists the weekly PDFs, self-hosted on the parish's Squarespace
site, so the provider is `other` and the website is the Holy Family homepage (its
"Bulletin" link leads there). St. Marianne Cope's own site (stmariannecope.org, the
diocese directory's website for both its churches) has no bulletin of its own: its bulletin
link goes to holyfamilysyr.org/bulletin. So there is one publication, `url:` of that page.

Fetch recipe `page-pdfs https://holyfamilysyr.org/bulletin`, pinned 2026-10-03: on the
pages recorded 2026-09-27
(`tests/fixtures/fetch/holy-family-st-marianne-cope-syracuse.json.gz`) the resolver found
https://holyfamilysyr.org/s/HF-Bulletin-September-27-2026.pdf this way, dated that week.

## Not yet confirmed

Nothing.
