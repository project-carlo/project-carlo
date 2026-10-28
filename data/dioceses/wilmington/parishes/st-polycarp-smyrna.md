---
name: St. Polycarp
website: https://saintpolycarp.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-polycarp-church-smyrna-de-19977
publication: ['url:https://www.church-bulletin.org/saint-polycarp-church-smyrna-de-19977']
group: Iron Hill Deanery; pastor shared with St. Dennis, Galena
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-polycarp-church-smyrna-de-19977/2026-10-25.pdf
  seen: 2026-10-27
  quote: Rev. James D. Hreha, Pastor
  note: 'Page 1 (text layer, 8 pages) of the 25 October 2026 issue: masthead ''A Roman Catholic Church
    In The Iron Hill Deanery of The Diocese of Wilmington'', ''MASS SCHEDULE Saturday 4:00 pm & Sunday
    10:30 am, Tuesday & Wednesday 8:30 am'', ''55 Ransom Lane Smyrna, DE 19977'', www.saintpolycarp.org.
    A probe pdf --grep for ''Dennis'' and ''Galena'' over the whole issue finds nothing: the issue names
    St. Polycarp alone.'
- url: https://jppc.net/onlinebulletins/301template.pdf
  seen: 2026-10-27
  note: curl -L redirects to https://www.church-bulletin.org/saint-polycarp-church-smyrna-de-19977, a
    John Patrick Publishing listing of dated PDFs, newest first (2026-10-25, 10-18, 10-11 ...). Template
    301 is the diocese-wide playbook's number for St. Polycarp.
- url: https://thedialog.org/our-diocese/clergy-appointments-as-announced-may-19-by-bishop-koenig-in-the-diocese-of-wilmington/
  seen: 2026-10-27
  quote: The Reverend James D. Hreha is reappointed Pastor of Saint Dennis, Galena. This is in addition
    to his appointment as Pastor of Saint Polycarp, Smyrna.
  note: 'Clergy appointments of 19 May 2024: the shared-pastor link that put this batch together.'
promoted: 2026-10-27
research:
- method: probe url and the browser (visit.py --bulletin) on https://saintpolycarp.org/ and curl on http/https
    and www variants
  url: https://saintpolycarp.org/
  checked: '2026-10-27'
  outcome: access-blocked
  next_action: Reread the site's home page for its bulletin link and Mass times; the Wayback copy (20260610)
    shows it exists
  retry_when: The site answers (it returned HTTP 500 on www and no connection on the bare domain from
    this sandbox)
bulletin_status: available
---

## Publisher

St. Polycarp, Smyrna publishes its own weekly bulletin, printed by John Patrick Publishing (template 301). The 25 October 2026 issue's page 1 (text layer) carries a masthead naming 'Rev. James D. Hreha, Pastor', the Iron Hill Deanery, the Mass schedule 'Saturday 4:00 pm & Sunday 10:30 am / Tuesday & Wednesday 8:30 am' and the address 55 Ransom Lane, Smyrna. Searching the whole 8-page issue for 'Dennis' and 'Galena' finds nothing.

**Shared pastor, separate bulletin.** The Dialog (19 May 2024) reappointed Fr. Hreha pastor of St. Dennis, Galena in addition to St. Polycarp. St. Dennis publishes its own John Patrick bulletin (listing 732) whose cover names Fr. Hreha as pastor and gives its own Mass schedule; so the two are separate rows (see `st-dennis-galena`). St. Dennis's cover lists the St. Polycarp parish office and livestream as a contact, which is the only overlap seen.

## Worship sites

One church: St. Polycarp, 55 Ransom Lane, Smyrna (`churches/st-polycarp-smyrna.md`). The chapel the bulletin mentions (Eucharistic Adoration 'in the Chapel') is part of the same campus; nothing suggests a separate Mass site.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing as for the other John Patrick parishes here. The parish site (saintpolycarp.org) did not answer from this sandbox (see `research`), so the link from the site to the listing was not read; the template redirect is the evidence for the number. The site is also what the directory and GCatholic give.

## Not yet confirmed

The parish website was unreachable, so its own Mass times page and bulletin link are unread. The cover, directory (Sun 10:30, Tue/Wed 8:30, Sat 16:00) and the Mass schedule agree.
