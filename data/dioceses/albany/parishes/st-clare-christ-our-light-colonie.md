---
name: Church of Saint Clare and Christ Our Light
website: https://www.stclarescolonie.com
bulletin_provider: parishes_online
provider_id: church-of-saint-clare
publication: ['po-org:church-of-saint-clare', 'lpi:0018000000Qx7NaAAJ', 'po-container:03/1389', 'po-org:christ-our-light-church-12211',
  'lpi:0018000000Qx7OVAAZ', 'po-container:03/1011']
group: St. Clare / Christ Our Light (shared bulletin)
evidence:
- url: https://container.parishesonline.com/bulletins/03/1389/20260927B.pdf
  seen: 2026-09-28
  quote: The Roman Catholic Communities of Church of Saint Clare and Christ Our Light
  note: Masthead, page 1 of the 27 September 2026 issue in St. Clare's container (03/1389). It then gives
    both offices, "1947 Central Avenue, Albany, NY 12205" and "1 Maria Drive, Loudonville, NY 12211".
- url: https://container.parishesonline.com/bulletins/03/1389/20260927B.pdf
  seen: 2026-09-28
  quote: 'ANOINTING OF THE SICK: Is offered on the first weekend of each month following the Saturday
    4:00 PM Mass at Christ Our Light and the Sunday 9:30 AM Mass at St. Clare''s.'
  note: Page 2 of the same issue, which also lists Mass intentions under separate CHRIST OUR LIGHT and
    SAINT CLARE headings (Saturday 4 pm and Sunday 10 am at Christ Our Light; Saturday 4 pm and Sunday
    9:30 am at St. Clare).
- url: https://container.parishesonline.com/bulletins/03/1011/20260927B.pdf
  seen: 2026-09-28
  quote: The Roman Catholic Communities of Church of Saint Clare and Christ Our Light
  note: The same 27 September 2026 issue in Christ Our Light's container (03/1011). Pages 1-3 are word
    for word the St. Clare file; only the LPi advertising page differs ("Christ Our Light, Loudonville,
    NY 03-1011" vs "Church of Saint Clare | 03-1389"), so the files' hashes differ.
- url: https://parishesonline.com/organization/church-of-saint-clare
  seen: 2026-09-28
  note: '`probe po` 2026-09-28: org church-of-saint-clare, 1947 Central Ave, Albany, NY 12205, LPi 0018000000Qx7NaAAJ,
    container 03/1389, weekly issues through 2026-09-27.'
- url: https://parishesonline.com/organization/christ-our-light-church-12211
  seen: 2026-09-28
  note: '`probe po` 2026-09-28: org christ-our-light-church-12211, 1 Maria Drive, Loudonville, LPi 0018000000Qx7OVAAZ,
    container 03/1011, weekly issues through 2026-09-27.'
- url: https://container.parishesonline.com/bulletins/03/1011/20250907B.pdf
  seen: 2026-09-28
  quote: SUNDAY, SEPTEMBER 7, 2025
  note: '`probe container --step 8` over both containers back to 7 September 2025: every sampled issue
    (Sep, Nov, Dec 2025; Feb, Apr, Jun, Aug 2026) has the same shared content in both, so the two have
    shared one bulletin for at least a year.'
---

## Publisher

St. Clare (Colonie) and Christ Our Light (Loudonville) are two parishes that publish one
weekly bulletin. The 27 September 2026 issue's masthead (page 1) reads "The Roman Catholic
Communities of Church of Saint Clare and Christ Our Light" and gives both parish offices;
page 2 carries each church's Mass intentions under its own heading and says anointing is
offered after "the Saturday 4:00 PM Mass at Christ Our Light and the Sunday 9:30 AM Mass at
St. Clare's". The bulletin is written by Deacon Dick ("From Deacon Dick ~").

LPi prints it twice, once in each parish's ParishesOnline container: 03/1389 (St. Clare) and
03/1011 (Christ Our Light). I compared the text of both 27 September files: the editorial
pages are identical and only the advertising page differs. Sampling both containers every
eight weeks back to September 2025 found the same shared content throughout. That is one
bulletin, so one row, with both organizations' ids in `publication`.

## Worship sites

Two: `st-clare-colonie` (1947 Central Ave.) and `christ-our-light-loudonville` (1 Maria Dr.).
The diocese lists them as two separate parishes with no "Other Worship Sites", and so does
GCatholic; neither records the shared bulletin. The diocese's institutional-records index
says Our Lady of Mercy (Colonie) and the Korean Catholic Apostolate (Loudonville) have their
records at Christ Our Light. Neither is in this region's roster entries and neither appears
in the bulletin; they were not given records here.

## Website and bulletin provider

ParishesOnline. `provider_id` is St. Clare's organization (church-of-saint-clare), whose
site stclarescolonie.com embeds it (`probe url` found po-org:church-of-saint-clare there);
Christ Our Light's site links its own container on christourlightchurch.org/bulletin
(visit.py found lpi:0018000000Qx7OVAAZ and po-container:03/1011). Either container gives
the same bulletin; St. Clare's was picked because its parish is named first in the
masthead. The row's name follows the masthead.

## Not yet confirmed

Nothing. The GCatholic site for Christ Our Light (christ-our-light.org) no longer resolves
(DEAD-DNS on 2026-09-28); christourlightchurch.org is the live one.
