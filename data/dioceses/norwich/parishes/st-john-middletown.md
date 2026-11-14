---
name: St. John
website: https://saintjohnmiddletownct.weebly.com/
bulletin_provider: parishes_online
provider_id: st-john-church
publication: ['po-org:st-john-church', 'lpi:0018000000Qc1P9AAJ', 'po-container:03/1513']
group: 'Yoked: St. John, St. Sebastian Middletown'
evidence:
- url: https://container.parishesonline.com/bulletins/03/1513/20261115B.pdf
  seen: 2026-11-14
  quote: 19 St. John Square * Middletown CT
  note: 'Page 1 masthead of the November 15, 2026 issue names SAINT JOHN CATHOLIC CHURCH, Established
    1843, pastor Rev. Gregory Galvin, with its own schedule: Saturday Vigil Mass 4:00 PM, Sunday Holy
    Mass 9:00 AM.'
- url: https://saintjohnmiddletownct.weebly.com/area-parish-bulletins.html
  seen: 2026-11-14
  note: The parish's Area Parish Bulletins page embeds the LPi widget id 0018000000Qc1P9AAJ ('Saint John
    - Middletown (See Below)') and links 'Saint Sebastian - Middletown' separately to parishesonline.com/organization/st-sebastian-st-john.
bulletin_status: available
publication_reviews:
- parish: st-sebastian-middletown
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1513/20261115B.pdf
    seen: 2026-11-14
    note: The November 15, 2026 masthead (page 1) names Saint John Catholic Church, 19 St. John Square,
      alone, with pastor Rev. Gregory Galvin and its own Mass times; the issue has no 'Sebastian' anywhere.
  - url: https://container.parishesonline.com/bulletins/03/0082/20261115B.pdf
    seen: 2026-11-14
    note: The November 15, 2026 masthead (page 1) of container 03/0082 names Saint Sebastian Catholic
      Church, 155 Washington Street, alone, with Rev. James Thaikoottathil as pastor; that issue has no
      'St. John' or 'Saint John'.
---

## Publisher

St. John, Middletown publishes its own LPi bulletin, ParishesOnline org `st-john-church` (container 03/1513, lpi:0018000000Qc1P9AAJ; `probe po` gives 19 Saint Johns Sq, Middletown). The November 15, 2026 issue (read 2026-11-14) has on page 1 "SAINT JOHN CATHOLIC CHURCH", "Established 1843", "St. John Rectory & Parish Office 19 St. John Square * Middletown CT" and "PASTOR: Rev. Gregory Galvin".

## Worship sites

The page 1 schedule lists Masses at the one parish only: Saturday Mass 8:30 AM, Saturday Vigil 4:00 PM, Sunday 9:00 AM, weekday Masses Tuesday and Thursday 7:30 AM "in the Chapel" and Friday 12:05 PM "in the Church". The chapel is given no address of its own and is taken to be the weekday chapel at the church (inferred; no separate site in any roster).

## Yoked with St. Sebastian: separate bulletins

The diocese's List of Parishes (March 6, 2026) yokes St. John and St. Sebastian under Rev. James Thaikoottathil. They publish separate bulletins: St. John in container 03/1513 and St. Sebastian in 03/0082 (org `st-sebastian-st-john`, whose name suggests a shared account, but its masthead names St. Sebastian alone). The November 15, 2026 issues have different mastheads, pastors (Galvin here, Thaikoottathil at St. Sebastian) and schedules, and neither names the other parish. St. John's own bulletin page embeds its widget and links St. Sebastian's org as another parish. Recorded as a `separate` review; the group is kept so audit sees the pair.

## Website and bulletin provider

The list's www.saintjohnmiddletownct.weebly.com fails TLS (`probe url` UNREACHABLE on 2026-11-14; the www. form is not covered by Weebly's certificate), but saintjohnmiddletownct.weebly.com without www works, and GCatholic's saintjohnchurchmiddletown.com redirects there. The masthead prints www.stjohnmiddletownct.weebly.com. fetch reads the bulletin by `provider_id`.

## Not yet confirmed

The pastor change: the bulletin names Rev. Gregory Galvin where the March 2026 list names Rev. James Thaikoottathil for both parishes, so the yoke may have ended. It doesn't change the rows.
