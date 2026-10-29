---
name: St. Anne Parish
website: https://www.stannephila.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-church-and-shrine-of-saint-anne-philadelphia-pa-19125
publication: ['url:https://www.church-bulletin.org/the-church-and-shrine-of-saint-anne-philadelphia-pa-19125']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/the-church-and-shrine-of-saint-anne-philadelphia-pa-19125/2026-10-25.pdf
  seen: 2026-10-29
  note: 'The 25 October 2026 issue (6 pages, image-only, md5 c4e49fa5...) rendered: page 1 masthead ''The
    Church and Shrine of Saint Anne, A Catholic - Christian Community, Port Richmond - Olde Richmond Neighborhoods,
    2328 East Lehigh Avenue, Philadelphia, PA 19125, October 24-25, 2026, 30th Sunday in Ordinary Time''.
    Page 2 gives the Mass schedule (Sat 5:00 PM; Sun 7:30 AM, 10:30 AM; weekdays 6:30 AM) and names St.
    Anne''s rectory and Rev. Dharshana Jayamanne, Parochial Administrator. It names no other church.'
- url: https://www.church-bulletin.org/the-church-and-shrine-of-saint-anne-philadelphia-pa-19125
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 154, 'The Church and Shrine of Saint Anne', Philadelphia PA 19125, newest
    dated issue 2026-10-25, older ones weekly back through 2026-10-04.
- url: https://www.stannephila.org/
  seen: 2026-10-29
  note: Parish eCatholic site (id 34036; answers 403 to probe url, loads in visit.py). Its only bulletin
    link, 'Bulletins', goes to jppc.net/onlinebulletins/154template.pdf; there is no /bulletins page hosting
    files, so the eCatholic id is not a publication.
- url: https://archphila.org/parish/st-anne-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 7 months ago): E. Lehigh Ave. and Memphis St., Rev. Lourdes Sri Dharshanna
    Jayamanne, Parochial Administrator; Vigil Saturdays 5 PM, Sundays 7:30 and 10:30 AM, which agrees
    with the bulletin.'
research:
- method: pnpm fetch:check --diocese philadelphia --parish st-anne-philadelphia (page-pdfs on John Patrick
    listing 154)
  url: https://www.church-bulletin.org/the-church-and-shrine-of-saint-anne-philadelphia-pa-19125
  checked: '2026-10-29'
  outcome: found
  next_action: None
  retry_when: ''
bulletin_status: available
---

## Publisher

St. Anne (the Church and Shrine of Saint Anne, Rev. Dharshana Jayamanne, Parochial Administrator) prints with John Patrick Publishing: listing 154 has an issue for 25 October 2026, and the parish's eCatholic home page links only the jppc template for 154. The issue is image-only; the rendered page 1 masthead and page 2 Mass schedule name this parish alone. The row is `other`, `page-pdfs` on the listing.

## Worship sites

One church, St. Anne, 2328 East Lehigh Avenue (the shrine is in the parish church, settled rule). The bulletin's Mass schedule lists no other site. The directory's address is the intersection E. Lehigh Ave. and Memphis St.

## Website and bulletin provider

`https://www.stannephila.org/` is the parish's eCatholic site (id 34036); it hosts no bulletin files, so `ecatholic:34036` stays out of `publication`.

## Not yet confirmed

Nothing open. The 25 October issue has no text layer, so `fetch:check` can only report publication identity as unverified; the masthead was read from the render.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (issue date inferred from the file name); identity `unverified` because the issue is image-only (the masthead was read from the render above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
