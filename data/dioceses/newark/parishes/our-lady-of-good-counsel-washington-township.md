---
name: Our Lady of Good Counsel, Washington Township
website: https://www.olgcwt.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/586
publication: ['url:https://www.church-bulletin.org/our-lady-of-good-counsel-roman-catholic-church-washington-township-nj-07675']
group: Planning Area B
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-roman-catholic-church-washington-township-nj-07675/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 (Solemnity of All Saints - 11/01/26) issue, 8 pages, image-only (no text layer;
    page 1 rendered with render.py). Masthead: Our Lady of Good Counsel, 668 Ridgewood Road, Washington
    Township, New Jersey 07676; MASS SCHEDULE Saturday 5:00pm; Sunday 8:00am, 10:30am, 12:00pm, 6:00pm;
    Daily 8:45am; Rev. Raymond Rodrigue, Pastor. No other church named.'
- url: https://www.church-bulletin.org/our-lady-of-good-counsel-roman-catholic-church-washington-township-nj-07675
  seen: 2026-11-03
  note: John Patrick Publishing listing (church-bulletin.org/586 redirects here) headed Our Lady of Good
    Counsel Roman Catholic Church, Washington Township NJ; dated PDFs newest first, 2026-11-01.pdf, 2026-10-25.pdf,
    2026-10-18.pdf ...
- url: https://www.olgcwt.org/
  seen: 2026-11-03
  quote: Click For This Week
  note: Parish WordPress homepage; the button 'Click For This Week's Bulletin' links https://www.jppc.net/onlinebulletins/586template.pdf
    (John Patrick id 586).
bulletin_status: available
---

## Publisher

Our Lady of Good Counsel, 668 Ridgewood Road, Washington Township, publishes its own weekly bulletin through John Patrick Publishing (id 586). I read page 1 of the 1 November 2026 issue (image-only, rendered): the masthead names Our Lady of Good Counsel alone, with its own Mass schedule and staff (Rev. Raymond Rodrigue, Pastor).

## Worship sites

- Our Lady of Good Counsel Church, 668 Ridgewood Road (`our-lady-of-good-counsel-washington-township`): every Mass in the schedule (Saturday 5:00pm; Sunday 8:00, 10:30am, 12:00, 6:00pm; daily 8:45am).

The directory (206) and GCatholic (18574) list only this church, and the issue names no chapel or mission.

## Website and bulletin provider

The directory's https://www.olgcwt.org/ (WordPress) answers `probe get`; its bulletin button links `jppc.net/onlinebulletins/586template.pdf`. church-bulletin.org/586 redirects to the dated listing, read with a pinned `page-pdfs` recipe (provider `other`). The issue has no text layer, so the pipeline must read it as images. GCatholic gives the same domain.

Fetch check (2026-11-03, headed browser): `page-pdfs on https://church-bulletin.org/586: current`, transport ok, PDF, picked `.../2026-11-01.pdf` (`fresh`), the 1 November issue read above. Recipe pinned in `provider_id`.

## Not yet confirmed

Nothing open.
