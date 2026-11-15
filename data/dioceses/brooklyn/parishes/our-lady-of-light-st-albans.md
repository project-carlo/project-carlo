---
name: Our Lady of Light (St. Albans)
website: https://ourladyoflightqueens.org/
bulletin_provider: other
provider_id: page-pdfs https://ourladyoflightqueens.org/bulletins
publication: []
group: Deanery Q9 (Queens East)
evidence:
- url: https://ourladyoflightqueens.org/system/resources/W1siZiIsIjIwMjYvMTEvMDEvOHl4bXNtNzIwcl9PdXJfTGFkeV9vZl9MaWdodF9CdWxsZXRpbl82Xy5wZGYiXV0/Our%20Lady%20of%20Light%20Bulletin%20%286%29.pdf
  seen: 2026-11-06
  quote: Solemnity of  All Saints Day Sunday, November 1, 2026
  note: '1 November 2026 issue, 9 pages (page 7 an image). Page 1 masthead ''Our Lady of Light Parish''
    lists two churches with their own Mass schedules: St. Pascal Baylon (113th Ave and 199th St.; Sunday
    10am and Spanish Mass 12:30pm, Monday to Saturday 9am) and St. Catherine of Sienna (Riverton St. and
    Baisley Blvd.; Sunday 8am, Monday to Saturday 8am). Office addresses 118-22 Riverton Street and 112-43
    198th Street. Staff: Rev. Erick Balderas Vega M.Afr, Parochial Vicar/Administrator.'
- url: https://ourladyoflightqueens.org/system/resources/W1siZiIsIjIwMjYvMTEvMDEvOHl4bXNtNzIwcl9PdXJfTGFkeV9vZl9MaWdodF9CdWxsZXRpbl82Xy5wZGYiXV0/Our%20Lady%20of%20Light%20Bulletin%20%286%29.pdf
  seen: 2026-11-06
  note: 'Grep of all pages for an LPi footer (03-/04-NNNN), ''BULLETIN INC'' and ''lpi'' found nothing:
    the bulletin is produced by the parish itself (earlier issues are office scans named SKM_C361i...pdf).'
- url: https://ourladyoflightqueens.org/bulletins
  seen: 2026-11-06
  note: 'Tilma bulletins page, server-rendered, newest first, cards ''<Month DD, YYYY>'' linking /system/resources/<token>/
    PDFs on the parish domain: November 01, 2026; October 18, 2026; October 11, 2026; September 27, 2026;
    September 20, 2026; ... (no card for 25 October).'
promoted: 2026-11-12
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://ourladyoflightqueens.org/bulletins
  url: https://ourladyoflightqueens.org/bulletins
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check after 8 November and confirm it picks that issue (the parish skipped
    25 October)
  revisit_after: 2026-11-10
bulletin_status: available
---

## Publisher

Our Lady of Light Parish, St. Albans (the merged parish of St. Catherine of Siena and St. Pascal Baylon) publishes one weekly bulletin of its own making and posts it on its Tilma site. The 1 November 2026 issue (read 2026-11-06, 9 pages) has the page 1 masthead "Our Lady of Light Parish" with both former parishes' offices (St. Catherine of Sienna, 118-22 Riverton Street; St. Pascal Baylon, 112-43 198th Street) and Rev. Erick Balderas Vega M.Afr, Parochial Vicar/Administrator. No LPi footer or Church Bulletin Inc. footer appears in any page, and earlier issues are office scans (`SKM_C361i...pdf`), so there is no publisher container.

## Worship sites

Two, both with a Mass schedule on page 1 of the 1 November 2026 issue (page 1 rendered to confirm which schedule sits under which church drawing):

- St. Pascal Baylon, "113thAve and199thSt.": Sunday 10am and Spanish Mass 12:30pm, Monday to Saturday 9am.
- St. Catherine of Sienna, "RivertonSt.and Baisley Blvd.": Sunday 8am, Monday to Saturday 8am.

The current bulletin covers both churches, so under the settled rule for merged parishes they are one row. GCatholic lists both (16636, 16637) under "Our Lady of Light Parish"; the directory and deanery list give the parish at 118-22 Riverton Street (St. Catherine), and Mass finder 381 names St. Catherine of Siena. No other chapel is named in the issue.

## Website and bulletin provider

`other`, recipe `page-pdfs https://ourladyoflightqueens.org/bulletins`. The Tilma page uses the '<Month DD, YYYY>' card theme with PDFs at `ourladyoflightqueens.org/system/resources/<token>/`. Posting is irregular (no card for 25 October 2026). Page 7 of the 1 November issue is an image; pages 1-6 and 8-9 have text.

## Not yet confirmed

Nothing structural. The parish skipped 25 October 2026; if the 8 November issue isn't posted the fetch will keep the 1 November one.
