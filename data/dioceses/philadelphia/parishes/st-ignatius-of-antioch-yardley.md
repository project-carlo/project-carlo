---
name: St. Ignatius of Antioch Parish
website: http://www.stignatius.church
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-ignatius-of-antioch-church-yardley-pa-19067
publication: ['url:https://www.church-bulletin.org/saint-ignatius-of-antioch-church-yardley-pa-19067']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-ignatius-of-antioch-church-yardley-pa-19067
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 245 (church-bulletin.org/?id=245), 'Saint Ignatius of Antioch Church', Yardley,
    PA 19067, 999 Reading Avenue, phone (215) 493-3377; latest edition October 25, 2026.
- url: https://www.church-bulletin.org/bulletin/saint-ignatius-of-antioch-church-yardley-pa-19067/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages, image-only; md5 c1e9c0f6c3db17ebc2a53e30f8be83d7). Rendered
    page 1 masthead: ''St. Ignatius of Antioch Church, 999 Reading Avenue Yardley, PA ... The Thirtieth
    Sunday in Ordinary Time, October 25, 2026''; ''SCHEDULE OF MASSES: Saturday: 5:15PM Vigil Mass; Sunday:
    7:30AM, 9:30AM, 11:30AM and 6PM; Daily, Monday to Friday: 7:00AM''. Page 2 Mass intentions list only
    ''Parishioners of St. Ignatius''. Names this parish alone.'
- url: http://www.stignatius.church/Bulletins/2026/Bulletin-October-25-2026.pdf
  seen: 2026-10-29
  quote: 'Sunday: 7:30AM, 9:30AM, 11:30AM and 6PM'
  note: 'The parish''s own copy of the same Sunday: 10 pages with a text layer (md5 340833e91d76b5bd0a8d8e6f8bd3644c),
    not byte-identical to the listing''s 12-page image-only file, same masthead and Mass schedule.'
- url: http://www.stignatius.church/bulletin.html
  seen: 2026-10-29
  note: 'Parish site Bulletin page: ''Read Our Current Bulletin'' links http://www.jppc.net/onlinebulletins/245template.pdf
    (the listing) and an archive of Bulletins/<yyyy>/Bulletin-<Month>-<dd>-<yyyy>.pdf links, ordered by
    month then by year, not newest first.'
- url: https://archphila.org/parish/st-ignatius-of-antioch-yardley/
  seen: 2026-10-29
  quote: Rev. Andrew C. Brownholtz
  note: 'Directory: pastor; 999 Reading Ave., Yardley 19067-1626; Bucks County Central and North deanery;
    Mass times match the bulletin (page last updated 2 years ago).'
research:
- method: Compared the listing's 25 October PDF with the parish site's same-date file; read the site's
    Bulletin page
  url: http://www.stignatius.church/bulletin.html
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Ignatius of Antioch Parish, Yardley (Rev. Andrew C. Brownholtz, Pastor) prints with John Patrick Publishing: listing 245 (`church-bulletin.org/?id=245`) has an issue for 25 October 2026. The PDF has no text layer; the masthead and Mass schedule were read from the rendered page 1. It names this parish alone.

The parish site also hosts its own copy of each issue (`stignatius.church/Bulletins/2026/Bulletin-October-25-2026.pdf`, 10 pages, text layer), the same Sunday with the same masthead and schedule but not byte-identical to the listing's file. Its Bulletin page lists the archive by month, so `page-pdfs` on it would pick a January issue first; the row uses the listing, whose 'Latest Edition' is the current Sunday.

## Worship sites

One church, St. Ignatius, 999 Reading Avenue. The bulletin's Adoration Chapel (hours Monday to Saturday, call 215-550-5638 for openings) is a room of the church with no Mass listed. The directory's cemetery line (River Rd., Yardley) is a burial ground, not a Mass site.

## Website and bulletin provider

`http://www.stignatius.church` (the directory's URL) is the parish's own site.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (date inferred from the listing's file name); identity `unverified` because the PDF has no text layer to match, so the masthead was read by hand above. It printed no `recipe` line, as the pinned `provider_id` already holds it.
