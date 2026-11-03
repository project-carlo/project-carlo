---
name: St. Aedan's, Jersey City
website: https://www.staedans.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6056
publication: ['url:https://www.church-bulletin.org/saint-aedan-s-church-jersey-city-nj-07306']
group: Planning Area E
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-aedan-s-church-jersey-city-nj-07306/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 6 pages, image only (render.py; recheck cannot find quotes). Page 1 masthead:
    ''Saint Aedan''s Church, Church: 800 Bergen Avenue · Jersey City, NJ | Parish Center: 39 Tuers Avenue
    · Jersey City, NJ'', ''November 1, 2026'', Father Asiel Rodriguez, Pastor. Mass Times: Saturday 9:00am
    (Chapel, 39 Tuers Ave), Evening Vigil 5:00pm; Sunday 9:00am (English), 11:00am (Español), 1:00pm (English);
    weekdays 12:10pm; Viernes 7pm (Español) en el Centro Parroquial. Page 6 footer: ''6056 St. Aedan''s
    Church, Jersey City, NJ … John Patrick Publishing Company''.'
- url: https://church-bulletin.org/6056
  seen: 2026-11-03
  quote: Latest Edition November 1, 2026 Bulletin
  note: Redirects to church-bulletin.org/saint-aedan-s-church-jersey-city-nj-07306, 'Saint Aedan's Church
    Bulletin', 800 Bergen Avenue, Jersey City, NJ 07306; issues 2026-08-23 through 2026-11-01. Found by
    scanning John Patrick ids (scratch/newark-map-1/tools/jp_scan.sh); the parish site does not link it.
- url: https://parishesonline.com/organization/st-aedan-s-r-c-church
  seen: 2026-11-03
  note: 'probe po: org ''Saint Aedan''s R.C. Church'', 800 Bergen Ave, lpi 0018000000QxABSAA3, container
    03/1045, latest issue 2026-08-16; probe container 03/1045 found nothing for 23 Aug-8 Nov (403 each
    week; a live container, 03/0649, answered for 8 Nov). The 16 Aug 2026 LPi issue (image only) has the
    same masthead and Mass times. The parish''s homepage ''Subscribe to Our Bulletin'' button still links
    this org. The John Patrick listing begins the next week, 23 Aug: the parish changed printers, so the
    LPi ids are not this bulletin''s now and are left out of publication.'
- url: https://www.staedans.org/
  seen: 2026-11-03
  note: 'Wix site (visit.py --text): MASSES Sunday 9 AM (English), 11 AM (Spanish), 1 PM (English); Saturday
    9:00 AM at the Parish Center Chapel, 5:00 PM; Monday to Friday 12:10 PM; 7:00 PM (Spanish) on Friday
    at the Parish Center Chapel. Weekly ''Announcements'' blog posts (latest 18 October) say ''take a
    bulletin''. No bulletin PDFs on the site.'
bulletin_status: available
---

## Publisher

St. Aedan's, Jersey City, publishes a weekly bulletin printed by John Patrick Publishing (id 6056) since 23 August 2026. I read the 1 November 2026 issue (image only, rendered with render.py): page 1 masthead 'Saint Aedan's Church, Church: 800 Bergen Avenue · Jersey City, NJ | Parish Center: 39 Tuers Avenue · Jersey City, NJ', dated November 1, 2026, Father Asiel Rodriguez, Pastor; page 6 footer '6056 St. Aedan's Church, Jersey City, NJ … John Patrick Publishing Company'.

Until 16 August 2026 the bulletin was printed by LPi (ParishesOnline org st-aedan-s-r-c-church, container 03/1045, same masthead). That container has no issue after 16 August, and the John Patrick listing starts on 23 August, so the parish changed printers. The LPi ids are kept in evidence, not in `publication`.

## Worship sites

- St. Aedan's Church, 800 Bergen Avenue (`st-aedan-jersey-city`): Saturday 5:00 PM vigil; Sunday 9:00 AM (English), 11:00 AM (Spanish), 1:00 PM (English); weekdays 12:10 PM.
- Parish Center Chapel, 39 Tuers Avenue (`st-aedan-parish-center-chapel-jersey-city`): Saturday 9:00 AM; Friday 7:00 PM (Spanish).

Both from the 1 November 2026 page-1 Mass Times box, and the parish homepage agrees. The directory (77) and GCatholic (18447) list only the church. DiscoverMass has a page 'St. Aedan's (St. Peter's University Church)' with no bulletins; Saint Peter's University's own campus chapel is not in this batch's rosters and was not checked.

## Website and bulletin provider

https://www.staedans.org/ is a Wix site with no bulletin files; its 'Subscribe to Our Bulletin' button still points to the stale ParishesOnline org. The provider is `other`, read with `page-pdfs https://church-bulletin.org/6056`. The issues are image only: the pipeline has to read them as images.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/6056: current` and picked church-bulletin.org/bulletin/saint-aedan-s-church-jersey-city-nj-07306/2026-11-01.pdf, the 1 November 2026 issue read above (date from the file name; the issue has no text layer); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open for the row.
