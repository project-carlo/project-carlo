---
name: Christ the Good Shepherd
website: https://christthegoodshepherd.org/
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.church-bulletin.org/christ-the-good-shepherd-parish-oswego-ny-13126']
group: Catholic Community of Oswego, Minetto & Hannibal
evidence:
- url: https://www.church-bulletin.org/bulletin/christ-the-good-shepherd-parish-oswego-ny-13126/2026-09-27.pdf
  seen: 2026-09-26
  quote: The Catholic Community of Oswego, Minetto & Hannibal
  note: 'Page 1 of the 27 September 2026 issue. The masthead gives Christ the Good Shepherd (134 East
    Fifth Street, Oswego; mailing 50 E. Mohawk St.), Our Lady of Perpetual Help (2913 State Route 48,
    Minetto) and Our Lady of the Rosary (931 Cayuga Street, Hannibal), and one weekend schedule for all
    of them: Sat 4:00 pm OLPH, 4:30 pm CTGS; Sun 8:00 am CTGS, 9:00 am OLPH, 10:15 am OLR, 10:30 am CTGS,
    6:30 pm Hall Newman Center; weekdays 10:00 am CTGS. (The PDF text layer doubles some letters, e.g.
    "Ourr Ladyy off Perpetuall Helpp"; the quote is from a clean line.)'
- url: https://www.church-bulletin.org/bulletin/christ-the-good-shepherd-parish-oswego-ny-13126/2026-06-21.pdf
  seen: 2026-09-26
  quote: We are no longer able to celebrate
  note: 'Page 4 of the 21 June 2026 issue (repeated 28 June): "We are no longer able to celebrate baptisms,
    weddings or funerals at St. Peter''s, St. Stephen''s or St. Joseph''s. Going forward all sacraments
    at Christ the Good Shepherd will be at CTGS @ St. Paul''s". The 17 Aug 2025 issue had still said such
    services "may also take place at our heritage churches".'
- url: https://www.church-bulletin.org/christ-the-good-shepherd-parish-oswego-ny-13126
  seen: 2026-09-26
  quote: Christ the Good Shepherd Parish
  note: John Patrick Publishing's bulletin page for the parish (church-bulletin.org/486 redirects here).
    Weekly PDFs at /bulletin/christ-the-good-shepherd-parish-oswego-ny-13126/YYYY-MM-DD.pdf, newest 27
    September 2026, archive back to 2025. Gives 50 East Mohawk Street and the parish website.
- url: https://christthegoodshepherd.org/
  seen: 2026-09-26
  quote: 6:30 pm – (Hall Newman Center- SUNY Oswego)
  note: The parish homepage. It links church-bulletin.org/486 as its bulletin, gives "Christ the Good
    Shepherd 134 E. Fifth St., Oswego" with the same Masses, and says CTGS "was formed as a unification
    of the parishes of St. Paul, St. Joseph, St. Stephen the King, St. Peter, Sacred Heart, and the territory
    of St. Mary of the Assumption, plus the closed parishes of St. John the Evangelist and St. Louis".
- url: https://files.ecatholic.com/31250/documents/2022/8/Decree-for-St.-Jospeh-St.-Paul-St.-Peter-St.-Stephen.pdf
  seen: 2026-09-26
  note: 'The merger decree, dated 21 May 2020, effective 31 May 2020 (a scan with no text layer; read
    rendered). Item 1 unites St. Joseph, St. Paul, St. Peter and St. Stephen, the King of Hungary "to
    form the new parish of Christ the Good Shepherd"; item 3: "The parish church will be the church of
    Saint Paul located at 50 East Mohawk Street"; item 4 keeps the other three churches open for Mass
    "on the anniversary of the dedication and on the patronal feast of each church".'
promoted: 2026-09-26
---

## Publisher

Christ the Good Shepherd (CTGS) publishes one weekly bulletin through John Patrick Publishing
(church-bulletin.org). I read the 27 September 2026 issue: its page-1 masthead is "The Catholic
Community of Oswego, Minetto & Hannibal", with the addresses of CTGS (134 East Fifth Street,
Oswego), Our Lady of Perpetual Help (Minetto) and Our Lady of the Rosary (Hannibal), and a single
weekend schedule covering all three plus a Sunday 6:30 pm Mass at the Hall Newman Center (SUNY
Oswego). The page-2 intentions list Masses at "OLPH", "OLR" and "CTGS". So the two Minetto and
Hannibal missions, which the diocese lists as their own entries, share this bulletin: the
directory gives christthegoodshepherd.org as the website of both, and I found no bulletin of
their own anywhere.

CTGS was created by decree of 21 May 2020 (effective 31 May 2020) from St. Joseph, St. Paul,
St. Peter and St. Stephen the King, Oswego, with St. Paul's church as the parish church; the
homepage adds Sacred Heart (Scriba, merged 2021 per the 2024 reduction decree) and the long-closed
St. John the Evangelist and St. Louis. St. Mary of the Assumption, Oswego, left the merger and
publishes its own bulletin (`parishes/st-mary-of-the-assumption-oswego.md`).

## Worship sites

Four, all from the 27 September 2026 schedule:

- `churches/christ-the-good-shepherd-oswego.md`: the former St. Paul's church, the parish church.
- `churches/our-lady-of-perpetual-help-minetto.md`
- `churches/our-lady-of-the-rosary-hannibal.md`
- `churches/hall-newman-center-oswego.md`: SUNY Oswego's Newman Center, Sunday 6:30 pm. In no roster.

Ruled out, each with its own `excluded/` record: the heritage churches St. Joseph, St. Peter and
St. Stephen the King (open for private use only; the June 2026 bulletin ended even weddings and
funerals there, and no Mass appears in any 2026 schedule I read), Sacred Heart, Scriba (reduced to
profane use by decree of 20 June 2024), and the long-closed St. John the Evangelist and St. Louis
(demolished 2010).

## Website and bulletin provider

christthegoodshepherd.org is the parish's own WordPress site; its bulletin link
(church-bulletin.org/486) redirects to John Patrick Publishing's page for the parish, which lists a
dated PDF per Sunday. `bulletin_provider: other`, with the parish site as `website`, is how the
`other` fetcher reaches it: it follows the site's bulletin link to the listing page and picks the
PDF whose URL carries the current date. `publication` is that listing page (`url:`), the only id
this publisher exposes.

## Not yet confirmed

Nothing for the structure. Whether the heritage churches still get a patronal-feast Mass (as the
2020 decree allowed) was checked only by grepping the 2026 issues around their feasts (15 and 22
March, 21 and 28 June, 9 and 16 August): none mentions one.
