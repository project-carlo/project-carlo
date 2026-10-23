---
name: Our Lady of Peace Parish
website: https://www.olp.org
bulletin_provider: discover_mass
provider_id: our-lady-of-peace-erie-pa
publication: ['discovermass:our-lady-of-peace-erie-pa']
group: ''
evidence:
- url: https://www.olp.org/assets/bulletins/2026/10.25.2026.pdf
  seen: 2026-10-23
  quote: 2401 West 38th Street, Erie, PA 16506
  note: Page 1 (cover) of the 25 October 2026 issue (12 pages), first listed on the parish site's /bulletin
    page, which links each week's PDF as assets/bulletins/2026/<mm.dd.yyyy>.pdf (6 Sept to 25 Oct 2026
    present). Cover names Our Lady of Peace alone; page 2 header 'OURLADYOFPEACECHURCH ERIE,PA'.
- url: https://www.olp.org/assets/bulletins/2026/10.25.2026.pdf
  seen: 2026-10-23
  quote: 7:30AM Living &D eceasedM embers of OLP
  note: 'Page 3, Mass intentions (the PDF text layer splits words): Saturday 31 Oct 8:00AM and 5:00PM;
    Sunday 1 Nov 7:30AM, 9:00AM, 11:00AM, 4:30PM; weekdays 7:00AM and 12:10PM. Matches the diocese directory''s
    schedule.'
- url: https://discovermass.com/church/our-lady-of-peace-erie-pa/
  seen: 2026-10-23
  note: 'Discover Mass church page: current bulletin cover class carries the bulletin number 3518 for
    the 25 Oct 2026 issue. The olp.org PDF''s last page prints ''3518'', so the parish-site PDF and the
    Discover Mass channel are one bulletin.'
- url: https://www.eriercd.org/Parish10303-Our-Lady-of-Peace.html
  seen: 2026-10-23
  note: 'Diocese directory record 10303 (also GCatholic 24456): one parish record, no mission or secondary
    church, no partner.'
research:
- method: pnpm fetch:check --diocese erie --parish our-lady-of-peace-erie --expected-identity 'Our Lady
    of Peace' --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://discovermass.com/church/our-lady-of-peace-erie-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, identity matched in first-page text; the date check was 'unknown'
    because the cover's date text is split by the layout. The downloaded file is 4,684,076 bytes, the
    same size as olp.org's 10.25.2026.pdf, whose last page prints bulletin number 3518 (the Discover Mass
    number).
---

## Publisher

Our Lady of Peace Parish, Erie (Pastor Rev. Richard Toohey per the diocese directory and the bulletin's staff page) publishes its own weekly bulletin, produced by Diocesan Publications (the 'Diocesan.com' advertising line and the 'View this bulletin online at www.DiscoverMass.com' footer on every page). I read the 25 October 2026 issue on 2026-10-23: the cover names 'Our Lady of Peace', 2401 West 38th Street, and every page is about this parish only. The diocese has no families here; the directory shows OLP as a single parish with no partner or secondary church (record 10303).

## Worship sites

One church, Our Lady of Peace at 2401 W. 38th St. The bulletin's Mass intentions list Saturday 8:00AM and 5:00PM and Sunday 7:30, 9:00, 11:00AM and 4:30PM, plus 7:00AM and 12:10PM weekdays, all at this church (a weekday 12:10 Mass 'in the Chapel' is a place inside the same campus building, not a separate site; the bulletin gives no separate address). The bulletin also mentions St. Joseph's, 147 W. 24th St. as the host of a joint grief ministry with St. Joseph/Sacred Heart/St. Paul: a different parish, outside this batch.

## Website and bulletin provider

The lead said olp.org fails TLS on the bare host; `https://www.olp.org` works (probe url 200, 2026-10-23). The same issue is on three channels: the parish site's /bulletin page (self-hosted PDFs), Discover Mass (church slug our-lady-of-peace-erie-pa, bulletin number 3518) and the PDF itself. Provider is `discover_mass` because fetch reads Discover Mass by slug, and the site PDF is the same document (number 3518). Discover Mass downloads are capped per IP per day, so if fetch:check is `not_pdf`, the fallback is an `other` recipe `page-pdfs https://www.olp.org/bulletin`.

## Not yet confirmed

Nothing open for the row itself.
