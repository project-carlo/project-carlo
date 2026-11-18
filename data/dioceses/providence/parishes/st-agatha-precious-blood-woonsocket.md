---
name: St. Agatha and Precious Blood Parishes, Woonsocket
website: https://sapbwoonsocket.weebly.com/bulletins--announcements.html
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://sapbwoonsocket.weebly.com/bulletins--announcements.html#canva']
group: ''
evidence:
- url: https://www.canva.com/design/DAHaQvZafUs/YxUN94j1cw6-5B5VyrNbkQ/view
  seen: 2026-11-15
  quote: St Agatha Precious Blood Parishes
  note: Canva design titled 'Bulletin 11/15/26', 2 pages, read with visit.py --text. Masthead 'St Agatha
    Precious Blood Parishes', 'NOVEMBER 15, 2026 THIRTY-THIRD SUNDAY IN ORDINARY TIME'; Mass Times 'Saturday
    4:00 pm Precious Blood / 5:30 pm St. Agatha; Sunday 9:00 am Precious Blood / 10:30 am St. Agatha;
    Daily Masses M, T, Th, F 12:00 pm St. Agatha's Chapel'; Precious Blood Parish, 94 Carrington Avenue;
    St. Agatha's Parish, 34 Joffre Avenue; Rev. Michael A. Kelley, Pastor.
- url: https://sapbwoonsocket.weebly.com/bulletins--announcements.html
  seen: 2026-11-15
  note: Weebly page 'BULLETINS & ANNOUNCEMENTS' lists posts 'Helping Hands Thanksgiving', 'Bulletin 11/15/26',
    'Bulletin 11/8/26', 'Bulletin 11/1/26', each a Canva embed; no PDF links.
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-14
  note: 'Finder 12253 Precious Blood and 12255 St. Agatha both give website sapbwoonsocket.weebly.com,
    Pastor Rev. Michael A. Kelley, and ''06.2018: Precious Blood, Woonsocket, has merged their office
    with St. Agatha''s in Woonsocket''.'
research:
- method: probe get of the Weebly bulletin page; visit.py --text on the 15 November 2026 Canva embed
  url: https://sapbwoonsocket.weebly.com/bulletins--announcements.html
  checked: '2026-11-15'
  outcome: unsupported-format
  next_action: Check whether the parish also posts a PDF (e.g. on Facebook @stagathapreciousbloodparishes)
    or whether a Canva collector exists
  retry_when: A collector for Canva design viewers lands, or the page starts linking PDFs
bulletin_status: unsupported-format
fetch_gap:
  kind: canva-design-viewer
  seen: 2026-11-15
  note: The weekly bulletin is a Canva design embedded on the Weebly 'Bulletins & Announcements' page
    (iframe canva.com/design/<id>/<key>/view?embed), one post per week ('Bulletin 11/15/26'); no PDF is
    linked, so no collector reads it.
  url: https://www.canva.com/design/DAHaQvZafUs/YxUN94j1cw6-5B5VyrNbkQ/view
---

## Publisher

The two Woonsocket parishes of Rev. Michael A. Kelley, St. Agatha and Precious Blood, publish one weekly bulletin, posted on their joint Weebly site (https://sapbwoonsocket.weebly.com/bulletins--announcements.html) as an embedded Canva design. The 15 November 2026 design ("Bulletin 11/15/26", https://www.canva.com/design/DAHaQvZafUs/YxUN94j1cw6-5B5VyrNbkQ/view, read 2026-11-15 in a browser) has the masthead "St Agatha Precious Blood Parishes", lists both parish addresses and Fr. Kelley as pastor of both. The two canonical parishes stay separate (the finder lists both, offices merged in June 2018), but their bulletin is one, so they are one row.

## Worship sites

The 15 November 2026 Mass Times: "Saturday 4:00 pm Precious Blood, 5:30 pm St. Agatha; Sunday 9:00 am Precious Blood, 10:30 am St. Agatha; Daily Masses M, T, Th, F 12:00 pm St. Agatha's Chapel". So two churches: Precious Blood (94 Carrington Ave.) and St. Agatha (34 Joffre Ave.); St. Agatha's Chapel is in the St. Agatha building ("enter Chapel from lower parking lot", finder) and isn't a separate site.

## Website and bulletin provider

`unsupported`, fetch_gap `canva-design-viewer`: each week's issue is a Canva design in an iframe, with no PDF link, so no collector reads it. The website is the bulletin page. The publication id is the bulletin page, as no publisher id exists.

`fetch:check` on 2026-11-15 refused the row as `unsupported` (no collector), as expected.

## Not yet confirmed

Whether a PDF copy is posted anywhere (the parish Facebook page @stagathapreciousbloodparishes was not read).
