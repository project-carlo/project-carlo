---
name: St. Theodore
website: https://sttheodorenj.org/bulletins
bulletin_provider: other
provider_id: ''
publication: ['url:https://sttheodorenj.org/bulletins']
group: ''
evidence:
- url: https://storage.googleapis.com/production-sitebuilder-v1-0-9/209/781209/ACJ3WL1E/f0198800e5c04753bb2f5786d92addb7?fileName=11.01.26%20web.pdf
  seen: 2026-11-03
  quote: Saint Theodore Roman Catholic Church
  note: '1 November 2026 issue, 4 pages, text layer. Page 1 masthead names Saint Theodore Roman Catholic
    Church alone: ''Post Office Box 146, 855 Route 57, Port Murray, New Jersey 07865'', ''Father Damian
    Tomiczek, SDS'', Holy Sacrifice of the Mass Saturday 5:00 PM, Sunday 8:00 AM and 10:30 AM, weekdays
    Monday through Wednesday and Friday 8:45 AM.'
- url: https://storage.googleapis.com/production-sitebuilder-v1-0-9/209/781209/ACJ3WL1E/f0198800e5c04753bb2f5786d92addb7?fileName=11.01.26%20web.pdf
  seen: 2026-11-03
  quote: 060E (JA) - St. Theodore, Port Murray, NJ
  note: 'Page 4 ad-page code line: Bon Venture Services prints the bulletin (account 060E); the parish
    posts it on its own site.'
- url: https://sttheodorenj.org/bulletins
  seen: 2026-11-03
  quote: All Saints Day
  note: The parish's GoDaddy site-builder Bulletins page lists issues newest first (November 1, 2026;
    October 25, 2026; ...), each linking storage.googleapis.com/production-sitebuilder-v1-0-9/209/781209/...
    PDFs named like '11.01.26 web.pdf'.
- url: https://diometuchen.org/parishfinder
  seen: 2026-10-30
  note: 'The finder lists St. Theodore, 855 Route 57, Port Murray, NJ 07865, mailing P. O. Box 146, website
    http://www.sttheodorenj.com (which answered HTTP 502 on 2026-11-03), ''Administrator: Rev. Damian
    Tomiczek SDS''.'
research:
- method: DuckDuckGo search (visit.py) for sponsors.bonventure.net and St. Theodore, Port Murray
  checked: '2026-11-03'
  outcome: not-found
  next_action: Scan Bon Venture listing ids with tools/bonventure_scan.sh for 'Port Murray' if the parish
    site stops posting issues
  retry_when: The parish Bulletins page stops posting current issues
bulletin_status: available
fetch_gap:
  kind: filename-date-misread
  seen: 2026-11-03
  url: https://sttheodorenj.org/bulletins
  note: GoDaddy site-builder page; each PDF is storage.googleapis.com/production-sitebuilder-v1-0-9/209/781209/ACJ3WL1E/<hash>?fileName=<name>.
    page-pdfs reads the list (newest first, '11.01.26 web.pdf' for 1 November 2026) but parses an archived
    'Nov 7.21.pdf' (7 November 2021) as 7 November 2026 and picks it as current. A filename= glob can't
    exclude it, since the recipe matches the hash path, not the fileName query.
---

## Publisher

Bon Venture Services prints the bulletin (page 4 code line "060E (JA) - St. Theodore, Port Murray, NJ") and the parish posts each issue on its own Bulletins page. The 1 November 2026 issue (4 pages, text layer) has the masthead on page 1: "Saint Theodore Roman Catholic Church", Post Office Box 146, 855 Route 57, Port Murray, New Jersey 07865, "Father Damian Tomiczek, SDS", Masses Saturday 5:00 PM, Sunday 8:00 AM and 10:30 AM, Monday-Wednesday and Friday 8:45 AM. No other parish or church is named. A DuckDuckGo search on 2026-11-03 found no `sponsors.bonventure.net` listing for the parish, so only the parish-hosted copy is known.

## Worship sites

One church, 855 Route 57 (directory:24532, gcatholic:18689). The masthead's Mass schedule names no other place.

## Website and bulletin provider

`other`, website https://sttheodorenj.org/bulletins, a GoDaddy site-builder page listing issues newest first as storage.googleapis.com PDFs whose names sit in a `fileName=` query ("11.01.26 web.pdf"). The finder's and GCatholic's domain `sttheodorenj.com` answered HTTP 502 on 2026-11-03; the live `sttheodorenj.org`, found by search, is the one the masthead prints ("Web ... www.sttheodorenj.org"), and ParishesOnline's dormant org `st-theodore-church-07865` (LPi id 0018000000QxA2pAAF, no publications) also gives it. `probe url` reported DEAD-DNS, but `probe get` and the browser loaded it.

`fetch:check` (2026-11-03) with `page-pdfs` on the Bulletins page picked an archived "Nov 7.21.pdf" (7 November 2021), whose name it reads as 7 November 2026; no `filename=` glob can exclude it because the recipe matches the hashed path. No recipe is recorded, and `fetch_gap` `filename-date-misread` holds the problem.

## Not yet confirmed

Nothing about the bulletin itself; the fetch gap stays until a collector reads the newest-first order or the fileName query.
