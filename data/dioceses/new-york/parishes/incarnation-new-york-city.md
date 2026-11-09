---
name: Incarnation
website: https://incarnationnyc.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:6897']
group: ''
evidence:
- url: https://incarnationnyc.com/
  seen: 2026-11-09
  quote: SUNDAY, JUNE 15, 2025
  note: Home page BULLETIN list, rendered in headed Chrome (plain fetches get a Cloudflare 403). Its newest
    entry is 15 June 2025, a file under files.ecatholic.com/6897/documents/2025/7/; the list runs January-June
    2025 and nothing later is linked.
- url: https://incarnationnyc.com/
  seen: 2026-11-09
  quote: 10:30 AM Spanish Español (abajo)
  note: 'Same page, current Mass schedule: Saturday 5:30 PM English and 7:00 PM Spanish; Sunday 9:00 AM
    Spanish, 10:30 AM English and Spanish (lower church), 12:00 PM Spanish, 1:30 PM English and Spanish
    (lower church); weekdays 12:00 PM and 7:00 PM Spanish. It also lists All Saints Masses for 31 October-1
    November 2026, so the schedule is maintained.'
research:
- method: visit.py (headed Chrome) on incarnationnyc.com home page, which carries the bulletin list
  url: https://incarnationnyc.com/
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read the home page BULLETIN list; if an issue newer than 15 June 2025 appears, decide
    a provider (eCatholic documents uploads are read by `other` page-pdfs) and run fetch:check
  retry_when: The home page lists an issue dated after 15 June 2025
  revisit_after: 2027-02-01
- method: issues.py ecatholic ecatholic:6897 over the 12 Sundays to 1 November 2026 (bulletins/YYYYMMDD.pdf
    paths)
  url: https://files.ecatholic.com/6897/bulletins/20261101.pdf
  checked: '2026-10-31'
  outcome: not-found
  next_action: None; the parish uploads to documents/, not the bulletin module
  retry_when: The site starts using the eCatholic bulletin module
- method: probe po incarnation-church-10033 (LPi org 0018000000QxAHxAAN exists as a directory listing
    with no issues); probe po incarnation-10033 and church-of-the-incarnation-10033 (no org); Discover
    Mass incarnation-new-york-ny and church-of-the-incarnation-new-york-ny (no listing); web search of
    parishesonline.com, discovermass.com, church-bulletin.org and bonventure.net
  url: https://parishesonline.com/organization/incarnation-church-10033
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the parish site links another publisher
  retry_when: The parish site or the LPi org lists an issue
- method: 'ParishesOnline organization search by the church''s coordinates (1 mile), then probe po on
    the Catholic orgs at this church: only incarnation-church-10033 (empty)'
  url: https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=40.8451875&longitude=-73.9365625&distance=1
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the org lists an issue
  retry_when: probe po on the org returns an issue
bulletin_status: not-found
---

## Publisher

Incarnation (1290 St. Nicholas Avenue, Washington Heights) posts its bulletin as PDF uploads on its own eCatholic site (6897), listed on the home page. Read 9 November 2026 in headed Chrome, the newest listed issue is Sunday 15 June 2025 and the list runs January-June 2025. No eCatholic bulletin-module issue exists for the 12 Sundays to 1 November 2026, the LPi org `incarnation-church-10033` is an empty directory listing (no issues), and no Discover Mass, John Patrick or Bon Venture listing was found. No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, Incarnation, 1290 St. Nicholas Avenue, with Saturday, Sunday and weekday Masses in English and Spanish (home page, 9 November 2026). The Sunday 10:30 AM and 1:30 PM Spanish Masses are in the lower church of the same building, not a separate site.

## Website and bulletin provider

`no_bulletin`; the website is the home page, where the bulletin list appears. If issues resume as `documents/` uploads, the `other` page-pdfs collector reading the home page is the likely recipe; check with fetch:check before switching. `ecatholic:6897` identifies the parish's own eCatholic site.

## Not yet confirmed

Whether the parish still prints a bulletin it no longer posts. The LPi directory org is not evidence of an LPi bulletin.
