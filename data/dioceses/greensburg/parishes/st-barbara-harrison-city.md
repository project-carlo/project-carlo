---
name: St. Barbara Parish, Harrison City
website: https://www.stbarbara.org
bulletin_provider: discover_mass
provider_id: st-barbara-harrison-city-pa
publication: ['discovermass:st-barbara-harrison-city-pa']
group: 'Shared pastor: St. Barbara, Harrison City + St. Regis, Trafford'
evidence:
- url: https://discovermass.com/church/st-barbara-harrison-city-pa/
  seen: 2026-10-22
  quote: St. Barbara Current Bulletin Oct 18, 2026
  note: 'Discover Mass church page (J.S. Paluch) with weekly issues back to Aug 2, 2026 (Aug 2 ... Oct 11,
    Oct 18). Read once with curl. The Oct 18 issue (downloaded once via its tokenised link, 2026-10-22) has
    the masthead "ST. BARBARA CATHOLIC CHURCH ... October 18, 2026 ... 111 Raymaley Rd. Harrison City, PA
    15636 724-744-7474" and Mass times "SATURDAY 5:30PM Vigil, SUNDAY 8:00AM /10:30AM ... Daily Mass Mon–Fri
    9:00AM". It names St. Barbara alone; the pastor''s letter says "I am the pastor/administrator at St.
    Regis and St. Barbara".'
- url: https://www.stbarbara.org/bulletins
  seen: 2026-10-22
  note: 'eCatholic site (ecatholic:35057), 403 to plain fetches; opened headed with parish-site-access
    visit.py. Its bulletin list has one file, "July 30, 2023" (files.ecatholic.com/35057/bulletins/20230730.pdf),
    and a "Bulletin" menu link to https://discovermass.com/church/st-barbara-harrison-city-pa/#bulletin.'
- url: https://www.dioceseofgreensburg.org/official-april-11-2026/
  seen: 2026-10-22
  quote: Administrator of Saint Barbara Parish, Harrison City, Pennsylvania
  note: 'Father Daniel Carr, pastor of St. Regis, Trafford, made administrator of St. Barbara.'
---

## Publisher

St. Barbara Parish, Harrison City (directory 126) publishes its own weekly bulletin through J.S. Paluch's Discover Mass, church page `st-barbara-harrison-city-pa`. The 18 October 2026 issue (the current one on 2026-10-22; downloaded once) is headed "ST. BARBARA CATHOLIC CHURCH ... October 18, 2026 ... 111 Raymaley Rd. Harrison City, PA 15636" and names no other parish in its masthead or Mass times.

Since April 2026 the parish has been administered by Father Daniel Carr, pastor of St. Regis, Trafford (diocese Official post, 11 Apr 2026). His letter in this issue says "I am the pastor/administrator at St. Regis and St. Barbara". St. Regis publishes its own bulletin in ParishesOnline container 14/1158 (row `st-regis-trafford`), whose 25 Oct 2026 masthead names St. Regis alone and mentions St. Barbara only as a venue for shared youth events. Both channels are live and each names one parish, so these are two rows.

## Worship sites

One church: St. Barbara, 111 Raymaley Road, Harrison City, with "SATURDAY 5:30PM Vigil, SUNDAY 8:00AM /10:30AM" and daily Mass Mon-Fri 9:00 AM in the 18 Oct 2026 issue. GCatholic (24120) and the directory (126) list no other site. The issue's Mass-times box also lists "6:00PM Mother of Sorrows": that is the Sunday evening Mass at Mother of Sorrows, Murrysville, which belongs to the row `st-john-st-mary-mother-of-sorrows-export`. It is a pointer for parishioners, not a St. Barbara site.

## Website and bulletin provider

`discover_mass`, provider_id `st-barbara-harrison-city-pa`: the parish's own site links its "Bulletin" menu item to this Discover Mass page, which had weekly issues from 2 Aug to 18 Oct 2026. Website https://www.stbarbara.org, the directory's homepage for the parish: an eCatholic site (35057) behind bot-blocking, whose own bulletin list stopped at 30 July 2023 and is not recorded as a publication. The LPi organization `st-barbara-church-15636` (0018000000QxBzwAAF) exists but `probe po` listed no issues on 2026-10-22: an empty organization, not a channel.

## Not yet confirmed

Discover Mass caps downloads per IP per day, so `fetch:check` may report `not_pdf` on a day the bulletin was already downloaded.
