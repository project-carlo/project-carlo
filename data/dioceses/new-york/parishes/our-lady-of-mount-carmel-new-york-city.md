---
name: Pontifical Shrine of Our Lady of Mount Carmel
website: https://www.olmtc.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.olmtc.org/_files/ugd/13fb0e_a6d35fc241ed4bbab143a3bc94ef4bb3.pdf
  seen: 2026-11-09
  quote: February 1, 2026 1 de febrero de 2026
  note: 'Page 1 masthead of the newest linked issue: THE PONTIFICAL SHRINE OF OUR LADY OF MOUNT CARMEL,
    Pallottine Fathers, 448 East 116th Street. Page 2 lists Mass intentions for the shrine alone (Saturday
    9:00, 4:00, 5:30; Sunday 8:00, 9:15, 10:30, 12:00, 1:00, 2:30).'
- url: https://www.olmtc.org/bulletins
  seen: 2026-11-09
  quote: 2026 02 01
  note: 'Wix bulletin page rendered in headed Chrome: the Past Bulletins list starts at 2026 02 01 and
    runs back to 2022; no issue after 1 February 2026 is linked, nine months on.'
- url: https://www.olmtc.org/mass-times-and-hours
  seen: 2026-11-09
  quote: 2:30 PM (Polish)
  note: 'Current Mass schedule page: Saturday 9:00 AM Latin, 4:00 PM English and 5:30 PM Spanish vigils;
    Sunday 8:00 AM Spanish, 9:15 AM English, 10:30 AM Latin, 12:00 noon Spanish, 1:00 PM English, 2:30
    PM Polish; weekdays 7:00 AM English and 9:00 AM Latin; Haitian Mass every third Saturday 10:00 AM.'
research:
- method: visit.py (headed Chrome) on olmtc.org/bulletins and /copy-of-bulletins; the bulletin links are
    Wix _files/ugd/<hash>.pdf uploads named by date in the link text
  url: https://www.olmtc.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read /bulletins; if issues after 1 February 2026 appear, set bulletin_provider other,
    run fetch:check (page-pdfs on the bulletin page) and record the recipe
  retry_when: The bulletin page lists an issue dated after 2026-02-01
  revisit_after: 2027-02-01
- method: probe po our-lady-of-mount-carmel-church-10029 (LPi org 0018000000QxAHpAAN exists as a directory
    listing with no issues) and our-lady-of-mount-carmel-10029 (no org); Discover Mass our-lady-of-mount-carmel-new-york-ny
    (listing with no bulletins); web search of parishesonline.com, church-bulletin.org and bonventure.net
  url: https://discovermass.com/church/our-lady-of-mount-carmel-new-york-ny/
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the shrine site links another publisher
  retry_when: The shrine site links another publisher
- method: 'ParishesOnline organization search by the church''s coordinates (1 mile), then probe po on
    the Catholic orgs at this church: only our-lady-of-mount-carmel-church-10029 (empty); the others are
    neighbouring parishes'
  url: https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=40.7946875&longitude=-73.9341875&distance=1
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the org lists an issue
  retry_when: probe po on the org returns an issue
bulletin_status: not-found
---

## Publisher

The Pontifical Shrine of Our Lady of Mount Carmel (Pallottine Fathers, 448 East 116th Street, East Harlem) published its own weekly bulletin as PDFs on its Wix site. The newest linked issue, read 9 November 2026, is 1 February 2026; its page 1 masthead names the shrine alone at 448 East 116th Street and page 2 lists Mass intentions for its own Masses. Nothing later is posted, the LPi org `our-lady-of-mount-carmel-church-10029` is an empty directory listing, and the Discover Mass listing has no bulletins. No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, Our Lady of Mount Carmel, 448 East 116th Street: Saturday 9:00 AM Latin, 4:00 PM English and 5:30 PM Spanish vigils; Sunday 8:00 AM, 9:15 AM, 10:30 AM (Latin), 12:00 noon, 1:00 PM and 2:30 PM (Polish); weekdays 7:00 AM and 9:00 AM; a Haitian Mass every third Saturday at 10:00 AM (Mass Times page, 9 November 2026). Adoration is in the convent chapel; no Mass is listed there.

## Website and bulletin provider

`no_bulletin`; the website is the shrine's bulletin page, where an issue would appear first. The issues are Wix `_files/ugd/<hash>.pdf` uploads whose date is only in the link text, so a newest-first `page-pdfs` recipe would need a fetch:check before use. The bulletin is self-hosted with no publisher id.

## Not yet confirmed

Whether the shrine still prints a bulletin it stopped posting after 1 February 2026.
