---
name: Our Lady of Hope Church
website: https://ourladyofhopewny.org
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: 'Family #23'
evidence:
- url: https://ourladyofhopewny.org
  seen: 2026-09-26
  note: The parish's own website. It posts no bulletin. It blocked automated reads (HTTP 403).
- url: https://parishesonline.com/organization/our-lady-of-hope-14213
  seen: 2026-10-07
  note: 'ParishesOnline has an organization for it (18 Greenwood Pl, LPi 0018000000QbyuTAAR), but `probe
    po our-lady-of-hope-14213` lists no issues: it publishes nothing there.'
- url: https://discovermass.com/church/our-lady-of-hope-buffalo-ny/
  seen: 2026-10-07
  quote: There are currently no bulletins available for Our Lady of Hope
- url: https://www.buffalodiocese.org/sunday-morning-mass-times/
  seen: 2026-10-07
  quote: Sun. 9 a.m. Our Lady of Hope Buffalo
  note: Open with public Mass; the Saturday page lists "Sat. 4 p.m. Our Lady of Hope Buffalo".
- url: https://www.buffalodiocese.org/sunday-morning-mass-times/
  seen: 2026-11-16
  quote: Our Lady of Hope Buffalo Sun. 11 a.m.
  note: Re-read 16 November 2026; the same page also has 'Our Lady of Hope Buffalo Sun. 9 a.m.', and the
    Saturday-afternoon page has Sat. 4 p.m.
- url: https://discovermass.com/church/our-lady-of-hope-buffalo-ny/
  seen: 2026-11-16
  quote: There are currently no bulletins available for Our Lady of Hope.
  note: 'Its Mass times there (MassTimes.org data, under a COVID-era banner): Saturday 4:00pm; Sunday
    9:00am, 11:00am; Monday to Friday 11:30am. It gives the address 248 Lafayette Ave.'
revisit: 'Owner''s rule (16 November 2026): keep this row unresolved with its published Mass times for
  the coming feature. Look again for a bulletin on ourladyofhopewny.org (Cloudflare blocks automated reads),
  ParishesOnline our-lady-of-hope-14213 or Discover Mass.'
revisit_after: 2027-03-01
research:
- method: parish-site-access visit.py --bulletin on ourladyofhopewny.org (headed Chrome, 10 retries)
  url: https://ourladyofhopewny.org
  checked: '2026-11-16'
  outcome: access-blocked
  next_action: Retry the site in a browser later, or ask the parish whether it publishes a bulletin
  retry_when: Cloudflare lets a load through
- method: probe po our-lady-of-hope-14213; Discover Mass church page; web search for an Our Lady of Hope
    bulletin
  url: https://parishesonline.com/organization/our-lady-of-hope-14213
  checked: '2026-11-16'
  outcome: not-found
  next_action: Check again at the revisit date
  retry_when: A bulletin appears on any of these
bulletin_status: not-found
---

## Publisher

Our Lady of Hope Church holds public Mass (the diocese's Mass-times pages, read 7 October 2026: Saturday 4 pm, Sunday 9 and 11 am) but publishes no bulletin the pipeline can read. It is a `no_bulletin` parish row, so since 7 October 2026 it and its church are kept here but left off the site (see the README's *Settled policy*). PR 14 modelled this as `our-lady-of-hope-buffalo`.

## Worship sites

Our Lady of Hope Church. Each church record gives the Mass evidence. Churches of the family that no longer hold Mass are in excluded/ or open/.

## Website and bulletin provider

https://ourladyofhopewny.org is its own site; no bulletin or newsletter was found there.

Checked on 7 October 2026 and found nothing: its own site stayed behind Cloudflare in about 39 headed-Chrome loads; its ParishesOnline organization has no issues; its Discover Mass page has no bulletins. The Holy Cross bulletin (same family; 20 and 27 September, 4 October 2026) gives Our Lady of Hope office hours and events but only Holy Cross's Masses, so the church can't be attached to that row.

## Not yet confirmed

Whether ourladyofhopewny.org posts a bulletin behind its Cloudflare check: on 16 November 2026 headed Chrome was challenged on every load (10 retries), ParishesOnline our-lady-of-hope-14213 still has no issues, and Discover Mass has none. Revisit 2027-03-01.

The church's address: the church record gives 18 Greenwood Pl. (GCatholic, the diocesan finder), while Discover Mass and a directory give 248 Lafayette Ave.; the church was the former Annunciation, at Grant St. and Lafayette Ave. Not changed here; check it before the row ever goes live.

## Mass times published

Our Lady of Hope publishes no bulletin that could be found, but its Mass times are published online (owner's rule of 16 November 2026: keep it unresolved, not excluded, so a coming feature can show these):

- https://www.buffalodiocese.org/saturday-afternoon-mass-times/ and https://www.buffalodiocese.org/sunday-morning-mass-times/ (seen 2026-11-16): Sat. 4 p.m.; Sun. 9 a.m.; Sun. 11 a.m.
- https://discovermass.com/church/our-lady-of-hope-buffalo-ny/ (seen 2026-11-16): Saturday 4:00pm; Sunday 9:00am, 11:00am; Monday to Friday 11:30am (MassTimes.org data, age unknown).

The row stays `no_bulletin`, which already keeps it and its church off the site without excluding it; it is the closest status the CLI has to "open, Mass published, no bulletin".
