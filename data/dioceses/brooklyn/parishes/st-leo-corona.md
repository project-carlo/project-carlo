---
name: St. Leo the Great (Corona)
website: https://stleo-queens.org/
bulletin_provider: other
provider_id: page-pdfs https://stleo-queens.org/bulletins
publication: []
group: Deanery Q3 (Queens West)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMjkvODNkZGQ1d2V2cl9PY3RvYmVyXzMxX05vdmVtYmVyXzFfMjAyNl9QYXJpc2hfQnVsbGV0aW5fU3QuX0xlb190aGVfR3JlYXRfUi5DLl9DaHVyY2gucGRmIl1d/October%2031%20-%20November%201%2C%202026%20Parish%20Bulletin%20%7C%20St.%20Leo%20the%20Great%20R.C.%20Church.pdf
  seen: 2026-11-05
  quote: SAINT LEO THE GREAT ROMAN CATHOLIC CHURCH
  note: Page 1 masthead of the October 30 - November 1, 2026 bulletin names Saint Leo the Great Roman
    Catholic Church, 48-01 104th Street, Corona alone (rectory 104-05 49th Avenue), Very Rev. Carlos A.
    Agudelo, Pastor.
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMjkvODNkZGQ1d2V2cl9PY3RvYmVyXzMxX05vdmVtYmVyXzFfMjAyNl9QYXJpc2hfQnVsbGV0aW5fU3QuX0xlb190aGVfR3JlYXRfUi5DLl9DaHVyY2gucGRmIl1d/October%2031%20-%20November%201%2C%202026%20Parish%20Bulletin%20%7C%20St.%20Leo%20the%20Great%20R.C.%20Church.pdf
  seen: 2026-11-05
  quote: 'Every Thursday:  5-7 pm - Chapel'
  note: 'Page 1 Mass times: Saturday 5:30pm English, 7:30pm Spanish; Sunday 7:00am, 8:30am, 11:30am, 1:00pm
    Spanish and 10:00am English; daily Mon-Sat 9:00am, Tuesday 7:30pm. No place is given for the Masses.
    The Our Lady of Mount Carmel Chapel, 103-56 52nd Avenue, appears only under Exposition (Thursday 5-7
    pm).'
- url: https://stleo-queens.org/mass-times
  seen: 2026-11-05
  quote: 'Every Thursday: 5-7:00 pm – Our Lady of Mount Carmel Chapel (103-56 52nd Ave., Corona, NY 11368)'
  note: The site's Mass Times page gives the same Mass schedule as the bulletin, with no place named,
    and attaches only Thursday adoration to the chapel.
- url: https://stleo-queens.org/bulletins
  seen: 2026-11-05
  note: Tilma bulletins page, newest first. The top card, Bulletin for November 8, 2026 (posted 5 Nov),
    has no file yet (its link is /bulletins/null); the next card links the October 30 - November 1 PDF.
research:
- method: fetch:check against the Tilma bulletins page
  url: https://stleo-queens.org/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Rerun fetch:check and confirm it picks the November 8, 2026 issue
  retry_when: The November 8, 2026 card on /bulletins links a PDF
  revisit_after: 2026-11-09
---

## Publisher

St. Leo publishes its own weekly bulletin on its Tilma site. The October 30 - November 1, 2026 issue (read 2026-11-05) has its masthead on page 1: "SAINT LEO THE GREAT ROMAN CATHOLIC CHURCH / ESTABLISHED IN 1903 / 48-01 104th Street, Corona, NY 11368", rectory at 104-05 49th Avenue, Very Rev. Carlos A. Agudelo, Pastor.

## Worship sites

One church, St. Leo. The page 1 Mass times (Saturday 5:30pm English, 7:30pm Spanish; Sunday 7:00am, 8:30am, 10:00am English, 11:30am, 1:00pm; Mon-Sat 9:00am; Tuesday 7:30pm Spanish) name no other place; the site's /mass-times page agrees.

The bulletin also prints "Our Lady of Mount Carmel Chapel, 103-56 52nd Avenue, Corona" (GCatholic 16796), but under Exposition only: "Every Thursday: 5-7 pm - Chapel". The 12 and 19 July 2026 issues (around the 16 July feast of Our Lady of Mount Carmel) have the same line and no Mass at the chapel. The chapel belongs to St. Leo, and nothing shows public Mass there or says it closed, so it is an `open/` record (`our-lady-of-mount-carmel-chapel-corona`), not a church row.

## Website and bulletin provider

`other`, read from the Tilma bulletins page `https://stleo-queens.org/bulletins` (newest first) with a `page-pdfs` recipe. The directory gives stleo-queens.org; GCatholic gives an older saintleoparish.org.

## Not yet confirmed

On 2026-11-05 the November 8 card was posted with no file, so the current pick is the November 1 issue; see research. Whether any Mass is said at the Mount Carmel chapel: see its `open/` record.
