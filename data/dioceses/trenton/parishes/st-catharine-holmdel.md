---
name: Church of St. Catharine
website: https://www.stcatharine.net/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stcatharine.net/weekly-constant-contact']
group: Cohort 13 (Marlboro, Colts Neck, Holmdel, Lincroft)
evidence:
- url: https://myemail.constantcontact.com/October-29th-Events-at-St--Catharine-s-Church.html?soid=1104301294497&aid=LhQWZRJIcoc
  seen: 2026-10-30
  quote: Weekly Parish Update - October 29
  note: 'The parish''s weekly communication, an HTML Constant Contact email (no PDF) with Mass Times (Saturday
    5:00 pm; Sunday 8:00 am, 10:00 am, 12:00 pm) and ''Weekly Mass Intentions: Week of November 1, 2026''.
    It names St. Catharine''s alone; Monday-Wednesday 9:00 AM are listed as ''Mass at St. Mary'' and Thursday-Saturday
    9:00 AM Masses as St. Catharine''s own.'
- url: https://www.stcatharine.net/weekly-constant-contact
  seen: 2026-10-30
  quote: Sign-up for Weekly Emails Here
  note: The site's 'Weekly Email' page is the archive of these emails, one link per week (the newest,
    'October 29', through conta.cc/3Uop4pK).
- url: https://www.stcatharine.net/bulletins
  seen: 2026-10-30
  note: The site's 'Bulletin' page (eCatholic) shows only the heading 'Bulletin' and 'Archive' and no
    PDF; its one PDF link is a youth-ministry registration packet. Sunday, Friday and Saturday-dated files.ecatholic.com/35015/bulletins/
    files for the last six to eight weeks all answered 403 (missing).
- url: https://www.stcatharine.net/staff
  seen: 2026-10-30
  quote: Reverend Patrick McPartland
  note: 'Staff page: Pastor Reverend Patrick McPartland. St. Mary, Colts Neck''s pastor is Reverend Fr.
    Jeffrey E. Lee (its 1 November 2026 masthead), so the two parishes don''t share a pastor.'
revisit: Check whether St. Catharine posts a PDF bulletin, or the pipeline gains a reader for its Constant
  Contact 'Weekly Parish Update' emails
revisit_after: 2027-01-15
research:
- method: fetch:check ecatholic resolver on stcatharine.net/bulletins; files.ecatholic.com/35015/bulletins/
    probes by Sunday, Friday and Saturday date for 6-8 weeks; the Run's John Patrick ZIP scan (no 07733
    listing); read the Weekly Email archive and its newest issue
  url: https://www.stcatharine.net/bulletins
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: A reader for the Constant Contact 'Weekly Parish Update' HTML emails (a collector, owner
    decision), or find a PDF bulletin on the parish site or a printer
  retry_when: The pipeline can read HTML parish emails, or the parish posts a PDF bulletin
  revisit_after: 2027-01-15
- method: probe get on the Weekly Email archive and its newest issue, and on the eCatholic /bulletins
    page (hand refresh against main)
  url: https://www.stcatharine.net/weekly-constant-contact
  checked: '2026-11-07'
  outcome: unsupported-format
  next_action: Set a provider once a collector reads Constant Contact HTML newsletters (or the parish
    posts a PDF bulletin), run fetch:check, and clear fetch_gap when it picks this week's issue.
  retry_when: A collector for fetch_gap kind constant-contact-html-newsletter exists, or the parish posts
    a PDF bulletin
bulletin_status: unsupported-format
fetch_gap:
  kind: constant-contact-html-newsletter
  seen: 2026-11-07
  note: The parish's weekly bulletin is an HTML Constant Contact email ('Weekly Parish Update'), archived
    one link per week on https://www.stcatharine.net/weekly-constant-contact (conta.cc short links to
    myemail.constantcontact.com pages); no PDF. The 5 November 2026 issue carries the Mass times and 'Weekly
    Mass Intentions | Week of November 8, 2026'. The eCatholic /bulletins page (35015) still holds no
    bulletin.
  url: https://myemail.constantcontact.com/November-5th-Events-at-St--Catharine-s-Church.html?soid=1104301294497&aid=EnK3w9P6Gs4
publication_reviews:
- parish: st-gabriel-marlboro
  decision: separate
  evidence:
  - url: https://myemail.constantcontact.com/November-5th-Events-at-St--Catharine-s-Church.html?soid=1104301294497&aid=EnK3w9P6Gs4
    seen: 2026-11-07
    quote: Weekly Parish Update - November 5
    note: 'Bulletin for the Church of St. Catharine (row st-catharine-holmdel): the 5 November 2026 Constant
      Contact email names St. Catharine''s alone, with its own Mass times (Saturday 5:00 pm; Sunday 8:00,
      10:00 am, 12:00 pm) and ''Weekly Mass Intentions | Week of November 8, 2026''. It is a different
      publication from each Cohort 13 neighbour''s PDF bulletin.'
  - url: https://www.church-bulletin.org/bulletin/saint-gabriel-s-roman-catholic-church-marlboro-nj-07746/2026-11-01.pdf
    seen: 2026-10-30
    note: 'Bulletin for St. Gabriel Parish (row st-gabriel-marlboro), read by its map batch: Masthead,
      page 2 of the 1 November 2026 issue (12 pages, scanned images with no text layer; read from a render
      of the page). Reads "St. Gabriel''s Roman Catholic Church, 100 North Main Street, Marlboro, New
      Jersey 07746", Pastor Rev. Brian T. Butch, and the schedule ''WEEKEND MASSES: Saturday Evening Vigil:
      4:30PM; Sunday Masses: 8:00AM; 9:30AM; 11:00AM; 5:00PM''. Names St. Gabriel alone; no other parish
      or church appears in the masthead.'
- parish: st-leo-the-great-lincroft
  decision: separate
  evidence:
  - url: https://myemail.constantcontact.com/November-5th-Events-at-St--Catharine-s-Church.html?soid=1104301294497&aid=EnK3w9P6Gs4
    seen: 2026-11-07
    quote: Weekly Parish Update - November 5
    note: 'Bulletin for the Church of St. Catharine (row st-catharine-holmdel): the 5 November 2026 Constant
      Contact email names St. Catharine''s alone, with its own Mass times (Saturday 5:00 pm; Sunday 8:00,
      10:00 am, 12:00 pm) and ''Weekly Mass Intentions | Week of November 8, 2026''. It is a different
      publication from each Cohort 13 neighbour''s PDF bulletin.'
  - url: http://sponsors.bonventure.net/pdfs/2156/2026-11-01.pdf
    seen: 2026-10-30
    quote: Reverend Daniel F. Swift
    note: 'Bulletin for St. Leo the Great Parish (row st-leo-the-great-lincroft), read by its map batch:
      Page 2 of the 1 November 2026 issue (16 pages, text layer), ''Pastoral Staff'', Pastor Reverend
      Daniel F. Swift. Page 1 gives the Mass schedule: weekend Saturday 5:30 p.m., Sunday 7:00, 8:30,
      10:00, 11:30 a.m.; daily Monday through Saturday 9:00 a.m. The issue names St. Leo the Great alone
      (its own school, staff and parish center); the text layer has no mention of St. Catharine, St. Gabriel
      or St. Mary.'
- parish: st-mary-colts-neck
  decision: separate
  evidence:
  - url: https://myemail.constantcontact.com/November-5th-Events-at-St--Catharine-s-Church.html?soid=1104301294497&aid=EnK3w9P6Gs4
    seen: 2026-11-07
    quote: Weekly Parish Update - November 5
    note: 'Bulletin for the Church of St. Catharine (row st-catharine-holmdel): the 5 November 2026 Constant
      Contact email names St. Catharine''s alone, with its own Mass times (Saturday 5:00 pm; Sunday 8:00,
      10:00 am, 12:00 pm) and ''Weekly Mass Intentions | Week of November 8, 2026''. It is a different
      publication from each Cohort 13 neighbour''s PDF bulletin.'
  - url: https://files.constantcontact.com/6512d43c001/1aa2d97e-3e96-48ad-8188-7213e02b7ca6.pdf
    seen: 2026-10-30
    quote: 'Pastor: Reverend Fr. Jeffrey E. Lee'
    note: 'Bulletin for St. Mary Parish (row st-mary-colts-neck), read by its map batch: Masthead, page
      1 of the 1 November 2026 issue (12 pages, text layer): ''THE PARISH OF SAINT MARY'', One Phalanx
      Road, Colts Neck, NJ 07722, Pastor Reverend Fr. Jeffrey E. Lee, Parish Trustees Linda Dickinson-Pancila
      and Tom Nathanson (the text layer reads "One Phalanz Road", a typo in the PDF). Names St. Mary alone.'
---

## Publisher

The Church of St. Catharine, Holmdel publishes its own weekly communication, the Constant Contact "Weekly Parish Update" (the 29 October 2026 issue: "Weekly Parish Update - October 29", with its Mass times and the Weekly Mass Intentions for the week of 1 November). It is an HTML email, not a PDF bulletin. Its pastor is Reverend Patrick McPartland, and the email names St. Catharine's alone, so it is not a shared bulletin with St. Mary, Colts Neck, though that parish's bulletin lists St. Catharine's Thursday-Saturday 9 AM Masses and this email lists St. Mary's Monday-Wednesday ones (the two parishes' weekday Masses alternate between the two churches).

## Worship sites

One church, 108 Middletown Rd, Holmdel (see `st-catharine-holmdel`). The Mass Schedule page lists Saturday 5:00 pm, Sunday 8:00 am, 10:00 am and 12:00 pm, and Thursday, Friday and Saturday 9:00 am "in the Church"; "The Chapel remains open for private prayer" and Confession is Saturdays 3:30-4:30 pm in the chapel, so the chapel is not a separate Mass site.

## Website and bulletin provider

The site is eCatholic (35015) but its Bulletin page holds no bulletin and the resolver fails (`fetch:check` 2026-10-30: "No matching anchor link found for ecatholic provider_id"). Its `/bulletins` archive is empty and no `files.ecatholic.com/35015/bulletins/` file turned up. The parish does publish a weekly bulletin, as that email (the 5 November 2026 issue, read 2026-11-07, carries the Mass times and the intentions for the week of 8 November), but no collector reads HTML emails. The row is therefore `unsupported` with a `fetch_gap` of kind `constant-contact-html-newsletter` and `bulletin_status: unsupported-format` (hand refresh, 2026-11-07; it was `no_bulletin` until then): it stays off the site (Settled policy 4) and `pnpm diocese gaps` lists it for the collector work. Its publication id is the email archive page. The Run's John Patrick scan (`tools/jppc-trenton.tsv`, ids 1-1300 and 6000-6110) has no listing with Holmdel's ZIP 07733; church-bulletin.org's own search page returned the same page for every query, so it was not usable as a check.

## Not yet confirmed

Whether St. Catharine's posts a PDF bulletin anywhere (a printed bulletin, a parish app, ParishSoft); the parish site's Mass page says "Please see weekly communications for holy day mass schedule", which suggests the email is the bulletin. See `research`.
