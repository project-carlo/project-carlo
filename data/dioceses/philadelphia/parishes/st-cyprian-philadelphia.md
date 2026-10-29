---
name: St. Cyprian
website: https://saintcyprianchurch.org
bulletin_provider: other
provider_id: page-pdfs https://saintcyprianchurch.org filename=bulletin_*.pdf
publication: ['url:https://saintcyprianchurch.org#st-cyprian']
group: ''
evidence:
- url: https://saintcyprianchurch.org/wp-content/uploads/2026/10/bulletin_10-25.pdf
  seen: 2026-10-29
  quote: ST. CYPRIAN CATHOLIC CHURCH
  note: '25 October 2026 issue, 8 pages, text layer. Page 1: ''525 S 63RD ST, PHILADELPHIA, PA 19143,
    T: 215-747-3250'', Pastor Msgr. Federico A. Britto, Parochial Vicar Fr. Rene Againglo, Deacon Anthony
    Willoughby; ''Mass Schedule: Weekdays 8:00 AM; Sunday 8:00 AM (English), 11:00 AM (English, Live Stream),
    1:00 PM (Igbo), 3:30 PM (Francophone)''. Lists one church.'
- url: https://saintcyprianchurch.org/
  seen: 2026-10-29
  note: The home page (www.saintcyprian.net, the directory's website, redirects here; WordPress.com) has
    a 'Weekly Bulletin' menu item and link to /wp-content/uploads/2026/10/bulletin_10-25.pdf (and the
    saintcyprianchurch.wordpress.com copy of the same path). The page's own nav carries no archive page
    of earlier issues (links read in the page source, so cited as a note).
- url: https://saintcyprianchurch.org/schedule-of-masses/
  seen: 2026-10-29
  quote: English Mass Sunday 8:00 am & 11:00 am Weekdays 8:00 am
  note: 'Parish Schedule of Masses page: also Nigerian Mass Sunday 1:00 pm and African French Mass Sunday
    3:30 pm, matching the bulletin box. It names no second church.'
- url: https://www.church-bulletin.org/saint-cyprian-church-philadelphia-pa-19143
  seen: 2026-10-28
  note: 'John Patrick listing 115 ''Saint Cyprian Church'', Philadelphia, PA 19143: no editions (raw/jppc-directory.json,
    latest empty).'
- url: https://archphila.org/parish/st-cyprian-philadelphia/
  seen: 2026-10-28
  quote: 'Merged with Our Lady of the Blessed Sacrament: 2013'
  note: 'Directory page (updated 7 months before): Rev. Msgr. Federico A. Britto, pastor; Cobbs Creek
    Pkwy. at Cedar Ave.; rectory 525 Cobbs Creek Pkwy.; website saintcyprian.net.'
promoted: 2026-10-29
bulletin_status: available
publication_reviews:
- parish: st-barbara-philadelphia
  decision: separate
  evidence:
  - url: https://saintcyprianchurch.org/wp-content/uploads/2026/10/bulletin_10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead names St. Cyprian Catholic Church alone, at 525 S 63rd St, with
      its own Mass schedule (8:00 AM and 11:00 AM English, 1:00 PM Igbo, 3:30 PM Francophone) and an 8-page
      layout; St. Barbara appears only in an events line ('St. Barbara's Events').
  - url: https://files.ecatholic.com/21577/bulletins/20261025.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead names Saint Barbara Catholic Church alone, at 5359 Lebanon Avenue,
      with its own Mass box; a 2-page issue on a different host.
---

## Publisher

St. Cyprian publishes its own bulletin as a PDF on its WordPress.com site, saintcyprianchurch.org (the directory's saintcyprian.net redirects there). The home page's 'Weekly Bulletin' menu item links the current file, `wp-content/uploads/2026/10/bulletin_10-25.pdf`; no archive page is linked, so only the newest issue is reachable from the site. John Patrick listing 115 has no editions.

## One bulletin with St. Barbara?

No. The two share Msgr. Federico A. Britto (pastor here, parochial administrator at St. Barbara; each directory page, 2026-10-28) but their 25 October 2026 issues are separate documents: this 8-page issue with a St. Cyprian masthead and Mass box, and St. Barbara's 2-page eCatholic issue with its own. The review in `publication_reviews` records the mastheads. St. Barbara appears here only as an events heading. St. Ignatius of Loyola, also under Msgr. Britto, has a third bulletin.

## Worship sites

One church, St. Cyprian (Cobbs Creek Pkwy. at Cedar Ave.). Our Lady of the Blessed Sacrament (345 N. 63rd St.) merged into St. Cyprian in 2013 and the 2013 decree said its church 'will remain open as a worship site'; the 25 October 2026 bulletin and the parish's Schedule of Masses page name no Mass there. It closed permanently as a place of worship on 1 August 2014 (CatholicPhilly, 4 August 2014): `excluded/our-lady-of-the-blessed-sacrament-philadelphia` (reconcile, 2026-10-29).

## Website and bulletin provider

`other`, reading the site. Fetch check: see below.

## Fetch check

`fetch:check` (2026-10-29) with the website alone printed `"recipe": "page-pdfs"` and picked `saintcyprianchurch.wordpress.com/wp-content/uploads/2026/10/bulletin_10-25.pdf`, the home page's own 'Weekly Bulletin' link (the `.org` path holds the same file name): transport ok, PDF, 25 October 2026, freshness fresh. I pinned `page-pdfs https://saintcyprianchurch.org filename=bulletin_*.pdf` as the recipe and re-ran it with the same pick. Identity `unverified` (no expected identity supplied); the masthead was read above.

## Not yet confirmed

Whether the site keeps older issues (none linked), which affects only how a late fetch behaves.
