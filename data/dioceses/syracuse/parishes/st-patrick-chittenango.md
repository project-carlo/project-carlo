---
name: St. Patrick's Roman Catholic Church
website: https://www.stpatrickschittenango.com
bulletin_provider: parishes_online
provider_id: st-patricks-roman-catholic-church
publication: ['po-org:st-patricks-roman-catholic-church', 'lpi:0018000000Qc2cLAAR', 'po-container:03/0872']
group: Rev. Kevin Corcoran (Cazenovia, Chittenango)
evidence:
- url: https://container.parishesonline.com/bulletins/03/0872/20260927B.pdf
  seen: 2026-09-26
  quote: St. Patrick’s Roman Catholic Church, Chittenango, NY 03-0872
  note: 27 September 2026 issue. Pages 1 to 4 are images with no text layer; this quote is from the
    text layer of the ad page (page 5). Page 1, read by rendering the PDF, is headed "ST. PATRICK'S ROMAN
    CATHOLIC CHURCH, SEPTEMBER 27, 2026" and gives "WEEKEND MASSES Saturday | 4:00 pm Vigil, Sunday |
    10:30 am; WEEKDAY MASS Wednesday | 11:00 am" and the one church, 1341 Murray Drive.
- url: https://www.stpatrickschittenango.com/bulletin
  seen: 2026-09-26
  quote: Click here to visit Parishes Online for archived Bulletins
  note: 'The parish''s Bulletins page (Google Sites; read with visit.py). It links parishesonline.com/organization/st-patricks-roman-catholic-church
    and embeds recent issues from Google Drive; its sidebar: "Mass Times: Saturday Vigil 4 pm, Sunday
    10:30 am, Wednesday 11 am".'
- url: https://parishesonline.com/organization/st-patricks-roman-catholic-church
  seen: 2026-09-26
  note: '`probe po st-patricks-roman-catholic-church`: 1341 Murray Drive, Chittenango, website stpatrickschittenango.com,
    LPi id 0018000000Qc2cLAAR, container 03/0872, newest issue 2026-09-27.'
---

## Publisher

St. Patrick's publishes its own weekly bulletin through ParishesOnline. I read the 27 September 2026
issue of container 03/0872 by rendering it (its parish pages have no text layer): page 1 names
St. Patrick's Roman Catholic Church, 1341 Murray Drive, Chittenango, alone, with its Mass schedule
(Saturday 4:00 pm vigil, Sunday 10:30 am, Wednesday 11:00 am) and Rev. Kevin Corcoran as pastor.
Fr. Corcoran is also pastor of St. James, Cazenovia, which publishes separately on its own site;
neither bulletin carries the other's Masses. Two rows.

## Worship sites

One: `churches/st-patrick-chittenango.md`.

## Website and bulletin provider

stpatrickschittenango.com's Bulletins page links the ParishesOnline organization
`st-patricks-roman-catholic-church`; `probe po` gives LPi id 0018000000Qc2cLAAR and container 03/0872
(weekly to 27 September 2026). The page also embeds issues as Google Drive previews, the same
bulletins. **The PDFs are image-only apart from the ad page**, so the pipeline's text extraction
will get almost nothing from them without OCR.

## Not yet confirmed

Whether the pipeline can read these image-only issues.
