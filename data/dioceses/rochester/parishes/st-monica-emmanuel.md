---
name: St. Monica / Emmanuel Church of the Deaf
website: https://www.stmonicaofrochester.org
bulletin_provider: other
provider_id: ''
publication:
- url:https://www.stmonicaofrochester.org/copy-of-bulletins
group: St. Monica / Immaculate Conception-St. Bridget's cluster
evidence:
- url: https://www.stmonicaofrochester.org/_files/ugd/cea846_00334ad9684947469dd533a9f70fcc50.pdf
  seen: '2026-10-02'
  quote: St. Monica Roman Catholic Church of Rochester
  note: Masthead, page 1 of the 27 September 2026 issue (Wix-hosted PDF, "Sept. 27, 2026" on the bulletin
    page). It names St. Monica and Emmanuel Church of the Deaf only.
- url: https://www.stmonicaofrochester.org/_files/ugd/cea846_00334ad9684947469dd533a9f70fcc50.pdf
  seen: '2026-10-02'
  quote: Weekend Masses Saturday at 4:00 pm Sunday at 10:15am + Livestream
  note: 'Page 1 of the same issue. "Emmanuel Church of the Deaf: Sunday at 11:30 AM" follows; the week
    page lists "11:30 am - ECD Mass, Church", so Emmanuel meets in St. Monica Church.'
- url: https://www.stmonicaofrochester.org/copy-of-bulletins
  seen: '2026-10-02'
  note: Wix "bulletins" page (the slug is a copy of an older page). It lists 2026 issues from "Jan 4,
    2026" to "Oct. 4, 2026", newest after "Sept. 27, 2026". The home page also links /copy-of-2021-bulletins,
    which is the 2024 archive; the 2025 archive is /copy-of-bulletins-1.
- url: https://ps.dor.org/directory/st-monica/
  seen: '2026-10-02'
  quote: 'Sunday: 10:15 AM, 11:30 AM (Emmanuel Church of the Deaf)'
  note: Diocesan directory listing, read 2 October 2026.
promoted: 2026-10-02
---

## Publisher

St. Monica publishes its own weekly bulletin as a PDF on its Wix site. The 27 September 2026 issue's masthead is "St. Monica Roman Catholic Church of Rochester", with Saturday 4:00 pm and Sunday 10:15 am, and "Emmanuel Church of the Deaf: Sunday at 11:30 AM". Emmanuel Church of the Deaf is a community that meets in St. Monica Church (its Mass appears in St. Monica's weekly calendar as "ECD Mass, Church"), so it is not a separate row. The 4 October issue is already posted.

Pastor Fr. Raymond Fleming is also pastor of Immaculate Conception / St. Bridget's, which the directory calls a cluster with St. Monica, and the two share an office (34 Monica Street). Each parish still publishes its own bulletin with its own masthead (this one and `immaculate-conception-st-bridgets`), so they stay separate rows and share a `group`.

## Worship sites

One: `churches/st-monica.md` (831 Genesee Street, at the corner of Monica Street). Emmanuel Church of the Deaf uses the same church. The locator's "Emmanuel Church of the Deaf" entry (`directory:58-emmanuel-church-of-the-deaf`, no address) and the directory's `emmanuel-church-of-the-deaf` entry (34 Monica Street) are linked to that church record.

## Website and bulletin provider

`stmonicaofrochester.org` is alive (200). The bulletins live on three year pages (/copy-of-2021-bulletins is the 2024 one, /copy-of-bulletins the 2026 one, /copy-of-bulletins-1 the 2025 one); only /copy-of-bulletins has the current issues. The fetch's `other` resolver tries several bulletin links in turn and falls back past old archives, so provider `other` with the home page should find it, but the first "bulletins" link on the home page is the 2024 archive. Recorded as `url:` of the 2026 page.

## Not yet confirmed

That the `other` resolver picks the 2026 page rather than the 2024 archive; a fetch run will show it. Revisit after the next fetch.
