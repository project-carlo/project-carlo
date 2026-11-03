---
name: St. Peter the Apostle University and Community Parish
website: https://www.stpeternewbrunswick.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:21126']
group: ''
evidence:
- url: https://files.ecatholic.com/21126/bulletins/20261025.pdf
  seen: 2026-11-03
  quote: All masses are in the Church.
  note: 'Page 1 of the 25 October 2026 issue (6 pages, text): masthead ''St.Peter the Apostle'', ''UNIVERSITY
    & COMMUNITY PARISH'', ''94 Somerset St. New Brunswick, NJ 08901'', www.stpeternewbrunswick.org; Mass
    Saturday 5pm, Sunday 9am, 11:30am, 6pm, weekdays Mon-Fri 7:30am and 12:15pm, Saturday 9am, ''All masses
    are in the Church.''; adoration Thursday ''in the Catholic Center Chapel''. Page 2 staff list: ''Rev.
    Michael Tabernero, Pastor''. Pages 5-6 ad-page line ''G60664 (CK) - St. Peter The Apostle • New Brunswick,
    NJ … BON VENTURE SERVICES, LLC''.'
- url: https://www.stpeternewbrunswick.org/bulletins
  seen: 2026-11-03
  note: The parish's eCatholic Bulletin page (read with visit.py; probe get answers 403) lists files.ecatholic.com/21126/bulletins/<YYYYMMDD>.pdf
    weekly from 20260802 to 20261025, newest first; files.ecatholic.com/21126/bulletins/20261101.pdf answered
    403 on 2026-11-03 (not yet posted).
- url: https://diometuchen.org/parishfinder
  seen: 2026-11-03
  note: 'Parish finder: St. Peter the Apostle University and Community Parish, 94 Somerset Street, New
    Brunswick; ''The Catholic Center at Rutgers University | Pastor: Rev. Msgr. Joseph G. Celano''. The
    bulletin names Rev. Michael Tabernero as pastor; Msgr. Celano is named pastor by Immaculate Conception,
    Somerville''s own bulletin (lead from an earlier batch).'
bulletin_status: available
---

## Publisher

St. Peter the Apostle University and Community Parish, New Brunswick, posts its own weekly bulletin on its eCatholic site (`ecatholic:21126`). The 25 October 2026 issue (read 2026-11-03) has the masthead 'St.Peter the Apostle' / 'UNIVERSITY & COMMUNITY PARISH', 94 Somerset St., and its page 2 staff list names 'Rev. Michael Tabernero, Pastor'. The parish finder's pastor, Msgr. Joseph G. Celano, is wrong for this parish: an earlier batch read Immaculate Conception, Somerville's 1 November 2026 bulletin naming him its pastor, with its own eCatholic bulletin (22346), so the shared finder pastor is no shared bulletin. The bulletin is printed by Bon Venture (ad pages carry account code 'G60664 (CK) - St. Peter The Apostle • New Brunswick, NJ'); I did not look for a sponsors.bonventure.net listing, since the parish-hosted copy is the one recorded.

## Worship sites

One church, St. Peter the Apostle, 94 Somerset Street (directory:24515, gcatholic:18684). The 25 October bulletin says 'All masses are in the Church.' The Catholic Center at Rutgers (rutgerscatholic.org), named in the finder entry and the bulletin's contacts, appears only as the place of Thursday adoration ('in the Catholic Center Chapel'), with no Mass, so it gets no church record.

## Website and bulletin provider

Website https://www.stpeternewbrunswick.org (eCatholic 21126; the finder's http URL redirects there). GCatholic lists an older domain, stpetertheapostle.org, which I did not follow. The Bulletin page answers 403 to `probe get` but loads in the browser.

## Not yet confirmed

Nothing about the publisher. The Bon Venture listing number, if one exists, is unrecorded.

## Fetch check

`pnpm fetch:check` on 2026-11-03 read the eCatholic Bulletin page and picked files.ecatholic.com/21126/bulletins/20261025.pdf: transport ok, PDF, issue date inferred from the file name (25 October 2026), freshness `fresh`, identity unverified by the tool. The 1 November issue was not yet posted that day. I read the 25 October masthead myself (above). eCatholic needs no `recipe`.
