---
name: Sacred Heart Cathedral
website: https://sacredheartrochester.org
bulletin_provider: parishes_online
provider_id: the-cathedral-community
publication:
- po-org:the-cathedral-community
- lpi:0018000000Qc0EgAAJ
- po-container:06/0007
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/06/0007/20260927B.pdf
  seen: '2026-10-02'
  quote: Saturday | 4:00 pm Vigil
  note: 'Page 1 of the 27 September 2026 issue under "SACRED HEART CATHEDRAL": "Saturday | 4:00 pm Vigil
    / Sunday | 7:00 am, 9:15 am, 11:15 am", weekdays Mon/Wed/Thu/Fri 12:10 pm, Tuesday 7:30 am; "The Cathedral
    Community, 296 Flower City Park, Rochester, NY 14615".'
- url: https://sacredheartrochester.org/about/bulletins/
  seen: '2026-10-02'
  note: 'Parish site Bulletins page lists container.parishesonline.com/bulletins/06/0007/<date>B.pdf for
    every Sunday from 26 July to 27 September 2026 (visit.py --bulletin; the page is WordPress and embeds
    po-container:06/0007). `probe po the-cathedral-community`: latest issue 2026-10-04.'
- url: https://ps.dor.org/directory/sacred-heart-cathedral/
  seen: '2026-10-02'
  quote: Weekends - Saturday 4:00 pm; Sunday 7:00 am, 9:15 am, & 11:15 am
promoted: 2026-10-02
---

## Publisher

The Cathedral Community publishes a ParishesOnline bulletin (container 06/0007, org `the-cathedral-community`, LPi id 0018000000Qc0EgAAJ). The 27 September 2026 issue is headed "SACRED HEART CATHEDRAL" and lists one Mass schedule (Saturday 4:00 pm vigil, Sunday 7:00, 9:15 and 11:15 am), at 296 Flower City Park. It names the Cathedral alone.

## Worship sites

One: `churches/sacred-heart-cathedral.md`. The sacramental-records index lists Holy Rosary and Most Precious Blood as records now held by the Cathedral Community (see `excluded/holy-rosary-rochester.md`).

## Website and bulletin provider

The live row had `bulletin_provider: other` with the cathedral's website. The site's Bulletins page embeds the ParishesOnline container, so I changed the provider to `parishes_online` with `provider_id: the-cathedral-community` (the org slug; found by `probe po the-cathedral-community`, whose address is 296 Flower City Park). The slug is not "sacred-heart-cathedral": the obvious guesses return a Davenport, Iowa organization or nothing. Website unchanged.

## Not yet confirmed

Nothing.
