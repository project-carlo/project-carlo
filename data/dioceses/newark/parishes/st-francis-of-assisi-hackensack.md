---
name: St. Francis of Assisi, Hackensack
website: https://stfrancisofassisihackensack.com/
bulletin_provider: parishes_online
provider_id: st-francis-of-assisi-church-07601
publication: ['po-org:st-francis-of-assisi-church-07601', 'lpi:0018000000QxABgAAN', 'po-container:03/4011']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/4011/20261101B.pdf
  seen: 2026-11-03
  note: 'Page 1 of the 1 November 2026 issue (pages 1-7 are images with no text layer; read rendered with
    parish-site-access render.py). Masthead shows ST. FRANCIS OF ASSISI CATHOLIC CHURCH, "NOVEMBER 1ST,
    2026 ALL SAINTS DAY", contact "Saint Francis of Asisi, 50 Lodi Street, Hackensack, NJ 07601", website
    stfrancisofassisihackensack.com. MASS SCHEDULE: Saturday 8AM, 5:30PM (EN), 7PM (SP); Sunday 8AM (EN/SP),
    9:30AM (IT), 11AM (EN), 12:30PM (SP); Monday-Saturday 8AM (EN); Mon, Wed, Thurs 7PM (SP); 4th Friday
    7PM (IT).'
- url: https://container.parishesonline.com/bulletins/03/4011/20261101B.pdf
  seen: 2026-11-03
  quote: St. Francis of Assisi Church  |  03-4011
  note: LPi footer on page 8 (the only page with text).
- url: https://parishesonline.com/organization/st-francis-of-assisi-church-07601
  seen: 2026-11-03
  note: 'probe po: org St. Francis of Assisi Church, 50 Lodi St, Hackensack, lpi 0018000000QxABgAAN, container
    03/4011, weekly issues 2026-09-27 to 2026-11-01.'
- url: https://stfrancisofassisihackensack.com/
  seen: 2026-11-03
  quote: 50 Lodi Street, Hackensack, N.J. 07601
  note: 'eCatholic site (site id 16524) behind a bot check: probe get answered HTTP 403, visit.py loaded
    it on the first try and found po-org:st-francis-of-assisi-church-07601 on it.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Francis of Assisi, 50 Lodi Street, Hackensack, publishes its own weekly bulletin through LPi / ParishesOnline (container 03/4011). I read page 1 of the 1 November 2026 issue (image only, rendered): the masthead names St. Francis of Assisi Catholic Church alone, with its Mass schedule and its 50 Lodi Street address.

## Worship sites

One church, `st-francis-of-assisi-hackensack`: the bulletin's MASS SCHEDULE (weekend Masses in English, Spanish and Italian, daily 8AM) names no other place. The directory (55) and GCatholic (18417) list only this church.

## Website and bulletin provider

The directory's https://stfrancisofassisihackensack.com/ is an eCatholic site (id 16524, not a bulletin id) that `probe get` can't read (HTTP 403) but `visit.py` loads; it links the ParishesOnline org recorded here. GCatholic's stfrancisofassisihackensack.org now serves only a script redirecting to `/lander` (a parked page, 114 bytes on 3 November 2026), so it is not used. Provider `parishes_online`. Pages 1-7 of the bulletin are images, so the pipeline has to read it as images.

Fetch check (2026-11-03): resolved the latest ParishesOnline issue for `st-francis-of-assisi-church-07601`, the 20261101B.pdf (1 November 2026).

## Not yet confirmed

Nothing open.
