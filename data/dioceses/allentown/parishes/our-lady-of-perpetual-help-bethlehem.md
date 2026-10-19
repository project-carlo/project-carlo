---
name: Our Lady of Perpetual Help Parish
website: https://my-olph.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1588
publication: ['url:http://sponsors.bonventure.net/?page=1588']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1588/2026-10-18.pdf
  seen: 2026-10-18
  quote: 'Sunday: 7:30, 9:30 and 11:30'
  note: 'Page 1 of the 18 October 2026 issue (12 pages): "Our Lady of Perpetual Help Parish Center, 3219
    Santee Road, Bethlehem, PA 18020", Pastor Rev. Martin F. Kern; "LITURGICAL SCHEDULE: Weekend Masses:
    Saturday: 5:00 PM Sunday: 7:30, 9:30 and 11:30"; weekdays Monday-Thursday 6:45 & 8:00 AM. Page 2 header
    "Web Site - www.my-olph.org".'
- url: https://my-olph.org/
  seen: 2026-10-18
  note: 'The parish''s eCatholic site (site id 1414; Cloudflare, read in a browser with parish-site-access
    visit.py) links "Weekly Bulletin" and "Parish Bulletin" to sponsors.bonventure.net/?page=1588. Its
    eCatholic bulletin feed is unused: files.ecatholic.com/1414/bulletins/ answers 403 for the last four
    Sundays.'
promoted: 2026-10-19
---

## Publisher

Our Lady of Perpetual Help, 3219 Santee Road, Bethlehem (Hanover Township) publishes its own
weekly bulletin through Bon Venture Services (page 1588, one PDF per Sunday at
`pdfs/1588/<YYYY-MM-DD>.pdf`, newest 18 October 2026). The 18 October issue's page 1 names
this parish alone, with Saturday 5:00 PM and Sunday 7:30, 9:30 and 11:30 Masses, matching the
diocesan directory. The diocese lists no partner parish.

## Worship sites

- Our Lady of Perpetual Help, 3219 Santee Road, Bethlehem (`our-lady-of-perpetual-help-bethlehem`).

## Website and bulletin provider

my-olph.org is the parish site (directory, GCatholic and the bulletin agree); it is an
eCatholic site behind Cloudflare, but it posts its bulletin on Bon Venture, not through
eCatholic, so the provider is `other` and the recipe pins the Bon Venture page over `http://`
(Bon Venture's https chain is broken server-side, as recorded for Scranton). The ParishesOnline
org `our-lady-of-perpetual-help-church-18020` and the Discover Mass page
`our-lady-of-perpetual-help-bethlehem-pa` exist with no bulletins; not recorded.

Fetch check (2026-10-19, `fetch_check` on a temporary CSV of the unpromoted rows): resolved, `page-pdfs on http://sponsors.bonventure.net/?page=1588: current`, pdfs/1588/2026-10-18.pdf.

## Not yet confirmed

Nothing.
