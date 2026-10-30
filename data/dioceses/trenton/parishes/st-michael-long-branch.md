---
name: St. Michael's Church
website: https://www.stmichaelnj.com/
bulletin_provider: other
provider_id: page-pdfs https://www.stmichaelnj.com/sunday-bulletins filename=bulletin*.pdf
publication: ['url:https://www.stmichaelnj.com/sunday-bulletins']
group: Cohort 17 (Long Branch, West Long Branch)
evidence:
- url: https://www.stmichaelnj.com/images/bulletins/bulletin102526.pdf
  seen: 2026-10-30
  quote: 'Saturday: 4:00PM, 5:30PM, 7:00 PM Sunday: 7:00'
  note: 'Page 1 of the 25 October 2026 issue (7 pages; the cover is an image, read from a render): masthead
    ''St. Michael''s Church'', ''Parish Office 800 Ocean Avenue | Long Branch, NJ 07740'', ''Rev. John
    K. Butler, Pastor''. Text layer: weekend Masses ''Saturday: 4:00PM, 5:30PM, 7:00 PM Sunday: 7:00 AM,
    8:30AM, 10:00AM, 12:00 PM, 4:00 PM, 7:00 PM''; daily ''Mon - Sat: 8:00 AM | Mon: 7:00 PM''. Page 2
    Mass intentions for the week. Names the church alone.'
- url: https://www.stmichaelnj.com/sunday-bulletins
  seen: 2026-10-30
  quote: Sunday Bulletins 2026
  note: 'Parish site''s Sunday Bulletins page: /images/bulletins/bulletin<mmddyy>.pdf links, newest first,
    25 October 2026 at the top (the 1 November file, bulletin110126.pdf, returned 404 on 2026-10-30).
    No 27 September issue is listed.'
- url: https://www.church-bulletin.org/saint-michael-church-trenton-nj-08638
  seen: 2026-10-30
  note: 'No John Patrick listing for this parish: tools/jppc-trenton.tsv and the jsonl scans hold no Long
    Branch 07740 entry except 539 (Christ the King); the ''Saint Michael'' listings are Trenton (530,
    no edition), Gibbstown (550) and Union (622).'
- url: https://dioceseoftrenton.org/parishfinder
  seen: 2026-10-30
  note: Finder pin directory:14622 'St. Michael Church', 800 Ocean Ave, Long Branch 07740-9001, (732)
    222-8080, website stmichaelnj.com.
research:
- method: fetch:check on the row (page-pdfs on /sunday-bulletins, filename=bulletin*.pdf), 25 October
    2026 issue
  url: https://www.stmichaelnj.com/images/bulletins/bulletin102526.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: the pick is the newest file on the page (25 October); issue date is ''unknown''
    to fetch:check because the masthead prints it as an image, but the cover read from a render shows
    ''October 25, 2026''. Check that bulletin110126.pdf (404 on 2026-10-30) appears after 1 November.'
bulletin_status: available
---

## Publisher

St. Michael's (West End, Long Branch; Cohort 17) publishes its own bulletin as dated PDFs on its own site, stmichaelnj.com/sunday-bulletins. The 25 October 2026 issue's cover names 'St. Michael's Church, 800 Ocean Avenue' with Rev. John K. Butler as pastor, a Mass schedule of its own and a Mass-intentions page for its church only. It does not name Christ the King or Our Lady of Hope, which have their own bulletins.

## Worship sites

One church, 800 Ocean Ave (`st-michael-long-branch`). GCatholic and the finder carry the same address once each.

## Website and bulletin provider

Self-hosted `/images/bulletins/bulletin<mmddyy>.pdf` files on a Joomla page. The page also links unrelated PDFs (a registration form, a USCCB statement), so the recipe pins `filename=bulletin*.pdf`. The site is a week behind the calendar (the 1 November file did not exist on 2026-10-30). GCatholic's stmichaels-westend.com does not resolve (DNS, 2026-10-30).

## Not yet confirmed

Nothing open beyond the fetch check noted in `research`.
