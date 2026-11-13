---
name: St. Catherine of Genoa (East Flatbush)
website: https://stcatherinegenoabrooklyn.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery B7 (Brooklyn East)
evidence:
- url: https://stcatherinegenoabrooklyn.com/bulletins
  seen: 2026-11-06
  quote: Bulletin for Sunday, Aug 23, 2026
  note: 'Tilma (webstudio) bulletins page, cards newest first: Aug 23, Aug 16, Aug 09, Aug 02, Jul 26
    ... 2026; the homepage''s latestBulletinData gives totalCount 254 with the newest ''bulletin-for-sunday-aug-23-2026''.
    Nothing posted for September-November. Upload tokens decode to 2026/08/07, 08/14, 08/21: weekly uploads
    that then stopped.'
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMDgvMjEvNm1iaDFuMnNrNF81MDA3ODUuMDgyMzI2LnBkZiJdXQ/500785.082326.pdf
  seen: 2026-11-06
  quote: 'Church: 846 Albany Avenue, Brooklyn, NY 11203'
  note: '23 August 2026 issue (the newest), 8 pages, text layer with a shifted-font date line. Masthead
    ''Saint Catherine of Genoa R. C. Church'', Mailing: 520 Linden Boulevard; Pastor Rev. Raphael Munday
    Kukana. Eucharistic Liturgies: Sunday 8:00 AM & 11:00 AM (English), 1:00 PM (French & Kreyol), 5:00
    PM (Twi); weekdays Monday-Saturday 9:00 AM. No publisher footer or LPi number; file name 500785.MMDDYY.pdf.'
- url: https://parishesonline.com/organization/st-catherine-of-genoa-church
  seen: 2026-11-06
  note: 'probe po st-catherine-of-genoa-church: org ''St. Catherine of Genoa Church'', 520 Linden Blvd,
    lpi 0018000000Qc1FzAAJ, no publications. Not a publication id (no issues). The forms st-catherine-of-genoa-church-11203,
    st-catherine-church-11203, saint-catherine-of-genoa-church-11203 and st-catherine-of-genoa-roman-catholic-church-11203
    find no org.'
- url: https://discovermass.com/church/st-catherine-of-genoa-brooklyn-ny/
  seen: 2026-11-06
  quote: There are currently no bulletins available for St. Catherine of Genoa.
  note: Discover Mass page exists (846 Albany Ave.) with no bulletins.
research:
- method: Tilma /bulletins page, ParishesOnline org probes, Discover Mass page
  url: https://stcatherinegenoabrooklyn.com/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Reread https://stcatherinegenoabrooklyn.com/bulletins for cards after Aug 23, 2026 and
    probe po st-catherine-of-genoa-church for issues; if a current issue appears, set bulletin_provider
    other with provider_id 'page-pdfs https://stcatherinegenoabrooklyn.com/bulletins' (or parishes_online
    with the org) and run fetch:check
  retry_when: The parish posts a bulletin after 23 August 2026, or a month has passed
  revisit_after: 2026-12-07
bulletin_status: not-found
---

## Publisher

St. Catherine of Genoa, East Flatbush, published its own weekly bulletin on its Tilma site until the 23 August 2026 issue (masthead "Saint Catherine of Genoa R. C. Church", Mailing: 520 Linden Boulevard, Church: 846 Albany Avenue; Pastor Rev. Raphael Munday Kukana). The issues carry no publisher footer or LPi number; the file names are `500785.MMDDYY.pdf`. As read on 2026-11-06, nothing newer has been posted: the `/bulletins` cards run weekly to "Bulletin for Sunday, Aug 23, 2026" (254 in all), uploaded weekly until 21 August.

## Worship sites

One: St. Catherine of Genoa church, 846 Albany Avenue (corner of Linden Boulevard). The 23 August bulletin's Eucharistic Liturgies give Sunday 8:00 AM and 11:00 AM (English), 1:00 PM (French and Kreyol), 5:00 PM (Twi), weekdays Monday-Saturday 9:00 AM; the site's `/mass-times` page (read 2026-11-06) gives the same times. The directory, deanery list, GCatholic (16694) and Mass finder (753) each list this one place, at the 520 Linden Blvd mailing address.

## Website and bulletin provider

`no_bulletin`, status `not-found`: the newest issue anywhere is 23 August 2026, about eleven weeks old. Checked: the Tilma `/bulletins` page and the homepage's `latestBulletinData`; ParishesOnline (`st-catherine-of-genoa-church` exists, lpi 0018000000Qc1FzAAJ, with no issues; zip and long forms find no org); Discover Mass (page, no bulletins). The ParishesOnline org has no issues, so it is not recorded as a publication id. If posting resumes, the recipe is `page-pdfs https://stcatherinegenoabrooklyn.com/bulletins` (Tilma webstudio, cards newest first).

## Not yet confirmed

Whether the parish has stopped posting or is behind: the research item rechecks the Tilma page and the ParishesOnline org after 7 December 2026.
