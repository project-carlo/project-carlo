---
name: St. Athanasius, Bronx
website: https://stathanasiusbx.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://stathanasiusbx.org/bulletins
  seen: 2026-11-08
  quote: Bulletin Archive
  note: The eCatholic site's (11077) Bulletin Archive page, read in headed Chrome, lists no issues at
    all.
- url: https://stathanasiusbx.org/
  seen: 2026-11-08
  quote: 'SATURDAY: 7:00 PM Spanish SUNDAY: 8:00 AM Spanish 10:00 AM 11:30 AM Spanish'
  note: Home page Mass schedule; header 'St. Athanasius Church Catholic Parish 878 Tiffany Street Bronx,
    New York 10459'.
research:
- method: visit.py on stathanasiusbx.org and /bulletins; issues.py ecatholic ecatholic:11077 over 15 Sundays
    to 8 November 2026
  url: https://stathanasiusbx.org/bulletins
  checked: '2026-11-08'
  outcome: not-found
  next_action: Re-read the archive page; if issues appear, set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue
  revisit_after: 2027-02-01
- method: issues.py discovermass st-athanasius-bronx-ny ('no bulletins available'); ParishesOnline st-athanasius-10459,
    saint-athanasius-10459, st-athanasius-church-10459 (no org)
  url: https://discovermass.com/church/st-athanasius-bronx-ny/
  checked: '2026-11-08'
  outcome: not-found
  next_action: None
  retry_when: The parish site links another publisher
bulletin_status: not-found
---

## Publisher

St. Athanasius has an eCatholic site (11077) with an empty Bulletin Archive, and no dated eCatholic issue exists for the 15 Sundays to 8 November 2026. Discover Mass lists the church with 'no bulletins available' and ParishesOnline has no org under the likely slugs. No bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4). `publication` is empty because no bulletin was seen; the eCatholic id is the website's, recorded in evidence.

## Worship sites

One church, St. Athanasius, 878 Tiffany Street, with Saturday 7:00 PM (Spanish), Sunday 8:00 AM (Spanish), 10:00 AM and 11:30 AM (Spanish), and daily Masses per the home page (8 November 2026).

## Website and bulletin provider

`no_bulletin`; the website is the parish's (empty) bulletin archive, where an issue would appear first.

## Not yet confirmed

Whether the parish prints a bulletin it does not post.
