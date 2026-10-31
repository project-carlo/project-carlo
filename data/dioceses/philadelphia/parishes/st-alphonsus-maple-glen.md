---
name: St. Alphonsus Parish
website: https://www.stalphonsusparish.org
bulletin_provider: ecatholic
provider_id: '27039'
publication: ['ecatholic:27039', 'url:https://www.church-bulletin.org/saint-alphonsus-church-maple-glen-pa-19002']
group: ''
evidence:
- url: https://files.ecatholic.com/27039/bulletins/20261025.pdf
  seen: 2026-10-28
  note: The parish's eCatholic copy of the 25 October 2026 issue (8 pages, image-only, 6,272,648 bytes,
    md5 283c4183) is byte-identical to the John Patrick listing's 2026-10-25.pdf. Page 1 reads 'St. Alphonsus
    Church, Maple Glen, PA / October 25, 2026 / The Thirtieth Sunday in Ordinary Time', with the sidebar
    '1567 Temple Drive, Maple Glen, PA 19002', 'Rev. Msgr. Brian P. Hennessy, Pastor' and 'MASS SCHEDULES
    Saturday Vigil 5:00 pm, Sunday 8:00 am, 10:15 am, 12 Noon, Tuesday - Saturday 9:00 am'. Page 2 is
    a pastor's letter. The masthead names St. Alphonsus alone.
- url: https://www.church-bulletin.org/saint-alphonsus-church-maple-glen-pa-19002
  seen: 2026-10-28
  quote: Latest Edition
  note: Listing 81 'Saint Alphonsus Church', Maple Glen, PA 19002; latest edition October 25, 2026; its
    2026-10-25.pdf has the same md5 as the eCatholic file.
- url: https://www.stalphonsusparish.org/bulletins
  seen: 2026-10-28
  note: Parish eCatholic site (27039) /bulletins page links files.ecatholic.com/27039/bulletins/<yyyymmdd>.pdf
    for every Sunday from 20201129 to 20261025 (the page source; not visible text).
- url: https://archphila.org/parish/st-alphonsus-maple-glen/
  seen: 2026-10-28
  quote: Rev. Msgr. Brian P. Hennessy
  note: 'Directory: pastor Rev. Msgr. Brian P. Hennessy; rectory 1567 Temple Dr., Maple Glen 19002.'
promoted: 2026-10-29
bulletin_status: available
---

## Publisher

St. Alphonsus Parish, Maple Glen (Rev. Msgr. Brian P. Hennessy, Pastor) publishes one weekly bulletin that reaches us two ways: the parish's own eCatholic archive (site 27039, `/bulletins`, files `files.ecatholic.com/27039/bulletins/<yyyymmdd>.pdf`) and John Patrick Publishing listing 81 ('Saint Alphonsus Church'). The 25 October 2026 files are byte-identical (md5 283c4183), so this is an `ecatholic` row with both ids in `publication`; the listing is the fallback `other` channel. The masthead names St. Alphonsus Church alone; no other parish shares it, and the directory names no shared pastor for it.

## Worship sites

One church, St. Alphonsus Church, 1567 Temple Drive. The bulletin's Mass-schedule box gives one set of times and names no mission, chapel or second building. Our Lady of Mercy Regional Catholic School (29 Conwell Drive) is listed as the parish school only, with no Mass.

## Website and bulletin provider

stalphonsusparish.org is eCatholic-hosted (27039); `probe url` finds the `/bulletins` archive, which is current to 20261025.

## Fetch check

`fetch:check` (2026-10-28) with the `ecatholic` resolver picked `files.ecatholic.com/27039/bulletins/20261025.pdf`: transport ok, PDF, fresh (3 days); issue date inferred from the file name; identity `unverified` because the PDF has no text layer (cover and sidebar read from renders, above). That file is byte-identical to the listing's issue.

## Not yet confirmed

Pages 3-8 of the issue were not read.
