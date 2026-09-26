---
name: St. Anthony of Padua
website: https://stanthonysyr.org
bulletin_provider: other
provider_id: ''
publication: ['url:https://stanthonysyr.org/']
group: 'Fr. Kurgan: Holy Cross, St. Daniel, St. Anthony of Padua'
evidence:
- url: https://stanthonysyr.org/wp-content/uploads/St.Anthonys-Bulletin-September-20-2026.pdf
  seen: 2026-09-26
  note: 'The 20 September 2026 issue, 4 pages, image-only (no text layer; read by rendering page 1). Its
    page-1 masthead reads "St. Anthony of Padua / San Antonio de Padua", "Mass Schedule | Horario de Misas:
    Sunday 9am (English) 11am (Español)", "1515 Midland Ave. Syracuse NY", "Office | Oficina Located @
    Holy Cross Church 4112 E Genesee Street DeWitt NY 13214".'
- url: https://stanthonysyr.org/
  seen: 2026-09-26
  note: The homepage links the current bulletin PDF directly (href wp-content/uploads/St.Anthonys-Bulletin-September-20-2026.pdf
    on 2026-09-26; visit.py --bulletin found it there; no separate bulletin page).
---

## Publisher

St. Anthony of Padua publishes its own weekly bilingual bulletin, linked from its
homepage. I read the 20 September 2026 issue by rendering its pages (the PDF is scanned
images with **no text layer**, so `probe pdf` returns nothing and the pipeline's text
extraction will not read it either): page 1 names St. Anthony of Padua / San Antonio de
Padua, 1515 Midland Ave., with Sunday Mass at 9 am (English) and 11 am (Spanish), and says
the office is "Located @ Holy Cross Church" in DeWitt. The diocese lists Rev. John Kurgan
(pastor of Holy Cross and St. Daniel) as its administrator, and Rev. Brendan Foley with a
"special ministry, Spanish apostolate" there; neither Holy Cross's nor St. Daniel's
bulletin covers St. Anthony, so it is its own row.

## Worship sites

One: the church at 1515 Midland Avenue (`st-anthony-of-padua-syracuse`).

## Website and bulletin provider

stanthonysyr.org (WordPress) links the week's PDF from the homepage
(wp-content/uploads/St.Anthonys-Bulletin-<Month>-<day>-<year>.pdf). Provider `other`,
publication `url:` of the homepage.

## Not yet confirmed

The bulletin is image-only; if the pipeline cannot OCR it this row will yield no events.
