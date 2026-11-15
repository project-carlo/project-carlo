---
name: Saint Anne's Catholic Community
website: https://www.saintannecluster.org/bulletin
bulletin_provider: parishes_online
provider_id: saint-anne-s-catholic-community
publication: ['po-org:saint-anne-s-catholic-community', 'lpi:0018000000Qc044AAB', 'po-container:03/0123']
group: 'Yoked: Baltic, Occum, Taftville'
evidence:
- url: https://container.parishesonline.com/bulletins/03/0123/20261115B.pdf
  seen: 2026-11-14
  quote: Saint Anne's Catholic Community  |  03-0123
  note: 'Page 1 (an image, read with render.py) of the November 15, 2026 issue: masthead ''SAINT ANNE''S
    CATHOLIC COMMUNITY / SACRED HEART CHURCH * ST. JOSEPH CHURCH * ST. MARY CHURCH'', Fr. Joseph Tito,
    Pastor; Mass schedules for Sacred Heart Church, Taftville, St. Joseph Church, Occum and St. Mary Church,
    Baltic. The quote is the page 6 footer, the only text page.'
- url: https://www.saintannecluster.org/bulletin
  seen: 2026-11-14
  note: 'Squarespace site of Saint Anne''s Catholic Community; its ''Parish Bulletins & Weekly Readings''
    link goes to parishesonline.com/organization/saint-anne-s-catholic-community. stjosephoccum.org and
    sacredheartchurchtaftville.org redirect here (probe url, 2026-11-14); stmarybaltic.com (the locator
    map''s link) does not resolve. probe po: org ''Saint Anne''s Catholic Community'', 156 Providence
    St, Taftville, lpi:0018000000Qc044AAB, container 03/0123, latest issue 2026-11-15.'
promoted: 2026-11-14
research:
- method: probe pdf of the November 15, 2026 issue
  url: https://container.parishesonline.com/bulletins/03/0123/20261115B.pdf
  checked: '2026-11-14'
  outcome: unsupported-format
  next_action: Check that the pipeline OCRs page 1 and gets the three churches' Mass schedules
  retry_when: The row is first extracted after promotion
bulletin_status: available
---

## Publisher

St. Mary of the Immaculate Conception, Baltic, St. Joseph, Occum and Sacred Heart, Taftville (yoked under Rev. Joseph Tito: diocese List of Parishes, March 6, 2026) publish one LPi bulletin as Saint Anne's Catholic Community: ParishesOnline org `saint-anne-s-catholic-community` (container 03/0123, lpi:0018000000Qc044AAB). The November 15, 2026 issue (read 2026-11-14) has pages 1-5 as images; page 1, read with render.py, is headed "SAINT ANNE'S CATHOLIC COMMUNITY / SACRED HEART CHURCH * ST. JOSEPH CHURCH * ST. MARY CHURCH / NOVEMBER 15, 2026", with Fr. Joseph Tito, Pastor, and Fr. Christopher Zmuda, Parochial Vicar. The page 6 footer reads "Saint Anne's Catholic Community | 03-0123". Page 2 has priest schedules and offertory for Sacred Heart and St. Joseph, and an adoration note for St. Mary's, Baltic.

Other ParishesOnline accounts: the locator map links `sacred-heart-church-06380` (no such org) and `st-josephs-church-06383` (org "St. Joseph's Church", 11 Baltic Rd., Occum, lpi:0018000000Qc1TuAAJ, no issues listed by `probe po`); the cluster site also links `sacred-heart-church-taftville-and-st-joseph-church-occum` (no such org). None publishes now, so none is a `publication` id of this row.

## Worship sites

Page 1's "MASS SCHEDULES" lists three churches: Sacred Heart Church, Taftville (Sunday Vigil 4:30 PM Saturday; Sunday 8:00 and 10:30 AM; weekdays 7:00 AM Mon.-Fri., 8:00 AM Sat.), St. Joseph Church, Occum (Saturday 5:00 PM, Sunday 9:00 AM) and St. Mary Church, Baltic (Monday-Friday 8:00 AM; Saturday 8:00 AM and 5:00 PM; Sunday 8 AM and 10:00 AM; Monday 7:00 PM). The diocese's Full Group Directory also lists the Holy Family Motherhouse and the Academy of the Holy Family at 54 West Main Street, Baltic; pages 1-2 of this issue do not name them, and the motherhouse has its own `excluded/` record (no-public-mass).

## Website and bulletin provider

saintannecluster.org is a Squarespace site whose bulletin link is the ParishesOnline org; fetch reads the bulletin by `provider_id`. Pages 1-5 of the issue are images with no text layer (only the page 6 ad page has text), so the pipeline has to read them as images.

## Not yet confirmed

Whether the pipeline's text extraction gets the Mass times from the image pages; see research.
