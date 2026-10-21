---
name: Saint Michael Parish, Saint Michael
website: https://saintmichaelchurch.weebly.com/bulletin.html
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://saintmichaelchurch.weebly.com/bulletin.html']
group: ''
evidence:
- url: https://saintmichaelchurch.weebly.com/uploads/7/1/2/8/7128011/10-18-2026_webbulletin.docx
  seen: '2026-10-21'
  note: 'Downloaded with curl (HTTP 200, 3.3 MB, Microsoft Word 2007+) and read from word/document.xml; recheck cannot read a .docx, so this is a note, not a quote. Masthead of the 18 Oct 2026 issue: "ST. MICHAEL ROMAN CATHOLIC CHURCH, 751 Locust Street, PO Box 103, St. Michael, Pennsylvania 15951", Rev. Fr. Jerzy Auguscik, OFM Conv., Pastor, 814-495-9640; "MASSES: Saturday 4:00 pm; Sunday Morning 8:00 am, 10:30 am; Daily Mass: Tue, Wed, Thur, Fri 9:00 am; No Mass on Monday"; Confessions Saturday 3:15 pm. It names St. Michael alone.'
- url: https://saintmichaelchurch.weebly.com/bulletin.html
  seen: '2026-10-21'
  quote: '10-18-2026'
  note: 'Weebly Bulletin page. Every current issue is a link to /uploads/7/1/2/8/7128011/MM-DD-2026_webbulletin.docx (10-18-2026, 10-11-2026, 10-04-2026 ... back to 03-2026; Easter and Palm Sunday are .doc). Older entries (2022, 2024) are plain dates with no link. No PDF is offered anywhere on the page.'
- url: https://discovermass.com/church/st-michael-saint-michael-pa/
  seen: '2026-10-21'
  quote: Shucks! There are no bulletins available.
  note: Discover Mass page for St. Michael, Saint Michael PA; empty Bulletins tab, so no PDF copy there.
- url: https://www.dioceseaj.org/parishes/
  seen: '2026-10-21'
  note: 'Directory: Saint Michael Parish, Saint Michael, 751 Locust Street 15951, homepage saintmichaelchurch.weebly.com; Masses Sat 4:00 PM, Sun 8:00 AM and 10:30 AM, Mon-Fri 9:00 AM (the bulletin says no Mass on Monday); Confession Saturday 3:30 PM.'
revisit: Switch to a real provider if the pipeline reads .docx or the parish posts PDFs; the bulletin is a weekly .docx at saintmichaelchurch.weebly.com/bulletin.html
revisit_after: 2027-01-15
---

## Publisher

Saint Michael Parish (pastor Fr. Jerzy Auguscik, OFM Conv., 814-495-9640) publishes its own weekly bulletin on its Weebly site, `saintmichaelchurch.weebly.com/bulletin.html`, **only as Word files** (`.docx`, `.doc` for Easter and Palm Sunday). The 18 Oct 2026 issue (read 2026-10-21) names St. Michael alone and gives the Mass times quoted in the evidence. It is not shared with another parish.

## Worship sites

One: St. Michael, 751 Locust Street (see `churches/saint-michael-saint-michael.md`). Nothing else is named in the bulletin masthead or schedule.

## Website and bulletin provider

`no_bulletin` (Settled policy 4). The fetch pipeline resolves the page to the newest link, `10-18-2026_webbulletin.docx`, and then fails: `fetch:check` on 2026-10-21 reported `resolve_failed ... Page.goto: Download is starting`, and the code has no .docx reader (grep for "docx" in the Python source finds only a test file name). Discover Mass has an empty Bulletins tab for the church, and no ParishesOnline or other PDF copy was found. The site is a live channel with a fixed URL pattern (`/uploads/7/1/2/8/7128011/<MM-DD-YYYY>_webbulletin.docx`), so the row is worth switching to a real provider if the pipeline gains .docx reading (or the parish starts posting PDFs).

## Not yet confirmed

The directory lists Monday 9:00 AM Mass; the 18 Oct bulletin says "No Mass on Monday" (the later, parish-own source, followed).
