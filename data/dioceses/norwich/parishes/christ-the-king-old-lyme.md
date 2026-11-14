---
name: Christ the King
website: https://www.christthekingchurch.net/
bulletin_provider: parishes_online
provider_id: christ-the-king-roman-catholic-parish-06371
publication: ['po-org:christ-the-king-roman-catholic-parish-06371', 'lpi:0018000000Qbyx1AAB', 'po-container:03/0387']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0387/20261115B.pdf
  seen: 2026-11-14
  quote: Christ the King Roman Catholic Parish
  note: 'November 15, 2026 issue: pages 7-8 carry the LPi footer ''Christ the King Roman Catholic Parish
    | 03-0387''; pages 1-6 are images. Page 1, read as an image (render.py), shows ''Christ the King ...
    Catholic Church'', One McCurdy Rd, Old Lyme, CT 06371, with Mass Monday-Friday 8:00am, Saturday Vigil
    5:00pm, Sunday 8:00am and 10:30am.'
- url: https://parishesonline.com/organization/christ-the-king-roman-catholic-parish-06371
  seen: 2026-11-14
  note: 'probe po: title ''Christ the King Roman Catholic Parish'', 1 McCurdy Rd, Old Lyme 06371-1629,
    website www.christthekingchurch.net, lpi 0018000000Qbyx1AAB, container 03/0387, latest issue 2026-11-15.'
- url: https://www.christthekingchurch.net/sunday-bulletins
  seen: 2026-11-14
  note: 'probe url: the parish''s Wix site lists its bulletins as _files/ugd PDFs; the first, 4cd92f_8ad34628b3c546c789c978f17a323c71.pdf,
    has the same 8 pages and 03-0387 footer as the ParishesOnline issue.'
research:
- method: probe pdf / probe container 03/0387 --pages 2 on the 2026-11-15 issue
  url: https://container.parishesonline.com/bulletins/03/0387/20261115B.pdf
  checked: '2026-11-14'
  outcome: unsupported-format
  next_action: Check whether the pipeline OCRs image pages and so gets the page 1 Mass schedule
  retry_when: The pipeline's handling of image-only bulletin pages is known
bulletin_status: available
---

## Publisher

Christ the King, Old Lyme publishes its own LPi bulletin: ParishesOnline org `christ-the-king-roman-catholic-parish-06371`, container 03/0387, lpi:0018000000Qbyx1AAB. Pages 1-6 of the November 15, 2026 issue are images with no text layer; pages 7-8 carry the footer "Christ the King Roman Catholic Parish | 03-0387". Page 1, read as an image on 2026-11-14, shows "Christ the King ... Catholic Church", One McCurdy Rd, Old Lyme, CT 06371, and the pastor Fr. Joseph C. Ashe.

## Worship sites

One church. Page 1's box (image): Mass Monday-Friday 8:00am, Saturday Vigil 5:00pm, Sunday 8:00am and 10:30am; no other place named. The diocese's List of Parishes (March 6, 2026) lists no mission of Christ the King.

## Website and bulletin provider

ParishesOnline, read by `provider_id`. The parish's Wix site posts the same LPi issues as _files/ugd PDFs on /sunday-bulletins; the ParishesOnline org was found by guessing the '<name>-<zip>' slug (the bare christ-the-king-roman-catholic-parish is a Mesa, Arizona parish).

## Not yet confirmed

The bulletin is image-only on its first six pages; whether the pipeline reads Mass times from it is open (research).
