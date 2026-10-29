---
name: St. John the Evangelist Parish
website: https://www.stjohnpa.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067
publication: ['url:https://www.church-bulletin.org/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 193, 'Saint John the Evangelist Roman Catholic Parish', Morrisville, PA 19067;
    latest edition October 25, 2026, then 2026-10-18 and 2026-10-11.
- url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (8 pages, image only: pdftotext gives 8 characters; page 1 rendered at
    60 dpi and read). Masthead ''ST. JOHN THE EVANGELIST ROMAN CATHOLIC PARISH, WWW.STJOHNPA.ORG''; ''PARISH
    CLERGY: Deacon John Teson, Pastoral Life Director; Reverend Eugene Wilson and Reverend Jacob John,
    Pastoral Associate; Reverend David Friel, Weekend Assistant; Deacon Thomas Cusick; Deacon James E.
    Hartmann (Retired)''; ''OUR MASS SCHEDULE: Sunday Vigil Mass: Saturday 4:00 PM; Sunday: 7:30, 9:30
    and 11:30 AM; Weekdays Monday - Saturday 8:00 AM; Holy Day Vigil 5:30 PM; Holy Day 8:00 AM and 7:00
    PM''; ''PASTORAL LIFE CENTER (Parish Office) 752 Big Oak Road, Morrisville, PA 19067, 215.295.4102,
    4103''. Names this parish alone. Adoration Monday-Friday after the daily Mass; Miraculous Medal Novena
    Saturdays 8:00 AM Mass; Wednesdays Lectio Divina 8:30 AM ''in the Chapel''.'
- url: https://stjohnpa.org/
  seen: 2026-10-29
  note: 'probe url: 200, title ''St. John the Evangelist Catholic Church |Morrisville, PA''. Bulletin
    links: https://www.jppc.net/onlinebulletins/193template.pdf (the listing) and self-uploaded stjohnpa.org/wp-content/uploads/2026-10-18.pdf.pdf,
    2026-10-11 and 2026-10-04: the site''s own archive is a week behind the listing (newest 18 October),
    so the listing is the channel.'
- url: https://archphila.org/parish/st-john-the-evangelist-morrisville/
  seen: 2026-10-28
  quote: Deacon John Teson (Parish Life Director)
  note: 'Directory: church ''Big Oak and Makefield Rds.''; rectory 752 Big Oak Rd., Morrisville 19067;
    Mass Sat 4 PM, Sun 7:30, 9:30, 11:30 AM, weekdays 8 AM, Saturdays 8 AM, as the bulletin.'
promoted: 2026-10-29
research:
- method: Read listing 193, rendered page 1 of the 25 October image-only issue, read the 2 August text-layer
    issue and the parish home page
  url: https://www.church-bulletin.org/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
publication_reviews:
- parish: holy-trinity-morrisville
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067/2026-10-25.pdf
    seen: 2026-10-29
    note: 25 October 2026 masthead (page 1, image rendered) names St. John the Evangelist Roman Catholic
      Parish alone, with its own Mass schedule (Sat vigil 4:00 PM; Sun 7:30, 9:30, 11:30 AM). 8 pages,
      md5 02bb18c19f89c46b7b04e9fd36e75e87.
  - url: https://www.church-bulletin.org/bulletin/holy-trinity-church-morrisville-pa-19067/2026-10-25.pdf
    seen: 2026-10-29
    note: 25 October 2026 masthead 'HOLY TRINITY CHURCH, Morrisville' with its own Masses box (Sun 7:30,
      9:30, 11:00 a.m.); 4 pages, md5 fb55732b0caae06e3edca058283ee138. Same Parish Life Director, different
      issue.
---

## Publisher

St. John the Evangelist Parish, Morrisville, prints with John Patrick Publishing: listing 193 (`church-bulletin.org/?id=193`) has an issue for 25 October 2026 (image only). The parish home page links the jppc template for 193 and a self-upload archive that is a week behind (newest 18 October), so the row is `other`, `page-pdfs` on the listing.

**One bulletin or two with Holy Trinity, Morrisville?** Two. Deacon John Teson is Parish Life Director of both since July 2026, and the clergy list on page 1 is the same, but each issue has its own masthead, Mass schedule and page count (see `publication_reviews` and Holy Trinity's record). Shared leadership is not a joint bulletin.

## Worship sites

One: St. John the Evangelist Church, Big Oak and Makefield Roads. The Mass schedule box lists no other place; the Pastoral Life Center (752 Big Oak Road) is the parish office and hall, and 'the Chapel' is where the Wednesday Lectio Divina is held, with no Mass of its own listed.

## Website and bulletin provider

stjohnpa.org is the parish's own site; its self-uploaded files lag the listing. Recipe `page-pdfs https://www.church-bulletin.org/saint-john-the-evangelist-roman-catholic-parish-morrisville-pa-19067`.

## Not yet confirmed

Only page 1 of the image-only 25 October issue was rendered, so later pages were not read for another Mass location.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (issue age 4 days, date inferred from the listing's file name); identity `unverified` because the check is given no expected identity (the masthead and Mass schedule were read from the rendered page 1 above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
