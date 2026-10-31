---
name: Saint Martha Parish
website: https://www.stmarthachurch.com
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-martha-parish-philadelphia-pa-19154
publication: ['url:https://www.church-bulletin.org/saint-martha-parish-philadelphia-pa-19154']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-martha-parish-philadelphia-pa-19154
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 200, 'Saint Martha Parish', Philadelphia, PA 19154 (11301 Academy Road, 215-632-3720);
    latest edition October 25, 2026, then October 18 and 11.
- url: https://www.church-bulletin.org/bulletin/saint-martha-parish-philadelphia-pa-19154/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages, image only, md5 b1f95da17ad899fe490b3d9daa91838c; pages 1-2
    rendered, so no quote). Page 1 cover: ''Saint Martha Parish'', ''Most Reverend Efren V. Esmilla, Priest
    Moderator'', ''Deacon Stephen A. Guckin, Parish Life Director'', 11301 Academy Road, 215.632.3720,
    www.stmarthachurch.com. Mass Schedule: Monday-Saturday 8:15am; Saturday Vigil 4:00pm; Sunday 8:00,
    10:00, Noon; Holy Days 7pm vigil day before, 8:15am and 12:00pm day of; Sensory Friendly Mass 4th
    Sunday of the month September to June, 1:30pm. Staff: Rev. Tariq Isaac parochial vicar. Names this
    parish alone.'
- url: https://www.stmarthachurch.com
  seen: 2026-10-29
  note: 'probe url 200: title ''Saint Martha Parish - 11301 Academy Road Philadelphia, PA 19154-3304'';
    links the jppc template 200 and the listing (church-bulletin.org/saint-martha-parish-philadelphia-pa-19154)
    and hosts no weekly PDF (its uploads are online-giving and archdiocesan insert files).'
- url: https://archphila.org/parish/st-martha-philadelphia/
  seen: 2026-10-28
  quote: Deacon Stephen Guckin (Parish Life Director)
  note: Directory Pastor line; Mass times match the bulletin cover (Sat vigil 4 PM; Sun 8, 10 AM, Noon;
    weekdays 8:15 AM). CatholicPhilly 2026-07-22 (cited by the batch plan, not re-read) reports the PLD
    appointment.
promoted: 2026-10-29
research:
- method: Read listing 200, rendered pages 1-2 of the 25 October image-only issue (no text layer), and
    the parish home page
  url: https://www.church-bulletin.org/saint-martha-parish-philadelphia-pa-19154
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

Saint Martha Parish prints with John Patrick Publishing: listing 200 (`church-bulletin.org/?id=200`) has an issue for 25 October 2026, image only, and the home page links the jppc template and the listing. The row is `other`, `page-pdfs` on the listing. The cover (rendered) names Most Rev. Efren V. Esmilla as Priest Moderator and Deacon Stephen A. Guckin as Parish Life Director, with the parish's own Mass schedule.

**Parish Life Director and other parishes.** Deacon Guckin leads St. Martha alone: the cover names no other parish and its Mass schedule is St. Martha's. The Far Northeast neighbours (Christ the King, Our Lady of Calvary, St. Anselm) publish their own issues under other pastors. Nothing here points to a shared bulletin.

## Worship sites

One: St. Martha Church, 11321 Academy Road (directory) / 'Academy Rd. south of Comly Rd.' (GCatholic). The cover's Mass schedule names no other place. The Sensory Friendly Mass (4th Sunday, 1:30pm) is at the same church as far as the cover says; the cover names no other building.

## Website and bulletin provider

stmarthachurch.com is the parish's own WordPress site; the weekly bulletin is on the listing only. Recipe `page-pdfs https://www.church-bulletin.org/saint-martha-parish-philadelphia-pa-19154`. The current issue is image only, so `fetch:check` reports identity `unverified`, by design.

## Not yet confirmed

The identity of the issue rests on the rendered cover, not a text layer.

## Fetch check

`fetch:check` (2026-10-29) with the pinned `page-pdfs` recipe picked `2026-10-25.pdf` on listing 200: transport ok, PDF, fresh (issue age 4 days, date inferred from the listing's file name; the issue is image only); identity `unverified` because the check is given no expected identity (masthead and Mass schedule read above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
