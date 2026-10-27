---
name: Holy Rosary Church
website: https://www.hrparish.com/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2100
publication: ['url:http://sponsors.bonventure.net/?page=2100']
group: Brandywine Hundred Deanery
evidence:
- url: http://sponsors.bonventure.net/pdfs/2100/2026-10-25.pdf
  seen: 2026-10-27
  quote: Rev. John J. Gayton
  note: 'Cover of the 25 October 2026 issue: ''Holy Rosary Church / THIRTIETH SUNDAY IN ORDINARY TIME
    • OCTOBER 25, 2026 / 3200 PHILADELPHIA PIKE, CLAYMONT, DELAWARE 19703'', Pastor Rev. John J. Gayton,
    Deacon Jose Perez, Hispanic Ministry. Read with pdftotext after fetching through Chrome (the host''s
    TLS chain fails verification outside the browser).'
- url: http://sponsors.bonventure.net/pdfs/2100/2026-10-25.pdf
  seen: 2026-10-27
  quote: 'Sunday: 8:00 am, 10:00 am, 12:30 pm (Español)'
  note: 'Mass schedule block, with ''Saturday: 4:30 pm''. One church.'
- url: http://sponsors.bonventure.net/?page=2100
  seen: 2026-10-27
  quote: Click to View Current Bulletin
  note: Bonventure page 2100, headed 'Holy Rosary Church, 3200 Philadelphia Pike • Claymont, DE 19703';
    dated issues listed weekly from 2026-10-25 back to August 2025.
- url: https://www.hrparish.com/
  seen: 2026-10-27
  note: Static fetch shows no bulletin link; the rendered page (visit.py) has a 'Bulletin' link to http://sponsors.bonventure.net/?page=2100.
---

## Publisher

Holy Rosary publishes its own weekly bulletin, hosted by Bonventure (sponsors.bonventure.net page 2100, a PDF per Sunday at `/pdfs/2100/<date>.pdf`). The 25 October 2026 issue's cover names Holy Rosary Church alone, with its own pastor (Rev. John J. Gayton, who is not the Holy Child / St. Helena pastor), and Mass schedule including the Spanish Mass.

## Worship sites

One church, 3200 Philadelphia Pike, Claymont. Mass (bulletin and diocese map agree): Saturday 4:30 pm; Sunday 8:00 am, 10:00 am, 12:30 pm (Español); weekdays 8:00 am. The Spanish Mass is a Sunday time at this church, not a separate site.

## Website and bulletin provider

hrparish.com is an OSV (Duda) site whose 'Bulletin' button goes to Bonventure; its HTML is invisible to `probe url` because the link is found only after rendering. The recipe uses the `http://` form of the Bonventure URL, as the Allentown and Scranton rows do: `https://sponsors.bonventure.net` fails certificate verification from this sandbox with `probe pdf` (SSLCertVerificationError, 2026-10-27), though Chrome loads it.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish holy-rosary-claymont` (2026-10-27): Resolved from hrparish.com to `page-pdfs on http://sponsors.bonventure.net/?page=2100`, picking `pdfs/2100/2026-10-25.pdf`, fresh, transport ok, document type PDF. Identity 'unverified' by the tool (no expected identity supplied); the cover read above settles it.

## Not yet confirmed

Nothing outstanding. If Bonventure moves to a valid certificate chain the `https://` form would work too.
