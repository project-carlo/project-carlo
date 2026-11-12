---
name: St. Joseph Parish
website: https://www.saintjosephchurch.us/weekly-bulletins/
bulletin_provider: other
provider_id: page-pdfs https://www.saintjosephchurch.us/weekly-bulletins/
publication: ['url:https://www.saintjosephchurch.us/weekly-bulletins/']
group: ''
evidence:
- url: https://www.saintjosephchurch.us/weekly-bulletins/
  seen: 2026-10-29
  quote: 'List of the Weekly Bulletins:'
  note: 'Parish site (WordPress, New Concepts Online) Weekly Bulletins page: dated list newest first,
    October 25, 2026 down to January 5, 2025, each linking wp-content/uploads/<yyyy>/<mm>/bulletin-<yyyy-mm-dd>.pdf
    (the hrefs were read in the page source, so not quotable).'
- url: https://www.saintjosephchurch.us/wp-content/uploads/2026/10/bulletin-2026-10-25.pdf
  seen: 2026-10-29
  quote: 1795 Columbia Avenue, Warrington, PA 18976
  note: 25 October 2026 issue, 8 pages, text layer. Page 1 masthead 'Saint Joseph Church', Founded June
    16, 1922, Pastor Rev. Michael J. Pawelko, Mass box 'Daily Mass (Mon.-Sat.) 8:00 a.m.; Saturday Vigil
    Mass 4:00 p.m.; Sunday Masses 7:30 a.m., 9:30 a.m. & 11:30 a.m.'. Names this parish alone.
- url: https://www.saintjosephchurch.us/wp-content/uploads/2026/10/bulletin-2026-10-25.pdf
  seen: 2026-10-29
  quote: View this bulletin online at www.DiscoverMass.com
  note: 'Page 2 footer. The parish''s own archive carries the current issue (see the playbook: a Discover
    Mass footer does not make it the publisher).'
- url: https://archphila.org/parish/st-joseph-warrington/
  seen: 2026-10-29
  quote: Rev. Michael J. Pawelko
  note: 'Directory: pastor; rectory 1795 Columbia Ave., Warrington 18976-2596; page updated 2 years ago,
    so its Mass times (Saturday 5:30 PM, Sunday 7, 8:30, 10, 11:30 AM) are stale against the bulletin.'
promoted: 2026-10-29
research:
- method: church-bulletin.org listing scan (jppc_scan ids 1-1300) and directory match by name and town;
    no Warrington St. Joseph listing; probe url on the parish site found no John Patrick or other printer
    link
  url: https://www.saintjosephchurch.us/
  checked: '2026-10-29'
  outcome: not-found
  next_action: None while the parish's own archive stays current; if it stops, look for a John Patrick
    listing again
  retry_when: The Weekly Bulletins page stops adding issues
bulletin_status: available
---

## Publisher

St. Joseph Parish, Warrington (Rev. Michael J. Pawelko, Pastor) has no John Patrick listing. It posts its own bulletin on a WordPress page, https://www.saintjosephchurch.us/weekly-bulletins/, which lists every Sunday newest first (25 October 2026 down to 5 January 2025) as `wp-content/uploads/<yyyy>/<mm>/bulletin-<yyyy-mm-dd>.pdf`. The row is `other`, `page-pdfs` on that page. The 25 October 2026 issue has a text layer; its masthead and Mass box name this parish alone.

## Worship sites

One church, St. Joseph, 1795 Columbia Avenue. The Mass box lists every Mass without a mission or chapel.

## Website and bulletin provider

The directory's website `http://www.saintjosephchurch.us` is the parish's own site. The bulletin footer says 'View this bulletin online at www.DiscoverMass.com'; that does not make Discover Mass the publisher, as the parish's own archive is current. St. Robert Bellarmine, also in Warrington, publishes separately (own row, John Patrick 122); the two parishes share a school (St. Joseph/St. Robert School, 850 Euclid Avenue) but not a bulletin.

## Fetch check

`fetch:check` (2026-10-29) with page-pdfs on the Weekly Bulletins page picked `bulletin-2026-10-25.pdf`: transport ok, PDF, fresh (8-page issue, date read from the masthead); identity `unverified` because the check is given no expected identity (the masthead was read by hand above). It printed no `recipe` line, as the pinned `provider_id` already holds it.

## Not yet confirmed

Pages 3-8 were not read.
