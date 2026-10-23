---
name: St. Florian Parish, United
website: https://www.saintflorian.org
bulletin_provider: other
provider_id: dated-post https://www.saintflorian.org/category/bulletin/ filename=[0-9]*.pdf
publication: ['url:https://www.saintflorian.org/category/bulletin/']
group: ''
evidence:
- url: https://www.saintflorian.org/wp-content/uploads/2026/10/20261018.pdf
  seen: 2026-10-22
  quote: Pastor/Trust Administrator
  note: 'Page 1 of the 18 Oct 2026 issue (5 pages; linked from the post https://www.saintflorian.org/the-twenty-ninth-sunday-in-ordinary-time-october-18th-2026/):
    "REV. JOHN A. SEDLAK Pastor/Trust Administrator"; Mass Schedule "Weekday & Sat. Morning: 8:00 am",
    "Saturday Vigil: 5:00 pm", "Sunday: 9:00 & 11:00 am"; Mailing Address "PO Box 187 4263 Route 981 United
    PA 15689"; Website "www.saintflorian.org". One parish, one schedule; no other church or chapel named
    (grep Chapel, Stanislaus, Trauger: none).'
- url: https://www.saintflorian.org/category/bulletin/
  seen: 2026-10-22
  note: 'Diocese-template WordPress category page (403 to probe url and curl; read in headed Chrome with
    parish-site-access visit.py), one post per issue, newest first: October 18th, October 11th, October
    4th, September 27th 2026 ... back to May 31st 2026 on page 1, 20 pages in all. Each post embeds one
    PDF named YYYYMMDD.pdf (20261018.pdf).'
- url: https://www.dioceseofgreensburg.org/parish/?LocationID=291
  seen: 2026-10-22
  note: 'Directory: St. Florian Parish, 4263 Route 981, Mount Pleasant 15666; mailing "P.O. Box 187, United,
    PA 15689"; pastor Father John A. Sedlak (no other parish); "Saturday: 5:00 p.m.; Sunday: 9:00 a.m.,
    11:00 a.m."; no Partner Parishes listed.'
promoted: 2026-10-23
---

## Publisher

St. Florian Parish, United publishes its own weekly bulletin and posts it on its diocese-template WordPress site.
The 18 October 2026 issue (read 2026-10-22, `20261018.pdf`, 5 pages) has Rev. John A. Sedlak as "Pastor/Trust
Administrator", one Mass schedule (weekday and Saturday morning 8:00 am, Saturday Vigil 5:00 pm, Sunday 9:00 and
11:00 am) and the mailing address "PO Box 187, 4263 Route 981, United PA 15689". Fr. Sedlak serves no other parish
in the directory, which lists no partners for St. Florian.

## Worship sites

One: St. Florian church on Route 981, United, the only place in the bulletin's schedule. The Former Churches
Directory lists St. Stanislaus, Calumet (Mammoth) and Forty Martyrs, Trauger (both closed 2008) with records at St.
Florian; no roster lists either as a church and the bulletin names neither. GCatholic's St. Mary Holy Protection,
4480 Route 981, Mount Pleasant (17296) is a Byzantine Catholic church, not part of this parish.

## Website and bulletin provider

`website` is the parish's own site. No ParishesOnline organization for St. Florian turned up in the LPi geo-search
around United (6 miles, 2026-10-22), and the site's bulletin pages embed no publisher id (visit.py: "bulletin PDFs but
no publisher id: looks self-hosted"). Provider `other` with the recipe `dated-post
https://www.saintflorian.org/category/bulletin/ filename=[0-9]*.pdf`: the category page lists one post per issue,
newest first, and each post embeds the issue PDF (`YYYYMMDD.pdf`); the filter keeps the sidebar's
`Virtual-Mandated-Reporter-Training.pdf` and the diocese's footer privacy-policy PDF out. `fetch:check` (2026-10-22,
a Thursday) picked `wp-content/uploads/2026/10/20261018.pdf`, "dated-post ... current", the latest issue posted; the
25 October issue was not up yet.

## Not yet confirmed

The site posts each issue around its Sunday, so a mid-week fetch gets the previous Sunday's issue. If the parish
stops naming files `YYYYMMDD.pdf`, the filename filter will make the fetch fail and needs updating.
