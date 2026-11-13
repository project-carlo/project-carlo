---
name: St. Jerome (Flatbush)
website: https://stjeromercchurch.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/417
publication: ['url:https://www.church-bulletin.org/saint-jerome-s-roman-catholic-church-brooklyn-ny-11226']
group: Deanery B7 (Brooklyn East)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-jerome-s-roman-catholic-church-brooklyn-ny-11226/2026-11-08.pdf
  seen: 2026-11-06
  note: '8 November 2026 issue, 6 pages; page 1 is an image (read with render.py). Masthead ''ST. JEROME
    R.C. CHURCH, BROOKLYN, NEW YORK 11226'', 125th anniversary 1901-2026; Fr. Hilaire Belizaire, Pastor;
    parish office 455 East 29th St. Schedule of Masses, Sunday, Upper Church: 7:30 AM Creole, 9:45 AM
    English, 11:30 AM Spanish, 1:15 PM Creole; weekdays, Lower Church: 7:30 AM Monday-Friday English,
    9:30 AM Monday-Saturday Creole. Footer ''THIRTY-SECOND SUNDAY IN ORDINARY TIME - NOVEMBER 8, 2026''.'
- url: https://stjeromercchurch.org/wp-content/uploads/2026/10/St-Jerome-Bulletin-November-1-2026.pdf
  seen: 2026-11-06
  quote: 417 St. Jerome, Brooklyn, NY
  note: 1 November 2026 issue as posted on the parish site; page 6 footer names John Patrick Publishing
    Company job 417; page 2 lists the week's Mass intentions (7:30 AM daily) and a 9:45 AM English Mass.
- url: https://church-bulletin.org/417
  seen: 2026-11-06
  note: 'Redirects to https://www.church-bulletin.org/saint-jerome-s-roman-catholic-church-brooklyn-ny-11226,
    listing issue PDFs up to 2026-11-08.pdf, a week ahead of the parish site (newest there: November 1).'
promoted: 2026-11-12
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://church-bulletin.org/417
  url: https://church-bulletin.org/417
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check after 15 November and confirm it picks that issue
  retry_when: The 15 November issue is posted
  revisit_after: 2026-11-16
bulletin_status: available
---

## Publisher

St. Jerome, Flatbush publishes its own weekly bulletin, printed by John Patrick Publishing (job 417; page 6 footer "417 St. Jerome, Brooklyn, NY ... John Patrick Publishing Company"). The 8 November 2026 issue (read 2026-11-06 from church-bulletin.org; page 1 is an image) has the masthead "ST. JEROME R.C. CHURCH, BROOKLYN, NEW YORK 11226", Fr. Hilaire Belizaire, Pastor.

## Worship sites

One: St. Jerome church, 2900 Newkirk Avenue. Page 1's Schedule of Masses gives Sunday Masses in the Upper Church (7:30 AM Creole, 9:45 AM English, 11:30 AM Spanish, 1:15 PM Creole) and weekday Masses in the Lower Church (7:30 AM Monday-Friday English, 9:30 AM Monday-Saturday Creole): two levels of the one building. The directory, deanery list, GCatholic (16721) and Mass finder (1142) each list this one place.

## Website and bulletin provider

`other`, recipe `page-pdfs https://church-bulletin.org/417` (John Patrick slug page, a week ahead of the parish's WordPress `/bulletins/` page, which reposts the same issues as `St-Jerome-Bulletin-<Month>-<D>-<YYYY>.pdf`). Publication id `url:` the slug page. Page 1 is an image; pages 2-6 have text. `fetch:check` (2026-11-06) resolved "page-pdfs on https://church-bulletin.org/417: current" and picked `2026-11-08.pdf`, the 8 November 2026 issue (freshness `future`, already posted), transport ok, a PDF.

## Not yet confirmed

Nothing open; the next weekly pick is in research.
