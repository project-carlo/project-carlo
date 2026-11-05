---
name: St. Vincent de Paul
website: https://stvincentschurch.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=10184
publication: ['url:http://sponsors.bonventure.net/?page=10184']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/10184/2026-11-08.pdf
  seen: 2026-11-04
  note: 'Rendered page 1 (garbled text layer): masthead names St. Vincent de Paul Roman Catholic Parish,
    www.stvincentschurch.org, Fr. Hernan Cely Pastor; Mass Schedule Daily Mass Monday-Saturday 8:30AM,
    Saturday 4PM (Vigil), Sunday 7AM, 9AM and 11AM; 250 Bebout Avenue Stirling, New Jersey 07980. Page
    2 header: November 8, 2026, THIRTY SECOND SUNDAY IN ORDINARY TIME. Pages 7-8 footer: 156A (JR) St.
    Vincent de Paul - Stirling, NJ.'
- url: https://stvincentschurch.org/bulletin-email
  seen: 2026-11-04
  note: The site's bulletin page (read with parish-site-access visit.py; probe url gets 403) links Bulletin
    to http://sponsors.bonventure.net/?page=10184; the rest is a weekly parish email signup (app.ecatholic.com
    group messages).
- url: http://sponsors.bonventure.net/?page=10184
  seen: 2026-11-04
  note: Bon Venture sponsor page; probe url finds the bulletin link http://sponsors.bonventure.net/pdfs/10184/2026-11-08.pdf.
promoted: 2026-11-05
research:
- method: issues.py ecatholic ecatholic:11664 --weeks 4
  url: https://files.ecatholic.com/11664/bulletins/20261108.pdf
  checked: '2026-11-04'
  outcome: not-found
  next_action: None needed while the Bon Venture page carries the bulletin; re-check eCatholic only if
    the Bon Venture page stops updating
  retry_when: The Bon Venture page shows no issue newer than 30 days
bulletin_status: available
---

## Publisher

St. Vincent de Paul, Stirling publishes its own weekly bulletin through Bon Venture (sponsor page 10184). The 8 November 2026 issue (`http://sponsors.bonventure.net/pdfs/10184/2026-11-08.pdf`, read 2026-11-04) has a garbled text layer, so pages 1-2 were rendered with render.py: page 1's masthead reads "St. Vincent de Paul Roman Catholic Parish ... www.stvincentschurch.org ... Fr. Hernan Cely Pastor ... 250 Bebout Avenue Stirling, New Jersey 07980"; page 2's header reads "November 8, 2026 THIRTY SECOND SUNDAY IN ORDINARY TIME". The ad pages' footer reads "156A (JR) St. Vincent de Paul - Stirling, NJ".

## Worship sites

- `st-vincent-de-paul-stirling`: the only church. Page 1's "Mass Schedule" (Daily Mass Monday-Saturday 8:30AM; Saturday 4PM Vigil; Sunday 7AM, 9AM and 11AM) names no other place, and page 2's Mass intentions list only those times.

The diocese's finder (directory:11664) and GCatholic (19014) list this church. GCatholic also lists the Shrine of St. Joseph, 1050 Long Hill Rd., Stirling (33104), which is a separate retreat house of the Missionary Servants of the Most Holy Trinity; this bulletin's schedule doesn't include it (its record is `shrine-of-st-joseph-stirling`). The text layer can't be grepped, so pages 3-8 were not searched for other mentions of the shrine.

## Website and bulletin provider

`stvincentschurch.org` is the parish's eCatholic site (site id 11664, the finder's link; GCatholic's stvincents.com is an older domain, not used). It answers `probe url` with 403; `visit.py` loaded it on 2026-11-04. Its bulletin page (/bulletin-email) links "Bulletin" to the Bon Venture sponsor page. `issues.py ecatholic ecatholic:11664` found no `bulletins/<YYYYMMDD>.pdf` for the 4 Sundays 18 October-8 November, so the eCatholic id is not this bulletin's publication and is not recorded. Provider `other` with the recipe `page-pdfs http://sponsors.bonventure.net/?page=10184`; `fetch:check` on 2026-11-04 resolved it to `http://sponsors.bonventure.net/pdfs/10184/2026-11-08.pdf` (the 8 November 2026 issue, posted ahead of its Sunday). It reports identity unverified, as expected for this garbled text layer.

## Not yet confirmed

Nothing open.
