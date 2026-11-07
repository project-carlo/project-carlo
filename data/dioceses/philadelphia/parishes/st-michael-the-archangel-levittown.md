---
name: St. Michael the Archangel Parish
website: https://stmichaellvt.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-michael-the-archangel-church-levittown-pa-19054
publication: ['url:https://www.church-bulletin.org/saint-michael-the-archangel-church-levittown-pa-19054']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-michael-the-archangel-church-levittown-pa-19054
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 217, 'Saint Michael the Archangel Church', Levittown, PA 19054; latest edition
    October 25, 2026, then 2026-10-18.
- url: https://www.church-bulletin.org/bulletin/saint-michael-the-archangel-church-levittown-pa-19054/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (8 pages, image only; page 1 rendered at 60 dpi and read). Cover: ''Saint
    Michael the Archangel Church, 66 Levittown Parkway, Levittown, PA 19054'', ''Pastor: Reverend Jonathan
    Dalin''; ''MASS SCHEDULE: Masses Tuesday thru Saturday 8:00 am Celebrated in the Chapel; Saturday
    Vigil Mass: 4:30 pm; Sunday: 8:00 am, 10:00 am, 12:00 Noon''; ''Adoration: Every Friday from 8:30
    to 6:00pm in the Chapel (September - June)''. Names this parish alone.'
- url: https://www.church-bulletin.org/bulletin/saint-michael-the-archangel-church-levittown-pa-19054/2026-09-06.pdf
  seen: 2026-10-29
  quote: 'Pastor: Reverend Jonathan Dalin'
  note: 6 September 2026 issue has a text layer with the same cover box. The Pastor's Desk letter says
    daily Mass is 'at 8 AM in Saint Michael the Archangel Chapel' from 1 September and that the Saturday
    vigil moves to 4:00 PM from 28 November. It names no other Mass place.
- url: https://stmichaellvt.com/
  seen: 2026-10-29
  note: The directory's stmichaellvt.org redirects here (the title is 'Saint Michael the Archangel Church
    – 66 Levittown Parkway Levittown, PA 19054'); probe url alone read it as NO-PARISH-WORDS and visit.py
    loaded it. Its only bulletin link is http://www.jppc.net/onlinebulletins/217template.pdf, the listing,
    with no embedded publication id.
- url: https://archphila.org/parish/st-michael-the-archangel-levittown/
  seen: 2026-10-28
  quote: 66 Levittown Pkwy., Levittown
  note: 'Directory: Pastor Rev. Jonathan J. Dalin; rectory 66 Levittown Pkwy., Levittown 19054; Mass times
    ''Vigil Mass, Saturdays, 4:30 PM. Sundays, 8, 10 AM; Noon''; no worship sites or merger named.'
promoted: 2026-10-29
research:
- method: Read listing 217, rendered page 1 of the 25 October image-only issue, read the 6 September text
    layer and searched issues of 2024-11-03, 2025-06-01, 2026-01-04, 2026-06-07 and 2026-09-06 for 'Tullytown'
    and 'Sacred Heart of Jesus'
  url: https://www.church-bulletin.org/saint-michael-the-archangel-church-levittown-pa-19054
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Michael the Archangel Parish, Levittown, prints with John Patrick Publishing: listing 217 (`church-bulletin.org/?id=217`) has an issue for 25 October 2026 (image only). The row is `other`, `page-pdfs` on the listing. The cover names this parish alone.

## Worship sites

One church: St. Michael the Archangel, 66 Levittown Parkway (OpenStreetMap files it under Lakeside, Tullytown). The 'Chapel' in the Mass box is where weekday Mass and Friday adoration are held ('Saint Michael the Archangel Chapel', 6 September letter); no source gives it another address, so it is a room of the church campus and its Masses go on the church row (playbook rule). **Sacred Heart of Jesus, Tullytown**, whose GCatholic pin is about 500 m away, is not named in any of the five text-layer issues searched; see `open/sacred-heart-of-jesus-tullytown`.

## Website and bulletin provider

The directory's stmichaellvt.org redirects to stmichaellvt.com, whose only bulletin link is the listing's jppc template (217); probe url read it as NO-PARISH-WORDS (JavaScript) and visit.py loaded it. Recipe `page-pdfs https://www.church-bulletin.org/saint-michael-the-archangel-church-levittown-pa-19054`.

## Not yet confirmed

Only page 1 of the image-only 25 October issue was rendered; the text-layer 6 September issue was searched for other Mass places.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (issue age 4 days, date inferred from the listing's file name); identity `unverified` and 'First page has no extractable text' because the issue is image only (page 1 was rendered and read above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
