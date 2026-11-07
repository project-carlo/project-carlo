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
- url: https://www.stpaulchurchde.org/bulletins
  seen: 2026-11-07
  note: 'Browser read (visit.py): the newest file is still files.ecatholic.com/5218/bulletins/20260802.pdf.
    Its upload stamp (?t=1785698710000) and those of the June and July files (?t=17856985...) are all
    2 August 2026: the parish uploads bulletins in batches. The home page''s ''Bulletins'' button links
    the same 2 August issue (stpaulchurchde.org/documents/2026/8/11222_StPaul_WilmingtonDE_8.2.26.pdf);
    its events calendar lists the Wednesday and Friday 5:00 PM Masses and the Tuesday 24 November Mass
    for the sick, as the August bulletin gives them.'
- url: https://discovermass.com/church/st-paul-wilmington-de/
  seen: 2026-11-07
  quote: There are currently no bulletins available for St. Paul.
  note: Discover Mass lists the church (1010 W 4th St.) with Mass times matching the August bulletin,
    but no bulletins.
revisit: Re-read stpaulchurchde.org/bulletins for an issue after 2 August 2026 and rerun fetch:check for
  this parish.
revisit_after: 2026-12-07
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
- method: 'Browser read of stpaulchurchde.org home, /bulletins and /documents-documentos; issues.py ecatholic
    5218 for the 14 Sundays 2026-08-09 to 2026-11-08 (all 403); Discover Mass church page; the parish
    Facebook page (facebook.com/StPaulWilmington: ''This page isn''t available right now'' without a login)'
  url: https://www.stpaulchurchde.org/bulletins
  checked: '2026-11-07'
  outcome: not-found
  next_action: Re-read the bulletins page and run fetch:check --parish st-paul-wilmington; the parish
    uploads in batches (June to August all on 2 August), so a new batch would bring the row current with
    no change to its records
  retry_when: The site lists a bulletin dated after 2 August 2026, or another channel for St. Paul's bulletin
    turns up
  revisit_after: 2026-12-07
---

## Publisher

St. Paul, Wilmington (1010 W. 4th St., Spanish-language Masses) publishes its own bulletin on its eCatholic site (id 5218), at files.ecatholic.com/5218/bulletins/<YYYYMMDD>.pdf. The 2 August 2026 issue names St. Paul alone, with its own pastor, priest in residence and Mass schedule.

## Worship sites

One church, 1010 W. 4th St. (Wednesday and Friday Spanish Masses are in its chapel, inside the same address). See the church record.

## Website and bulletin provider

`ecatholic`, website https://www.stpaulchurchde.org/ (the eCatholic-hosted site; it answers curl with 403, the browser reads it).

## Fetch check

`pnpm fetch:check --diocese wilmington` (hand refresh, 2026-11-07; output in `scratch/wilmington-map-1/refresh/fetch_check.out`): picked files.ecatholic.com/5218/bulletins/20260802.pdf again; transport ok, document type PDF, issue date 2026-08-02 inferred from the file name, freshness **stale** (97 days), overall `failed`. The first check (2026-10-27) gave the same pick at 86 days. The pick is the newest file the site lists, so the staleness is the source's, not a wrong pick, and `fetch` collects this bulletin: this is not a `fetch_gap`. Identity is 'unverified' to the tool; the cover read above names St. Paul.

## Not yet confirmed

**The newest bulletin is dated 2 August 2026, 97 days old on 7 November.** No other channel was found (2026-11-07): the site's /bulletins and documents pages, its home-page Bulletins button, eCatholic's file host for every Sunday since, Discover Mass (listed, no bulletins) and Facebook (unreadable without a login). The upload stamps show June to August were all posted on 2 August, so the parish posts in batches and may post again. The row stays live as `ecatholic`: the August Mass schedule still matches the site's events calendar, Discover Mass and the diocese map (Sun 9:00 English; 11:00, 1:00, 3:00 Spanish; Wed and Fri 5:00 Spanish), and the weekly run reports the parish as stale until a newer issue arrives. See `research`.
