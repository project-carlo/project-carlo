---
name: St. Marguerite Bourgeoys
website: https://stmarguerite.org/
bulletin_provider: other
provider_id: page-pdfs https://stmarguerite.org/bulletin-archive/ filename=*E-News*.pdf
publication: ['url:https://stmarguerite.org/bulletin-archive/']
group: ''
evidence:
- url: https://stmarguerite.org/wp-content/uploads/2026/11/2026.Nov15-E-News-2.pdf
  seen: 2026-11-12
  quote: 138 Candlewood Lake Rd, Brookfield, CT 06804
  note: 'Page 1 of the 15 November 2026 E-News (6 pages), rendered: masthead ''St. Marguerite Bourgeoys''
    logo, ''E-NEWS'', ''15 November 2026 | 33rd Sunday in Ordinary Time''; pastor Rev. Shawn W. Jordan;
    Mass schedule Saturday 4:30pm Vigil, Sunday 8:30am, 11am, 5pm, Monday-Friday 8:30am; intentions for
    16-22 November. Names no other church.'
- url: https://stmarguerite.org/bulletin-archive/
  seen: 2026-11-12
  quote: Please click on the desired date to view that week’s E-News.
  note: 'WordPress page titled ''E-News'' (menu: Parish Life > E-News) listing weekly issues from January
    5, 2025 to November 15, 2026, newest first; the page also links other PDFs (registration form, year-end
    statements) from its menu.'
revisit: Rerun fetch:check and confirm it still picks the newest E-News (it cannot date the file)
revisit_after: 2027-02-01
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

St. Marguerite Bourgeoys, Brookfield publishes its own weekly newsletter, called *E-News*, which serves as its bulletin: a 6-page PDF with the Mass schedule, the week's Mass intentions and announcements. The 15 November 2026 issue (`https://stmarguerite.org/wp-content/uploads/2026/11/2026.Nov15-E-News-2.pdf`, read 2026-11-12, page 1 rendered because the masthead is an image) has the St. Marguerite Bourgeoys logo, "E-NEWS", "15 November 2026 | 33rd Sunday in Ordinary Time", Rev. Shawn W. Jordan as pastor (the pastor the diocese's directory names) and the footer "138 Candlewood Lake Rd, Brookfield, CT 06804 | stmarguerite.org". No outside publisher.

## Worship sites

- `st-marguerite-bourgeoys-brookfield`: page 1 lists Saturday 4:30pm Vigil, Sunday 8:30am, 11am and 5pm, Monday-Friday 8:30am, with intentions for 16-22 November 2026. The issue names no other church.

The diocese's directory (directory:1346) and GCatholic (22029) list this one church. Page 2 of the issue reports a golf tournament shared with St. Joseph, Brookfield, whose bulletin is separate (`st-joseph-brookfield`, its own masthead and Mass schedule).

## Website and bulletin provider

`stmarguerite.org` is a WordPress site. Its *E-News* page (`/bulletin-archive/`) lists the weekly issues newest first, as PDFs in `wp-content/uploads/<year>/<month>/` named `<YYYY>.<MonD>-E-News[-n].pdf`; the same page links other PDFs from the site menu (registration form, year-end statements), so the recipe filters on `*E-News*.pdf`. Provider `other`, pinned `page-pdfs`; see the fetch check below.

`fetch:check` on 2026-11-12 (headed Chrome) resolved "page-pdfs on https://stmarguerite.org/bulletin-archive/: current" and picked `2026/11/2026.Nov15-E-News-2.pdf`, the 15 November 2026 issue read above. It reported issue date and freshness `unknown`: the date is in the image masthead and the file name's `2026.Nov15` form isn't parsed, so the pick rests on the page's newest-first order. Identity unverified as reported; masthead checked by hand.

## Not yet confirmed

fetch can't date these issues from the file name or text (see above); if the page's order changes, the pick could go stale unnoticed. Recheck the pick at the revisit date.
