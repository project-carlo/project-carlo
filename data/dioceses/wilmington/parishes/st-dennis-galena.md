---
name: St. Dennis
website: https://www.stdennischurch.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-dennis-catholic-church-galena-md-21635
publication: ['url:https://www.church-bulletin.org/saint-dennis-catholic-church-galena-md-21635']
group: Iron Hill Deanery; pastor shared with St. Polycarp, Smyrna
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-dennis-catholic-church-galena-md-21635/2026-10-25.pdf
  seen: 2026-10-27
  note: 'Page 1 of the 25 October 2026 issue (6 pages, scanned images with no text layer, so read as a
    rendered image): masthead ''St. Dennis Catholic Church / In THE IRON HILL DEANERY Of THE DIOCESE OF
    WILMINGTON / Rev. James D. Hreha, Pastor / Rev. Pedro Chalacan, Hispanic Priest'', ''MASS SCHEDULE
    Sunday 8 am, Thursday & Friday 8:30 am'', ''HISPANIC MASS Sunday 11am'', parish office ''156 N. Main
    St. (P.O. Box 249)''; it also lists ''PARISH OFFICE—ST. POLYCARP office@saintpolycarp.org (302-653-8279)''
    and the St. Polycarp livestream as extra contacts. No second church''s Mass schedule.'
- url: https://jppc.net/onlinebulletins/732template.pdf
  seen: 2026-10-27
  note: curl -L redirects to https://www.church-bulletin.org/saint-dennis-catholic-church-galena-md-21635,
    a John Patrick listing of dated PDFs, newest first (2026-10-25, 10-18, 10-11 ...). church-bulletin.org
    id 732 is the number the survey recorded for this parish.
- url: https://thedialog.org/our-diocese/clergy-appointments-as-announced-may-19-by-bishop-koenig-in-the-diocese-of-wilmington/
  seen: 2026-10-27
  quote: The Reverend James D. Hreha is reappointed Pastor of Saint Dennis, Galena. This is in addition
    to his appointment as Pastor of Saint Polycarp, Smyrna.
  note: Clergy appointments of 19 May 2024.
research:
- method: probe url and the browser (visit.py --bulletin) on https://www.stdennischurch.org/ and curl
    on http/https and bare-domain variants
  url: https://www.stdennischurch.org/
  checked: '2026-10-27'
  outcome: access-blocked
  next_action: Read the home page for its bulletin link and Mass times, and check whether it links jppc.net/onlinebulletins/732template.pdf
  retry_when: The site answers (HTTP 500 on www and no connection on the bare domain from this sandbox)
bulletin_status: available
publication_reviews:
- parish: st-polycarp-smyrna
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-dennis-catholic-church-galena-md-21635/2026-10-25.pdf
    seen: 2026-10-27
    note: 'St. Dennis''s 25 October 2026 cover is headed ''St. Dennis Catholic Church'' with its own Mass
      schedule (Sunday 8 am and 11 am Spanish, Thursday & Friday 8:30 am); St. Polycarp''s cover of the
      same date is a different John Patrick file (listing 301) headed by its own schedule (Saturday 4
      pm, Sunday 10:30 am, Tuesday & Wednesday 8:30 am). Same pastor, different bulletins. Checked 2026-10-27:
      St. Dennis''s rendered cover masthead names St. Dennis Catholic Church alone with its own Mass schedule;
      St. Polycarp''s cover of the same date names St. Polycarp with a different schedule.'
---

## Publisher

St. Dennis, Galena publishes its own weekly bulletin, printed by John Patrick Publishing (church-bulletin.org listing 732). The 25 October 2026 file is scanned images (6 pages, no text layer), so the pipeline will have to read it as an image. Its page 1 (rendered) is headed 'St. Dennis Catholic Church', names 'Rev. James D. Hreha, Pastor' and 'Rev. Pedro Chalacan, Hispanic Priest', and gives 'MASS SCHEDULE Sunday 8 am, Thursday & Friday 8:30 am' and 'HISPANIC MASS Sunday 11am'.

**Shared pastor, separate bulletin.** Fr. Hreha is also pastor of St. Polycarp, Smyrna (The Dialog, 19 May 2024). St. Polycarp's bulletin (listing 301) is a different file with its own masthead and schedule, so this is its own row. The St. Dennis cover does print the St. Polycarp office email and livestream as an extra contact; it is not a shared schedule.

## Worship sites

One church: St. Dennis, 153 N. Main Street, Galena (`churches/st-dennis-galena.md`), with an English Mass Sunday 8 am and a Spanish Mass Sunday 11 am.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing. The parish site (stdennischurch.org) did not answer from this sandbox (see `research`). The cover prints the domain as 'stdennischurch.org'.

## Not yet confirmed

The parish website was unreadable, so its own bulletin link and Mass page are unread; the pick rests on the template redirect and the 25 October cover. Mass times are read from an image.
