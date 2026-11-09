---
name: Our Lady of Pompeii
website: https://olpnyc.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:our-lady-of-pompeii-church-10014', 'lpi:0018000000QbzzmAAB', 'po-container:04/0225',
  'ecatholic:19247']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0225/20260809C.pdf
  seen: 2026-11-09
  quote: Our Lady of Pompei, New York, NY 04-0225
  note: 'The newest file in the parish''s LPi container is a two-page Cover (C) upload dated 9 August
    2026: page 1 is a standing masthead (25 Carmine Street, Scalabrinians, Schedule of Masses), page 2
    the advertisers. It has no dated content; the container''s other uploads are also Covers at irregular
    intervals (14 June, 19 April 2026, 28 December, 7 September 2025...), i.e. LPi''s printed wrapper,
    not a weekly issue.'
- url: https://olpnyc.org/bulletins
  seen: 2026-11-09
  quote: August 27, 2023
  note: 'eCatholic (19247) bulletin archive, rendered in headed Chrome: newest issue 27 August 2023.'
- url: https://olpnyc.org/
  seen: 2026-10-08
  quote: 11:00 AM Italian
  note: 'Home page Mass schedule (October research): Saturday 5:00 PM vigil; Sunday 9:00 AM English, 11:00
    AM Italian, 1:00 PM Portuguese, 5:00 PM English; weekdays 12:05 PM; Wednesday 6:30 PM.'
research:
- method: probe po our-lady-of-pompeii-church-10014 --issues 30; probe container 04/0225 over the 12 Sundays
    to 1 November 2026 (all 403)
  url: https://parishesonline.com/organization/our-lady-of-pompeii-church-10014
  checked: '2026-11-09'
  outcome: not-found
  next_action: Re-run probe po; if a weekly B (bulletin) issue appears, set bulletin_provider parishes_online
    with provider_id our-lady-of-pompeii-church-10014 and run fetch:check
  retry_when: The LPi org lists a dated bulletin issue (type B) rather than a Cover
  revisit_after: 2027-02-01
- method: visit.py (headed Chrome) on olpnyc.org and /bulletins; issues.py ecatholic ecatholic:19247 over
    the 12 Sundays to 1 November 2026; Discover Mass our-lady-of-pompeii-new-york-ny (listing with no
    bulletins)
  url: https://olpnyc.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: None unless the archive resumes
  retry_when: The eCatholic archive lists an issue after 27 August 2023
bulletin_status: not-found
---

## Publisher

Our Lady of Pompeii (25 Carmine Street, Greenwich Village; Scalabrinian Missionaries of St. Charles) has an LPi account, container 04/0225 (org `our-lady-of-pompeii-church-10014`), but the container holds only two-page Cover uploads at irregular intervals: the newest, 9 August 2026, is a standing masthead with the Mass schedule plus an advertisers page, with no dated content. LPi prints the wrapper; the weekly inside pages are not posted. The parish's eCatholic archive (19247) stops at 27 August 2023, Discover Mass has a listing with no bulletins, and no John Patrick or Bon Venture bulletin was found. No current bulletin was found, so the row is `no_bulletin` and kept off the site (Settled policy 4).

## Worship sites

One church, Our Lady of Pompeii, 25 Carmine Street. The 9 August 2026 LPi cover's Schedule of Masses gives Saturday vigil 5:00 PM (English); Sunday 9:00 AM (English), 11:00 AM (Italian), 1:00 PM (Portuguese), 5:00 PM (English); weekdays 12:05 PM; Wednesday 6:30 PM, matching the home page read 8 October 2026.

## Website and bulletin provider

`no_bulletin`. The publication ids are the parish's own LPi and eCatholic accounts, recorded so audit can compare them; neither carries a current weekly issue. If the LPi org starts posting type-B issues, `parishes_online` with provider_id `our-lady-of-pompeii-church-10014` is the route.

## Not yet confirmed

Whether the full weekly bulletin is printed with the LPi cover and simply not uploaded.
