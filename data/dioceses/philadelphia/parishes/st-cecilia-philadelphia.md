---
name: St. Cecilia Church
website: https://www.stceciliafc.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-cecilia-church-philadelphia-pa-19111
publication: ['url:https://www.church-bulletin.org/saint-cecilia-church-philadelphia-pa-19111']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-cecilia-church-philadelphia-pa-19111/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue, 12 pages, image only (pdftotext reads nothing), pages 1-2 rendered. Page
    1 title ''St. Cecilia Church - Fox Chase, October 25, 2026 - 30th Sunday of Ordinary Time'' over a
    Mass Intentions list (Sunday 8:00 am, 11:00 am, 5:00 pm; weekdays 6:30 am and 8:30 am; Saturday 8:30
    am and 5:00 pm) and a calendar. Page 2: ''Saint Cecilia Church, 535 Rhawn Street Philadelphia, PA
    19111'', Pastor Rev. Christopher M. Walsh, Parochial Vicar Rev. Phong Le, parish 215-725-1240, www.stceciliafc.org,
    page footer ''#179'' (the listing id). It names this parish alone; the issue prints no separate Mass-times
    box.'
- url: https://www.church-bulletin.org/bulletin/saint-cecilia-church-philadelphia-pa-19111/2026-08-02.pdf
  seen: 2026-10-29
  quote: St. Cecilia Church - Fox Chase
  note: Older issue with a text layer (12 pages, 2 August 2026) giving the same masthead and the '#179'
    footer; its intentions list shows the summer schedule (Sunday 8:00 and 11:00 am; Monday-Friday 8:30
    am; 'The Monday to Friday 6:30 am Mass will return on September 1st').
- url: https://www.church-bulletin.org/saint-cecilia-church-philadelphia-pa-19111
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 179, 'Saint Cecilia Church', Philadelphia, PA 19111; latest edition October
    25, 2026.
- url: https://www.stceciliafc.org/
  seen: 2026-10-29
  note: 'Parish site answers 403 to probe url and loads in visit.py (title ''St. Cecilia Church - Philadelphia,
    PA''; behind Cloudflare, read in a browser). Its only bulletin link is ''https://church-bulletin.org/?id=179''.
    Mass Times page: Saturday 5:00 pm; Sunday 6:30, 8:00, 9:30, 11:00 am and 5:00 pm (not June-August);
    weekdays 6:30 am (not August) and 8:30 am; Saturday 8:30 am.'
research:
- method: visit.py on the parish site, listing 179, downloaded and rendered the 25 October issue, read
    a text-layer issue
  url: https://www.stceciliafc.org/
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
---

## Publisher

St. Cecilia, Fox Chase prints with John Patrick Publishing: listing 179 has an issue for 25 October 2026 (12 pages, image only). The masthead names St. Cecilia alone and page 2 carries the '#179' footer. Older issues (2 August 2026, 1 March 2026) have a text layer and the same masthead.

## Worship sites

One: St. Cecilia Church, 535 Rhawn St. No other place appears in the intentions list, calendar or site. The convent grotto (rosary, Mondays) is a devotion, not a Mass.

## Website and bulletin provider

`other`, `page-pdfs` on the listing https://www.church-bulletin.org/saint-cecilia-church-philadelphia-pa-19111. The site stceciliafc.org is behind a bot check (403 to `probe url`) and links only the listing.

## Not yet confirmed

The current issue is image-only and prints no Mass-times box: the Mass times come from its intentions list and the parish site. `fetch:check` reports identity `unverified`, as for any image-only issue.
