---
name: St. Rose of Lima
website: https://stroseoflimaparish.org/bulletin-archives
bulletin_provider: other
provider_id: page-pdfs https://stroseoflimaparish.org/bulletin-archives
publication: ['url:https://stroseoflimaparish.org/bulletin-archives']
group: ''
evidence:
- url: https://stroseoflimaparish.org/wp-content/uploads/2026/11/RoseMass11-8R.pdf
  seen: 2026-11-13
  quote: 2 BAYVIEW AVENUE MASSAPEQUA NY 11758
  note: 'Page 1 masthead of the Sunday, November 8, 2026 bulletin names St. Rose of Lima alone, with its
    Mass schedule: Saturday Vigil 5:15 pm; Sunday 8:00 am, 10:00 am, 12:00 pm, 5:15 pm; weekdays 7:30
    and 9:00 am; Monday 7:30 pm; Saturday 8:00 am.'
- url: https://stroseoflimaparish.org/bulletin-archives
  seen: 2026-11-13
  note: 'WordPress bulletin archive read with visit.py: self-hosted PDFs under /wp-content/uploads/, e.g.
    RoseMass11-8R.pdf, 11-1-26SRpdf.pdf, 10-18-26SRpdf.pdf. No printer id on the page.'
bulletin_status: available
---

## Publisher

St. Rose of Lima, 2 Bayview Avenue, Massapequa publishes its own weekly bulletin. The Sunday, November 8, 2026 issue (`https://stroseoflimaparish.org/wp-content/uploads/2026/11/RoseMass11-8R.pdf`, read 2026-11-13) has a page-1 masthead "St. Rose of Lima Catholic Church Bulletin, 2 Bayview Avenue Massapequa NY 11758" with one Mass schedule: Saturday Vigil 5:15 pm; Sunday 8:00 am, 10:00 am, 12:00 pm and 5:15 pm; weekdays 7:30 and 9:00 am; Monday 7:30 pm; Saturday 8:00 am. The 1 November issue has the same masthead and schedule.

## Worship sites

One: the church at 2 Bayview Avenue (`st-rose-of-lima-massapequa-church`). The diocesan locator (directory:1), GCatholic (16880) and the diocese's Mass-times page list only this building, and the bulletin's schedule names no other place. The parish school at 4704 Merrick Road (page 2) is listed for its office, not for Mass.

## Website and bulletin provider

The locator links stroseoflimaparish.org and the Mass-times page srolchurch.org; the latter redirects to https://stroseoflimaparish.org/ (visit.py, 2026-11-13). Its `/bulletin-archives` page lists self-hosted PDFs with irregular file names (`RoseMass11-8R.pdf`, `11-1-26SRpdf.pdf`). `fetch:check` on 2026-11-13 picked the 8 November issue ("Sunday, November 8, 2026" in its text) with page-pdfs on that page, so the row is `other` with that recipe.

## Not yet confirmed

Nothing. File names vary from week to week; if `fetch` later picks an old issue, pin a newer page or a filename filter.
