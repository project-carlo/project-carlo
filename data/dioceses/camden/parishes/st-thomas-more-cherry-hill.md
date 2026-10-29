---
name: St. Thomas More Church
website: https://www.stthomasmorenj.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-thomas-more-church-cherry-hill-nj-08003
publication: ['url:https://www.church-bulletin.org/saint-thomas-more-church-cherry-hill-nj-08003#john-patrick-632']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-thomas-more-church-cherry-hill-nj-08003/2026-10-25.pdf
  seen: 2026-10-29
  note: Image-only PDF (8 pages, no text layer; page 1 rendered with render.py and read). Masthead 'St.
    Thomas More Church, 1439 Springdale Road, Cherry Hill, New Jersey 08003', 'Father Michael J. Matveenko,
    Administrator'; Mass Schedule Daily Mass Mon.-Fri. 9:00 AM in the Chapel, Sat. 4:30 PM, Sun. 8:30
    and 11:00 AM. Names this parish alone; recheck can't find the words as text.
- url: https://www.stthomasmorenj.org/sunday-bulletins.html
  seen: 2026-10-29
  quote: Below you can find the latest copies of our weekly parish bulletin.
  note: The parish's Sunday Bulletins page builds its links in JavaScript from 'https://church-bulletin.org/632/'
    (John Patrick id 632); the fixed href in its source is church-bulletin.org/632/2026-07-05.pdf, which
    redirects to the church-bulletin.org listing's PDF for that date.
- url: https://www.church-bulletin.org/saint-thomas-more-church-cherry-hill-nj-08003
  seen: 2026-10-29
  note: Listing 'Saint Thomas More Church Bulletin'; dated weekly PDFs, latest 2026-10-25 (the 1 November
    issue was not yet posted).
---

## Publisher

John Patrick Publishing (id 632) prints the bulletin and the church-bulletin.org listing serves it; the parish's Sunday Bulletins page reads from `church-bulletin.org/632/` (checked 2026-10-29). The 25 October 2026 issue is an image-only PDF. Page 1 (rendered and read) is headed 'St. Thomas More Church, 1439 Springdale Road, Cherry Hill, New Jersey 08003' and names Father Michael J. Matveenko as Administrator, Father Victorino Coronado in residence and Deacon Frank A. Baratta. Its Mass Schedule is Daily Mass Monday to Friday 9:00 AM in the Chapel, Saturday 4:30 PM, Sunday 8:30 and 11:00 AM; Reconciliation Saturday 3:00-4:00 PM in the Chapel. It names no other church.

## Worship sites

One: 1439 Springdale Road (church record `st-thomas-more-cherry-hill`). The weekday Mass is in the church's chapel, the same building.

## Website and bulletin provider

`other` with a `page-pdfs` recipe on the church-bulletin.org listing. The parish's own page assembles its links in JavaScript, so the listing is the stable page. The issues are image-only, so the pipeline has to read them as images. `fetch:check` (2026-10-29) picked `2026-10-25.pdf` (`page-pdfs ...: current`, fresh, 8 pages, no text on page 1).

## Shared pastor

Rev. Michael J. Matveenko is Administrator here and Pastor of St. Mary, Cherry Hill (its 1 November 2026 masthead). The two parishes publish separate bulletins: this one is John Patrick 632 with its own masthead and Mass times; St. Mary's is LPi container 04/0346 (see `st-mary-cherry-hill`). A shared pastor is not a shared bulletin, so the rows stay separate.

## Not yet confirmed

Nothing blocking.
