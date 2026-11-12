---
name: St. Michael (Sunset Park)
website: https://www.stmichaelssunsetpark.com/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:19776']
group: Deanery B8 (Brooklyn West)
evidence:
- url: https://files.ecatholic.com/19776/bulletins/20261004.pdf
  seen: 2026-11-06
  quote: 352 42nd Street, Brooklyn, NY 11232
  note: '4 October 2026 issue, 7 pages. Page 1 (masthead title is artwork): saintmichaelbrooklyn@gmail.com,
    www.stmichaelssunsetpark.com, 352 42nd Street, Pastor Very Rev. Fulgencio Gutiérrez, and St. Michael''s
    own Mass schedule; every page header reads ''St. Michael''s R.C. Church''.'
- url: https://files.ecatholic.com/19776/bulletins/20261004.pdf
  seen: 2026-11-06
  quote: The parishes of St. Michael and St. Agatha will
  note: Page 6 joint notice; page 3 prints St. Michael's Mass intentions and then a list headed St. Agatha's
    Mass Intentions.
- url: https://www.stmichaelssunsetpark.com/bulletins
  seen: 2026-11-06
  note: 'probe url answers 403; visit.py renders ''St. Michael''s R.C Church'' with publication ecatholic:19776.
    The /bulletins archive lists October 4, 2026 newest, then weekly back to July 5; the file timestamps
    (?t=) show July 5 posted 2026-07-06 and July 12 to October 4 all posted 2026-10-05. issues.py ecatholic:
    20261011 to 20261108 answer 403 (not posted).'
- url: https://parishesonline.com/organization/st-michael-roman-catholic-church-11232
  seen: 2026-11-06
  note: 'probe po: org ''St. Michael Roman Catholic Church'', website stmichaelssunsetpark.com, has no
    issues; an empty org, not a publication id.'
revisit: Check that the eCatholic archive has issues after 4 October 2026, and whether the LPi org st-michael-roman-catholic-church-11232
  has started publishing
revisit_after: 2026-12-01
research:
- method: issues.py ecatholic ecatholic:19776 --weeks 6 and the /bulletins archive via visit.py
  url: https://www.stmichaelssunsetpark.com/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Re-run issues.py ecatholic ecatholic:19776 and probe po st-michael-roman-catholic-church-11232;
    if eCatholic is still months behind and the LPi org has issues, switch to parishes_online
  retry_when: After 2026-12-01, or when the archive posts an issue after 4 October 2026
  revisit_after: 2026-12-01
- method: 'Reconcile: headed fetch:check of every Brooklyn row still picked the issue dated 2026-10-04;
    nothing newer is posted'
  url: https://files.ecatholic.com/19776/bulletins/20261004.pdf?t=1791228758000
  checked: '2026-11-12'
  outcome: not-found
  next_action: 'As the earlier research item: look for a newer issue or another channel at the revisit'
  retry_when: At this record's revisit_after, or when a newer issue is posted
bulletin_status: available
publication_reviews:
- parish: st-agatha-sunset-park
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/19776/bulletins/20261004.pdf
    seen: 2026-11-06
    note: The 4 October 2026 masthead names St. Michael's R.C. Church, 352 42nd Street, alone, with its
      own Mass schedule (Sunday 7:00 AM and 10:00 AM Spanish, 12:00 PM English), in a separate eCatholic
      issue.
  - url: https://container.parishesonline.com/bulletins/03/9993/20261108B.pdf
    seen: 2026-11-06
    note: The 8 November 2026 masthead names St. Agatha's R.C. Church, 702 48th St., alone, with St. Agatha's
      own Mass schedule, in its own LPi issue; St. Michael appears there only in the intentions column
      and the Thanksgiving Mass notice.
---

## Publisher

St. Michael publishes its own bulletin on eCatholic (site id 19776, `files.ecatholic.com/19776/bulletins/<YYYYMMDD>.pdf`). The newest issue, 4 October 2026 (read 2026-11-06), gives on page 1 352 42nd Street, Brooklyn, NY 11232, www.stmichaelssunsetpark.com and Very Rev. Fulgencio Gutiérrez as pastor, and heads each page "St. Michael's R.C. Church".

Fr. Gutierrez is also pastor of St. Agatha, Sunset Park. The two parishes print each other's Mass intentions and joint notices (page 6: "The parishes of St. Michael and St. Agatha will be CLOSED on Tuesday, October 12"), but St. Agatha publishes its own LPi issue with its own masthead and schedule (row `st-agatha-sunset-park`), so the rows are separate; recorded as a `separate` review.

## Worship sites

One church, St. Michael, 352 42nd Street. Page 1's schedule gives only this church's Masses and names no other place. The diocese directory, GCatholic 16755 and Mass finder 1157 list only this church. The deanery page's B8 list gives "St. Michael-St. Malachy" (East New York) instead of this parish (batch note, 2026-11-06); that is another parish.

## Website and bulletin provider

`ecatholic`. stmichaelssunsetpark.com, the directory's link, is the eCatholic site; it answers 403 to `probe url` and renders in the browser.

The parish posts in batches: the archive's timestamps show 5 July posted 6 July, then 12 July to 4 October all posted on 5 October. On 2026-11-06 the newest issue was 4 October, so `fetch` picks an issue about a month old until the next batch. A ParishesOnline org for the parish (`st-michael-roman-catholic-church-11232`) exists with no issues; St. Agatha's LPi container began on 4 October, so St. Michael may follow. See research.

## Not yet confirmed

Whether issues after 4 October 2026 get posted on eCatholic, or move to LPi; recheck after 2026-12-01. Whether St. Michael and St. Agatha move to one bulletin: if a later masthead names both, merge the rows.
