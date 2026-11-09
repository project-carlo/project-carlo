---
name: St. Aloysius
website: https://staloysiuschurchny.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://staloysiuschurchny.com/
  seen: 2026-11-09
  quote: 'Sunday: 2:00 p.m. (French)'
  note: 'Parish home page (PostcardMania site), rendered in headed Chrome: menu Home/About Us/Special
    Events/Photo Gallery/Contact Us, no bulletin link; Schedule of Masses Sunday 10:00 AM English, 12:00
    PM Spanish, 2:00 PM French; Tuesday and Thursday noon; Wednesday and Friday 7:30 PM Spanish.'
- url: https://staloysiuschurchny.com/bulletins
  seen: 2026-10-08
  quote: Sorry! That page doesn't seem to exist.
  note: No bulletin page on the parish site.
research:
- method: visit.py (headed Chrome) on staloysiuschurchny.com with --links (no bulletin, PDF or publisher
    links)
  url: https://staloysiuschurchny.com/
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read the home page for a bulletin link
  retry_when: The parish site adds a bulletin page or publisher link
  revisit_after: 2027-02-01
- method: probe po st-aloysius-church-10027 (LPi org 0018000000QxALjAAN exists as a directory listing
    with no issues) and st-aloysius-10027 (no org); Discover Mass st-aloysius-new-york-ny (listing with
    no bulletins); web search of parishesonline.com, discovermass.com, church-bulletin.org and bonventure.net
  url: https://discovermass.com/church/st-aloysius-new-york-ny/
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless a publisher listing gains issues
  retry_when: The LPi org or Discover Mass listing shows an issue
- method: 'ParishesOnline organization search by the church''s coordinates (1 mile), then probe po on
    the Catholic orgs at this church: only st-aloysius-church-10027 (empty)'
  url: https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=40.8136&longitude=-73.9466&distance=1
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the org lists an issue
  retry_when: probe po on the org returns an issue
bulletin_status: not-found
---

## Publisher

St. Aloysius (219 West 132nd Street, Harlem) has a small PostcardMania site with no bulletin page or link (/bulletins is a not-found page). The LPi org `st-aloysius-church-10027` is an empty directory listing, the Discover Mass listing has no bulletins, and no John Patrick, Bon Venture or eCatholic bulletin was found. No bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, St. Aloysius, 219 West 132nd Street: Sunday 10:00 AM (English), 12:00 PM (Spanish) and 2:00 PM (French); Tuesday and Thursday 12:00 noon (English); Wednesday and Friday 7:30 PM (Spanish), per the home page read 9 November 2026.

## Website and bulletin provider

`no_bulletin`; the website is the parish home page, where a bulletin link would appear.

## Not yet confirmed

Whether the parish prints a bulletin at all.
