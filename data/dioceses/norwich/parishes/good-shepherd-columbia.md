---
name: Catholic Community of the Good Shepherd
website: https://www.goodshepherdct.org/
bulletin_provider: parishes_online
provider_id: st-columba-church-06237
publication: ['po-org:st-columba-church-06237', 'lpi:0018000000Qc1HlAAJ', 'po-container:03/0984']
group: 'Yoked: Good Shepherd, St. Maurice Bolton'
evidence:
- url: https://container.parishesonline.com/bulletins/03/0984/20261115B.pdf
  seen: 2026-11-14
  note: 'Page 1 (an image, read with render.py; pages 1-6 have no text layer) of the November 15, 2026
    bulletin: ''The Catholic Community of THE GOOD SHEPHERD, SERVING ST. COLUMBA CHURCH & CHURCH OF THE
    HOLY FAMILY''; clergy Fr. Michael Phillippino; addresses St. Columba Church, 328 Route 66, Columbia
    and Church of the Holy Family, 185 Church Street, Hebron; Weekly Mass Schedule: Saturday 5:00 pm Vigil
    Holy Family, Sunday 8:00 am St. Columba, 10:00 am Holy Family, Tuesday 6:00 pm Holy Family, Wednesday
    8:30 am St. Columba, Thursday 6:30 am Holy Family, Friday 8:30 am St. Columba.'
- url: https://container.parishesonline.com/bulletins/03/0984/20261115B.pdf
  seen: 2026-11-14
  quote: Holy Family, Hebron, CT 03-0984
  note: LPi footer on text pages 7-8.
- url: https://www.goodshepherdct.org/
  seen: 2026-11-14
  note: 'probe url: Squarespace site ''Catholic Community of the Good Shepherd'' links po-org:st-columba-church-06237.'
- url: https://parishesonline.com/organization/st-columba-church-06237
  seen: 2026-11-14
  note: 'probe po: ''St. Columba Church'', PO Box 146, Columbia, lpi 0018000000Qc1HlAAJ, container 03/0984,
    issues to November 15, 2026.'
research:
- method: probe pdf of the November 15, 2026 issue
  url: https://container.parishesonline.com/bulletins/03/0984/20261115B.pdf
  checked: '2026-11-14'
  outcome: unsupported-format
  next_action: Check that the pipeline OCRs pages 1-6 and gets the Mass schedule from page 1
  retry_when: The row is first extracted after promotion
bulletin_status: available
publication_reviews:
- parish: st-maurice-bolton
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/0984/20261115B.pdf
    seen: 2026-11-14
    note: The November 15, 2026 masthead (page 1, image) names St. Columba Church and Church of the Holy
      Family only, with their own Mass schedule; St. Maurice is not named.
  - url: https://container.parishesonline.com/bulletins/03/0312/20261115B.pdf
    seen: 2026-11-14
    note: The November 15, 2026 St. Maurice masthead names Saint Maurice Parish, 32 Hebron Road, Bolton
      alone, with its own Mass schedule (container 03/0312).
---

## Publisher

The Catholic Community of the Good Shepherd (St. Columba, Columbia and Church of the Holy Family, Hebron, merged per the diocese's March 2026 List of Parishes) publishes one bulletin through ParishesOnline, container 03/0984. Page 1 of the November 15, 2026 issue (an image, read 2026-11-14 with render.py) reads 'SERVING ST. COLUMBA CHURCH & CHURCH OF THE HOLY FAMILY', with Fr. Michael Phillippino. The text pages' LPi footer says 'Holy Family, Hebron, CT 03-0984' while the ParishesOnline org is named 'St. Columba Church'.

## Worship sites

Page 1's Weekly Mass Schedule lists two churches: Church of the Holy Family (Saturday 5:00 pm Vigil, Sunday 10:00 am, Tuesday 6:00 pm, Thursday 6:30 am) and St. Columba Church (Sunday 8:00 am, Wednesday and Friday 8:30 am).

St. Maurice, Bolton is yoked with this parish under the same pastor in the diocese's list, but publishes its own bulletin (ParishesOnline 03/0312) whose November 15, 2026 masthead names St. Maurice alone; it is a separate row, st-maurice-bolton, and this bulletin does not name it. The yoking is kept in group.

## Website and bulletin provider

goodshepherdct.org (Squarespace) links the ParishesOnline org st-columba-church-06237 (lpi 0018000000Qc1HlAAJ, container 03/0984), with weekly issues to November 15, 2026. Row is `parishes_online`, read by org slug. The locator map's saintcolumbacatholicchurch.org and GCatholic's holyfamilyhebron.org did not answer (probe url UNREACHABLE, 2026-11-14). Pages 1-6 of the issue are images with no text layer, so the pipeline must OCR the schedule.

## Not yet confirmed

Whether the pipeline gets the Mass times from the image-only pages; see research.
