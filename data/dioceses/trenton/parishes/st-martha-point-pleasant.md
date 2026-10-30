---
name: The Church of St. Martha
website: https://saintmartha.net/
bulletin_provider: other
provider_id: page-pdfs https://saintmartha.net/bulletin/
publication: ['url:https://saintmartha.net/bulletin/#st-martha']
group: Cohort 20 (Point Pleasant, Brick)
evidence:
- url: https://saintmartha.net/wp-content/uploads/2026/10/Bulletin-11-1-2026.pdf
  seen: 2026-10-30
  quote: THE CATHOLIC COMMUNITY OF SAINT MARTHA
  note: 'Page 1 of the 1 November 2026 (All Saints) issue, 8 pages with a text layer. Masthead names St.
    Martha alone: ''Pastor: Rev. David Swantek'', Mass ''Saturday Vigil 4:30 pm; Sunday 7:30 am, 10:00
    am, 12:00 noon; Daily Mass: Tuesday - Friday 9:00 am'', 3800 Herbertsville Road, Point Pleasant, NJ
    08742.'
- url: https://saintmartha.net/bulletin/
  seen: 2026-10-30
  quote: Week of November 1st – All Saints
  note: The parish's WordPress Bulletin page lists one entry, 'Bulletin 11-1-2026 Download', linking the
    PDF above (wp-content/uploads/2026/10/Bulletin-11-1-2026.pdf).
- url: https://saintmartha.net/wp-content/uploads/2026/10/Bulletin-11-1-2026.pdf
  seen: 2026-10-30
  quote: 'St. Martha''s & St. Peter''s: Weekend of December 5 & 6 (all Masses)'
  note: 'Page 2: the St. Vincent de Paul wreath-sale notice names Sacred Heart, St. Martha''s and St.
    Peter''s as sale venues. It shows cooperation among cohort parishes, not a shared bulletin; the bulletin''s
    own Mass schedule lists St. Martha only.'
research:
- method: pnpm fetch:check --diocese trenton --parish st-martha-point-pleasant (headed Chrome); page-pdfs
    on the Bulletin page
  url: https://saintmartha.net/bulletin/
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: transport ok, document_type pdf, picks Bulletin-11-1-2026.pdf (''current''; freshness
    ''future'', the coming Sunday''s issue posted two days early).'
bulletin_status: available
---

## Publisher

The Church of St. Martha, Point Pleasant Borough publishes its own weekly bulletin on its WordPress site (saintmartha.net/bulletin/), one PDF per week under `wp-content/uploads/<yyyy>/<mm>/`. The 1 November 2026 issue (read 2026-10-30; page 1) is headed 'THE CATHOLIC COMMUNITY OF SAINT MARTHA', names Rev. David Swantek as pastor and gives the parish's own Mass schedule: Saturday vigil 4:30 pm; Sunday 7:30 am, 10:00 am and 12:00 noon; weekdays Tuesday-Friday 9:00 am. It names no other parish.

## Worship sites

One: St. Martha Church, 3800 Herbertsville Road (see `st-martha-point-pleasant`). A grep of the issue for 'Chapel' finds nothing, and its Mass schedule lists no other building. The other two Cohort 20 parishes (Epiphany, Brick; St. Peter, Point Pleasant Beach) publish their own bulletins with their own mastheads (see `epiphany-brick`, `st-peter-point-pleasant-beach`), so the cohort is three rows. The John Patrick listing 522 ('Saint Martha Church', Point Pleasant NJ 08742, in `tools/jppc-trenton.tsv`) has no edition, so it is a dead listing, not a second channel.

## Website and bulletin provider

Provider `other`: the parish's own site. The directory's saintmartha.net redirects (`probe url`) to https://saintmartha.net/, whose Bulletin page carries the PDFs. See `research` for the fetch check.

## Not yet confirmed

Nothing outstanding.
