---
name: Cathedral of the Blessed Sacrament Parish, Altoona
website: https://www.altoonacathedral.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://www.altoonacathedral.org/bulletin/']
group: ''
evidence:
- url: https://www.altoonacathedral.org/download/24/bulletin-2026/2617/october-18-2026.pdf
  seen: 2026-10-21
  quote: Serving the People of God in the City of Altoona Since 1851
  note: 'Page 2 of the 18 October 2026 issue (2 pages, 3,296,001 bytes; page 1 is a pizzelle-party notice).
    Page 2 is the masthead: "THE CATHEDRAL OF THE BLESSED SACRAMENT, ONE CATHEDRAL SQUARE, Altoona, Pennsylvania
    16601-3315", Mass times, office phone 814-944-4603. It names the cathedral alone.'
- url: https://www.altoonacathedral.org/bulletin/
  seen: 2026-10-21
  note: The Bulletin page lists dated PDFs at /download/24/bulletin-2026/<id>/<month>-<day>-2026.pdf,
    weekly from january-11-2026 to october-18-2026 (the newest), and archive pages for 2014-2025.
promoted: 2026-10-21
---

## Publisher

The Cathedral of the Blessed Sacrament publishes its own weekly bulletin on its own site
(altoonacathedral.org, with `/download/` links;
`probe url` and `curl` read it directly). The newest issue on 21 October 2026
was dated October 18, 2026. Its page 2 is the masthead, which names the cathedral alone with
the Mass times and Msgr. Carson as contact; page 1 is a one-item notice (a pizzelle-making
event). The directory lists the parish with one church and no companion parish.

## Worship sites

One church, the Cathedral of the Blessed Sacrament (churches/cathedral-of-the-blessed-sacrament-altoona).
The diocese's parish pages list Mass only at that church. The cathedral is not in the
GCatholic roster that was fetched (alto0 list) but has its own GCatholic page,
`churches/northamerica/2439`.

## Website and bulletin provider

`bulletin_provider: other`, `website` the Bulletin page. `pnpm fetch:check --diocese
altoona-johnstown --parish cathedral-of-the-blessed-sacrament-altoona` on 2026-10-21 resolved
"page-pdfs on https://www.altoonacathedral.org/bulletin/: current" and fetched
`.../bulletin-2026/2617/october-18-2026.pdf` (url date 2026-10-18, status ok). Recipe
`page-pdfs` is the `provider_id`. `publication` is `url:` of the Bulletin page. The directory
homepage is `https://www.altoonacathedral.org`.

## Not yet confirmed

Nothing about the bulletin. The issues are thin (two pages); if the pipeline finds too
little in them, check whether the parish also posts a longer version.
