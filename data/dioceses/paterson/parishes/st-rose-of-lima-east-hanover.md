---
name: St. Rose of Lima
website: https://saintroseoflimachurch.org/
bulletin_provider: other
provider_id: page-pdfs https://saintroseoflimachurch.org/parish-bulletins
publication: ['ecatholic:11932']
group: ''
evidence:
- url: https://files.ecatholic.com/11932/documents/2026/10/October%2025%202026.pdf
  seen: 2026-11-04
  quote: BULLETIN October 25, 2026
  note: Page 1 text begins "312 Ridgedale Avenue / East Hanover, New Jersey 07936 / BULLETIN October 25,
    2026" and gives Mass times for All Saints (Saturday Oct 31 5:30 pm; Sunday Nov 1 7:30, 9:15, 10:30
    am, 12:15 and 7:00 pm) and All Souls (Monday Nov 2 9:00 am and 7:00 pm); page 2 thanks donors for
    "your weekly contribution to St. Rose!" and lists Mass intentions for 7:30, 9:15, 10:30, 12:15 and
    7:00 on Sunday and 9:00 weekdays. Six pages; names no other church.
- url: https://saintroseoflimachurch.org/parish-bulletins
  seen: 2026-11-04
  note: 'The parish''s eCatholic site (site id 11932, behind Cloudflare; read in headed Chrome with visit.py).
    Its Parish Bulletins page lists weekly PDFs in the eCatholic documents folder, newest first: "Parish
    Bulletin October 25, 2026" (files.ecatholic.com/11932/documents/2026/10/October%2025%202026.pdf),
    then October 18, 11, 4 and September 27. No 1 November issue was posted on 4 November.'
revisit: Check /parish-bulletins lists the 1 November 2026 issue and fetch:check picks it; on 5 November
  the newest was 25 October.
revisit_after: 2026-11-09
promoted: 2026-11-05
research:
- method: 'Reconcile fetch:check (page-pdfs on /parish-bulletins) and visit.py --links on the listing:
    newest link October 25 2026; probe get of documents/2026/10 and 2026/11 ''November 1 2026.pdf'' answered
    403'
  url: https://saintroseoflimachurch.org/parish-bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Rerun fetch:check and confirm it picks the 1 November or a later issue
  retry_when: On or after 2026-11-09, or when the listing shows a November issue
bulletin_status: available
---

## Publisher

St. Rose of Lima, East Hanover publishes its own weekly bulletin, posted to the eCatholic documents folder of its site (site id 11932) and listed on `https://saintroseoflimachurch.org/parish-bulletins`. The 25 October 2026 issue's page 1 reads "312 Ridgedale Avenue / East Hanover, New Jersey 07936 / BULLETIN October 25, 2026", with the All Saints and All Souls Mass times; page 2 lists Sunday Mass intentions at 7:30, 9:15, 10:30, 12:15 and 7:00 and weekdays at 9:00. The parish name on page 1 is in the artwork, not the text layer.

## Worship sites

- `st-rose-of-lima-east-hanover`: the only church in the schedule.

The diocese's finder (directory:11932) and GCatholic (18955) list this one church.

## Website and bulletin provider

The issues are not at the eCatholic `bulletins/<YYYYMMDD>.pdf` path (`issues.py ecatholic ecatholic:11932` got 403 for 18 Oct-8 Nov) but in `documents/<year>/<month>/<Month D YYYY>.pdf`. Provider `other` with the recipe `page-pdfs https://saintroseoflimachurch.org/parish-bulletins`; `fetch:check` on 2026-11-04 picked the 25 October 2026 issue ("page-pdfs on https://saintroseoflimachurch.org/parish-bulletins: first-listed, dated 2026-10-25", fresh, 10 days old), the newest one posted.

## Not yet confirmed

Nothing open. The 1 November issue was not yet posted on 4 November; the parish appears to post a few days late.
