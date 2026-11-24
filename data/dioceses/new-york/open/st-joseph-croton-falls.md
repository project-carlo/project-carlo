---
name: St. Joseph
revisit: Read the archived Catholic New York story 'All can come home to new church at St. Joseph's, Somers'
  (cny.org story 11271, now 404; try web.archive.org) for the planned sale of the former Croton Falls
  church, then look for the sale or reuse of the Croton Falls Road property (Town of North Salem records,
  local news). A sale or reuse makes this an exclusion (closed); a dated Mass there makes it a church
  under St. Joseph Somers.
revisit_after: 2026-12-01
roster: ['gcatholic:16482']
evidence:
- url: https://gcatholic.org/churches/usa-02/16482
  seen: 2026-10-07
  note: GCatholic identity/address and building-precise Plus Code; historical merger alone is not building
    closure.
- url: https://stjosephsomers.org/a-brief-history-of-st-josephs-parish
  seen: 2026-10-10
  quote: The day finally arrived in June of 2013.
  note: Actual primary HTML saved October 10 and reread October 11. History describes dedication of the
    new church at 95 Plum Brook Road, Somers, by Cardinals Dolan and Egan. It does not state the actual
    last Mass or present use of the old Croton Falls Road building.
- url: https://stjosephsomers.org/mass-times
  seen: 2026-10-11
  quote: 95 Plum Brook Road, Somers, NY 10589 (914) 232-2910
  note: Actual T3-rendered primary timetable read October 11 after HTTP 403. Saturday vigil 5 PM; Sunday
    8 AM, 10 AM, noon and 6 PM; weekdays 7:30 and 9 AM, Saturday 8 AM. No former-Croton-Falls-building
    attribution is supplied.
- url: https://www.church-bulletin.org/bulletin/saint-joseph-church-somers-ny-10589/2026-11-08.pdf
  seen: 2026-11-08
  note: 'Current 12-page St. Joseph, Somers issue: no mention of Croton Falls, the old church or Route
    22 (grep).'
- url: https://www.cny.org/stories/all-can-come-home-to-new-church-at-st-josephs-somers,11271
  seen: 2026-11-08
  note: 'Lead only: a web search snippet of this 2013 Catholic New York story says the former parish site,
    including the old church, rectory and school, would be sold, with the proceeds applied to the new
    church''s mortgage, and that the daily Mass chapel''s tabernacle and windows came from the Croton
    Falls church. The page now answers 404 and the quote could not be read; not used as evidence of closure.'
parish: st-joseph-somers
line1: Croton Falls Rd.
city: Croton Falls
state: NY
postal_code: '10519'
research:
- method: probe pdf --grep on the 8 November 2026 Somers bulletin (Croton Falls, old church, Route 22)
  url: https://www.church-bulletin.org/bulletin/saint-joseph-church-somers-ny-10589/2026-11-08.pdf
  checked: '2026-11-08'
  outcome: not-found
  next_action: None in the bulletin; settle the building's fate from the sale record
  retry_when: A Somers bulletin mentions Croton Falls
- method: probe get on the cny.org story (404) and its web.archive.org copy (HTTP 429)
  url: https://web.archive.org/web/2016/https://www.cny.org/stories/all-can-come-home-to-new-church-at-st-josephs-somers,11271
  checked: '2026-11-08'
  outcome: access-blocked
  next_action: Read the archived article and quote what it says about the old church
  retry_when: web.archive.org stops rate-limiting (retry after a day)
  revisit_after: 2026-12-01
---

## What is known

St. Joseph's parish moved from its old church on Croton Falls Road, Croton Falls, to a new church at 95 Plum Brook Road, Somers, dedicated in June 2013 (parish history page, read October 10). The [St. Joseph Somers](../parishes/st-joseph-somers.md) bulletin and Mass-times page give only the Somers church; the 8 November 2026 issue does not mention Croton Falls or the old church. A 2013 Catholic New York story, now 404 and seen only as a search snippet, reportedly said the former parish site, including the old church, was to be sold.

## Why it is not decided

No source read says the old church was sold, closed or relegated, or when its last Mass was; the planned sale is a plan. Nothing shows a Mass there now either. The next step is to read the archived Catholic New York story and find the property's sale or reuse.
