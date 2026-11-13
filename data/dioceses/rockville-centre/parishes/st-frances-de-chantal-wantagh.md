---
name: St. Frances de Chantal
website: https://saintjanefrances.org/
bulletin_provider: other
provider_id: page-pdfs https://saintjanefrances.org/ filename=*_20*_*.pdf
publication: ['url:https://saintjanefrances.org/#st-frances-de-chantal']
group: ''
evidence:
- url: https://saintjanefrances.org/wp-content/uploads/sites/99/2026/11/nov8_2026_saintjan_compressed.pdf
  seen: 2026-11-13
  note: 'Page 1 of the issue for November 7-8, 2026 (20 pages; InDesign, compressed with iLovePDF), read
    as an image: ''THE ROMAN CATHOLIC PARISH OF St. Frances de Chantal'', ''www.saintjanefrances.org •
    1309 Wantagh Avenue . Wantagh . New York . 11793''. Saturday Vigil Mass 4:00 p.m., 5:30 p.m.; Sunday
    Masses 7:00 a.m., 8:30 a.m., 10:00 a.m., 12 Noon, 5:00 p.m.; Weekday Masses Monday-Friday 7 a.m. &
    9 a.m., Saturday 8:30 a.m. Pastoral Staff: Rev. Seth N. Awo Doku, Pastor.'
- url: https://saintjanefrances.org/
  seen: 2026-11-13
  note: 'WordPress home page (probe url could not connect, RemoteDisconnected; read with visit.py) links
    the current bulletin only: .../2026/11/nov8_2026_saintjan_compressed.pdf, besides ThanksgivingDinner.pdf,
    Catholic-Online-Media.pdf and anInvitation.pdf.'
- url: https://saintjanefrances.org/wp-json/wp/v2/media?search=compressed&per_page=20&_fields=source_url,date
  seen: 2026-11-13
  note: 'WordPress media list (visit.py): weekly uploads named <month><day>_2026_<saintjan|saintjane|stjane|SAINTJAN>_compressed.pdf,
    e.g. nov1_2026_saintjan_compressed.pdf, oct25_2026_saintjane_compressed_compressed.pdf, oct18_2026_stjane_compressed.pdf.'
promoted: 2026-11-13
bulletin_status: available
---

## Publisher

St. Frances de Chantal, 1309 Wantagh Avenue, Wantagh publishes its own weekly bulletin on its WordPress site (laid out in InDesign by the parish; no printer's id or LPi/John Patrick marks). The issue for November 7-8, 2026 (`https://saintjanefrances.org/wp-content/uploads/sites/99/2026/11/nov8_2026_saintjan_compressed.pdf`, 20 pages, read 2026-11-13) has the page 1 masthead "THE ROMAN CATHOLIC PARISH OF St. Frances de Chantal ... 1309 Wantagh Avenue . Wantagh . New York . 11793" and names Rev. Seth N. Awo Doku, Pastor. Its Mass schedule: Saturday Vigil 4:00 p.m. and 5:30 p.m.; Sunday 7:00 a.m., 8:30 a.m., 10:00 a.m., 12 Noon and 5:00 p.m.; Monday-Friday 7 a.m. and 9 a.m.; Saturday 8:30 a.m. Page 1 is laid out as an image with little text, so it was rendered and read as an image.

## Worship sites

One: the church at 1309 Wantagh Avenue (`st-frances-de-chantal-wantagh-church`). The bulletin's schedule names no other building; its parish calendar places the Thanksgiving and KoC Masses in the "Church", and the "Pastoral Center Chapel" it mentions hosts a group meeting, with no Mass listed there. The diocesan locator (directory:42), GCatholic (16929) and the drvc.org Mass-times page list only this church, and the Mass-times schedule matches the bulletin's.

## Website and bulletin provider

saintjanefrances.org (the address every list gives; the parish's domain uses St. Jane Frances, the saint's other name) is a WordPress site that `probe url` could not connect to (RemoteDisconnected) and `visit.py` reads. The home page links only the current bulletin; there is no bulletin archive page. Its file names vary week to week (`nov8_2026_saintjan_compressed.pdf`, `oct18_2026_stjane_compressed.pdf`, `oct25_2026_saintjane_compressed_compressed.pdf`), so the recipe pins page-pdfs on the home page with `filename=*_20*_*.pdf` to keep the other PDFs linked there (ThanksgivingDinner.pdf, Catholic-Online-Media.pdf, anInvitation.pdf) out. `fetch:check` (2026-11-13) picked `nov8_2026_saintjan_compressed.pdf`, the 8 November 2026 issue and the newest uploaded ("page-pdfs on https://saintjanefrances.org/: first-listed"); it could not date the issue itself.

## Not yet confirmed

A flyer whose name has the pattern (e.g. a `..._2026_...` event PDF) could be picked instead of the bulletin. If a later fetch picks a non-bulletin, tighten the filename filter.
