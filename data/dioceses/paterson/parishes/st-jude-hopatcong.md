---
name: St. Jude
website: https://stjudehopatcong.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:13527']
group: ''
evidence:
- url: https://files.ecatholic.com/13527/bulletins/20261101.pdf
  seen: 2026-11-04
  quote: Welcome to Saint Jude
  note: 'Page 1 of the 1 November 2026 issue (12 pages): ''Welcome to Saint Jude We are a Roman Catholic
    Parish, which gathers believers in Jesus Christ in Hopatcong and surrounding areas. Our Pastor is
    Fr. Peter Wierzbicki.'', ''40 Maxim Drive · Hopatcong · New Jersey · 07843''. Page 2 (rendered with
    render.py) is headed ''ALL SAINTS DAY NOVEMBER 1, 2026'' with Mass intentions 31 October to 8 November.
    Page 11: ''Sunday Masses: 5:00PM (Saturday Vigil Mass), 9:00AM and 11:00AM'', ''Weekday Masses (Mon
    - Sat) 8:00 a.m.'''
- url: https://stjudehopatcong.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403, Cloudflare). eCatholic site id 13527;
    the page lists weekly issues newest first, 'November 1, 2026' https://files.ecatholic.com/13527/bulletins/20261101.pdf
    back to 'September 13, 2026' .../20260913.pdf.
- url: https://stjudehopatcong.org/
  seen: 2026-11-04
  note: 'visit.py''s verdict was SPAM-SQUAT, but the rendered home page is the parish''s own (''St. Jude
    Parish 40 Maxim Dr. Hopatcong NJ 07843'', ''Welcome to St Jude'', Holiday Craft Fair, Diocesan Ministries
    Appeal): the trigger is the parish fundraiser headline ''Casino Night 2026''. It also embeds ecatholic:5303,
    the diocese''s own site, which is not recorded.'
bulletin_status: available
---

## Publisher

St. Jude, Hopatcong publishes its own weekly bulletin on its eCatholic site (id 13527). The 1 November 2026 issue (`https://files.ecatholic.com/13527/bulletins/20261101.pdf`, read 2026-11-04) opens on page 1 with "Welcome to Saint Jude … Our Pastor is Fr. Peter Wierzbicki" and "40 Maxim Drive · Hopatcong · New Jersey · 07843"; page 2 (rendered) is headed "ALL SAINTS DAY NOVEMBER 1, 2026".

## Worship sites

- `st-jude-hopatcong`: the only church. Page 2's Mass intentions (Saturday 8:00 AM and 5:00 PM; Sunday 9:00 AM, 11:00 AM and a 12:30 PM "Polish Mass" on 1 November; weekdays 8:00 AM) and page 11's schedule ("Sunday Masses: 5:00PM (Saturday Vigil Mass), 9:00AM and 11:00AM", "Weekday Masses (Mon - Sat) 8:00 a.m.") name no other place.

The diocese's finder (directory:13527) and GCatholic (19040) list this one church. The diocesan historian's list (https://rcdop.org/parishes-of-the-paterson-diocese, read 2026-11-04 with visit.py) has "1924 Saint Joseph, Hopatcong church colapsed and mission closed in 1947; See Saint Jude, Hopatcong" and "1958 Saint Jude, Hopatcong see Saint Joseph's, Hopatcong; parish status in 1966", and its closing note mentions "the four [now three] Catholic churches around Lake Hopatcong". St. Joseph is the fourth: its building collapsed and the mission closed in 1947, no roster lists it, and there is no building, so it has no record.

## Website and bulletin provider

`stjudehopatcong.org` is the parish's eCatholic site (site id 13527, the finder pin id), behind Cloudflare (probe url: 403). visit.py rated the home page SPAM-SQUAT, a false positive set off by the fundraiser headline "Casino Night 2026"; the page is the parish's own. Its `/bulletins` page (read 2026-11-04) lists weekly issues in `files.ecatholic.com/13527/bulletins/`, newest "November 1, 2026". Provider `ecatholic`. `fetch:check` on 2026-11-04 picked `https://files.ecatholic.com/13527/bulletins/20261101.pdf` (the 1 November 2026 issue, 3 days old: fresh). It reports identity unverified because no expected identity is supplied for eCatholic rows; page 1 was checked by hand above.

## Not yet confirmed

Nothing open.
