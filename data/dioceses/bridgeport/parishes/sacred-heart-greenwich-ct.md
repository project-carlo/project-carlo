---
name: Sacred Heart
website: https://sacredheartgreenwich.org/bulletin/
bulletin_provider: unsupported
provider_id: page-pdfs https://sacredheartgreenwich.org/bulletin/
publication: ['url:https://sacredheartgreenwich.org/bulletin/']
group: ''
evidence:
- url: https://sacredheartgreenwich.org/wp-content/uploads/2026/11/bulletin-11-8-26-32nd-sunday-ordinary-time.pdf
  seen: 2026-11-12
  quote: 95A HENRY ST., Greenwich, CT 06830
  note: 'Page 1 masthead of the 8 November 2026 issue: ''SACRED HEART CHURCH'' / ''32ND SUNDAY IN ORDINARY
    TIME – NOVEMBER 8, 2026''; pastor Father Mark D''Silva; 6 pages, text-readable, no printer named.'
- url: https://sacredheartgreenwich.org/wp-content/uploads/2026/11/bulletin-11-8-26-32nd-sunday-ordinary-time.pdf
  seen: 2026-11-12
  note: 'Page 1: ''Weekend Masses Saturday: 4:00 p.m. Sunday: 7:30 a.m., 9:30 a.m. & 11:30 a.m. Weekday
    Masses (Chapel) 7:00 a.m. Monday to Friday''; Holy Day vigil 5:30 p.m., Holy Day 7:00 a.m., 12:15
    p.m. Page 2 Mass intentions for those times only; no other place named.'
- url: https://sacredheartgreenwich.org/bulletin/
  seen: 2026-11-12
  note: 'probe get: the WordPress Bulletin page links wp-content/uploads PDFs, newest first (''bulletin-11-8-26-32nd-sunday-ordinary-time.pdf'',
    then 11-1-26, 10-25-26 ...), back to 2021.'
bulletin_status: unsupported-format
fetch_gap:
  kind: litespeed-guest-reload
  seen: 2026-11-12
  url: https://sacredheartgreenwich.org/bulletin/
  note: 'The WordPress Bulletin page lists the issues as plain wp-content/uploads PDF links, newest first
    (probe get reads them), but the site''s LiteSpeed Cache guest mode POSTs to /wp-content/plugins/litespeed-cache/guest.vary.php
    on first visit and calls window.location.reload(true). fetch:check (headed Chrome and plain, page-pdfs
    on the Bulletin page) failed twice with ''Page.query_selector_all: Protocol error (DOM.describeNode):
    Cannot find context with specified id'' (once ''Unable to adopt element handle from a different document''):
    the reload destroys the page while the collector reads it.'
---

## Publisher

Sacred Heart, Greenwich posts its own weekly bulletin as PDFs on its WordPress Bulletin page (`https://sacredheartgreenwich.org/bulletin/`); no printer is named. The 8 November 2026 issue (`https://sacredheartgreenwich.org/wp-content/uploads/2026/11/bulletin-11-8-26-32nd-sunday-ordinary-time.pdf`, newest listed on 2026-11-12, read with probe pdf) is headed "SACRED HEART CHURCH / 95A HENRY ST., Greenwich, CT 06830 / 32ND SUNDAY IN ORDINARY TIME – NOVEMBER 8, 2026".

## Worship sites

One church, `sacred-heart-greenwich-ct`. Page 1: Saturday 4:00 p.m.; Sunday 7:30, 9:30 and 11:30 a.m.; "Weekday Masses (Chapel) 7:00 a.m. Monday to Friday". The weekday chapel is not given a separate address (the directory's notes say "In chapel"); it is taken as the parish's own chapel at the church and kept on this church's row (rule settled in batch `stamford-central`). No other place is named. The diocese's directory (directory:1382) and GCatholic (21949) list this one church.

## Website and bulletin provider

Provider `unsupported`, `fetch_gap` `litespeed-guest-reload`. The Bulletin page (`https://sacredheartgreenwich.org/bulletin/`) links each issue as a plain `wp-content/uploads/<yyyy>/<mm>/bulletin-<m>-<d>-<yy>-....pdf`, newest first, which `page-pdfs` would read; but the site's LiteSpeed Cache guest mode reloads the page on a first visit (`guest.vary.php` then `window.location.reload(!0)` in the page source), and `fetch:check` on 2026-11-12 (pinned `page-pdfs https://sacredheartgreenwich.org/bulletin/`, headed Chrome and again without the Chrome channel) failed both times with `Cannot find context with specified id` / `Unable to adopt element handle from a different document`. When the collector waits out a reload, rerun `fetch:check`, set provider `other` with the printed recipe and clear the gap.

## Not yet confirmed

Nothing about the parish is open; the row waits for a collector that survives the LiteSpeed guest-mode reload.
