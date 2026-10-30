---
name: St. Joseph Parish
website: https://stjosephtomsriver.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=3204
publication: ['url:http://sponsors.bonventure.net/?page=3204']
group: Cohort 24 RCCTR (Toms River)
evidence:
- url: http://sponsors.bonventure.net/pdfs/3204/2026-10-25.pdf
  seen: 2026-10-30
  quote: Very Rev. G. Scott Shaffer, VF
  note: 'Page 1 of the 25 October 2026 issue (12 pages, text layer; Bon Venture 3204; the 1 November file
    answered HTTP 404 on 2026-10-30, so 25 October is the latest posted): St. Joseph alone: ''685 Hooper
    Ave., Toms River, NJ 08753'', Pastor Very Rev. G. Scott Shaffer, VF; Mass schedule weekdays 7:00 and
    9:00 am, Saturday 8:00 am and 5:00 pm, Sunday 7:30, 9:00, 10:30 am, 12:00 noon, 5:00 and 6:30 pm (Spanish),
    and ''St. Gertrude, Island Heights: 2nd Sunday of the Month: 9:00am''. Page 2''s weekend Mass table
    repeats ''9:00 AM St. Gertrude''.'
- url: http://sponsors.bonventure.net/?page=3204
  seen: 2026-10-30
  quote: Click to View Current Bulletin
  note: Bon Venture sponsor page 3204, headed 'St. Joseph, 685 Hooper Avenue Toms River, NJ 08753'; previous
    bulletins listed weekly from 25 October 2026.
- url: https://stjosephtomsriver.org/bulletin/7-latest-bulletin
  seen: 2026-10-30
  note: 'Solutio CMS site, answers 403 to probe url and loads in the browser (visit.py --bulletin): its
    ''Latest Bulletin'' page redirects to sponsors.bonventure.net/?page=3204. John Patrick listing 561
    for the same church (church-bulletin.org/saint-joseph-church-toms-river-nj-08753) is a site-hosting
    page with no issues, so it is not a bulletin channel.'
- url: https://stjosephtomsriver.org/our-parish/st-gertrude
  seen: 2026-10-30
  note: 'Read in the browser. ''St. Gertrude Catholic Church, 103 Central Ave, Island Heights, NJ 08732;
    Mass Times: 2nd Sunday of each Month 9:00am; Summer Months: Sunday: 9:00am''. St. Gertrude is this
    parish''s mission, so GCatholic''s entry 18816 (which carries this site''s address as its website)
    is St. Joseph''s second worship site.'
- url: https://www.stmaximiliankolbechurch.com/rcctr
  seen: 2026-10-30
  quote: 'the four Roman Catholic parishes in Toms River: St. Joseph’s, St. Justin the Martyr, St. Luke’s
    and St. Maximilian Kolbe'
  note: 'Kolbe''s RCCTR page: a collaboration of leaders and clergy of four parishes that ''collaborate
    to find ways to strengthen our parishes''. It describes four parishes, not a shared bulletin; each
    publishes its own (see the four mastheads in the peer reviews).'
research:
- method: pnpm fetch:check --diocese trenton --parish st-joseph-toms-river (headed Chrome); page-pdfs
    on http://sponsors.bonventure.net/?page=3204
  url: http://sponsors.bonventure.net/?page=3204
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: picked the 25 October 2026 issue (fresh, 5 days; text PDF 20.6 MB; masthead names
    St. Joseph). The 1 November file answered 404 on 2026-10-30, so 25 October was the latest posted.'
- method: John Patrick listing 561 (church-bulletin.org/saint-joseph-church-toms-river-nj-08753) read
    with probe get
  url: https://www.church-bulletin.org/saint-joseph-church-toms-river-nj-08753
  checked: '2026-10-30'
  outcome: not-found
  next_action: 'None: the listing is a hosting page with no PDFs; the bulletin is on Bon Venture 3204.'
  retry_when: A dated PDF appears on the listing
bulletin_status: available
publication_reviews:
- parish: st-luke-toms-river
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/3204/2026-10-25.pdf
    seen: 2026-10-30
    note: The issue is a bulletin for St. Joseph alone, with its own pastor (Very Rev. G. Scott Shaffer,
      VF) and its own Mass times; it does not name St. Luke.
  - url: http://sponsors.bonventure.net/pdfs/4167/2026-11-01.pdf
    seen: 2026-10-30
    note: The issue is a bulletin for St. Luke alone, with its own pastor (Rev. Michael Kennedy) and its
      own Mass times.
- parish: st-justin-the-martyr-toms-river
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/3204/2026-10-25.pdf
    seen: 2026-10-30
    note: The issue is a bulletin for St. Joseph alone, with its own pastor (Very Rev. G. Scott Shaffer,
      VF) and its own Mass times; it does not name St. Justin the Martyr.
  - url: https://www.church-bulletin.org/bulletin/saint-justin-the-martyr-roman-catholic-church-toms-river-nj-08753/2026-11-01.pdf
    seen: 2026-10-30
    note: The issue is a bulletin for St. Justin the Martyr alone, with its own pastor (Rev. Mark A. Kreder)
      and its own Mass times.
- parish: st-maximilian-kolbe-toms-river
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/3204/2026-10-25.pdf
    seen: 2026-10-30
    note: The issue is a bulletin for St. Joseph alone, with its own pastor (Very Rev. G. Scott Shaffer,
      VF) and its own Mass times; it does not name St. Maximilian Kolbe.
  - url: http://sponsors.bonventure.net/pdfs/6497/2026-11-01.pdf
    seen: 2026-10-30
    note: The issue is a bulletin for St. Maximilian Kolbe alone, with its own pastor (Rev. Stephen M.
      Piga) and its own Mass times.
- parish: st-junipero-serra-seaside-park
  decision: separate
  evidence:
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
  - url: http://sponsors.bonventure.net/pdfs/2156/2026-11-01.pdf
    seen: 2026-10-30
    quote: Reverend Daniel F. Swift
    note: 'Bulletin for St. Leo the Great Parish (row st-leo-the-great-lincroft), read by its map batch:
      Page 2 of the 1 November 2026 issue (16 pages, text layer), ''Pastoral Staff'', Pastor Reverend
      Daniel F. Swift. Page 1 gives the Mass schedule: weekend Saturday 5:30 p.m., Sunday 7:00, 8:30,
      10:00, 11:30 a.m.; daily Monday through Saturday 9:00 a.m. The issue names St. Leo the Great alone
      (its own school, staff and parish center); the text layer has no mention of St. Catharine, St. Gabriel
      or St. Mary.'
- parish: st-peter-point-pleasant-beach
  decision: separate
  evidence:
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

St. Joseph publishes its own weekly bulletin, printed by Bon Venture (sponsor page 3204, reached from the parish's Solutio site). The 25 October 2026 issue, page 1, lists 'Mass Schedule: Weekdays 7:00am & 9:00am; Saturday 8:00am, 5:00pm; Sunday 7:30am, 9:00am, 10:30am, 12:00noon, 5:00pm, & 6:30pm (Mass in Spanish)' and 'St. Gertrude, Island Heights: 2nd Sunday of the Month: 9:00am', with the address 685 Hooper Ave., Toms River and Very Rev. G. Scott Shaffer, VF as pastor. It names no other Toms River parish, and the other three RCCTR parishes have different pastors and Mass tables (see publication_reviews).

## Worship sites

Two: St. Joseph, 685 Hooper Avenue, and its mission St. Gertrude, 103 Central Avenue, Island Heights (second Sunday of the month at 9:00 am; every Sunday at 9:00 am in the summer months, per the parish site). The bulletin's Mass schedule lists both. The parish's other addresses (Parish Ministry Center, 509 Hooper Ave.; St. Joseph's Cemetery and Mausoleums, 62 Cedar Grove Ave.; Carpenter Shop) are not Mass sites.

## Website and bulletin provider

Finder website http://www.stjosephtomsriver.org/ (now https://stjosephtomsriver.org/), a Solutio site that refuses `probe url` and loads in the browser. Its latest-bulletin page goes to Bon Venture 3204; the row reads that with `page-pdfs http://sponsors.bonventure.net/?page=3204`. The Solutio `/file` PDFs are blocked (diocese.md), but the Bon Venture PDFs are fetched directly.

## Not yet confirmed

Nothing outstanding. The fetch check result is in `research`.
