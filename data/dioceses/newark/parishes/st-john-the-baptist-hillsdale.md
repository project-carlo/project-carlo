---
name: St. John the Baptist, Hillsdale
website: https://www.stjohnhillsdale.org/
bulletin_provider: other
provider_id: page-pdfs https://www.stjohnhillsdale.org/
publication: ['url:https://www.stjohnhillsdale.org/']
group: Planning Area B
evidence:
- url: https://www.stjohnhillsdale.org/_files/ugd/f67067_dab717a18fea43e981f1450a04963537.pdf
  seen: 2026-11-03
  quote: 69 VALLEY STREET, HILLSDALE NJ 07642
  note: 'Bulletin for the Solemnity of All Saints & All Souls, November 1-November 2, 2026 (4 pages, text
    layer). Page 1 masthead: SAINT JOHN THE BAPTIST ROMAN CATHOLIC CHURCH; MASS SCHEDULE Saturday Vigil
    5:00 PM; Sunday 8:00 AM, 10:00 AM, 12:00 PM; Weekdays & Saturday 8:00 AM; Holy Days 8:00 AM, 12:00
    PM, 7:00 PM; Pastor Rev. Msgr. Peter Smutelovic. No other church named.'
- url: https://www.stjohnhillsdale.org/
  seen: 2026-11-03
  quote: WEEKEND BULLETIN
  note: Parish Wix homepage; its WEEKEND BULLETIN button links the _files/ugd/f67067_dab717a1... PDF above.
    The homepage also links other ugd PDFs (a message from Fr. Peter, a letter). No separate bulletin
    page or archive in the site menu.
bulletin_status: available
---

## Publisher

St. John the Baptist, 69 Valley Street, Hillsdale, self-publishes a weekly bulletin on its Wix site. I read pages 1–2 of the November 1–2, 2026 issue (All Saints and All Souls): the page 1 masthead names Saint John the Baptist Roman Catholic Church alone, with its own Mass schedule and staff (Rev. Msgr. Peter Smutelovic, Pastor), and page 2 that week's Mass intentions. No publisher footer; 4 pages with no ads.

## Worship sites

- St. John the Baptist Church, 69 Valley Street (`st-john-the-baptist-hillsdale`): every Mass in the schedule (Saturday 5:00pm vigil; Sunday 8:00, 10:00am, 12:00pm; weekdays and Saturday 8:00am).

The directory (63) and GCatholic (18424) list only this church; St. John's Academy is the school. The issue names no chapel or mission.

## Website and bulletin provider

The directory's https://www.stjohnhillsdale.org/ (Wix) answers `probe get`; the homepage's WEEKEND BULLETIN button links the current issue as a Wix `_files/ugd/` PDF whose name changes each upload. GCatholic gives an older stjohnhillsdale.com, not checked. Provider `other`, read from the homepage.

Fetch check (2026-11-03, headed browser): `page-pdfs on https://www.stjohnhillsdale.org/: first-listed`, transport ok, PDF, picked `_files/ugd/f67067_dab717a18fea43e981f1450a04963537.pdf`, the November 1–2 issue read above (the WEEKEND BULLETIN button). Recipe pinned in `provider_id`. Freshness `unknown`: neither the file name nor the masthead gives the check a date it can parse. The pick depends on the bulletin being the first PDF the homepage lists; if a later check picks a letter or flyer instead, that needs a `fetch_gap`.

## Not yet confirmed

Nothing open.
