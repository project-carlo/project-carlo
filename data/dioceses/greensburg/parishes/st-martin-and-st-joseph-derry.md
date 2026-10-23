---
name: Partner Parishes of St. Martin and St. Joseph, Derry
website: https://www.stmartinstjoseph.org
bulletin_provider: other
provider_id: dated-post https://www.stmartinstjoseph.org/bulletin/bulletins/
publication: ['url:https://www.stmartinstjoseph.org/bulletin/bulletins/']
group: 'Partners: St. Joseph, Derry + St. Martin, New Derry'
evidence:
- url: https://www.stmartinstjoseph.org/wp-content/uploads/2026/10/october-25th-2026.pdf
  seen: 2026-10-22
  quote: Mission Statement of the Partner Parishes of St. Martin and St. Joseph
  note: 'Page 1 of the 25 Oct 2026 issue: "October 25th, 2026 ... 30th Sunday in Ordinary Time", "Partner
    Parishes of the Diocese of Greensburg", "125 SOUTH LIGONIER ST. DERRY, PA. 15627 Partner Parish Office",
    "WEBSITE: www.stmartinstjoseph.org", "Rev. Salvatore Lamendola, Pastor", footer "St. Joseph and St.
    Martin Partner Parishes, Derry".'
- url: https://www.stmartinstjoseph.org/wp-content/uploads/2026/10/october-25th-2026.pdf
  seen: 2026-10-22
  quote: 9:00 AM, St. Martin
  note: 'Page 2, Mass intentions for the week: Saturday 4:00 PM St. Joseph; Sunday 9:00 AM St. Martin
    and 10:30 AM St. Joseph; Monday 6:00 PM St. Martin; Tuesday and Thursday 8:00 AM St. Joseph; Friday
    8:00 AM St. Martin. No other place.'
- url: https://www.stmartinstjoseph.org/bulletin/bulletins/
  seen: 2026-10-22
  note: 'Read in headed Chrome (parish-site-access visit.py; probe url gets 403). "Read our Weekly Bulletins"
    lists one post per issue, newest first: "October 25th, 2026", "October 18th, 2026" ... "August 23rd,
    2026". The 25 Oct post embeds a dFlip flipbook whose source is wp-content/uploads/2026/10/october-25th-2026.pdf.'
- url: https://parishesonline.com/organization/st-martin-st-joseph-churches
  seen: 2026-10-22
  note: 'probe po: LPi organizations st-martin-st-joseph-churches (lpi:0018000000QxC0cAAF, "St. Martin
    & St. Joseph Churches", 117 S Ligonier St, Derry) and st-martin-church-15671 (lpi:0018000000QxC0hAAF,
    5684 Route 982, New Derry) both answer "no publications". Old, empty accounts, not a live channel.'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=077
  seen: 2026-10-22
  note: 'Directory: St. Joseph Parish, Derry, pastor Father Salvatore R. Lamendola, "Saturday: 4:00 p.m.;
    Sunday: 10:30 a.m.", Partner Parishes "St. Martin Parish, New Derry (219)", website stmartinstjoseph.org.
    LocationID=219 (St. Martin): same pastor, "Saturday: no Mass; Sunday: 9:00 a.m.", partner St. Joseph,
    same website, mailing address c/o 125 South Ligonier Street.'
promoted: 2026-10-23
---

## Publisher

St. Joseph Parish, Derry (directory 077) and St. Martin Parish, New Derry (directory 219) are two canonical parishes in a diocesan partnership with one pastor (Fr. Salvatore Lamendola), one office (125 South Ligonier St., Derry) and one website, stmartinstjoseph.org. They publish one weekly bulletin, self-hosted on that site. The 25 October 2026 issue (read 2026-10-22 with `probe pdf`) has both towns in its masthead ("Derry, Pa. 15627", "New Derry, Pa. 15671"), "Partner Parishes of the Diocese of Greensburg", one joint staff list, and a single week of Mass intentions for both churches (page 2). One bulletin, so one row.

## Worship sites

St. Joseph (Derry) and St. Martin (New Derry): the only two places in the 25 Oct Mass intentions and on the site's home-page Mass times ("Saturday: 4:00 p.m. – St. Joseph", "Sunday: 9:00 a.m. – St. Martin, 10:30 a.m. – St. Joseph", weekdays split between them). GCatholic and the diocesan directory list no other site for either parish. Both parishes' cemeteries (a "Cemetery Supervisor" is on the staff list) are not worship sites and were not recorded.

## Website and bulletin provider

stmartinstjoseph.org is a diocese-template WordPress site; it answers 403 to `probe url` but opens in headed Chrome. Its bulletin page `/bulletin/bulletins/` links one child post per issue (e.g. `/october-25th-2026/`), each embedding a dFlip flipbook of a PDF in `wp-content/uploads/<yyyy>/<mm>/`. Provider `other`; `fetch:check` on 2026-10-22 resolved "dated-post on https://www.stmartinstjoseph.org/bulletin/bulletins/: current", downloaded `october-25th-2026.pdf` (url_date 2026-10-25, 2,475,577 bytes) and printed the recipe recorded as `provider_id`. The two LPi organizations near Derry (st-martin-st-joseph-churches, st-martin-church-15671) have no publications and are not recorded as publication ids. Searched the LPi geo-search within 4 miles of Derry; no other publisher found.

## Not yet confirmed

Nothing about the bulletin. The site blocks plain fetches (403), so the pipeline's fetch depends on the headed-browser path working for this host; `fetch:check` succeeded headed on 2026-10-22. St. Joseph's street number (117 vs 125 S Ligonier) is unsettled; see its church record.
