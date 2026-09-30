---
name: Catholic Community of St. Peter, St. Mary and St. Hedwig (Lowville)
website: https://spsmshcatholic.org
bulletin_provider: ecatholic
provider_id: '19929'
publication: ['ecatholic:19929']
group: Catholic Community of St. Peter and St. Mary and St. Hedwig
evidence:
- url: https://files.ecatholic.com/19929/bulletins/20260809.pdf
  seen: 2026-09-30
  quote: CATHOLIC COMMUNITY OF ST. PETER AND ST. MARY AND ST. HEDWIG
  note: 'The 9 August 2026 issue (2 pages, text layer): the churches box "St. Mary’s 6106 Blue St. Glenfield;
    St. Peter’s 5449 Shady Ave, Lowville; St. Hedwig’s 5432 St Rt 26, Turin", and the weekly schedule
    with codes (SP), (SM), (SH): Sunday 9:00 am (SP) and 11:00 am (SH), Saturday 4:00 pm (SP) and 5:30
    pm (SM).'
- url: https://files.ecatholic.com/19929/bulletins/20260927.pdf
  seen: 2026-09-30
  note: 'Image-only PDF (4 pages, no text layer), drawn with render.py and read by eye, so `recheck` cannot
    quote it. Page 1 is headed "Welcome Home  CATHOLIC COMMUNITY OF ST. PETER AND ST. MARY AND ST. HEDWIG"
    with photos of St. Peter''s (5449 Shady Ave, Lowville), St. Mary''s (6106 Blue Street, Glenfield)
    and St. Hedwig''s (5432 St Rt 26, Turin), pastor Rev. Sony G. Pulickal, and "Parish Weekly Mass Schedule":
    Sunday 27 September 9:00 am (SP) and 11:00 am (SH); weekdays 8:30 am (SP); Saturday 3 October 4:00
    pm (SP) and 5:30 pm (SM); Sunday 4 October 9:00 am (SP) and 11:00 am (SH). Page 2 "St. Mary''s News":
    "St. Mary’s Church will close for the winter following the October 10th Mass" and "Parish Bulletin
    Update": the parish is changing its bulletin publishing system "beginning next week".'
- url: https://spsmshcatholic.org/bulletins
  seen: 2026-09-30
  quote: Catholic Community of
  note: The parish site (eCatholic; behind Cloudflare, its home page challenged all 8 loads and /bulletins
    loaded on the 2nd, read with visit.py). Its Bulletins page embeds ecatholic:19929 and lists weekly
    issues from 4 January to 27 September 2026 as files.ecatholic.com/19929/bulletins/<YYYYMMDD>.pdf,
    each dated by the Sunday. Its header reads "Catholic Community of St. Peter, St. Mary, St. Hedwig"
    and "Parish Office 5457 Shady Ave. | Lowville, NY 13367".
- url: https://www.rcdony.org/directory/parish-bulletins.html
  seen: 2026-09-30
  note: The diocese's bulletin page links spsmshcatholic.org/bulletins for Glenfield, Houseville and Lowville.
revisit: Read the 4 October 2026 and later issues (files.ecatholic.com/19929/bulletins/20261004.pdf or
  wherever the new publishing system puts them) and update website/provider/publication if the bulletin
  moved
revisit_after: 2026-10-15
promoted: 2026-09-30
---

## Publisher

The Catholic Community of St. Peter, St. Mary and St. Hedwig (Lowville, Glenfield and Turin
/ Houseville) publishes one weekly bulletin, hosted as dated PDFs on eCatholic (site id
19929). The 27 September 2026 issue (`files.ecatholic.com/19929/bulletins/20260927.pdf`) is
headed "Catholic Community of St. Peter and St. Mary and St. Hedwig", with one pastor (Rev.
Sony G. Pulickal), one office (5457 Shady Ave, Lowville) and one weekly Mass schedule for the
three churches. The directory groups the same three entries. One bulletin, one row.

## Worship sites

Three, all with Mass now: St. Peter's, Lowville (`st-peter-lowville`), St. Mary's, Glenfield
(`st-mary-glenfield`, **seasonal**: Saturday 5:30 pm, closing for the winter after the 10
October Mass) and St. Hedwig's, Turin, which the directory calls Houseville
(`st-hedwig-turin`). The directory and GCatholic list the same three. The office at 5457
Shady Avenue is the parish office and rectory, not a church.

## Website and bulletin provider

`spsmshcatholic.org` is the directory's and the diocese bulletin page's link, and is an
eCatholic site (footer "powered by eCatholic"; `visit.py` found `ecatholic:19929` on its
Bulletins page). `issues.py ecatholic ecatholic:19929` reads the dated files without a
browser (Cloudflare only guards the site). **The 27 September, 6 September, 12 July and 14 June issues
are image-only PDFs** (no text layer); the 9 August issue has text. The pipeline will need to
read image bulletins for this parish.

## Not yet confirmed

The 27 September issue says the bulletin "is changing! Beginning next week, we will be using a
new bulletin publishing system due to the discontinuation of the software we have used for
many years." The 4 October issue was not yet posted when read (403 on 2026-09-30). The new
system may move the bulletin off eCatholic or change its layout, so `revisit` (15 October
2026) is to read the new issue and update `publication` and `website` if it moved.
