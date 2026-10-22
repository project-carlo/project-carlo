---
name: Sacred Heart Parish, Altoona
website: https://www.sacredheartaltoona.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.sacredheartaltoona.org/bulletin/bulletin.pdf']
group: ''
evidence:
- url: https://www.sacredheartaltoona.org/bulletin/bulletin.pdf
  seen: 2026-10-21
  quote: SACRED HEART ROMAN CATHOLIC CHURCH
  note: Page 1 of the issue dated October 18, 2026 (9 pages, text layer, 4,119,507 bytes, Last-Modified
    Fri 16 Oct 2026). The masthead names Sacred Heart alone; the directory section lists a Rev. as Pastor.
- url: https://www.sacredheartaltoona.org/bulletin/bulletin.pdf
  seen: 2026-10-21
  quote: 'Saturday: (Vigil) 5:30 P.M. • Sunday: 7:45 a.m., 10:00 a.m., 12:00 Noon'
  note: Mass schedule on page 1 of the same issue; page 2 is "MASS SCHEDULE AND INTENTIONS" for this church
    only.
promoted: 2026-10-21
---

## Publisher

Sacred Heart publishes its own weekly bulletin on its own site. The file
`https://www.sacredheartaltoona.org/bulletin/bulletin.pdf` served, on 21 October 2026, the
issue dated "October 18, 2026" (9 pages, text layer), whose masthead is "SACRED HEART ROMAN
CATHOLIC CHURCH ... 511 TWENTIETH STREET, ALTOONA, PA  16602" with the rectory phone
814-943-8553 (GCatholic's number for the church). Page 2, "MASS SCHEDULE AND INTENTIONS",
lists intentions for this church only. No other parish or church is named in the masthead.
The directory lists the parish with one church and no companion parish.

## Worship sites

One church, Sacred Heart (churches/sacred-heart-altoona). Nothing else in the bulletin or the
directory entry. (Sacred Heart Worship Site in Central City belongs to Our Lady Queen of
Angels, a different parish.)

## Website and bulletin provider

`bulletin_provider: other`. The site's `/bulletin/` page links one fixed file,
`bulletin.pdf`, which the parish overwrites weekly (so the URL is not a dated, permanent
record), and a "past" page that lists no PDFs. `pnpm fetch:check --diocese altoona-johnstown
--parish sacred-heart-altoona` on 2026-10-21 resolved "page-pdfs on
https://www.sacredheartaltoona.org/bulletin/: first-listed" and fetched `bulletin.pdf` (status
ok, 4,119,507 bytes, no date in the URL; the issue inside is October 18, 2026, which is this
week's). Recipe `page-pdfs` is the `provider_id`. `publication` is `url:` of the bulletin
file. The homepage the directory gives is `https://www.sacredheartaltoona.org`.

## Not yet confirmed

Nothing about the bulletin. Because the URL never changes, check on later runs that the issue
inside is the current week's.
