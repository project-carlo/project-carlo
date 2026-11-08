---
name: Chapel of the Immaculate Conception, Seton Hall University
reason: no-bulletin
line1: 400 South Orange Avenue
city: South Orange
state: NJ
postal_code: 07079
decided: 2026-11-04
roster: ['gcatholic:40399']
evidence:
- url: https://www.shu.edu/catholic-mission/mass-schedule.html
  seen: 2026-11-04
  quote: All Masses and Confessions are celebrated in our historic University Chapel of the
  note: 'Seton Hall''s ''Catholic Mass at Seton Hall'' page: ''All really are welcome here…come just as
    you are.'' Regular schedule Monday-Friday 8 a.m., 12 p.m. and 5 p.m.; Saturday 12 p.m.; Sunday 10
    a.m., 6 p.m., 8 p.m. and 10 p.m.; winter/summer break Monday-Friday 12 p.m., Sunday 10 a.m. and 6
    p.m.'
- url: https://church-bulletin.org/673
  seen: 2026-11-04
  note: 'Redirects to church-bulletin.org/seton-hall-university-campus-ministry-south-orange-nj-07079,
    ''Seton Hall University Campus Ministry Bulletin'': a John Patrick listing with no issues, only the
    readings for the week of November 1, 2026.'
- url: https://blogs.shu.edu/chapel/
  seen: 2026-11-04
  note: 'The chapel''s history site (read with quick_snap.py): Welcome, History, Interior, Windows, Restoration,
    Acknowledgements, Contact Us; no schedule or bulletin.'
- url: https://gcatholic.org/churches/usa-03/40399
  seen: 2026-11-03
  quote: 400 S Orange Ave., South Orange, New Jersey 07079
  note: GCatholic 'Immaculate Conception' (Seton Hall University, Immaculate Conception Seminary), Plus
    Code 87G7PQR2+JP.
parish: our-lady-of-sorrows-south-orange
revisit: Check church-bulletin.org/673 for issues; if Seton Hall Campus Ministry posts a bulletin, make
  it a parish row with a church at 400 South Orange Avenue (campus rule in diocese.md Rules settled).
revisit_after: 2027-02-01
---

## Why it is excluded

Seton Hall's University Chapel of the Immaculate Conception (400 South Orange Avenue) holds Mass. The university's 'Catholic Mass at Seton Hall' page (read 2026-11-04) gives Monday-Friday 8 a.m., 12 p.m. and 5 p.m., Saturday 12 p.m., and Sunday 10 a.m., 6, 8 and 10 p.m. (fewer during breaks), says 'All Masses and Confessions are celebrated in our historic University Chapel of the Immaculate Conception', and 'All really are welcome here…come just as you are.' The schedule is public with no restriction to students, so I judged the Mass public; under the campus rule (diocese.md *Rules settled*) the chapel would be a church row. But no bulletin covers it: John Patrick's 'Seton Hall University Campus Ministry' listing (id 673) has no issues, only the week's readings; the chapel's own site (blogs.shu.edu/chapel) is a history site; and Our Lady of Sorrows' 1 November 2026 bulletin gives only its own church's schedule. A campus ministry is a parish row only when it posts its own bulletin, so the chapel is excluded as `no-bulletin`: open with public Mass, nothing the pipeline can read. The `parish` field names Our Lady of Sorrows as the neighbouring parish the roster pairs it with, not a bulletin that covers it.

## What would change this

Issues on church-bulletin.org/673: then a parish row for Seton Hall Campus Ministry with provider `other`, `page-pdfs https://church-bulletin.org/673`, and a church row at 400 South Orange Avenue. Revisit 2027-02-01, at the start of the spring semester.
