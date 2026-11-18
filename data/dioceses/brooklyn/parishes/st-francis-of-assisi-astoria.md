---
name: St. Francis of Assisi (Astoria)
website: https://stfrancisofassisiastoria.org/important-information/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://stfrancisofassisiastoria.org/important-information/bulletin/
publication: ['url:https://stfrancisofassisiastoria.org/important-information/bulletin/']
group: Deanery Q1 (Queens West)
evidence:
- url: http://stfrancisofassisiastoria.org/wp-content/uploads/sites/15/2026/11/nov8_2026_stfrancis_compressed.pdf
  seen: 2026-11-06
  quote: For the People of St. Francis
  note: '8 November 2026 issue (13 pages, downloaded with tools/fetch-pdf.py; pages 6-8, 10-12 images).
    No cover page: page 1 opens ''Sunday, Nov. 8 32nd Sunday in Ordinary Time'' with Mass intentions Sunday
    8:00AM, 9:30AM, 11:00AM, weekdays and Saturday 9:00AM, Saturday 5:00PM ''For the People of St. Francis
    Of Assisi''. Pastor''s letters signed ''Msgr. Maresca''; ''through the Rectory at (718) 728-7801'';
    ''The Entrance is on the 45th Street side of the Church.'' No other church named; no LPi footer (page
    11 is a parish tuition form, page 12 an SFA altar server form).'
- url: https://stfrancisofassisiastoria.org/important-information/bulletin/
  seen: 2026-11-06
  note: 'Bulletin page (WordPress multisite, sites/15; read with parish-site-access visit.py, probe url
    gets RemoteDisconnected) lists weekly PDFs newest first: nov8_2026_stfrancis_compressed.pdf, nov1_...,
    oct25_..., oct18_..., oct11_..., oct4_..., sept27_...'
- url: https://stfrancisofassisiastoria.org/
  seen: 2026-11-06
  quote: 'Sunday: 8:00am, 9:30am, and 11:00am'
  note: 'Homepage (visit.py): ''SUNDAY MASSES: Saturday: 5:00pm Sunday: 8:00am, 9:30am, and 11:00am WEEKDAY
    MASS: Monday - Saturday: 9:00am''; footer ''St. Francis of Assisi Parish, Astoria NY''.'
- url: https://parishesonline.com/organization/st-francis-of-assisi-church-11105
  seen: 2026-11-06
  note: 'probe po: ''St. Francis of Assisi Church'', 2117 45th St, lpi 0018000000QxB9AAAV, no issues (''this
    organization does not publish a bulletin here now''): an empty org, not a publication id.'
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

St. Francis of Assisi, Astoria publishes its own weekly bulletin as PDFs on its parish site's bulletin page (https://stfrancisofassisiastoria.org/important-information/bulletin/, newest first). The 8 November 2026 issue (`nov8_2026_stfrancis_compressed.pdf`, read 2026-11-06) has no cover page; page 1 gives the week's Mass intentions, with Saturday 5:00PM and Sunday 11:00AM "For the People of St. Francis Of Assisi", the pastor's letter is signed "Msgr. Maresca", and it gives the rectory number (718) 728-7801 that the diocese directory lists. It is self-made: no LPi footer, and the ParishesOnline org `st-francis-of-assisi-church-11105` holds no issues.

## Worship sites

One. The 8 November 2026 intentions give Saturday 5:00PM, Sunday 8:00AM, 9:30AM and 11:00AM, and Monday-Saturday 9:00AM, matching the homepage's Mass schedule; no other church or chapel is named. The directory, the deanery list, GCatholic 16709 and Mass finder 1194 give the one church at 21-17 45th Street.

## Website and bulletin provider

`other`, recipe `page-pdfs` on the bulletin page. The site is on the WordPress multisite (`/wp-content/uploads/sites/15/`) that drops `probe url` and `probe pdf` connections; it loads in `visit.py` and fetch. Files are named `<mon><d>_<yyyy>_stfrancis_compressed.pdf`. Publication id is the bulletin page (`url:`), as the issue is self-hosted.

## Not yet confirmed

Nothing open. The issue's image pages 7-8 were not read.
