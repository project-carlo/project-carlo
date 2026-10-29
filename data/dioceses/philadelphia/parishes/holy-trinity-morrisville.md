---
name: Holy Trinity Parish
website: https://www.holytrinitymorrisville.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/holy-trinity-church-morrisville-pa-19067
publication: ['url:https://www.church-bulletin.org/holy-trinity-church-morrisville-pa-19067']
group: ''
evidence:
- url: https://www.church-bulletin.org/holy-trinity-church-morrisville-pa-19067
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 9, 'Holy Trinity Church', Morrisville, PA 19067; latest edition October 25,
    2026, then 2026-10-18 and 2026-10-11.
- url: https://www.church-bulletin.org/bulletin/holy-trinity-church-morrisville-pa-19067/2026-10-25.pdf
  seen: 2026-10-29
  quote: Deacon John Teson
  note: '25 October 2026 issue (4 pages, text layer; some small-capital title lines are garbled by font
    substitution). Page 1 masthead ''HOLY TRINITY CHURCH, Morrisville, Pennsylvania'', lists ''Rev. Monsignor
    John C. Eckert'', ''Deacon John Teson'' (title line garbled, read as Parish Life Director from the
    directory and the rectory e-mail Parishlifedirector@Holytrinitypa.com), Rev. Jacob John and Rev. Eugene
    Wilson (parochial vicars), 201 N. Pennsylvania Avenue, 215-295-3045. MASSES box: daily Mon/Wed/Fri/Sat
    9:00 a.m., Tue/Thu 7:00 p.m.; Sunday vigil 5:30 p.m. Saturday, 7:30, 9:30 and 11:00 a.m.; holydays
    9:00 a.m. and 7:00 p.m. Footer ''HOLY TRINITY CHURCH - OCTOBER 25, 2026''. Names this parish alone,
    with no St. John Mass times.'
- url: https://www.holytrinitymorrisville.org
  seen: 2026-10-29
  note: 'probe url answered HTTP 403; opened in Chrome (visit.py --bulletin): 200, title ''Holy Trinity
    Catholic Church | Morrisville, PA'', links only http://www.jppc.net/onlinebulletins/009template.pdf
    (the listing''s template) and embeds ecatholic:1047, which hosts no bulletin files that visit could
    follow (no /bulletins link).'
- url: https://archphila.org/parish/holy-trinity-morrisville/
  seen: 2026-10-28
  quote: Deacon John Teson (Parish Life Director)
  note: 'Directory page: Pastor line ''Deacon John Teson (Parish Life Director)'', parochial vicars Rev.
    Eugene C. Wilson and Rev. Jacob John; church and rectory 201 N. Pennsylvania Ave., Morrisville 19067;
    Mass times Sat 5:30 PM, Sun 7:30, 9:30, 11 AM match the bulletin.'
promoted: 2026-10-29
research:
- method: Read listing 9, the 25 October text layer, and the parish home page in Chrome; compared with
    St. John's listing 193 issue
  url: https://www.church-bulletin.org/holy-trinity-church-morrisville-pa-19067
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
publication_reviews:
- parish: st-john-the-evangelist-morrisville
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/holy-trinity-church-morrisville-pa-19067/2026-10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead names Holy Trinity Church, Morrisville alone, with its own Masses
      box (Sat vigil 5:30 p.m.; Sun 7:30, 9:30, 11:00 a.m.). 4 pages, md5 fb55732b0caae06e3edca058283ee138.
      It mentions Holy Trinity & St. John CYO only as a joint youth program.
  - url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067/2026-10-25.pdf
    seen: 2026-10-29
    note: '25 October 2026 issue (8 pages, image only, page 1 rendered): masthead ''ST. JOHN THE EVANGELIST
      ROMAN CATHOLIC PARISH, www.stjohnpa.org'', own Mass schedule (Sat vigil 4:00 PM; Sun 7:30, 9:30,
      11:30 AM), Pastoral Life Center 752 Big Oak Road. A different PDF (md5 02bb18c19f89c46b7b04e9fd36e75e87).'
---

## Publisher

Holy Trinity Parish, Morrisville, prints with John Patrick Publishing: listing 9 (`church-bulletin.org/?id=9`) has an issue for 25 October 2026 with a text layer, and the parish home page links only the jppc template for 009. The row is `other`, `page-pdfs` on the listing. The issue's masthead and Masses box name this parish alone.

**One bulletin or two with St. John the Evangelist, Morrisville?** Two. Deacon John Teson has been Parish Life Director of both since July 2026 (directory; CatholicPhilly 2026-07-22), and Holy Trinity's masthead lists him, but each parish still publishes its own issue under its own listing (9 and 193): different mastheads, different page counts (4 and 8), different Mass schedules and different md5. Holy Trinity's issue carries no St. John Mass times; the two share a youth program ('Holy Trinity & St. John's CYO'), which is content, not a joint bulletin. See `publication_reviews`.

## Worship sites

One: Holy Trinity Church, 201 N. Pennsylvania Avenue. The Masses box lists no other place. 'Trinity Hall' (rectory basement) and Holy Trinity School are meeting places, not Mass sites.

## Website and bulletin provider

holytrinitymorrisville.org is the parish's own site (403 to `probe url`, loads in Chrome), an eCatholic site (id 1047) that links the John Patrick template and hosts no bulletin files. Recipe `page-pdfs https://www.church-bulletin.org/holy-trinity-church-morrisville-pa-19067`.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (issue age 4 days, date inferred from the listing's file name); identity `unverified` because the check is given no expected identity (the masthead and Mass schedule were read from the text layer above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
