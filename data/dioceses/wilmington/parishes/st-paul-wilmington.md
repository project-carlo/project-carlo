---
name: St. Paul
website: https://www.stpaulchurchde.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:5218']
group: City Deanery
evidence:
- url: https://files.ecatholic.com/5218/bulletins/20260802.pdf
  seen: 2026-10-27
  quote: Rev. John E. Olson, Pastor
  note: 'Page 1 of the 2 August 2026 issue (7 pages, Microsoft Publisher; the newest file on the site):
    ''The Catholic Community of Saint Paul / LA IGLESIA CATÓLICA DE SAN PABLO'', 1010 West Fourth Street,
    Wilmington, DE 19805; Rev. Anthony M. Pileggi, priest in residence; Felipe Almendarez, deacon. Page
    2 Mass schedule: Sundays 9:00 a.m. English (Church), 11:00 a.m., 1:00 p.m. and 3:00 p.m. Spanish (Church);
    Wednesday and Friday 5:00 p.m. Spanish (Chapel); Mass for the Sick last Tuesday 5:00 p.m. (Chapel).
    Names this parish alone.'
- url: https://www.stpaulchurchde.org/bulletins
  seen: 2026-10-27
  note: 'Browser read (probe url gets HTTP 403): title ''Bulletin'', ecatholic:5218. The listing''s newest
    file is files.ecatholic.com/5218/bulletins/20260802.pdf, then 20260726, 20260719 ... back to 20260426.
    Nothing after 2 August 2026 is listed. `issues.py ecatholic ecatholic:5218` got 403 for 25 October,
    18 October, 11 October and 1 November.'
promoted: 2026-10-27
research:
- method: Browser read of stpaulchurchde.org/bulletins and home page; issues.py ecatholic for the 2026-10-11
    to 2026-11-01 Sundays
  url: https://www.stpaulchurchde.org/bulletins
  checked: '2026-10-27'
  outcome: not-found
  next_action: Re-read the bulletins page; if it still ends at 2 August 2026, look for the current bulletin
    on Facebook (the site links one) or another publisher
  retry_when: The site posts a bulletin dated after 2 August 2026, or the owner names another source
  revisit_after: 2026-11-17
---

## Publisher

St. Paul, Wilmington (1010 W. 4th St., Spanish-language Masses) publishes its own bulletin on its eCatholic site (id 5218), at files.ecatholic.com/5218/bulletins/<YYYYMMDD>.pdf. The 2 August 2026 issue names St. Paul alone, with its own pastor, priest in residence and Mass schedule.

## Worship sites

One church, 1010 W. 4th St. (Wednesday and Friday Spanish Masses are in its chapel, inside the same address). See the church record.

## Website and bulletin provider

`ecatholic`, website https://www.stpaulchurchde.org/ (the eCatholic-hosted site; it answers curl with 403, the browser reads it).

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-paul-wilmington` (2026-10-27): picked files.ecatholic.com/5218/bulletins/20260802.pdf; transport ok, document type PDF, issue date 2026-08-02 inferred from the file name, freshness **stale** (86 days), overall `failed`. The pick is the newest file the site lists, so the staleness is the source's, not a wrong pick. Identity is 'unverified' to the tool; the cover read above names St. Paul.

## Not yet confirmed

**The newest bulletin on the site is dated 2 August 2026, almost three months old on 27 October.** Whether the parish stopped uploading or publishes elsewhere is unknown. The diocese map's Mass times match the August schedule (Sun 9:00 English; 11:00, 1:00, 3:00 Spanish; Wed and Fri 5:00 Spanish), so the church is open. See `research`.
