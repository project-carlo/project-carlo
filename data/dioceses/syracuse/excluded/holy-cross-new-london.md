---
name: Holy Cross Church
reason: closed
line1: ''
city: New London
state: NY
postal_code: ''
decided: 2026-09-26
roster: ['directory:36300']
evidence:
- url: https://www.syracusediocese.org/parishfinder
  seen: 2026-09-26
  note: 'Listed in Diocese of Syracuse parish finder (Mass-times map) as ''Holy Cross (Closed)'', New
    London, NY; kind: closed'
- url: https://www.syracusediocese.org/spirit-of-hope-oneida
  seen: 2026-09-26
  quote: Sacramental Records for Holy Cross, New London
  note: behind Cloudflare; read in a browser (parish-site-access visit.py). The diocese's Spirit of Hope
    page keeps its records; Holy Cross is not among the seven churches the page lists. The diocese's parish
    list (read 2026-09-26) says 'Holy Cross, New London (CLOSED - See Spirit of Hope Catholic Community,
    Oneida)'.
- url: https://container.parishesonline.com/bulletins/04/0592/20260927B.pdf
  seen: 2026-09-26
  note: The 27 September 2026 issue is scanned images with no text layer (and at 31 MB is over `probe
    pdf`'s 30 MB cap); read by extracting the page-1 image and viewing it. The masthead's four worship
    sites and Mass schedule do not include New London.
parish: spirit-of-hope-oneida
---

## Why it is excluded

The diocese's parish list marks Holy Cross, New London, "CLOSED - See Spirit of Hope Catholic
Community, Oneida", its sacramental records are kept by Spirit of Hope, and Spirit of Hope's
current schedule (27 September 2026 masthead: St. Agatha, St. Mary of the Lake, St. Joseph,
Holy Family) has no Mass there. It is not named in the 2023 Spirit of Hope decree, so it closed
before that; no date, street address or news source was found (the diocese's finder gives none,
and it is not in GCatholic).

## What would change this

Nothing expected. A dated source for the closure would fill in `last_mass`.
