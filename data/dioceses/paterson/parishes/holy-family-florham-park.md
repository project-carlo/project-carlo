---
name: Holy Family
website: https://holyfamilyfp.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/church-of-the-holy-family-florham-park-nj-07932
publication: ['url:https://www.church-bulletin.org/church-of-the-holy-family-florham-park-nj-07932']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/church-of-the-holy-family-florham-park-nj-07932/2026-11-01.pdf
  seen: 2026-11-04
  quote: 662 Holy Family, Florham Park, NJ
  note: Page 1 of the 1 November 2026 issue reads "ALL SAINTS SUNDAY NOVEMBER 1, 2026", Rev. Thomas Rekiel,
    Pastor, Rectory 1 Lloyd Ave., Florham Park, NJ 07932, and the Mass schedule Saturday 5:30 pm, Sunday
    7:30 am, 10:00 am, 12:00 pm, Monday-Saturday 8:15 am. The ad pages' footer reads "662 Holy Family,
    Florham Park, NJ ... John Patrick Publishing Co., Inc.". Eight pages; a grep for Chapel and Mission
    finds no other worship site.
- url: https://www.jppc.net/onlinebulletins/662template.pdf
  seen: 2026-11-04
  note: The Bulletins link on the parish site; it redirects to https://www.church-bulletin.org/church-of-the-holy-family-florham-park-nj-07932,
    which lists weekly issues newest first, 2026-11-01 then 10-25, 10-18, 10-11.
- url: https://holyfamilyfp.org/bulletins
  seen: 2026-11-04
  note: The parish's eCatholic site (site id 12451; /bulletins read in headed Chrome with visit.py). Its
    Bulletins page links "Bulletins" to https://www.jppc.net/onlinebulletins/662template.pdf; the eCatholic
    archive below it ends at files.ecatholic.com/12451/bulletins/20260628.pdf (28 June 2026).
bulletin_status: available
---

## Publisher

Holy Family, Florham Park publishes a weekly bulletin through John Patrick Publishing (JPPC customer 662), posted on church-bulletin.org. Page 1 of the 1 November 2026 issue (`https://www.church-bulletin.org/bulletin/church-of-the-holy-family-florham-park-nj-07932/2026-11-01.pdf`, read 2026-11-04) reads "ALL SAINTS SUNDAY NOVEMBER 1, 2026", names Rev. Thomas Rekiel, Pastor, and gives the rectory at 1 Lloyd Ave., Florham Park, NJ 07932; the ad pages' footer reads "662 Holy Family, Florham Park, NJ (I) John Patrick Publishing Co., Inc.".

## Worship sites

- `holy-family-florham-park`: the only church. The page 1 Mass schedule (Saturday 5:30 pm; Sunday 7:30 am, 10:00 am, 12:00 pm; Monday-Saturday 8:15 am) names no other place, and a grep of all 8 pages for Chapel and Mission found none.

The diocese's finder (directory:12451) and GCatholic (19010) list this one church.

## Website and bulletin provider

The website is the parish's eCatholic site (site id 12451). Its Bulletins page (read in headed Chrome with visit.py, 2026-11-04) links `https://www.jppc.net/onlinebulletins/662template.pdf`, which redirects to the church-bulletin.org listing; the eCatholic archive below it stops at 28 June 2026, and `issues.py ecatholic ecatholic:12451` found no issue for 25 October-8 November. So `ecatholic:12451` is not this bulletin's publication id and is not recorded. Provider `other` with the recipe `page-pdfs https://www.church-bulletin.org/church-of-the-holy-family-florham-park-nj-07932`; `fetch:check` on 2026-11-04 picked the 1 November 2026 issue ("page-pdfs on https://www.church-bulletin.org/church-of-the-holy-family-florham-park-nj-07932: current", 3 days old).

## Not yet confirmed

Nothing open.
