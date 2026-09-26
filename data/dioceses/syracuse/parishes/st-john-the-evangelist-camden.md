---
name: St. John the Evangelist & St. Mary's Oratory
website: https://stjohncamden.com/
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.church-bulletin.org/saint-john-the-evangelist-saint-mary-s-oratory-camden-ny-13316']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-saint-mary-s-oratory-camden-ny-13316/2026-09-27.pdf
  seen: 2026-09-26
  note: 'The 27 September 2026 issue (no text layer; read rendered). Page-1 masthead "St. John the Evangelist
    & St. Mary''s Oratory, Pastor: Rev. John F. Hogan, Jr.", schedule "Saturday Vigil 4:00 p.m., Sunday
    Morning 9:00 a.m., Wednesday, Thursday & Friday @9:00 a.m.", and "St. John the Evangelist Parish & St.
    Mary Mount Carmel Oratory, 35 Third Street, Camden, N.Y. 13316".'
- url: https://www.church-bulletin.org/bulletin/saint-john-the-evangelist-saint-mary-s-oratory-camden-ny-13316/2026-08-23.pdf
  seen: 2026-09-26
  quote: Mary Mount Carmel Oratory
  note: The 23 August 2026 issue, which has a text layer; same masthead and schedule ("Saturday Vigil 4:00
    p.m.", "Sunday Morning 9:00 a.m.").
- url: https://www.church-bulletin.org/saint-john-the-evangelist-saint-mary-s-oratory-camden-ny-13316
  seen: 2026-09-26
  quote: Saint John the Evangelist & Saint Mary's Oratory
  note: John Patrick Publishing's page for the parish (the site's CURRENT BULLETIN link, jppc.net/onlinebulletins/4011template.pdf,
    redirects here via church-bulletin.org/?id=4011). Weekly PDFs, newest 27 September 2026.
- url: https://stjohncamden.com/
  seen: 2026-09-26
  quote: 'Saturday Vigil Mass: 4:00 p.m.'
  note: 'The parish site (hosted by John Patrick Publishing). Mass Schedule: Saturday Vigil 4:00 p.m., Sunday
    9:00 a.m., daily Wed-Fri 9:00 a.m., at "St. John the Evangelist Church, 35 Third Street, Camden, NY
    13316". probe url timed out on it; it loads in a browser and with curl.'
- url: https://stjohncamden.com/?page_id=61
  seen: 2026-09-26
  quote: Sale of St. Patrick’s church  property to Ranch of Hope church
  note: 'The parish timeline: St. Mary, Florence "will now serve as a devotional chapel" from 1 July 2003;
    "October 2016 Sale of St. Patrick''s church property to Ranch of Hope church" (Williamstown).'
---

## Publisher

St. John the Evangelist, Camden publishes its own weekly bulletin through John Patrick Publishing
(church-bulletin.org). Its masthead names "St. John the Evangelist & St. Mary's Oratory": St. Mary of
Mount Carmel in Florence, a former parish that became a devotional chapel in 2003, is part of the same
parish. I read the 27 September 2026 issue (rendered: it has no text layer) and the 23 August 2026 issue
(text): one pastor, one schedule, all regular Masses at St. John's.

## Worship sites

- `churches/st-john-the-evangelist-camden.md`: every weekly Mass.
- `churches/st-mary-of-mount-carmel-florence.md`: the oratory, which gets an annual Mass announced in this
  bulletin (Sunday 21 September 2025 and Sunday 20 September 2026, both 11:00 am).

Excluded: St. Patrick Mission, Williamstown (`excluded/st-patrick-williamstown.md`, sold in 2016). The
diocese's list also names St. Paul Mission, Redfield (closed); it is in no roster and was not recorded.

## Website and bulletin provider

stjohncamden.com is the parish's own site; its "CURRENT BULLETIN" link redirects to the
church-bulletin.org page, which lists dated PDFs. `bulletin_provider: other` with the site as `website`,
as for Christ the Good Shepherd; `publication` is the listing page. Recent issues alternate between PDFs
with and without a text layer; the pipeline's extraction reads the rendered PDF, so both should work.

## Not yet confirmed

Nothing.
