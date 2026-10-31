---
name: Holy Redeemer Chinese Catholic Church
website: https://holyredeemerccc.org
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://holyredeemerccc.org/category/bulletin/#holy-redeemer']
group: ''
evidence:
- url: https://holyredeemerccc.org/2026/10/09/october-11-2026/
  seen: 2026-10-29
  quote: Sunday readings for October 11, 2026
  note: 'The church''s own ''Bulletin'' post (category Bulletin, posted 9 October 2026): readings, announcements
    (the 18 October procession, a wedding invitation, World Youth Day Korea 2027) and a mailto link. It
    is a WordPress text post with no PDF or image attached, and it is the newest post: the 18 and 25 October
    Sundays have none, so it lags by two weeks. The WP REST posts list (probe get /wp-json/wp/v2/posts)
    shows the same: 11 October, then 16 August to 6 September.'
- url: https://holyredeemerccc.org
  seen: 2026-10-29
  quote: Sunday 10:00 am Cantonese
  note: 'Home page: Sunday 10:00 am Cantonese, 11:15 am English, 12:30 pm Mandarin (Cantonese and Mandarin
    livestreamed on Zoom); Monday-Friday 8:30 am school Mass on Wednesday in the school year; Saturday
    by arrangement with Ms. Leung. Footer: ''Church & School 915 Vine St Philadelphia, PA 19107, 215.922.0999''
    and a link to ''St. John the Evangelist Catholic Church ... StJohnsPhilly.org''.'
- url: https://container.parishesonline.com/bulletins/04/0978/20261025B.pdf
  seen: 2026-10-29
  quote: CHINESE CATHOLIC CHURCH
  note: 'St. John the Evangelist''s 25 October 2026 bulletin (also 11 and 18 October) prints a sidebar
    box ''HOLY REDEEMER CHINESE CATHOLIC CHURCH, 915 Vine St., Phila., PA, 215-922-0999. Sunday Mass Schedule:
    10:00am - Cantonese, 11:15am - English, 12:30pm - Mandarin. Friar Thomas Betz, OFM Cap - Pastor. Parish
    website: www.stjohnsphilly.org'', and the masthead lists ''Father Joseph Lei Jin, Chinese Apostolate''.
    The 11 and 18 October issues repeat the church''s procession announcement. The Mass schedule, the
    masthead and the footer code (04-0978) are St. John''s; the box is a neighbour''s, not a joint masthead.'
- url: https://archphila.org/parish/holy-redeemer-philadelphia/
  seen: 2026-10-28
  quote: 'Coordinator of the Chinese Apostolate: Father Thomas Betz, O.F.M. Cap.'
  note: 'Directory page (updated 1 year earlier): 915 Vine St.; no pastor, no deanery; phone 215 563-4145,
    which is St. John the Evangelist''s friary line; Director of Parish Services Linda Mei Hing Leung;
    Mass times match the church''s site.'
revisit: Check whether the church posts its bulletin as a PDF or image, whether the Oct 18/25 posts appear,
  and whether the owner wants this church filed as a worship site of St. John the Evangelist's row instead.
revisit_after: 2027-01-15
research:
- method: probe get on holyredeemerccc.org, its Oct 11 bulletin post and the WP REST posts list
  url: https://holyredeemerccc.org/2026/10/09/october-11-2026/
  checked: '2026-10-29'
  outcome: unsupported-format
  next_action: The bulletin is an HTML post without a PDF; the dated-post and page-pdfs recipes need a
    linked PDF. Re-check if posts start attaching a PDF or image, or decide with the owner whether the
    Mass schedule in St. John the Evangelist's bulletin should carry this church.
  retry_when: A post links a PDF or bulletin image, or the owner decides to file the church under St.
    John the Evangelist
- method: John Patrick scan (ids 1-1300; no Holy Redeemer listing) and ParishesOnline search near 915
    Vine St (probe po holy-redeemer)
  url: https://parishesonline.com/organization/holy-redeemer
  checked: '2026-10-29'
  outcome: not-found
  next_action: 'None: the ParishesOnline organization holy-redeemer (915 Vine st, website www.holyredeemer.cc,
    lpi 001C000000wZ3ftIAC) has no publications, and St. John''s container 04/0978 only prints the church''s
    box.'
  retry_when: The organization gains issues, or the church site links church-bulletin.org, ParishesOnline
    or eCatholic
bulletin_status: unsupported-format
---

## Publisher

Holy Redeemer Chinese Catholic Church (915 Vine St., Chinatown) keeps its own website, holyredeemerccc.org, and posts a weekly 'Bulletin' there as an HTML page (readings and announcements, no PDF). The newest is 11 October 2026, two Sundays behind. The pipeline reads PDFs and images, so the row is `no_bulletin` with `bulletin_status: unsupported-format`, kept in the records and off the site until a readable bulletin appears.

## One bulletin or several?

The lead was that the directory page gives St. John the Evangelist's phone (215 563-4145) and a Capuchin coordinator. Both are true, and both are contact lines: Fr. Thomas Betz, O.F.M. Cap., is St. John's pastor and the Chinese Apostolate's coordinator, and the friars staff both. St. John's ParishesOnline bulletin (04-0978) prints a sidebar box with this church's Sunday Masses and repeats its announcements, but its masthead, Mass schedule and footer are St. John's, so it is not a joint bulletin. Holy Redeemer also has a school, a Director of Parish Services and its own posts. I kept two rows. An owner who would rather file the church under St. John's row (its Mass times are printed in that bulletin) can merge the rows; see the flag in this batch's handoff.

## Worship sites

One: Holy Redeemer Church, 915 Vine St. (`churches/holy-redeemer-philadelphia.md`).
