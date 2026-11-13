---
name: Stony Brook Catholic Campus Ministry Sunday Mass (Student Union Ballroom, Stony Brook University)
reason: no-bulletin
line1: Stony Brook Union, Stony Brook University
city: Stony Brook
state: NY
postal_code: '11794'
decided: 2026-11-13
roster: []
evidence:
- url: https://www.sbucatholic.org/
  seen: 2026-11-13
  quote: We celebrate Mass every Sunday during the academic year in the Stony Brook Student Union Ballroom.
  note: Stony Brook Catholic Campus Ministry home page; it 'serves every member of the University community,
    students, faculty, and staff'. No bulletin or newsletter PDF is linked from the home page.
- url: https://www.drvc.org/mass-times/
  seen: 2026-11-12
  note: 'The diocese''s Mass-times entry for St. James, Setauket (mass-times:church-of-st-james-setauket)
    ends: ''5:00 PM Stony Brook University during the academic year''.'
- url: https://container.parishesonline.com/bulletins/03/0634/20261115B.pdf
  seen: 2026-11-13
  note: St. James's 15 November 2026 bulletin Mass schedule (page 1, image, read rendered) lists only
    the parish church; no Stony Brook University Mass.
parish: st-james-setauket
revisit: Check sbucatholic.org for a bulletin or newsletter the pipeline could read.
revisit_after: 2027-05-01
research:
- method: probe get on sbucatholic.org home page; DuckDuckGo search for the campus ministry
  url: https://www.sbucatholic.org/
  checked: '2026-11-13'
  outcome: not-found
  next_action: Look on sbucatholic.org's 'more info' Mass page and its newsletter/Instagram for a posted
    bulletin, and confirm the Mass is open to non-students
  retry_when: Next audit of this diocese, or a bulletin or newsletter appears on sbucatholic.org
  revisit_after: 2027-05-01
---

## Why it is excluded

Stony Brook Catholic Campus Ministry says (home page, read 2026-11-13): "We celebrate Mass every Sunday during the academic year in the Stony Brook Student Union Ballroom." The diocese's Mass-times page lists it under St. James, Setauket as "5:00 PM Stony Brook University during the academic year". St. James's own 15 November 2026 bulletin does not carry it, and the campus ministry links no bulletin, so this regular Mass has nothing the pipeline can read: `no-bulletin`. It is a multipurpose ballroom used for Mass in term time, not a church; no roster lists it as a place. The address is the Student Union on the Stony Brook University campus (zip 11794 is the university's; street address not checked).

## What would change this

A bulletin or newsletter posted by the campus ministry, or St. James's bulletin adding the campus Mass to its schedule, would make it a church row (of St. James, or of its own publisher row).
