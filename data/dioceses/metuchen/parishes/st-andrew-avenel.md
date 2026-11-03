---
name: St. Andrew
website: https://www.standrewparish.com
bulletin_provider: parishes_online
provider_id: st-andrew-church-07001
publication: ['ecatholic:22662', 'po-org:st-andrew-church-07001', 'lpi:0018000000Qc09rAAB', 'po-container:04/1116']
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
- url: https://parishesonline.com/organization/st-andrew-church-07001
  seen: 2026-11-03
  quote: St. Andrew Church
  note: 'ParishesOnline org st-andrew-church-07001 (probe po, 2026-11-03): 244 Avenel St, Avenel, LPi
    id 0018000000Qc09rAAB, container 04/1116; latest listed issue 1 November 2026, and 20261108B.pdf (6.3
    MB) already downloads. The same day files.ecatholic.com/22662/bulletins/20261101.pdf and 20261108.pdf
    answered 403, so the eCatholic page was still at 25 October.'
promoted: 2026-11-03
research:
- method: pnpm fetch:check --parish st-andrew-avenel after switching to parishes_online
  url: https://container.parishesonline.com/bulletins/04/1116/20261101B.pdf
  checked: '2026-11-03'
  outcome: found
bulletin_status: available
---

## Publisher

St. Andrew, Avenel publishes its own weekly bulletin, laid out by LPi. The parish posts it on its eCatholic site (22662), and LPi carries the same file in ParishesOnline container 04/1116. The 25 October 2026 eCatholic issue (read 2026-11-02) is headed 'St. Andrew Church, Avenel NJ' with its Mass schedule and names no other church. Its masthead names no pastor; it gives 'Facebook: Frdavidkosmoski' and closes 'Happy Sunday, Fr. David', which fits the finder's 'Pastor: Rev. David B. Kosmoski'.

## Worship sites

One church, 244 Avenel Street (directory:24465, gcatholic:18634). Saturday Vigil 4:00 pm, Sunday 8:00, 10:00 and 11:30 am, weekdays 8:00 am, all at St. Andrew.

## Website and bulletin provider

Website https://www.standrewparish.com (finder, GCatholic and the masthead agree), eCatholic site 22662. Under the diocese's rule for a bulletin carried both on the parish's eCatholic site and in a ParishesOnline container, this is one publication recorded on the parish-hosted copy: provider `ecatholic`, with `ecatholic:22662` and `po-container:04/1116` both listed. I compared the two 25 October 2026 files with `pdftotext`: identical. No ParishesOnline org slug or LPi id was looked up. The eCatholic page lags the container: on 2026-11-02 it had 25 October as its newest issue while the container already had 1 November, and its upload stamps show issues posted several at a time. On 2026-11-03 (reconcile) the gap had grown to two issues: container 04/1116 had 1 and 8 November, while eCatholic 22662 still had 25 October as its newest. So the row now reads the container: provider `parishes_online`, org `st-andrew-church-07001` (`probe po`, 2026-11-03, address 244 Avenel St), with every id of the one publication listed (`ecatholic:22662`, `po-org`, `lpi`, `po-container:04/1116`). The 1 November container issue's page 1 reads 'St. Andrew Church, Avenel NJ' with the same Mass schedule.

## Fetch check

`pnpm fetch:check` on 2026-11-02 and again in the reconcile run on 2026-11-03 picked the eCatholic 25 October 2026 issue (fresh at 8–9 days, but a week behind the container). After the switch to `parishes_online`, see the fetch check recorded in `research`.

## Not yet confirmed

Nothing structural. If the parish stops sending its bulletin to LPi (the container goes silent while eCatholic keeps posting), switch back to `ecatholic`.
