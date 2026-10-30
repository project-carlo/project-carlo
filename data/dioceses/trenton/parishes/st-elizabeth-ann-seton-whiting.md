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
promoted: 2026-10-30
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
- parish: st-gregory-the-great-hamilton
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/2098/2026-11-01.pdf
    seen: 2026-10-30
    quote: Rev. Michael Hall, Pastor
    note: 'Bulletin for St. Gregory the Great Parish (row st-gregory-the-great-hamilton), read by its
      map batch: 1 November 2026 issue (12 pages, text layer). Page 1 is a cover (''SUNDAY, NOVEMBER 1,
      2026''); page 2: pastor Rev. Michael Hall, parochial vicar Rev. Cyril Johnson; Mass Times: Sunday
      7:30 AM, 9:00 AM, 10:30 AM, 12:00 PM; Saturday 8:30 AM and 5:00 PM vigil; weekdays 7:00 AM, 8:30
      AM; Eucharistic Adoration Wednesday ''in the Chapel''; Parish Office 4620 Nottingham Way, Hamilton
      Square, NJ.'
- parish: st-joseph-toms-river
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/3204/2026-10-25.pdf
    seen: 2026-10-30
    quote: Very Rev. G. Scott Shaffer, VF
    note: 'Bulletin for St. Joseph Parish (row st-joseph-toms-river), read by its map batch: Page 1 of
      the 25 October 2026 issue (12 pages, text layer; Bon Venture 3204; the 1 November file answered
      HTTP 404 on 2026-10-30, so 25 October is the latest posted): St. Joseph alone: ''685 Hooper Ave.,
      Toms River, NJ 08753'', Pastor Very Rev. G. Scott Shaffer, VF; Mass schedule weekdays 7:00 and 9:00
      am, Saturday 8:00 am and 5:00 pm, Sunday 7:30, 9:00, 10:30 am, 12:00 noon, 5:00 and 6:30 pm (Spanish),
      and ''St. Gertrude, Island Heights: 2nd Sunday of the Month: 9:00am''. Page 2''s weekend Mass table
      repeats ''9:00 AM St. Gertrude''.'
- parish: st-junipero-serra-seaside-park
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/4142/2026-11-01.pdf
    seen: 2026-10-30
    quote: Dos Templos en una Parroquia UNIDA
    note: 'Bulletin for St. Junipero Serra Parish (row st-junipero-serra-seaside-park), read by its map
      batch: Page 1 of the 1 November 2026 issue (8 pages, text layer; md5 of the file e3c3c4e2a15a0705ace462adb94938e8):
      header ''50 E Street • Seaside Park, NJ 08752, 732-793-0041 / www.stjuniperoserra.org'', ''Served
      by the Franciscan Friars Conventual'', ''Two Houses of Worship in ONE UNITED Parish'' (the English
      words are font-garbled in the text layer; the Spanish line is readable), then each church''s Sunday
      and daily Masses: Our Lady of Perpetual Help, 100 Grant Avenue, Seaside Heights, and St. Catharine
      of Siena Church, 50 E Street, Seaside Park. It names this parish alone.'
- parish: st-leo-the-great-lincroft
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/2156/2026-11-01.pdf
    seen: 2026-10-30
    quote: Reverend Daniel F. Swift
    note: 'Bulletin for St. Leo the Great Parish (row st-leo-the-great-lincroft), read by its map batch:
      Page 2 of the 1 November 2026 issue (16 pages, text layer), ''Pastoral Staff'', Pastor Reverend
      Daniel F. Swift. Page 1 gives the Mass schedule: weekend Saturday 5:30 p.m., Sunday 7:00, 8:30,
      10:00, 11:30 a.m.; daily Monday through Saturday 9:00 a.m. The issue names St. Leo the Great alone
      (its own school, staff and parish center); the text layer has no mention of St. Catharine, St. Gabriel
      or St. Mary.'
- parish: st-luke-toms-river
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/4167/2026-11-01.pdf
    seen: 2026-10-30
    quote: Rev. Michael Kennedy
    note: 'Bulletin for St. Luke Parish (row st-luke-toms-river), read by its map batch: Page 1 of the
      1 November 2026 issue (12 pages, text layer; Bon Venture 4167): St. Luke alone: ''ST. LUKE'', ''1674
      OLD FREEHOLD ROAD • TOMS RIVER, NEW JERSEY 08755'', pastor Rev. Michael Kennedy, Mass schedule Saturday
      vigil 4:00 pm, Sunday 7:30, 10:00 am and 12:00 pm, weekdays 7:30 am (Wednesday also 12:30 pm, Friday
      also 11:00 am). The Bon Venture issue is the coming Sunday''s (future freshness).'
- parish: st-maximilian-kolbe-toms-river
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/6497/2026-11-01.pdf
    seen: 2026-10-30
    quote: Rev. Stephen M. Piga
    note: 'Bulletin for St. Maximilian Kolbe Parish (row st-maximilian-kolbe-toms-river), read by its
      map batch: Page 1 of the 1 November 2026 issue (12 pages, text layer; Bon Venture 6497): St. Maximilian
      Kolbe alone: ''Prayer to Saint Maximilian Kolbe'', Pastor Rev. Stephen M. Piga; Mass schedule weekend
      Saturday 4:00 pm, Sunday 7:00, 9:00, 11:00 am and 1:00 pm; weekday Tuesday and Saturday 7:00 am,
      Monday, Wednesday, Thursday and Friday 8:30 am.'
- parish: st-peter-point-pleasant-beach
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/2097/2026-11-01.pdf
    seen: 2026-10-30
    quote: Saint Peter Catholic Church
    note: 'Bulletin for St. Peter Church (row st-peter-point-pleasant-beach), read by its map batch: Page
      1 of the 1 November 2026 issue (12 pages; text on 10, pages 6-7 image-only): ''The Solemnity of
      All Saints, St. Peter Church, November 1, 2026, Saint Peter Catholic Church, 406 Forman Avenue,
      Point Pleasant Beach, New Jersey 08742, (732) 892-0049''. Page 2: Sunday Masses 7:30, 9:00 and 11:00
      a.m.; weekday 8:30 a.m.; Saturday 5:00 p.m. It names St. Peter alone.'
- parish: st-rose-belmar
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    quote: A Roman Catholic Parish in the Diocese of Trenton
    note: 'Bulletin for St. Elizabeth Ann Seton Parish (row st-elizabeth-ann-seton-whiting), read by its
      map batch: Pages 1-2 of the 1 November 2026 issue (16 pages, text layer): ''St. Elizabeth Ann Seton,
      30 Schoolhouse Road ~ Whiting, New Jersey''; ''Rev. Evarist Kabagambe ... Pastor''; Masses Saturday
      4:00 pm, Sunday 8:00, 10:00 am & 12:00 pm, Monday-Friday 8:00 am & 12:00 pm, First Saturday 8:00
      am, ''Daily Masses in All Saints Chapel unless otherwise specified''. It names this parish alone.'
  - url: http://sponsors.bonventure.net/pdfs/2155/2026-11-01.pdf
    seen: 2026-10-30
    quote: Rev. Msgr. Edward J. Arnister
    note: 'Bulletin for Church of Saint Rose (row st-rose-belmar), read by its map batch: Page 1 of the
      1 November 2026 issue (16 pages, text layer): ''MASS SCHEDULE / WEEKDAYS 6:45 am & 9:00 am / SATURDAY
      5:00 pm (Vigil) / SUNDAY 7:00, 9:30, 11:30 am & 5:00 pm'', Rev. Msgr. Edward J. Arnister, Pastor,
      Rev. Dr. John Paul Del Rosario, Parochial Vicar, ''RECTORY & PARISH OFFICE 603 Seventh Ave., Belmar,
      NJ 07719 p: 732-681-0512''; page 2''s header reads ''CHURCH OF SAINT ROSE - BELMAR, NEW JERSEY -
      NOVEMBER 1, 2026''. It names this parish alone.'
---

## Publisher

St. Elizabeth Ann Seton Parish (Whiting) publishes one weekly bulletin through Bon Venture (sponsor page 2166), which its own Solutio site links as "Bulletins". The 1 November 2026 issue (text layer) is headed "St. Elizabeth Ann Seton, 30 Schoolhouse Road ~ Whiting, New Jersey", names Rev. Evarist Kabagambe as pastor and gives one Mass schedule. It names this parish alone. No John Patrick listing for it turned up in the Run's scans (tools/jppc-trenton.tsv has none), and the other Cohort 23 parishes publish through John Patrick under their own mastheads.

## Worship sites

One church campus at 30 Schoolhouse Road: the church (weekend Masses) and All Saints Chapel (weekday Masses, Adoration, columbarium; dedicated 2 May 1998 per the parish's Chapel & Columbarium page), both on the parish's one street address (see `st-elizabeth-ann-seton-whiting`). The chapel is recorded as part of that site, not a second church.

## Website and bulletin provider

seaswhiting.org refused `probe url` (403) but loaded in the browser; it is a Solutio site whose Bulletins link goes to sponsors.bonventure.net/?page=2166. The header of the bulletin names this parish, so the account is its own (page numbers are per account).

## Not yet confirmed

Nothing outstanding.
