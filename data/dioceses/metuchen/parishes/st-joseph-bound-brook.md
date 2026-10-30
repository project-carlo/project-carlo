---
name: St. Joseph Catholic Community
website: https://www.dreamsofstjoseph.org
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/557
publication: ['url:https://www.church-bulletin.org/saint-joseph-catholic-community-bound-brook-nj-08805']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-joseph-catholic-community-bound-brook-nj-08805/2026-10-25.pdf
  seen: 2026-10-30
  quote: ST. JOSEPH CATHOLIC COMMUNITY
  note: 'Page 1 of the 25 October 2026 issue: the masthead names St. Joseph Catholic Community alone,
    above its own MASSES AND SERVICES (Saturday 5:00 pm English; Sunday 8:00 am English).'
- url: https://www.church-bulletin.org/bulletin/saint-joseph-catholic-community-bound-brook-nj-08805/2026-11-01.pdf
  seen: 2026-10-30
  quote: Joseph Kerrigan Habla Español
  note: 'Page 1 of the 1 November 2026 issue (already posted): Mass schedule Saturday 5:00 pm English
    and 7:00 Español, Sunday 8:00 am English and 12:00 pm Español, weekdays 8:30 am; staff list gives
    Joseph Kerrigan as Pastor. A grep for Czestochowa found nothing.'
- url: https://church-bulletin.org/?id=557
  seen: 2026-10-30
  note: John Patrick Publishing listing for St. Joseph Catholic Community, Bound Brook, NJ 08805 (redirects
    to church-bulletin.org/saint-joseph-catholic-community-bound-brook-nj-08805); newest issue 2026-11-01,
    one issue per Sunday back to 2024-11-03.
- url: https://www.dreamsofstjoseph.org/news-and-contacts/weekly-bulletin/
  seen: 2026-10-30
  note: The parish's own Weekly Bulletin page links https://church-bulletin.org/?id=557.
bulletin_status: available
---

## Publisher

St. Joseph Catholic Community (124 East Second Street, Bound Brook) publishes its own weekly bulletin through John Patrick Publishing, listing id 557. I read the 25 October and 1 November 2026 issues (the latter is already posted on 30 October). Page 1 of each gives one Mass schedule (Saturday 5:00 pm English, 7:00 Español; Sunday 8:00 am English, 12:00 pm Español; weekdays 8:30 am English, Tuesday to Friday 7:00 pm Español) and the staff list names Joseph Kerrigan as Pastor. No other church is named, and a grep of the 1 November issue for Czestochowa found nothing; it does not mention Our Lady of Mercy except in an unrelated sentence about God's mercy.

The finder lists Rev. Msgr. Joseph J. Kerrigan as pastor, with Rev. Pauly Thekkan in residence and three deacons; the bulletin's staff list agrees on the pastor and deacons.

## Worship sites

One church, 124 East Second Street (`st-joseph-bound-brook`; directory:24472, gcatholic:18662). The bulletin's schedule names no chapel or mission. The "Contemplative Practice" times on the same page are prayer sessions, not Mass.

## Website and bulletin provider

The parish site (www.dreamsofstjoseph.org; the finder's dreamsofstjoseph.org redirects there) links `https://church-bulletin.org/?id=557` on its Weekly Bulletin page. Provider `other`, recipe `page-pdfs https://church-bulletin.org/557`, as Allentown records John Patrick Publishing. The listing page names its files `bulletin/saint-joseph-catholic-community-bound-brook-nj-08805/<YYYY-MM-DD>.pdf`. See the fetch check below.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved `page-pdfs` on the church-bulletin.org listing and picked `bulletin/saint-joseph-catholic-community-bound-brook-nj-08805/2026-11-01.pdf`: transport ok, PDF, issue date 2026-11-01 read from the document text ("NOVEMBER 1, 2026"), freshness `future` (two days ahead; John Patrick posts the coming Sunday early). Publication identity was not machine-checked; I read the masthead of the 25 October issue (above) and the 1 November Mass schedule myself.

## Not yet confirmed

Nothing outstanding beyond the fetch check result.
