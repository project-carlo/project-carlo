---
name: St. Jane Frances de Chantal Parish
website: https://www.stjanesofeastonpa.com/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1817
publication: ['url:http://sponsors.bonventure.net/?page=1817']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1817/2026-10-18.pdf
  seen: 2026-10-18
  quote: 'Sunday: 8:00AM, 10:00AM & 12:00PM'
  note: 'Page 1 of the 18 October 2026 issue (12 pages): "Twenty-Ninth Sunday in Ordinary Time October 18, 2026 /
    St. Jane Frances de Chantal Church / 4049 Hartley Avenue, Easton, Pa 18045", Pastor Rev. Philip Rodgers;
    "Weekend Masses: Saturday: 5:00PM Sunday: 8:00AM, 10:00AM & 12:00PM"; weekdays Monday-Friday 6:30AM & 8:15AM.
    (Page 1 also keeps a stray "August 9, 2026 Nineteenth Sunday" line from a template.)'
- url: https://www.stjanesofeastonpa.com/about/office-and-mass-schedule
  seen: 2026-10-18
  note: 'The parish site''s Office and Mass Schedule page gives the bulletin link https://sponsors.bonventure.net/?page=1817.
    The site answers 403 to curl and to the sandbox''s Chrome (a StackProtect WAF); the page was read through
    WebFetch, so this is a lead, not a quote; the Bon Venture page itself was read with curl.'
---

## Publisher

St. Jane Frances de Chantal, 4049 Hartley Avenue, Easton (Palmer Township area) publishes its
own weekly bulletin through Bon Venture Services (page 1817; `pdfs/1817/<YYYY-MM-DD>.pdf`,
newest 18 October 2026). The 18 October issue names this church alone, with Saturday 5:00 PM
and Sunday 8:00, 10:00 and 12:00, matching the diocesan directory.

## Worship sites

- St. Jane Frances de Chantal, 4049 Hartley Avenue, Easton (`st-jane-frances-de-chantal-easton`).

## Website and bulletin provider

stjanesofeastonpa.com is the parish site (directory, GCatholic, bulletin), but it blocks the
sandbox entirely (HTTP 403 from a StackProtect WAF, in curl and in Chrome). Its schedule page,
read through a fetch service, links the Bon Venture page, so the recipe pins that page over
`http://` and the resolver never needs the parish site. Older issues were once self-hosted at
`stjanesofeastonpa.com/images/pdf/bulletin/bulletinMMDDYY.pdf` (a January 2025 one is
indexed by search engines). Discover Mass `st-jane-frances-de-chantal-easton-pa` lists no
bulletins.

Fetch check (2026-10-19, `fetch_check` on a temporary CSV of the unpromoted rows): resolved, `page-pdfs on http://sponsors.bonventure.net/?page=1817: current`, pdfs/1817/2026-10-18.pdf.

## Not yet confirmed

Nothing beyond the site block above.
