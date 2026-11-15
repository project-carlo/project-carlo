---
name: Our Lady Queen of Peace Parish
website: https://www.stmary-stthomas.community/bulletins
bulletin_provider: parishes_online
provider_id: st-thomas-aquinas-chapel-at-uconn-storrs-ct-our-lady-queen-of-peace-parish
publication: ['po-org:st-thomas-aquinas-chapel-at-uconn-storrs-ct-our-lady-queen-of-peace-parish', 'lpi:0018000000Qc2VwAAJ',
  'po-container:04/0008']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0008/20261115B.pdf
  seen: 2026-11-14
  note: 'Page 1 (an image, read with render.py; pages 1-6 have no text layer) of the November 15, 2026
    bulletin: ''OUR LADY QUEEN OF PEACE PARISH'', Weekly Schedule: ST. MARY CHURCH Saturday Vigil 4:00
    pm, Sunday 10:30 am, Tuesday 6:00 pm; ST. THOMAS AQUINAS UCONN STORRS CAMPUS Sunday 8:30 am, 12:30
    pm* and 7:00 pm*, Mon-Fri 12:30 pm*, Wednesday 5:00 pm*, Thursday 8:00 pm*, Saturday 8:30 am (*when
    UConn is in session); St. Mary Church & Office, 1600 Main Street, Coventry; St. Thomas Aquinas Chapel,
    46 North Eagleville Road, Storrs; www.olqop.com.'
- url: https://container.parishesonline.com/bulletins/04/0008/20261115B.pdf
  seen: 2026-11-14
  quote: St. Thomas Aquinas, Storrs, CT 04-0008
  note: LPi footer on the text pages 7-8.
- url: https://www.stmary-stthomas.community/bulletins
  seen: 2026-11-14
  note: 'probe url: the parish''s Duda site ''Our Lady Queen of Peace'' embeds the ParishesOnline widget
    lpi:0018000000Qc2VwAAJ on /bulletins; olqop.com redirects to this site.'
- url: https://parishesonline.com/organization/st-thomas-aquinas-chapel-at-uconn-storrs-ct-our-lady-queen-of-peace-parish
  seen: 2026-11-14
  note: 'probe po: ''St. Thomas Aquinas Chapel at UConn, Storrs CT / Our Lady Queen of Peace Parish'',
    46 N Eagleville Rd, Storrs, container 04/0008, weekly issues to November 15, 2026.'
- url: https://www.stmaryscoventry.org/
  seen: 2026-11-14
  note: GCatholic's site for St. Mary and St. Joseph is now a Church of England parish in Coventry, England
    (menus 'The Walsgrave (magazine)', 'APCM Paper Work 2025'); not this parish. The diocese's www.stmarycoventy.org
    and www.stmary-stthomas.community.org do not resolve; stthomasaquinasuconn.org answered 403.
research:
- method: probe pdf of the November 15, 2026 issue
  url: https://container.parishesonline.com/bulletins/04/0008/20261115B.pdf
  checked: '2026-11-14'
  outcome: unsupported-format
  next_action: Check that the pipeline OCRs pages 1-6 and gets the Mass schedule from page 1
  retry_when: The row is first extracted after promotion
bulletin_status: available
---

## Publisher

Our Lady Queen of Peace Parish (St. Mary, Coventry and St. Thomas Aquinas Chapel, Storrs, merged per the diocese's March 2026 List of Parishes) publishes one bulletin through ParishesOnline, container 04/0008. Page 1 of the November 15, 2026 issue (read 2026-11-14 as an image with render.py) is headed 'OUR LADY QUEEN OF PEACE PARISH'; the text pages' LPi footer reads 'St. Thomas Aquinas, Storrs, CT 04-0008', the older account name.

## Worship sites

Page 1's Weekly Schedule lists two churches: St. Mary Church (Saturday Vigil 4:00 pm, Sunday 10:30 am, Tuesday 6:00 pm) and St. Thomas Aquinas, UConn Storrs campus (Sunday 8:30 am, plus 12:30 and 7:00 pm and weekday Masses when UConn is in session). St. Joseph, Eagleville, which the diocese lists as closed with records at St. Mary, Coventry, is not on page 1 and 'Eagleville' does not occur in the text pages; it has its own excluded record.

## Website and bulletin provider

The diocese's listed domains (www.stmarycoventy.org, www.stmary-stthomas.community.org) do not resolve. The locator map's stmary-stthomas.community (Duda, also reached from olqop.com) embeds lpi:0018000000Qc2VwAAJ on /bulletins, which probe po resolves to the org above and container 04/0008, with weekly issues to November 15, 2026. GCatholic's stmaryscoventry.org is now an English Anglican parish's site. Row is `parishes_online`, read by org slug. Pages 1-6 of the issue are images with no text layer; only the ad pages 7-8 have text, so the pipeline must OCR the schedule.

## Not yet confirmed

Whether the pipeline gets the Mass times from the image-only pages; see research.
