---
name: Our Lady of Esperanza
website: https://ourladyofesperanza.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:10863']
group: ''
evidence:
- url: https://ourladyofesperanza.org/bulletins
  seen: 2026-11-09
  quote: Archive
  note: The eCatholic (10863) bulletin page, rendered in headed Chrome (plain fetches get a Cloudflare
    403), shows the Bulletin/Archive headings and no dated issue, as it did on 8 October.
- url: https://ourladyofesperanza.org
  seen: 2026-11-09
  quote: 12:00 PM Spanish
  note: 'Home page Mass Times: Saturday 6:00 PM Spanish; Sunday 9:00 AM Spanish, 10:30 AM, 12:00 PM Spanish;
    Monday-Friday and Saturday 9:00 AM Spanish. The page shows the day''s readings, so it is maintained.'
research:
- method: visit.py (headed Chrome) on ourladyofesperanza.org and /bulletins; issues.py ecatholic ecatholic:10863
    over the 12 Sundays to 1 November 2026
  url: https://ourladyofesperanza.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read /bulletins; if issues appear, set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue
  revisit_after: 2027-02-01
- method: probe po our-lady-of-esperanza-10032 and our-lady-of-esperanza-church-10032 (no org); Discover
    Mass our-lady-of-esperanza-new-york-ny (no listing); web search of parishesonline.com, discovermass.com,
    church-bulletin.org and bonventure.net
  url: https://discovermass.com/church/our-lady-of-esperanza-new-york-ny/
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the parish site links another publisher
  retry_when: The parish site links another publisher or a Flocknote bulletin
- method: 'ParishesOnline organization search by the church''s coordinates (1 mile), then probe po on
    the Catholic orgs at this church: our-lady-of-esperanza-church (LPi 0018000000QxAHvAAN), probed: a
    directory listing with no issues'
  url: https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=40.8340625&longitude=-73.9444375&distance=1
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the org lists an issue
  retry_when: probe po on the org returns an issue
bulletin_status: not-found
---

## Publisher

Our Lady of Esperanza (624 West 156th Street, Washington Heights) has an eCatholic site (10863) whose bulletin archive is empty: read 9 November 2026 in headed Chrome, /bulletins shows only the Bulletin and Archive headings. No eCatholic issue exists for the 12 Sundays to 1 November 2026, the LPi org `our-lady-of-esperanza-church` is an empty directory listing, Discover Mass has no listing, and no John Patrick or Bon Venture bulletin was found. No bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, Our Lady of Esperanza, 624 West 156th Street: Saturday 6:00 PM (Spanish); Sunday 9:00 AM (Spanish), 10:30 AM and 12:00 PM (Spanish); Monday-Saturday 9:00 AM (Spanish), per the home page read 9 November 2026.

## Website and bulletin provider

`no_bulletin`; the website is the parish's (empty) eCatholic bulletin archive, where an issue would appear first.

## Not yet confirmed

Whether the parish prints a bulletin it does not post. The home page links Flocknote only through a generic flocknote.com link, so no Flocknote bulletin channel was found.
