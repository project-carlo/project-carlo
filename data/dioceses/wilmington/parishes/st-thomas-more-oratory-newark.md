---
name: St. Thomas More Oratory (The Newman Center, University of Delaware)
website: https://www.udcatholic.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Iron Hill Deanery
evidence:
- url: https://www.udcatholic.org/newman-newsletter
  seen: 2026-10-27
  quote: Check out our newsletter to see what’s been going on in campus ministry this school year!
  note: The only publications are three semester newsletters (Fall 2026, Spring 2026, Fall 2025 PDFs under
    /s/). The Fall 2026 one (12 pages) is a campus-ministry magazine of student stories; it carries no
    parish masthead and no weekly schedule (Mass only as 'Mass at 11:30 AM' event notes).
- url: https://www.udcatholic.org/
  seen: 2026-10-27
  quote: The Newman Center Masses, Adoration & Confessions are for UD students and actively employed UD
    faculty/staff.
  note: 'Home page. Mass schedule: Sunday 11:30 AM and 8:15 PM; Monday-Thursday 4:30 PM; Friday 12:45
    PM. The page asks everyone else to attend ''their home parish or one of the Iron Hill Deanery parishes''.'
- url: https://irp.cdn-website.com/ba20104a/files/uploaded/10.25.2026-13a56019.pdf
  seen: 2026-10-27
  quote: Immaculate Conception Parish & St. Jude Mission Church
  note: 'Shared pastor (Fr. Jasper, appointed 2024-05-19) does not mean a shared bulletin: this issue
    has no mention of St. Thomas More or the Newman Center.'
revisit: Check whether the Newman Center starts posting a weekly bulletin, or whether the diocese lets
  the public attend; look again at the start of the spring 2027 semester.
revisit_after: 2027-01-25
research:
- method: visit.py (Chrome) on udcatholic.org home, /newman-newsletter and /prayerliturgy; probe pdf --grep
    on the Fall 2026 newsletter; probe pdf --grep on Immaculate Conception's 25 October 2026 bulletin
  url: https://www.udcatholic.org/newman-newsletter
  checked: '2026-10-27'
  outcome: not-published
  next_action: Re-read the site's pages for a weekly bulletin link at the start of the spring semester.
  retry_when: The Newman Center site adds a bulletin page, or Immaculate Conception's bulletin starts
    covering the Oratory
bulletin_status: not-published
---

## Publisher

No weekly bulletin. The Newman Center (45 Lovett Ave., Newark, the University of Delaware's Catholic campus ministry; the diocese lists it as 'Saint Thomas More Oratory, Newark', Iron Hill Deanery) posts a Mass schedule on its home page and a semester newsletter (Fall 2026, Spring 2026, Fall 2025). The newsletter is a campus-ministry magazine, not a bulletin, and has no Mass-time page. The pastor it shares with Immaculate Conception, Elkton (Fr. Richard Jasper, 'Pastor of both', The Dialog 2024-05-19) does not put it in that parish's bulletin, so there is no shared row (see `parishes/immaculate-conception-st-jude-elkton.md`).

## Audience

The site restricts Masses to UD students and actively employed faculty and staff. The place is recorded as a worship site (a campus chapel with a published schedule), but whether that is 'public' Mass is a question for the data owner: see the handoff flag. Either way no bulletin exists, so the row stays off the site (Settled policy 4).

## Website and bulletin provider

`no_bulletin`, `bulletin_status: not-published`, website https://www.udcatholic.org/.
