---
name: Ss. Philip and James
website: https://www.sspj.org/copy-of-bulletins-1
bulletin_provider: unsupported
provider_id: page-pdfs https://www.sspj.org/copy-of-bulletins-1
publication: ['url:https://www.sspj.org/copy-of-bulletins-1']
group: ''
evidence:
- url: https://www.sspj.org/_files/ugd/a9ac9d_3a062befebc14d119c888d281fbdf01c.pdf
  seen: 2026-11-13
  quote: 1 Carow Place, St. James, NY 11780
  note: 'Issue headed ''November 15, 2026 Weekly Bulletin www.sspj.org'', ''Thirty-third Sunday in Ordinary
    Time'' (18 pages, Creator Adobe Express, self-made). Page 1 MASS TIMES: Weekday 7:30 AM, 9:15 AM;
    Saturday 9:15 AM, 5 PM (Vigil); Sunday 8 AM, 10 AM, 12 NOON; no other place of Mass. Page 2 parish
    directory: Pastor Rev. Sean Magaldi. No printer named.'
- url: https://www.sspj.org/copy-of-bulletins-1
  seen: 2026-11-13
  note: 'Wix ''Bulletins'' page (read with visit.py) links 15 hashed /_files/ugd/a9ac9d_*.pdf issues with
    no link text and not in date order: the first two are 1 and 8 November 2026, the third 15 November,
    then 4 and 11 October (dates read from each PDF''s page 1).'
research:
- method: fetch:check page-pdfs on the Wix bulletins page; visit.py on the home page for a direct current-issue
    link
  url: https://www.sspj.org/copy-of-bulletins-1
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Set provider other once fetch can date undated PDFs by their page-1 text or the page lists
    issues newest first; rerun fetch:check
  retry_when: A collector dates issues from content, or the parish reorders or relabels its list
bulletin_status: available
fetch_gap:
  kind: first-pdf-not-current
  seen: 2026-11-13
  url: https://www.sspj.org/copy-of-bulletins-1
  note: 'The Wix Bulletins page lists 15 hash-named /_files/ugd/a9ac9d_*.pdf issues with no link text
    and out of date order (1 Nov, 8 Nov, 15 Nov, 4 Oct, 11 Oct 2026 ...). fetch:check 2026-11-13 (page-pdfs
    on the page: first-listed) picked a9ac9d_819225316b57421d907e420e8741d078.pdf, the 1 November issue;
    the current one is 15 November (a9ac9d_3a062befebc14d119c888d281fbdf01c.pdf). No filename glob can
    select by date; the home page links only this page.'
---

## Publisher

Ss. Philip and James, St. James, publishes its own weekly bulletin (Adobe Express, no printer named). The 15 November 2026 issue (`https://www.sspj.org/_files/ugd/a9ac9d_3a062befebc14d119c888d281fbdf01c.pdf`, read 2026-11-13) is headed "November 15, 2026 Weekly Bulletin www.sspj.org" with "1 Carow Place, St. James, NY 11780" and the pastor Rev. Sean Magaldi.

## Worship sites

One: the church at 1 Carow Place (`ss-philip-and-james-st-james-church`). The issue's MASS TIMES (Weekday 7:30 AM, 9:15 AM; Saturday 9:15 AM, 5 PM Vigil; Sunday 8 AM, 10 AM, 12 NOON) name no other place, and the diocesan locator, GCatholic and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

The Wix page `https://www.sspj.org/copy-of-bulletins-1` (the home page's only bulletin link) lists the issues as hashed `/_files/ugd/` PDFs with no link text, not in date order (1 Nov, 8 Nov, 15 Nov, 4 Oct, 11 Oct ... on 2026-11-13). fetch:check (page-pdfs on that page) took the first-listed file, the 1 November issue, so the row is `unsupported` with fetch_gap `first-pdf-not-current` (as Newark's Blessed Sacrament–St. Charles Borromeo); the recipe stays in `provider_id`.

## Not yet confirmed

Nothing about the parish. The row goes live once a collector can pick the newest issue from this list; see research.
