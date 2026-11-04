---
name: Church of the Assumption of the Blessed Virgin Mary
website: https://assumptionparish.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11358']
group: ''
evidence:
- url: https://files.ecatholic.com/11358/bulletins/20261101.pdf
  seen: 2026-11-04
  quote: The Parish Family of
  note: 'Page 1 of the 1 November 2026 issue (10 pages): ''November 1, 2026 The Solemnity of All Saints'',
    Mass Schedule Saturday 8:00 a.m., 5:30 p.m.; Sunday 7:00, 8:00, 10:00 a.m., 12:00 p.m., 5:30 p.m.
    (Sept.-May); Weekdays 7:00 a.m., 12:05 p.m.; ''Since 1848 The Parish Family of The Church of the Assumption
    of the Blessed Virgin Mary''. Page 2 header ''Assumption Church Morristown, NJ'' and ''91 Maple Avenue,
    Morristown, New Jersey 07960''. A grep for Chapel finds nothing.'
- url: https://assumptionparish.org/bulletins
  seen: 2026-11-04
  note: Bulletin page (read with parish-site-access visit.py; probe url gets 403) lists an Archive of
    weekly issues for 2026, newest November 1, 2026, back to January 4, 2026, plus 2025 and 2024 folders.
    visit.py on the home page found ecatholic:11358.
bulletin_status: available
---

## Publisher

The Church of the Assumption of the Blessed Virgin Mary, Morristown publishes its own weekly bulletin on eCatholic (site id 11358, the diocese finder's pin id). The 1 November 2026 issue (`https://files.ecatholic.com/11358/bulletins/20261101.pdf`, read 2026-11-04) has on page 1 "November 1, 2026 The Solemnity of All Saints" and "Since 1848 The Parish Family of The Church of the Assumption of the Blessed Virgin Mary"; page 2 is headed "Assumption Church Morristown, NJ" and gives "91 Maple Avenue, Morristown, New Jersey 07960".

## Worship sites

- `assumption-morristown`: the only church. Page 1's Mass Schedule (Saturday 8:00 a.m., 5:30 p.m.; Sunday 7:00, 8:00, 10:00 a.m., 12:00 p.m., 5:30 p.m. Sept.-May; weekdays 7:00 a.m., 12:05 p.m.) names no other place, and a grep of all 10 pages for Chapel finds nothing.

The diocese's finder (directory:11358) and GCatholic (19015) list this one church. Holy Rood Cemetery (page 2) is the parish's cemetery, not a worship site.

## Website and bulletin provider

`assumptionparish.org` is the parish's eCatholic site (the finder's link; GCatholic gives the same domain with www). It answers `probe url` with 403 (Cloudflare); `visit.py` loaded it on 2026-11-04 and found `ecatholic:11358`. Its /bulletins page lists weekly issues for 2026, newest November 1, 2026. Provider `ecatholic`; `fetch:check` on 2026-11-04 resolved the latest bulletin link on https://assumptionparish.org/ to `files.ecatholic.com/11358/bulletins/20261101.pdf` (1 November 2026, 3 days old; identity unverified because no expected identity is supplied).

## Not yet confirmed

Nothing open.
