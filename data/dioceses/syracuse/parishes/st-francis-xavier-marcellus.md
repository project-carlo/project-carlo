---
name: St. Francis Xavier Church
website: https://sfxmarcellus.com
bulletin_provider: other
provider_id: page-pdfs https://sfxmarcellus.com/weekly-bulletins/
publication: ['url:https://sfxmarcellus.com/weekly-bulletins/']
group: ''
evidence:
- url: https://sfxmarcellus.com/wp-content/uploads/Bulletin-9-27-2026-2-combined.pdf
  seen: 2026-09-26
  quote: Sunday Masses ...... 8:30 am & 10:45 am
  note: 'Page 1 of the 27 September 2026 bulletin: "SAINT FRANCIS XAVIER CHURCH MARCELLUS, NEW YORK 13108
    FOUNDED 1873", "Saturday Evening Vigil ...............4:30 pm", daily Mass Monday, Thursday, Friday
    6:45 am and Tuesday 6:00pm, "1 West Main St. PO Box 177", website www.sfxmarcellus.com.'
- url: https://sfxmarcellus.com/weekly-bulletins/
  seen: 2026-09-26
  note: The parish's Weekly Bulletins page, linking one PDF per Sunday in wp-content/uploads from 2023
    through Bulletin-9-27-2026-2-combined.pdf.
promoted: 2026-09-26
---

## Publisher

St. Francis Xavier, Marcellus publishes its own weekly bulletin on its website. I read the
27 September 2026 issue: page 1 is "Saint Francis Xavier Church, Marcellus, New York 13108,
Founded 1873", with its own Masses (Saturday vigil 4:30 pm; Sunday 8:30 am and 10:45 am; daily
Monday, Thursday and Friday 6:45 am, Tuesday 6:00 pm), office at 1 West Main St. and its website.
Page 2's intentions cover only this church ("A Note from Fr. Dan"). The diocese's finder and list
show it alone, in no grouping.

## Worship sites

One: St. Francis Xavier, 1 West Main Street (`churches/st-francis-xavier-marcellus.md`).

## Website and bulletin provider

sfxmarcellus.com is the parish's own WordPress site. `probe url` found its Weekly Bulletins page,
which lists dated PDFs in wp-content/uploads, and no publisher id: provider `other`,
`publication` that page. A test run of the pipeline's `other` fetcher on 2026-09-26 found the
27 September issue. GCatholic's website for the parish (stfrancisxavier.webs.com) is an old one
and was not used.

Fetch recipe `page-pdfs https://sfxmarcellus.com/weekly-bulletins/`, pinned 2026-10-03: on
the pages recorded 2026-09-27 (`tests/fixtures/fetch/st-francis-xavier-marcellus.json.gz`)
the resolver found
https://sfxmarcellus.com/wp-content/uploads/Bulletin-9-27-2026-2-combined.pdf this way,
dated that week.

## Not yet confirmed

Nothing.
