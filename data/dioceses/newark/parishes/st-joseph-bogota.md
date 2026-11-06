---
name: St. Joseph, Bogota
website: https://stjosephbogota.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6032
publication: ['url:https://www.church-bulletin.org/saint-joseph-church-bogota-nj-07603']
group: 'Parish Mission Partners: Teaneck and Bogota'
evidence:
- url: https://church-bulletin.org/bulletin/saint-joseph-church-bogota-nj-07603/2026-11-01.pdf
  seen: 2026-11-03
  quote: 6032 St. Joseph, Bogota, NJ (back) John Patrick Publishing Company
  note: '1 November 2026 issue, 12 pages; pages 1-11 are images (rendered pages 1-2 with render.py; recheck
    can''t find quotes there), only the page-12 ad page has text. Page 1 masthead (image): ''ST. JOSEPH
    CHURCH'', ''115 East Fort Lee Road, Bogota NJ 07603'', ''11/01/2026'', ''Rev. Scott Attanasio, Pastor'',
    ''Rev. Eduardo Bustamante, Vicar'', ''Deacon Kevin Regan''; Saturday Eve 5pm, Sunday 8am, 10am & Spanish
    11:30am, Weekdays 8am, Civic Holidays 8am, Adoration Chapel Mon-Sat 8:30am-4pm. Page 2 (image): ''ST.
    JOSEPH''S MASS AND PRAYER SCHEDULE'', the same Masses; no other church named.'
- url: https://church-bulletin.org/6032
  seen: 2026-11-03
  note: John Patrick listing 'Saint Joseph Church Bulletin' (redirects to church-bulletin.org/saint-joseph-church-bogota-nj-07603),
    listing 104 weekly PDFs from 2024-11-10 to 2026-11-01.
- url: https://stjosephbogota.org/
  seen: 2026-11-03
  note: Parish WordPress site; its 'Current Bulletin' menu item links https://www.jppc.net/onlinebulletins/6032template.pdf,
    which redirects to the church-bulletin.org listing.
bulletin_status: available
publication_reviews:
- parish: st-anastasia-teaneck
  decision: separate
  evidence:
  - url: https://church-bulletin.org/bulletin/saint-joseph-church-bogota-nj-07603/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead (page 1, image) names St. Joseph Church, 115 East Fort Lee Road,
      Bogota alone, with Rev. Scott Attanasio, Pastor and its own Mass times; Teaneck is not mentioned.
  - url: https://files.ecatholic.com/25519/bulletins/20261025.pdf
    seen: 2026-11-03
    note: The 25 October 2026 masthead names St. Anastasia, 1095 Teaneck Road alone, with its own Mass
      schedule and pastor (Very Rev. Joseph D'Amico); Bogota is not mentioned.
---

## Publisher

John Patrick Publishing prints St. Joseph's weekly bulletin (id 6032). I read the 1 November 2026 issue: pages 1-11 are images (rendered pages 1-2), page 12 is the ad page with the footer '6032 St. Joseph, Bogota, NJ (back) John Patrick Publishing Company'. Page 1 masthead: 'ST. JOSEPH CHURCH', '115 East Fort Lee Road, Bogota NJ 07603', '11/01/2026', 'Rev. Scott Attanasio, Pastor', 'Rev. Eduardo Bustamante, Vicar', 'Deacon Kevin Regan'.

St. Joseph and St. Anastasia, Teaneck are 'Parish Mission Partners' (June 2026 letter, per the batch plan) and share Fr. Bustamante and Deacon Regan, but each has its own pastor and its own bulletin: St. Anastasia's 25 October eCatholic issue has its own masthead and never mentions Bogota, and this issue names only St. Joseph. Two rows, recorded as a `separate` peer review.

## Worship sites

- St. Joseph, 115 East Fort Lee Road (`st-joseph-bogota`): Saturday vigil 5pm; Sunday 8am, 10am, 11:30am (Spanish); Monday-Saturday 8am. The 'Adoration Chapel' on the masthead is for adoration (Mon-Sat 8:30am-4pm), not a separate Mass site.

The directory (13) and GCatholic (18369) list only this church.

## Website and bulletin provider

The parish site (stjosephbogota.org, WordPress) links jppc.net/onlinebulletins/6032template.pdf as 'Current Bulletin', which redirects to the church-bulletin.org listing. Provider `other`, pinned to `page-pdfs https://church-bulletin.org/6032` as the playbook says. The issues are image-only apart from the ad page, so the pipeline will need to read them as images.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/6032: current` and picked church-bulletin.org/bulletin/saint-joseph-church-bogota-nj-07603/2026-11-01.pdf, the 1 November 2026 issue read above; freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open.
