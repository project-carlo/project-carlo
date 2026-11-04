---
name: Our Lady of the Valley, Orange
website: https://olvsalesianchurch.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:20387']
group: Planning Area H
evidence:
- url: https://files.ecatholic.com/20387/bulletins/20261011.pdf
  seen: 2026-11-04
  quote: OUR LADY OF THE VALLEY CHURCH  OCTOBER 11, 2026
  note: '11 October 2026 issue (3 pages, text layer), the newest posted on 4 November. Page 1 gives 510
    Valley Street Orange, NJ 07050, olvsalesianchurch.org, ''CONDUCTED BY: Salesians of St. John Bosco'',
    and one schedule (THE EUCHARIST/MISAS) with no other church. No printer''s footer: the parish makes
    it itself.'
- url: https://olvsalesianchurch.org/bulletins
  seen: 2026-11-04
  note: 'visit.py (probe url got HTTP 403, eCatholic behind Cloudflare): the bulletin archive (ecatholic:20387)
    lists October 11, 2026, October 4, September 27, September 20, September 13 … as files.ecatholic.com/20387/bulletins/<yyyymmdd>.pdf.
    The 4 October and 27 September files carry upload stamps from the same day, so the parish posts in
    batches.'
research:
- method: visit.py on the eCatholic bulletin archive; probe get on files.ecatholic.com/20387/bulletins/20261018,
    20261025 and 20261101.pdf (403, Cloudflare, so inconclusive)
  url: https://olvsalesianchurch.org/bulletins
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reread the archive and check that issues after 11 October 2026 have been posted; if posting
    has stopped, look for another place the parish posts its bulletin (Flocknote, Facebook)
  retry_when: fetch:check reports this row stale, or on the revisit date
  revisit_after: 2026-12-01
bulletin_status: available
---

## Publisher

The parish makes its own bulletin and posts it on its eCatholic site (20387). I read the 11 October 2026 issue, the newest posted on 4 November: its pages are headed 'OUR LADY OF THE VALLEY CHURCH  OCTOBER 11, 2026', and page 1 gives 510 Valley Street Orange, NJ 07050, olvsalesianchurch.org, the Salesian pastor Rev. Dieunel Victor, S.D.B., and one schedule: Saturday 5:30 pm (English) and 7:00 pm (Español); Sunday 9:00 and 10:30 am (English), 7:00 am and 12:00 pm (Español); weekdays 9 am and 7 pm. No printer's footer appears.

## Worship sites

One church, `our-lady-of-the-valley-orange`: the schedule names no other place. The directory (164) and GCatholic (18529) list only this church. The issue doesn't mention Our Lady of Mount Carmel or St. John, Orange ('St. John Bosco' is the Salesians' founder).

## Website and bulletin provider

The website is the parish's eCatholic site (Cloudflare answers probe url with 403; the browser reads it), provider `ecatholic`. GCatholic's olvchurchorange.org is an older address. The parish posts irregularly: on 4 November the newest issue was 11 October, and two earlier issues were uploaded together. fetch:check (2026-11-04) picks that 11 October issue and reports it stale (24 days).

## Not yet confirmed

- Whether issues after 11 October 2026 will be posted: see `research`, from 2026-12-01.
