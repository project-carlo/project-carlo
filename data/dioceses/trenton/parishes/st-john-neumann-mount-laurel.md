---
name: St. John Neumann Roman Catholic Church
website: https://www.sjnmtl.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:2914', 'url:https://www.church-bulletin.org/saint-john-neumann-roman-catholic-church-mt-laurel-nj-08054']
group: Cohort 26 (Moorestown, Mount Laurel, Marlton)
evidence:
- url: https://files.ecatholic.com/2914/bulletins/20261101.pdf
  seen: 2026-10-30
  quote: 560 WALTON AVE., MT. LAUREL, NJ 08054
  note: 'The eCatholic issue dated 1 November 2026 (10 pages, text layer; md5 4671b2a3802925bddc66b5f8e417e639):
    ''St. John Neumann Roman Catholic Church'', ''Pastor - Rev. Fr. Michael Dunn'', ''1 November 2026
    - Solemnity of All Saints''. Page 2 ''Weekly Liturgical Schedule'': Monday 9:00am, Wednesday 7:00pm,
    Thursday 9:00am, Friday 9:00am (Tuesday no Masses), Saturday 4:00pm, Sunday 8:00am and 10:00am. It
    names this parish alone.'
- url: https://www.church-bulletin.org/bulletin/saint-john-neumann-roman-catholic-church-mt-laurel-nj-08054/2026-11-01.pdf
  seen: 2026-10-30
  note: The John Patrick listing's 2026-11-01.pdf (listing 6000; 12 pages, image-only, md5 f7fc68fdd7702f1f7640319204ca4508)
    is a different file of the same issue; rendered pages 1-2 show the same masthead, pastor, address
    and Mass schedule as the eCatholic PDF.
- url: https://www.sjnmtl.org/bulletins
  seen: 2026-10-30
  note: The parish's own eCatholic site (id 2914; plain fetch answers 403, read in the browser). Its Bulletins
    page links files.ecatholic.com/2914/bulletins/20261101.pdf and 20261025.pdf.
research:
- method: pnpm fetch:check --diocese trenton --parish st-john-neumann-mount-laurel (headed Chrome)
  url: https://www.sjnmtl.org/bulletins
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
publication_reviews:
- parish: st-isaac-jogues-marlton
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/2914/bulletins/20261101.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. John Neumann: its masthead names St. John
      Neumann Roman Catholic Church alone at 560 Walton Ave. with Rev. Fr. Michael Dunn, Pastor, and gives
      Masses Sat 4:00pm and Sun 8:00 and 10:00am. St. Isaac Jogues'' bulletin has a different pastor (Rev.
      James Smith), address, staff and Mass times, and comes from separate listings (6000 and 637) and
      eCatholic sites (2914 and 13541).'
---

## Publisher

St. John Neumann (Mount Laurel) publishes its own weekly bulletin. The same 1 November 2026 issue is on its own eCatholic site (2914), with a text layer, and on John Patrick Publishing's listing 6000 on church-bulletin.org as a different, image-only file. The cover names Rev. Fr. Michael Dunn as pastor and the page 2 schedule gives one set of Masses.

## Linkage with St. Isaac Jogues

The 2017 decisions linked St. Isaac Jogues and St. John Neumann under one pastor, but the current bulletins show different pastors (Fr. Dunn here, Rev. James Smith at St. Isaac Jogues), different staff and different Mass times, and each has its own listing and eCatholic site. Separate rows (see `publication_reviews`).

## Worship sites

One church, 560 Walton Ave. (see `st-john-neumann-mount-laurel`). Page 2 also gives 'Our Lady of Sorrows Adoration Chapel' hours (Mon-Thu 9:45am-4:00pm, Fri 9:45am-1:00pm); it is adoration, no Mass is listed there, and the parish offices are 'attached to the main church building', so it is not a second church. The Monday-Friday Masses carry devotions to Our Lady of the Miraculous Medal, St. Padre Pio and St. Monica, Our Lady of Perpetual Help and St. John Neumann, not other places.

## Website and bulletin provider

The directory's and GCatholic's site (sjnmtl.org) is an eCatholic site (id 2914) whose Bulletins page links the newest issue, 1 November, the same Sunday as the John Patrick listing, so the row reads eCatholic (text layer) and keeps the listing in `publication`. The homepage also embeds ecatholic:15175, not identified here (diocese.md lists 15175 as one of St. Benedict's two ids), so it is not recorded.
