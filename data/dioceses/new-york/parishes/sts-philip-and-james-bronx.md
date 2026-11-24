---
name: Sts. Philip and James, Bronx
website: https://stsphilipandjameschurchbronx.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['ecatholic:27745']
group: ''
evidence:
- url: https://stsphilipandjameschurchbronx.org/bulletins
  seen: 2026-11-09
  quote: Bulletin Archive 2023 March 5, 2023
  note: 'eCatholic archive (site 27745) read in headed Chrome: newest issue 5 March 2023. (The old session''s
    ''November 26, 2023 issue at files.ecatholic.com/6761'' was St. Martin of Tours'' archive, not this
    parish''s.)'
- url: https://stsphilipandjameschurchbronx.org/
  seen: 2026-11-09
  quote: 'SATURDAY: 4:00 PM SUNDAY: 8:00 AM 9:30 AM Spanish 11:30 AM Choir 1:30 PM Other 1st and 3rd Sunday
    Only - Igbo Mass MONFRI 9:00 AM'
  note: Home page Mass schedule.
research:
- method: visit.py --bulletin on the parish site and /bulletins; issues.py ecatholic ecatholic:27745 over
    10 Sundays to 8 November 2026
  url: https://stsphilipandjameschurchbronx.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-read the archive; if issues resume, set bulletin_provider ecatholic and run fetch:check
  retry_when: The archive lists an issue dated after 5 March 2023
  revisit_after: 2027-02-01
- method: issues.py discovermass sts-philip-and-james-bronx-ny ('no bulletins available'); ParishesOnline
    sts-philip-and-james-10469, saints-philip-and-james-10469, st-philip-and-james-10469, sts-philip-and-james-church-10469,
    sts-philip-james-church-10469 (no org)
  url: https://discovermass.com/church/sts-philip-and-james-bronx-ny/
  checked: '2026-11-08'
  outcome: not-found
  next_action: None
  retry_when: The parish site links another publisher
bulletin_status: not-found
---

## Publisher

Sts. Philip and James (1160 E 213th St) published its bulletin on its eCatholic site (27745) until 5 March 2023, the archive's newest issue. Nothing newer is posted there or at the dated eCatholic paths, Discover Mass lists no bulletins, and ParishesOnline has no org under the likely slugs (8-9 November 2026). No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, Sts. Philip and James, 1160 East 213th Street: Saturday 4:00 PM, Sunday 8:00 AM, 9:30 AM (Spanish), 11:30 AM, and 1:30 PM Igbo Mass on the 1st and 3rd Sundays, Monday-Friday 9:00 AM, per the home page read 9 November 2026. The Igbo Mass is in the same church.

## Website and bulletin provider

`no_bulletin`; the website is the eCatholic archive, where a new issue would appear first.

## Not yet confirmed

Whether the parish still prints a bulletin it no longer posts.
