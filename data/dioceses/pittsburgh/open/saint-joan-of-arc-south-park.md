---
name: St. Joan of Arc
revisit: Read the St. Catherine Labouré bulletin (container 14/1380) for any Mass at St. Joan of Arc (6470
  Library Rd) and the diocese parish page for a change from 'No Weekend Mass Scheduled'; exclude as closed
  only when a source says the building closed
revisit_after: 2027-01-31
roster: ['gcatholic:24307', 'directory:saint-catherine-laboure-parish/1']
evidence:
- url: https://gcatholic.org/churches/usa-03/24307
  seen: 2026-10-23
  quote: 6414 Montour St., South Park, Pennsylvania 15129
  note: GCatholic lists St. Joan of Arc, 6414 Montour St., South Park; history 'ded. 1924.10.19; 1949;
    ded. 1955; parishes merged 2021.01.04'. No closure stated.
- url: https://diopitt.org/saint-catherine-laboure-parish
  seen: 2026-10-23
  quote: No Weekend Mass Scheduled
  note: 'Diocese parish page, Weekend Mass Schedule by Church Building: Saint Joan of Arc Church (South
    Park), 6414 Montour Street, ''No Weekend Mass Scheduled''; Saint Louise de Marillac has four Sunday
    and one Saturday Mass. Read headed Chrome.'
- url: https://container.parishesonline.com/bulletins/14/1380/20261025B.pdf
  seen: 2026-10-23
  quote: 6470 Library Road
  note: Page 1 of the 25 October 2026 St. Catherine Labouré bulletin names 'Saint Joan of Arc, 6470 Library
    Road, South Park Township, PA 15129' as a parish location, but the only Mass schedule printed is headed
    'Saint Louise de Marillac Church'. A search of 12 issues from 7 September 2025 to 25 October 2026
    (probe pdf --grep Joan) found Joan of Arc only in the page-1 address list; no intention, schedule
    line or event names a Mass there.
- url: https://www.sclpgh.org/st-joan-church-history
  seen: 2026-10-23
  quote: St. Joan of Arc Catholic Church
  note: 'Parish site (headed Chrome): footer lists ''St. Joan of Arc Catholic Church, 6470 Library Rd.
    South Park, PA 15129'' as a parish location; the site has a ''Tour St. Joan of Arc Church'' page and
    a history running to the 2012 school closure. The home page''s Mass Times list only St. Louise de
    Marillac. Neither says the church closed.'
- url: https://diopitt.org/saint-catherine-laboure-upper-saint-clair
  seen: 2026-10-23
  note: 'Search-result snippet read 2026-10-23 (diocese page not opened): ''On January 4, 2021, the two
    parishes were formally merged to create the new St. Catherine Laboure Parish. Both churches remained
    open to serve the new parish.'' Dates the 2021 merger only.'
parish: saint-catherine-laboure-pittsburgh
line1: 6414 Montour St.
city: South Park
state: PA
postal_code: '15129'
research:
- method: probe pdf --grep Joan over 12 St. Catherine Labouré issues (container 14/1380), Sept 2025 to
    Oct 2026; parish site home, history and tour pages; web search for a closure or relegation notice
  url: https://container.parishesonline.com/bulletins/14/1380/20261025B.pdf
  checked: '2026-10-23'
  outcome: not-found
  next_action: Re-grep the monthly bulletins for a Mass or funeral at St. Joan of Arc, and check the diocese
    page and clergy-official posts for a relegation decree
  retry_when: A bulletin schedules a Mass at St. Joan of Arc, or the diocese or parish announces the building's
    closure or sale
  revisit_after: 2027-01-31
---

## What is known

St. Joan of Arc (Library, South Park Township) merged with St. Louise de Marillac on 2021-01-04 into St. Catherine Labouré Parish, whose one bulletin (ParishesOnline container 14/1380) is recorded in parishes/saint-catherine-laboure-pittsburgh. The diocese page lists this church as 'No Weekend Mass Scheduled'. The 25 October 2026 bulletin cover and the parish site footer still list it as a parish location (6470 Library Road), and the parish site keeps a tour page for it, but every Mass in the bulletin and on the site is at St. Louise de Marillac. Twelve issues from September 2025 to October 2026 mention Joan of Arc only in the cover address list. Scout 1's lead (ParishesOnline org st-joan-of-arc-church-15129 is container 14/1380) was checked: that org is this parish's bulletin, not a separate publisher.

Address disagreement: the diocese and GCatholic give 6414 Montour Street; the bulletin, parish site and a South Park advertiser's address ('6430 Library Rd.') point to Library Road, 6470. The ParishesOnline org pin (40.28738, -80.02578) and GCatholic's Plus Code agree to about 10 m, so these are probably one campus with two street addresses. Not settled; the Montour Street address is kept from the roster.

## Why it is not decided

Rule 2 for this diocese: a 'No Masses Scheduled' listing does not make a church closed, and no source read says it closed or was relegated. It cannot be called a worship site either, because no Mass is printed anywhere. It stays open until a bulletin shows an occasional Mass (a church row under St. Catherine Labouré) or a source states the closure (an excluded record with a date).
