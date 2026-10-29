---
name: St. Titus Parish
website: https://www.sttitus.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-titus-parish-east-norriton-pa-19403
publication: ['url:https://www.church-bulletin.org/saint-titus-parish-east-norriton-pa-19403']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-titus-parish-east-norriton-pa-19403/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick Publishing listing 95, issue of 25 October 2026 (12 pages, image-only, so pages
    1-3 were rendered). Page 1: ''St. Titus Parish'', ''3000 KEENWOOD ROAD, EAST NORRITON, PA 19403'',
    ''PARISH PHONE: 610-279-4990'', ''October 25, 2026'', and an Anointing Mass notice (Sunday, October
    25 at 10:00 AM, Saint Titus Church). Page 2: Parish Mission Statement; Clergy (''Fr. Joseph W. Bongard:
    St. Titus Parochial Admin and Pastor, St. Helena''); a ''ST. TITUS PARISH MASS SCHEDULE'' (Saturday
    4:30 PM Vigil; Sunday 10:00 AM; weekdays Mon, Tues, Thurs, Fri 8:00 AM, ''Wednesday & Saturday No
    Morning Mass''; Holydays 8:00 AM and 7:00 PM) and a ''SAINT HELENA (PARTNER PARISH) MASS SCHEDULE''.
    Page 3: ''Partner Parishes Mass Intentions''.'
- url: https://www.church-bulletin.org/saint-titus-parish-east-norriton-pa-19403
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 95 'Saint Titus Parish', East Norriton, PA 19403 (the township, not Norristown); latest
    edition October 25, 2026.
- url: https://www.sttitus.org/
  seen: 2026-10-28
  quote: NO MORNING MASS on Wednesdays & Saturdays
  note: 'Parish site (eCatholic 5092; probe url HTTP 200). Mass Times: Saturday 4:30 PM, Sunday 10:00
    AM, weekdays 8:00 AM Mon, Tue, Thu, Fri; address ''3000 Keenwood Road | East Norriton, PA 19403''.
    It links ''https://church-bulletin.org/?id=095'' as the current bulletin.'
- url: https://www.sttitus.org/bulletins
  seen: 2026-10-28
  note: 'The site''s own /bulletins archive on eCatholic stops at 16 February 2025: the newest file link
    on the page is files.ecatholic.com/5092/bulletins/20250216.pdf (read from the page source, not visible
    text). The John Patrick listing is therefore the current channel. An eCatholic id alone is not a publication
    id and is left out of `publication`.'
- url: https://archphila.org/parish/st-titus-norristown/
  seen: 2026-10-28
  quote: in residence at Saint Helena, Blue Bell
  note: 'Directory: Rev. Joseph W. Bongard (Parochial Administrator) in residence at Saint Helena; office
    3000 Keenwood Rd., Norristown 19403; Mass times (Sundays 9 and 11 AM) older than the bulletin and
    the site (Sunday 10:00 AM only).'
publication_reviews:
- parish: st-helena-blue-bell
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-titus-parish-east-norriton-pa-19403/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names St. Titus Parish, 3000 Keenwood
      Road, East Norriton, alone, with its own cover (an Anointing Mass notice); 12 pages, md5 8ecb9184,
      a different file in a different listing (95). Both bulletins print the partner parish's Mass times
      and a joint Mass-intentions list, but each is its own issue.
  - url: https://www.church-bulletin.org/bulletin/saint-helena-church-blue-bell-pa-19422/2026-10-25.pdf
    seen: 2026-10-28
    note: The 25 October 2026 masthead (page 1, image rendered) names Saint Helena Parish, 1489 DeKalb
      Pike, Blue Bell, alone, with its own Mass schedule and a green Saint Helena layout; 16 pages, md5
      28af7c1e.
---

## Publisher

St. Titus Parish (Rev. Joseph W. Bongard, Parochial Administrator, who lives at St. Helena, Blue Bell) is distributed by John Patrick Publishing as listing 95, 'Saint Titus Parish', filed under East Norriton, the township, not Norristown. The 25 October 2026 issue has its own cover headed 'St. Titus Parish, 3000 Keenwood Road, East Norriton, PA 19403', 12 pages of images. The parish's own eCatholic site (5092) links the listing as its current bulletin; its `/bulletins` archive ends at 16 February 2025. The row is `other` with `page-pdfs` on the listing.

**Shared with St. Helena?** No: separate listing, separate file and cover (see `st-helena-blue-bell` and `publication_reviews`). Both bulletins print both parishes' Mass times and a joint intentions list.

## Worship sites

One church, St. Titus Church, 3000 Keenwood Rd. (the directory and GCatholic give 'Norriton Dr. & Keenwood Rd.'). The bulletin's Mass schedule gives Saturday 4:30 PM vigil, Sunday 10:00 AM and weekday 8:00 AM Masses; the parish site agrees. The directory's Sunday 9 and 11 AM is out of date (page 'updated 1 year ago'). The St. Helena schedule printed beside it is St. Helena's own church, not a worship site of this row.

## Website and bulletin provider

sttitus.org is an eCatholic site whose bulletin archive stopped in February 2025; the listing's dated PDFs `https://www.church-bulletin.org/bulletin/saint-titus-parish-east-norriton-pa-19403/<yyyy-mm-dd>.pdf` are the channel.

## Fetch check

`fetch:check` (2026-10-28) resolved `page-pdfs` on the listing to the 2026-10-25 issue: transport ok, PDF, fresh; issue date inferred from the file name; identity `unverified` because the PDF has no text layer (the masthead was read from a render, above). The recipe is already in `provider_id`.

## Not yet confirmed

Image-only PDF, so `fetch:check` identity is unverified by design; masthead read from a render. Pages 4-12 were not read.
