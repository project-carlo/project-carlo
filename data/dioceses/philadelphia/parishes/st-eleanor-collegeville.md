---
name: St. Eleanor Parish
website: https://www.steleanor.com
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-eleanor-catholic-church-collegeville-pa-19426
publication: ['url:https://www.church-bulletin.org/saint-eleanor-catholic-church-collegeville-pa-19426']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-eleanor-catholic-church-collegeville-pa-19426/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick Publishing listing 10, issue of 25 October 2026 (16 pages, image-only: probe pdf
    reads 0 pages, so pages 1-5 were rendered). Page 1 masthead reads ''Saint Eleanor Catholic Church
    · Collegeville, Pa'' with ''Rev. Msgr. J. Brian Bransfield, Pastor · October 25, 2026 · Thirtieth
    Sunday in Ordinary Time''; page 2 onward is headed ''Saint Eleanor Catholic Church'' (Order of the
    Mass, Reflection by Msgr. Bransfield, weekly calendar with Chapel and Church on the same campus).
    md5 f16f72ac.'
- url: https://www.church-bulletin.org/saint-eleanor-catholic-church-collegeville-pa-19426
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 10 'Saint Eleanor Catholic Church', Collegeville, PA 19426, 647 Locust Street, phone (610)
    489-1647; latest edition October 25, 2026.
- url: https://www.steleanor.com/
  seen: 2026-10-28
  quote: Saturday - 4:30 p.m.
  note: 'Parish site (probe url HTTP 403; read in the browser): Weekend Mass Saturday 4:30 PM, Sunday
    7:30, 9, 10:30 AM, 12 PM; weekday Monday-Friday 6:30, 9 AM, Saturday 9 AM. Its Bulletin page /resources/bulletin
    lists dated files only to 31 August 2025 plus a fixed ''297-most-recent-bulletin'' file that answers
    403 to probe pdf.'
- url: https://archphila.org/parish/st-eleanor-collegeville/
  seen: 2026-10-28
  quote: Rev. Msgr. J. Brian Bransfield
  note: 'Directory: pastor Msgr. Bransfield; rectory 647 Locust St., Collegeville 19426.'
research:
- method: probe pdf on the parish site's fixed 'Most Recent Bulletin' file
  url: https://www.steleanor.com/resources/bulletin/297-most-recent-bulletin/file
  checked: '2026-10-28'
  outcome: access-blocked
  next_action: Open the file with the browser (parish-site-access visit.py) and compare md5 and masthead
    with listing 10; if byte-identical and current, note it as an equal copy
  retry_when: The listing stops posting current issues, or a later job wants the parish's own copy
---

## Publisher

St. Eleanor Parish, Collegeville (Rev. Msgr. J. Brian Bransfield, Pastor) is distributed by John Patrick Publishing as listing 10, 'Saint Eleanor Catholic Church'. The 25 October 2026 issue is 16 pages of images with no text layer; the page-1 masthead reads 'Saint Eleanor Catholic Church · Collegeville, Pa' and each later page carries the same running head. The row is `other` with `page-pdfs` on the listing.

## Worship sites

One church, St. Eleanor Church, 647 Locust Street. The bulletin's calendar puts the Rosary group and Divine Mercy devotions 'Chapel' and meetings in Vianney Hall and Kateri Hall; the parish site says confession is 'In Chapel' and no page gives it another address, so it is treated as a room of the church campus, not another worship site. No mission, worship site or second Mass location appears in the bulletin or on the site.

## Website and bulletin provider

steleanor.com answers 403 to `probe url` and loads in Chrome. Its /resources/bulletin page is a Joomla list whose dated files stop at 31 August 2025; its 'Most Recent Bulletin' file answers 403 to `probe pdf` and was not compared. The listing has the 25 October 2026 issue, so it is the channel.

## Fetch check

`fetch:check` (2026-10-28) resolved `page-pdfs` on the listing to the 2026-10-25 issue: transport ok, PDF, fresh (3 days); issue date inferred from the file name; identity `unverified` because the PDF has no text layer (the masthead was read from a render, above). The recipe is already in `provider_id`.

## Not yet confirmed

The parish's own 'Most Recent Bulletin' copy was not read (see research). Pages 6-16 of the bulletin were not read.
