---
name: Holy Cross (Flatbush)
website: https://www.holycrossrcchurch.org/weekly-bulletin
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/487
publication: ['url:https://www.church-bulletin.org/holy-cross-roman-catholic-church-brooklyn-ny-11226']
group: Deanery B7 (Brooklyn East)
evidence:
- url: https://www.church-bulletin.org/bulletin/holy-cross-roman-catholic-church-brooklyn-ny-11226/2026-11-08.pdf
  seen: 2026-11-06
  note: '8 November 2026 issue, 6 pages, all images (no text layer; read with render.py). Page 1 masthead:
    ''Holy Cross Roman Catholic Church'', 2530 Church Ave, Brooklyn, NY 11226; Pastor Msgr. Joseph P.
    Malagreca; ''32nd SUNDAY IN ORDINARY TIME - Nov. 8, 2026''. Sunday Mass Schedule: 5:00 PM Saturday;
    8:30 AM (church) & 11:30 AM Sunday (chapel) in English; 10:00 AM domingo en espanol; 11h30 en creole
    dans l''eglise; weekday Masses every day 8:30 AM.'
- url: https://www.church-bulletin.org/bulletin/holy-cross-roman-catholic-church-brooklyn-ny-11226/2026-11-08.pdf
  seen: 2026-11-06
  note: 'Page 6 (image) footer: ''487 Holy Cross, Brooklyn, NY (B) U'' and ''John Patrick Publishing Co.
    1.800.333.3166 www.jppc.net'': John Patrick Publishing job 487.'
- url: https://church-bulletin.org/487
  seen: 2026-11-06
  note: Redirects to https://www.church-bulletin.org/holy-cross-roman-catholic-church-brooklyn-ny-11226,
    listing issue PDFs up to 2026-11-08.pdf.
- url: https://www.holycrossrcchurch.org/weekly-bulletin
  seen: 2026-11-06
  note: Parish site's Weekly Bulletin page links the church-bulletin.org/bulletin/holy-cross-roman-catholic-church-brooklyn-ny-11226/YYYY-MM-DD.pdf
    issues, 2026-01-04 to 2026-11-01 when read.
promoted: 2026-11-12
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://church-bulletin.org/487
  url: https://church-bulletin.org/487
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check after 15 November and confirm it picks that issue
  retry_when: The 15 November issue is posted
  revisit_after: 2026-11-16
bulletin_status: available
---

## Publisher

Holy Cross, Flatbush publishes its own weekly bulletin, printed by John Patrick Publishing (page 6 footer "487 Holy Cross, Brooklyn, NY (B) U", "John Patrick Publishing Co."). The 8 November 2026 issue (read 2026-11-06 from church-bulletin.org) has the page 1 masthead "Holy Cross Roman Catholic Church", 2530 Church Ave, Brooklyn, NY 11226, Pastor Msgr. Joseph P. Malagreca. Every page is an image; read with `render.py`.

## Worship sites

One: Holy Cross church, 2530 Church Avenue. The page 1 Sunday Mass Schedule gives 5:00 PM Saturday; 8:30 AM (church) and 11:30 AM Sunday (chapel) in English; 10:00 AM in Spanish; 11:30 AM in Creole in the church; weekdays 8:30 AM. The "chapel" Mass runs at the same hour as the Creole Mass in the church, and the bulletin gives no other address, so it is read as a chapel at the parish's own premises, not a separate worship site (inferred; not confirmed). The directory, deanery list, GCatholic (16607) and Mass finder (1118) each list this one place.

## Website and bulletin provider

`other`, recipe `page-pdfs https://church-bulletin.org/487` (the John Patrick slug page, which gets each issue first). Publication id `url:` the slug page. The parish site's `/weekly-bulletin` page links the same PDFs. The PDFs are image-only. `fetch:check` (2026-11-06) resolved "page-pdfs on https://church-bulletin.org/487: current" and picked `2026-11-08.pdf`, the 8 November 2026 issue (freshness `future`: this coming Sunday's, already posted), transport ok, a PDF.

## Not yet confirmed

Where the "chapel" of the 11:30 AM English Mass is: assumed on the church premises; a page of the parish site or a later bulletin naming it would settle it.
