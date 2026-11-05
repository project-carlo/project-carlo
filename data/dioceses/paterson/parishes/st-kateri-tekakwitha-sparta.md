---
name: St. Kateri Tekakwitha
website: https://saintkateri.org/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:11335']
group: ''
evidence:
- url: https://files.ecatholic.com/11335/bulletins/20261101.pdf
  seen: 2026-11-04
  note: 'Page 1 of the 1 November 2026 issue (8 pages) is an image (no text layer; read with render.py):
    ''THE PARISH COMMUNITY OF SAINT KATERI TEKAKWITHA, 427 STANHOPE ROAD, SPARTA, NEW JERSEY 07871, NOVEMBER
    1, 2026, ALL SAINTS''.'
- url: https://files.ecatholic.com/11335/bulletins/20261101.pdf
  seen: 2026-11-04
  quote: 9:30 AM, 11:30 AM, 6:00 PM
  note: 'Page 2, CELEBRATION OF THE EUCHARIST: Daily Mass at 8:15 AM (Monday ~ Friday), Saturday at 5:00
    PM, Sunday at 8:00 AM, 9:30 AM, 11:30 AM, 6:00 PM; SPANISH MASS Sunday at 2:00 PM. Pastor Fr. Michael
    Lee. A grep for ''chapel'' finds nothing; the Bon Venture ad footer on page 8 reads ''070B (PK) -
    Blessed Kateri, Sparta''.'
- url: https://saintkateri.org/bulletins
  seen: 2026-11-04
  note: The parish's eCatholic site (site id 11335, behind Cloudflare; read in headed Chrome with parish-site-access
    visit.py). The Bulletins page lists weekly issues at files.ecatholic.com/11335/bulletins/<YYYYMMDD>.pdf,
    newest November 1, 2026, then October 25, 18, 11, 4, September 27 ...
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Kateri Tekakwitha, Sparta posts a weekly bulletin on its eCatholic site (site id 11335). It is printed by Bon Venture (ad footer "070B (PK) - Blessed Kateri, Sparta" on page 8), but the parish posts it itself, so eCatholic is the host. Page 1 of the 1 November 2026 issue (`https://files.ecatholic.com/11335/bulletins/20261101.pdf`) is an image, read with render.py: "The Parish Community of Saint Kateri Tekakwitha, 427 Stanhope Road, Sparta, New Jersey 07871, November 1, 2026, All Saints". Page 2 gives daily Mass 8:15 AM Monday to Friday, Saturday 5:00 PM, Sunday 8:00, 9:30, 11:30 AM and 6:00 PM, and a Spanish Mass Sunday at 2:00 PM.

## Worship sites

- `st-kateri-tekakwitha-sparta`: the only church in the schedule; the bulletin names no mission or chapel.

The diocese's finder (directory:11335) and GCatholic (19037) each list this one church.

## Website and bulletin provider

The website is the eCatholic site; provider `ecatholic` reads the `/bulletins` archive, whose newest link on 2026-11-04 was the 1 November 2026 issue (the 8 November issue was not yet posted). `fetch:check` on 2026-11-04 picked `https://files.ecatholic.com/11335/bulletins/20261101.pdf` (fresh, age 3 days); identity reports unverified because page 1 is an image-only cover with no text.

## Not yet confirmed

Nothing outstanding.
