---
name: Oratory of St. Emery
reason: no-bulletin
line1: 838 Kings Highway East
city: Fairfield
state: CT
postal_code: 06825
decided: 2026-11-12
roster: ['gcatholic:21986']
evidence:
- url: https://www.bridgeportdiocese.org/wp-content/uploads/2025/09/Press-Release-on-St.-Emerys-becoming-an-Oratory-Final-Oct-1-2025.pdf
  seen: 2026-11-12
  quote: The Oratory will serve primarily as the spiritual home of the Carmelites of Mary Ever Virgin
  note: 'Diocesan release of 1 October 2025: the former parish church of St. Emery erected an Oratory
    effective 29 September 2025; the Carmelite sisters, a private association of the faithful, have been
    on the St. Emery campus since 2023.'
- url: https://gcatholic.org/churches/usa-01/21986
  seen: 2026-11-12
  note: 'GCatholic: ''St. Emery'', Church, 838 Kings Hwy. E, Fairfield 06825; Plus Code 87H85Q99+73; website
    stemerys.com.'
- url: https://maryevervirgin.org/contact-us/the-holy-sacrifice-of-the-mass
  seen: 2026-11-12
  quote: Daily Mass is offered at 7 AM in St. Emery Church.
  note: 'The Carmelites of Mary Ever Virgin''s site (838 Kings Hwy E, Fairfield), read in the browser
    (visit.py; probe get answers 403): ''(Please use ramp door.) Any changes in schedule will be posted
    here: Join us for First Saturday Marian Devotion: SATURDAY, NOVEMBER 7 ... 7:00 a.m. Mass followed
    by Exposition & Confession''. A public invitation to a weekday Mass, current to November 2026. No
    bulletin, newsletter or PDF linked on the site.'
- url: https://www.bridgeportdiocese.org/two-carmelite-traditions-in-one-county/
  seen: 2026-11-12
  quote: the Carmelites of Mary Ever Virgin of the Ancient Observance of Carmel arrived in Fairfield in
    April of 2023
  note: Fairfield County Catholic, 1 July 2026; gives www.MaryEverVirgin.org as the community's site.
parish: our-lady-of-the-assumption-fairfield
revisit: Look for a bulletin from the Oratory of St. Emery or the Carmelites of Mary Ever Virgin (maryevervirgin.org,
  stemerys.com); if one appears, make the oratory a parish row with its church.
revisit_after: 2027-05-01
research:
- method: parish-site-access visit.py on maryevervirgin.org (home, The Holy Sacrifice of the Mass, A Day
    in Carmel, Contact Us), found via the diocese's 1 July 2026 article
  url: https://maryevervirgin.org/contact-us/the-holy-sacrifice-of-the-mass
  checked: '2026-11-12'
  outcome: found
- method: 'Looked for a bulletin for the oratory: maryevervirgin.org pages above (no bulletin or PDF link),
    stemerys.com (blocked), the receiving parishes'' bulletins (Assumption, St. Ann, St. Peter; no St.
    Emery Masses)'
  checked: '2026-11-12'
  outcome: not-found
  next_action: Check maryevervirgin.org and the receiving parishes' bulletins for a published oratory
    bulletin or schedule sheet
  retry_when: On revisit
---

## Why it is excluded

Open, with public Mass, but nothing the pipeline can read. The former parish church of St. Emery, 838 Kings Highway East, Fairfield, became the Oratory of St. Emery on 29 September 2025, "primarily as the spiritual home of the Carmelites of Mary Ever Virgin" (diocesan release of 1 October 2025), and its parish merged into Assumption, St. Ann and St. Peter on 1 November 2025. The Carmelites' own site (`https://maryevervirgin.org/contact-us/the-holy-sacrifice-of-the-mass`, read 2026-11-12 in the browser) says "Daily Mass is offered at 7 AM in St. Emery Church. (Please use ramp door.)" and invites the public to a First Saturday devotion on Saturday, 7 November 2026 beginning with 7:00 a.m. Mass: a public Mass, current.

No bulletin: the site links no bulletin, newsletter or PDF; `stemerys.com` is blocked; Assumption's (15 November 2026), St. Ann's (15 November 2026) and St. Peter's (8 November 2026) bulletins list no Mass at St. Emery. So it is `no-bulletin`, not a parish row (it never had a row of its own in these records). `parish` is Assumption, the main receiving parish, as the related parish; Assumption's bulletin does not carry the oratory's Masses.

Until 2026-11-12 this was an `open/` record (no public Mass found); reconcile found the Carmelites' site through the diocese's 1 July 2026 article "Two Carmelite traditions in one county".

## What would change this

A bulletin or weekly sheet published for the oratory (on maryevervirgin.org or stemerys.com) would make it a parish row with this church; a notice that the Mass is for the community alone would make it `no-public-mass`.
