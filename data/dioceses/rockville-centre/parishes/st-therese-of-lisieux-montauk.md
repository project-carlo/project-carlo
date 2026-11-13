---
name: St. Therese of Lisieux
website: https://sttheresemontauk.com/
bulletin_provider: parishes_online
provider_id: st-therese-of-lisieux-parish-11954
publication: ['po-org:st-therese-of-lisieux-parish-11954', 'lpi:0018000000Qx83QAAR', 'po-container:03/4096']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/4096/20261115B.pdf
  seen: 2026-11-13
  quote: St. Therese of Lisieux Parish  |  03-4096
  note: 'November 15, 2026 issue (16 pages; pages 1-14 are images, read by rendering 1-2). Page 1 masthead
    ''November 15, 2026 | Thirty-third Sunday in Ordinary Time ... SAINT THERESE OF LISIEUX 67 South Essex
    Street, Montauk, NY 11954 | StThereseMontauk.com''; Sunday Mass ''Saturday Vigil | 5pm, 7pm (Espanol)'',
    ''Sunday | 8:30am, 10:30am''; Daily Mass ''Tuesday - Friday | 8:30am''. Page 2: ''Father Ryan Creamer
    Pastor'', ''Father Maddela Prathap Pastoral Associate''. Pages 15-16 LPi footer (the quote).'
- url: https://parishesonline.com/organization/st-therese-of-lisieux-parish-11954
  seen: 2026-11-13
  note: 'probe po: ''St. Therese of Lisieux Parish'', 67 Essex St, Montauk, NY 11954, website sttheresemontauk.com,
    LPi id 0018000000Qx83QAAR, container 03/4096, latest issue 2026-11-15.'
- url: https://sttheresemontauk.com/
  seen: 2026-11-13
  note: 'Parish site (WordPress; probe url could not connect, read with parish-site-access visit.py):
    embeds the ParishesOnline org st-therese-of-lisieux-parish-11954; Mass schedule ''Sat: 5pm, 7pm (Winter)
    / 8pm (Summer) en Espanol; Sun: 8:30am, 10:30am''; ''Daily Masses: Tues - Fri: 8:30am''. It also links
    an old e-churchbulletins.com/bulletins/009340.pdf, which now returns an HTML page, not a PDF.'
revisit: Compare the mastheads of St. Therese (LPi 03-4096) and Most Holy Trinity, East Hampton (mostholytrinityeh.com/bulletin-homily)
  for a joint bulletin under their shared pastor, Fr. Ryan Creamer.
revisit_after: 2027-03-01
bulletin_status: available
publication_reviews:
- parish: most-holy-trinity-east-hampton
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/4096/20261115B.pdf
    seen: 2026-11-13
    note: The 15 November 2026 masthead (page 1, an image) names Saint Therese of Lisieux, 67 South Essex
      Street, Montauk alone, LPi 03-4096, with its own Mass times; page 2 lists Father Ryan Creamer, Pastor.
  - url: https://www.mostholytrinityeh.com/_files/ugd/ad8d48_7fd14bad4bc64e068a35e01bad3e1bfe.pdf
    seen: 2026-11-13
    note: The 15 November 2026 masthead names Most Holy Trinity Parish, East Hampton with St. Peter, Amagansett,
      with its own Mass times; the issue never mentions Montauk or St. Therese.
---

## Publisher

St. Therese of Lisieux, Montauk publishes its own weekly bulletin, printed by LPi (footer "St. Therese of Lisieux Parish | 03-4096"). The November 15, 2026 issue (`https://container.parishesonline.com/bulletins/03/4096/20261115B.pdf`, read 2026-11-13 by rendering pages 1-2, which are images) has the masthead "SAINT THERESE OF LISIEUX, 67 South Essex Street, Montauk, NY 11954" with its own Mass schedule, and page 2 lists "Father Ryan Creamer, Pastor".

Fr. Creamer has also been pastor of Most Holy Trinity, East Hampton since 2026-09-23 (batch brief, June 2026 appointments). The two parishes still print separate bulletins: Most Holy Trinity's 15 November issue names only East Hampton and St. Peter, Amagansett, and this one only St. Therese (see `publication_reviews`). Recheck after a few more months of the shared pastorate.

## Worship sites

One: the church at 67 South Essex Street (`st-therese-of-lisieux-montauk-church`). The 15 November schedule names no other place, and the diocesan locator, GCatholic and the Mass-times page list only this church in Montauk.

## Website and bulletin provider

sttheresemontauk.com is a WordPress site (`probe url` could not connect; it loads in the browser) that embeds the ParishesOnline org, so the provider is `parishes_online` with `st-therese-of-lisieux-parish-11954`. Pages 1-14 of the LPi issue are images; the pipeline needs OCR for the schedule.

fetch:check on 2026-11-13 picked the 15 November 2026 issue (container 03/4096, 20261115B.pdf), whose rendered page 1 is St. Therese's masthead dated November 15, 2026.

## Not yet confirmed

Whether the shared pastor merges the two bulletins later: check the masthead of both parishes' issues after the next appointments.
