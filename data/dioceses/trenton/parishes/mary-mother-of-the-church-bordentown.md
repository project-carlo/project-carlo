---
name: Mary, Mother of the Church Parish
website: https://www.mmotcp.org/bulletins
bulletin_provider: other
provider_id: page-pdfs https://www.mmotcp.org/bulletins
publication: ['po-org:mary-mother-of-the-church-parish-08505', 'lpi:0018000000Qx8ofAAB', 'po-container:03/4119']
group: Cohort 5
evidence:
- url: https://container.parishesonline.com/bulletins/03/4119/20261101B.pdf
  seen: 2026-10-30
  quote: MARY, MOTHER OF THE CHURCH PARISH
  note: '1 November 2026 issue, 12 pages, page 1 masthead: ''ST. MARY CHURCH 45 Crosswicks Street Bordentown,
    NJ 08505'' and ''HOLY ASSUMPTION CHURCH 1290 Hornberger Avenue Roebling, NJ 08554''; ''REV. MARTIN
    O’REILLY, Pastor'', ''REV. CESAR R. ANSON, Parochial Vicar'', Parish Office 609-298-0261. Page 2 ''MASS
    TIMES'': Saturday Vigil Holy Assumption 4:00 PM, St. Mary 5:30 PM; Sunday Holy Assumption 8:00 AM,
    St. Mary 9:45 AM and 11:30 AM; weekdays Holy Assumption - Roebling 9:30 AM (Tues., Wed., & Fri.),
    St. Mary - Bordentown 12:30 PM (Mon.-Fri.). The text was read from the parish site''s copy of the
    same issue (mmotcp.org/s/20261101web.pdf); the ParishesOnline copy is a different file (25 MB against
    the site''s smaller one) with the identical page-1 masthead. Footer ''Mary, Mother of the Church,
    Bordentown, NJ 03-4119'' is the LPi container.'
- url: https://parishesonline.com/organization/mary-mother-of-the-church-parish-08505
  seen: 2026-10-30
  note: 'probe po mary-mother-of-the-church-parish-08505: lpi 0018000000Qx8ofAAB, container 03/4119, title
    ''Mary, Mother of the Church Parish'', website mmotcp.org, address ''St. Mary Church, Bordentown,
    NJ, 08505'', latest issue 2026-11-01; weekly issues 4 October to 1 November 2026 listed.'
- url: https://www.mmotcp.org/bulletins
  seen: 2026-10-30
  quote: Recent Bulletins
  note: Squarespace page; lists 5 issues (Oct 4 to Nov 1 2026), each a file at www.mmotcp.org/s/<yyyymmdd>web.pdf
    (read in the browser with visit.py; probe get returns the page text without the file links). Same
    Sundays as the ParishesOnline container.
- url: https://trentonmonitor.com/2025/07/11/bishop-joins-bordentown-parish-for-feast-day-celebration-2/
  seen: 2026-10-30
  quote: Mary, Mother of the Church Parish was created in 2018 from the merger of St. Mary Parish, Bordentown,
    with Sts. Francis and Clare Parish, Florence Township. Today, Mary, Mother of the Church Parish has
    two worship sites – Holy Assumption, Roebling, and St. Mary Church, Bordentown.
  note: The Monitor, post dated 2025-07-11 (Feast of Mary, Mother of the Church Mass, 9 June 2025). Dates
    the merger and names the two worship sites.
- url: https://dioceseoftrenton.org/decisions
  seen: 2026-10-30
  quote: Linkage Model for Sts. Francis and Clare and St. Mary, no later than July 1, 2017; Merger Model,
    no later than July 1, 2018
  note: 'January 2017 decisions, Cohort 5 item 2: the plan the 2018 merger carried out.'
promoted: 2026-10-30
research:
- method: probe url mmotcp.org; probe po mary-mother-of-the-church-parish-08505; probe container 03/4119;
    probe pdf on the site's and ParishesOnline's 1 Nov 2026 issue; visit.py --links on /bulletins
  url: https://www.mmotcp.org/bulletins
  checked: '2026-10-30'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese trenton --parish mary-mother-of-the-church-bordentown, first as parishes_online
    (po-org slug), then as other with page-pdfs https://www.mmotcp.org/bulletins (headed Chrome)
  url: https://www.mmotcp.org/s/20261101web.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: the page-pdfs recipe picked the 1 November 2026 issue (5.9 MB, document_type pdf,
    freshness ''future'' as the coming Sunday''s issue). The ParishesOnline route picked 03/4119/20261101B.pdf
    (25,324,636 bytes), which exceeds fetch:check''s 25,000,000-byte inspection limit (document_type ''pdf_signature''
    only), hence the switch.'
bulletin_status: available
publication_reviews:
- parish: st-katharine-drexel-burlington
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/4119/20261101B.pdf
    seen: 2026-10-30
    quote: MARY, MOTHER OF THE CHURCH PARISH
    note: 'Bulletin for Mary, Mother of the Church Parish (row mary-mother-of-the-church-bordentown),
      read by its map batch: 1 November 2026 issue, 12 pages, page 1 masthead: ''ST. MARY CHURCH 45 Crosswicks
      Street Bordentown, NJ 08505'' and ''HOLY ASSUMPTION CHURCH 1290 Hornberger Avenue Roebling, NJ 08554'';
      ''REV. MARTIN O’REILLY, Pastor'', ''REV. CESAR R. ANSON, Parochial Vicar'', Parish Office 609-298-0261.
      Page 2 ''MASS TIMES'': Saturday Vigil Holy Assumption 4:00 PM, St. Mary 5:30 PM; Sunday Holy Assumption
      8:00 AM, St. Mary 9:45 AM and 11:30 AM; weekdays Holy Assumption - Roebling 9:30 AM (Tues., Wed.,
      & Fri.), St. Mary - Bordentown 12:30 PM (Mon.-Fri.). The text was read from the parish site''s copy
      of the same issue (mmotcp.org/s/20261101web.pdf); the ParishesOnline copy is a different file (25
      MB against the site''s smaller one) with the identical page-1 masthead. Footer ''Mary, Mother of
      the Church, Bordentown, NJ 03-4119'' is the LPi container.'
  - url: https://container.parishesonline.com/bulletins/03/4122/20261101B.pdf
    seen: 2026-10-30
    quote: The Parish of St. Katharine Drexel
    note: 'Bulletin for St. Katharine Drexel Parish (row st-katharine-drexel-burlington), read by its
      map batch: 1 November 2026 issue, 12 pages (text layer). Page 1 ''The Parish of St. Katharine Drexel
      Burlington, New Jersey''; page 2 ''PARISH CLERGY: Rev. Jerome Guld, Pastor, Deacon Matthew Fung,
      Deacon Walter J. Karpecik, Jr.''; ''MASS SCHEDULE: SATURDAY: 4:00 PM--All Saints Church. SUNDAY:
      8:00 AM--All Saints Church, 10:30 AM--St. Paul Church. Daily: 8:00 AM--St. Paul Church.'' ''PARISH
      LOCATIONS: All Saints Church 502 High Street, Burlington, NJ 08016; St. Paul Church 223 E. Union
      Street, Burlington, NJ 08016''. Parish office 223 E. Union Street. Intentions for 2 to 8 November
      are at St. Paul (Mass of Remembrance 6:30 PM, Holy Hour 7:00 PM Friday) and All Saints.'
---

## Publisher

Mary, Mother of the Church Parish, Bordentown (Cohort 5 in the July 2024 list, with St. Katharine Drexel, Burlington). It publishes its own weekly bulletin through ParishesOnline/LPi (container 03/4119). The 1 November 2026 masthead names the parish alone, with two churches, St. Mary (45 Crosswicks Street, Bordentown) and Holy Assumption (1290 Hornberger Avenue, Roebling), and one pastor, Rev. Martin O’Reilly. It does not mention St. Katharine Drexel, whose bulletin is a separate ParishesOnline container (03/4122) with its own masthead and pastor (see `st-katharine-drexel-burlington`).

The parish was created in 2018 by merging St. Mary Parish, Bordentown with Sts. Francis and Clare Parish, Florence Township (the Monitor, 2025-07-11), as the January 2017 decisions planned. GCatholic still lists the pre-merger churches St. Mary (Bordentown), St. Clare (Florence) and Holy Assumption (Roebling) with the old parish name 'St. Francis and St. Clare Parish'; the first and last still hold Mass, as `st-mary-bordentown` and `holy-assumption-roebling`, and St. Clare is in `open/st-clare-florence`.

## Worship sites

Two churches, both with public Mass in the 1 November 2026 schedule: St. Mary and Holy Assumption. St. Mary also has a 'Chapel of Saints' reached by a side door (open daily 7 AM to 7 PM, Wednesday exposition, Thursday Holy Hour 'St. Mary (Main Church)'): a chapel inside the church's campus with no address of its own, so not a separate church row (rule settled for this diocese). No Mass is listed anywhere else; St. Clare, Florence is not named in the issue (see `open/st-clare-florence`).

## Website and bulletin provider

Two channels carry the same weeks: the parish's Squarespace site (mmotcp.org/bulletins, files `www.mmotcp.org/s/<yyyymmdd>web.pdf`) and ParishesOnline container 03/4119. For 1 November 2026 they are different files with the same page-1 masthead and Mass schedule (md5 differ; the site's is 5.9 MB, ParishesOnline's 25.3 MB). Both are current to the same Sunday, so I took the one with a text layer that `fetch:check` can inspect: the row is `other` with `page-pdfs https://www.mmotcp.org/bulletins`. The ParishesOnline ids stay in `publication` (they identify this parish's bulletin; the org slug is `mary-mother-of-the-church-parish-08505`), and the row can go back to `parishes_online` with `provider_id: mary-mother-of-the-church-parish-08505` if the site stops posting. The finder's website, mmotcp.org, redirects to https://www.mmotcp.org/.

The parish homepage's Mass Times block differs from the bulletin's weekday lines: homepage 'Weekday Mass: Tuesday and Thursday 12:30 PM' at St. Mary and 'Wednesday and Friday 9:30 AM' at Holy Assumption; the bulletin says St. Mary 12:30 PM Monday to Friday and Holy Assumption 9:30 AM Tuesday, Wednesday and Friday. Weekend Masses agree. The bulletin is newer by construction, and both place weekday Mass at the same two churches.

## Not yet confirmed

Whether St. Clare Church, Florence holds Mass is in `open/st-clare-florence`.
