---
name: St. Patrick Parish
website: https://saintpatrick-norristown.net
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401
publication: ['url:https://www.church-bulletin.org/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick Publishing listing 89, issue of 25 October 2026 (6 pages, bilingual English/Spanish).
    The text layer is a substitution cipher (pdftotext gives ''TRDQ...''-style gibberish; probe pdf is
    unreadable), so pages 1-2 were rendered. Page 1 masthead: ''ST. PATRICK CHURCH, 714 DEKALB ST., NORRISTOWN,
    PA 19401'', Gospel reflection in Spanish and English. Page 2 (footer ''Saint Patrick Church, Page
    2 - 0089''): Mass Intention Book for 2027, a Mass for St. Jude on Wednesday 28 October at 7:30 PM,
    Sunday collections 4 and 11 October. No Mass schedule box in the pages read.'
- url: https://www.church-bulletin.org/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 89 'Saint Patrick Church (Parroquia Catolica de San Patricio)', Norristown, PA 19401;
    latest edition October 25, 2026.
- url: https://saintpatrick-norristown.net/
  seen: 2026-10-28
  quote: Mass & Confession Schedule
  note: 'Parish site (probe url HTTP 200) links ''http://www.jppc.net/onlinebulletins/089template.pdf''
    and ''https://church-bulletin.org/?id=089'' for ''Our Church Bulletins''; hosts no PDFs of its own.
    Schedule on the home page: Saturday vigil 4 PM (English) and 6 PM (Spanish); Sunday 10 AM (English),
    8 AM and 12 PM (Spanish); weekdays Monday 6:00 PM (Spanish), Tuesday 8:00 AM, Wednesday 8:00 AM (bilingual),
    Thursday 8:00 AM (Spanish), Friday 8:00 AM; 5:00 PM bilingual vigil in summer.'
- url: https://parishesonline.com/organization/st-patrick-church-19401
  seen: 2026-10-28
  note: 'probe po st-patrick-church-19401 (lpi 0018000000Qx7ntAAB, 714 DeKalb St): ''no publications:
    this organization does not publish a bulletin here now''. An empty organization, so not a publication
    id.'
- url: https://archphila.org/parish/st-patrick-norristown/
  seen: 2026-10-28
  quote: Rev. Carlos F. Keen (Parochial Administrator)
  note: 'Directory: church at DeKalb and Chestnut Sts., rectory 714 DeKalb St., parish offices 703 Green
    Street, Hispanic apostolate; Mass times as on the site.'
publication_reviews:
- parish: holy-saviour-norristown
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names St. Patrick Church, 714 DeKalb St.,
      alone, in English and Spanish.
  - url: https://www.church-bulletin.org/bulletin/holy-saviour-parish-norristown-pa-19401/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead names Holy Saviour Parish, 407 E. Main Street, alone, with Masses
      at Holy Saviour Church and Our Lady of Mount Carmel only (Sunday 7:30, 9:30, 11:30 AM).
- parish: st-francis-of-assisi-norristown
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names St. Patrick Church, 714 DeKalb St.,
      alone, in English and Spanish.
  - url: https://www.church-bulletin.org/bulletin/saint-francis-of-assisi-parish-norristown-pa-19401/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 cover (page 1, image rendered) names St. Francis of Assisi, Norristown,
      alone; page 2 gives its own staff and Mass schedule (Saturday 5:30 PM, Sunday 7:00, 9:00 Spanish,
      11:30 AM).
- parish: epiphany-of-our-lord-plymouth-meeting
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names St. Patrick Church, 714 DeKalb St.,
      alone, in English and Spanish.
  - url: https://www.church-bulletin.org/bulletin/epiphany-of-our-lord-church-plymouth-meeting-pa-19462/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names Epiphany of Our Lord Church, 3050
      Walton Rd., alone, with its own Mass schedule (Saturday 5 PM, Sunday 8, 10 AM and 4 PM).
---

## Publisher

St. Patrick Parish, Norristown (Parochial Administrator Rev. Carlos F. Keen; English and Spanish Masses) is distributed by John Patrick Publishing as listing 89, 'Saint Patrick Church (Parroquia Catolica de San Patricio)'. The 25 October 2026 issue's page-1 masthead reads 'St. Patrick Church, 714 DeKalb St., Norristown, PA 19401' and its footer on page 2 'Saint Patrick Church ... 0089'. The parish's own site links the listing and posts no files. The ParishesOnline organization `st-patrick-church-19401` exists but is empty ('does not publish a bulletin here now'), so it is not a channel and not in `publication`. The row is `other` with `page-pdfs` on the listing.

The PDF's text layer is garbled (a font-encoding substitution), so `fetch:check` can't verify identity from text; the masthead was read from the rendered page.

## Worship sites

One church, St. Patrick (DeKalb and Chestnut Sts.). The pages of the issue read (1-2) have no Mass box; the Mass schedule is the parish site's (Saturday vigil 4 PM English and 6 PM Spanish, Sunday 8 AM and 12 PM Spanish and 10 AM English, weekdays 8:00 AM or Monday 6:00 PM), which agrees with the directory. The parish site and bulletin name no other church. The Missionary Sisters of Charity convent (630 DeKalb St.) and the Patrician Society on the directory page are not worship sites listed by the parish.

## Website and bulletin provider

saintpatrick-norristown.net hosts no bulletin; the listing's dated PDFs `https://www.church-bulletin.org/bulletin/saint-patrick-church-parroquia-catolica-de-san-patricio-norristown-pa-19401/<yyyy-mm-dd>.pdf` are the channel.

## Fetch check

`fetch:check` (2026-10-28) resolved `page-pdfs` on the listing to the 2026-10-25 issue: transport ok, PDF, fresh (3 days); identity "unverified" because the PDF has no usable text layer (a read-only render of the masthead settled identity above). The recipe is already in `provider_id`.

## Not yet confirmed

Pages 3-6 of the 25 October issue were not read; a Mass box there would confirm the site's schedule from the bulletin itself. Nothing suggests another church.
