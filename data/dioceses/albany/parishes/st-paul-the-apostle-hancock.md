---
name: St. Paul the Apostle
website: https://www.stpaulshancock.org/bulletin.htm
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.stpaulshancock.org/bulletin.htm']
group: ''
evidence:
- url: https://www.stpaulshancock.org/Bulletins/Bull_9_27_26.pdf
  seen: 2026-09-28
  quote: 346 West Main Street, Hancock, New York 13783
  note: 'Page 1 masthead of the 27 September 2026 issue: "St. Paul The Apostle Roman Catholic Church";
    "Mass for The Sabbath Saturday 6:30 PM Sunday 8:00 AM"; Pastor Rev. Dr. Bernard Osei Ampong. Page
    2 lists Masses Saturday 26 September 6:30 P.M. and Sunday 27 September 8:00 A.M., weekdays only rosary,
    Communion service and adoration.'
- url: https://www.stpaulshancock.org/bulletin.htm
  seen: 2026-09-28
  note: 'The site''s bulletin page (JavaScript menu; read in a browser with visit.py): links Bulletins/Bull_9_27_26.pdf
    and Homilies/Homily_9_27_26.pdf.'
promoted: 2026-09-28
---

## Publisher

St. Paul the Apostle, Hancock publishes its own weekly bulletin on its own site. I read the 27
September 2026 issue: masthead "St. Paul The Apostle Roman Catholic Church, 346 West Main
Street, Hancock", "Mass for The Sabbath Saturday 6:30 PM, Sunday 8:00 AM", pastor Rev. Dr.
Bernard Osei Ampong.

## Worship sites

- `churches/st-paul-the-apostle-hancock.md`: 346 West Main Street, Hancock.

No other place is named in the bulletin or grouped with it by the directory.

## Website and bulletin provider

stpaulshancock.org (both rosters) renders its menu by script, so `probe url` said
NO-PARISH-WORDS; `visit.py --bulletin` found `bulletin.htm`, which links the week's PDF as
`Bulletins/Bull_<M>_<D>_<YY>.pdf`. Self-hosted: `bulletin_provider: other`.

Fetch recipe `page-pdfs`, pinned 2026-10-03: on the pages recorded 2026-10-03
(`tests/fixtures/fetch/st-paul-the-apostle-hancock.json.gz`) the resolver found
https://www.stpaulshancock.org/Bulletins/Bull_10_4_26.pdf this way, dated that week.

## Not yet confirmed

Nothing.
