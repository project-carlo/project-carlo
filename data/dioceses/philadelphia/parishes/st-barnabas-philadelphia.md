---
name: St. Barnabas
website: https://stbarnabasphl.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://stbarnabasphl.org/mass-schedule
  seen: 2026-10-29
  quote: Monday - Friday 7:00 a.m. - English
  note: 'Parish site (Wix, footer ''Copyright 2020''): Saturday vigil 5:00 p.m.; Sunday 8:00 a.m. and
    10:00 a.m. English, 12:00 p.m. Spanish; weekdays 7:00 a.m.; Saturday 8:00 a.m. Communion service;
    holy days 9:00 a.m. and 7:00 p.m. Its menu has Home, Parish Staff and Mass Schedule only, with no
    bulletin link.'
- url: https://archphila.org/parish/st-barnabas-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 4 months ago): 6300 Buist Ave., 19142; Rev. Miguel Angel Bravo Alvarez
    (Parochial Administrator); Sat 5 PM, Sun 8, 10 AM, Noon (Spanish), weekdays 7 AM. Matches the parish
    site.'
- url: https://discovermass.com/church/st-barnabas-philadelphia-pa/
  seen: 2026-10-29
  note: Discover Mass lists the church with the same Mass times (from MassTimes.org) and a Bulletins tab
    with no bulletin.
revisit: Look for a St. Barnabas bulletin on a John Patrick listing, ParishesOnline or eCatholic, or a
  bulletin page on the parish site.
revisit_after: 2027-01-15
research:
- method: John Patrick listing scan (ids 1-1300, no 19142 listing), pnpm diocese probe url on the site,
    site menu and Mass Schedule page
  url: https://www.church-bulletin.org/
  checked: '2026-10-29'
  outcome: not-found
  next_action: Look again only if the parish site links a bulletin publisher
  retry_when: The parish site or the directory links church-bulletin.org, ParishesOnline, eCatholic or
    a bulletin file
- method: ParishesOnline search API near the church (distance 3) and probe po on the st-barnabas-church-19142
    organization
  url: https://parishesonline.com/organization/st-barnabas-church-19142
  checked: '2026-10-29'
  outcome: not-found
  next_action: 'None: the organization has no publications'
  retry_when: The organization gains a publication
- method: Web search for the parish's bulletin, Discover Mass church page, Facebook page via visit.py
    (page not available)
  url: https://www.facebook.com/stbarnabasphilly/
  checked: '2026-10-29'
  outcome: not-found
  next_action: 'The one PDF the search found (irp.cdn-website.com ''10-25-2026 St Barnabas Bulletin.pdf'')
    is St. Barnabas, West Allis, Wisconsin: not this parish. Re-read the Facebook page if it loads'
  retry_when: The Facebook page loads or a bulletin PDF naming 6300 Buist Ave. turns up
bulletin_status: not-found
---

## Publisher

St. Barnabas (6300 Buist Ave., Elmwood Park / Southwest Philadelphia) is an open parish with public Mass, but no bulletin has been found. It has no John Patrick listing (scan of ids 1-1300 found none in 19142), its ParishesOnline organization (st-barnabas-church-19142) has no publications, its Discover Mass page has no bulletin, and its own site (stbarnabasphl.org) has no bulletin page. A search hit for '10-25-2026 St Barnabas Bulletin.pdf' is the West Allis, Wisconsin parish's, not this one (page 1 shows 'Parish office: 1526 South 72nd Street, West Allis').

## Worship sites

One: St. Barnabas Church, 6300 Buist Ave. Neither the directory nor the parish site names another.

## Website and bulletin provider

stbarnabasphl.org answers HTTP 200 and has Mass times but no bulletin. The row is `no_bulletin` (kept in the records, left off the site) until a bulletin turns up (README, Settled policy 4).

## Not yet confirmed

Whether a bulletin exists at all: the research entries list what was checked. The 'Hispanic apostolate' directory flag suggests a Spanish-language community that may use social media; the Facebook page did not load.
