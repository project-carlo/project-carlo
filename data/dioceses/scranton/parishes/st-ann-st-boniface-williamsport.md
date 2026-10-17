---
name: The Parishes of Saint Ann & Saint Boniface
website: http://sponsors.bonventure.net/?page=1801
bulletin_provider: other
provider_id: ''
publication: ['url:http://sponsors.bonventure.net/?page=1801']
group: Saint Ann Parish Williamsport; Saint Boniface Parish
evidence:
- url: http://sponsors.bonventure.net/pdfs/1801/2026-10-18.pdf
  seen: 2026-10-16
  quote: THE PARISHES OF … SAINT ANN … SAINT BONIFACE … October 18, 2026 … Rev. Glenn E. McCreary, V.E.
  note: 'Cover (page 1) of the 18 October 2026 issue: "The Parishes of Saint Ann & Saint Boniface", Rev.
    Glenn E. McCreary, V.E. and Rev. Dias Antony Valiamarathungal, "Parish Office & Rectory, 326 Washington
    Boulevard".'
- url: http://sponsors.bonventure.net/pdfs/1801/2026-10-18.pdf
  seen: 2026-10-16
  quote: 4:00 PM at Saint Boniface … 5:30 PM at Saint Ann … 8:00 AM at Saint Lawrence … 9:30 AM at Saint
    Ann … 11:00 AM at Saint Boniface
  note: Page 2 "REGULAR SCHEDULE", Masses Saturday and Sunday; weekdays at Saint Lawrence, Saint Boniface,
    Saint Ann and (Wednesday 7:00 AM) Divine Providence Hospital Chapel.
- url: http://sponsors.bonventure.net/?page=1801
  seen: 2026-10-16
  note: 'Bonventure''s page for publication 1801, "The Parishes of St. Ann and St. Boniface": "Click to
    View Current Bulletin" -> pdfs/1801/2026-10-18.pdf, and a "Previous bulletins" menu of every Sunday
    back to 2018 (pdfs/1801/<yyyy-mm-dd>.pdf). Read over http on 2026-10-16; the https address fails certificate
    verification (incomplete chain on the server).'
- url: https://www.stbonifacecatholic.com/
  seen: 2026-10-16
  quote: as we celebrate the first anniversary of the linkage of St. Ann and St. Boniface parishes
  note: Homepage, read 2026-10-16. Its bulletin posts ("This Week's Bulletin October 11") link sponsors.bonventure.net/pdfs/1801/2026-10-11.pdf;
    stannrcc.org's "Weekly Bulletin" tile links sponsors.bonventure.net/?page=1801.
promoted: 2026-10-17
---

## Publisher

St. Ann and St. Boniface, Williamsport are two canonical parishes in the diocesan finder that
were linked about October 2025 (St. Boniface's homepage announces "the first anniversary of the
linkage of St. Ann and St. Boniface parishes" on 24 October 2026). They share a pastor (Rev.
Glenn E. McCreary, V.E.), one office (326 Washington Boulevard; the finder gives that address for
both parishes) and **one bulletin**, printed by Bonventure: the 18 October 2026 cover reads "The
Parishes of Saint Ann & Saint Boniface". Both parish websites link that same bulletin. One row.

## Worship sites

Three churches, all with weekend Mass in the 18 October 2026 "REGULAR SCHEDULE":

- `st-boniface-williamsport` (Saturday 4:00 pm, Sunday 11:00 am, weekdays 8:00 am)
- `st-ann-williamsport` (Saturday 5:30 pm, Sunday 9:30 am, Thursday and Friday 7:00 am)
- `st-lawrence-south-williamsport` (Sunday 8:00 am, Monday and Tuesday 7:00 am)

The schedule also lists "Wednesday 7:00 AM at Divine Providence Hospital Chapel", a place no
roster has; it is in `open/divine-providence-hospital-chapel-williamsport` until it is clear
whether that Mass is public. The bulletin's Mary, Mother of Mercy Adoration Chapel (convent
building behind St. Ann's parish center, 1648 Sheridan Street) has adoration, not Mass, so it is
not a church row.

## Website and bulletin provider

The bulletin is published on Bonventure's sponsor site, page 1801, which links the current issue
and every earlier one as `pdfs/1801/<yyyy-mm-dd>.pdf` (dated file names; the 18 October issue was
up on 16 October). `website` is that page over **http**, because its https certificate chain is
incomplete and fails verification (a server problem, not the proxy). Provider `other`;
`provider_id` is left empty until a `fetch:check` run after promotion suggests a recipe. The
parish sites (stannrcc.org, stbonifacecatholic.com) only link to Bonventure.

## Not yet confirmed

Whether the `other` resolver handles Bonventure's select-menu archive (the current-issue link is
a plain `<a href>`, so `page-pdfs` should see it).
