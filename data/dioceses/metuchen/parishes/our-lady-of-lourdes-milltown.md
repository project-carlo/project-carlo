---
name: Our Lady of Lourdes
website: https://www.ololchurchnj.org
bulletin_provider: other
provider_id: page-pdfs https://www.ololchurchnj.org/olol/Bulletins/Current%20Bulletins/
publication: ['url:https://www.ololchurchnj.org/olol/Bulletins/Current%20Bulletins/']
group: ''
evidence:
- url: https://www.ololchurchnj.org/olol/Bulletins/Current%20Bulletins/October%2025%2C%202026.pdf
  seen: 2026-10-30
  quote: Our Lady of Lourdes Church
  note: 'Page 1 of the 25 October 2026 issue (6 pages, text): ''Our Lady of Lourdes Church, Milltown,
    New Jersey'', ''Rev. Edward A. Czarcinski, Pastor'', ''Rev. Michael Crummy, In Residence'', deacons
    Gerling and Holzinger, ''233 North Main Street, Milltown, NJ 08850''; Mass Saturday 5:00 PM, Sunday
    8:00 & 11:30, Monday 7:00 PM with Miraculous Medal Novena, Tuesday through Saturday 7:00 AM. Names
    no other church.'
- url: https://www.ololchurchnj.org/olol/Liturgy/Mass%20Times/
  seen: 2026-10-30
  quote: 'Tuesday through Saturday: 7:00 AM'
  note: 'Mass Times page: Saturday 5:00 PM; Sunday 8:00 AM & 11:30 AM; Monday 7:00 PM; Tuesday through
    Saturday 7:00 AM.'
- url: https://www.ololchurchnj.org/olol/Bulletins/Current%20Bulletins/
  seen: 2026-10-30
  quote: October 25, 2026
  note: 'Current Bulletins page, a self-hosted file list: ''October 25, 2026 (pdf)'' and ''October 18,
    2026 (pdf)'' are PDFs; ''October 11, 2026.crdownload'' and ''October 4, 2026.crdownload'' are unfinished
    browser-download uploads, not readable PDFs.'
bulletin_status: available
---

## Publisher

Our Lady of Lourdes, 233 North Main Street, Milltown, publishes its own weekly bulletin as dated PDFs on its own website (`/olol/Bulletins/Current Bulletins/<Month D, YYYY>.pdf`; the site is not eCatholic and the probes find no provider ids). The 25 October 2026 issue's page 1 (read 2026-10-30) names 'Rev. Edward A. Czarcinski, Pastor' and 'Rev. Michael Crummy, In Residence', matching the finder's pastor, and gives the parish's own address; it names no other church.

## Worship sites

One church, 233 North Main Street (directory:24508, gcatholic:18618). The bulletin's schedule and the Mass Times page list one set of Masses and no second site. The parish was the mother church of Our Lady of Peace, North Brunswick (OLOP's history page, 1944 mission), which now has its own bulletin: the two are separate publishers.

## Website and bulletin provider

Website https://www.ololchurchnj.org, a self-hosted site; recipe `page-pdfs` on the Current Bulletins page. Publication identity is the page URL because the site has no provider id.

## Not yet confirmed

The Current Bulletins page lists the 11 and 4 October issues only as `.crdownload` files, so the PDFs for those weeks aren't readable; a later reader should confirm that the page still lists the newest issue first.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved `page-pdfs https://www.ololchurchnj.org/olol/Bulletins/Current%20Bulletins/` and picked the 25 October 2026 PDF: transport ok, PDF, issue date inferred from the file name, freshness fresh, identity unverified by the tool; I read that issue's page 1 myself (above). No `recipe` line was printed, so the pinned recipe stays as set.
