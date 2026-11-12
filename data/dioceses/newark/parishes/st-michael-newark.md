---
name: St. Michael's Parish, Newark
website: https://stmichaelsparish.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6052
publication: ['url:https://www.church-bulletin.org/saint-michael-s-parish-newark-nj-07104']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-michael-s-parish-newark-nj-07104/2026-11-01.pdf
  seen: 2026-11-04
  quote: 172 Broadway, Newark, NJ 07104
  note: '1 November 2026 issue (4 pages, text layer). Page 1 masthead: St. Michael''s Parish, ''Staffed
    by the VOCATIONIST FATHERS'', Rev. Robinson Gonzalez, S.D.V., Pastor; Weekday Masses 8:00 AM (English
    in Chapel), 7:00 PM (Spanish in Chapel); Saturday 8:00 AM (English in Chapel), 7:00 PM (Spanish in
    Church); Sunday 8:30 AM & 11:30AM (English), 7:00 AM, 10:00 AM & 1:00 PM (Spanish). Page 4 footer:
    ''6052 St. Michael''s Parish, Newark, NJ (B) John Patrick Publishing Co.'''
- url: https://church-bulletin.org/6052
  seen: 2026-11-04
  note: 'Redirects to church-bulletin.org/saint-michael-s-parish-newark-nj-07104, "Saint Michael''s Parish
    Bulletin": dated issues 2026-11-01, 10-25, 10-18, 10-11, 10-04, 09-27 and earlier.'
- url: https://stmichaelsparish.org/weekly-bulletins/
  seen: 2026-11-04
  note: 'Parish WordPress site (''Saint Michael''s Parish - Staffed by the Vocationist Fathers''), read
    with visit.py (probe url: UNREACHABLE through the proxy). The Weekly Bulletins page links https://www.jppc.net/onlinebulletins/6052template.pdf.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Michael's Parish, Newark, staffed by the Vocationist Fathers, publishes a weekly bulletin printed by John Patrick Publishing (id 6052). I read the 1 November 2026 issue (4 pages, text): page 1 masthead 'St. Michael's Parish, 172 Broadway, Newark, NJ 07104', Rev. Robinson Gonzalez, S.D.V., Pastor, with one Mass schedule; page 4 footer '6052 St. Michael's Parish, Newark, NJ (B) John Patrick Publishing Co.'. No other parish is named in the masthead or footer.

## Worship sites

- St. Michael Church, 172 Broadway (`st-michael-newark-nj`): Sunday 7:00 AM, 8:30 AM, 10:00 AM, 11:30 AM, 1:00 PM; Saturday 7:00 PM (Spanish, in church); weekday 8:00 AM and 7:00 PM 'in Chapel' (page 1, 1 November 2026).

The weekday Masses are 'in Chapel'. The bulletin gives no separate address for the chapel; I read it as a chapel in the parish buildings at 172 Broadway / 23 Crittenden Street, not a separate worship site (inferred, not confirmed). The directory (136) and GCatholic (18510) list only this church.

## Website and bulletin provider

https://stmichaelsparish.org/ is a WordPress site that `probe url` couldn't reach through the proxy (UNREACHABLE, RemoteDisconnected); `visit.py` loads it. Its Weekly Bulletins page links the John Patrick template `jppc.net/onlinebulletins/6052template.pdf`. GCatholic's website, saintmichaelparish.com, did not load (visit.py ERROR). Provider `other`, read with `page-pdfs https://church-bulletin.org/6052`.

Fetch check (2026-11-04, headed): transport ok, PDF, `page-pdfs on https://church-bulletin.org/6052: current` picked `saint-michael-s-parish-newark-nj-07104/2026-11-01.pdf`, the issue read above; issue date 2026-11-01, freshness fresh. Identity `unverified` only because no expected identity is supplied. The recipe is the one in `provider_id`.

## Not yet confirmed

Where the weekday 'Chapel' is: the bulletin gives no address for it. If a later issue gives it a separate address, it needs its own church row.
