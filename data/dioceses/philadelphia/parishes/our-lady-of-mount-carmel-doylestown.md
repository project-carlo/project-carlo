---
name: Our Lady of Mount Carmel Parish
website: https://www.ourladymtcarmel.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-mount-carmel-catholic-church-doylestown-pa-18901
publication: ['url:https://www.church-bulletin.org/our-lady-of-mount-carmel-catholic-church-doylestown-pa-18901']
group: ''
evidence:
- url: https://www.church-bulletin.org/our-lady-of-mount-carmel-catholic-church-doylestown-pa-18901
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 64, 'Our Lady of Mount Carmel Catholic Church', Doylestown, PA 18901, 235
    East State Street, phone (215) 348-4190; latest edition October 25, 2026, dated archive back to November
    2024.
- url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-catholic-church-doylestown-pa-18901/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages, image-only; pages 1-3 rendered). Page 1 masthead ''Our Lady
    of Mount Carmel Catholic Church, Doylestown, Pennsylvania'', signed Father Matthew Guckin. Page 2
    ''Our Lady of Mount Carmel Church, 235 East State Street, Doylestown, PA 18901''. Page 3 ''Weekly
    Mass Schedule'': ''Sunday 7:00 AM, 9:00 AM, 10:30 AM & 12:00 Noon; Monday - Friday 8:00 AM; Saturday
    5:00 PM Vigil''. Names this parish alone.'
- url: https://www.ourladymtcarmel.org/parish-bulletins
  seen: 2026-10-29
  note: 'Parish site (Duda): its Bulletins page lists irp.cdn-website.com/502397d4/files/uploaded/2026-10-25.pdf,
    2026-10-18.pdf, 2026-10-11.pdf ... newest first, and links jppc.net/onlinebulletins/064template.pdf.
    The 2026-10-25.pdf copy is byte-identical (md5 412019524b38e0a7a9e1488d8767b40c) to the listing''s
    2026-10-25.pdf. Link list read in the browser (visit.py), so not a quotable string.'
- url: http://olmcs.org
  seen: 2026-10-29
  note: The directory's website for this parish, olmcs.org, is titled 'Our Lady of Mount Carmel School'
    (the parish school's site), not the parish's. The parish site is ourladymtcarmel.org (the footer of
    the bulletin's page 1 prints www.ourladymtcarmel.org).
- url: https://archphila.org/parish/our-lady-of-mount-carmel-doylestown/
  seen: 2026-10-29
  quote: Rev. Matthew W. Guckin
  note: 'Directory: pastor; rectory 235 E. State St., Doylestown 18901-4770; page updated 3 weeks ago.'
research:
- method: visit.py on the parish site's /parish-bulletins page and curl of the 2026-10-25.pdf copy; md5
    against the listing's PDF
  url: https://www.ourladymtcarmel.org/parish-bulletins
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

Our Lady of Mount Carmel Parish, Doylestown (Rev. Matthew W. Guckin, Pastor) prints its bulletin with John Patrick Publishing: listing 64 (`church-bulletin.org/?id=064`) has an issue for 25 October 2026 and a dated archive back to November 2024, and the parish's own site links the same listing (`jppc.net/onlinebulletins/064template.pdf`). The row is `other`, `page-pdfs` on the listing. The parish site's Bulletins page also carries `irp.cdn-website.com/.../files/uploaded/<yyyy-mm-dd>.pdf` copies, newest first; the 25 October 2026 copy is byte-identical to the listing's, so either channel serves, and the listing is kept as the recipe (see the playbook's note on byte-identical site copies). The PDFs have no text layer, so the masthead and Mass schedule were read from renders of pages 1-3.

## Worship sites

One church, Our Lady of Mount Carmel, 235 East State Street. The page-3 'Weekly Mass Schedule' lists every Mass at the one church (no mission, chapel or second location). Page 2 of the 25 October issue also prints 'Sacrament of Reconciliation at the Shrine of Our Lady of Czestochowa' and 'at Our Lady of Guadalupe' boxes; those are other Doylestown-area places, not Mount Carmel worship sites, and Our Lady of Guadalupe has its own bulletin (own row). The National Shrine of Our Lady of Czestochowa (654 Ferry Road, Doylestown, Pauline Fathers) is in neither the directory nor the GCatholic roster; it has public Mass but no bulletin and is excluded `no-bulletin` (reconcile, 2026-10-29: excluded/national-shrine-of-our-lady-of-czestochowa-doylestown). The Czestochowa box on page 2 gives confession hours, not a Mass schedule.

## Website and bulletin provider

`https://www.ourladymtcarmel.org` is the parish's own site (Duda-built). The directory's `olmcs.org` is the parish school's site and does not carry the bulletin. Directory Mass times (Saturday vigil 5 PM, Sunday 7, 9, 10:30 AM, noon, weekdays 8 AM) match page 3.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on the listing picked `2026-10-25.pdf`: transport ok, PDF, fresh (4 days, date inferred from the file name); identity `unverified` because no expected identity is supplied by the check and the PDF has no text layer (masthead read from a render). It printed no `recipe` line, as the pinned `provider_id` already holds it.

## Not yet confirmed

Pages 4-12 were not read.
