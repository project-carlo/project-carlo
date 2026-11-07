---
name: St. Ephrem (Dyker Heights)
website: https://stephremparish-brooklyn.org/
bulletin_provider: other
provider_id: page-pdfs https://stephremparish-brooklyn.org/bulletins
publication: []
group: Deanery B9 (Brooklyn West)
evidence:
- url: https://stephremparish-brooklyn.org/system/resources/W1siZiIsIjIwMjYvMTEvMDUvMnV5MHgyeGt5Zl9Ob3ZlbWJlcl84XzIwMjYucGRmIl1d/November%208%2C%202026.pdf
  seen: 2026-11-06
  note: '8 November 2026 issue, 6 pages, all images (no text layer; read with render.py). Page 1 masthead:
    CHURCH OF ST. EPHREM CATHOLIC CHURCH, November 8, 2026; Rev. Ralph Edel, Pastor; Schedule of Masses:
    Saturday Vigil 5:00 pm, Sunday 8:00 am & 11:00 am, Monday through Friday 7:00 am & 8:45 am, Saturday
    8:45 am; St. Ephrem Rectory Office, 929 Bay Ridge Parkway, Brooklyn, NY 11228. No other church or
    chapel is named.'
- url: https://stephremparish-brooklyn.org/system/resources/W1siZiIsIjIwMjYvMTEvMDUvMnV5MHgyeGt5Zl9Ob3ZlbWJlcl84XzIwMjYucGRmIl1d/November%208%2C%202026.pdf
  seen: 2026-11-06
  note: 'Page 6 (image) header ''Church of St. Ephrem, Brooklyn, New York'', with the parish''s collection
    and Mass attendance; no LPi, John Patrick or Church Bulletin Inc. footer: the parish makes its own
    bulletin.'
- url: https://stephremparish-brooklyn.org/bulletins
  seen: 2026-11-06
  note: 'Tilma bulletins page, server-rendered, newest first: November 08, 2026 (November 8, 2026.pdf
    under /system/resources/), November 01, October 25, October 18, October 11, October 04, weekly back
    to August.'
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://stephremparish-brooklyn.org/bulletins
  url: https://stephremparish-brooklyn.org/bulletins
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
---

## Publisher

St. Ephrem, Dyker Heights publishes its own weekly bulletin, laid out by the parish (no LPi, John Patrick or Church Bulletin Inc. footer) and posted as image-only PDFs on its Tilma site. The 8 November 2026 issue (read 2026-11-06 with render.py, 6 pages) has the masthead "CHURCH OF ST. EPHREM CATHOLIC CHURCH" on page 1, with Rev. Ralph Edel, Pastor, and the rectory at 929 Bay Ridge Parkway, Brooklyn, NY 11228.

## Worship sites

One. The page 1 Schedule of Masses gives Saturday Vigil 5:00 pm, Sunday 8:00 am and 11:00 am, Monday-Friday 7:00 am and 8:45 am, Saturday 8:45 am, with no other church or chapel. The directory, the deanery list (St. Ephrem Parish), GCatholic 16702 and Mass finder 331 all give the one church at 929 Bay Ridge Parkway.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stephremparish-brooklyn.org/bulletins` (the Tilma bulletins page, newest first, one card per Sunday). No publication id: the bulletin is self-made and has no online container. Every page is an image, so the pipeline has to read it as images.

## Not yet confirmed

Nothing open.
