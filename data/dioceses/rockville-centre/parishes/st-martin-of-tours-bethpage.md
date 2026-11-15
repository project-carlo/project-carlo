---
name: Parish of Saint Martin of Tours
website: https://www.smtbethpage.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.smtbethpage.org/news/bulletin']
group: ''
evidence:
- url: https://www.smtbethpage.org/news/bulletin/756-november-8-2026/file
  seen: 2026-11-12
  quote: 40 Seaman Avenue, Bethpage, New York 11714
  note: 'Page 1 masthead of the 8 November 2026 issue, "Parish of Saint Martin of Tours" alone (made in
    Microsoft Publisher by the rectory; downloaded through Chrome with tools/browser_get.py, since probe
    get answers 403). Mass Times: Monday-Friday 9 a.m.; Saturday 9 a.m. & 5 p.m.; Sunday 7:30 a.m., 10
    a.m., 12 Noon, 5:30 p.m.'
- url: https://www.smtbethpage.org/news/bulletin
  seen: 2026-11-12
  note: 'Solutio (Joomla) bulletin list read with visit.py (probe url failed TLS on the bare domain):
    756-november-8-2026, 755-november-1-2026, 754-october-25-2026; each issue page redirects to .../file,
    the PDF.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-12
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-12 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../756-november-8-2026/file" (the post redirects to the PDF, which
    answers 403 outside a browser). Chrome downloads it.'
  url: https://www.smtbethpage.org/news/bulletin/756-november-8-2026/file
---

## Publisher

St. Martin of Tours, 40 Seaman Avenue, Bethpage publishes its own weekly bulletin, made by the rectory in Microsoft Publisher (no printer's id or LPi/John Patrick marks). The 8 November 2026 issue (`https://www.smtbethpage.org/news/bulletin/756-november-8-2026/file`, read 2026-11-12) has a page-1 masthead for "Parish of Saint Martin of Tours" alone and its Mass Times: Monday-Friday 9 a.m.; Saturday 9 a.m. and 5 p.m.; Sunday 7:30 a.m., 10 a.m., 12 Noon and 5:30 p.m. Page 2 lists Mass intentions for 9-15 November at those times.

The diocese's Mass-times page (read 2026-11-12) still lists a Monday-Thursday 6:30 AM Mass "until the end of this year"; the 8 November bulletin lists none, so it has already ended or is not advertised. Either way the row is the same.

## Worship sites

One: the church at 40 Seaman Avenue (`st-martin-of-tours-bethpage-church`). The diocesan locator (directory:55), GCatholic (16813) and the Mass-times page list only this building. The bulletin also names the parish school's cafeteria (a reception venue) and a Knights of Columbus house at 517 Central Ave., neither with Mass.

## Website and bulletin provider

smtbethpage.org (the locator's link) is a Solutio (Joomla) site. `probe url` failed on the bare domain (certificate hostname mismatch); `www.smtbethpage.org` loads in Chrome. Its issue PDFs at `/news/bulletin/<n>-<month>-<d>-<yyyy>/file` answer 403 to `probe get`; Chrome downloads them. No printer listing exists: the issue is a parish-made Publisher PDF. Following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
