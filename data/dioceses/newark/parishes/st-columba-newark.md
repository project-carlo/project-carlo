---
name: St. Columba, Newark
website: https://www.stcolumbachurchnewark.org/
bulletin_provider: google_drive
provider_id: drive-folder https://drive.google.com/drive/folders/1hoeusEJqpRDahxMdP1zpmg-cyTZFfLFZ
publication: ['url:https://drive.google.com/drive/folders/1hoeusEJqpRDahxMdP1zpmg-cyTZFfLFZ', 'po-org:st-columba-church-07114',
  'lpi:0018000000QxAB6AAN']
group: ''
evidence:
- url: https://drive.google.com/uc?export=download&id=1HSdIP-f2oQeWopV2z6ub85cUa5wLGBYM
  seen: 2026-11-04
  quote: AT SAINT AUGUSTINE CHURCH
  note: '''11-01-2026 Bulletin - All Saints.pdf'' (2 pages, text layer). Page 1: ''Welcome to Saint Columba'',
    ''Pastor: Rev Andres Codoner Contel'', ''Parochial: Vicar: Rev. Drazen Hozi'', phone 973-622-7712;
    Saturday 5:00 PM (English & Spanish); Sunday 8:00 AM (English), Domingo 11:00 AM (Español); ''AT SAINT
    AUGUSTINE CHURCH Sunday: 9:30 AM (Eng & Spa) 170 Sussex Ave. Newark, NJ''; daily Mass 6:00 PM Mon
    (Sp), Tue (Eng), Wed (Sp), Fri (Sp), 7:30 AM Thursday (English); Neocatechumenal Way Saturday 6:00
    and 8:00 PM.'
- url: https://drive.google.com/drive/folders/1hoeusEJqpRDahxMdP1zpmg-cyTZFfLFZ
  seen: 2026-11-04
  note: Public folder listing '10-04-2026 Bulletin 27th Sunday OT.pdf', '10-18-2026 …', '10-25-2026 Bulletin
    30th Sunday OT.pdf', '11-01-2026 Bulletin - All Saints.pdf'.
- url: https://www-stcolumbachurchnewark-org.filesusr.com/html/00a235_f50004b45509924b56e4f4ec13e6b365.html
  seen: 2026-11-04
  quote: Access past bulletins from 2025.
  note: 'The Wix site''s whole content is this embedded HTML app (the site''s /bulletins and /mass-schedule
    paths 404). Its Bulletins section links ''2026 Bulletins'' (Drive folder 1hoeusEJqpRDahxMdP1zpmg-cyTZFfLFZ)
    and ''2025 Archive'' (1xBGlxWapumnQyfjPmMmXHoz_3F5o2kRg). Its Mass schedule: St. Columba Saturday
    5:00 PM, Sunday 8:00 AM and 11:00 AM; ''St. Augustine Church'' 9:30 AM (Bilingual); Daily Mass under
    ''St. Mary''s Chapel''.'
- url: https://parishesonline.com/organization/st-columba-church-07114
  seen: 2026-11-04
  note: 'probe po: ''St. Columba Church'', 25 Thomas St, Newark, lpi 0018000000QxAB6AAN, website stcolumbanewark.com;
    no publications now.'
revisit: The Drive folder is the site's '2026 Bulletins'; check whether 2027 issues go to a new folder
  and repoint provider_id
revisit_after: 2027-01-05
research:
- method: Read the 1 November 2026 bulletin and the site's schedule for where 'St. Mary's Chapel' (the
    site's heading over the daily Masses) is
  url: https://www-stcolumbachurchnewark-org.filesusr.com/html/00a235_f50004b45509924b56e4f4ec13e6b365.html
  checked: '2026-11-04'
  outcome: not-found
  next_action: Find the chapel's location (a later bulletin, the parish office); if it is a separate building
    with public Mass, add a church row
  retry_when: A bulletin or the site names the chapel's address
bulletin_status: available
---

## Publisher

The parish publishes its own bulletin as weekly PDFs in a public Google Drive folder, linked from its website as "2026 Bulletins". The 1 November 2026 issue ("11-01-2026 Bulletin - All Saints.pdf", text layer) opens "Welcome to Saint Columba", names Rev Andres Codoner Contel as pastor and gives the Mass schedule. Its earlier LPi org (`st-columba-church-07114`) publishes nothing now; its ids are kept in `publication`.

## Worship sites

Two churches:

- `st-columba-newark`, 25 Thomas Street.
- `st-augustine-newark`, 170 Sussex Avenue. The same schedule lists a Sunday 9:30 AM bilingual Mass "AT SAINT AUGUSTINE CHURCH… 170 Sussex Ave." This is St. Augustine, Newark (directory 128, GCatholic 18500). It has no bulletin of its own: its ParishesOnline org and Discover Mass listing publish nothing, no John Patrick listing matches, and it has no website (the `i-newark-downtown` batch checked these; see that church's record). So it is a church of this row. The site puts the daily Masses under "St. Mary's Chapel", which no source locates: probably a weekday chapel at St. Columba (inferred, not checked; see research).

## Website and bulletin provider

The Wix site (https://www.stcolumbachurchnewark.org/) is one embedded HTML page that links the Drive folders. Provider `google_drive`, `provider_id: drive-folder <2026 folder>`, which reads the folder directly. The folder is the year's: recheck in January 2027 (`revisit_after`).

## Not yet confirmed

Where St. Mary's Chapel is (research).
