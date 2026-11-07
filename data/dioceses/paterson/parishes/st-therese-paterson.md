---
name: St. Therese
website: https://sttheresepaterson.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://sttheresepaterson.com/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403; eCatholic site, publication id ecatholic:11749
    in the page). The page shows the heading 'Bulletin' and an 'Archive' link and no bulletin files or
    links (screenshot and link list checked).
- url: https://sttheresepaterson.com/mass-times
  seen: 2026-11-04
  quote: 12:30 PM Spanish
  note: 'Mass Times page (visit.py): Sunday 10:00 AM and 12:30 PM Spanish; weekdays Monday 8:30 AM and
    7:00 PM Spanish, Tuesday 7:00 PM Spanish, Wednesday 8:30 AM and 7:00 PM Spanish, Friday 8:30 AM and
    7:00 PM Spanish; Saturday 7:30 AM Spanish, 5:00 PM, 7:00 PM Spanish. Header ''St. Therese RC Church
    - 80 13th Avenue Paterson, NJ 07504''.'
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: 'Diocese of Paterson parish finder (directory:11749): ''St. Therese, Paterson'', 80 13th Avenue,
    Paterson 07504, website https://sttheresepaterson.com/; its Mass times match the parish''s Mass Times
    page.'
revisit: Reload https://sttheresepaterson.com/bulletins with parish-site-access visit.py and probe files.ecatholic.com/11749/bulletins/<Sunday>.pdf;
  if issues appear, set provider ecatholic and publication ecatholic:11749 and run fetch:check.
revisit_after: 2027-02-01
research:
- method: parish-site-access visit.py on the site's /bulletins page (link list and screenshot)
  url: https://sttheresepaterson.com/bulletins
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reload the /bulletins page and its Archive in visit.py
  retry_when: On the revisit date, or when the finder or site links a bulletin
- method: issues.py ecatholic ecatholic:11749 (files.ecatholic.com/11749/bulletins/<YYYYMMDD>.pdf, every
    Sunday 4 Oct - 8 Nov 2026, and 14 Jun, 19 Jul, 23 Aug, 27 Sep 2026)
  url: https://files.ecatholic.com/11749/bulletins/20261101.pdf
  checked: '2026-11-04'
  outcome: not-found
  next_action: Probe the coming Sundays' file names again; also try Saturday-dated names (--day sat)
  retry_when: On the revisit date
- method: visit.py on the parish Facebook page linked from the site
  url: https://www.facebook.com/st.therese.paterson
  checked: '2026-11-04'
  outcome: access-blocked
  next_action: Look for bulletin posts on the Facebook page in a logged-in or later public view
  retry_when: Facebook shows the page publicly
bulletin_status: not-found
---

## Publisher

No bulletin found. St. Therese, Paterson runs an eCatholic site (site id 11749, the finder pin id) whose Bulletin page, read 2026-11-04 with parish-site-access visit.py, shows a heading and an "Archive" link and no issues. `files.ecatholic.com/11749/bulletins/<YYYYMMDD>.pdf` answered 403 (not posted) for every Sunday from 4 October to 8 November 2026 and for four Sundays June-September 2026. The parish's Facebook page (linked from the site) showed "This content isn't available right now" to the browser. See `research`.

## Worship sites

One church, `st-therese-paterson` (80 13th Avenue), whose Mass Times page lists Sunday 10:00 AM and 12:30 PM Spanish, Saturday 5:00 PM and Spanish Masses, and daily Masses. The site's "Perpetual Eucharistic Adoration Chapel" page is for adoration, not Mass, and was not taken as a separate worship site. The finder (directory:11749) and GCatholic (19052) list this one church.

## Website and bulletin provider

`https://sttheresepaterson.com/` (the finder's website; eCatholic behind Cloudflare, so probe url gets 403 and visit.py reads it). Provider `no_bulletin`: the parish has public Mass but posts no bulletin anywhere found, so promote keeps the row and its church off the site until a bulletin turns up. No publication id is recorded because no bulletin was found; if issues appear they will be `ecatholic:11749`.

## Not yet confirmed

Whether the parish prints a bulletin it doesn't post online (the office, 973-881-0400, could say). The revisit on 2027-02-01 rereads the Bulletin page and the eCatholic file names.
