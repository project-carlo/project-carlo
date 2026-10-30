---
name: St. Elizabeth Ann Seton Parish
website: https://seaswhiting.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2166
publication: ['url:http://sponsors.bonventure.net/?page=2166']
group: Cohort 23 (Jackson, Lakehurst, Whiting)
evidence:
- url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
  seen: 2026-10-30
  quote: A Roman Catholic Parish in the Diocese of Trenton
  note: 'Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton, 30
    Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday 4:00
    pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00 am, ''Daily
    Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
- url: http://sponsors.bonventure.net/?page=2166
  seen: 2026-10-30
  note: 'Bon Venture sponsor page 2166: lists pdfs/2166/<yyyy-mm-dd>.pdf for 2026-10-11, 10-18, 10-25
    and 11-01. Found as the ''Bulletins'' link on the parish homepage (seaswhiting.org, browser read).'
- url: https://seaswhiting.org/news/mass-schedules
  seen: 2026-10-30
  quote: All Weekday Masses are held in All Saints Chapel unless otherwise specified.
  note: 'The parish''s Solutio site Mass Times page (browser read; probe url answers 403): Saturday 4:00
    pm; Sunday 8:00, 10:00 am and 12:00 pm; Mon-Fri 8:00 am and 12:00 pm; First Saturday 8:00 am. Agrees
    with the bulletin.'
- url: https://dioceseoftrenton.org/decisions
  seen: 2026-10-30
  quote: Collaborative Model for all four parishes in the Cohort
  note: 'Faith in Our Future decisions, Cohort 23 (St. Aloysius and St. Monica, Jackson; St. John, Lakehurst;
    St. Elizabeth Ann Seton, Whiting): the Collaborative Model for all four, so a cohort and not a linkage;
    item 2 ''Status of St. Monica to be reviewed periodically, beginning July 1, 2018''. Read in the browser
    with visit.py --text.'
research:
- method: pnpm fetch:check --diocese trenton --parish st-elizabeth-ann-seton-whiting (headed Chrome);
    page-pdfs on the Bon Venture sponsor page
  url: http://sponsors.bonventure.net/?page=2166
  checked: '2026-10-30'
  outcome: found
  next_action: None
- method: pnpm diocese probe url / recheck on seaswhiting.org (Solutio site)
  url: https://seaswhiting.org/news/mass-schedules
  checked: '2026-10-30'
  outcome: access-blocked
  next_action: 'Read the site with parish-site-access visit.py (done 2026-10-30: the Mass Times page and
    the Bulletins link to Bon Venture 2166 loaded); the bulletin itself is on Bon Venture, which plain
    fetch reads'
  retry_when: Plain fetch of seaswhiting.org stops answering 403, at which point 'diocese recheck' can
    verify the page quotes
bulletin_status: available
publication_reviews:
- parish: st-aloysius-jackson
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-aloysius-church-jackson-nj-08527/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. Aloysius: page 1 masthead ''SAINT ALOYSIUS
      CHURCH'' names St. Aloysius alone (Pastor Very Rev. John P. Bambrick, Mass schedule 8:30am daily,
      Sat 5:00pm, Sun 7:00am, 8:30am and 10:30am). Different pastor, staff and Mass times from St. Elizabeth
      Ann Seton.'
- parish: st-monica-jackson
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/church-of-saint-monica-jackson-nj-08527/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. Monica: page 1 masthead ''CHURCH OF SAINT
      MONICA'' names St. Monica alone (Pastor Rev. Alex Enriquez, Masses Mon-Thu 9 am, Sat 4 pm, Sun 9
      am and 11 am). Different pastor, staff and Mass times from St. Elizabeth Ann Seton.'
- parish: st-john-lakehurst
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-john-s-catholic-church-lakehurst-nj-08733/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. John''s, Lakehurst: pages 1-2 masthead (read
      from renders) names St. John''s Catholic Church, Lakehurst alone (Pastor Rev. James F. O''Neill,
      Sat 4 and 6 PM, Sun 9 and 11 AM). Different pastor, staff and Mass times from St. Elizabeth Ann
      Seton.'
---

## Publisher

St. Elizabeth Ann Seton Parish (Whiting) publishes one weekly bulletin through Bon Venture (sponsor page 2166), which its own Solutio site links as "Bulletins". The 1 November 2026 issue (text layer) is headed "St. Elizabeth Ann Seton, 30 Schoolhouse Road ~ Whiting, New Jersey", names Rev. Evarist Kabagambe as pastor and gives one Mass schedule. It names this parish alone. No John Patrick listing for it turned up in the Run's scans (tools/jppc-trenton.tsv has none), and the other Cohort 23 parishes publish through John Patrick under their own mastheads.

## Worship sites

One church campus at 30 Schoolhouse Road: the church (weekend Masses) and All Saints Chapel (weekday Masses, Adoration, columbarium; dedicated 2 May 1998 per the parish's Chapel & Columbarium page), both on the parish's one street address (see `st-elizabeth-ann-seton-whiting`). The chapel is recorded as part of that site, not a second church.

## Website and bulletin provider

seaswhiting.org refused `probe url` (403) but loaded in the browser; it is a Solutio site whose Bulletins link goes to sponsors.bonventure.net/?page=2166. The header of the bulletin names this parish, so the account is its own (page numbers are per account).

## Not yet confirmed

Nothing outstanding.
