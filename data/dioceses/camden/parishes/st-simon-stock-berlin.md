---
name: St. Simon Stock Parish
website: https://www.stsimonstock.net/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2221
publication: ['url:http://sponsors.bonventure.net/?page=2221#bon-venture-2221']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/2221/2026-11-01.pdf
  seen: 2026-10-29
  quote: Rev. Michael A. de Leon, A.M., Pastor
  note: 'Page 1 of the 1 November 2026 issue (12 pages, text layer): ''Saint Simon Stock Parish'', ''178
    W. WHITE HORSE PIKE • BERLIN, NJ 08009'', ''established in 2009 from the merger of Saint Edward Church
    (Pine Hill) and Our Lady of Mount Carmel Church (Berlin)'', and a Mass Schedule block.'
- url: http://sponsors.bonventure.net/pdfs/2221/2026-11-01.pdf
  seen: 2026-10-29
  quote: 'Sunday: 8:00, 10:00 am & 12:00 pm'
  note: 'The Mass Schedule block on page 1 also gives ''Monday - Saturday: 8:00 am'' and ''Saturday: 4:00
    pm''. It names no church other than the parish''s own.'
- url: http://sponsors.bonventure.net/?page=2221
  seen: 2026-10-29
  quote: St. Simon Stock Parish
  note: 'Bon Venture sponsor page for the parish: ''Click to View Current Bulletin'' and a list of dated
    issues from 1 November 2026 back to 2025 and earlier; the file links are pdfs/2221/<date>.pdf.'
- url: https://www.stsimonstock.net/
  seen: 2026-10-29
  quote: 'Saturday: 4PM'
  note: 'Parish site: Mass Times Saturday 4PM, Sunday 8AM, 10AM, 12PM, daily Monday - Saturday 8AM; its
    Bulletins button links sponsors.bonventure.net/?page=2221.'
promoted: 2026-10-30
publication_reviews:
- parish: holy-eucharist-cherry-hill
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/?page=2221
    seen: 2026-10-29
    note: Bon Venture sponsor page 2221 serves St. Simon Stock Parish, 178 West White Horse Pike, Berlin,
      NJ 08009, with its own list of dated issues; the 1 November 2026 issue's masthead names St. Simon
      Stock Parish alone.
  - url: http://sponsors.bonventure.net/?page=2088
    seen: 2026-10-29
    note: 'Bon Venture sponsor page 2088 serves Holy Eucharist Parish, 344 Kresson Road, Cherry Hill,
      NJ 08034: a separate account and issue list on the same host, for a different parish.'
---

## Publisher

St. Simon Stock publishes its own weekly bulletin through Bon Venture Services (sponsor page 2221), which the parish site's Bulletins button links. The 1 November 2026 issue (read 2026-10-29, posted ahead of its Sunday) is a text-layer PDF headed 'Saint Simon Stock Parish, 178 W. White Horse Pike, Berlin, NJ 08009'. It names Rev. Michael A. de Leon, A.M., as pastor, Rev. Joseph D. Ciar, A.M., as parochial vicar and says the parish was 'established in 2009 from the merger of Saint Edward Church (Pine Hill) and Our Lady of Mount Carmel Church (Berlin), under the pastoral care of the Religious Institute of the Alagad ni Maria (Disciples of Mary)'. Its Mass schedule: Monday - Saturday 8:00 am, Saturday 4:00 pm, Sunday 8:00, 10:00 am and 12:00 pm.

## Worship sites

One confirmed: Our Lady of Mount Carmel, 178 W. White Horse Pike, Berlin (church record `our-lady-of-mount-carmel-berlin`), the address on the masthead, the directory and the site. GCatholic also lists St. Edward, 500 Erial Rd., Pine Hill under this parish; the bulletin and the site give one set of Mass times and name neither Pine Hill nor St. Edward as a Mass site, so it sits in `open/st-edward-pine-hill` until a source says whether Mass is held or the church closed. The parish also has Our Lady of Mt. Carmel School at the same address (a school).

## Website and bulletin provider

The directory (http://www.stsimonstock.net/) and GCatholic (stsimonstock.net) resolve to https://www.stsimonstock.net/ (200). `other` with a `page-pdfs` recipe on Bon Venture's page over `http://` (the https host fails TLS verification in Python).

`fetch:check` (2026-10-29): the recipe picks `pdfs/2221/2026-11-01.pdf` (transport ok, PDF, issue date inferred from the URL, freshness `future` because Bon Venture posts an issue before its Sunday, not a wrong pick; parish identity read from the masthead above).

## Not yet confirmed

Whether St. Edward, Pine Hill holds Mass (see the open record). Nothing blocks the bulletin itself.
