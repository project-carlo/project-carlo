---
name: St. Paul
website: https://stpaulprospect.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-paul-roman-catholic-church-prospect-park-nj-07508
publication: ['url:https://www.church-bulletin.org/saint-paul-roman-catholic-church-prospect-park-nj-07508']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-paul-roman-catholic-church-prospect-park-nj-07508/2026-11-01.pdf
  seen: 2026-11-04
  note: '1 November 2026 issue, 6 pages, all images (probe pdf finds no text); page 1 rendered: masthead
    ''SAINT PAUL R.C. CHURCH 286 Haledon Avenue, Prospect Park, NJ Serving the Communities of Paterson-
    Prospect Park - Haledon -North Haledon'', ''SOLEMNITY OF ALL SAINTS November 1, 2026''; Mass Schedule
    ''DAILY MASS: 8:00 AM'', Weekend Masses ''SATURDAY ...... 5:00 PM (also live streamed) SUNDAY 8:00
    AM 10:00 AM 12:00 Noon: (Spanish)'', Misas en Espanol ''MIERCOLES ... Santa Misa 6:30pm''; Rev. Henry
    Pinto, Pastor; parish office 80 North 13th Street, Prospect Park NJ 07508; image credit ''© JPPC''.
    No other church named.'
- url: https://www.jppc.net/onlinebulletins/6012template.pdf
  seen: 2026-11-04
  note: 'The Bulletins link on the parish site (home page and /bulletins); probe get follows it to an
    HTML page, https://www.church-bulletin.org/saint-paul-roman-catholic-church-prospect-park-nj-07508,
    which (read with visit.py) lists weekly issues newest first: 2026-11-01, Oct 25 2026, Oct 18 2026,
    Oct 11 2026, Oct 4 2026, Sep 27 2026.'
- url: https://stpaulprospect.com/bulletins
  seen: 2026-11-04
  note: Read with visit.py (probe url gets 403). eCatholic site 11956, title 'St. Paul, Prospect Park
    - Prospect Park, NJ' on the home page; /bulletins links only 'Bulletins' to the jppc.net template
    and lists no eCatholic bulletin files.
bulletin_status: available
---

## Publisher

St. Paul, Prospect Park publishes a weekly bulletin through John Patrick Publishing (JPPC customer 6012), posted on church-bulletin.org. Page 1 of the 1 November 2026 issue (`https://www.church-bulletin.org/bulletin/saint-paul-roman-catholic-church-prospect-park-nj-07508/2026-11-01.pdf`, read 2026-11-04, rendered as the issue is image-only) reads "SAINT PAUL R.C. CHURCH 286 Haledon Avenue, Prospect Park, NJ Serving the Communities of Paterson- Prospect Park - Haledon -North Haledon", "November 1, 2026", and names Rev. Henry Pinto, Pastor. It names no other parish.

## Worship sites

- `st-paul-prospect-park`: the 1 November 2026 masthead gives daily Mass 8:00 AM, "SATURDAY ...... 5:00 PM ... SUNDAY 8:00 AM 10:00 AM 12:00 Noon: (Spanish)" and a Wednesday Spanish Mass at 6:30pm.

The bulletin names no other place of Mass; 80 North 13th Street is the parish office. The finder (directory:11956) and GCatholic (18966) list this one church.

## Website and bulletin provider

The website is the parish's eCatholic site (site id 11956; read with visit.py, as `probe url` gets 403). Its Bulletins link is `https://www.jppc.net/onlinebulletins/6012template.pdf`, which redirects to the church-bulletin.org listing; the site posts no eCatholic bulletin files, so `ecatholic:11956` is not recorded as a publication id. Provider `other` with the recipe `page-pdfs https://www.church-bulletin.org/saint-paul-roman-catholic-church-prospect-park-nj-07508`. `fetch:check` on 2026-11-04 picked the 1 November 2026 issue ("page-pdfs on https://www.church-bulletin.org/saint-paul-roman-catholic-church-prospect-park-nj-07508: current", 3 days old, dated from the file name); identity is unverified because the issue has no text layer, and the masthead was checked by rendering page 1.

The issues are images only (no text layer), so the pipeline will need OCR to read Mass times.

## Not yet confirmed

Nothing outstanding.
