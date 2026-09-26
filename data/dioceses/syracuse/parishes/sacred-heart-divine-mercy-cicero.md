---
name: Sacred Heart & Divine Mercy
website: https://www.sh-dm.org
bulletin_provider: parishes_online
provider_id: sacred-heart-divine-mercy-13039
publication: ['po-org:sacred-heart-divine-mercy-13039', 'lpi:0018000000Qc0EhAAJ', 'po-container:06/0003']
group: Sacred Heart & Divine Mercy (Rev. Christopher Seibt)
evidence:
- url: https://container.parishesonline.com/bulletins/06/0003/20260927B.pdf
  seen: 2026-09-26
  quote: Two Parishes, One Family … 8229 Brewerton Rd. Cicero, NY 13039 … 592 S. Main St. Central Square,
    NY 13036
  note: Masthead of the 27 September 2026 issue, page 1. Names the two parishes, Sacred Heart (Cicero)
    and Divine Mercy (Central Square), with one pastor and one Mass schedule.
- url: https://container.parishesonline.com/bulletins/06/0003/20260927B.pdf
  seen: 2026-09-26
  quote: 4:00 PM at Divine Mercy … 5:15 PM at Sacred Heart
  note: The same masthead's weekend schedule. Sunday 7:00 and 10:00 am at Sacred Heart, 8:30 and 11:30
    am at Divine Mercy; weekday Masses alternate between the two. No other church is named.
- url: https://www.sh-dm.org/bulletin
  seen: 2026-09-26
  note: 'The parishes'' Bulletin page (read with parish-site-access visit.py) embeds the ParishesOnline
    publication page sacred-heart-divine-mercy-13039 with the 27 September 2026 issue of container 06/0003.'
- url: https://parishesonline.com/organization/sacred-heart-divine-mercy-13039
  seen: 2026-09-26
  note: '`probe po 0018000000Qc0EhAAJ`: organization "Sacred Heart & Divine Mercy", 8229 Brewerton Rd,
    Cicero, website sh-dm.org, container 06/0003, weekly issues through 2026-09-27.'
- url: https://thecatholicsun.com/mission-st-bernadette-decree-july-8-2023/
  seen: 2026-09-26
  quote: The church of Divine Mercy located at 592 South Main Street, Central Square, New York, is hereby
    officially designated as the sole church of the parish.
  note: The bishop's decree of 6 July 2023 (published 8 July) merging the Mission of St. Bernadette into
    Divine Mercy and relegating the Constantia church, effective 16 July 2023.
---

## Publisher

Sacred Heart (Cicero) and Divine Mercy and the Mission of St. Bernadette (Central Square) are two
canonical parishes under one pastor, Rev. Christopher Seibt, and they publish one weekly bulletin
through ParishesOnline. I read the 27 September 2026 issue of container 06/0003: its masthead is
headed "Two Parishes, One Family", gives both addresses (8229 Brewerton Rd., Cicero; 592 S. Main St.,
Central Square), both offices and both sets of trustees, and one Mass schedule covering both
churches. The 20 September issue is the same. The parishes' site sh-dm.org ("The Parishes of Sacred
Heart and Divine Mercy") gives the same schedule. One bulletin, one row.

## Worship sites

Two churches, the only ones the 27 September 2026 schedule names:

- `churches/sacred-heart-cicero.md`: Saturday 5:15 pm, Sunday 7:00 and 10:00 am.
- `churches/divine-mercy-central-square.md`: Saturday 4:00 pm, Sunday 8:30 and 11:30 am.

Ruled out, each in `excluded/` with its evidence. The diocese keeps the sacramental records of all
of these at Divine Mercy ("Sacramental records for St. Agnes, Brewerton; St. Michael, Central
Square; St. Bernadette Mission, Constantia; and St. Mary of the Assumption, Cleveland, are retained
here"):

- St. Bernadette Mission, Constantia: relegated in 2023, last Mass 15 July 2023
  (`excluded/st-bernadette-constantia.md`). The canonical name "Divine Mercy Parish & The Mission of
  St. Bernadette" survives, but the decree makes Divine Mercy the parish's sole church.
- St. Mary of the Assumption Oratory, Cleveland (`excluded/st-mary-of-the-assumption-cleveland.md`).
- St. Michael, Central Square: the old church across Main Street, a pastor's residence by 2016
  (`excluded/st-michael-central-square.md`).
- St. Agnes, Brewerton: merged into Divine Mercy in 2013, church sold (`excluded/st-agnes-brewerton.md`).
- St. Patrick, Cleveland: in the diocese's list as closed, no roster entry (`excluded/st-patrick-cleveland.md`).

## Website and bulletin provider

sh-dm.org is the two parishes' shared site (Our Sunday Visitor); its Bulletin page embeds the
ParishesOnline publication page for `sacred-heart-divine-mercy-13039`. `probe po` on the LPi id
from that page gives the organization slug, LPi id 0018000000Qc0EhAAJ and container 06/0003, weekly
through 27 September 2026; all three are in `publication`. GCatholic links Divine Mercy to
divinemercyparishbcs.com and the search results show divinemercycny.org; neither was needed, because
the diocese's own page for Divine Mercy gives "Website: sh-dm.org". Discover Mass has listings for
"Sacred Heart", "Divine Mercy (St. Michael Campus)", "St. Bernadette" and "St. Mary of the Assumption"
(Cleveland) with no issues (issues.py, 2026-09-26), so no second channel exists.

## Not yet confirmed

Nothing.
