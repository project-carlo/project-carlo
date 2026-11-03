---
name: St. Ann, Hoboken
website: https://stannhoboken.com/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:24244', 'discovermass:st-ann-hoboken-nj']
group: ''
evidence:
- url: https://files.ecatholic.com/24244/bulletins/20261101.pdf
  seen: 2026-11-03
  quote: Served by Capuchin Franciscan Friars
  note: 1 November 2026 issue (8 pages, text layer). Page 2 'November 1st, 2026 - Solemnity of All Saints',
    'View this bulletin online at www.DiscoverMass.com'. Page 6 masthead block 'Saint Ann Catholic Church',
    Parish Office 704 Jefferson Street Hoboken NJ 07030, Pastor Fr Martin Schratz OFM Cap; Mass Schedule
    Saturday 5:00pm Vigil, Sunday 8:00am, 10:30am*, 12:00pm, 7:00pm, Monday-Friday 7:00am, Saturday 9:00am,
    Wednesday 7:00pm Mass with novena. Page 8 '©2026 Diocesan View Our Parish Supporters at www.DiscoverMass.com'.
- url: https://stannhoboken.com/bulletins
  seen: 2026-11-03
  note: 'eCatholic site (probe get answers 403; read with visit.py): bulletins page links files.ecatholic.com/24244/bulletins/20261101.pdf,
    20261025, 20261018 ... weekly back through August 2026.'
- url: https://discovermass.com/church/st-ann-hoboken-nj/
  seen: 2026-11-03
  note: Discover Mass page 'St. Ann', 704 Jefferson Street, Hoboken, NJ 07030; issues.py reads its latest
    issue as 2026-11-01, 8 pages, page 1 text identical to the eCatholic copy ('NOVEMBER 1, 2026').
bulletin_status: available
---

## Publisher

Diocesan prints St. Ann's bulletin. The parish posts each issue on its eCatholic site (id 24244), and Discover Mass carries it too (`st-ann-hoboken-nj`). I read the 1 November 2026 issue from files.ecatholic.com. Page 6 masthead: "Saint Ann Catholic Church, A Roman Catholic Community, Served by Capuchin Franciscan Friars, Parish Office 704 Jefferson Street Hoboken NJ 07030", with Fr Martin Schratz OFM Cap as pastor and one Mass schedule. Page 8: "©2026 Diocesan". The Discover Mass copy of 1 November has the same 8 pages and the same page 1, so it is one bulletin, and both ids are recorded.

## Worship sites

- St. Ann, 704 Jefferson Street (`st-ann-hoboken`): Saturday 5:00pm vigil; Sunday 8:00am, 10:30am, 12:00pm, 7:00pm; Monday–Friday 7:00am; Saturday 9:00am; Wednesday 7:00pm Mass with the St. Ann novena.

The bulletin's schedule names one church. The directory (67) and GCatholic (18428) list only this church.

## Website and bulletin provider

The directory's https://stannhoboken.com/ is the parish's eCatholic site. Its /bulletins page posts the current issue under files.ecatholic.com/24244/bulletins/, so the provider is `ecatholic`. The site answers `probe get` with 403 (Cloudflare); `visit.py` loads it. Discover Mass caps downloads per IP per day in other dioceses, so I chose eCatholic as the collector rather than Discover Mass. GCatholic's website, st-annchurch.com, was not checked.

Fetch check (2026-11-03, headed): resolved the latest bulletin link on the eCatholic site; transport ok, PDF, picked files.ecatholic.com/24244/bulletins/20261101.pdf, the issue read above (date observed 2026-11-01); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied.

## Not yet confirmed

Nothing open.
