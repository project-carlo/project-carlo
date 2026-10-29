---
name: St. Mary Magdalen
website: https://www.stmarymagdalen.net/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-magdalen-parish-media-pa-19063
publication: ['url:https://www.church-bulletin.org/saint-mary-magdalen-parish-media-pa-19063']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-magdalen-parish-media-pa-19063/2026-10-25.pdf
  seen: 2026-10-28
  note: 'The 25 October 2026 issue (12 pages, image only, pages 1-2 rendered and read). Page 1 masthead:
    ''Saint Mary Magdalen Church ... 25 OCTOBER 2026, THIRTIETH SUNDAY IN ORDINARY TIME ... 2400 N. PROVIDENCE
    ROAD, MEDIA, PENNSYLVANIA''. Page 2 ''PARISH MASS & CONFESSION SCHEDULE'': Sunday 7:30 AM, 9:30 AM,
    11:30 AM & 7 PM; weekdays Tuesday through Friday 6:30 AM & 8:30 AM, Monday 8:30 AM; Saturday 8:30
    AM & 4:30 PM Anticipated Mass; plus an Adoration Chapel open 24 hours. Clergy list: Rev. Kenneth L.
    Cavara, Pastor. It names no other church. md5 63c0ce52b460c461f330841dd154c73d.'
- url: https://www.church-bulletin.org/saint-mary-magdalen-parish-media-pa-19063
  seen: 2026-10-28
  note: John Patrick listing 35 'Saint Mary Magdalen Parish', Media PA 19063, 2400 North Providence Road,
    phone (610) 566-8821; Latest Edition October 25, 2026, then Oct 18 and Oct 11.
- url: https://www.stmarymagdalen.net/events/bulletins
  seen: 2026-10-28
  note: The parish's own Wix page lists 57 dated issues as links to /_files/ugd/2b3272_<hash>.pdf, the
    first headed 'OCTOBER 25, 2026' (2b3272_ab73b0683f614abeb8dd8642e3ac9ff5.pdf), and also links the
    printer's listing (church-bulletin.org/?id=035). That file (read with probe get) is byte-identical
    (md5 63c0ce52b460c461f330841dd154c73d) to the listing's 25 October PDF, so the two channels carry
    one document.
- url: https://archphila.org/parish/st-mary-magdalen-media/
  seen: 2026-10-28
  note: 'Directory (page updated about four months earlier): ''Pastor: Rev. Kenneth L. Cavara'', rectory
    2400 N. Providence Rd., Mass times Saturday 4:30 PM, Sunday 7:30, 9:30, 11:30 AM and 7:00 PM, weekdays
    6:30 and 8:30 AM, Saturday 8:30 AM; no worship site named.'
---

## Publisher

St. Mary Magdalen, Media publishes its own weekly bulletin, printed by John Patrick Publishing (listing 35). The 25 October 2026 issue (image only, 12 pages; pages 1-2 rendered) has a cover headed 'Saint Mary Magdalen Church' with the pastor's letter, and page 2 gives the parish's own Mass and confession schedule.

## Worship sites

One: St. Mary Magdalen Church, 2400 N. Providence Road (see `churches/st-mary-magdalen-media`). The Mass schedule lists no other location. The Adoration Chapel, open 24 hours for personal prayer with Exposition Tuesday 9 AM to Thursday 2 PM, lists no Mass of its own, so it is not a separate church row.

## Website and bulletin provider

stmarymagdalen.net is a Wix site. Its /events/bulletins page posts each issue as a `/_files/ugd/` PDF with the date as button text, and links the listing; the newest file is byte-identical to the listing's. The row follows the listing with recipe `page-pdfs https://www.church-bulletin.org/saint-mary-magdalen-parish-media-pa-19063`, as the listing's file names are dated and the Wix file names are not. The issues are image-only, so `fetch:check` can't verify the masthead from text.

## Not yet confirmed

Pages 3-12 of the issue were not read.
