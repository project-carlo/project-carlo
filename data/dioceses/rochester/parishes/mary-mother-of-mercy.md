---
name: The Parish of Mary, Mother of Mercy
website: https://www.marymotherofmercy.com
bulletin_provider: other
provider_id: page-pdfs https://www.marymotherofmercy.com/mass/bulletins/
publication: ['url:https://www.marymotherofmercy.com/mass/bulletins/']
group: Mary, Mother of Mercy
evidence:
- url: https://www.marymotherofmercy.com/wp-content/uploads/Bulletin-September-27-2026.pdf
  seen: 2026-10-02
  quote: 'St. Francis Solanus 3660 Orchard St. Interlaken, NY Weekend Mass: Saturday, 4:00 p.m.'
  note: '27 Sep 2026 issue, page 1: the page-1 panels give each church and its Mass times (the 4 Oct issue
    was not posted on 2 Oct).'
- url: https://www.marymotherofmercy.com/wp-content/uploads/Bulletin-September-27-2026.pdf
  seen: 2026-10-02
  quote: 'Parish Center : St. Francis Solanus P.O. Box 403 Interlaken, NY 14847'
  note: 'Page 1: one parish centre; pastor Rev. Robert Lasrado, OFM Cap.'
- url: https://www.marymotherofmercy.com/mass/bulletins/
  seen: 2026-10-02
  note: 'Parish bulletin page (visit.py, 2 Oct 2026): one PDF per Sunday, newest "September 27, 2026",
    back to March 2026; no ParishesOnline id, so self-hosted.'
- url: https://ps.dor.org/directory/mary-mother-of-mercy/
  seen: 2026-10-02
  quote: St. James the Apostle , 17 Whig St, Trumansburg, NY Holy Cross , 7231 Main Street, Ovid, N.Y.
    St. Francis Solanus , 3660 Orchard St., Interlaken, N.Y.
  note: 'Diocesan directory listing: the same three churches.'
promoted: 2026-10-02
---

## Publisher

The Parish of Mary, Mother of Mercy (Interlaken, Ovid, Trumansburg; a Capuchin-served parish) publishes one weekly PDF bulletin on its own site. The 27 September 2026 issue's first page has a panel for each of St. Francis Solanus (Interlaken), St. James the Apostle (Trumansburg) and Holy Cross (Ovid) with address and Mass times, and the parish centre at Interlaken. One bulletin, one row; the Locator groups the same churches under "Mary, Mother of Mercy".

## Worship sites

St. Francis Solanus (Sat 4:00 p.m.; weekday Mass Tue-Fri 8:30), St. James the Apostle (Sun 9:00 a.m.; Monday communion service), Holy Cross (Sun 10:30 a.m.). The Locator lists St. James twice: once at Trumansburg with an address and once (`368-st-james-the-apostle`) at "Interlaken" with no address and the same 9 am Sunday Mass. That second entry is a duplicate of the Trumansburg church and is linked to `st-james-apostle`.

## Website and bulletin provider

`website` https://www.marymotherofmercy.com links `/mass/bulletins/`, a WordPress page listing every PDF. Provider `other`, no provider_id. The publication is that page. No change to the live row.

Fetch recipe `page-pdfs https://www.marymotherofmercy.com/mass/bulletins/`, pinned 2026-10-03: on the pages recorded in `tests/fixtures/fetch/mary-mother-of-mercy.json.gz` the resolver found https://www.marymotherofmercy.com/wp-content/uploads/Bulletin-September-27-2026.pdf this way, dated that week.

## Not yet confirmed

Nothing. The 4 October issue was not yet posted on 2 October (the page runs one week behind the Sunday).
