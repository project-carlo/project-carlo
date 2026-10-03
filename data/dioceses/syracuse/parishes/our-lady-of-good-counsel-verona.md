---
name: Our Lady of Good Counsel
website: https://olgcc.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://olgcc.org/bulletin/']
group: ''
evidence:
- url: https://olgcc.org/wp-content/uploads/simple-file-list/27-September-2026.pdf
  seen: 2026-09-26
  quote: 'Sunday  Mass:  Anticipated  Sat.4PM/Sun.  8AM  Ancient  Rite  Latin  Mass  Sunday  10AM   Mass  with  Choir'
  note: '27 September 2026 issue, page 1: the week''s Masses, all at the one church; the rectory is at
    5259 Beacon Light Rd., Verona (page 2).'
- url: https://olgcc.org/bulletin/
  seen: 2026-09-26
  quote: Weekly Bulletin - Our Lady of Good Counsel
  note: The parish's bulletin page (WordPress Simple File List); the current file is wp-content/uploads/simple-file-list/27-September-2026.pdf,
    with Current-Year and Past-Years folders.
- url: https://www.syracusediocese.org/our-lady-of-good-counsel-verona
  seen: 2026-09-26
  quote: Our Lady of Good Counsel - Verona
  note: 'Diocese''s page: physical address 5652 East Main Street, website olgcc.org, one pastor, no other
    worship site. behind Cloudflare; read in a browser (parish-site-access visit.py). '
promoted: 2026-09-26
---

## Publisher

Our Lady of Good Counsel, Verona, is a single parish that publishes its own weekly bulletin as
PDFs on its site. I read the 27 September 2026 issue: page 1 gives "Sunday Mass: Anticipated
Sat. 4PM / Sun. 8AM Ancient Rite Latin Mass / Sunday 10AM Mass with Choir" and the week's
Masses, all at this church; nothing in it serves another parish or worship site.

## Worship sites

One: `churches/our-lady-of-good-counsel-verona.md`. The diocese's page lists no other site.

## Website and bulletin provider

Self-hosted on https://olgcc.org/bulletin/ (a Simple File List folder of dated PDFs), so that
page is `website` and the `url:` publication, and the provider is `other`.

Fetch recipe `page-pdfs`, pinned 2026-10-03: on the pages recorded 2026-09-27
(`tests/fixtures/fetch/our-lady-of-good-counsel-verona.json.gz`) the resolver found
https://olgcc.org/wp-content/uploads/simple-file-list/27-September-2026.pdf this way,
dated that week.

## Not yet confirmed

Nothing.
