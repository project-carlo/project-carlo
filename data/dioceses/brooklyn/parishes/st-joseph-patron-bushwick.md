---
name: St. Joseph Patron of the Universal Church (Bushwick)
website: https://www.stjosephpatronchurch.org/
bulletin_provider: other
provider_id: page-pdfs https://www.stjosephpatronchurch.org/bulletins
publication: []
group: Deanery B2 (Brooklyn East)
evidence:
- url: https://www.stjosephpatronchurch.org/api/bulletin-file?name=bulletins%2FBULLETIN%20OCT%2011%202026.pdf
  seen: 2026-11-07
  note: '11 October 2026 issue (''BULLETIN OCT 11 2026.pdf''), 4 pages, scanned images with no text layer
    (page 1 read with render.py). Self-made: no LPi, John Patrick or Church Bulletin Inc. footer. Page
    1 masthead: ''ST. JOSEPH PATRON OF THE UNIVERSAL CHURCH'', 185 Suydam St, Brooklyn, NY 11221, ''Founded
    in 1921'', staffed by the Missionaries of St. Charles - Scalabrinians, R. Sergio Dall Agnese, C.S.,
    Administrator. Weekend Mass schedule: Saturday 7:00PM (Español); Sunday 8:30AM, 10:00AM, 1:00PM, 7:00PM
    (Misas en español), English Mass 11:30AM; daily Monday-Friday 8:30AM and 7:00PM (Español). No other
    church named. The page is an image, so recheck can''t find a quote.'
- url: https://www.stjosephpatronchurch.org/api/bulletins
  seen: 2026-11-07
  quote: BULLETIN OCT 11 2026.pdf
  note: 'JSON list the /bulletins page loads in the browser (the HTML says ''Loading bulletins...''):
    OCT 11 2026 (created 2026-10-10), OCT 04 2026 (2026-10-07), SEPT 27 2026 (2026-09-28), SEPT 20 2026
    (2026-09-22); each url is /api/bulletin-file?name=bulletins%2F<title>. Nothing newer on 2026-11-07,
    28 days after the last upload.'
- url: https://www.stjosephpatronchurch.org/mass-sacraments/mass-times
  seen: 2026-11-07
  quote: 'Sunday Midday (English): 11:30 AM'
  note: 'Mass Times page: Saturday vigil 7:00 PM, Sunday 8:30, 10:00 AM, 1:00 and 7:00 PM in Spanish,
    11:30 AM English; Monday-Friday 8:30 AM and 7:00 PM. Same as the bulletin.'
- url: https://discovermass.com/church/st-joseph-patron-brooklyn-ny/
  seen: 2026-11-07
  note: The diocesan directory's website for this parish. A Discover Mass listing with no bulletins (issues.py
    discovermass); its 'Visit Website' links the parish Facebook page (profile.php?id=61560358307870).
    The parish site stjosephpatronchurch.org was found by a Yahoo search.
revisit: Recheck /api/bulletins for an issue after 11 October 2026 and rerun fetch:check.
revisit_after: 2026-11-21
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://www.stjosephpatronchurch.org/bulletins
  url: https://www.stjosephpatronchurch.org/bulletins
  checked: '2026-11-07'
  outcome: found
  next_action: Rerun fetch:check and confirm it picks an issue after 11 October 2026 (the newest on 2026-11-07,
    uploaded 2026-10-10); if none appears by the recheck, set no_bulletin with status not-found and keep
    this recipe here
  retry_when: /api/bulletins lists an issue after OCT 11 2026
  revisit_after: 2026-11-21
bulletin_status: available
---

## Publisher

St. Joseph Patron of the Universal Church publishes its own bulletin, a self-made 4-page scan (pages are images, no text layer) posted on its Next.js site stjosephpatronchurch.org. The 11 October 2026 issue (read 2026-11-07 with render.py) has the masthead "ST. JOSEPH PATRON OF THE UNIVERSAL CHURCH", 185 Suydam St, Brooklyn, NY 11221, staffed by the Scalabrinian Missionaries of St. Charles, R. Sergio Dall Agnese, C.S., Administrator.

## Worship sites

One: St. Joseph Patron Church, 185 Suydam Street. The bulletin's schedule (Saturday 7:00PM; Sunday 8:30AM, 10:00AM, 11:30AM English, 1:00PM, 7:00PM; weekdays 8:30AM and 7:00PM) names no other place, and the site's Mass Times page agrees.

## Website and bulletin provider

`other`, recipe `page-pdfs https://www.stjosephpatronchurch.org/bulletins`. The page renders its list from `/api/bulletins` (JSON) in the browser; each issue is `/api/bulletin-file?name=bulletins%2FBULLETIN%20<MON DD YYYY>.pdf`. fetch:check (headed Chrome, 2026-11-07) resolved "page-pdfs ... first-listed" and downloaded the 11 October issue; issue date and freshness come back `unknown` because the pages are images, so read the date from the file name. The bulletin is image-only: the pipeline needs OCR to read its Mass times. The directory's website for this parish is a Discover Mass listing with no bulletins; its own site was found by web search. No publication id: self-made, no online container (LPi slugs st-joseph-patron-church-11221, -of-the-universal-church-11221 and bare forms don't exist).

## Not yet confirmed

Whether posting continues: the newest issue on 2026-11-07 was 11 October (uploaded 10 October), after uploads 3-9 days apart. See research.
