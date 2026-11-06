---
name: St. Paul the Apostle (Corona)
website: https://saintpaulcorona.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q3 (Queens West)
evidence:
- url: https://saintpaulcorona.org/bulletins
  seen: 2026-11-05
  note: 'Tilma bulletins page, newest first: 24 PDFs, the newest St. Paul the Apostle Bulletin October
    5, 2025 (uploaded 2025-10-10); nothing from 2026.'
- url: https://saintpaulcorona.org/system/resources/W1siZiIsIjIwMjUvMTAvMTAvM3YzdjlqY2ZheV9TdC5fUGF1bF90aGVfQXBvc3RsZV9CdWxsZXRpbl9PY3RvYmVyXzVfMjAyNS5wZGYiXV0/St.%20Paul%20the%20Apostle%20Bulletin%20October%205%2C%202025.pdf
  seen: 2026-11-05
  quote: Saint Paul the Apostle Roman Catholic Church
  note: Page 1 masthead of the last posted issue (October 5, 2025) names Saint Paul the Apostle Roman
    Catholic Church, 98-16 55th Avenue, Corona alone; Saturday 5:00pm, 7:00pm; Sunday 9:00am, 11:00am;
    Mon-Fri 8:30am.
- url: https://saintpaulcorona.org/mass-times
  seen: 2026-11-05
  quote: SATURDAY 5pm – English 7pm – Español
  note: 'The parish''s Mass Times page: Sunday 9am English, 11am Español; Saturday 5pm, 7pm; Mon-Fri 8:30am
    bilingual; one church.'
- url: https://www.discovermass.com/church/st-paul-the-apostle-corona-ny/
  seen: 2026-11-05
  quote: There are currently no bulletins available for St. Paul the Apostle.
  note: Discover Mass names saintpaulcorona.org as the website and has no bulletins.
research:
- method: Tilma bulletins page, fetch:check with page-pdfs recipe, Discover Mass church page
  url: https://saintpaulcorona.org/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reread /bulletins; if a 2026 issue is posted, set bulletin_provider other with provider_id
    page-pdfs https://saintpaulcorona.org/bulletins and rerun fetch:check
  retry_when: saintpaulcorona.org/bulletins lists an issue newer than October 5, 2025
  revisit_after: 2027-01-05
bulletin_status: not-found
---

## Publisher

St. Paul the Apostle published its own weekly bulletin on its Tilma site, but has posted none for a year. On 2026-11-05 `https://saintpaulcorona.org/bulletins` listed 24 issues, the newest "St. Paul the Apostle Bulletin October 5, 2025" (uploaded 2025-10-10). That issue's page 1 masthead names "Saint Paul the Apostle Roman Catholic Church / 98-16 55th Avenue, Corona, New York, 11368" alone. fetch:check with `page-pdfs https://saintpaulcorona.org/bulletins` picked that file and rated it stale (396 days). Discover Mass has no bulletins for the parish.

## Worship sites

One church, St. Paul the Apostle, 98-16 55th Avenue. The October 2025 bulletin and the site's /mass-times page (read 2026-11-05) give Saturday 5pm (English), 7pm (Spanish), Sunday 9am (English), 11am (Spanish) and Mon-Fri 8:30am, naming no other place.

## Website and bulletin provider

`no_bulletin`: no current bulletin was found, so the row stays in the records and off the site (Settled policy 4). The website is the parish's Tilma site, which the diocese directory and Discover Mass also give. If issues resume, it is a Tilma `page-pdfs https://saintpaulcorona.org/bulletins` row like its neighbours.

## Not yet confirmed

Whether the parish still prints a bulletin it no longer posts, or posts it elsewhere; see research.
