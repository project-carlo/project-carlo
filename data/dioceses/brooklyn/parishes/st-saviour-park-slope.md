---
name: St. Saviour (Park Slope)
website: https://stsaviourchurch.org/
bulletin_provider: parishes_online
provider_id: st-saviour-church
publication: ['po-org:st-saviour-church', 'lpi:0018000000Qc2SBAAZ', 'po-container:04/0259']
group: Deanery B4 (Brooklyn West)
evidence:
- url: https://container.parishesonline.com/bulletins/04/0259/20261101B.pdf
  seen: 2026-11-06
  quote: St. Saviour Church, Brooklyn, NY 04-0259
  note: '1 November 2026 issue (8 pages; page 1 an image). Rendered page 1 (render.py on the site''s copy,
    same cover): masthead ''SAINT SAVIOUR CHURCH, 611 8TH AVENUE, BROOKLYN, NY 11215 | 718.768.4055'',
    ''SUNDAY, NOVEMBER 1, 2026''. Page 2: ''WEEKEND MASSES 5:00 pm: Saturday Evening, 9:30 am: Sunday
    Morning, 11:30 am: Sunday Morning; WEEKDAY MASSES 8:30 am Monday, Tuesday, Wednesday & Thursday'',
    one church. Pages 7-8 footer is the quote.'
- url: https://parishesonline.com/organization/st-saviour-church
  seen: 2026-11-06
  note: 'probe po: org ''St. Saviour Church'' (lpi 0018000000Qc2SBAAZ, container 04/0259), 611 8th Ave,
    Brooklyn 11215, website stsaviourchurch.org; weekly issues to 2026-11-08. The slugs st-saviour-church-11215
    and saint-saviour-church(-11215) don''t exist.'
- url: https://stsaviourchurch.org/events/bulletin/
  seen: 2026-11-06
  note: 'Diocesan WordPress-multisite parish site (uploads under /wp-content/uploads/sites/103/; probe
    url gets RemoteDisconnected, visit.py loads it). The bulletin page lists the LPi issues reposted with
    their ad pages cut, newest first: nov8_2026_saintsav_compressed.pdf, nov1_2026_saintsav_compressed.pdf
    (6 pages, same pages 1-6 as the container issue, no footer), oct25_2026_stsaviour2_compressed.pdf,
    ...'
- url: https://saintsaviourchurch.org
  seen: 2026-11-06
  note: 'GCatholic''s website for the parish now redirects to soh.church, ''Sound of Heaven Church | Long
    Island Church | Deer Park NY'': a lapsed domain, not the parish.'
promoted: 2026-11-12
research:
- method: fetch:check parishes_online org st-saviour-church
  url: https://parishesonline.com/organization/st-saviour-church
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
---

## Publisher

The parish publishes a weekly LPi bulletin, ParishesOnline container 04/0259 under the org `st-saviour-church` (lpi `0018000000Qc2SBAAZ`). I read the 1 November 2026 issue (2026-11-06): page 1 is an image; rendered, its masthead reads "SAINT SAVIOUR CHURCH, 611 8TH AVENUE, BROOKLYN, NY 11215", "SUNDAY, NOVEMBER 1, 2026"; pages 7-8 carry the footer "St. Saviour Church, Brooklyn, NY 04-0259". The prefix is 04, not 03.

## Worship sites

One church, St. Saviour, 611 8th Avenue: page 2's WEEKEND MASSES (Saturday 5:00 pm; Sunday 9:30 and 11:30 am) and WEEKDAY MASSES (8:30 am Monday-Thursday) name no other place. The pastor's letter mentions a seminarian's first Mass at Saint Michael Church, Sunset Park (another parish), and seating "in the chapel" for an event, not a separate Mass site.

## Website and bulletin provider

`parishes_online`, org `st-saviour-church`. The website is the parish's diocesan WordPress-multisite site, whose `/events/bulletin/` page reposts each LPi issue without its ad pages (`nov1_2026_saintsav_compressed.pdf`, 6 pages, no footer), so the site's copy alone looks self-made; the container is the live source. GCatholic's `saintsaviourchurch.org` now redirects to an unrelated Deer Park church. `fetch:check` (2026-11-06) picked `04/0259/20261108B.pdf`, the 8 November 2026 issue (freshness `future`: this coming Sunday, already posted), transport ok as a PDF.

## Not yet confirmed

Nothing open.
