---
name: Visitation B.V.M. Parish
website: https://www.visitationbvm.net
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/visitation-bvm-parish-philadelphia-pa-19125
publication: ['url:https://www.church-bulletin.org/visitation-bvm-parish-philadelphia-pa-19125']
group: ''
evidence:
- url: https://www.church-bulletin.org/visitation-bvm-parish-philadelphia-pa-19125
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 57, 'Visitation BVM Parish', 2625 B Street, Philadelphia PA 19125, phone
    (215) 634-1133; newest dated issue October 25, 2026, weekly issues back through at least November
    2024.
- url: https://www.church-bulletin.org/bulletin/visitation-bvm-parish-philadelphia-pa-19125/2026-10-25.pdf
  seen: 2026-10-29
  note: 'The 25 October 2026 issue (6 pages, text layer, md5 872db27c...): page 2 headed ''Visitation
    BVM Church, 2625 B Street, Philadelphia, PA 19125, Rectory: 215-634-1133, Visitationbvm.net'' with
    one trilingual Mass box (Sat vigil 5 pm; Sun 8 am Spanish, 9:30 English, 10 Spanish, 11 Vietnamese;
    weekdays 8:00 am Mon-Sat; 7 pm Tuesday and Wednesday Spanish; confessions Sat 4-5 pm, Lower Church).
    It names no other church.'
- url: https://visitationbvm.net/
  seen: 2026-10-29
  note: Parish site (visit.py, verdict ok). It embeds no bulletin id; visit.py --bulletin found its bulletin
    link on the John Patrick listing 57 and its dated PDFs (2026-10-25, 2026-10-18, ...), so the listing
    is the channel.
- url: https://archphila.org/parish/visitation-bvm-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 2 years ago): Lehigh Ave. and B St., Rev. Francis D. Mulvaney, C.Ss.R.,
    rectory 2625 B St.; Sunday Masses 8 Spanish, 9:30 English, 10 Spanish (upper church), 11 Vietnamese,
    which agrees with the bulletin.'
promoted: 2026-10-29
research:
- method: pnpm fetch:check --diocese philadelphia --parish visitation-bvm-philadelphia (page-pdfs on John
    Patrick listing 57)
  url: https://www.church-bulletin.org/visitation-bvm-parish-philadelphia-pa-19125
  checked: '2026-10-29'
  outcome: found
  next_action: None
  retry_when: ''
bulletin_status: available
publication_reviews:
- parish: st-peter-the-apostle-philadelphia
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-peter-the-apostle-national-shrine-of-saint-john-neumann-philadelphia-pa-19123/2026-10-25.pdf
    seen: 2026-10-29
    note: St. Peter's issue (listing 125) has its own masthead, address (1019 North 5th Street), pastor
      and Mass box (Sat 12:15, 5:30; Sun 7:30, 9:30, 11:00, 12:30). It lists Fr. Francis Mulvaney, CSsR,
      only among the 'Missionaries In-Residence'; Visitation's issue (listing 57) carries its own Mass
      box at 2625 B Street.
---

## Publisher

Visitation B.V.M. (Rev. Francis D. Mulvaney, C.Ss.R., rectory 2625 B Street) prints with John Patrick Publishing: listing 57 has an issue for 25 October 2026 with a text layer, and the parish's own site leads to it. The row is `other`, `page-pdfs` on the listing.

## Worship sites

One church, Visitation B.V.M., 2625 B Street. The bulletin's single Mass box covers it; the directory's 'lower church', 'upper church' and chapel are rooms of the same building. GCatholic's 'Visitation of the Child Jesus, E Lehigh Ave. & B St.' (phone +1 215 634-1133, the rectory's number) is this church, not a second one.

## Website and bulletin provider

`https://www.visitationbvm.net` (redirects to visitationbvm.net) hosts no bulletin files and embeds no publisher id; it links the John Patrick listing.

## Shared clergy

The parish and St. Peter the Apostle (1019 N. 5th St.) and Holy Name of Jesus are all Redemptorist parishes (Fr. Mulvaney is listed 'in residence' at St. Peter; Fr. Bradley, C.Ss.R., is Holy Name's administrator). Their bulletins have different mastheads, Mass boxes and listings (57, 125, 283): separate rows.

## Not yet confirmed

Nothing open.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on listing 57 picked `2026-10-25.pdf`: transport ok, PDF, issue date 2026-10-25, fresh. Identity shows `unverified` only because no expected identity is supplied; the masthead was read from the issue as described above. It printed no `recipe` line, as the pinned `provider_id` already holds it.
