---
name: St. Teresa
website: https://stteresany.org/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://stteresany.org/documents/2026/10/Bulletin.pdf', 'ecatholic:6639']
group: ''
evidence:
- url: https://stteresany.org/documents/2026/10/Bulletin.pdf
  seen: 2026-11-08
  quote: CHURCH OF ST. TERESA
  note: 'The whole one-page PDF the site''s ''Bulletins'' menu links: no date; Mass schedule (Saturday
    vigil 5:00 p.m. English; Sunday 10:00 a.m. English, 12:00 p.m. Español; Tuesday-Friday 8:30 a.m. Español;
    First Saturday 8:30 a.m. Bilingual), sacraments, office hours, ''141 Henry Street, New York, NY 10002'',
    Pastor Fr. Edwin Bonifacio.'
- url: https://stteresany.org/bulletins
  seen: 2026-11-08
  quote: February 9, 2025
  note: The eCatholic issue archive (site 6639) still ends at 9 February 2025; the site's navigation 'Bulletins'
    item now links /documents/2026/10/Bulletin.pdf instead.
- url: https://stteresany.org
  seen: 2026-10-08
  quote: |-
    St. Teresa Patronal Mass

    OCTOBER 15:

    7:00 PM Bilingual
  note: Homepage read October 8; weekly schedule Saturday 5 PM, Sunday 10 AM and noon Spanish, Tuesday-Friday
    8:30 AM Spanish.
revisit: Check whether the site's Bulletins link has moved to a newer /documents/<yyyy>/<mm>/ file or
  back to dated eCatholic issues, and that the sheet's Mass schedule still matches the homepage.
revisit_after: 2026-12-08
promoted: 2026-11-09
research:
- method: 'check_fetch on a hypothetical row: provider ecatholic picks files.ecatholic.com/6639/bulletins/20250209.pdf
    (stale); provider other picks /documents/2026/10/Bulletin.pdf (page-pdfs on the homepage)'
  url: https://stteresany.org/
  checked: '2026-11-08'
  outcome: found
bulletin_status: available
---

## Publisher

St. Teresa, 141 Henry Street, publishes no dated weekly issue that can be found now. Its eCatholic archive (https://stteresany.org/bulletins, site 6639) ends at 9 February 2025, then 2017 and 2016. Instead the site's menu item "Bulletins" links https://stteresany.org/documents/2026/10/Bulletin.pdf, uploaded in October 2026: one undated page headed "Church of St. Teresa" with the Mass schedule, sacraments, office hours, the address and the pastor (Fr. Edwin Bonifacio). This row treats that sheet as the parish's bulletin, because it is what the parish publishes under that name and it carries the current schedule. It names only this church.

## Worship sites

One: St. Teresa, 141 Henry Street (`churches/st-teresa-new-york-city.md`). The sheet gives Saturday vigil 5:00 p.m. English; Sunday 10:00 a.m. English and 12:00 p.m. Español; Tuesday-Friday 8:30 a.m. Español; First Saturday 8:30 a.m. bilingual; Friday adoration 9-10 a.m. The homepage (October 8) agreed and announced a patronal Mass on October 15.

## Website and bulletin provider

`bulletin_provider` is `other`, not `ecatholic`: as `ecatholic` the resolver takes the February 2025 archive issue. As `other` it reads the homepage and picked the October 2026 sheet (`page-pdfs on https://stteresany.org/: first-listed`, November 8), and the recipe `page-pdfs` is pinned. The sheet has no date, so fetch:check can't judge freshness; it is current only in the sense that the parish links it now.

## Not yet confirmed

Whether the sheet is replaced weekly or monthly (the file name is fixed, the folder is the upload month), and whether the parish still prints a dated weekly bulletin it does not post.
