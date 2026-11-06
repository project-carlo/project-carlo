---
name: St. John the Evangelist, Bergenfield
website: https://sjrc.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6050
publication: ['url:https://www.church-bulletin.org/saint-john-the-evangelist-roman-catholic-church-bergenfield-nj-07621']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-church-bergenfield-nj-07621/2026-11-01.pdf
  seen: 2026-11-03
  note: 'Page 1 is an image (no text layer; rendered with render.py). Masthead: ''ST. JOHN THE EVANGELIST,
    29 N. WASHINGTON AVE, BERGENFIELD, NJ | 201.384.0101 | SJRC.ORG'', ''SOLEMNITY OF ALL SAINTS NOVEMBER
    1, 2026'', pastor Rev. Sean A. Manson. Mass schedule box: Sat Vigil 5:30, 7:00 PM (Sp); Sun 7:30,
    9:00, 10:30 AM, 12:00, 1:15 PM (Sp); Daily (Mon-Fri) 7:00, 9:00 AM, 6:30 PM (Tues 6:30 PM Sp); Sat
    7:00, 9:00 AM. No other worship site named.'
- url: https://www.church-bulletin.org/saint-john-the-evangelist-roman-catholic-church-bergenfield-nj-07621
  seen: 2026-11-03
  quote: '2026-11-01'
  note: John Patrick Publishing listing, one PDF per Sunday, newest 2026-11-01; https://church-bulletin.org/6050
    redirects here.
- url: https://sjrc.org/wp-content/uploads/2026/09/2026-08-30.pdf
  seen: 2026-11-03
  note: 'Last issue on the parish''s own Bulletin page (image-only, rendered): same masthead, 30 August
    2026; page 8 footer ''6050 St. John the Evangelist, Bergenfield, NJ (B) … John Patrick Publishing
    Co., Inc.'', which gives the JPP id.'
- url: https://sjrc.org/wp-json/wp/v2/media?mime_type=application/pdf&per_page=10&orderby=date
  seen: 2026-11-03
  quote: 2026-08-30.pdf
  note: The parish WordPress media library's newest PDF is the 30 August 2026 bulletin, uploaded 2026-09-05;
    the site's /bulletin page (modified 2026-09-05) lists nothing later.
bulletin_status: available
publication_reviews:
- parish: st-mary-dumont
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-church-bergenfield-nj-07621/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names St. John the Evangelist, Bergenfield alone, with its own
      Mass times.
  - url: https://www.church-bulletin.org/bulletin/saint-mary-s-church-dumont-nj-07628/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead of the peer's bulletin names St. Mary's Church, Dumont alone, with
      its own Mass times.
- parish: ascension-new-milford
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-church-bergenfield-nj-07621/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names St. John the Evangelist, Bergenfield alone, with its own
      Mass times.
  - url: https://files.ecatholic.com/39014/bulletins/20261101.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead of the peer's bulletin names Church of the Ascension, New Milford
      alone, with its own Mass times.
- parish: st-joseph-oradell
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-church-bergenfield-nj-07621/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names St. John the Evangelist, Bergenfield alone, with its own
      Mass times.
  - url: https://container.parishesonline.com/bulletins/04/0064/20261101B.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead of the peer's bulletin names Saint Joseph Roman Catholic Church,
      Oradell/New Milford alone, with its own Mass times.
---

## Publisher

St. John the Evangelist, 29 N. Washington Ave, Bergenfield, publishes its own weekly bulletin through John Patrick Publishing (id 6050, from the footer '6050 St. John the Evangelist, Bergenfield, NJ (B)' of the 30 August 2026 issue). I read the 1 November 2026 (All Saints) issue from the church-bulletin.org listing: page 1 is an image, and its masthead names St. John the Evangelist alone, pastor Rev. Sean A. Manson.

## Worship sites

One church, `st-john-the-evangelist-bergenfield`: the masthead's Mass schedule (Saturday Vigil 5:30 and 7:00 PM Spanish; Sunday 7:30, 9:00, 10:30 AM, 12:00 and 1:15 PM Spanish; weekdays 7:00, 9:00 AM and 6:30 PM) names no other place. The directory (8) and GCatholic (18364) list only this church.

## Website and bulletin provider

https://sjrc.org/ (WordPress) answers `probe get`. Its /bulletin page lists self-hosted copies, but the newest is the 30 August 2026 issue (media library, 2026-11-03), so the row reads John Patrick's listing instead: `page-pdfs https://church-bulletin.org/6050`, which redirects to the dated listing recorded in `publication` (newest 2026-11-01). Provider `other`. The issues are image-only (no text layer), so the pipeline has to read them as images, and the evidence above is cited by note.

Fetch check (2026-11-03, headed): ok, `page-pdfs on https://church-bulletin.org/6050: current`, picked the 2026-11-01 issue (PDF, first page without text); the pinned recipe is the one it printed.

## Not yet confirmed

Nothing outstanding.
