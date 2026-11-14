---
name: Our Lady of Victory
website: https://olvfpny.org/bulletin/
bulletin_provider: unsupported
provider_id: page-pdfs https://olvfpny.org/bulletin/
publication: ['url:https://olvfpny.org/bulletin/#our-lady-of-victory']
group: ''
evidence:
- url: https://olvfpny.org/wp-content/uploads/bulletin/Bulletin_2026-11-15.pdf
  seen: 2026-11-13
  quote: 'WEBSITE: olvfpny.org'
  note: Issue for November 15, 2026 (12 pages). Page 1 (rendered; its text layer is doubled) heads 'WELCOME
    TO OUR LADY OF VICTORY CHURCH, 2 FLORAL PARKWAY, FLORAL PARK, NY'; Rev. Thomas M. Fusco Pastor; MASS
    SCHEDULE daily Monday-Friday 8:30 am & 12 noon; Saturday 8:30 am, 4:00 pm & 5:30 pm; Sunday 7:30 am,
    9:00 am, 10:30 am, 12 noon & 5:30 pm. Downloaded through Chrome (tools/browser_get.py); probe get
    answered 403.
- url: https://olvfpny.org/bulletin/
  seen: 2026-11-13
  note: WordPress bulletin page (read with parish-site-access visit.py; probe url answers 403) lists issues
    by month as wp-content/uploads/bulletin/Bulletin_<yyyy-mm-dd>.pdf, the newest November 15, 2026.
bulletin_status: available
fetch_gap:
  kind: pdf-download-403
  seen: 2026-11-13
  note: fetch:check resolves page-pdfs on https://olvfpny.org/bulletin/ to the current issue (Bulletin_2026-11-15.pdf),
    but the PDF download answers HTTP 403 to the fetcher (and to probe get); Chrome downloads it (tools/browser_get.py).
  url: https://olvfpny.org/wp-content/uploads/bulletin/Bulletin_2026-11-15.pdf
---

## Publisher

Our Lady of Victory, Floral Park publishes its own weekly bulletin. The newest issue on 2026-11-13, `https://olvfpny.org/wp-content/uploads/bulletin/Bulletin_2026-11-15.pdf` (12 pages), has on page 1 "WELCOME TO OUR LADY OF VICTORY CHURCH, 2 FLORAL PARKWAY, FLORAL PARK, NY, WEBSITE: olvfpny.org", "THIRTY THIRD SUNDAY IN ORDINARY TIME NOVEMBER 15, 2026", Rev. Thomas M. Fusco, Pastor, and a MASS SCHEDULE: Monday-Friday 8:30 am & 12 noon; Saturday 8:30 am, 4:00 pm & 5:30 pm; Sunday 7:30 am, 9:00 am, 10:30 am, 12 noon & 5:30 pm. Page 1's text layer is printed twice over itself, so I read it rendered.

## Worship sites

One: the church at 2 Floral Parkway (`our-lady-of-victory-floral-park-church`). The schedule names no other place. The diocesan locator (directory:24), GCatholic (16843) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

olvfpny.org (WordPress) is the locator's and Mass-times page's link (GCatholic gives ourladyofvictoryfp.com). `probe url` and `probe get` answer 403; the site loads in the browser. Its `/bulletin/` page lists issues by month as `wp-content/uploads/bulletin/Bulletin_<yyyy-mm-dd>.pdf`, oldest first within each month, alongside some form PDFs.

`fetch:check` (2026-11-13) with page-pdfs on `/bulletin/` picked `Bulletin_2026-11-15.pdf`, the November 15, 2026 issue, the newest posted, but its download failed with HTTP 403 (download_failed). So the row is `unsupported` with fetch_gap `pdf-download-403`; the recipe is kept in `provider_id` for when a browser-backed download lands. Then set `bulletin_provider: other`, rerun fetch:check and clear the gap.

## Not yet confirmed

Nothing open.
