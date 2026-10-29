---
name: St. Margaret of Antioch Parish
website: https://www.saintmarg.org
bulletin_provider: ecatholic
provider_id: '34693'
publication: ['ecatholic:34693', 'url:https://www.church-bulletin.org/saint-margaret-of-antioch-church-narberth-pa-19072']
group: ''
evidence:
- url: https://files.ecatholic.com/34693/bulletins/20261025.pdf
  seen: 2026-10-28
  quote: Saint Margaret Parish, Narberth, PA
  note: 'The parish''s own eCatholic archive file for 25 October 2026 (8 pages, text layer): page 1 ''MASS
    SCHEDULE: Saturday Evening Vigil 5:15 PM; Sunday 7:30, 10:00 and 11:30 AM; Daily Monday - Friday 7:00
    AM; Saturday 8:00 AM'', rectory ''208 N Narberth Ave, Narberth, PA 19072 - 610.664.3770'', Msgr. Paul
    V. Dougherty, Pastor; page footers ''Saint Margaret Parish, Narberth, PA''. md5 b7fca345a4535bbb79d15032a100193b.'
- url: https://www.church-bulletin.org/bulletin/saint-margaret-of-antioch-church-narberth-pa-19072/2026-10-25.pdf
  seen: 2026-10-28
  note: 'John Patrick Publishing''s copy of the same issue (listing 110): byte-identical to the eCatholic
    file (same md5 b7fca345a4535bbb79d15032a100193b, 6,039,727 bytes); the page footers and cover code
    read ''0110''.'
- url: https://www.saintmarg.org/bulletins
  seen: 2026-10-28
  note: 'eCatholic site 34693: the page lists files.ecatholic.com/34693/bulletins/<yyyymmdd>.pdf from
    20260809 to 20261025, newest first, so the archive is current. The site''s home page also links church-bulletin.org/?id=110.'
- url: https://www.church-bulletin.org/saint-margaret-of-antioch-church-narberth-pa-19072
  seen: 2026-10-28
  quote: Latest Edition
  note: John Patrick listing id 110, 'Saint Margaret of Antioch Church', Narberth, PA 19072, 208 North
    Narberth Avenue; latest edition October 25, 2026.
- url: https://archphila.org/parish/st-margaret-narberth/
  seen: 2026-10-28
  note: 'Directory entry (updated 4 months ago): Rev. Msgr. Paul V. Dougherty; 208 N Narberth Ave.; Mass
    times Saturday vigil 5:15 PM, Sundays 7:30, 8:45, 10, 11:30 AM. The 8:45 AM Sunday Mass is not in
    the 25 October 2026 bulletin.'
---

## Publisher

St. Margaret of Antioch Parish publishes one weekly bulletin, hosted on its own eCatholic site (34693) and also listed by John Patrick Publishing (listing 110). The 25 October 2026 issue is the same file in both places (md5 equal), so the row is `ecatholic` with the listing as a second publication id, as for the Chester County parishes whose archive carries the John Patrick PDF. The archive is current (25 October posted by 28 October).

## Worship sites

One church: St. Margaret of Antioch Church, 208 N. Narberth Ave. The Mass schedule box lists Saturday vigil, Sunday, daily and Saturday morning Masses with no other location. Eucharistic Exposition (Wednesday and First Fridays) is listed without a place, and no chapel or hall Mass is listed. St. Margaret School is a school, not a worship site.

## Other parishes

The pastor, Msgr. Dougherty, is named on no other parish's directory page, so there is no shared-pastor pair to compare. The masthead names St. Margaret alone.

## Website and bulletin provider

saintmarg.org is on eCatholic and hosts the bulletin PDFs under `/bulletins`, so the `ecatholic` resolver reads it. If a future issue is posted early and `fetch:check` rejects it as `future`, the listing is the fallback `other` row (`page-pdfs https://www.church-bulletin.org/saint-margaret-of-antioch-church-narberth-pa-19072`).
