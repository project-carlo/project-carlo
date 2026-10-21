---
name: Saint Benedict Parish, Johnstown
website: https://stbenedictchurch.org
bulletin_provider: other
provider_id: page-pdfs https://stbenedictchurch.org/about-us/weekly-bulletin/
publication: ['url:https://stbenedictchurch.org/about-us/weekly-bulletin/']
group: ''
evidence:
- url: https://stbenedictchurch.org/files/2026/10/Bulletin-101826-complete.pdf
  seen: 2026-10-21
  quote: Angel Tree Program
  note: 'The 18 October 2026 issue (14 pages; downloaded with the fetch client, since SiteGround sgcaptchas curl). Pages 1-3 are images: I rendered page 1 and read it. It is headed "St. Benedict Church, OCTOBER 18, 2026 | 29TH SUNDAY ORDINARY TIME", "MASS SCHEDULE Saturday | 5:00pm Vigil Sunday | 8:30 am & 10:30 am", "Weekday Masses Monday & Friday | 8:00 am Tuesday & Thursday | 12:05 pm Wednesday | 9:00 am", and "GET IN TOUCH 2310 Bedford Street Johnstown, PA 15904 814-266-9718 sbpastor@stbenedictchurch.org www.stbenedictchurch.org". It names St. Benedict alone. The quote is from the text layer of a later page.'
- url: https://stbenedictchurch.org/about-us/weekly-bulletin/
  seen: 2026-10-21
  note: 'St. Benedict''s Weekly Bulletin page (WordPress on SiteGround; read in headed Chrome) links /files/2026/10/Bulletin-101826-complete.pdf, Bulletin-101126-complete.pdf and Bulletin-100426-complete.pdf: one PDF per week, current. The home page links here.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory lists Saint Benedict, 2310 Bedford Street, Johnstown 15904, homepage stbenedictchurch.org; Saturday 5:00 PM, Sunday 8:30 AM and 10:30 AM, weekdays as the bulletin.'
---

## Publisher

St. Benedict publishes its own weekly bulletin on its WordPress site (SiteGround) at
https://stbenedictchurch.org/about-us/weekly-bulletin/, one PDF a week under `/files/YYYY/MM/`.
The 18 October 2026 issue's cover (an image, rendered and read 2026-10-21) is headed "St.
Benedict Church" with its Mass schedule and the 2310 Bedford Street address and names no other
parish. The Resurrection / St. Clare bulletin lists a "Marian Celebration" at St. Benedict
Church on 18 October, but that is only an event in a neighbour's calendar. One church, one
bulletin.

## Worship sites

One: St. Benedict Church, 2310 Bedford Street, Johnstown 15904.

## Website and bulletin provider

`bulletin_provider: other`, website https://stbenedictchurch.org, publication id the bulletin
page. `fetch:check` on 2026-10-21 resolved `page-pdfs on https://stbenedictchurch.org/about-us/weekly-bulletin/:
current` to Bulletin-101826-complete.pdf (11.8 MB, ok) and printed the recipe `page-pdfs
https://stbenedictchurch.org/about-us/weekly-bulletin/`. The site resets `probe url` (UNREACHABLE) and
sgcaptchas curl on its PDFs; headed Chrome reads the pages and the fetch client downloads the PDFs.
The 11.8 MB file has image pages 1-3, so the schedule on the cover is not in the text layer.

## Not yet confirmed

Nothing outstanding for the row. Because the cover is an image, the pipeline will need image
reading for the Mass schedule.
