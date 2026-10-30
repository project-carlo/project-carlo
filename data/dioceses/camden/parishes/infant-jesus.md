---
name: Infant Jesus Parish
website: https://theinfantjesusparish.org/weekly-bulletin/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/infant-jesus-parish-woodbury-heights-nj-08097
publication: ['url:https://www.church-bulletin.org/infant-jesus-parish-woodbury-heights-nj-08097#john-patrick-507']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/infant-jesus-parish-woodbury-heights-nj-08097/2026-10-25.pdf
  seen: 2026-10-29
  note: Image-only PDF (16 pages); page 1 rendered and read, so recheck can't find these words as text.
    The masthead names 'Infant Jesus Parish' with 'St. John Vianney Church, 2901 Good Intent Road, Deptford,
    NJ 08096' and 'St. Margaret Church, 845 Third Street, Woodbury Heights, NJ 08097' under the date October
    25, 2026, one bulletin for both churches.
- url: https://www.church-bulletin.org/bulletin/infant-jesus-parish-woodbury-heights-nj-08097/2026-10-25.pdf
  seen: 2026-10-29
  note: 'Page 1 liturgical schedule (image): Saturday 4:00 PM at St. Margaret (live streamed); Sunday
    8:30 and 10:00 AM at St. Margaret, 11:30 AM at St. John Vianney; daily 6:45 AM in the convent on school
    days, Monday to Saturday 8:30 AM at St. Margaret; Reverend Joseph L. Pham, Pastor; Reverend Alfred
    Mungujakisa, Parochial Vicar.'
- url: https://theinfantjesusparish.org/weekly-bulletin/
  seen: 2026-10-29
  note: 'probe get: the parish''s own bulletin page links http://www.jppc.net/onlinebulletins/507template.pdf,
    which curl -L resolves (301, 301, 302) to the church-bulletin.org listing used here.'
- url: https://www.church-bulletin.org/infant-jesus-parish-woodbury-heights-nj-08097
  seen: 2026-10-29
  note: Listing for Infant Jesus Parish, Woodbury Heights NJ 08097; dated PDFs weekly, latest 2026-11-01
    (posted ahead), then 2026-10-25, 2026-10-18, 2026-10-11.
promoted: 2026-10-30
---

## Publisher

John Patrick Publishing (id 507) prints the bulletin and the church-bulletin.org listing serves it. The 25 October 2026 issue (page 1, read 2026-10-29 from a rendered image) is headed 'Infant Jesus Parish' with the two churches' names and addresses either side of the date, and its schedule assigns Masses to both. Pastor Rev. Joseph L. Pham (the directory's Fr. Joseph Szolack is from 2015). One bulletin for the two churches.

## Worship sites

Two churches, both in the 25 October 2026 schedule: St. Margaret, 845 Third Street, Woodbury Heights (Saturday 4:00 PM, Sunday 8:30 and 10:00 AM, weekday 8:30 AM, Holy Day and Reconciliation) and St. John Vianney, 2901 Good Intent Road, Deptford (Sunday 11:30 AM, Holy Day vigil 6:00 PM). GCatholic lists both with group 'Infant Jesus Parish'; the diocese directory lists the parish once, at the mailing address 334 Beech Avenue, Woodbury Heights (the parish office, not a worship site). The convent at 745 Third Street hosts the school-day 6:45 AM Mass; it is a convent chapel and the bulletin gives no public Mass there beyond that, so it gets no church row (see Not yet confirmed).

## Website and bulletin provider

`other` with a `page-pdfs` recipe on the church-bulletin.org listing, which the parish's own page reaches through jppc.net 507. The parish's /weekly-bulletin/ page is an archive by year. The publication id is the listing URL with a John Patrick suffix. The bulletin is image-only (no text layer), so the pipeline has to read it as an image.

`fetch:check` (2026-10-29) picked the 2026-11-01 PDF on the listing: transport ok, PDF, issue date inferred from the file name (image-only), freshness 'future' (posted three days ahead, not a wrong pick; 2026-10-25 is the Sunday read above), publication identity unverified because the text layer is empty.

## Not yet confirmed

Whether the 6:45 AM school-day Mass 'in Convent' is open to the public: the bulletin says only 'School Days'. It is a daily convent Mass of the Sisters; no other source read.
