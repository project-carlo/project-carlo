---
name: Sacred Heart Church
website: https://parishes.rcda.org/sacredheartsidney/bulletin.php
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://parishes.rcda.org/sacredheartsidney/bulletin.php']
group: ''
evidence:
- url: https://parishes.rcda.org/sacredheartsidney/bulletins/2026/September_20.pdf
  seen: 2026-09-28
  quote: Fr. Peter Anglaaere
  note: The 20 September 2026 issue (2 pages, newest listed on 2026-09-28). Page 1 lists Mass intentions
    for 9/21 to 9/27 (Mon-Thu 9:00 AM, Fri 9:00 AM Communion Service, Sat 4:00 PM, Sun 10:30 AM) and the
    celebrant for "Saturday 4:00 PM" and "Sunday 10:30AM" on 26/27 September. The bulletin prints no parish
    name or address in its text (checked by grep for "Sacred Heart", "Sidney", "Liberty"); it is identified
    by where it is posted.
- url: https://parishes.rcda.org/sacredheartsidney/bulletin.php
  seen: 2026-09-28
  quote: 'Saturday Vigil: 4:00 pm Sunday: 10:30 am Monday-Thursday 9:00 am'
  note: '"Sacred Heart Church, Sidney, NY": the parish''s page on the diocese''s parish-site host, with
    the list of dated bulletin PDFs.'
promoted: 2026-09-28
---

## Publisher

Sacred Heart, Sidney publishes its own weekly bulletin on its diocese-hosted site
("Sacred Heart Church, Sidney, NY"). I read the 20 September 2026 issue: page 1 lists the
week's Mass intentions (Monday to Thursday 9:00 am, a Friday Communion service, Saturday 4:00
pm, Sunday 10:30 am) and names Fr. Peter Anglaaere as celebrant for the 26/27 September
weekend Masses. The issue itself prints no parish name or address; I attribute it to Sacred
Heart because the parish's own page lists it (and its Mass times match that page's schedule).

## Worship sites

- `churches/sacred-heart-sidney.md`: 15 Liberty Street, Sidney.

The institutional-records index says the records of St. Ambrose, Unadilla (and St. Paul's,
Franklin, whose records are at "Sacred Heart Church") are held at Sacred Heart; neither
building is in a roster and the bulletin lists no Mass there.

## Website and bulletin provider

`parishes.rcda.org/sacredheartsidney/` is the site the directory links (GCatholic still has
sidneyonline.com). `bulletin.php` lists one PDF per Sunday at
`bulletins/<year>/<Month>_<DD>.pdf`. `bulletin_provider: other`.

Fetch recipe `page-pdfs`, pinned 2026-10-03: on the pages recorded 2026-10-03
(`tests/fixtures/fetch/sacred-heart-sidney.json.gz`) the resolver found
https://parishes.rcda.org/sacredheartsidney/bulletins/2026/October_04.pdf this way, dated
that week.

## Not yet confirmed

Which "Sacred Heart Church" holds St. Paul's, Franklin records (Sidney or Stamford): the index
does not say, and it does not affect any row. The 27 September issue was not yet posted on
2026-09-28.
