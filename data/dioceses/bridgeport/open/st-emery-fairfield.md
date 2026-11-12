---
name: Oratory of St. Emery
revisit: 'Find whether the Oratory of St. Emery (Carmelites of Mary Ever Virgin) has a public Mass schedule:
  try stemerys.com in the browser again, search for the Carmelites'' own site or social page, or ask the
  diocese''s Mass-times listing; then make it a church (with its bulletin, or an excluded no-bulletin)
  or excluded no-public-mass.'
revisit_after: 2027-01-15
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
parish: our-lady-of-the-assumption-fairfield
line1: 838 Kings Highway East
city: Fairfield
state: CT
postal_code: 06825
research:
- method: probe url and parish-site-access visit.py on stemerys.com (http and https)
  url: http://stemerys.com/
  checked: '2026-11-12'
  outcome: access-blocked
  next_action: Retry in the browser; look for a Carmelites of Mary Ever Virgin site or social page with
    an oratory Mass schedule
  retry_when: A new site or listing for the oratory turns up, or on revisit
- method: grep of the receiving parishes' current bulletins (Assumption 04/0776 15 Nov 2026, St. Ann 03/0286
    15 Nov 2026, St. Peter 8 Nov 2026) for 'Emery'
  checked: '2026-11-12'
  outcome: not-found
  next_action: Recheck the receiving bulletins and the diocesan Mass-times page for oratory Masses
  retry_when: On revisit
---

## What is known

The diocese's release of 1 October 2025 says the former parish church of St. Emery, 838 Kings Highway East, Fairfield, was erected the Oratory of St. Emery effective 29 September 2025, "primarily as the spiritual home of the Carmelites of Mary Ever Virgin", a private association of the faithful on the campus since 2023 who "lead a life of prayer and quiet ministry". The parish of Holy Family–St. Emery then merged into Assumption, St. Ann and St. Peter on 1 November 2025.

Checked 2026-11-12 with no Mass schedule found: the receiving parishes' current bulletins (Assumption's 15 November 2026 issue names St. Emery only as the former host of Taste of Christmas; St. Ann's and St. Peter's don't name it); the diocese's directory and Mass-times page (no entry); `stemerys.com` (probe url 403; the browser got ERR_BLOCKED_BY_CLIENT over http and a certificate-name error over https).

## Why it is not decided

An oratory can hold public Mass, and a Carmelite community's chapel Mass may or may not be open to the public; no source read says either. It goes in as a church only on a source showing public Mass, and in `excluded/` (no-public-mass) only on one saying Mass there is for the community alone. The `parish` link to Assumption is the nearest receiving parish, not a finding that Assumption serves it.
