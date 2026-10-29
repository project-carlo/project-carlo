---
name: St. Frances Cabrini Parish
website: https://www.saintfrancescabrini.net
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-frances-cabrini-parish-fairless-hills-pa-19030
publication: ['url:https://www.church-bulletin.org/saint-frances-cabrini-parish-fairless-hills-pa-19030']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-frances-cabrini-parish-fairless-hills-pa-19030
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 228, 'Saint Frances Cabrini Parish', Fairless Hills, PA 19030; latest edition
    October 25, 2026, then 2026-10-18 and 2026-10-11.
- url: https://www.church-bulletin.org/bulletin/saint-frances-cabrini-parish-fairless-hills-pa-19030/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (8 pages, image only; page 1 rendered at 60 dpi and read). Masthead ''ST.
    FRANCES CABRINI PARISH, Come and See, 325 S. Oxford Valley Road, Fairless Hills, PA 19030''; ''Rev.
    Msgr. Michael P. McCormac, Pastor'', Deacon Mace M. Mazzoni, Rev. Msgr. Michael K. Magee, Weekend
    Assistant; ''Mass Schedule: Saturday Evening Vigil: 5:30 PM; Sunday: 7:00, 9:00 & 11:00 AM; Monday
    - Saturday: 9:30 AM; Holy Days: 6:30 AM, 12:00 Noon, 7:00 PM''; ''Daily Adoration of the Blessed Sacrament,
    Saint Joseph Chapel, Monday - Saturday: 8:00 AM - 8:00 PM, Sunday: 12:30 PM - 8:00 PM''; Holy Family
    Regional Catholic School, 2477 Trenton Road, Levittown. Names this parish alone.'
- url: https://www.church-bulletin.org/bulletin/saint-frances-cabrini-parish-fairless-hills-pa-19030/2026-08-02.pdf
  seen: 2026-10-29
  quote: Daily Adoration of the Blessed Sacrament
  note: The 2 August 2026 issue has a text layer and the same cover box (Mass schedule, 'Saint Joseph
    Chapel' adoration hours). Its text names no Mass in the chapel and no Fallsington church.
- url: https://saintfrancescabrini.net/parish-bulletin/
  seen: 2026-10-29
  note: probe url on www.saintfrancescabrini.net answered 200 (it gave HTTP 500 to the survey on 2026-10-28;
    see the playbook). The Parish Bulletin page links only https://www.jppc.net/onlinebulletins/228template.pdf
    (the listing), a stewardship booklet and a history PDF, plus a livestream Mass block; the listing
    is the channel.
- url: https://archphila.org/parish/st-frances-cabrini-fairless-hills/
  seen: 2026-10-28
  quote: 'Merged with St. Joseph the Worker, Fallsington: 2014'
  note: 'Directory: Pastor Rev. Msgr. Michael P. McCormac; church ''Oxford Valley Rd. and Southway Dr.'';
    rectory 325 S. Oxford Valley Rd., Fairless Hills 19030; Mass times as in the bulletin.'
research:
- method: Read listing 228, rendered page 1 of the 25 October image-only issue, the 2 August text layer,
    the parish site's bulletin and adoration pages
  url: https://www.church-bulletin.org/saint-frances-cabrini-parish-fairless-hills-pa-19030
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Frances Cabrini Parish, Fairless Hills, prints with John Patrick Publishing: listing 228 (`church-bulletin.org/?id=228`) has an issue for 25 October 2026 (image only), and the parish site's Parish Bulletin page links only the jppc template for 228. The row is `other`, `page-pdfs` on the listing. The masthead and Mass schedule name this parish alone.

## Worship sites

One church: St. Frances Cabrini, Oxford Valley Road at Southway Drive (the bulletin and the directory give the rectory, 325 S. Oxford Valley Road). **St. Joseph the Worker, Fallsington**, absorbed in 2014 as a worship site, is closed: relegated to profane but not sordid use effective 1 November 2015 (see its excluded record), and the current bulletin's Mass schedule lists no Fallsington Mass. The 'Saint Joseph Chapel' on the bulletin cover is the adoration chapel on the first floor of the Parish Center, 2 Goble Court, Fairless Hills ('just around the corner from our church', parish site); it has adoration hours and no Mass line, so it is not a church row.

## Website and bulletin provider

saintfrancescabrini.net (shared WordPress host) answered 500 on 2026-10-28 and 200 on 2026-10-29; its bulletin page links the listing only. Recipe `page-pdfs https://www.church-bulletin.org/saint-frances-cabrini-parish-fairless-hills-pa-19030`.

## Not yet confirmed

Only page 1 of the image-only 25 October issue was rendered; the 2 August text issue was searched for 'chapel', 'Fallsington' and 'Joseph' and shows no Mass at the chapel or elsewhere.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (issue age 4 days, date inferred from the listing's file name); identity `unverified` because the check is given no expected identity (the masthead and Mass schedule were read from the rendered page 1 above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
