---
name: St. Luke, Bronx
website: https://stlukebronx.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:10936']
group: ''
evidence:
- url: https://stlukebronx.org/bulletins
  seen: 2026-11-08
  quote: Bulletin ARCHIVE 2025 March 1, 2025 February 9, 2025 January 1, 2025
  note: 'eCatholic archive (site 10936) read in headed Chrome: newest issue 1 March 2025; before that
    2021.'
- url: https://files.ecatholic.com/10936/bulletins/20250301.pdf
  seen: 2026-10-08
  note: 'Old-session read of the 1 March 2025 issue: page 1 names ST. LUKE´S CHURCH, 623 E 138th Street,
    so the archive is St. Luke''s own bulletin.'
- url: https://stlukebronx.org/
  seen: 2026-11-08
  quote: 'Sunday: 8:30 AM English 10:30 AM Bilingual English/Spanish - Family Mass 12:30 PM Spanish /
    Español 4:00 PM Ghanaian'
  note: Home page Mass schedule; the news feed announces the Feast of Saint Luke on 17 October, so the
    site is maintained.
research:
- method: visit.py on stlukebronx.org and /bulletins; issues.py ecatholic ecatholic:10936 over 12 Sundays
    to 8 November 2026
  url: https://stlukebronx.org/bulletins
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-read the archive; if issues resume, set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue dated after 1 March 2025
  revisit_after: 2027-02-01
- method: issues.py discovermass st-luke-bronx-ny ('no bulletins available'); probe po st-luke-church-10454
    (org exists, no publications)
  url: https://parishesonline.com/organization/st-luke-church-10454
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-run probe po
  retry_when: The parish site links another publisher
bulletin_status: not-found
---

## Publisher

St. Luke (623 E 138th St) published its own bulletin on its eCatholic site (10936); the archive's newest issue is 1 March 2025, whose page 1 names St. Luke's Church. Nothing newer is posted there or at the dated eCatholic paths, Discover Mass lists the church with no bulletins, and ParishesOnline has a directory org with no publications (all 8 November 2026). No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, St. Luke, 623 East 138th Street: Saturday 7:00 PM (Spanish), Sunday 8:30 AM, 10:30 AM (bilingual), 12:30 PM (Spanish) and 4:00 PM (Ghanaian), Tuesday-Saturday 7:00 PM, per the home page read 8 November 2026.

## Website and bulletin provider

`no_bulletin`; the website is the eCatholic archive, where a new issue would appear first.

## Not yet confirmed

Whether the parish still prints a bulletin it no longer posts.
