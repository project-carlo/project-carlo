---
name: St. Columba (Marine Park)
website: http://www.saintcolumbabrooklyn.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:st-columba-church-11234', 'lpi:0018000000QxB83AAF']
group: Deanery B11 (Brooklyn East)
evidence:
- url: http://www.saintcolumbabrooklyn.org/bulletin.pdf
  seen: 2026-11-06
  quote: DECEMBER 7, 2025
  note: 'The site''s only bulletin file (linked as bulletin.pdf from the links.htm frame of the frameset
    homepage), 6 pages; page 2 is dated DECEMBER 7, 2025. Page 1 masthead: Saint Columba, A Roman Catholic
    Parish, Diocese of Brooklyn, 2245 Kimball Street, Brooklyn, New York 11234-5154; Rev. Timothy J. Lambert,
    Pastor; Masses Saturdays 5 PM, Sundays 11:30 AM, weekdays Monday, Tuesday, Wednesday & Friday 9 AM.
    No LPi or Church Bulletin Inc. footer found by grep.'
- url: https://parishesonline.com/organization/st-columba-church-11234
  seen: 2026-11-06
  note: 'probe po: org St. Columba Church, 2245 Kimball St, Brooklyn, New York, 11234, lpi 0018000000QxB83AAF,
    website saintcolumbabrooklyn.org, no issues and no container.'
- url: https://discovermass.com/church/st-columba-brooklyn-ny/
  seen: 2026-11-06
  quote: There are currently no bulletins available for St. Columba.
  note: 'Discover Mass listing, 2245 Kimball St., Brooklyn, NY 11234: no bulletins.'
- url: https://www.facebook.com/StColumbaBrooklyn
  seen: 2026-11-06
  note: 'Facebook page ''Saint Columba RC Church, Diocese of Brooklyn'' (visit.py, logged out): its intro
    links saintcolumbabrooklyn.org/bulletin.pdf, the same stale file; no other bulletin channel shown.'
revisit: Reread http://www.saintcolumbabrooklyn.org/bulletin.pdf (the site's one fixed bulletin file)
  and probe po st-columba-church-11234; if either carries a current issue, set the provider (other with
  page-pdfs http://www.saintcolumbabrooklyn.org/links.htm, or parishes_online) and run fetch:check.
revisit_after: 2026-12-07
research:
- method: probe url / probe get on the frameset homepage and links.htm; probe pdf on bulletin.pdf; fetch:check
    with page-pdfs http://www.saintcolumbabrooklyn.org/links.htm (resolves and downloads bulletin.pdf,
    freshness unknown)
  url: http://www.saintcolumbabrooklyn.org/bulletin.pdf
  checked: '2026-11-06'
  outcome: not-found
  next_action: Reread bulletin.pdf's date; if current, set bulletin_provider other with provider_id 'page-pdfs
    http://www.saintcolumbabrooklyn.org/links.htm' and run fetch:check
  retry_when: After 2026-12-07, or when the parish site links a new bulletin
  revisit_after: 2026-12-07
- method: probe po st-columba-church-11234 and saint-columba-church-11234; Discover Mass listing; Facebook
    page via visit.py
  url: https://parishesonline.com/organization/st-columba-church-11234
  checked: '2026-11-06'
  outcome: not-found
  next_action: probe po st-columba-church-11234 for issues; if a container appears, set parishes_online
    with that org slug
  retry_when: After 2026-12-07 or when the LPi org shows issues
  revisit_after: 2026-12-07
bulletin_status: not-found
---

## Publisher

St. Columba publishes its own bulletin, posted as one fixed file, http://www.saintcolumbabrooklyn.org/bulletin.pdf, linked from the site's frameset menu (links.htm) and from its Facebook page. Read 2026-11-06, that file is the 7 December 2025 issue ("DECEMBER 7, 2025" on page 2), with the masthead "Saint Columba, A Roman Catholic Parish, Diocese of Brooklyn", 2245 Kimball Street, and Rev. Timothy J. Lambert, Pastor. No current issue was found anywhere: the parish's LPi org (`st-columba-church-11234`) has no issues or container, and Discover Mass shows no bulletins. The LPi ids are recorded in `publication` as this parish's own org for when issues appear.

## Worship sites

One church, St. Columba, 2245 Kimball Street (`churches/st-columba-marine-park`); the December 2025 issue names no other place. The priests' directory gives Rev. Timothy J. Lambert as "Pastor, St. Columba, Marine Park" alone.

## Website and bulletin provider

`no_bulletin`, status `not-found`: the only bulletin is 11 months old. `fetch:check` with `page-pdfs http://www.saintcolumbabrooklyn.org/links.htm` resolves and downloads bulletin.pdf (transport ok, freshness unknown), but that is the stale issue, so the recipe is kept in the research next_action rather than set. The unpinned homepage fails (`NoBulletin`, the frameset hides the link).

## Not yet confirmed

Whether the parish still publishes a bulletin at all. Recheck bulletin.pdf and the LPi org after 2026-12-07 (see research).
