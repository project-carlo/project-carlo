---
name: The Parish Family of St. Bernard
website: https://stbernard-mayfair.wixsite.com/website
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-parish-family-of-saint-bernard-church-philadelphia-pa-19136
publication: ['url:https://www.church-bulletin.org/the-parish-family-of-saint-bernard-church-philadelphia-pa-19136']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/the-parish-family-of-saint-bernard-church-philadelphia-pa-19136/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (6 pages, image only; page 1 rendered, so cited as a note). Header ''The
    Parish Family of St. Bernard'', 7341 Cottage Street, Philadelphia 19136, Parish Office 215-333-0446,
    Pastor Rev. Joseph N. Accardi. Mass Schedule: Saturday vigil 5:00 p.m.; Sunday 8:30 a.m., 10:30 a.m.
    and 4:30 p.m.; daily 8:00 a.m. Monday through Saturday; Holy Day vigil 7:00 p.m., 8:00 a.m. and 12
    noon. It names this parish alone.'
- url: https://www.church-bulletin.org/the-parish-family-of-saint-bernard-church-philadelphia-pa-19136
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 93, 'The Parish Family of Saint Bernard Church', Philadelphia, PA 19136;
    latest edition October 25, 2026, then 2026-10-18 and 2026-10-11.
- url: https://stbernard-mayfair.wixsite.com/website
  seen: 2026-10-29
  note: 'probe url and Chrome: 200, a Wix page (''Catholic Church | St. Bernard Church''). Its ''Previous
    Bulletins'' page links filesusr.com PDFs oldest first (7 June 2026 first, 1 November 2026 last). The
    25 October file (md5 f4ad49d3037afafb8caac2473e0833d8, text layer) is not byte-identical to the listing''s
    image-only 6-page issue (md5 1d99fda24b0cb555f5a09695d0798038), and page-pdfs would pick a stale first
    link, so the listing stays the channel.'
- url: https://archphila.org/parish/st-bernard-philadelphia/
  seen: 2026-10-28
  quote: Rev. Joseph N. Accardi
  note: 'Directory: Pastor Rev. Joseph N. Accardi, church at Cottage and Bleigh Sts., rectory 7341 Cottage
    St. 19136; Mass times match the bulletin.'
research:
- method: Read listing 93, rendered pages 1 of the 25 October issue, opened the parish site
  url: https://www.church-bulletin.org/the-parish-family-of-saint-bernard-church-philadelphia-pa-19136
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Bernard, Philadelphia prints with John Patrick Publishing: listing 93 has an issue for 25 October 2026 (image only). The parish's Wix site holds a 'Previous Bulletins' page of self-uploaded files, but oldest first and ending with next Sunday's issue, so `page-pdfs` on it would read June 2026. The row is `other`, `page-pdfs` on the listing. Separate bulletin from St. Matthew (276) and St. Timothy and St. Bartholomew (116).

## Worship sites

One: St. Bernard Church, Cottage and Bleigh Sts. The Mass schedule lists no other place.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (date inferred from the listing file name); identity `unverified` because the check is given no expected identity (masthead and Mass schedule read above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
