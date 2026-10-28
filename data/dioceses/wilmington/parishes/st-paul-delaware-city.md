---
name: St. Paul
website: https://stpauldc.org/bulletins/
bulletin_provider: other
provider_id: dated-post https://stpauldc.org/bulletins/
publication: ['url:https://stpauldc.org/bulletins/']
group: New Castle Deanery
evidence:
- url: https://stpauldc.org/wp-content/uploads/2026/10/B102526.pdf
  seen: 2026-10-27
  quote: Saturday Oct. 24 - 5:00pm
  note: The 25 October 2026 bulletin is one page of St. Paul's own Mass intentions (Sat 5:00pm, Sun 9:00am,
    Mon/Tue/Fri 8:30am), a letter 'From the Pastor' signed 'Fr. Dave' about the St. Paul capital campaign
    and the St. Paul Parish Christmas Bazaar. The page names no other parish.
- url: https://stpauldc.org/bulletins/
  seen: 2026-10-27
  note: 'probe url (and the Chrome browser): HTTP 200, ''Bulletins – St. Paul Parish – Delaware City''.
    The page lists one dated WordPress post per week (October 25, 2026 -> https://stpauldc.org/october-25-2026/,
    category ''bulletin''), each wrapping a PDF (https://stpauldc.org/wp-content/uploads/2026/10/B102526.pdf).
    The heading says ''Please click on a date below to see a past bulletin:''. No PDF link is on the listing
    page itself.'
promoted: 2026-10-27
publication_reviews:
- parish: holy-spirit-st-peter-the-apostle-new-castle
  decision: separate
  evidence:
  - url: https://stpauldc.org/wp-content/uploads/2026/10/B102526.pdf
    seen: 2026-10-27
    quote: Saturday Oct. 24 - 5:00pm
    note: '25 October 2026 St. Paul issue: one page, own Mass intentions (Sat 5:00pm, Sun 9:00am) and
      Christmas bazaar notice, different publisher. Checked 2026-10-27: St. Paul''s one-page issue names
      St. Paul alone; the Holy Spirit / St. Peter masthead lists those two churches only, naming St. Paul
      only in a food-pantry partner strip (p.4).'
  - url: https://container.parishesonline.com/bulletins/03/1089/20261025B.pdf
    seen: 2026-10-27
    quote: Rev. Timothy M. Nolan, Pastor
    note: '25 October 2026 joint Holy Spirit / St. Peter issue: its own cover, Mass schedules for those
      two churches and pastor; its food-pantry strip names Our Lady of Fatima and St. Paul only as ministry
      partners.'
- parish: our-lady-of-fatima-new-castle
  decision: separate
  evidence:
  - url: https://stpauldc.org/wp-content/uploads/2026/10/B102526.pdf
    seen: 2026-10-27
    quote: Saturday Oct. 24 - 5:00pm
    note: '25 October 2026 St. Paul issue: one page, own Mass intentions (Sat 5:00pm, Sun 9:00am) and
      Christmas bazaar notice, different publisher. Checked 2026-10-27: St. Paul''s one-page issue names
      St. Paul alone and never names Fatima; Our Lady of Fatima''s masthead names Fatima alone and its
      text never names St. Paul.'
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-fatima-church-new-castle-de-19720/2026-10-25.pdf
    seen: 2026-10-27
    quote: Rev. David F. Murphy, Pastor
    note: '25 October 2026 Our Lady of Fatima issue: own masthead, Mass schedule (Sat 5PM and 7:30PM Spanish;
      Sun 9:30AM, Noon) and content.'
---

## Publisher

St. Paul, Delaware City, self-hosts its bulletin on stpauldc.org as weekly one-page PDFs under /wp-content/uploads/YYYY/MM/ (names like B102526.pdf = 25 October 2026). The /bulletins/ page lists one dated post per week (the newest is 'October 25, 2026'), and each post wraps that week's PDF. The 25 October issue is about St. Paul alone: its own Mass intentions, a pastor's letter and the parish Christmas bazaar.

## Worship sites

One church, 209 Washington Street, Delaware City. The diocese map and GCatholic agree on the address. GCatholic's website for it, stpaulsrcchurch.org, is an older domain that returned HTTP 5xx in the survey; the live site is stpauldc.org (the diocese map's http://www.stpauldc.org redirects there).

## Website and bulletin provider

`other`. A first pin of `page-pdfs https://stpauldc.org/bulletins/` failed (`NoBulletin: No PDF links found on bulletin page`) because the listing holds post links, not PDF links; the `dated-post` collector reads it. See *Fetch check*.

## Shared pastor?

The bulletin is signed 'Fr. Dave' and Our Lady of Fatima's pastor is Rev. David F. Murphy. No source read links them (no appointment in The Dialog posts of 2025-05-19, 2025-08-14, 2025-12-01 or 2026-04-27 names either), so this is only a possible shared pastor. The bulletins are separate in any case.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-paul-delaware-city` (2026-10-27) with the pinned `dated-post https://stpauldc.org/bulletins/` recipe: resolved `dated-post ... first-listed` to B102526.pdf, transport ok, document type PDF. The tool leaves identity 'unverified' (no expected identity supplied); the page-1 read above settles it. The pick is the newest listed issue, which the page lists first.
