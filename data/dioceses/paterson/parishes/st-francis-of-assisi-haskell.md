---
name: St. Francis of Assisi
website: https://stfrancishaskell.org/
bulletin_provider: other
provider_id: page-pdfs https://stfrancishaskell.org/bulletin
publication: ['ecatholic:11332']
group: ''
evidence:
- url: https://files.ecatholic.com/11332/documents/2026/11/110826.pdf
  seen: 2026-11-04
  quote: 868 RINGWOOD AVENUE
  note: 'Page 1 masthead of the 8 November 2026 issue (6 pages): spaced-letter ''8 6 8  R I N G W O O
    D  A V E N U E  •  H A S K E L L ,  N E W  J E R S E Y  0 7 4 2 0'', ''November 8, 2026 Thirty-second
    Sunday in Ordinary Time'', ''Rev. Greg Golba ---- Pastor''. MASS SCHEDULE: Saturday 5:30 pm; Sunday
    7:30 am, 10:00 am & 12:00 noon. Ad page footer ''003B (PK) - St. Francis, Haskell ... BON VENTURE
    SERVICES, LLC''.'
- url: https://stfrancishaskell.org/bulletin
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site 11332, 'Parish Bulletins'
    page listing PDFs newest first under date labels ('November 8, 2026', 'November 1, 2026', ...), files
    under files.ecatholic.com/11332/documents/<y>/<m>/<MMDDYY>.pdf.
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Francis of Assisi, Haskell (Wanaque) publishes its own weekly bulletin and posts it to its eCatholic site's documents folder. The 8 November 2026 issue (`https://files.ecatholic.com/11332/documents/2026/11/110826.pdf`, 6 pages, read 2026-11-04) has on page 1 "868 RINGWOOD AVENUE • HASKELL, NEW JERSEY 07420" (letter-spaced), "November 8, 2026 Thirty-second Sunday in Ordinary Time" and "Rev. Greg Golba ---- Pastor". Bon Venture prints it (ad footer "003B (PK) - St. Francis, Haskell"), but the parish posts it itself.

## Worship sites

- `st-francis-of-assisi-haskell`: the only church. Page 1's MASS SCHEDULE gives Saturday 5:30 pm; Sunday 7:30 am, 10:00 am & 12:00 noon; page 2's intentions add weekdays 8:00 A.M. No other place is named; the Healing Mass on 14 November and the Mass for Our Country are in the same schedule with no other location.

The finder (directory:11332) and GCatholic (18985) list this one church.

## Website and bulletin provider

`stfrancishaskell.org` is the parish's eCatholic site (id 11332), behind Cloudflare. Its `/bulletin` page (read with visit.py on 2026-11-04) lists PDFs newest first, each labelled with its Sunday date ("November 8, 2026", "November 1, 2026", ...), under `files.ecatholic.com/11332/documents/<y>/<m>/<MMDDYY>.pdf`, not the `bulletins/` archive, so the row uses a page-pdfs recipe on that page. `fetch:check` on 2026-11-04 resolved 'page-pdfs on https://stfrancishaskell.org/bulletin: current' and picked `110826.pdf`, the 8 November 2026 issue (freshness future, age -4 days: next Sunday's issue, the right pick; identity unverified because no expected identity is supplied).

## Not yet confirmed

Nothing open.
