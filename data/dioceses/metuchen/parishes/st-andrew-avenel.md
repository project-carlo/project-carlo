---
name: St. Andrew
website: https://www.standrewparish.com
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:22662', 'po-container:04/1116']
group: ''
evidence:
- url: https://files.ecatholic.com/22662/bulletins/20261025.pdf
  seen: 2026-11-02
  quote: St. Andrew Church, Avenel NJ
  note: 'Page 1 of the 25 October 2026 issue (6 pages, text, LPi layout): ''St. Andrew Church, Avenel
    NJ'', ''MASS SCHEDULE SATURDAY VIGIL: 4:00PM SUNDAY: 8:00AM, 10:00AM & 11:30AM'', parish website www.standrewparish.com,
    phone 732-634-4355, ''Facebook: Frdavidkosmoski''; weekday Mass intentions at 8:00 AM Monday to Friday.
    The last page''s LPi code line reads ''St. Andrew Church | 04-1116''. No other church is named.'
- url: https://container.parishesonline.com/bulletins/04/1116/20261101B.pdf
  seen: 2026-11-02
  quote: St. Andrew Church, Avenel NJ
  note: 'ParishesOnline container 04/1116 (the LPi code on the eCatholic copy): the 1 November 2026 issue,
    6 pages, same masthead and Mass schedule. Its 25 October issue (20261025B.pdf) has pdftotext output
    identical to the eCatholic 25 October file, so the two are one publication.'
- url: https://www.standrewparish.com/bulletins
  seen: 2026-11-02
  quote: October 25, 2026
  note: eCatholic site 22662 (loaded with visit.py; probe url said DEAD-DNS and probe get 403). Bulletin
    page lists files.ecatholic.com/22662/bulletins/<YYYYMMDD>.pdf; newest 25 October 2026 on 2026-11-02
    (the 1 November issue was not yet posted there). Upload stamps show issues posted in batches (4, 11
    October and 27 September all stamped 10 October).
revisit: Check whether the eCatholic Bulletin page is still behind ParishesOnline container 04/1116; if
  so, switch the row to parishes_online with the org slug.
revisit_after: 2026-11-16
bulletin_status: available
---

## Publisher

St. Andrew, Avenel publishes its own weekly bulletin, laid out by LPi. The parish posts it on its eCatholic site (22662), and LPi carries the same file in ParishesOnline container 04/1116. The 25 October 2026 eCatholic issue (read 2026-11-02) is headed 'St. Andrew Church, Avenel NJ' with its Mass schedule and names no other church. Its masthead names no pastor; it gives 'Facebook: Frdavidkosmoski' and closes 'Happy Sunday, Fr. David', which fits the finder's 'Pastor: Rev. David B. Kosmoski'.

## Worship sites

One church, 244 Avenel Street (directory:24465, gcatholic:18634). Saturday Vigil 4:00 pm, Sunday 8:00, 10:00 and 11:30 am, weekdays 8:00 am, all at St. Andrew.

## Website and bulletin provider

Website https://www.standrewparish.com (finder, GCatholic and the masthead agree), eCatholic site 22662. Under the diocese's rule for a bulletin carried both on the parish's eCatholic site and in a ParishesOnline container, this is one publication recorded on the parish-hosted copy: provider `ecatholic`, with `ecatholic:22662` and `po-container:04/1116` both listed. I compared the two 25 October 2026 files with `pdftotext`: identical. No ParishesOnline org slug or LPi id was looked up. The eCatholic page lags the container: on 2026-11-02 it had 25 October as its newest issue while the container already had 1 November, and its upload stamps show issues posted several at a time. If `fetch` keeps picking a stale issue, switching the row to `parishes_online` would be the fix (see *Not yet confirmed*).

## Fetch check

`pnpm fetch:check` on 2026-11-02 picked https://files.ecatholic.com/22662/bulletins/20261025.pdf (the 25 October 2026 issue, the newest the eCatholic page had): transport ok, PDF, issue date inferred from the file name, freshness fresh (8 days, within the 14-day limit), identity unverified by the tool; I read that issue myself (evidence above). It is a week behind the container's 1 November issue.

## Not yet confirmed

Whether the eCatholic page keeps up. Check again after 2026-11-16: if the eCatholic Bulletin page is still more than a week behind container 04/1116, find the ParishesOnline org slug (`probe po`) and record the row as `parishes_online`.
