---
name: Ascension (Elmhurst)
website: https://ascensionparishelmhurst.org/
bulletin_provider: other
provider_id: page-pdfs https://ascensionparishelmhurst.org/bulletins
publication: []
group: Deanery Q6 (Queens West)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMzAvOWcxMnR3d3hpZl8yNl8xMV8xLnBkZiJdXQ/26-11-1.pdf
  seen: 2026-11-06
  quote: 86-13 55 t h  Avenue Elmhurst, NY 11373
  note: '1 November 2026 issue (Solemnity of All Saints), 6 pages. Page 1 masthead: ASCENSION Roman Catholic
    Church, 86-13 55th Avenue, Elmhurst; Rev. Anacleto S. Asebias Jr., Pastor; Mass schedule Monday-Friday
    8:00 AM, Saturday 8:00 AM and 5:00 PM Vigil, Sunday 9:30 AM, 11:30 AM and 1:00 PM (Spanish). No other
    church or chapel is named.'
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMzAvOWcxMnR3d3hpZl8yNl8xMV8xLnBkZiJdXQ/26-11-1.pdf
  seen: 2026-11-06
  quote: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY 11704-1104
  note: 'Page 6 ad-page footer ''#224'': printed by The Church Bulletin Inc., not LPi; no ParishesOnline
    container.'
- url: https://ascensionparishelmhurst.org/bulletins
  seen: 2026-11-06
  note: 'Tilma bulletins page, server-rendered, newest first: a card linking /bulletins/null (next issue
    not yet posted), then ''Bulletin for Sunday, Nov 1, 2026'' (26-11-1.pdf), Oct 25, Oct 18, Oct 11.'
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://ascensionparishelmhurst.org/bulletins
  url: https://ascensionparishelmhurst.org/bulletins
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check after 8 November and confirm it picks that issue
  retry_when: The 8 November card links a PDF instead of /bulletins/null
  revisit_after: 2026-11-09
- method: 'Reconcile: headed fetch:check of every Brooklyn row'
  url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTEvMDYvNG14aWlvY3ZsXzI2XzExXzgucGRmIl1d/26-11-8.pdf
  checked: '2026-11-12'
  outcome: found
  next_action: 'None: the pick is the 8 November 2026 issue (26-11-8.pdf, uploaded 2026-11-06).'
bulletin_status: available
---

## Publisher

Ascension, Elmhurst publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "#224") and posted as PDFs on the parish's Tilma site. The 1 November 2026 issue (read 2026-11-06, 6 pages) has the masthead "ASCENSION Roman Catholic Church, 86-13 55th Avenue Elmhurst, NY 11373" on page 1, with Rev. Anacleto S. Asebias Jr., Pastor.

## Worship sites

One. The page 1 Mass schedule lists Monday-Friday 8:00 AM, Saturday 8:00 AM and 5:00 PM (Vigil), Sunday 9:30 AM, 11:30 AM and 1:00 PM (Spanish), with no other church or chapel. The directory, the deanery list, GCatholic 16601 and Mass finder 956 all give the one church at 86-13 55th Avenue.

GCatholic's Our Lady of China chapel (16801, 54-09 92nd St., Elmhurst), placed in this batch by the survey, is not in this bulletin; see its own record.

## Website and bulletin provider

`other`, recipe `page-pdfs https://ascensionparishelmhurst.org/bulletins` (the Tilma bulletins page, newest first). There is no publication id: The Church Bulletin Inc. has no online container.

## Not yet confirmed

On 2026-11-06 the newest card linked `/bulletins/null`, so the 8 November issue was not yet posted; see research.
