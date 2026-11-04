---
name: Cathedral Basilica of the Sacred Heart, Newark
website: https://www.newarkbasilica.org/bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.newarkbasilica.org/bulletin filename=Monumental-Faith-*.pdf
publication: ['url:https://www.newarkbasilica.org/bulletin']
group: ''
evidence:
- url: https://www.newarkbasilica.org/s/Monumental-Faith-Nov-1-2026-EN-ES.pdf
  seen: 2026-11-04
  note: '1 November 2026 issue, 16 pages, image only (no text layer; read pages 1-2 rendered with render.py).
    Page 1 masthead: ''MONUMENTAL FAITH / The Bulletin for the Cathedral Basilica of the Sacred Heart'',
    ''November 1, 2026, Solemnity of All Saints''. Page 2: ''Cathedral Basilica of the Sacred Heart, 89
    Ridge St., Newark, NJ 07104''; Mass times: Saturday vigil 5:00 pm; Sundays 8:30 am, 10:00 am (Espanol),
    12:00 Noon; weekdays Mon-Fri 7:30 am, Tue/Thu/Fri 5:30 pm, Wednesdays and 1st Fridays 7:00 pm (Spanish);
    Saturdays 9:00 am (Spanish). No other church named.'
- url: https://www.newarkbasilica.org/bulletin
  seen: 2026-11-04
  note: Squarespace bulletin page; the first link is '/s/Monumental-Faith-Nov-1-2026-EN-ES.pdf' 'November
    1, 2026 - Solemnity of All Saints', then the October 2026 issues (Monumental-Faith-Oct-25-2026-EN-ES.pdf
    ...) and older CBSH-Monumental-Faith-<MMDDYY>.pdf issues back to 2024 and CBSH-<MMDDYY>.pdf from 2023.
    Two links labelled 'November 2, 2026' and 'November 9, 2026' point to 2025 files (CBSH-Monumental-Faith-103125.pdf,
    -110825.pdf).
bulletin_status: available
---

## Publisher

The Cathedral Basilica of the Sacred Heart publishes its own weekly bulletin, 'Monumental Faith', in English and Spanish, posted as PDFs on its Squarespace site. I read the 1 November 2026 issue (16 pages, image only, pages 1-2 rendered): page 1 masthead 'MONUMENTAL FAITH / The Bulletin for the Cathedral Basilica of the Sacred Heart', dated 'November 1, 2026, Solemnity of All Saints'; page 2 gives the address '89 Ridge St., Newark, NJ 07104', the clergy (Rev. Matthew Gonzalez, Rector) and one Mass schedule for the cathedral. No printer's footer was seen on pages 1-2; it is self-produced.

## Worship sites

- Cathedral Basilica of the Sacred Heart, 89 Ridge Street (`cathedral-basilica-sacred-heart-newark`): Saturday vigil 5:00 pm; Sunday 8:30 am, 10:00 am (Spanish), 12:00 noon; weekday Masses (page 2 of the 1 November 2026 issue).

The directory (127) lists only the cathedral. GCatholic has no entry for it in this roster.

## Website and bulletin provider

https://www.newarkbasilica.org/bulletin lists the issues newest first as `/s/<name>.pdf` links. Names changed in late September 2026 from `CBSH-Monumental-Faith-<MMDDYY>.pdf` to `Monumental-Faith-<Mon>-<D>-2026-EN-ES.pdf`. Two links further down the page are labelled 'November 2, 2026' and 'November 9, 2026' but point to 2025 files (`CBSH-Monumental-Faith-103125.pdf`, `-110825.pdf`), and a first fetch check filtering on `*Monumental-Faith*.pdf` picked `CBSH-Monumental-Faith-110825.pdf` (2025). So the recipe filters on the new prefix only, `filename=Monumental-Faith-*.pdf`, which also leaves out the parking-map PDF. Provider `other`, `page-pdfs` on the bulletin page. The current issues are image-only, so the pipeline has to read them as images.

Fetch check (2026-11-04, headed, recipe as in `provider_id`): transport ok, PDF (no text on page 1), picked `Monumental-Faith-Nov-1-2026-EN-ES.pdf`, issue date 2026-11-01 inferred from the file name, freshness fresh. That is the 1 November 2026 issue read above. Identity `unverified` only because no expected identity is supplied.

## Not yet confirmed

Nothing open for the row.
