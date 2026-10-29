---
name: St. Andrew Parish
website: https://www.standrewnewtown.com
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-andrew-catholic-church-newtown-pa-18940
publication: ['url:https://www.church-bulletin.org/saint-andrew-catholic-church-newtown-pa-18940']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-andrew-catholic-church-newtown-pa-18940
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 1 (church-bulletin.org/?id=1), 'Saint Andrew Catholic Church', Newtown, PA
    18940, 81 Swamp Road, phone (215) 968-2262; latest edition October 25, 2026.
- url: https://www.church-bulletin.org/bulletin/saint-andrew-catholic-church-newtown-pa-18940/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages, image-only; md5 e1b2ac41064c17ca7ad31c2808417a65). Rendered
    page 1 masthead: ''SAINT ANDREW NEWTOWN - OCTOBER 25, 2026 ... SAINT ANDREW CHURCH 81 SWAMP RD - NEWTOWN,
    PA - 18940'' beside ''SAINT ANDREW SCHOOL 51 WRIGHTS RD''; page 2 ''MASS TIMES: DAILY 7:00 & 9:00am;
    SATURDAY 9:00am & 5:00pm; SUNDAY 6:45, 7:45, 9:00, 10:30am & Noon; HOLY DAY 5:30pm Vigil, 7:00 & 9:00am;
    7:00pm''. Names this parish alone.'
- url: https://www.standrewnewtown.com/bulletins
  seen: 2026-10-29
  note: 'Parish eCatholic site (ecatholic:37063), Bulletin page rendered in Chrome: its only bulletin
    link is church-bulletin.org/?id=001, no files.ecatholic.com bulletin PDF, so the John Patrick listing
    is the channel and the eCatholic id stays out of publication. (probe url answers 403 on the home page;
    visit.py loads it.)'
- url: https://archphila.org/parish/st-andrew-newtown/
  seen: 2026-10-29
  quote: Rev. Msgr. Kevin C. Lawrence
  note: 'Directory: pastor; 81 Swamp Rd., Newtown 18940; Bucks County Central and North deanery; Mass
    times (Sat 5 PM; Sun 6:45, 7:45, 9, 10:30, Noon) match the bulletin.'
research:
- method: Read the Mass box and masthead on pages 1-2 of the 25 October 2026 issue; searched the text
    layers of the 2025-06-01, 2026-01-04, 2026-06-07 issues and the site pages for Mass at the 'Olde Church'
  url: https://www.church-bulletin.org/bulletin/saint-andrew-catholic-church-newtown-pa-18940/2026-01-04.pdf
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Andrew Parish, Newtown (Rev. Msgr. Kevin C. Lawrence, Pastor) prints with John Patrick Publishing: listing 1 (`church-bulletin.org/?id=1`) has an issue for 25 October 2026. The 25 October PDF has no text layer; page 1's masthead reads 'SAINT ANDREW NEWTOWN • OCTOBER 25, 2026' with the church (81 Swamp Rd.) and the parish school (51 Wrights Rd.) side by side, and page 2 carries the one Mass box. It names this parish alone. The parish's own site is eCatholic (37063), but its Bulletin page links only the listing.

## Worship sites

One church, St. Andrew, 81 Swamp Road. Page 2's footer banner reads 'OLDE CHURCH • 135 S. SYCAMORE ST. • NEWTOWN, PA • 18940', and the masthead of earlier issues repeats the address '(Olde Church)'. It appears as a venue (January 2026: 'AN 8 WEEK STUDY IN THE ST. ANDREW OLDE CHURCH', a grief group 'January 12TH, 7:00-8:30PM, Olde Church'), never in a Mass box, and the parish site's Mass schedule lists only 81 Swamp Road. So no church row for it; no Mass there is evidenced in the issues listed under research. Not an exclusion record either, since nothing states that no Mass is held.

## Website and bulletin provider

`https://www.standrewnewtown.com` (directory: `http://www.standrewnewtown.com/`) is the parish's eCatholic site (ecatholic:37063). `probe url` answers HTTP 403; the browser loads it.

## Not yet confirmed

Whether Mass is ever celebrated in the Olde Church (e.g. a school or feast-day Mass): none seen in the four issues read. Revisit if a bulletin's Mass box or calendar names it.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (date inferred from the listing's file name); identity `unverified` because the PDF has no text layer to match, so the masthead was read by hand above. It printed no `recipe` line, as the pinned `provider_id` already holds it.
