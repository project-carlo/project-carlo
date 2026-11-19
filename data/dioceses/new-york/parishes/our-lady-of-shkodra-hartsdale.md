---
name: Our Lady of Shkodra, Hartsdale
website: https://www.albchurch.org
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://www.albchurch.org/jeta']
group: ''
evidence:
- url: https://albchurch.org/2026
  seen: 2026-11-08
  quote: New issue soon.
  note: Jeta Katolike 2026 page, still with no issue; the site's year pages run 2000-2026, one magazine
    per year (the 2025 page embeds one Heyzine flipbook).
- url: https://www.albchurch.org/
  seen: 2026-11-08
  quote: SUNDAY MASS SCHEDULE
  note: 'Homepage Mass times: Sunday 10:00 AM and 12:00 PM Albanian; Monday-Saturday 1:00 PM Albanian.
    Links Jeta Katolike, Facebook and Flocknote; no bulletin link.'
- url: https://ourladyofshkodra.flocknote.com/home/api/mynotes
  seen: 2026-11-08
  note: 'Anonymous Flocknote feed: occasional notices only, newest 15 April 2026 (First Holy Communion
    rescheduled), then March 2026 and December 2025. No bulletin.'
revisit: Check albchurch.org and facebook.com/albanianchurch for a weekly bulletin or schedule post
revisit_after: 2027-02-01
research:
- method: headed browser on albchurch.org (homepage, /jeta, /2025, /2026)
  url: https://albchurch.org/2026
  checked: '2026-11-08'
  outcome: not-found
  next_action: Look again for a weekly bulletin link on albchurch.org
  retry_when: The homepage adds a Bulletin link, or the 2026 Jeta Katolike page changes
  revisit_after: 2027-02-01
- method: Flocknote notes feed API and issues.py ecatholic ecatholic:28834 (six Sundays)
  url: https://ourladyofshkodra.flocknote.com/home/api/mynotes
  checked: '2026-11-08'
  outcome: not-found
  next_action: None unless the feed starts carrying weekly notes
  retry_when: The parish site points to Flocknote for its bulletin
- method: Facebook page facebook.com/albanianchurch not read (login wall)
  url: https://www.facebook.com/albanianchurch
  checked: '2026-11-08'
  outcome: access-blocked
  next_action: Read the page's recent posts in a browser for a weekly bulletin or schedule
  retry_when: A browser session that can read public Facebook pages is available
bulletin_status: not-found
---

## Publisher

Our Lady of Shkodra, the Albanian Catholic parish in Hartsdale, has no weekly bulletin that could be found. Its site https://www.albchurch.org (eCatholic site 28834, read 8 November 2026) publishes Jeta Katolike, a yearly parish magazine: the site has one page per year from 2000 to 2026, the 2025 page embeds one Heyzine flipbook, and the 2026 page still says "New issue soon." (as it did on October 8). That is a yearly magazine, not a weekly schedule.

Other channels checked on 8 November: the parish Flocknote (ourladyofshkodra.flocknote.com) carries occasional notices, newest 15 April 2026 (First Communion), not a bulletin; the eCatholic file host has no `bulletins/` PDFs for site 28834 in the six Sundays to 8 November; Facebook (facebook.com/albanianchurch) was not read.

## Worship sites

[Our Lady of Shkodra](../churches/our-lady-of-shkodra-hartsdale.md), 361 West Hartsdale Avenue. The homepage's Mass times, read 8 November 2026: Sunday 10:00 AM and 12:00 PM (Albanian), Monday to Saturday 1:00 PM (Albanian).

## Website and bulletin provider

`no_bulletin` (Settled policy 4): the parish and its church stay in the records but off the site until a weekly bulletin turns up. This is not a statement that the parish has stopped publishing anything; its yearly magazine exists.

## Not yet confirmed

Whether the parish posts a weekly schedule on Facebook (Settled policy 1 would allow it if the bulletin itself is posted there).
