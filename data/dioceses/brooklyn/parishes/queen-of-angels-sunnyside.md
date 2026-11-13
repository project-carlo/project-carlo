---
name: Queen of Angels (Sunnyside)
website: https://queenofangelsnyc.org/
bulletin_provider: other
provider_id: page-pdfs https://queenofangelsnyc.org/bulletins
publication: []
group: Deanery Q2 (Queens West)
evidence:
- url: https://queenofangelsnyc.org/system/resources/W1siZiIsIjIwMjYvMTEvMDYvNGJoeDVicGFpcF9CdWxsZXRpbi5wZGYiXV0/Bulletin.pdf
  seen: 2026-11-06
  quote: Rev. Ambiorix D. Osorio- Pastor
  note: '8 November 2026 issue (8 pages; pages 1 and 8 are images, read with render.py). Page 1 is an
    LPi stock cover (''32ND SUNDAY IN ORDINARY TIME'') with no parish name; page 2 ''Mass Schedule/Horario
    de Misas: Saturday Vigil 5:00 PM; Sunday 9:00 AM, 10:30 AM (Español), 12:00 PM; Monday through Friday
    9:00 AM'' and the parish staff (the quote); page 3 ''44-04 Skillman Ave, Sunnyside, NY 11104'' and
    ''Sunday, November 8th, 2026''. Page 8 (image) ad page footer ''#171 FOR ADVERTISING: THE CHURCH BULLETIN
    INC., 200 DALE ST., W. BABYLON, NY''.'
- url: https://queenofangelsnyc.org/bulletins
  seen: 2026-11-06
  quote: November 08, 2026
  note: Tilma site; /bulletins lists '<Month DD, YYYY> / Download Bulletin' cards newest first, weekly
    from July 2026 to 8 Nov 2026, each a /system/resources/<token>/Bulletin.pdf.
- url: https://parishesonline.com/organization/queen-of-angels-church-11104
  seen: 2026-11-06
  note: 'probe po: org ''Queen of Angels Church'' (lpi 0018000000QxB6ZAAV), website queenofangelsnyc.org,
    no issues: an empty org, not a publication id.'
- url: https://queenofangelsnyc.org/mass-times
  seen: 2026-11-06
  quote: 'Sunday: 9am, 10:30am (Spanish), 12pm'
  note: Saturday Vigil 5pm; Sunday 9am, 10:30am (Spanish), 12pm; Monday-Friday 9am.
promoted: 2026-11-12
research:
- method: fetch:check page-pdfs https://queenofangelsnyc.org/bulletins
  url: https://queenofangelsnyc.org/bulletins
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
---

## Publisher

Queen of Angels publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad page footer "#171"), posted on its Tilma site's `/bulletins` page. I read the 8 November 2026 issue (read 2026-11-06): page 1 is a stock cover with no parish name; page 2 gives the Mass schedule and staff, "Rev. Ambiorix D. Osorio- Pastor"; page 3 gives "44-04 Skillman Ave, Sunnyside, NY 11104". The job note placed Queen of Angels between St. Raphael and St. Teresa, which share a pastor; it has its own pastor and bulletin, and neither neighbour's bulletin mentions it except St. Teresa's list of the Queens North 2 deanery's parishes.

## Worship sites

One church, Queen of Angels, 44-04 Skillman Ave. Page 2's schedule: Saturday Vigil 5:00 PM; Sunday 9:00 AM, 10:30 AM (Español), 12:00 PM; Monday-Friday 9:00 AM. No mission or chapel is named.

## Website and bulletin provider

`other`, recipe `page-pdfs https://queenofangelsnyc.org/bulletins` (Tilma; files at `queenofangelsnyc.org/system/resources/<token>/Bulletin.pdf`). The Church Bulletin Inc. has no online container, so there is no publication id; the ParishesOnline org `queen-of-angels-church-11104` exists but has no issues. Pages 1 and 8 are images. `fetch:check` (2026-11-06) resolved "page-pdfs on https://queenofangelsnyc.org/bulletins: first-listed" and picked the 8 November 2026 issue (`.../W1siZiIsIjIwMjYvMTEvMDYvNGJoeDVicGFpcF9CdWxsZXRpbi5wZGYiXV0/Bulletin.pdf`); freshness `unknown` because every file is named Bulletin.pdf, so I checked the date on page 3.

## Not yet confirmed

Nothing open.
