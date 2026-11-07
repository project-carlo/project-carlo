---
name: St. Mary Parish
website: https://www.stmaryscoltsneck.org/
bulletin_provider: unsupported
provider_id: page-pdfs https://www.stmaryscoltsneck.org/past-bulletins
publication: ['url:https://www.stmaryscoltsneck.org/bulletins-1', 'url:https://www.stmaryscoltsneck.org/past-bulletins']
group: Cohort 13 (Marlboro, Colts Neck, Holmdel, Lincroft)
evidence:
- url: https://files.constantcontact.com/6512d43c001/1aa2d97e-3e96-48ad-8188-7213e02b7ca6.pdf
  seen: 2026-10-30
  quote: 'Pastor: Reverend Fr. Jeffrey E. Lee'
  note: 'Masthead, page 1 of the 1 November 2026 issue (12 pages, text layer): ''THE PARISH OF SAINT MARY'',
    One Phalanx Road, Colts Neck, NJ 07722, Pastor Reverend Fr. Jeffrey E. Lee, Parish Trustees Linda
    Dickinson-Pancila and Tom Nathanson (the text layer reads "One Phalanz Road", a typo in the PDF).
    Names St. Mary alone.'
- url: https://files.constantcontact.com/6512d43c001/1aa2d97e-3e96-48ad-8188-7213e02b7ca6.pdf
  seen: 2026-10-30
  quote: AT ST. CATHARINE , HOLMDEL
  note: Page 2 'MASS SCHEDULE & INTENTIONS, Saturday 31 October - Sunday 8 November' (read from a render).
    Monday-Wednesday 9 AM have no location; Thursday 5 and Friday 6 November 9 AM and Saturday 7 November
    9 AM are 'AT ST. CATHARINE, HOLMDEL'; Saturday 4 PM and Sunday 8 AM, 10 AM, 12 PM have no location.
    Page 2 also headings 'THE CHAPEL LAMP BURNS FOR:'.
- url: https://www.stmaryscoltsneck.org/bulletins-1
  seen: 2026-10-30
  quote: click here for a printable PDF
  note: 'The parish''s ''Current Bulletin'' page (an eCatholic page, hand-edited) holds five Constant
    Contact PDF links in no date order and with stale ones left in: the first link is the 4 October 2026
    issue (ae8fbfa8), the visible ''click here for a printable PDF'' link is the 18 October issue (bcdaeb63),
    and the 1 November issue (1aa2d97e) appears only as raw link text.'
- url: https://www.stmaryscoltsneck.org/past-bulletins
  seen: 2026-10-30
  quote: October 25, 2026 bulletin
  note: 'The ''Past Bulletins'' page lists dated links newest first (25 October, 20, 13 and 6 September,
    30 August ...). Its first dated link, https://files.constantcontact.com/6512d43c001/51c737bf-c2ec-4a44-b348-2e69ace27468.pdf,
    is labelled 25 October but its page-1 masthead reads ''Pastor: Reverend Fr. Jeffrey E. Lee ... November
    1, 2026 Solemnity of All Saints'' (a second copy of the 1 November issue).'
research:
- method: fetch:check with page-pdfs on /bulletins-1 and on /past-bulletins
  url: https://www.stmaryscoltsneck.org/past-bulletins
  checked: '2026-10-30'
  outcome: found
  next_action: Re-run fetch:check after the 8 and 15 November 2026 issues to confirm the pick is the current
    issue
  retry_when: Two more weekly issues have been posted
  revisit_after: 2026-11-16
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese trenton, then probe
    get on /bulletins-1 and /past-bulletins and probe pdf --grep 2026 on each linked issue (hand refresh
    against main)
  url: https://www.stmaryscoltsneck.org/bulletins-1
  checked: '2026-11-07'
  outcome: unsupported-format
  next_action: Set bulletin_provider back to other once a collector can pick the newest undated issue
    on these pages (for example by reading each PDF's cover date), run fetch:check, and clear fetch_gap
    when it picks this week's issue.
  retry_when: A collector for fetch_gap kind first-pdf-not-current exists, or the parish lists this week's
    issue first on one page
bulletin_status: available
fetch_gap:
  kind: first-pdf-not-current
  seen: 2026-11-07
  note: Issues are undated Constant Contact PDFs (files.constantcontact.com/6512d43c001/<uuid>.pdf). On
    2026-11-07 the hand-edited 'Current Bulletin' page (/bulletins-1) had the 8 November issue (06f6a4f6...)
    but lists the 1 November one (1aa2d97e...) first, and the dated 'Past Bulletins' page only reaches
    1 November, so the pinned page-pdfs on /past-bulletins picked the 1 November issue (fetch:check) a
    week behind. Neither page puts this week's issue first.
  url: https://files.constantcontact.com/6512d43c001/06f6a4f6-f48a-4126-895f-70fab93a23ec.pdf
---

## Publisher

St. Mary, Colts Neck publishes its own weekly bulletin, posted as Constant Contact-hosted PDFs on the parish site. The 1 November 2026 issue's masthead (page 1) reads "THE PARISH OF SAINT MARY, One Phalanx Road, Colts Neck, NJ 07722" with Pastor Reverend Fr. Jeffrey E. Lee. St. Catharine's pastor is Reverend Patrick McPartland (stcatharine.net/staff, read 2026-10-30), and St. Catharine and St. Gabriel each publish their own bulletin or weekly email with their own masthead, so this is a single-parish row.

## Worship sites

One church, 1 Phalanx Rd, Colts Neck (see `st-mary-colts-neck`); the bulletin mentions a church and a chapel on the site ("The Lamp burns for seven days in the church and chapel"). The Mass schedule on page 2 lists the Thursday 5 and Friday 6 November and Saturday 7 November 9 AM Masses "AT ST. CATHARINE, HOLMDEL": St. Mary's bulletin carries those intentions, but they are Masses at St. Catharine's church, which has its own row (`st-catharine-holmdel`) and its own Mass schedule (Thursday, Friday, Saturday 9:00 am in the Church, stcatharine.net/mass-and-confession-schedule). I did not add St. Catharine as a St. Mary church.

## Website and bulletin provider

The site is eCatholic (33474) but has no files.ecatholic.com/33474/bulletins/ issues (six Sundays and the Friday and Saturday names returned 403, eCatholic's answer for a missing file). The PDFs are on Constant Contact (files.constantcontact.com/6512d43c001/<uuid>.pdf). The row is `other`, pinned to `page-pdfs https://www.stmaryscoltsneck.org/past-bulletins`. `fetch:check` on 2026-10-30 against /bulletins-1 chose its first link (the 4 October issue, `first-listed`, 26 days old, failed freshness) because that hand-edited page keeps old links first. Against /past-bulletins it chose `51c737bf...` ("current"), whose masthead reads 1 November 2026 under a link label of 25 October. That pick was right on 2026-10-30, but it relied on the page's newest dated link carrying the current issue.

It didn't hold. On 2026-11-07 (hand refresh) the 8 November issue (`06f6a4f6...`, cover "November 8, 2026") was on /bulletins-1, listed after the 1 November one, while /past-bulletins reached only "November 1, 2026 bulletin". `fetch:check` on the pinned recipe picked the 1 November issue, a week behind, and a recipe on /bulletins-1 would pick its first link, the same 1 November file. So no recipe collects this week's issue: the row is `unsupported` with a `fetch_gap` of kind `first-pdf-not-current`, kept in the records with its publication ids and left off the site until a collector can choose the newest of these undated PDFs. The `provider_id` keeps the /past-bulletins recipe for that day.

## Not yet confirmed

Nothing beyond the fetch gap: the masthead, pastor and Mass schedule above are read. See `research` and `fetch_gap`.
