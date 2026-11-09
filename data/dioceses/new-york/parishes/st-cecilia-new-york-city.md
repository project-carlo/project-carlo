---
name: St. Cecilia and Holy Agony
website: https://saintceciliaparishnyc.org/bulletin.html
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://saintceciliaparishnyc.org/bulletin.html
  seen: 2026-11-09
  quote: SUNDAY MAY 26, 2024
  note: 'The parish''s bulletin page, rendered in headed Chrome: newest download is 19 May 2024 (file
    2024/03-0914_5-19-24.pdf, an LPi-numbered file); nothing later in 2024, 2025 or 2026.'
- url: https://saintceciliaparishnyc.org/
  seen: 2026-11-09
  quote: Broadcasted 11/8/26 8:58am - 11/8/26 10:20am
  note: 'Home page BoxCast feed: the Sunday English 9:00 AM Mass was broadcast 8 November 2026, the Spanish
    Mass the same day and the Saturday vigil 7 November; the page names Saint Cecilia and Holy Agony and
    lists Saturday 5:00 PM and 7:00 PM, Sunday 9:00 AM, 11:00 AM and 1:00 PM, Monday-Friday 8:00 AM and
    Wednesday 7:00 PM.'
research:
- method: visit.py (headed Chrome) on saintceciliaparishnyc.org and /bulletin.html
  url: https://saintceciliaparishnyc.org/bulletin.html
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read /bulletin.html; if issues after May 2024 appear, set bulletin_provider other, run
    fetch:check and record the recipe
  retry_when: The bulletin page lists an issue dated after 2024-05-19
  revisit_after: 2027-02-01
- method: 'probe container 03/0914 (the LPi number in the self-hosted file names): every Sunday probed
    403, monthly from 8 November 2026 back to 26 May 2024 and on 19 May 2024 itself, so LPi never posted
    these issues to the container'
  url: https://container.parishesonline.com/bulletins/03/0914/20240519B.pdf
  checked: '2026-11-09'
  outcome: not-found
  next_action: None; the container is not a public channel for this parish
  retry_when: probe container 03/0914 returns an issue
- method: probe po st-cecilia-10029 and st-cecilia-church-10029 (no org); Discover Mass st-cecilia-new-york-ny
    (listing with no bulletins); web search of parishesonline.com, church-bulletin.org and bonventure.net
  url: https://discovermass.com/church/st-cecilia-new-york-ny/
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless a publisher listing gains issues
  retry_when: The parish site links another publisher
- method: 'ParishesOnline organization search by the church''s coordinates (1 mile), then probe po on
    the Catholic orgs at this church: roman-catholic-church-of-st-cecilia-and-holy-agony (LPi 0018000000Qc1GMAAZ)
    and holy-agony (0018000000QxAHoAAN), both probed: directory listings with no issues'
  url: https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=40.7924&longitude=-73.9469&distance=1
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the org lists an issue
  retry_when: probe po on the org returns an issue
bulletin_status: not-found
---

## Publisher

St. Cecilia and Holy Agony (East Harlem) published an LPi-printed bulletin (files named `03-0914_<date>.pdf`) on its own site, but the bulletin page, read 9 November 2026, still ends at 19 May 2024. LPi container 03/0914 serves none of these issues, the LPi orgs `roman-catholic-church-of-st-cecilia-and-holy-agony` and `holy-agony` are empty directory listings, Discover Mass has a listing with no bulletins, and no John Patrick or Bon Venture bulletin was found. No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, St. Cecilia, 120 East 106th Street: Saturday 5:00 PM (English) and 7:00 PM (Spanish); Sunday 9:00 AM (English), 11:00 AM and 1:00 PM (Spanish); Monday-Friday 8:00 AM; Wednesday 7:00 PM (home page, 9 November 2026), with the 7-8 November Masses broadcast from it. The Holy Agony church (1834 Third Avenue) in the parish's name was relegated to profane use on 30 June 2017 and is excluded (`excluded/holy-agony-new-york-city`).

## Website and bulletin provider

`no_bulletin`; the website is the parish's bulletin page, where an issue would appear first.

## Not yet confirmed

Whether the parish still prints its LPi bulletin and stopped posting it in May 2024.
