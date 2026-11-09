---
name: St. Benedict, Bronx
website: https://stbenedictchurchny.org/
bulletin_provider: parishes_online
provider_id: st-benedict-church-10465
publication: ['ecatholic:20621', 'po-org:st-benedict-church-10465', 'lpi:0018000000QxAJ1AAN', 'po-container:03/4035']
group: St. Benedict, Bronx
evidence:
- url: https://files.ecatholic.com/20621/bulletins/20261004.pdf?t=1790949558000
  seen: 2026-10-07
  quote: "St. Benedict’s Roman Catholic Church \n2969 Otis Avenue, Bronx, NY  10465  -  718-828-3403 \n\
    Bulletin: October 04, 2026   \n \nOCTOBER 2026 \nThe Month of the Rosary  \nThe Month of Missions\
    \  \nRespect Life Month  \n \nSunday:  October 4th  \n  Respect Life  \n \nWednesday:  October 7th\
    \  \n  The Feast of Our Lady  \n  of the Rosary  \n \nSunday  October 18th  \n  World Mission Sunday\
    \  \n \nMay Our Lady of the Rosary lead us to a \ngreat respect for human life! May the recita-\n\
    tion of the Rosary lead us closer to Christ! \nOur Lady of the Rosary Pray for Us! Amen!  \n===========================================-\
    \ \n \n  During the Month of                     \n  Octobe"
  note: Latest linked issue inspected October 7, 2026; publisher/masthead text, not an account name.
- url: https://files.ecatholic.com/20621/bulletins/20261004.pdf?t=1790949558000
  seen: 2026-10-07
  quote: "SUNDAY, October 4th; Twenty-seventh Sunday in  \nOrdinary Time   \n7:00 Joseph Doran \n8:00\
    \ Pasquale Del Vecchio  \n9:30 St. Benedict Parish \n11:00 A. Robert Terrero \n5:00 Stephen P. Pavlik\
    \ \nMONDAY, October 5th; Saint Faustina Kowalska; Blessed \nFrancis Xavier Seelos"
  note: Public Mass schedule/dated intentions in this issue.
- url: https://container.parishesonline.com/bulletins/03/4035/20261108B.pdf
  seen: 2026-11-09
  quote: NOVEMBER 08, 2026
  note: November 8, 2026 issue on ParishesOnline (container 03/4035, org st-benedict-church-10465); the
    masthead names St. Benedict's Roman Catholic Church, 2969 Otis Avenue, Bronx, with its Mass schedule.
    The parish's own eCatholic archive (ecatholic:20621) stopped at October 25.
promoted: 2026-10-08
research:
- method: 'Parish Bulletins page in headed Chrome (visit.py) and eCatholic dated paths: the page lists
    October 25, 2026 as newest (October 11, 18 and 25 uploaded together); files.ecatholic.com/20621/bulletins/20261101.pdf
    and 20261108.pdf answer 403'
  url: https://stbenedictchurchny.org/bulletins
  checked: '2026-11-09'
  outcome: not-found
  next_action: None while ParishesOnline is the channel; the eCatholic archive is kept as a fallback id
  retry_when: The ParishesOnline container stops receiving weekly issues
- method: 'ParishesOnline coordinates search API, then probe po st-benedict-church-10465: container 03/4035
    has weekly issues through November 8, 2026'
  url: https://parishesonline.com/organization/st-benedict-church-10465
  checked: '2026-11-09'
  outcome: found
  next_action: Switched the row to parishes_online by org slug; fetch:check picks the November 8 issue
---

## Publisher

The October 4, 2026 linked issue identifies St. Benedict, Bronx and supplies the quoted Mass schedule/dated intentions.

## Worship sites

The linked worship site [St. Benedict](../churches/st-benedict-bronx-16152.md) at 2969 Otis Ave. has affirmative public Mass evidence. 

## Website and bulletin provider

Since November 2026 the row reads ParishesOnline (org `st-benedict-church-10465`, container 03/4035), which had the November 1 and November 8 issues on 2026-11-09 while the parish's eCatholic archive (`ecatholic:20621`, linked from stbenedictchurchny.org/bulletins) ended at October 25, uploaded in batches, and its dated paths for November 1 and 8 answered 403. The November 8 container issue carries the St. Benedict's Roman Catholic Church, 2969 Otis Avenue masthead. The eCatholic id stays in `publication` as the parish's other channel.

## Not yet confirmed

If the ParishesOnline container stops receiving weekly issues, re-read the eCatholic archive at https://stbenedictchurchny.org/bulletins.
