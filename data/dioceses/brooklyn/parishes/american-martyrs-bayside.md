---
name: American Martyrs (Bayside)
website: https://www.amparish.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:25157']
group: Deanery Q5 (Queens East)
evidence:
- url: https://files.ecatholic.com/25157/bulletins/20261101.pdf
  seen: 2026-11-05
  quote: AMERICAN MARTYRS PARISH
  note: '1 November 2026 issue, 11 pages. Page 1 masthead: ''AMERICAN MARTYRS PARISH'', ''ROMAN CATHOLIC
    CHURCH • BAYSIDE, NEW YORK'', Rev. Sean M. Suckiel, Pastor; WEEKEND MASSES Vigil Saturday 4:00pm,
    Sunday 9:00am & 11:30am; weekday Monday-Saturday 8:30am. The footer gives contact boxes for both Holy
    Family Parish (Fresh Meadows) and American Martyrs Parish (79-43 Bell Boulevard).'
- url: https://files.ecatholic.com/25157/bulletins/20261101.pdf
  seen: 2026-11-05
  quote: American Martyrs Weekly Offering
  note: 'Page 2: American Martyrs'' own collection, attendance 625. Page 4 prints ''Our New Combined Mass
    Schedule'' with Holy Family''s times too.'
- url: https://www.amparish.org/
  seen: 2026-11-05
  note: 'probe url answers 403; visit.py renders ''American Martyrs RC Church - New York, NY'', ''Login
    powered by eCatholic'', publication ecatholic:25157, linking /bulletins. issues.py: 20261101.pdf 200,
    20261108.pdf 403 (not yet posted).'
- url: https://parishesonline.com/organization/american-martyrs-church-11364
  seen: 2026-11-05
  note: 'probe po: org ''American Martyrs Church'' (lpi 0018000000QxB8LAAV) has no issues; it is an empty
    org, not this bulletin''s publication id.'
revisit: Check whether American Martyrs and Holy Family have moved to one bulletin (masthead naming both)
revisit_after: 2027-02-01
publication_reviews:
- parish: holy-family-fresh-meadows
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/25157/bulletins/20261101.pdf
    seen: 2026-11-05
    note: The 1 November 2026 masthead names American Martyrs Parish, Bayside, with its own Mass times
      (Vigil 4:00pm, Sunday 9:00am and 11:30am) and its own weekly offering and attendance (625), in a
      separate 11-page eCatholic issue.
  - url: https://container.parishesonline.com/bulletins/04/0458/20261101B.pdf
    seen: 2026-11-05
    note: The 1 November 2026 masthead names Holy Family Roman Catholic Church, Fresh Meadows alone, with
      its own Mass times and its own weekly offering and attendance (916).
---

## Publisher

American Martyrs publishes its own weekly eCatholic bulletin (site id 25157, `files.ecatholic.com/25157/bulletins/<YYYYMMDD>.pdf`). The 1 November 2026 issue (read 2026-11-05) has on page 1 "AMERICAN MARTYRS PARISH", "ROMAN CATHOLIC CHURCH • BAYSIDE, NEW YORK", Rev. Sean M. Suckiel, Pastor, and page 2 its own "American Martyrs Weekly Offering".

## Worship sites

One church. Page 1 gives Vigil Saturday 4:00pm, Sunday 9:00am and 11:30am, Monday-Saturday 8:30am; page 4's combined schedule gives the same times for American Martyrs, "located at the 79-43 Bell Blvd." The diocese directory, deanery list, GCatholic 16592 and Mass finder 1110 list only this church.

Fr. Suckiel is also pastor of Holy Family, Fresh Meadows; both bulletins print one combined Mass schedule and both parishes' contact boxes. Holy Family still publishes its own LPi bulletin with its own masthead and collection (row `holy-family-fresh-meadows`), recorded as a `separate` review.

## Website and bulletin provider

`ecatholic`. amparish.org (the directory's link) is the eCatholic-hosted site; it answers 403 to `probe url` but renders in the browser. The ParishesOnline org `american-martyrs-church-11364` exists but has no issues and is not recorded as a publication.

## Not yet confirmed

The combined Mass schedule may precede a single bulletin for the two parishes; if a later masthead names Holy Family too, merge the rows.
