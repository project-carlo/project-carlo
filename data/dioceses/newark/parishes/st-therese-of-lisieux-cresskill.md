---
name: St. Therese of Lisieux, Cresskill
website: https://sttheresecresskill.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:10734', 'po-container:03/4008']
group: Planning Area B
evidence:
- url: https://files.ecatholic.com/10734/bulletins/20261101.pdf
  seen: 2026-11-03
  quote: St. Therese Church
  note: '1 November 2026 issue (8 pages; pages 1-6 are images, rendered with render.py). Page 1 masthead
    (image): ''ST. THERESE OF LISIEUX PARISH 120 MONROE AVE., CRESSKILL, NJ | 201.567.2528 | STTHERESECRESSKILL.ORG'',
    ''SUNDAY, NOVEMBER 1, 2026''. Page 2 (image) Mass Schedule box: Daily 8:30am; Saturday 4:30pm; Sunday
    7:30am, 9:30am, 11:30am. Pages 7-8 text footer: ''www.4lpi.com St. Therese Church | 03-4008''.'
- url: https://container.parishesonline.com/bulletins/03/4008/20261101B.pdf
  seen: 2026-11-03
  quote: St. Therese Church
  note: 'probe container 03/4008: the same 8-page 1 November 2026 issue is in the LPi container, footer
    ''St. Therese Church | 03-4008''.'
- url: https://sttheresecresskill.org/bulletins
  seen: 2026-11-03
  note: 'eCatholic bulletin page (read with parish-site-access visit.py): weekly files.ecatholic.com/10734/bulletins/YYYYMMDD.pdf
    issues, newest ''November 1, 2026'', then October 25, 18, 11, 4.'
bulletin_status: available
---

## Publisher

St. Therese of Lisieux Parish, Cresskill, publishes a weekly bulletin printed by LPi (footer 'St. Therese Church | 03-4008', container 03/4008) and posts it on its eCatholic site (ecatholic:10734). I read the 1 November 2026 issue: the page 1 masthead (image) names 'ST. THERESE OF LISIEUX PARISH, 120 MONROE AVE., CRESSKILL, NJ' and page 2 has one Mass schedule and one list of Mass intentions. No other parish or church is named.

## Worship sites

- St. Therese of Lisieux Church, 120 Monroe Avenue (`st-therese-of-lisieux-cresskill`): Saturday 4:30 PM (schedule box) or 5:00 PM (intentions); Sunday 7:30, 9:30, 11:30 AM; daily 8:30 AM.

The directory (20) and GCatholic (18376) list only this church.

## Website and bulletin provider

https://sttheresecresskill.org/ (the directory's address) is an eCatholic site. `probe get` read the homepage this time; `visit.py` loaded it and its /bulletins page on the first try and reported ecatholic:10734. The same issue is also in ParishesOnline container 03/4008 (no org slug known), so both ids are recorded as this bulletin's. Provider `ecatholic`, read from the site's Sunday-dated files, as for Our Lady of Victories, Harrington Park. GCatholic's www.4sttherese.org did not answer `probe get` (old domain, not used).

Pages 1-6 have no text layer (LPi image pages); only the ad-page footer is text. The pipeline needs to read the schedule as an image.

Fetch check (2026-11-03, headed): transport ok, PDF, picked `files.ecatholic.com/10734/bulletins/20261101.pdf`, the 1 November 2026 issue read above; freshness fresh (2 days). Publication identity `unverified` in the check (the masthead is an image); the rendered masthead confirms it.

## Not yet confirmed

The page 2 Mass Schedule box gives Saturday 4:30 PM, while the intentions for Saturday 31 October list 5:00. Which is current would be settled by the next issues or the site's Mass times page; it doesn't affect the row.
