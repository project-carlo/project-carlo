---
name: St. Jerome, Bronx
website: https://www.stjeromebronx.com/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.stjeromebronx.com/bulletins
  seen: 2026-11-08
  quote: Bulletin ARCHIVE
  note: The eCatholic site's (11293) bulletin archive, read in headed Chrome, lists no issues; the News
    pages carry only a Vatican News video.
- url: https://www.stjeromebronx.com/
  seen: 2026-11-08
  quote: SUNDAY | DOMINGO 9:00 AM Spanish / Español 10:30 AM English / Ingles 12:00 PM Spanish / Español
  note: Home page Mass schedule; the page shows the 32nd Sunday readings, so it is maintained.
research:
- method: visit.py --bulletin and --links on stjeromebronx.com, /bulletins, /news, /news-events; issues.py
    ecatholic ecatholic:11293 over 12 Sundays to 8 November 2026
  url: https://www.stjeromebronx.com/bulletins
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-read the archive page; if issues appear, set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue
  revisit_after: 2027-02-01
- method: Discover Mass slug st-jerome-bronx-ny (404); ParishesOnline st-jerome-10454, saint-jerome-10454,
    st-jerome-church-10454 (no org)
  url: https://discovermass.com/church/st-jerome-bronx-ny/
  checked: '2026-11-08'
  outcome: not-found
  next_action: None
  retry_when: The parish site links another publisher
bulletin_status: not-found
---

## Publisher

St. Jerome (230 Alexander Ave, Mott Haven) has an eCatholic site (11293) whose bulletin archive is empty; no dated eCatholic issue exists for the 12 Sundays to 8 November 2026, Discover Mass has no listing and ParishesOnline no org under the likely slugs. No bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, St. Jerome, 230 Alexander Avenue: Monday-Friday 9:00 AM, Saturday 7:00 PM, Sunday 9:00 AM, 10:30 AM (English) and 12:00 PM, mostly in Spanish, per the home page read 8 November 2026.

## Website and bulletin provider

`no_bulletin`; the website is the parish's (empty) bulletin archive, where an issue would appear first.

## Not yet confirmed

Whether the parish prints a bulletin it does not post.
