---
name: St. Nicholas, Palisades Park
website: https://stnicholasrcchurch.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6046
publication: ['url:https://www.church-bulletin.org/saint-nicholas-r-c-church-palisades-park-nj-07650']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-nicholas-r-c-church-palisades-park-nj-07650/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 6 pages, image only (no text layer; read with render.py). Page 1 masthead:
    ''ST. NICHOLAS RC CHURCH'', ''Served by the Vocationist Fathers'', Fr. Khin ''Firmin'' Maung Htwe,
    S.D.V., Pastor; ''Church & Rectory 442 East Brinkerhoff Ave Palisades Park, NJ 07650''; ''Solemnity
    of All Saints November 1, 2026''. Mass schedule: Saturday 7:00 AM & 8:00 AM (English), 5:00 PM Vigil
    (English); Sunday 7:30 AM, 9:30 AM (English), 11:00 AM (Italian), 12:30 PM (English), 6:00 PM (Portuguese);
    weekdays 7:00 & 8:00 AM. Page 6 footer: ''6046 St. Nicholas, Palisades Park, NJ (B)'' and ''John Patrick
    Publishing Co.'''
- url: https://church-bulletin.org/6046
  seen: 2026-11-03
  note: 'Redirects to church-bulletin.org/saint-nicholas-r-c-church-palisades-park-nj-07650, ''Saint Nicholas
    R.C. Church Bulletin'': dated issues 2026-11-01, 10-25, 10-18, 10-11, 10-04, 09-27.'
- url: https://stnicholasrcchurch.org/
  seen: 2026-11-03
  note: Parish WordPress site (probe get). Links http://www.jppc.net/onlinebulletins/6046template.pdf
    and self-hosted copies that stop in April 2024 (wp-content/uploads/2024/04/6046bulletin042124.pdf).
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Nicholas, Palisades Park, publishes a weekly bulletin printed by John Patrick Publishing (id 6046). I read the 1 November 2026 issue (6 pages, all images; read with render.py): page 1 masthead 'ST. NICHOLAS RC CHURCH', 'Served by the Vocationist Fathers', Fr. Khin 'Firmin' Maung Htwe, S.D.V., Pastor, 'Church & Rectory 442 East Brinkerhoff Ave Palisades Park, NJ 07650', 'Solemnity of All Saints November 1, 2026', with one Mass schedule for one church; page 6 footer '6046 St. Nicholas, Palisades Park, NJ (B)', 'John Patrick Publishing Co.'. It does not name St. Michael, Palisades Park, which prints its own bulletin with LPi.

## Worship sites

- St. Nicholas, 442 East Brinkerhoff Avenue (`st-nicholas-palisades-park`): Saturday 7:00 and 8:00 AM, 5:00 PM vigil; Sunday 7:30 AM, 9:30 AM, 11:00 AM (Italian), 12:30 PM, 6:00 PM (Portuguese); weekdays 7:00 and 8:00 AM.

The directory (166) and GCatholic (18532) list only this church.

## Website and bulletin provider

https://stnicholasrcchurch.org/ (the directory's site) is a WordPress site. It links the John Patrick template jppc.net/onlinebulletins/6046template.pdf, and its own uploaded copies stop at 21 April 2024, so the row reads the John Patrick listing: provider `other`, `page-pdfs https://church-bulletin.org/6046`. GCatholic's website http://www.saintnicholasparish.info does not resolve (probe get: 'no such host', 2026-11-03); it is not used. The bulletin is image-only, so the pipeline will need to read it as images.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/6046: current` and picked church-bulletin.org/bulletin/saint-nicholas-r-c-church-palisades-park-nj-07650/2026-11-01.pdf, the 1 November 2026 issue read above (date 2026-11-01); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row.
