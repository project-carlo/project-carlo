---
name: Good Shepherd
website: https://goodshepherdpanj.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:25544', 'po-org:good-shepherd-parish-08861', 'lpi:0018000000QxA3SAAV', 'po-container:03/4084']
group: ''
evidence:
- url: https://files.ecatholic.com/25544/bulletins/20261025.pdf
  seen: 2026-11-03
  quote: Good Shepherd Parish  |  03-4084
  note: '25 October 2026 issue, 12 pages, pages 1-11 images with no text layer; the quote is the LPi code
    line on page 12. Page 1 rendered: masthead ''GOOD SHEPHERD PARISH CATHOLIC CHURCH'', ''625 FLORIDA
    GROVE ROAD HOPELAWN, NEW JERSEY 08861'', www.goodshepherdpanj.org; Mass Schedule: Weekend Saturday
    4:30pm Vigil, Sunday 8:30am, 11:00am; Weekday Monday 7:00pm, Tuesday-Friday 8:00am. No other church
    is named.'
- url: https://goodshepherdpanj.org/bulletins
  seen: 2026-11-03
  quote: October 25, 2026
  note: eCatholic site 25544, read with visit.py (probe url said DEAD-DNS, probe get 403). The Bulletins
    page lists files.ecatholic.com/25544/bulletins/<YYYYMMDD>.pdf weekly through 25 October 2026; 20261101.pdf
    answered 403 on 2026-11-03.
- url: https://parishesonline.com/organization/good-shepherd-parish-08861
  seen: 2026-11-03
  quote: Good Shepherd Parish
  note: 'probe po: LPi id 0018000000QxA3SAAV, container 03/4084, address 625 Florida Grove Rd, Perth Amboy,
    website www.goodshepherdpanj.org; latest issue 2026-11-01. Its 20261025B.pdf is byte-identical (md5
    309a17d2…, 33,506,142 bytes) to the eCatholic 20261025.pdf, so they are one publication.'
- url: https://goodshepherdpanj.org/about-us
  seen: 2026-11-03
  quote: The Good Shepherd Parish was established on July 1, 2012, when both Holy Spirit Church and Our
    Lady of the Most Holy Rosary merged.
  note: 'Continues: ''the name of the church building itself did not change. It is still Our Lady of the
    Most Holy Rosary.'''
revisit: Check that files.ecatholic.com/25544/bulletins/20261101.pdf has been posted; if eCatholic still
  lags ParishesOnline by more than a week, switch to parishes_online (good-shepherd-parish-08861).
revisit_after: 2026-11-17
promoted: 2026-11-03
bulletin_status: available
---

## Publisher

Good Shepherd, Hopelawn publishes its own weekly bulletin, printed by LPi (code line 'Good Shepherd Parish | 03-4084'). The parish posts each issue on its eCatholic site (25544), and ParishesOnline container 03/4084 carries the same file. The 25 October 2026 issue (read 2026-11-03) is image-only on pages 1-11; the page 1 render shows the masthead 'GOOD SHEPHERD PARISH CATHOLIC CHURCH', '625 FLORIDA GROVE ROAD HOPELAWN, NEW JERSEY 08861', and one Mass schedule. It names no other church.

## Worship sites

One church, Our Lady of the Most Holy Rosary, 625 Florida Grove Road (the About page: 'the name of the church building itself did not change. It is still Our Lady of the Most Holy Rosary'). Masses (25 October 2026 bulletin, page 1): Saturday 4:30pm Vigil; Sunday 8:30am and 11:00am; Monday 7:00pm; Tuesday-Friday 8:00am. The parish office's chapel is open by appointment only, not a Mass site.

GCatholic also lists Holy Spirit, 580 Hazel Ave. (gcatholic:18602) under the parish. A 29 October 2015 MyCentralJersey article reports worship there suspended effective 14 September 2015, and the parish's Religious Education page (read 2026-11-03) holds classes 'in the newly renovated basement of the former Holy Spirit Church on Hazel Avenue'. It is excluded as closed (`excluded/holy-spirit-perth-amboy`).

## Website and bulletin provider

eCatholic site 25544 (goodshepherdpanj.org), the parish-hosted copy, recorded under the diocese's rule for one bulletin on two hosts; the ParishesOnline ids are listed as the same publication. The finder's http://www.Goodshepherdpanj.org is the same site; probe url said DEAD-DNS and probe get answered 403, but visit.py loads it.

## Not yet confirmed

The eCatholic page lags ParishesOnline by a week: on 2026-11-03 ParishesOnline had the 1 November issue (20261101B.pdf) while eCatholic's newest was 25 October. If eCatholic keeps lagging past freshness, switch the row to `parishes_online` with provider_id good-shepherd-parish-08861.
