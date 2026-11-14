---
name: Our Lady of Fatima
website: https://olfpw.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://olfpw.org/bulletin#fatima-focus']
group: ''
evidence:
- url: https://olfpw.org/bulletin/580-november-15-2026-thirty-third-sunday-in-ordinary-time/file
  seen: 2026-11-13
  quote: Our Lady of Fatima Parish Community
  note: 'Issue for November 15, 2026 (12 pages, Creator Canva; downloaded with browser_get.py). Masthead
    ''Fatima Focus, Our Lady of Fatima Parish Community, 6 Cottonwood Road - Manorhaven, New York 11050'';
    Mass: Saturday 5:00 PM, Sunday 8:00 AM, 10:00 AM, 12:00 PM (Spanish), Monday-Friday 8:00 AM; Rev.
    Msgr. Robert J. Clerkin, Pastor.'
- url: https://olfpw.org/bulletin
  seen: 2026-11-13
  note: Solutio (Joomla) bulletin list (read with visit.py; probe url got 403) links issues newest first,
    from 580-november-15-2026 back through August 2026, each as a /file PDF.
research:
- method: fetch:check on the Solutio bulletin list (provider other, unpinned)
  url: https://olfpw.org/bulletin
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Re-run fetch:check once a collector downloads Joomla /file PDFs through the browser
  retry_when: A joomla-file-endpoint collector lands
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: Solutio (Joomla) bulletin list links each issue as /bulletin/<n>-<date-title>/file; those PDFs
    answer 403 to probe get and fetch:check answered resolve_failed (its browser scrape of the /file URLs
    timed out). Chrome downloads them (browser_get.py). Canva-made, no printer listing.
  url: https://olfpw.org/bulletin/580-november-15-2026-thirty-third-sunday-in-ordinary-time/file
publication_reviews:
- parish: st-peter-of-alcantara-port-washington
  decision: separate
  evidence:
  - url: https://olfpw.org/bulletin/580-november-15-2026-thirty-third-sunday-in-ordinary-time/file
    seen: 2026-11-13
    note: The November 15, 2026 masthead names Our Lady of Fatima Parish Community, 6 Cottonwood Road,
      Manorhaven alone ('Fatima Focus'), with its own Mass schedule; pastor Msgr. Robert J. Clerkin.
  - url: https://flipbook.so/flip/ztexS2pcMP1b5jODqlXk
    seen: 2026-11-13
    note: The November 8, 2026 masthead names the Parish of St. Peter of Alcántara, 1327 Port Washington
      Blvd. alone, with its own Mass schedule and the same pastor; printed by The Church Bulletin Inc.
---

## Publisher

Our Lady of Fatima, Manorhaven publishes its own weekly bulletin, "Fatima Focus", made in Canva and posted on its Solutio site. The November 15, 2026 issue (`https://olfpw.org/bulletin/580-november-15-2026-thirty-third-sunday-in-ordinary-time/file`, 12 pages, read 2026-11-13) has the masthead "Fatima Focus, Our Lady of Fatima Parish Community, 6 Cottonwood Road - Manorhaven, New York 11050" and "Mass at Our Lady of Fatima Parish": Saturday 5:00 PM; Sunday 8:00 AM, 10:00 AM, 12:00 PM (Spanish); Monday-Friday 8:00 AM. Staff: "Rev. Msgr. Robert J. Clerkin, Pastor", Deacon John J. Hogan.

Msgr. Clerkin is also pastor of St. Peter of Alcantara, Port Washington (the bulletin says Thanksgiving Day's Mass is "an 8:30 morning Mass up at St. Peter's"), but each parish publishes its own bulletin with its own masthead and printer, so they are separate rows (see publication_reviews).

## Worship sites

One: the church at 6 Cottonwood Road (`our-lady-of-fatima-manorhaven-church`). The bulletin's schedule names no other place. The diocesan locator (directory:15), GCatholic (16878) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

The locator's and GCatholic's link ourladyoffatimapw.org redirects to olfpw.org (the Mass-times page's fatimafocus.org was not checked). It is a Solutio (Joomla) site, 403 to `probe url`, fine in `visit.py`. Its `/bulletin` list links issues newest first as `/bulletin/<n>-<date-title>/file`; those PDFs answer 403 to `probe get` and download with Chrome (`browser_get.py`). The PDF is Canva-made, so there is no printer listing (ParishesOnline, John Patrick) to use instead. `fetch:check` (2026-11-13, provider `other`, unpinned) answered `resolve_failed`. Following the diocese's Solutio rule, the row is `unsupported` with fetch_gap `joomla-file-endpoint`.

## Not yet confirmed

Nothing open.
