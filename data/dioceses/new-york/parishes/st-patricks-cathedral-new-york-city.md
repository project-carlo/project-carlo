---
name: St. Patrick's Cathedral
website: https://saintpatrickscathedral.org/
bulletin_provider: other
provider_id: page-pdfs https://saintpatrickscathedral.org/newsRSS filename=*_sun.pdf
publication: ['url:https://saintpatrickscathedral.org/newsRSS', 'ecatholic:6783', 'po-org:st-patrick-cathedral-10022',
  'lpi:0018000000QxAHfAAN']
group: ''
evidence:
- url: https://saintpatrickscathedral.org/documents/2026/11/20261108_XXXII_Sun.pdf
  seen: 2026-11-08
  quote: ST. PATRICK’S CATHEDRAL AMERICA’S PARISH CHURCH NEW YORK CITY 8 NOVEMBER 2026 Celebration of
    the Eucharist THIRTY-SECOND SUNDAY IN ORDINARY TIME
  note: Page 1 of the 14-page Sunday worship aid; page 2 gives the preludes by Mass ('Sat 5:30', 'Sun
    9', 'Sun 10:15', 'Sun 12 & 1', 'Sun 5:30'); page 14 footer 'Fifth Avenue between 50th & 51st Street'.
    It is an order of worship, not a bulletin with announcements or a full Mass schedule.
- url: https://saintpatrickscathedral.org/newsRSS
  seen: 2026-11-08
  quote: Thirty-second Sunday in Ordinary Time
  note: The cathedral's news feed has one item per day linking that day's worship aid PDF (20261108_XXXII_Sun.pdf,
    20261107_OT_XXXI_Sat.pdf, ... back to 20261022); Sunday files end in _Sun.pdf.
- url: https://saintpatrickscathedral.org/masses
  seen: 2026-11-08
  quote: 'Sunday: 7:00 AM, 8:00, 9:00, 10:15 AM - (Solemn), 12:00 Noon, 1:00, 4:00 PM - (Spanish), 5:30
    PM'
  note: Official Mass schedule; also Monday-Friday 7:00, 7:30, 8:00 AM, noon, 1:00 and 5:30 PM, Saturday
    8:00 AM, noon and 5:30 PM vigil.
- url: https://saintpatrickscathedral.org/bulletins
  seen: 2026-11-08
  note: The eCatholic (6783) bulletin page still lists no issues; files.ecatholic.com/6783/bulletins/<date>.pdf
    answers 403 for 18 October to 8 November 2026.
- url: https://discovermass.com/church/st-patricks-cathedral-new-york-ny/
  seen: 2026-11-08
  quote: no bulletins available
  note: Discover Mass listing has no bulletins; ParishesOnline orgs st-patrick-cathedral-10022 and cathedral-of-st-patrick-10022
    have no publications (probe po); Flocknote stpatrickscathedral.flocknote.com shows only a loading
    page.
revisit: Check that the Sunday worship aid still appears in /newsRSS as documents/<yyyy>/<m>/<yyyymmdd>_<week>_Sun.pdf
  (a feast-day Sunday may be named differently and be skipped), and whether a weekly bulletin appears
  on /bulletins.
revisit_after: 2026-12-08
promoted: 2026-11-09
research:
- method: 'check_fetch on a hypothetical row: page-pdfs https://saintpatrickscathedral.org/newsRSS filename=*_sun.pdf
    (dated-post on /cathedral-news found no PDF)'
  url: https://saintpatrickscathedral.org/documents/2026/11/20261108_XXXII_Sun.pdf
  checked: '2026-11-08'
  outcome: found
bulletin_status: available
---

## Publisher

St. Patrick's Cathedral publishes no weekly bulletin that can be found: its eCatholic bulletin page (6783) lists no issues, Discover Mass has none, both ParishesOnline organizations for it have no publications, and its Flocknote page shows nothing readable (all November 8, 2026). What it does publish every day is a worship aid, linked from its news feed (https://saintpatrickscathedral.org/newsRSS) as `documents/<yyyy>/<m>/<yyyymmdd>_..._<Day>.pdf`. The Sunday one for 8 November 2026 (`20261108_XXXII_Sun.pdf`, 14 pages) is headed "St. Patrick's Cathedral, America's Parish Church, New York City, 8 November 2026, Celebration of the Eucharist, Thirty-Second Sunday in Ordinary Time". This row uses the Sunday worship aid as the cathedral's weekly publication.

## Worship sites

One: St. Patrick's Cathedral, Fifth Avenue between 50th and 51st Streets (`churches/st-patricks-cathedral-new-york-city.md`). The official Mass page (November 8) gives Sunday 7:00, 8:00, 9:00, 10:15 AM (solemn), noon, 1:00, 4:00 PM (Spanish) and 5:30 PM; Saturday 8:00 AM, noon and 5:30 PM vigil; Monday-Friday 7:00, 7:30, 8:00 AM, noon, 1:00 and 5:30 PM.

## Website and bulletin provider

`other` with the pinned recipe `page-pdfs https://saintpatrickscathedral.org/newsRSS filename=*_sun.pdf`: the feed lists every day's worship aid newest first, and the glob keeps the Sunday ones. On November 8 it picked `20261108_XXXII_Sun.pdf` ("current"). A Sunday whose file is named for a feast rather than `_Sun` would be skipped and the previous Sunday's picked.

The worship aid is not a full schedule: it names only the Masses with music ("Sat 5:30", "Sun 9", "Sun 10:15", "Sun 12 & 1", "Sun 5:30" on page 2), not the 7:00 and 8:00 AM, the 4:00 PM Spanish or the weekday Masses. Whether a worship aid should stand in for a bulletin here is flagged for the owner.

## Not yet confirmed

Whether the Spanish 4:00 PM Mass has its own worship aid, and whether the cathedral prints a bulletin it does not post.
