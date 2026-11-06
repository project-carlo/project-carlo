---
name: Holy Name of Jesus, East Orange
website: https://www.hnjeo.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:holy-name-of-jesus-church-07017', 'lpi:0018000000QxA9nAAF']
group: ''
evidence:
- url: https://www.hnjeo.org/
  seen: 2026-11-04
  quote: 'Sunday: 9:00 AM and 11:30 AM'
  note: The homepage's 'Weekly Bulletin' link points to https://www.hnjeo.org/wp-content/uploads/2025/12/Dec-21.pdf,
    the newest PDF on the site; it also gives Saturday 5:30 PM and weekdays 8:00 AM in church.
- url: https://www.hnjeo.org/wp-content/uploads/2025/12/Dec-21.pdf
  seen: 2026-11-04
  quote: 184 Midland Avenue, East Orange, New Jersey 07017
  note: A two-page self-made bulletin, masthead 'CHURCH OF THE HOLY NAME OF JESUS', for 21 December 2025.
    No printer's footer.
- url: https://www.hnjeo.org/wp-json/wp/v2/media?mime_type=application/pdf&per_page=20
  seen: 2026-11-04
  note: 'The WordPress media list shows bulletin PDFs uploaded irregularly: 2025-12-21, 2025-04-17, 2025-03-22,
    2024-12-14, 2024-11-24, 2024-04-21 ... nothing in 2026.'
- url: https://parishesonline.com/organization/holy-name-of-jesus-church-07017
  seen: 2026-11-04
  note: 'probe po: org ''Holy Name of Jesus Church'', 246 Dodd Street, East Orange, website hnjeo.org,
    lpi 0018000000QxA9nAAF, no publications (''this organization does not publish a bulletin here now'').'
revisit: Reread https://www.hnjeo.org/wp-json/wp/v2/media?mime_type=application/pdf for a bulletin uploaded
  in 2026 (the last was the Christmas 2025 issue); if posting turns weekly, set provider other and run
  fetch:check.
revisit_after: 2027-01-04
research:
- method: WordPress media list and homepage 'Weekly Bulletin' link
  url: https://www.hnjeo.org/wp-json/wp/v2/media?mime_type=application/pdf&per_page=20
  checked: '2026-11-04'
  outcome: not-found
  next_action: Reread the media list for a 2026 bulletin upload; if uploads become weekly, record provider
    other with page-pdfs on the homepage and run fetch:check
  retry_when: The homepage's Weekly Bulletin link points to a 2026 issue
  revisit_after: 2027-01-04
- method: probe po on the ParishesOnline org; John Patrick scans (029-map jp-*.tsv) grepped for East Orange
    and 07017
  url: https://parishesonline.com/organization/holy-name-of-jesus-church-07017
  checked: '2026-11-04'
  outcome: not-found
  next_action: Recheck only if a bulletin names a publisher
  retry_when: A Holy Name bulletin carries a printer's footer
bulletin_status: not-found
---

## Publisher

The parish makes its own short bulletin and posts it to its WordPress site only now and then. The homepage's "Weekly Bulletin" link on 4 November 2026 pointed to `Dec-21.pdf`, a two-page issue of 21 December 2025 with the masthead "CHURCH OF THE HOLY NAME OF JESUS … 184 Midland Avenue, East Orange, New Jersey 07017" and no printer's footer. The site's media list shows bulletin PDFs uploaded on 2025-12-21, 2025-04-17, 2025-03-22, 2024-12-14, 2024-11-24 and earlier: a few a year, none in 2026. The ParishesOnline org holy-name-of-jesus-church-07017 exists with no publications, and no John Patrick listing in the Run's scans names East Orange or 07017.

## Worship sites

One church, `holy-name-of-jesus-east-orange`. The homepage's schedule (Saturday 5:30 PM, Sunday 9:00 AM and 11:30 AM, weekdays 8:00 AM "in Church") names no other place; the directory (26) and GCatholic (18381) each list only this church.

## Website and bulletin provider

The website is the parish's own https://www.hnjeo.org/. The provider is `no_bulletin`: the newest posted issue is ten months old, so no recipe would give a current schedule (Settled policy 4 keeps the row off the site). No fetch check was run, since there is no current bulletin to check. The ParishesOnline ids are kept in `publication` because they are this parish's account.

## Not yet confirmed

- Whether the parish will post 2026 issues (last year it posted the Christmas issue): see `revisit` and `research`, from 2027-01-04.
