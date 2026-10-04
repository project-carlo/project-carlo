---
name: Holy Trinity Church
website: https://holytrinityweb.org
bulletin_provider: other
provider_id: page-pdfs https://holytrinityweb.org/media
publication: ['url:https://holytrinityweb.org/media']
group: ''
evidence:
- url: https://holytrinityweb.org/wp-content/uploads/2026/09/20260927B.pdf
  seen: 2026-10-02
  quote: Page Two Holy Trinity Church, 1460 Ridge Road, Webster, New York September 27, 2026
  note: Page 2 header of the 27 September 2026 issue (6 pages, text). Holy Trinity alone.
- url: https://holytrinityweb.org/wp-content/uploads/2026/09/20260927B.pdf
  seen: 2026-10-02
  quote: 'WEEKEND MASS TIMES: Saturday (vigil) 4:30 p.m. Sunday 8:30 a.m. and 10:30 a.m.'
  note: Page 2 of the same issue.
- url: https://holytrinityweb.org/media/
  seen: 2026-10-02
  quote: The church’s weekly bulletin in pdf format.
  note: 'The "Weekly Bulletins" list on the Media page: one PDF per Sunday, newest "September 27, 2026"
    when read on 2 October (the 4 October issue was not posted yet; /2026/10/20261004B.pdf and /2026/09/20261004B.pdf
    both 404).'
- url: http://holytrinityweb.com
  seen: 2026-10-02
  note: 'The diocese locator and the Directory of Parishes still link holytrinityweb.com; it does not
    resolve (probe url: DEAD-DNS, checked with and without www.). holytrinityweb.org is the live site.'
promoted: 2026-10-02
---

## Publisher

Holy Trinity publishes its own weekly bulletin as a PDF on its own website. The 27 September
2026 issue (`/wp-content/uploads/2026/09/20260927B.pdf`) is headed "Holy Trinity Church, 1460
Ridge Road, Webster, New York" on page 2 and lists weekend Masses Saturday 4:30 pm and Sunday
8:30 and 10:30 am. It names no other church. The diocese's Directory of Parishes and its
Parish Locator both give Holy Trinity as a one-church parish with no group.

## Worship sites

One: Holy Trinity at 1460 Ridge Road (`holy-trinity`). Nothing else is listed for this parish
in the locator, the Directory of Parishes or GCatholic.

## Website and bulletin provider

`holytrinityweb.org` (WordPress). Its home page links "Bulletin" to `/media`, which lists the
PDFs, so provider `other` with the home page as website. The `publication` is the Media
page. The bulletin PDFs are named `YYYYMMDDB.pdf`, which looks like an LPi file name, but
they are hosted on the parish's own uploads folder, not on ParishesOnline (no container
id was found). The old domain `holytrinityweb.com` that the diocese lists is dead.

Fetch recipe `page-pdfs https://holytrinityweb.org/media`, pinned 2026-10-03: on the pages recorded in `tests/fixtures/fetch/holy-trinity-webster.json.gz` the resolver found https://holytrinityweb.org/wp-content/uploads/2026/09/20260927B.pdf this way, dated that week.

## Not yet confirmed

The newest issue on the page was 27 September; the 4 October issue was not posted when read.
`fetch-check` could not be run here (no browser binary for the pipeline's own launcher), so
the resolver was not exercised against this site.
