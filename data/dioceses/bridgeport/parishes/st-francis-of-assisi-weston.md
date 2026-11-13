---
name: St. Francis of Assisi
website: https://www.stfrancisweston.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-francis-of-assisi-parish-weston-ct-06883
publication: ['url:https://www.church-bulletin.org/saint-francis-of-assisi-parish-weston-ct-06883', 'ecatholic:19875']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-francis-of-assisi-parish-weston-ct-06883/2026-11-15.pdf
  seen: 2026-11-12
  note: '15 November 2026 issue, 8 pages, no text layer (read by rendering). Page 1 (image): ''St. Francis
    of Assisi Parish'', 35 Norfield Road, Weston, CT 06883, www.stfrancisweston.org; MASS SCHEDULE: Saturday
    Vigil 5:00 pm; Sunday 8:00 am, 9:30 am, 11:00 am; Daily Mass Tuesdays-Fridays 7:30 am, Saturdays 9:00
    am. Page 2: Fr. Augustine Nguyen, Pastor.'
- url: https://www.church-bulletin.org/saint-francis-of-assisi-parish-weston-ct-06883
  seen: 2026-11-12
  note: 'John Patrick Publishing''s church-bulletin.org listing for the parish: weekly PDFs through 2026-11-15.'
- url: https://www.stfrancisweston.org/bulletins
  seen: 2026-11-12
  note: 'visit.py: the eCatholic site (id 19875) links ''Bulletins'' to https://www.church-bulletin.org/st-francis-of-assisi-parish-weston-ct-06883,
    which serves only church-bulletin.org''s generic welcome page (no issues); the /bulletins page''s
    own files.ecatholic.com/19875/bulletins archive ends July 13, 2025.'
bulletin_status: available
---

## Publisher

St. Francis of Assisi, Weston publishes a weekly bulletin printed by John Patrick Publishing and listed on church-bulletin.org at `https://www.church-bulletin.org/saint-francis-of-assisi-parish-weston-ct-06883`. The 15 November 2026 issue (`https://www.church-bulletin.org/bulletin/saint-francis-of-assisi-parish-weston-ct-06883/2026-11-15.pdf`, read 2026-11-12 by rendering; it has no text layer) is headed "St. Francis of Assisi Parish, 35 Norfield Road, Weston, CT 06883" and gives one Mass schedule: Saturday Vigil 5:00 pm; Sunday 8:00, 9:30 and 11:00 am; daily Tuesday-Friday 7:30 am and Saturday 9:00 am. Page 2 names Fr. Augustine Nguyen, Pastor.

Until July 2025 the parish posted its bulletin on its eCatholic site (`files.ecatholic.com/19875/bulletins/`, newest 13 July 2025), the same parish's earlier channel, so `ecatholic:19875` stays in `publication`.

## Worship sites

One church, `st-francis-of-assisi-weston`; the schedule names no other place. The diocese directory's "October through May only" note marks one seasonal Mass time at the same church.

## Website and bulletin provider

Provider `other`, pinned with `page-pdfs` to the church-bulletin.org listing. The parish site's own Bulletins link goes to `church-bulletin.org/st-francis-of-assisi-parish-weston-ct-06883` ("st-"), which shows only the publisher's generic page; the working listing uses "saint-", found by trying slug variants on 2026-11-12. The bulletin has no text layer, so the pipeline has to read it as images.

`fetch:check` on 2026-11-12 (recipe `page-pdfs https://www.church-bulletin.org/saint-francis-of-assisi-parish-weston-ct-06883`) picked `https://www.church-bulletin.org/bulletin/saint-francis-of-assisi-parish-weston-ct-06883/2026-11-15.pdf`, the 15 November 2026 issue read above.

## Not yet confirmed

Nothing open for this row.
