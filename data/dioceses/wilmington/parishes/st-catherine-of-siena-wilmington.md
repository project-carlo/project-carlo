---
name: St. Catherine of Siena
website: https://www.scswilmde.org/
bulletin_provider: parishes_online
provider_id: st-catherine-of-siena-church-19808
publication: ['po-org:st-catherine-of-siena-church-19808', 'lpi:0018000000Qx8z8AAB', 'po-container:03/1410']
group: New Castle Deanery; pastor shared with St. John the Beloved, separate bulletin
evidence:
- url: https://container.parishesonline.com/bulletins/03/1410/20261025B.pdf
  seen: 2026-10-27
  quote: St. Catherine of Siena Church, Wilmington, DE 03-1410
  note: 'Page 1 is an image, rendered with render.py: bilingual masthead ''Saint Catherine of Siena Parish
    / Parroquia de Santa Catalina de Siena'', ''REV. MICHAEL CHRISTOPHER VANNICOLA, PASTOR'', ''OCTOBER
    25, 2026'', Mass schedule (weekend Sat 7 pm Spanish, Sun 8 and 10:30 English; weekday Mon-Fri 9 am
    English, Tue 7 pm Spanish), office hours Mon-Thu 9:30-2:30, address 2503 Centerville Road, Wilmington,
    DE 19808. The quote is the LPi footer on page 7, which names the container.'
- url: https://parishesonline.com/organization/st-catherine-of-siena-church-19808
  seen: 2026-10-27
  note: 'probe po: org ''St. Catherine of Siena Church'', LPi id 0018000000Qx8z8AAB, container 03/1410,
    website scswilmde.org; latest issue listed 2026-11-01 (issues are posted ahead; the 25 October issue
    is the one read). The org''s own address and pin (2503 Centerville Rd, 39.7350, -75.6598) sit near
    St. John the Beloved, not at the church: the pin is unreliable.'
- url: https://www.scswilmde.org/
  seen: 2026-10-27
  note: 'probe url: HTTP 200, title ''Home | StCathWilm'', embeds po-org:st-catherine-of-siena-church-19808.'
publication_reviews:
- parish: st-john-the-beloved-wilmington
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/1410/20261025B.pdf
    seen: 2026-10-27
    quote: St. Catherine of Siena Church, Wilmington, DE 03-1410
    note: 'St. Catherine''s own container 03/1410, bilingual masthead and Mass schedule on page 1 (image).
      Checked 2026-10-27: each masthead names one parish only (St. Catherine of Siena; St. John the Beloved),
      with its own Mass schedule.'
  - url: https://container.parishesonline.com/bulletins/03/1288/20261025B.pdf
    seen: 2026-10-27
    quote: St. John the Beloved Parish, Wilminton, DE 03-1288
    note: 'St. John''s issue of the same date: container 03/1288, a masthead and schedule for St. John
      alone.'
---

## Publisher

St. Catherine of Siena prints its own bilingual (English/Spanish) ParishesOnline bulletin, container 03/1410. The 25 October 2026 cover (an image page, read after rendering) is headed 'Saint Catherine of Siena Parish', names Rev. Michael Christopher Vannicola as pastor, and gives this church's Mass schedule, confession times and office hours.

## Worship sites

One church, 2503 Centerville Road, Wilmington 19808.

## Shared pastor, separate bulletin

Fr. Vannicola is also pastor of St. John the Beloved (since 3 September 2025; The Dialog 2025-08-14). The two bulletins are separate LPi containers (03/1410 and 03/1288) with their own mastheads and schedules, so they are two rows. The cover notes that confessions are also available at St. John the Beloved on Saturday mornings.

## Website and bulletin provider

scswilmde.org embeds the ParishesOnline org, so the resolver reads it as `parishes_online`. The cover is an image page.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-catherine-of-siena-wilmington` (2026-10-27): resolved by the ParishesOnline org to container 03/1410, 20261101B.pdf (32.7 MB), transport ok, PDF signature, freshness 'future' (-5 days): LPi posts the next weekend's issue early, so the newest file is 1 November. Its text names 'St. Catherine of Siena Church, Wilmington, DE 03-1410' (footer). Date is inferred from the filename. The masthead read above is the 25 October issue of the same container; identity tool-status is 'unverified' (none supplied).

## Not yet confirmed

Nothing outstanding.
