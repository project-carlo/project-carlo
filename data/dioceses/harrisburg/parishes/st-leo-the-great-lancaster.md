---
name: Saint Leo the Great Catholic Church
website: https://www.stleos.org/category/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://www.stleos.org/category/bulletins/
publication: ['url:https://www.stleos.org/category/bulletins/']
group: ''
evidence:
- url: https://www.stleos.org/category/bulletins/
  seen: 2026-10-20
  quote: Bulletins October 18, 2026 October 11, 2026 October 4, 2026
  note: The parish's WordPress "Bulletins" category, newest first; "October 18, 2026" links wp-content/uploads/2026/10/October-18-2026.pdf.
- url: https://www.stleos.org/wp-content/uploads/2026/10/October-18-2026.pdf
  seen: 2026-10-19
  note: 'The 18 October 2026 issue (12 pages) has no text layer: every page is an image. Rendered with
    parish-site-access render.py, page 2 reads "SAINT LEO THE GREAT CATHOLIC CHURCH 2427 Marietta Avenue
    Lancaster, PA 17601" and "MASS AND RECONCILIATION SCHEDULE Saturday Vigil 4:30 pm-Church Sunday 7:30
    am, 9:15 am, 11:00 am-Church ... Daily Mass Mon/Sat 9:00 am, Tues/Thurs 6:30 am & 9:00 am, Wed 6:30
    am & 7:00 pm and Friday 6:30 am & 9:00 am"; pastor Rev. Msgr. Peter I. Hahn. recheck cannot find text
    in it.'
- url: https://www.stleos.org/
  seen: 2026-10-20
  quote: Come meet our pastor, Rev. Peter I. Hahn and our Parochial Vicar, Rev. Thomas Meinert.
promoted: 2026-10-20
---

## Publisher

Saint Leo the Great Catholic Church, 2427 Marietta Avenue, Lancaster, posts its own weekly
bulletin as PDFs in the "Bulletins" category of its WordPress site. The 18 October 2026 issue
(posted by 19 October) is image-only; rendered, page 2 has the masthead "Saint Leo the Great
Catholic Church, 2427 Marietta Avenue, Lancaster, PA 17601" and one "Mass and Reconciliation
Schedule": Saturday Vigil 4:30 pm, Sunday 7:30, 9:15 and 11:00 am, all "-Church", and daily
Masses (6:30 am ones in the chapel per the directory). The cover carries a JPPC art credit
only; the PDF is the parish's own.

## Worship sites

One church, `st-leo-the-great-lancaster`. The weekday "Chapel" is part of the parish
buildings on the same campus, not a separate worship site.

## Website and bulletin provider

`other`, website the Bulletins category page, which lists one link per issue named with its
date (October-18-2026.pdf, October-11-2026.pdf, ...). **Image-only bulletin:** the 4, 11 and 18
October issues all have no text layer, so the pipeline must read them as images. The Discover
Mass page "st-leo-the-great-catholic-church-lancaster-pa" exists but lists no bulletins.

Fetch check (2026-10-20, `fetch_check.check_fetch` on a temporary CSV of this region's rows, under xvfb-run with Chrome): "page-pdfs on https://www.stleos.org/category/bulletins/: current", which is the 2026-10-18 issue (October-18-2026.pdf), this week's bulletin, so the printed recipe is pinned as `provider_id`.

## Not yet confirmed

Nothing.
