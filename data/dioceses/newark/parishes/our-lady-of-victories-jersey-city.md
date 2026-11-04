---
name: Our Lady of Victories, Jersey City
website: https://www.olvjc.org/treasure
bulletin_provider: unsupported
provider_id: page-pdfs https://www.olvjc.org/treasure
publication: ['url:https://www.olvjc.org/treasure']
group: Planning Area F
evidence:
- url: https://www.olvjc.org/_files/ugd/c03d65_8e910910e703498f8bbca8a6aa91a3dc.pdf
  seen: 2026-11-03
  quote: 2217 J.F. Kennedy Boulevard, Jersey City, New Jersey 07304
  note: 'Bulletin linked as ''Nov1 - All Saints Day'', 4 pages, text. Page 1 masthead ''Our Lady of Victories
    Church … Established 1917'', Pastor Rev. Ralph D. Siendo; ''THE LORD''S DAY: Saturday (Vigil) 5:00
    PM Sunday 8:00 AM, 10:00 AM, 12:00 Noon Weekdays 8:30 AM AND 6:30 PM Saturday 8:30 AM''. No other
    parish or church named; no publisher footer (self-produced).'
- url: https://www.olvjc.org/treasure
  seen: 2026-11-03
  note: 'Wix page (read with visit.py) that the homepage ''BULLETIN'' button opens. ''Download Bulletin
    >> All Saints Day'' and a ''Bulletins'' list: ''Nov1 - All Saints Day'', then ''Sep13 - 24th Sunday
    of OT'' … ''Oct25 - 30th Sunday of OT'' (oldest first), all _files/ugd PDFs with no date in the name.
    The same page also links five yearly financial reports (07/1/2021 - 06/30/2026) and an unlabelled
    2-page PDF (c03d65_b8d58d2c…pdf) above them.'
- url: https://www.olvjc.org/
  seen: 2026-11-03
  quote: 'Sunday: 8:00 AM | 10:00 AM | 12:00 NOON'
  note: 'probe url: Wix site, verdict ok, no publisher ids.'
bulletin_status: available
fetch_gap:
  kind: first-pdf-not-bulletin
  seen: 2026-11-03
  note: page-pdfs on https://www.olvjc.org/treasure picks the first-listed PDF, the parish coat of arms
    (_files/ugd/c03d65_b8d58d2c….pdf), not the bulletin. Issues are undated Wix _files/ugd PDFs linked
    by text such as 'Nov1 - All Saints Day', beside financial reports, so no filename glob selects them.
  url: https://www.olvjc.org/_files/ugd/c03d65_8e910910e703498f8bbca8a6aa91a3dc.pdf
---

## Publisher

Our Lady of Victories, Jersey City produces its own weekly bulletin and posts it as PDFs on its Wix site. I read the issue linked as 'Nov1 - All Saints Day' (4 pages, text). The page 1 masthead says 'Our Lady of Victories Church, 2217 J.F. Kennedy Boulevard, Jersey City, New Jersey 07304', with Rev. Ralph D. Siendo as pastor and one Mass schedule. It names no other parish and carries no printer's footer.

## Worship sites

- Our Lady of Victories, 2217 Kennedy Boulevard (`our-lady-of-victories-jersey-city`): Saturday Vigil 5:00 PM; Sunday 8:00, 10:00 AM and 12:00 Noon; weekdays 8:30 AM and 6:30 PM; Saturday 8:30 AM (bulletin page 1). The directory (91) and GCatholic (18443) list only this church.

## Website and bulletin provider

The homepage's 'BULLETIN' button opens https://www.olvjc.org/treasure, which lists the weekly issues ('Nov1 - All Saints Day', then September 13 to October 25, oldest first) beside financial reports. The files are Wix `_files/ugd/` names with no date, so no filename filter can tell issues from the reports, and freshness reads `unknown`. GCatholic gives the old domain www.olvjc.com; the masthead says olvjc.org. The provider is `unsupported`, with a `fetch_gap`, for the reason below. `provider_id` keeps `page-pdfs https://www.olvjc.org/treasure`, the page a collector would read.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://www.olvjc.org/treasure: first-listed` and picked `_files/ugd/c03d65_b8d58d2c37194f1caf61ed215ba2732b.pdf`. That file is the parish's coat of arms (2 pages, image; rendered with render.py), linked from an unlabelled image at the top of the page, not the bulletin. The homepage lists the same file first too. Wix file names carry no date or label, and the issue links are labelled 'Nov1 - All Saints Day' rather than 'bulletin', so neither a filename glob nor the `titled` fallback can choose the issue. Until a collector can choose by link text, the row is `unsupported` with `fetch_gap` `first-pdf-not-bulletin`.

## Not yet confirmed

Whether the parish keeps posting each issue to /treasure; the September and October issues listed there suggest it does, every week.
