---
name: St. Hedwig
website: https://www.sthedwigde.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-hedwig-church-wilmington-de-19805
publication: ['url:https://www.church-bulletin.org/saint-hedwig-church-wilmington-de-19805']
group: City Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-hedwig-church-wilmington-de-19805/2026-10-25.pdf
  seen: 2026-10-27
  quote: 408 S. Harrison Street, Wilmington, Delaware, 19805
  note: 'Page 1 of the 25 October 2026 issue (6 pages): ''St. Hedwig Church'', ''Fr. Janusz Brembor Administrator'',
    ''Deacon Ray Zolandz''. Mass schedule Saturday 4:00 p.m.; Sunday 9:00 a.m., 11:30 a.m. (Polish), 4:00
    p.m.; weekdays Monday-Friday 6:30 p.m. and Saturday 8:00 a.m. in the Pope Saint John Paul II Chapel;
    First Friday 6:30 p.m. Names this parish alone.'
- url: https://www.church-bulletin.org/bulletin/saint-hedwig-church-wilmington-de-19805/2026-10-25.pdf
  seen: 2026-10-27
  quote: 317 St. Hedwig, Wilmington, DE (b)
  note: 'Page 6 running head: 317 is the John Patrick Publishing number, ''John Patrick Publishing Company,
    Inc. (800) 333-3166 • www.jppc.net''.'
- url: https://church-bulletin.org/?id=317
  seen: 2026-10-27
  note: 'probe url: redirects to https://www.church-bulletin.org/saint-hedwig-church-wilmington-de-19805
    (''Saint Hedwig Church Bulletin''), which lists dated PDFs newest first (2026-10-25, 10-18, 10-11,
    10-04, 09-27 ...). The parish''s home page links it as https://church-bulletin.org/?id=317.'
- url: https://www.sthedwigde.org/bulletin
  seen: 2026-10-27
  note: The parish's own Duda 'Bulletin' page lists only 2024 files (317.12292024w.pdf back to 317.10062024w-bd0dd345.pdf);
    its newest was 29 December 2024, so it is stale and is not the pick.
---

## Publisher

St. Hedwig publishes through John Patrick Publishing (no. 317). The home page links https://church-bulletin.org/?id=317, which redirects to the church-bulletin.org listing of dated PDFs. The 25 October 2026 issue names St. Hedwig alone (Fr. Janusz Brembor, Administrator). The site's own /bulletin and /bulletin-2025 pages stop in 2024-2025 and are not used.

## Worship sites

One church, 408 S. Harrison Street, Wilmington. The bulletin's schedule adds the Pope Saint John Paul II Chapel for weekday Masses; the 25 October cover places it with the parish ('Weekday Mass Schedule (in Pope Saint John Paul II Chapel)'), so it is part of the same parish complex rather than a separate worship site. Polish Mass Sunday 11:30 a.m.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing, as the playbook records for John Patrick bulletins.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-hedwig-wilmington` (2026-10-27): picked church-bulletin.org 2026-10-25.pdf; transport ok, document type PDF, freshness fresh (2 days). Identity is 'unverified' to the tool; the masthead read above settles it. The pinned recipe is already in `provider_id`.

## Not yet confirmed

Where the chapel stands within the complex is not stated in the bulletin; it is treated as inside the church property.
