---
name: Basilica of the Sacred Heart of Jesus (Conewago Chapel)
website: https://sacredheartbasilica.com/bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://sacredheartbasilica.com/bulletins/']
group: ''
evidence:
- url: https://sacredheartbasilica.com/wp-content/uploads/2026/10/10.18.26-bulletin.pdf
  seen: 2026-10-19
  quote: Original Conewago Chapel built in 1741
  note: 'The 18 October 2026 issue (4 pages), page 1 masthead: "Basilica of the Sacred Heart of Jesus,
    30 Basilica Drive, Hanover, PA 17331 717-637-2721 www.sacredheartbasilica.com, Twenty Ninth Sunday
    in Ordinary Time October 18, 2026"; "Rev. Dwight Schlaline, Pastor". Recheck cannot reach this server
    (it drops the recheck user agent); curl with its default user agent over https gets the PDF.'
- url: https://sacredheartbasilica.com/bulletins/
  seen: 2026-10-19
  note: 'The WordPress "Bulletins" page lists one PDF per Sunday under wp-content/uploads, newest first:
    10.18.26-bulletin.pdf, 10.11.26-bulletin.pdf, 10.04.26-bulletin.pdf ... (read in a browser with parish-site-access
    visit.py; the homepage answers plain fetchers with 202 and no content).'
---

## Publisher

The Basilica of the Sacred Heart of Jesus (Conewago Chapel), 30 Basilica Drive, Hanover,
publishes its own weekly bulletin as a PDF on its WordPress site. I read the 18 October
2026 issue (4 pages): the page-1 masthead names the Basilica alone, with Rev. Dwight
Schlaline as pastor, and gives "Saturday: 5:30pm, Sunday: 7:30am & 10:00am, First Friday
of the Month: 7:00pm". It looks home-made (no publisher imprint). The diocese lists no
partner parish.

## Worship sites

- Basilica of the Sacred Heart of Jesus, 30 Basilica Drive, Hanover
  (`basilica-sacred-heart-conewago-hanover`). The directory's "Associated Locations" are
  the shared Saint Teresa of Calcutta School campuses; the bulletin's other venues (the
  "barn", the Parish Hall, the picnic grove at 3175 Centennial Road) hold no Mass.

GCatholic has no entry for the Basilica.

## Website and bulletin provider

`website` is the Bulletins page, which lists the dated PDFs newest first. The site runs
SiteGround's anti-bot screen: plain fetchers get a 202 "sgcaptcha" redirect over `http://`,
and the server drops `https://` connections that send the pipeline's Windows Chrome/124
user agent (curl's default or a Linux Chrome user agent get the files).

Fetch check (2026-10-20, `fetch_check` on a temporary CSV of this region's rows): `page-pdfs
on https://sacredheartbasilica.com/bulletins/: current`, picking
`http://sacredheartbasilica.com/wp-content/uploads/2026/10/10.18.26-bulletin.pdf`, the right
issue, but the download was `not_pdf` (222 bytes: the sgcaptcha page, because the page
links the PDFs over `http://`). Recipe `page-pdfs` pinned, since the pick is right. The
downloader now retries over https when http answers with something other than a PDF (same
PR), and the re-run on 2026-10-20 downloaded the 18 October issue (3,013,270 bytes, `ok`).

## Not yet confirmed

Nothing open.
