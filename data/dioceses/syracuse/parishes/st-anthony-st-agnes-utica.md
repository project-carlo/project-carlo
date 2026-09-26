---
name: St. Anthony & St. Agnes
website: https://www.stanthonystagnes.com
bulletin_provider: discover_mass
provider_id: st-anthony-and-st-agnes-utica-ny
publication: ['discovermass:st-anthony-and-st-agnes-utica-ny', 'url:https://www.stanthonystagnes.com/bulletins',
  'po-org:st-anthony-st-agnes-church', 'lpi:0018000000Qx7RSAAZ']
group: Rev. Jim Cesta (Mount Carmel–Blessed Sacrament, St. Anthony & St. Agnes)
evidence:
- url: https://discovermass.com/church/st-anthony-and-st-agnes-utica-ny/
  seen: 2026-09-26
  quote: 'NOTE: On January 21, 2008, the Parishes of St. Agnes and St. Anthony of Padua in Utica merged
    to form The Parish of St. Anthony & St. Agnes with one worship site. St. Agnes church closed permanently.'
  note: The Discover Mass listing, which also carries the bulletin (current issue 27 September 2026; read
    with issues.py). Page 1 of that issue is the parish's own masthead ("422 Tilden Ave, Utica 13501",
    pastor Rev. Jim Cesta, bulletin editor Judith Rosato) with "MASS SCHEDULE at St. Anthony & St. Agnes,
    Saturday 4:30 p.m., Sunday 9:30 a.m." and Mount Carmel's Sunday 8 and 11 a.m. Discover Mass download
    links are per-load tokens, so the issue is cited by the church page and date.
- url: https://www.stanthonystagnes.com/_files/ugd/ee674d_c439dde88b594ee0947682f7db45f35e.pdf
  seen: 2026-09-26
  note: 'Reads (not quotable mechanically: the text layer is letter-spaced or mis-spaced): "ST. ANTHONY
    AND ST. AGNES UTICA, NEW YORK September 13, 2026". The parish''s own Wix bulletin page (stanthonystagnes.com/bulletins)
    links this one PDF, the 13 September 2026 issue, same masthead and schedule as the Discover Mass issues.
    Its text layer has broken word spacing, so quote matching may fail.'
- url: https://parishesonline.com/organization/st-anthony-st-agnes-church
  seen: 2026-09-26
  note: '`probe po st-anthony-st-agnes-church`: LPi id 0018000000Qx7RSAAZ, website stanthonystagnes.com,
    no issues. An old account; recorded so no other row claims it.'
---

## Publisher

St. Anthony & St. Agnes, 422 Tilden Ave, Utica, publishes its own weekly bulletin. Its
current channel is Discover Mass (`st-anthony-and-st-agnes-utica-ny`, issues 6 to 27
September 2026 listed); I read the 27 September issue: page 1 is the parish's masthead (422
Tilden Ave, pastor Rev. Jim Cesta, bulletin editor Judith Rosato) with "MASS SCHEDULE at St.
Anthony & St. Agnes: Saturday 4:30 p.m., Sunday 9:30 a.m.", weekdays Monday and Tuesday 8:30
there and Thursday and Friday at Mt. Carmel. The parish's own site posts the same bulletin
(13 September issue) on its Wix bulletins page.

It shares its pastor with St. Mary of Mount Carmel / Blessed Sacrament, and each bulletin
lists the other's Masses, but their bulletins differ (masthead, editor, publisher), so they
are two rows.

## Worship sites

One: the church at 422 Tilden Ave (`churches/st-anthony-st-agnes-utica.md`), the former St.
Anthony of Padua church. Discover Mass (from MassTimes) says the two parishes merged on 21
January 2008 "with one worship site. St. Agnes church closed permanently"
(`excluded/st-agnes-utica.md`). That note also says the parish "is served by the same pastor
of St. Mark Parish", which is out of date: the bulletin and the diocese name Fr. Cesta.

## Website and bulletin provider

stanthonystagnes.com is the parish's own Wix site (`visit.py` flagged it SPAM-SQUAT, a false
positive: it is the parish's real site, with its bulletins page). Its bulletins page lags
(one issue, 13 September) while Discover Mass has every Sunday, so the provider is
discover_mass with the church slug as `provider_id`. The ParishesOnline org
`st-anthony-st-agnes-church` exists but publishes nothing; its ids are recorded so no other
row claims them.

## Not yet confirmed

Nothing.
