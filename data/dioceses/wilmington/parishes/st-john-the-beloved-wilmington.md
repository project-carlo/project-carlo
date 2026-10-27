---
name: St. John the Beloved
website: https://www.sjbde.org/
bulletin_provider: parishes_online
provider_id: st-john-the-beloved-parish
publication: ['po-org:st-john-the-beloved-parish', 'lpi:0018000000Qx8ywAAB', 'po-container:03/1288']
group: New Castle Deanery; pastor shared with St. Catherine of Siena, separate bulletin
evidence:
- url: https://container.parishesonline.com/bulletins/03/1288/20261025B.pdf
  seen: 2026-10-27
  quote: St. John the Beloved Parish, Wilminton, DE 03-1288
  note: 'Page 1 is an image (the PDF has text only on its last pages), rendered with render.py: masthead
    ''ST. JOHN THE BELOVED CATHOLIC CHURCH / REV. MICHAEL CHRISTOPHER VANNICOLA, PASTOR'', date ''OCTOBER
    25, 2026'', Mass schedule for this church alone (Sat 5:00pm; Sun 7:30am, 9:30am, 11:30am, 5:00pm;
    Mon-Sat 8:00am), parish address ''907 Milltown Road, Sherwood Park, Wilmington, DE 19808''. The quote
    is the LPi footer on page 12, which names the container.'
- url: https://parishesonline.com/organization/st-john-the-beloved-parish
  seen: 2026-10-27
  note: 'probe po: org ''St. John the Beloved Parish'', LPi id 0018000000Qx8ywAAB, container 03/1288,
    website www.sjbde.org, address 907 Milltown Rd; weekly issues, latest 2026-10-25.'
- url: https://www.sjbde.org/
  seen: 2026-10-27
  note: 'probe url: HTTP 200, title ''Home'', embeds lpi:0018000000Qx8ywAAB and po-org:st-john-the-beloved-parish;
    browser links point to parishesonline.com/publication-page/st-john-the-beloved-parish.'
publication_reviews:
- parish: st-catherine-of-siena-wilmington
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1288/20261025B.pdf
    seen: 2026-10-27
    quote: St. John the Beloved Parish, Wilminton, DE 03-1288
    note: 'St. John''s 25 October 2026 issue (container 03/1288): its own masthead and Mass schedule (page
      1, image), pastor Rev. Michael Christopher Vannicola.'
  - url: https://container.parishesonline.com/bulletins/03/1410/20261025B.pdf
    seen: 2026-10-27
    quote: St. Catherine of Siena Church, Wilmington, DE 03-1410
    note: St. Catherine's issue of the same date is a different LPi container (03/1410) with its own bilingual
      masthead 'Saint Catherine of Siena Parish', Mass schedule (Sat 7 pm Spanish; Sun 8 and 10:30; weekdays
      9 am) and office hours; it names the same pastor.
---

## Publisher

St. John the Beloved prints its own ParishesOnline (LPi) bulletin, container 03/1288. The 25 October 2026 issue's cover (an image page, read after rendering) is headed 'ST. JOHN THE BELOVED CATHOLIC CHURCH' with Rev. Michael Christopher Vannicola as pastor, and gives only this church's Mass schedule, reconciliation, office hours and address.

## Worship sites

One church, 907 Milltown Road (Sherwood Park), Wilmington 19808.

## Shared pastor, separate bulletin

Fr. Vannicola has been pastor of both St. John the Beloved and St. Catherine of Siena since 3 September 2025 (The Dialog, 2025-08-14). St. Catherine's cover names him too and even says confessions 'are also available at Saint John the Beloved on Saturday morning', but its bulletin is a different LPi container (03/1410) with its own masthead, schedule and office, so each is its own row.

## Website and bulletin provider

sjbde.org embeds the ParishesOnline org, so the resolver reads it as `parishes_online`. Most of the PDF's pages are images: the pipeline will need to read them as images.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-john-the-beloved-wilmington` (2026-10-27): resolved by the ParishesOnline org to container 03/1288, 20261025B.pdf (49.7 MB, image-heavy), transport ok, PDF signature, fresh (2 days; date inferred from the filename because page 1 is an image). Identity is 'unverified' by the tool; the rendered masthead read above settles it.

## Not yet confirmed

Nothing outstanding.
