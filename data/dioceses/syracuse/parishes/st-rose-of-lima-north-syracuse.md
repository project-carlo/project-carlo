---
name: St. Rose of Lima
website: https://strosecny.org
bulletin_provider: discover_mass
provider_id: st-rose-of-lima-north-syracuse-ny
publication: ['discovermass:st-rose-of-lima-north-syracuse-ny']
group: ''
evidence:
- url: https://discovermass.com/church/st-rose-of-lima-north-syracuse-ny/
  seen: 2026-09-26
  quote: St. Rose of Lima
  note: 'The Discover Mass church page the parish site links. issues.py: weekly issues, newest 2026-09-27
    (also 20 and 13 September). The 27 September issue has 8 pages; pages 1 to 6 are images with no text
    layer, so it was read by rendering the PDF. Page 1: "SEPTEMBER 27, 2026 ... SAINT ROSE OF LIMA CHURCH
    ... 407 SOUTH MAIN STREET | NORTH SYRACUSE, NEW YORK 13212".'
- url: https://strosecny.org/bulletin
  seen: 2026-09-26
  note: The parish's Bulletin page links only discovermass.com/church/st-rose-of-lima-north-syracuse-ny/.
- url: https://strosecny.org/newpageeaf31b5d
  seen: 2026-09-26
  quote: 'Saturday: 4:00pm'
  note: 'The parish''s "Mass Times, Confession & Adoration" page: Tuesday-Friday 9:00am, Saturday 4:00pm,
    Sunday 8:00am & 10:30am, all in the one church.'
---

## Publisher

St. Rose of Lima publishes its own weekly bulletin through Discover Mass (Diocesan). The 27 September
2026 issue's cover names "Saint Rose of Lima Church, 407 South Main Street, North Syracuse" and
nothing else; it is in no cluster in the diocese's lists. One parish, one church.

**The bulletin is image-only.** Pages 1 to 6 of the 27 September issue have no text layer (`probe pdf`
and issues.py read only the ad pages 7 and 8), so the pipeline's text extraction will get nothing from
the parish pages unless it OCRs. I read page 1 by rendering it. The Mass schedule used here comes from
the parish site.

## Worship sites

One: `churches/st-rose-of-lima-north-syracuse.md`. Mass times (parish site): Saturday 4:00 pm, Sunday
8:00 and 10:30 am, Tuesday to Friday 9:00 am.

## Website and bulletin provider

strosecny.org (an Our Sunday Visitor site) links its bulletin to Discover Mass, church slug
`st-rose-of-lima-north-syracuse-ny`, so that is `provider_id` and the only publication id. `probe url`
also reported `ecatholic:31250` for this site, but that id comes from a file linked from the
homepage (files.ecatholic.com/31250/documents/..., the bishop's Chapter 11 letter): 31250 is the
**Diocese of Syracuse's own eCatholic site**, not a parish bulletin, so it is not recorded.

## Not yet confirmed

Whether the pipeline can read an image-only Discover Mass bulletin (see Publisher).
