---
name: St. Mary's Church
website: https://stmarys-pompton.org/
bulletin_provider: parishes_online
provider_id: st-marys-church-07442
publication: ['po-org:st-marys-church-07442', 'lpi:0018000000QxAWvAAN', 'po-container:03/1364']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/1364/20261108B.pdf
  seen: 2026-11-04
  quote: St. Mary's Church  |  03-1364
  note: 'LPi ad footer of the 8 November 2026 issue. Page 1 masthead: ''SAINT MARY''S CATHOLIC CHURCH
    A FRANCISCAN COMMUNITY'' (logo image), ''17 POMPTON AVENUE POMPTON LAKES, NJ 07442'', ''November 8,
    2026''. Page 2 names Fr. Ed Shea, OFM and gives the MASS SCHEDULE: Saturday Vigil 5:00 PM, 7:00 PM;
    Sunday 7:30 AM, 8:45 AM Espanol, 9:00 AM English (Carnevale Center), 10:30 AM, 12:00 PM; weekdays
    8:00 AM, Wednesday 7:00 PM en Espanol.'
- url: https://parishesonline.com/organization/st-marys-church-07442
  seen: 2026-11-04
  note: 'probe po: ''St. Mary''s Church'', 17 Pompton Ave, Pompton Lakes, NJ 07442, website stmarys-pompton.org;
    lpi 0018000000QxAWvAAN, container 03/1364; weekly issues 4 Oct to 8 Nov 2026.'
- url: https://stmarys-pompton.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site 21395; the page lists
    files.ecatholic.com/21395/bulletins/<YYYYMMDD>.pdf copies, newest 20261101.pdf (1 November 2026),
    the same LPi issue as the container's 20261101B.pdf.
bulletin_status: available
---

## Publisher

St. Mary's, Pompton Lakes (a Franciscan parish) publishes its own weekly LPi bulletin on ParishesOnline (org `st-marys-church-07442`, container 03/1364). The 8 November 2026 issue (`https://container.parishesonline.com/bulletins/03/1364/20261108B.pdf`, read 2026-11-04) has on page 1 the logo "SAINT MARY'S CATHOLIC CHURCH A FRANCISCAN COMMUNITY" with "17 POMPTON AVENUE POMPTON LAKES, NJ 07442" and "November 8, 2026"; page 2 lists Fr. Ed Shea, OFM first among the friars; the ad footer reads "St. Mary's Church  |  03-1364".

## Worship sites

Page 2's MASS SCHEDULE (8 November 2026 and 1 November 2026 issues) gives Saturday Vigil 5:00 PM and 7:00 PM; Sunday 7:30 AM, 8:45 AM Espanol, "9:00 AM—English (Carnevale Center)", 10:30 AM, 12:00 PM; weekdays 8:00 AM and Wednesday 7:00 PM en Espanol. So two places:

- `st-mary-pompton-lakes`: the church, 17 Pompton Avenue.
- `carnevale-center-pompton-lakes`: the parish's Carnevale Center, where a weekly Sunday 9:00 AM Mass is held (and the sensory-friendly Masses on 15 November and 13 December). OSM puts it at 10 Lenox Avenue, about 100 m north of the church. It is a separate building with a regular public Sunday Mass, so it gets its own church row, though no roster lists it.

The finder (directory:21395) and GCatholic (18987) list only the church.

## Website and bulletin provider

`stmarys-pompton.org` is the parish's eCatholic site (id 21395), behind Cloudflare; visit.py read `/bulletins` on 2026-11-04: it posts copies of the LPi issue as `files.ecatholic.com/21395/bulletins/<YYYYMMDD>.pdf` (newest 1 November). As with other LPi copies here, the ParishesOnline org was found with `probe po st-marys-church-07442`; the container already carries the 8 November issue, so the row reads ParishesOnline by org slug. `fetch:check` on 2026-11-04 picked `03/1364/20261108B.pdf` (freshness future, age -4 days: next Sunday's issue, the right pick; identity unverified because no expected identity is supplied). The eCatholic id is the website's and is not recorded as a publication.

## Not yet confirmed

Nothing open.
