---
name: Corpus Christi
website: https://corpuschristi-mineola.net/
bulletin_provider: other
provider_id: page-pdfs https://corpuschristi-mineola.net/archived-bulletins/ filename=CC_*.pdf
publication: ['url:https://corpuschristi-mineola.net/archived-bulletins/#corpus-christi']
group: ''
evidence:
- url: https://corpuschristi-mineola.net/wp-content/uploads/CC_11-08-26.pdf
  seen: 2026-11-13
  quote: Corpus Christi Church
  note: 'Issue for November 8, 2026 (3 pages). Every page header reads ''32nd Sunday in Ordinary Time,
    Corpus Christi Church, November 8, 2026''. Mass intentions November 9-15: weekdays 7:30 AM and 12:30
    PM, Monday 7:30 PM Spanish Mass; Saturday 5:00 PM; Sunday 7:00 AM, 8:30 AM Portuguese Mass, 10:00
    AM, 11:30 AM, 5:00 PM, 7:00 PM. No other church is named.'
- url: https://corpuschristi-mineola.net/archived-bulletins/
  seen: 2026-11-13
  note: WordPress Archived Bulletins page (read with parish-site-access visit.py) links 288 issues named
    CC_<m>-<dd>-<yy>.pdf from 2021 on, the 2026 issues first and newest first (CC_11-08-26.pdf, CC_11-01-26.pdf,
    CC_10-25-26.pdf ...).
- url: https://corpuschristi-mineola.net/
  seen: 2026-11-13
  quote: 155 Garfield Avenue Mineola
  note: Home page title 'Corpus Christi Parish – 155 Garfield Avenue Mineola, New York, 11501-2583'; it
    links the current issue CC_11-08-26.pdf.
promoted: 2026-11-13
bulletin_status: available
---

## Publisher

Corpus Christi, Mineola publishes its own short weekly bulletin on its WordPress site. The newest issue on 2026-11-13, `https://corpuschristi-mineola.net/wp-content/uploads/CC_11-08-26.pdf` (3 pages, page 2 an image), has the running header "32nd Sunday in Ordinary Time, Corpus Christi Church, November 8, 2026". Its Mass intentions for November 9-15 list weekdays 7:30 AM and 12:30 PM, a Monday 7:30 PM Spanish Mass, Saturday 5:00 PM, and Sunday 7:00 AM, 8:30 AM (Portuguese), 10:00 AM, 11:30 AM, 5:00 PM and 7:00 PM, with the celebrants for each weekend Mass. It notes "only one Mass on Thanksgiving Day at 9:00 AM, for all three communities" (the English, Portuguese and Spanish-speaking communities, by the schedule; inferred, the bulletin does not spell them out).

## Worship sites

One: the church at 155 Garfield Avenue (`corpus-christi-mineola-church`). The bulletin names no other place of worship. The diocesan locator (directory:5), GCatholic (16887) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

The site corpuschristi-mineola.net (http www. redirects to it) links the current issue from its home page and keeps every issue since 2021 on `/archived-bulletins/`, named `CC_<m>-<dd>-<yy>.pdf` with no month words. The provider is `other` with `page-pdfs` on the archive page and the `CC_*.pdf` glob, so a flyer elsewhere on the page can't be picked.

`fetch:check` (2026-11-13) with this recipe picked `CC_11-08-26.pdf` (url_date 2026-11-08), the newest issue. It reported the issue date as a conflict only because the text carries the Mass-intention dates November 9-15; the header reads November 8, 2026.

## Not yet confirmed

The bulletin text carries no street address; the address comes from the site's title and the diocesan and GCatholic listings.
