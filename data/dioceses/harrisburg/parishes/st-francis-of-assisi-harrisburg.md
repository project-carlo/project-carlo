---
name: Saint Francis of Assisi
website: https://stfrancisharrisburg.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://stfrancisharrisburg.org/bulletin/
publication: ['url:https://stfrancisharrisburg.org/bulletin/']
group: ''
evidence:
- url: https://stfrancisharrisburg.org/wp-content/uploads/2026/10/bulletin-2026-10-18-en.pdf
  seen: 2026-10-19
  quote: Dear Parish Family of St. Francis
  note: 'Page 2 of the 18 October 2026 English issue (3 pages), letter from Father Anthony (Very Rev.
    Anthony R. Dill). Page 1 Mass intentions: Saturday 17 October 5:00 p.m.; Sunday 18 October 7:30 a.m.,
    9:00 a.m., 12:00 noon, 2:00 p.m.'
- url: https://stfrancisharrisburg.org/wp-content/uploads/2026/10/bulletin-2026-10-18-en.pdf
  seen: 2026-10-19
  quote: Sunday, October 18 7:30 a.m.
  note: Page 1, Mass Intentions.
- url: https://stfrancisharrisburg.org/bulletin/
  seen: 2026-10-19
  quote: 1439 Market St Harrisburg, PA 17103 Parish Archive Sunday Bulletins
  note: The site's Bulletin page lists one post per Sunday ("Sunday, October 18, 2026", "Bulletin (English)");
    each post links an English and a Spanish PDF (bulletin-2026-10-18-en.pdf, -es.pdf).
- url: https://www.hbgdiocese.org/parishes/closed-parishes-and-records-locations/
  seen: 2026-10-19
  quote: Saint Francis of Assisi, Harrisburg
  note: The diocese's closed-parishes list (as of November 21, 2024) puts Holy Family, Harrisburg under
    St. Francis of Assisi. The diocese's site sometimes drops scripted connections (recheck on 2026-10-19
    got 'Remote end closed connection'); plain curl and a browser (visit.py) loaded it the same day.
promoted: 2026-10-20
---

## Publisher

Saint Francis of Assisi, 1439 Market Street, Harrisburg (Allison Hill) publishes its own weekly
bulletin on its own WordPress site, in English and Spanish. I read the 18 October 2026 English
issue: page 1 lists the week's Masses (Saturday 5:00 p.m.; Sunday 7:30 a.m., 9:00 a.m., 12:00 noon
and 2:00 p.m.), and page 2 is the pastor's letter to the "Parish Family of St. Francis". The
issue has no masthead naming another parish or building.

Holy Family, Harrisburg was merged into this parish (the diocese's closed-parishes list puts it
under St. Francis); see `excluded/holy-family-harrisburg`.

## Worship sites

- Saint Francis of Assisi, 1439 Market St., Harrisburg (`st-francis-of-assisi-harrisburg`).

## Website and bulletin provider

The directory's website (stfrancisharrisburg.com) redirects to stfrancisharrisburg.org, the same
parish. Its Bulletin page lists one post per Sunday ("Parish Bulletin October 18, 2026"), and each
post links `wp-content/uploads/<y>/<m>/bulletin-<date>-en.pdf` and `-es.pdf`. A Discover Mass page
exists (`st-francis-of-assisi-harrisburg-pa`) but lists no bulletins. `other`, website the
Bulletin page. The English and Spanish PDFs are one bulletin in two languages; the pipeline
should take the `-en` file.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): picked the 18 October 2026 English issue (bulletin-2026-10-18-en.pdf), which I read; recipe `page-pdfs` pinned.

## Not yet confirmed

Nothing.
