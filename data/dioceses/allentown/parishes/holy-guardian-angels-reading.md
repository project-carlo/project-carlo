---
name: Holy Guardian Angels Parish
website: https://www.hgaparish.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/199
publication:
- url:https://www.church-bulletin.org/holy-guardian-angels-parish-reading-pa-19605
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/holy-guardian-angels-parish-reading-pa-19605/2026-10-18.pdf
  note: '18 October 2026 issue, 12 pages, all scanned images with no text layer (read rendered, parish-site-access
    render.py). Page 1: "HOLY GUARDIAN ANGELS PARISH EST. 1929"; MASS SCHEDULE "Saturday Vigil – 4:15
    pm | Sunday – 8:00, 9:45 & 11:30 am"; Daily Mon., Tues., Thur., Fri. 8:00 am, Wed. 8:00 am & 12:10
    pm; footer "HGA Rectory | 3121 Kutztown Road Reading, PA 19605". One church named.'
  seen: 2026-10-18
- url: https://www.church-bulletin.org/holy-guardian-angels-parish-reading-pa-19605
  quote: Holy Guardian Angels Parish Reading, PA 19605
  note: 'John Patrick Publishing listing (church-bulletin.org/?id=199 redirects here): one PDF per Sunday
    at /bulletin/holy-guardian-angels-parish-reading-pa-19605/YYYY-MM-DD.pdf, newest 18 October 2026.'
  seen: 2026-10-18
- url: https://www.hgaparish.com/bulletins
  note: The parish site's Bulletins page links https://www.jppc.net/onlinebulletins/199template.pdf, which
    301-redirects to https://church-bulletin.org/?id=199 (curl -I, 2026-10-18).
  seen: 2026-10-18
---

## Publisher

Holy Guardian Angels Parish (Hyde Park, Reading) publishes its own weekly bulletin through
John Patrick Publishing (church-bulletin.org). I read the 18 October 2026 issue: page 1 is
the parish's masthead ("Holy Guardian Angels Parish, Est. 1929") with one Mass schedule
(Saturday Vigil 4:15 pm; Sunday 8:00, 9:45 and 11:30 am) and the rectory at 3121 Kutztown
Road. No other worship site is named. The diocese lists no grouping for this parish.

## Worship sites

- Holy Guardian Angels, 3121 Kutztown Road, Reading (`holy-guardian-angels-reading`).

The bulletin's adoration chapel is on the same campus and is not a separate worship site.
No roster lists another building for this parish.

## Website and bulletin provider

hgaparish.com is the parish's own site; its Bulletins page links the John Patrick template
URL for id 199, which redirects to the church-bulletin.org listing recorded in
`publication`. Provider `other` with the recipe `page-pdfs https://church-bulletin.org/199`
(the form verified for this publisher in Scranton). fetch:check on 2026-10-18 (temporary
CSV, /tmp/alle-scripts/fetch_check_rows.py) picked the 18 October 2026 PDF: "page-pdfs on
https://church-bulletin.org/199: current". The whole bulletin is scanned images (no text
layer in the 18 October issue), so the pipeline has to read it as images.

## Not yet confirmed

Nothing.
