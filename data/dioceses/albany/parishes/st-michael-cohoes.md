---
name: St. Michael's Roman Catholic Church
website: https://www.stmichaelsofcohoes.org/bulletins.html
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.stmichaelsofcohoes.org/bulletins.html']
group: 'Cohoes (one pastor: Holy Trinity, St. Michael)'
evidence:
- url: https://www.stmichaelsofcohoes.org/uploads/1/3/8/9/138944200/bulletin-2026-09-27.pdf
  seen: 2026-09-28
  quote: ST. MICHAEL’S ROMAN CATHOLIC CHURCH 20 Page Avenue~Cohoes, N.Y. 12047
  note: Masthead, page 1 of the 27 September 2026 issue, self-hosted on the parish's Weebly site.
- url: https://www.stmichaelsofcohoes.org/uploads/1/3/8/9/138944200/bulletin-2026-09-27.pdf
  seen: 2026-09-28
  quote: Rev. Kyle Gorenski Pastor
  note: 'Same page; its staff box also gives "Parish Office: (518) 237-5151" and "Bulletin: bulletin@stmichaelsofcohoes.org".'
- url: https://www.stmichaelsofcohoes.org/bulletins.html
  seen: 2026-09-28
  quote: 2026 September 27, 2026 September 20, 2026
  note: The site's Bulletins page, which links one PDF per Sunday (bulletin-YYYY-MM-DD.pdf), from 2023
    through 27 September 2026 (read with curl, 2026-09-28).
promoted: 2026-09-28
---

## Publisher

St. Michael's publishes its own weekly bulletin as PDFs on its own site. The 27 September
2026 issue's masthead is "ST. MICHAEL'S ROMAN CATHOLIC CHURCH, 20 Page Avenue~Cohoes, N.Y.
12047", with Rev. Kyle Gorenski as pastor, its own parish office, trustees and a bulletin
e-mail address.

Fr. Gorenski is also pastor of Holy Trinity, Cohoes, and this bulletin prints the same
joint Cohoes schedule as Holy Trinity's. But the two parishes each publish a bulletin
(Holy Trinity's is ParishesOnline container 03/0435, masthead Holy Trinity alone), both
current, so they are two rows sharing a `group`.

## Worship sites

One: `st-michael-cohoes`.

## Website and bulletin provider

stmichaelsofcohoes.org is the site the diocese and GCatholic both give. Its Bulletins page
(bulletins.html) links every issue as `uploads/1/3/8/9/138944200/bulletin-YYYY-MM-DD.pdf`,
dated by the Sunday; the home page links the current one. No publisher id: self-hosted,
`other`, with the Bulletins page as the publication.

Fetch recipe `page-pdfs`, pinned 2026-10-03: on the pages recorded 2026-10-03
(`tests/fixtures/fetch/st-michael-cohoes.json.gz`) the resolver found
https://www.stmichaelsofcohoes.org/uploads/1/3/8/9/138944200/bulletin-2026-10-04.pdf this
way, dated that week.

## Not yet confirmed

Nothing.
