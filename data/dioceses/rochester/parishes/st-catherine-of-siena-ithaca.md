---
name: St. Catherine of Siena Church
website: https://stcathofsiena.org
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:10905', 'po-container:03/1311']
group: ''
evidence:
- {url: 'https://files.ecatholic.com/10905/bulletins/20261004.pdf', seen: 2026-10-02, quote: 'St. Catherine
    of Siena, Ithaca, NY 03-1311', note: 'LPi ad-page footer of the 4 October 2026 issue (text layer;
    pages 1 to 14 are images). Page 1, rendered with render.py, reads "St. Catherine of Siena Roman Catholic
    Church ITHACA, NEW YORK / October 4, 2026 | Twenty-seventh Sunday of Ordinary Time / 309 SIENA DRIVE,
    ITHACA, NY 14850 | WWW.STCATHOFSIENA.ORG | PHONE: 607-257-2493". Page 2 "MASS SCHEDULE": Weekend Saturday
    5:00 p.m., Sunday 9:00 a.m.; Weekday Tuesday, Thursday, Friday 9:00 a.m.; First Saturday 9:00 a.m.
    at Immaculate Conception. recheck cannot find those image-only words.'}
- {url: 'https://stcathofsiena.org/bulletins', seen: 2026-10-02, quote: 'October 4, 2026', note: 'Bulletins
    page of the eCatholic site (site id 10905, behind Cloudflare; read with visit.py) lists one PDF per
    Sunday, newest 20261004.'}
promoted: 2026-10-02
---

## Publisher

St. Catherine of Siena, Ithaca, publishes its own bulletin: the 4 October 2026 issue is headed "St. Catherine
of Siena Roman Catholic Church, Ithaca, New York" with "309 Siena Drive". It is a single-church parish. The
bulletin is image-only: its pages have no text layer apart from LPi's advertising footer, so I read the
masthead and Mass schedule by rendering pages 1 and 2 (render.py). The pipeline will need to read it as an
image.

## Worship sites

`churches/st-catherine-of-siena-ithaca.md` only.

## Website and bulletin provider

An eCatholic site (id 10905; probe url gets a 403 from Cloudflare, visit.py loads it). `/bulletins` lists
`files.ecatholic.com/10905/bulletins/YYYYMMDD.pdf`. The LPi footer "St. Catherine of Siena, Ithaca, NY
03-1311" points at ParishesOnline container 03/1311, which also has a 4 October 2026 issue; I recorded it as a
second publication id on the footer's evidence alone and did not compare the two files.

## Not yet confirmed

The container 03/1311 issue was not compared with the eCatholic one (same ad pages, so almost certainly the
same bulletin).
