---
name: St. Nicholas, Jersey City
website: http://stnicholaschurchorg.weebly.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/681
publication: ['url:https://www.church-bulletin.org/saint-nicholas-church-jersey-city-nj-07307']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-nicholas-church-jersey-city-nj-07307/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 6 pages, image only (read with render.py; recheck cannot find quotes).
    Page 1 masthead: ''SAINT NICHOLAS CHURCH, 122 Ferry Street, Jersey City, NJ 07307''. Page 2 Mass intentions:
    Sat 31 Oct 5:00PM; Sun 1 Nov 8:00AM, 11:00AM, 12:30PM; Mon-Fri 12:00PM (Thu 5 Nov also 7:00PM); Sat
    7 Nov 5:00PM; Sun 8 Nov 8:00AM, 11:00AM, 12:30PM. Page 6 footer: ''681 St. Nicholas, Jersey City,
    NJ (b)  John Patrick Publishing Company, Inc.'''
- url: https://church-bulletin.org/681
  seen: 2026-11-03
  quote: Latest Edition November 1, 2026 Bulletin
  note: Redirects to church-bulletin.org/saint-nicholas-church-jersey-city-nj-07307, 'Saint Nicholas Church
    Bulletin', 122 Ferry Street, Jersey City, NJ 07307.
- url: http://stnicholaschurchorg.weebly.com/
  seen: 2026-11-03
  note: 'The parish''s Weebly site (visit.py): its bulletin link is http://www.jppc.net/onlinebulletins/681template.pdf.
    The directory''s http://saintnicholaschurch.org/ is a 499-byte frameset that loads this Weebly site;
    GCatholic''s http://www.saintnicholasparishofjcnj.org answered HTTP 502.'
bulletin_status: available
---

## Publisher

St. Nicholas, Jersey City, publishes a weekly bulletin printed by John Patrick Publishing (id 681). I read the 1 November 2026 issue (image only, rendered with render.py): page 1 masthead 'SAINT NICHOLAS CHURCH, 122 Ferry Street • Jersey City • NJ 07307'; page 2 'St. Nicholas … Jersey City, New Jersey' with Mass intentions for 31 October-8 November; page 6 footer '681 St. Nicholas, Jersey City, NJ (b) John Patrick Publishing Company, Inc.'. One set of Mass intentions, for one church.

## Worship sites

- St. Nicholas, 122 Ferry Street (`st-nicholas-jersey-city`): Saturday 5:00 PM; Sunday 8:00 AM, 11:00 AM, 12:30 PM; weekdays 12:00 PM (page 2 intentions).

The directory (78) and GCatholic (18454) list only this church.

## Website and bulletin provider

The directory's http://saintnicholaschurch.org/ is a frameset over http://stnicholaschurchorg.weebly.com/, recorded as the website because that page holds the bulletin link (jppc.net/onlinebulletins/681template.pdf). GCatholic's www.saintnicholasparishofjcnj.org answered HTTP 502 on 2026-11-03. The provider is `other`, read with `page-pdfs https://church-bulletin.org/681`. The issues are image only: the pipeline has to read them as images.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/681: current` and picked church-bulletin.org/bulletin/saint-nicholas-church-jersey-city-nj-07307/2026-11-01.pdf, the 1 November 2026 issue read above (date from the file name; page 1 has no text); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row. Times are from the intentions list; the issue has no separate schedule box on pages 1-2.
