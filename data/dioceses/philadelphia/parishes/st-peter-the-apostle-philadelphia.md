---
name: St. Peter the Apostle Parish and National Shrine of St. John Neumann
website: https://spaphilly.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-peter-the-apostle-national-shrine-of-saint-john-neumann-philadelphia-pa-19123
publication: ['url:https://www.church-bulletin.org/saint-peter-the-apostle-national-shrine-of-saint-john-neumann-philadelphia-pa-19123']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-peter-the-apostle-national-shrine-of-saint-john-neumann-philadelphia-pa-19123
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 125, 'Saint Peter the Apostle & National Shrine of Saint John Neumann', 1019
    North Fifth Street, Philadelphia PA 19123, phone (215) 627-2386; newest dated issue October 25, 2026.
- url: https://www.church-bulletin.org/bulletin/saint-peter-the-apostle-national-shrine-of-saint-john-neumann-philadelphia-pa-19123/2026-10-25.pdf
  seen: 2026-10-29
  note: 'The 25 October 2026 issue (8 pages, text layer, md5 adffe3c2...): page 1 ''St. Peter the Apostle
    Church, National Shrine of St. John Neumann, A Redemptorist Parish, 1019 North 5th Street'', Rev.
    Michael Cunningham, CSsR, Pastor; Mass schedule Sat 12:15 p.m. and 5:30 p.m. vigil; Sunday English
    7:30, 9:30, 12:30 and Spanish 11:00; weekdays 7:30 a.m., 12:15 p.m., 5:30 p.m.; first Wednesday 7
    p.m.'
- url: https://spaphilly.org/bulletin-2/
  seen: 2026-10-29
  note: 'Parish WordPress site (visit.py --bulletin, verdict ok): its bulletin page''s newest file is
    2026-01-25.pdf (link-library-files), nine months behind the listing, so the listing is the current
    channel.'
- url: https://archphila.org/parish/st-peter-the-apostle-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 1 year ago): 5th St. and Girard Ave., Rev. Michael J. Cunningham, C.Ss.R.;
    includes the National Shrine of St. John Neumann, 1019 N. 5th St. Directory Mass times (Sat 5:30pm;
    Sun 9:30AM, 11:00AM Spanish, 12:30pm; weekdays 12:15pm and 5:30pm) omit the bulletin''s 7:30 a.m.
    Masses and Saturday 12:15.'
promoted: 2026-10-29
research:
- method: pnpm fetch:check --diocese philadelphia --parish st-peter-the-apostle-philadelphia (page-pdfs
    on John Patrick listing 125)
  url: https://www.church-bulletin.org/saint-peter-the-apostle-national-shrine-of-saint-john-neumann-philadelphia-pa-19123
  checked: '2026-10-29'
  outcome: found
  next_action: None
  retry_when: ''
bulletin_status: available
---

## Publisher

St. Peter the Apostle, with the National Shrine of St. John Neumann in the same church, prints with John Patrick Publishing: listing 125 has an issue for 25 October 2026 with a text layer. The parish's own WordPress archive stopped at 25 January 2026. The row is `other`, `page-pdfs` on the listing.

## Worship sites

One church, St. Peter the Apostle, 1019 North 5th Street, at 5th St. and Girard Ave.; the shrine is in the parish church (settled rule), so it has no row of its own. The bulletin's Mass schedule names no other site. GCatholic omits this church.

## Website and bulletin provider

`https://spaphilly.org` is the parish site (WordPress); its bulletin page is stale, so it is not the channel.

## Shared clergy

Redemptorist parish like Holy Name and Visitation B.V.M. (Fr. Mulvaney, Visitation's pastor, is listed as a missionary in residence here; Holy Name's bulletin refers religious education here). Different mastheads, Mass boxes and listings: separate rows.

## Not yet confirmed

Nothing open.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on listing 125 picked `2026-10-25.pdf`: transport ok, PDF, issue date 2026-10-25, fresh. Identity shows `unverified` only because no expected identity is supplied; the masthead was read from the issue as described above. It printed no `recipe` line, as the pinned `provider_id` already holds it.
