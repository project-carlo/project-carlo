---
name: Blessed Virgin Mary Parish
website: https://www.bvm-darby.com/
bulletin_provider: parishes_online
provider_id: blessed-virgin-mary-church
publication: ['po-org:blessed-virgin-mary-church', 'lpi:0018000000QbywDAAR', 'po-container:04/0756']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/04/0756/20261025B.pdf
  seen: 2026-10-28
  note: 'The 25 October 2026 issue (4 pages; pages 1-3 are images, page 1 rendered and read; page 4 footer
    ''Blessed Virgin Mary Church | 04-0756''). Page 1 masthead: ''BLESSED VIRGIN MARY CHURCH, 1101 Main
    Street, Darby, Pennsylvania 19023-1407, Founded 1913''; Rev. Msgr. David Quitugua, Parochial Administrator.
    Eucharistic Liturgy: Vigil Mass (Saturday evening) 4:30PM, BVM; Sundays 9:30 AM St. Louis, Yeadon;
    Sundays 8:00 & 11:00 AM & 4:00 PM, BVM; Holy Days 8:15 AM, 12:00 Noon & 7:30 PM, BVM; Daily 8:15 AM
    Monday through Saturday.'
- url: https://container.parishesonline.com/bulletins/04/0756/20261025B.pdf
  seen: 2026-10-28
  quote: Blessed Virgin Mary Church  |  04-0756
  note: Page 4 footer, the only text-layer line; ties the file to container 04-0756.
- url: https://parishesonline.com/organization/blessed-virgin-mary-church
  seen: 2026-10-28
  note: 'probe po 0018000000QbywDAAR: organization ''Blessed Virgin Mary Church'', 1101 Main St, Darby
    19023, ids po-org:blessed-virgin-mary-church, lpi:0018000000QbywDAAR, po-container:04/0756; issues
    2026-11-01 (posted early), 2026-10-25, 2026-10-18.'
- url: https://www.bvm-darby.com/page2
  seen: 2026-10-28
  note: 'The parish''s Bulletin page (Duda/LPi WeConnect site) embeds the ParishesOnline publicationWidget
    with id=0018000000QbywDAAR, the same LPi id. The home page''s Mass Schedule: ''Sunday: 9:30 am mass
    at St. Louis'', ''No daily at St. Louis''.'
- url: https://archphila.org/parish/blessed-virgin-mary-darby/
  seen: 2026-10-28
  note: 'Directory: Rev. Msgr. David C. Quitugua (Parochial Administrator) in residence at Redemptoris
    Mater Seminary; Mass times ''Sundays, 8, 9:30 (at St. Louis Church, Yeadon), 11 AM; 4 PM''; ''Worship
    Site: St. Louis Church, Yeadon''; page updated 2 years ago.'
publication_reviews:
- parish: st-joseph-collingdale
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0756/20261025B.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image) names Blessed Virgin Mary Church, 1101 Main Street,
      Darby alone, in ParishesOnline container 04/0756.
  - url: https://www.church-bulletin.org/bulletin/saint-joseph-church-collingdale-pa-19023/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1) names Saint Joseph Church, 500 Woodlawn Avenue, Collingdale
      alone, in John Patrick listing 50.
- parish: our-lady-of-peace-milmont-park
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0756/20261025B.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image) names Blessed Virgin Mary Church, 1101 Main Street,
      Darby alone, in ParishesOnline container 04/0756.
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-peace-milmont-park-pa-19033/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1) names Our Lady of Peace Catholic Parish, 208 Milmont Avenue,
      Milmont Park, with its Notre Dame de Lourdes worship site, in John Patrick listing 109.
- parish: our-lady-of-perpetual-help-morton
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/04/0756/20261025B.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image) names Blessed Virgin Mary Church, 1101 Main Street,
      Darby alone, in ParishesOnline container 04/0756.
  - url: https://container.parishesonline.com/bulletins/04/0612/20261025B.pdf
    seen: 2026-10-28
    note: The 25 October 2026 bulletin (page 3, 'OLPH is a tithing Parish') is Our Lady of Perpetual Help's
      alone, with its own Mass times and intentions, in ParishesOnline container 04/0612.
---

## Publisher

Blessed Virgin Mary Parish, Darby, publishes its own weekly bulletin through ParishesOnline / LPi (container 04/0756). The 25 October 2026 issue is headed 'BLESSED VIRGIN MARY CHURCH, 1101 Main Street, Darby' and its Mass box lists BVM and St. Louis, Yeadon. The issue is mostly image pages, so the masthead and Mass box were read from a render of page 1, not from a text layer.

## Worship sites

Two, both with Mass in the 25 October 2026 schedule: Blessed Virgin Mary Church (Darby) and St. Louis Church, Yeadon (Sunday 9:30 AM only; the parish site adds 'No daily at St. Louis'). The directory names St. Louis as 'Worship Site' of this parish (the closed parish St. Louis, 1928-2013, whose records are kept at BVM). See `churches/st-louis-yeadon`. No other place appears in the Mass box.

## Website and bulletin provider

bvm-darby.com is a WeConnect (LPi) Duda site whose Bulletin page embeds the ParishesOnline widget for the same LPi id, so the ParishesOnline resolver reads the bulletin directly. There is no John Patrick listing for this parish (`raw/jppc-pa.json` has none for Darby). The 1 November 2026 issue was already posted on 2026-10-28, so `fetch:check` may report freshness `future`.

## Not yet confirmed

Pages 2-3 of the issue were not read for Mass intentions; page 2 is a Gospel reflection. Nothing further was needed for the schedule.
