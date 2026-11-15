---
name: Holy Ghost
website: https://www.holyghostcc.org/bulletin-media/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://www.holyghostcc.org/bulletin-media/bulletin/
publication: ['url:https://www.holyghostcc.org/bulletin-media/bulletin/']
group: ''
evidence:
- url: https://www.holyghostcc.org/wp-content/uploads/2026/11/bulletin-2026_11_15.pages.pdf
  seen: 2026-11-15
  quote: Church of the Holy Ghost
  note: '15 November 2026 issue, 4 pages (saved with tools/fetch_pdf.py; the host drops probe connections).
    Page 1: ''Church of the Holy Ghost / November 15, 2026 - 33rd Sunday in Ordinary Time / 316 Judson
    Street / Tiverton, RI''. Page 4: ''Pastor Rev. Fr. Jay A. Finelli''; ''Mailing address: 311 Hooper
    St.''; ''Church address: 316 Judson St.''; ''Parish Center: ... 303 Hooper St. (Use Judson St. entrance)'';
    ''Sunday Mass Schedule 4:30 pm - Mass of Anticipation 7:30 am & 9:00 am''; ''Weekday Mass Schedule
    Monday - Friday: 7:00 am Saturday: 9:00 am''.'
- url: https://www.holyghostcc.org/bulletin-media/bulletin/
  seen: 2026-11-15
  note: 'WordPress Bulletin page (unreachable to probe url; read with parish-site-access visit.py) lists
    six issues oldest first: bulletin-2026_10_11.pages.pdf ... bulletin-2026_11_15.pages.pdf under wp-content/uploads/2026/11/.
    A 6 November 2026 post says ''Our weekly bulletins have returned to the website.'''
bulletin_status: available
---

## Publisher

Holy Ghost, Tiverton publishes its own weekly bulletin as PDFs on its WordPress site. The 15 November 2026 issue (https://www.holyghostcc.org/wp-content/uploads/2026/11/bulletin-2026_11_15.pages.pdf), page 1, is headed "Church of the Holy Ghost / November 15, 2026 - 33rd Sunday in Ordinary Time / 316 Judson Street / Tiverton, RI". The back page gives "Pastor Rev. Fr. Jay A. Finelli", "Church address: 316 Judson St." and the Mass schedule: Saturday 4:30 pm (Mass of Anticipation), Sunday 7:30 am & 9:00 am, Monday-Friday 7:00 am, Saturday 9:00 am.

## Worship sites

One church: Holy Ghost, 316 Judson St., Tiverton. The finder (12221) and GCatholic (22438) list only this church for the parish. The Adoration chapel in the parish center (303 Hooper St.) is for adoration, with no Mass listed there.

## Website and bulletin provider

`other`, `page-pdfs` on the Bulletin page https://www.holyghostcc.org/bulletin-media/bulletin/, which links each issue as wp-content/uploads/YYYY/MM/bulletin-YYYY_MM_DD.pages.pdf. The site drops `probe url`/`probe pdf` connections; it loads in a browser and through the pipeline's own downloader.

`fetch:check` on 2026-11-15 printed `page-pdfs on https://www.holyghostcc.org/bulletin-media/bulletin/: current` and downloaded bulletin-2026_11_15.pages.pdf, the issue read above, although the page lists issues oldest first; the recipe is pinned in provider_id.

## Not yet confirmed

Nothing open.
