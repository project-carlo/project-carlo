---
name: St. Anastasia, Teaneck
website: https://www.saintanastasia.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:25519']
group: 'Parish Mission Partners: Teaneck and Bogota'
evidence:
- url: https://files.ecatholic.com/25519/bulletins/20261025.pdf
  seen: 2026-11-03
  quote: 1095 TEANECK ROAD | TEANECK, NEW JERSEY 07666
  note: '25 October 2026 issue (8 pages, text layer, parish-made; no publisher footer). Page 1 masthead
    ''SUNDAY, OCTOBER 25, 2026'', ''CHURCH OF St. Anastasia'', Mass schedule Saturday evening 5:00 p.m.;
    Sunday 8:00 a.m., 10:00 a.m., 11:30 a.m. (Family Mass), 1:00 p.m. (Spanish); daily 8:30 a.m. Page
    2 ''Served By'' names Very Reverend Joseph D''Amico, V.F., Pastor and Reverend Eduardo Bustamante,
    Parochial Vicar. No mention of Bogota or St. Joseph (grep ''Bogota'': 0 hits).'
- url: https://www.saintanastasia.org/bulletins
  seen: 2026-11-03
  note: 'eCatholic bulletin page (read with visit.py --follow /bulletins --links) lists weekly issues
    newest first: October 25, 2026 (files.ecatholic.com/25519/bulletins/20261025.pdf), October 18, October
    11, October 4, September 27 ... The 1 November issue was not yet posted on 3 November (issues.py:
    20261101.pdf answers 403).'
- url: https://www.saintanastasia.org/mass-times
  seen: 2026-11-03
  quote: 1095 Teaneck Rd, Teaneck, NJ 07666
  note: 'Parish Mass times page: Saturday 5:00 PM; Sunday 8:00 AM, 10:00 AM, 11:30 AM, 1:00 PM Spanish;
    Mon-Sat 8:30 AM.'
- url: https://church-bulletin.org/bulletin/saint-joseph-church-bogota-nj-07603/2026-11-01.pdf
  seen: 2026-11-03
  note: 'Partner parish St. Joseph, Bogota''s own 1 November 2026 John Patrick bulletin (image-only page
    1, rendered): masthead names ST. JOSEPH CHURCH, 115 East Fort Lee Road, Bogota alone, with Rev. Scott
    Attanasio, Pastor and Rev. Eduardo Bustamante, Vicar, and its own Mass times. The two parishes share
    a vicar but not a bulletin.'
promoted: 2026-11-05
bulletin_status: available
publication_reviews:
- parish: st-joseph-bogota
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/25519/bulletins/20261025.pdf
    seen: 2026-11-03
    note: The 25 October 2026 masthead names St. Anastasia, 1095 Teaneck Road alone, with its own Mass
      schedule and pastor (Very Rev. Joseph D'Amico); Bogota is not mentioned.
  - url: https://church-bulletin.org/bulletin/saint-joseph-church-bogota-nj-07603/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead (page 1, image) names St. Joseph Church, 115 East Fort Lee Road,
      Bogota alone, with Rev. Scott Attanasio, Pastor and its own Mass times; Teaneck is not mentioned.
---

## Publisher

St. Anastasia makes its own weekly bulletin (8 pages, text layer, no publisher footer) and posts it on its eCatholic site (site id 25519). I read the 25 October 2026 issue: page 1 masthead 'SUNDAY, OCTOBER 25, 2026', 'CHURCH OF St. Anastasia', '1095 TEANECK ROAD | TEANECK, NEW JERSEY 07666', with one Mass schedule; page 2 'Served By' names Very Reverend Joseph D'Amico, V.F., Pastor, Reverend Eduardo Bustamante, Parochial Vicar, and Deacon Kevin Regan.

The batch plan notes St. Anastasia and St. Joseph, Bogota are 'Parish Mission Partners' (June 2026 letter) sharing a parochial vicar. The bulletins confirm the shared vicar (Fr. Bustamante) and deacon (Kevin Regan) but not a shared bulletin: St. Anastasia's 25 October issue never mentions Bogota, and St. Joseph's 1 November John Patrick issue (church-bulletin.org/6032) has its own masthead, its own pastor (Rev. Scott Attanasio) and its own Mass times. Two rows, recorded as a `separate` peer review.

## Worship sites

- St. Anastasia, 1095 Teaneck Road (`st-anastasia-teaneck`): Saturday 5:00pm; Sunday 8:00am, 10:00am, 11:30am (Family Mass), 1:00pm (Spanish); daily 8:30am.

The directory (193) and GCatholic (18561) list only this church; the bulletin names no other site.

## Website and bulletin provider

https://www.saintanastasia.org/ is the parish's eCatholic site; its /bulletins page lists weekly issues at files.ecatholic.com/25519/bulletins/<yyyymmdd>.pdf, newest 25 October 2026 on 3 November (the 1 November file answered 403, so this parish posts late or skipped a week). Provider `ecatholic`.

Fetch check (2026-11-03, headed): transport ok, PDF, picked files.ecatholic.com/25519/bulletins/20261025.pdf (the 25 October 2026 issue read above), freshness fresh (9 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it.

## Not yet confirmed

Nothing open. The 1 November issue was not yet posted; the 25 October one is the newest.
