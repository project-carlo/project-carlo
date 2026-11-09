---
name: St. Catherine of Genoa
website: https://stcatherineofgenoanyc.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:14415']
group: ''
evidence:
- url: https://stcatherineofgenoanyc.org/bulletins
  seen: 2026-11-09
  quote: August 16, 2026
  note: 'eCatholic (14415) archive rendered in headed Chrome: the newest of the 2026 issues is 16 August
    2026, unchanged since 8 October; nothing for the twelve Sundays since.'
- url: https://files.ecatholic.com/14415/bulletins/20260816.pdf?t=1787172315000
  seen: 2026-11-09
  quote: MASS SCHEDULE - KREYOL/FRENCH
  note: 'Page 1 of the 16 August issue (dated inside 8/19/2026): the parish''s own staff and Mass schedule,
    English Saturday 5:00 PM, Sunday 9:30 AM and 12:30 PM, weekdays 8:00 AM; Kreyol/French Sunday 5:00
    PM.'
- url: https://stcatherineofgenoanyc.org/
  seen: 2026-11-09
  quote: 5:00 PM French /Haitian Creole
  note: 'Home page Mass Times: Saturday 5:00 PM and 7:00 PM Spanish; Sunday 8:00 AM Spanish, 9:30 AM English,
    11:00 AM Spanish, 12:30 PM English, 5:00 PM French/Haitian Creole; Monday-Friday 8:00 AM English and
    7:00 PM Spanish; Saturday 9:00 AM Spanish.'
research:
- method: visit.py (headed Chrome) on stcatherineofgenoanyc.org/bulletins; issues.py ecatholic ecatholic:14415
    over the 12 Sundays to 1 November 2026 (newest 20260816.pdf)
  url: https://stcatherineofgenoanyc.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read the archive; if issues after 16 August 2026 appear and keep coming weekly, set
    bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue dated after 2026-08-16
  revisit_after: 2026-12-15
- method: probe po st-catherine-of-genoa-church-10031 (LPi org 0018000000QxALlAAN exists as a directory
    listing with no issues) and st-catherine-of-genoa-10031 (no org); Discover Mass st-catherine-of-genoa-new-york-ny
    (listing with no bulletins); web search of parishesonline.com, church-bulletin.org and bonventure.net
  url: https://discovermass.com/church/st-catherine-of-genoa-new-york-ny/
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless a publisher listing gains issues
  retry_when: The LPi org or Discover Mass listing shows an issue
- method: 'ParishesOnline organization search by the church''s coordinates (1 mile), then probe po on
    the Catholic orgs at this church: only st-catherine-of-genoa-church-10031 (empty)'
  url: https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=40.8303&longitude=-73.9442&distance=1
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the org lists an issue
  retry_when: probe po on the org returns an issue
bulletin_status: not-found
---

## Publisher

St. Catherine of Genoa (506 West 153rd Street, Hamilton Heights) publishes its own bulletin through its eCatholic site (14415): the 16 August 2026 issue's page 1 carries its own staff and Mass schedule. The archive, read 9 November 2026, still ends at 16 August 2026, with nothing for the twelve Sundays since, and no other channel was found (the LPi org `st-catherine-of-genoa-church-10031` is an empty directory listing; Discover Mass has no bulletins). With no current issue, the row is `no_bulletin` and kept off the site (Settled policy 4); it should go to `ecatholic` once weekly uploads resume.

## Worship sites

One church, St. Catherine of Genoa, 506 West 153rd Street: Saturday 5:00 PM and 7:00 PM (Spanish); Sunday 8:00 AM (Spanish), 9:30 AM (English), 11:00 AM (Spanish), 12:30 PM (English), 5:00 PM (French/Haitian Creole); Monday-Friday 8:00 AM and 7:00 PM; Saturday 9:00 AM (home page, 9 November 2026).

## Website and bulletin provider

`no_bulletin` for now; the website is the eCatholic bulletin archive, which `ecatholic` reads once issues are current.

## Not yet confirmed

Whether the parish has paused the bulletin or only its uploads. The parish's Facebook page was not read.
