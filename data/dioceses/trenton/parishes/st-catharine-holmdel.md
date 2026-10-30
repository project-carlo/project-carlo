---
name: Church of St. Catharine
website: https://www.stcatharine.net/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
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
bulletin_status: unsupported-format
---

## Publisher

The Church of St. Catharine, Holmdel publishes its own weekly communication, the Constant Contact "Weekly Parish Update" (the 29 October 2026 issue: "Weekly Parish Update - October 29", with its Mass times and the Weekly Mass Intentions for the week of 1 November). It is an HTML email, not a PDF bulletin. Its pastor is Reverend Patrick McPartland, and the email names St. Catharine's alone, so it is not a shared bulletin with St. Mary, Colts Neck, though that parish's bulletin lists St. Catharine's Thursday-Saturday 9 AM Masses and this email lists St. Mary's Monday-Wednesday ones (the two parishes' weekday Masses alternate between the two churches).

## Worship sites

One church, 108 Middletown Rd, Holmdel (see `st-catharine-holmdel`). The Mass Schedule page lists Saturday 5:00 pm, Sunday 8:00 am, 10:00 am and 12:00 pm, and Thursday, Friday and Saturday 9:00 am "in the Church"; "The Chapel remains open for private prayer" and Confession is Saturdays 3:30-4:30 pm in the chapel, so the chapel is not a separate Mass site.

## Website and bulletin provider

The site is eCatholic (35015) but its Bulletin page holds no bulletin and the resolver fails (`fetch:check` 2026-10-30: "No matching anchor link found for ecatholic provider_id"). Its `/bulletins` archive is empty and no `files.ecatholic.com/35015/bulletins/` file turned up. The row is therefore `no_bulletin` (Settled policy 4: open, with public Mass, but nothing the pipeline could read), with `bulletin_status: unsupported-format` because the parish does publish a weekly email. The Run's John Patrick scan (`tools/jppc-trenton.tsv`, ids 1-1300 and 6000-6110) has no listing with Holmdel's ZIP 07733; church-bulletin.org's own search page returned the same page for every query, so it was not usable as a check.

## Not yet confirmed

Whether St. Catharine's posts a PDF bulletin anywhere (a printed bulletin, a parish app, ParishSoft); the parish site's Mass page says "Please see weekly communications for holy day mass schedule", which suggests the email is the bulletin. See `research`.
