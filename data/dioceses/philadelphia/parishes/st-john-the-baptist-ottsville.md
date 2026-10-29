---
name: St. John the Baptist Parish
website: https://stjohnsottsville.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-roman-catholic-church-of-saint-john-the-baptist-parish-ottsville-pa-18942
publication: ['url:https://www.church-bulletin.org/the-roman-catholic-church-of-saint-john-the-baptist-parish-ottsville-pa-18942']
group: ''
evidence:
- url: https://www.church-bulletin.org/the-roman-catholic-church-of-saint-john-the-baptist-parish-ottsville-pa-18942
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 232, 'The Roman Catholic Church of Saint John the Baptist Parish', Ottsville,
    PA 18942, 4050 Durham Road, phone (610) 847-5521; latest edition October 25, 2026, dated archive back
    to November 2024.
- url: https://www.church-bulletin.org/bulletin/the-roman-catholic-church-of-saint-john-the-baptist-parish-ottsville-pa-18942/2026-10-25.pdf
  seen: 2026-10-29
  quote: The Roman Catholic Church of St. John the Baptist Parish
  note: '25 October 2026 issue (8 pages, text layer). Masthead names this parish alone (''4050 Durham
    Road, Ottsville, PA 18942''; ''Administered by the Missionaries of the Sacred Heart''); page 1 ''Pastor:
    Rev. Selvaraj Lucas, M.S.C.''.'
- url: https://www.church-bulletin.org/bulletin/the-roman-catholic-church-of-saint-john-the-baptist-parish-ottsville-pa-18942/2026-10-25.pdf
  seen: 2026-10-29
  quote: 'Mon- Fri: 9:00am (Thursday at old St. John’s Church)'
  note: 'Page-1 Mass times: Saturday Vigil 4:30pm, Sunday 8:00am & 10:30am, Monday-Friday 9:00am with
    the Thursday Mass at old St. John''s Church, Holy Days 9:00am & 7:00pm.'
- url: https://stjohnsottsville.org/
  seen: 2026-10-29
  quote: Thurs. 9am Mass at Old St. John Church, Haycock
  note: 'Parish site (WordPress, ''Proudly Designed and Hosted by John Patrick Publishing Company''):
    its Mass Schedule box repeats the Thursday Mass at Old St. John''s; the page links jppc.net/onlinebulletins/232template.pdf
    as the Current Bulletin and holds no bulletin PDFs of its own.'
- url: https://archphila.org/parish/st-john-the-baptist-ottsville/
  seen: 2026-10-29
  quote: St. Joseph's Daily Chapel
  note: 'Directory (page updated 2 years ago): Vigil Saturdays 5 PM, Sundays 8 and 10:30 AM, weekdays
    8:35 AM ''St. Joseph''s Daily Chapel''; pastor Rev. Selvaraj Lucas, M.S.C.; cemetery 453 Haycock Run
    Rd., Kintnersville 18930. Older than the bulletin, which gives 4:30 PM, 9:00 AM and the Thursday Mass
    at Old St. John''s; the bulletin was followed.'
research:
- method: probe pdf text of the 25 October 2026 issue and probe get of the parish site
  url: https://stjohnsottsville.org/
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. John the Baptist Parish, Ottsville (Rev. Selvaraj Lucas, M.S.C., Pastor; administered by the Missionaries of the Sacred Heart) prints its bulletin with John Patrick Publishing: listing 232 has the 25 October 2026 issue, which has a text layer, and its masthead names this parish alone. The parish site is John Patrick-hosted and links the listing's template PDF; it carries no files of its own. The row is `other`, `page-pdfs` on the listing.

## Worship sites

Two places hold Mass. The church at 4050 Durham Road holds every weekend and weekday Mass. **Old St. John's Church** at the base of Haycock Mountain (the 1855 church, per the parish history page) holds the Thursday 9:00am weekday Mass, named in both the bulletin and the parish site: a weekly public Mass, so it is a church row of its own (`old-st-johns-haycock`). Its address is not given by the bulletin or the parish site; the directory's cemetery line (453 Haycock Run Rd., Kintnersville 18930) is the cemetery 'surrounding Old St. John's' per the parish history page, so it is used with `address_verified` false. The directory's 'St. Joseph's Daily Chapel' (weekday 8:35 AM) appears in neither the bulletin nor the site; the bulletin's weekday time is 9:00am at the church. St. Joseph's Marienstein mission closed in 2000 and was sold (parish history page, 'In 2000 St Joseph church was closed and the building sold'); St. Lawrence, Riegelsville has been a separate parish since 1974 (its own row, `st-lawrence-riegelsville`).

## Website and bulletin provider

`https://stjohnsottsville.org` is a John Patrick-hosted WordPress site. Directory Mass times (Saturday vigil 5 PM, weekdays 8:35 AM) are older than the bulletin and the site (vigil 4:30pm since 1 November 2025).

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (4 days, date inferred from the file name); identity `unverified` because no expected identity is supplied by the check (the text-layer masthead was read above). It printed no `recipe` line, as the pinned `provider_id` already holds it.

## Not yet confirmed

Pages 2-8 of the bulletin were not read beyond the Mass box.
