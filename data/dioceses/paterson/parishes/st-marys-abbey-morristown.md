---
name: St. Mary's Abbey
website: https://www.saintmarysabbey.org/
bulletin_provider: other
provider_id: page-pdfs https://www.saintmarysabbey.org/monthly-bulletin
publication: ['ecatholic:15209']
group: ''
evidence:
- url: https://files.ecatholic.com/15209/documents/2026/10/Novmeber%202026.pdf
  seen: 2026-11-04
  quote: Sunday — Matins 7:30 AM · Mass 11:00 AM · Vespers 5:00 PM
  note: 'November 2026 ''MONTHLY NEWSLETTER'' of St. Mary''s Abbey (9 pages). Page 9 ''Prayer schedule,
    necrology, and Mass intentions'': Sunday Mass 11:00 AM; Mon–Fri Mass with Vespers 5:00 PM; Saturday
    Mass 8:00 AM; ''MASS INTENTIONS — NOVEMBER 2026''. Pages 3-4 refer to the ''Abbey Church''.'
- url: https://www.saintmarysabbey.org/monthly-bulletin
  seen: 2026-11-04
  quote: Links to Recent Issues
  note: 'Monthly Bulletin page (probe url reads it, HTTP 200): newest first November 2026, October 2026,
    July 2025, then 2020-2021 and 2016 issues, all files.ecatholic.com/15209/documents/<y>/<m>/ PDFs labelled
    by month.'
- url: https://www.saintmarysabbey.org/
  seen: 2026-11-04
  quote: We are a community of Benedictine monks
  note: 'Home page (read with parish-site-access visit.py): ''Worship with Us'' / ''Liturgy Schedule'':
    Sunday 11:00 AM Mass; Mon-Fri 5:00 PM Mass with Vespers; Saturday 8:00 AM Mass; address ''230 Mendham
    Road, Morristown NJ 07960-5089''. probe url found ecatholic:15209.'
revisit: Check /monthly-bulletin lists a December 2026 issue; the newsletter skipped months before October
  2026.
revisit_after: 2026-12-15
bulletin_status: available
---

## Publisher

St. Mary's Abbey, Morristown (Benedictine monks; the monastery beside Delbarton School) publishes a monthly newsletter its site calls the "Monthly Bulletin", on its eCatholic site (id 15209) as PDFs in the documents folder. The November 2026 issue (`https://files.ecatholic.com/15209/documents/2026/10/Novmeber%202026.pdf`, read 2026-11-04) is headed "NOVEMBER 2026 MONTHLY NEWSLETTER", and page 9 gives the prayer schedule and "MASS INTENTIONS — NOVEMBER 2026". It is a religious house, not a parish, but it is a worship site with public Mass and a schedule-bearing bulletin of its own, so it is one row (README, *The model*). Inferred: the Mass is public from the home page's "Worship with Us" heading over the Liturgy Schedule and the welcome "we invite you to visit us"; no page says in so many words that the public may attend.

## Worship sites

- `st-marys-abbey-morristown`: the abbey church at 230 Mendham Road. Page 9 of the November 2026 issue and the home page give Sunday Mass 11:00 AM, Monday-Friday Mass with Vespers 5:00 PM, Saturday Mass 8:00 AM; neither names another place.

GCatholic lists it as 39120 ("St. Mary", Monastery). The diocese's finder does not list it (it lists parishes only).

## Website and bulletin provider

`saintmarysabbey.org` (GCatholic's link) is an eCatholic site that `probe url` reads without a block. The issues are monthly, newest first on /monthly-bulletin, with irregular gaps (July 2025, then October and November 2026). `ecatholic:15209` is recorded as the publication id, as for other documents-folder bulletins here; it has no weekly bulletins/ files. Provider `other` with the recipe `page-pdfs https://www.saintmarysabbey.org/monthly-bulletin`, the recipe `fetch:check` prints. On 2026-11-04 it picked the November 2026 issue (`Novmeber%202026.pdf`, "page-pdfs on https://www.saintmarysabbey.org/monthly-bulletin: first-listed"), the current one; it reports the issue date and freshness as unknown ("No unambiguous issue date in inspected masthead or selected URL filename"), because a monthly label and file name carry no day, and identity unverified because no expected identity is supplied.

## Not yet confirmed

Whether the newsletter keeps coming monthly: before October 2026 the listing jumps from July 2025 back to 2021. If December 2026 is not posted by mid-December, fetch will go stale; re-check the listing (revisit).
