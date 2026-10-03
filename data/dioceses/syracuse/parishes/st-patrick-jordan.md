---
name: St. Patrick Roman Catholic Church
website: https://www.stpatricksjordan.com
bulletin_provider: other
provider_id: page-pdfs https://www.stpatricksjordan.com/bulletin
publication: ['url:https://www.stpatricksjordan.com/bulletin']
group: Rev. Robert Hyde (Camillus, Jordan)
evidence:
- url: https://irp.cdn-website.com/59394cb6/files/uploaded/20260927docx.pdf
  seen: 2026-09-26
  quote: 'Pastor: Rev. Robert Hyde'
  note: 'Page 1 of the 27 September 2026 bulletin: "St. Patrick Roman Catholic Church Jordan, New York
    Weekend Bulletin September 27, 2026", "Address: 28 N. Main Street, P.O. Box 567". Its "AREA WEEKEND
    MASS SCHEDULES" box gives "St. Patrick. Jordan … Vigil Mass Saturday 5:00 pm Sunday 8:00 & 10:00 am"
    followed by St. Joseph (Camillus), St. Mary of the Lake (Skaneateles) and St. Francis Xavier (Marcellus)
    for reference.'
- url: https://www.stpatricksjordan.com/bulletin
  seen: 2026-09-26
  note: The parish's Bulletin page, linking one PDF per week on the site builder's file host (irp.cdn-website.com/59394cb6/...),
    with irregular file names (20260927docx.pdf, St_Patrick_Bulletin_with_Letter_20260920.pdf, 2026-9-13+Bulletin.pdf,
    20260906.pdf ...), weekly through 27 September 2026.
promoted: 2026-09-26
---

## Publisher

St. Patrick's, Jordan publishes its own weekly bulletin on its website. I read the 27 September
2026 issue: page 1 is headed "St. Patrick Roman Catholic Church, Jordan, New York, Weekend
Bulletin", with its own address (28 N. Main Street), office, staff (Pastor: Rev. Robert Hyde) and
its Masses (Saturday vigil 5:00 pm, Sunday 8:00 and 10:00 am; weekday Tuesday and Thursday 9:00am
in the chapel). The "Area Weekend Mass Schedules" and "Daily Masses in Our Area" boxes also list
St. Joseph (Camillus), St. Mary of the Lake (Skaneateles), St. Francis Xavier (Marcellus) and
Holy Family (Fairmount) as a service to readers; those parishes publish their own bulletins and
are not part of this row.

Fr. Hyde is also pastor of St. Joseph's, Camillus, which publishes its own bulletin through
church-bulletin.org. Both are current, so they are two rows in the group "Rev. Robert Hyde
(Camillus, Jordan)".

## Worship sites

One: St. Patrick's, 28 North Main Street (`churches/st-patrick-jordan.md`). The weekday Masses
are in the parish center chapel, which is not modelled separately.

## Website and bulletin provider

stpatricksjordan.com is the parish's own site (a Duda site). `probe url` found its Bulletin page
and the PDFs on irp.cdn-website.com, with no publisher id, so the bulletin is self-hosted: provider
`other`, `publication` the Bulletin page. A test run of the pipeline's `other` fetcher on
2026-09-26 found the 27 September issue (20260927docx.pdf).

Fetch recipe `page-pdfs https://www.stpatricksjordan.com/bulletin`, pinned 2026-10-03: on
the pages recorded 2026-09-27 (`tests/fixtures/fetch/st-patrick-jordan.json.gz`) the
resolver found https://irp.cdn-website.com/59394cb6/files/uploaded/20260927docx.pdf this
way, dated that week.

## Not yet confirmed

Nothing.
