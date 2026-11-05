---
name: St. Francis de Sales
website: https://stfrancisvernon.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11490']
group: ''
evidence:
- url: https://stfrancisvernon.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site 11490 (the finder pin
    id); /bulletins lists files.ecatholic.com/11490/bulletins/<YYYYMMDD>.pdf weekly, newest 'November
    1, 2026' (20261101.pdf), then October 25, 18, 11 ...
- url: https://files.ecatholic.com/11490/bulletins/20261101.pdf
  seen: 2026-11-04
  note: '8 pages, image-only (probe pdf finds no text). Page 1 rendered with render.py: an All Souls cover,
    ''The Parish of St. Francis de Sales Remembers All Souls Day November 2, 2026'', with a box ''The
    Solemnity of All Saints November 1, 2026''; no masthead.'
- url: https://files.ecatholic.com/11490/bulletins/20261025.pdf
  seen: 2026-11-04
  quote: 614 Route 517, Vernon, NJ
  note: 'Page 1 of the 25 October 2026 issue: ''St. Francis de Sales Church'', ''Mailing Address: P .O.
    Box 785, McAfee, NJ. 07428'', ''Rev. Chris Barkhausen, Pastor'', ''Thirtieth Sunday in Ordinary Time
    October 25, 2026''. Weekend Masses: Saturday (Vigil) English 5:00 PM, Spanish 7:00 PM; Sunday 8:00
    AM, 10:00 AM, 12:00 PM; weekday Monday through Saturday 8:30 AM. No other worship site named.'
bulletin_status: available
---

## Publisher

St. Francis de Sales, Vernon (McAfee) publishes its own weekly bulletin and posts it to its eCatholic site's `bulletins/` archive (site id 11490). The newest on 4 November 2026 is the 1 November 2026 issue (`https://files.ecatholic.com/11490/bulletins/20261101.pdf`, 8 pages, image-only); its page 1 (rendered) is a seasonal All Souls cover, "The Parish of St. Francis de Sales Remembers All Souls Day November 2, 2026", with no masthead. The previous issue, 25 October 2026 (`20261025.pdf`, text), has on page 1 "St. Francis de Sales Church", "614 Route 517, Vernon, NJ", "Mailing Address: P .O. Box 785, McAfee, NJ. 07428" and Rev. Chris Barkhausen, Pastor.

## Worship sites

- `st-francis-de-sales-mcafee`: the only church. Page 1 of the 25 October 2026 issue gives Weekend Masses Saturday (Vigil) 5:00 PM English and 7:00 PM Spanish, Sunday 8:00 AM, 10:00 AM, 12:00 PM, and weekday Mass Monday through Saturday 8:30 AM, and names no other place.

The finder (directory:11490) and GCatholic (19025) each list this one church.

## Website and bulletin provider

`stfrancisvernon.org` is eCatholic site 11490 behind Cloudflare (read with visit.py on 2026-11-04); `/bulletins` lists the `bulletins/<YYYYMMDD>.pdf` archive newest first, so provider is `ecatholic`. fetch:check on 2026-11-04 picked `20261101.pdf`.

## Not yet confirmed

Nothing open. The 1 November issue is image-only, so fetch:check can't verify identity from text; the rendered cover names the parish.
