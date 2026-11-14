---
name: Our Lady of Guadalupe
website: https://www.iglesiaguadalupe.com/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=5008
publication: ['url:http://sponsors.bonventure.net/?page=5008']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/5008/2026-11-15.pdf
  seen: 2026-11-12
  quote: 150D (CK) • Our Lady of Guadalupe, Danbury, CT
  note: '15 November 2026 issue (6 pages). Page 1 rendered with render.py (its text layer is garbled):
    masthead ''OUR LADY OF GUADALUPE PARISH, 29 Golden Hill Road Danbury, CT 06811, Website: iglesiaguadalupe.com'',
    ''XXXIII SUNDAY IN ORDINARY TIME''; MASS SCHEDULE / HORARIOS DE MISAS: Monday to Friday 7:00 PM Spanish,
    Saturday Vigil 7:00 PM Spanish, Sunday 7:30 AM, 10:00 AM, 12:30 PM, 3:00 PM (All Spanish Masses),
    Holy Days 9:00 AM Spanish; Rev. Elio Sosa, Pastor. Page 6 ad footer quoted (Bon Venture Services).
    Names no other church.'
- url: https://www.iglesiaguadalupe.com/
  seen: 2026-11-12
  note: Wix site; its bulletin button links http://sponsors.bonventure.net/?page=5008, which lists pdfs/5008/2026-11-01.pdf,
    2026-11-08.pdf and 2026-11-15.pdf among its issues.
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

Our Lady of Guadalupe, Danbury publishes its own weekly bulletin, printed by Bon Venture Services and posted on Bon Venture's sponsor page 5008. The 15 November 2026 issue (`http://sponsors.bonventure.net/pdfs/5008/2026-11-15.pdf`, read 2026-11-12) is headed "OUR LADY OF GUADALUPE PARISH, 29 Golden Hill Road Danbury, CT 06811" with Rev. Elio Sosa as pastor, and its page 6 footer reads "150D (CK) • Our Lady of Guadalupe, Danbury, CT". It names no other church.

## Worship sites

- `our-lady-of-guadalupe-danbury`: page 1 gives Monday-Friday 7:00pm, Saturday Vigil 7:00pm, Sunday 7:30am, 10:00am, 12:30pm and 3:00pm, all in Spanish, and Holy Days 9:00am. The diocese's directory (directory:1354) and GCatholic (22023) list this one church. Page 1 also gives hours for a faith-formation "Satélite" coordinator, an office, not a Mass site.

## Website and bulletin provider

`iglesiaguadalupe.com` is a Wix site with no bulletin PDFs of its own; its bulletin button links `http://sponsors.bonventure.net/?page=5008`, which lists dated issues (`pdfs/5008/<YYYY-MM-DD>.pdf`). Provider `other`, pinned `page-pdfs` on the sponsor page. Page 1's text layer is garbled (the Mass table extracts as fragments), so the masthead and schedule above were read from a render; the pipeline may need to read that page as an image.

`fetch:check` on 2026-11-12 run headed with `PLAYWRIGHT_BROWSER_CHANNEL=chrome` resolved the sponsor page to `pdfs/5008/2026-11-15.pdf` but fetched it as `https://sponsors.bonventure.net/...`, which failed TLS verification ("CERTIFICATE_VERIFY_FAILED"); run without the Chrome channel the same day it fetched `http://sponsors.bonventure.net/pdfs/5008/2026-11-15.pdf`, the 15 November 2026 issue read above (`ok`, freshness `future` because Bon Venture posts before the Sunday; identity unverified as reported, masthead checked by hand).

## Not yet confirmed

Nothing open.
