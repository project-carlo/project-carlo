---
name: Holy Name of Jesus Parish
website: https://holynameofjesusparish.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/holy-name-of-jesus-philadelphia-pa-19125
publication: ['url:https://www.church-bulletin.org/holy-name-of-jesus-philadelphia-pa-19125']
group: ''
evidence:
- url: https://www.church-bulletin.org/holy-name-of-jesus-philadelphia-pa-19125
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 283, 'Holy Name of Jesus', 701 Gaul Street, Philadelphia PA 19125, phone
    (215) 739-3960; newest dated issue October 25, 2026, weekly back through at least November 2024.
- url: https://www.church-bulletin.org/bulletin/holy-name-of-jesus-philadelphia-pa-19125/2026-10-25.pdf
  seen: 2026-10-29
  note: 'The 25 October 2026 issue (6 pages, text layer, md5 14c952af...): page 1 headed ''Holy Name of
    Jesus, Rev. Alfred E. Bradley, C.Ss.R., Parochial Administrator, 701 Gaul St.'' with a single Mass
    box (Sat vigil 4:30 p.m.; Sunday 9:00 a.m.; Mon-Fri 9:00 a.m.; confessions Sat 3:30-4:15 p.m.). The
    only mention of St. Laurentius is ''St. Laurentius School of Holy Name Parish, 1608 E. Berks Street''
    and school news; no Mass is listed there.'
- url: https://holynameofjesusparish.org/about
  seen: 2026-10-29
  note: 'Parish site (visit.py; the directory''s holynameofjesus-fishtown.org fails TLS verification for
    probe url and redirects in the browser to holynameofjesusparish.org). Mass Times: Saturday 4:30PM;
    Sunday 9AM; Daily Mon-Fri 9AM; location 701 Gaul St. No bulletin link or PDF; its only other link
    is the St. Laurentius School site.'
- url: https://archphila.org/parish/holy-name-of-jesus-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 2 years ago): E. Berks and Gaul Sts., Rev. Alfred E. Bradley, C.Ss.R.;
    lists Sunday 8 and 11 AM and a Saturday 4:30 PM vigil. The Sunday times are stale: the bulletin and
    the parish site give 9 AM only.'
promoted: 2026-10-29
research:
- method: pnpm fetch:check --diocese philadelphia --parish holy-name-of-jesus-philadelphia (page-pdfs
    on John Patrick listing 283)
  url: https://www.church-bulletin.org/holy-name-of-jesus-philadelphia-pa-19125
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
    note: The 25 October 2026 masthead names St. Peter the Apostle Church and National Shrine of St. John
      Neumann, 1019 North 5th Street, alone (listing 125, 8 pages, md5 adffe3c2...), with its own Mass
      box (Sat 12:15 and 5:30; Sun 7:30, 9:30, 11:00, 12:30) under Rev. Michael Cunningham. Holy Name's
      own issue (listing 283, md5 14c952af...) names Holy Name of Jesus, 701 Gaul St., with Sat 4:30 and
      Sun 9:00, and only points religious-education enquiries to St. Peter's.
- parish: visitation-bvm-philadelphia
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/visitation-bvm-parish-philadelphia-pa-19125/2026-10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead names Visitation BVM Church, 2625 B Street, alone (listing 57,
      6 pages, md5 872db27c...), with a trilingual Mass box (Sat 5 pm; Sun 8, 9:30, 10, 11) and a pastor's
      column; it lists no Mass at Holy Name.
---

## Publisher

Holy Name of Jesus (Rev. Alfred E. Bradley, C.Ss.R., Parochial Administrator) prints with John Patrick Publishing: listing 283 has an issue for 25 October 2026 with a text layer. Its site hosts no bulletin. The row is `other`, `page-pdfs` on the listing.

## Worship sites

One church, Holy Name of Jesus, E. Berks and Gaul Sts. (rectory and church office 701 Gaul St.). The directory calls St. Laurentius (Polish), Memphis and E. Berks Sts., a worship site, but the bulletin and the parish site list Mass only at Holy Name, and St. Laurentius Church has been closed since March 2014 and was sold in 2020 (see `excluded/st-laurentius-philadelphia`). Only St. Laurentius School, 1608 E. Berks St., remains.

## Website and bulletin provider

The directory's `HolyNameofJesus-Fishtown.org` fails TLS verification under `probe url` and redirects in a real browser to `https://holynameofjesusparish.org/`, an own-built site with Mass times and no bulletin page. The row's website is that address.

## Shared clergy

Fr. Bradley is a Redemptorist, as are the clergy of St. Peter the Apostle and Visitation B.V.M.; the Holy Name bulletin sends religious-education enquiries to St. Peter's. The mastheads, Mass boxes and listings (283, 125, 57) differ: separate rows.

## Not yet confirmed

Nothing open.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on listing 283 picked `2026-10-25.pdf`: transport ok, PDF, issue date 2026-10-25, fresh. Identity shows `unverified` only because no expected identity is supplied; the masthead was read from the issue as described above. It printed no `recipe` line, as the pinned `provider_id` already holds it.
