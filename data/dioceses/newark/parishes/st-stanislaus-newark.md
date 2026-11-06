---
name: St. Stanislaus, Newark
website: https://www.ststanislausnewark.com/
bulletin_provider: other
provider_id: page-pdfs https://www.ststanislausnewark.com/
publication: ['url:https://www.ststanislausnewark.com/']
group: ''
evidence:
- url: https://www.ststanislausnewark.com/_files/ugd/a1e20e_f15583c353854a12bbd93e6cdcd9d0d1.pdf
  seen: 2026-11-04
  quote: Rev. Tomasz Koszalka, Pastor
  note: Four-page bilingual (Polish/English) self-made bulletin with a text layer, no printer's footer.
    The page-1 masthead names 'St. Stanislaus Bishop & Martyr Roman Catholic Church', October 11, 2026,
    146 Irvine Turner Boulevard, Newark, NJ 07103, alone. Page 4 'INTENCJE MSZALNE' lists Sunday 9:00
    AM, 10:30 AM and 12:00 PM, Monday and Friday 7:00 PM, Tuesday to Thursday and Saturday 7:30 AM.
- url: https://www.ststanislausnewark.com/
  seen: 2026-11-04
  quote: Download Bulletin
  note: 'Wix homepage. Its one PDF link (''Download Bulletin'') is the 11 October 2026 issue above. The
    schedule block gives ''Sunday: 9:00am (PL/EN)'' among the Mass times.'
- url: http://web.archive.org/cdx/search/cdx?url=ststanislausnewark.com/_files/ugd/&matchType=prefix&fl=timestamp,original,statuscode
  seen: 2026-11-04
  note: Wayback has captured 40-odd different _files/ugd PDFs from the site between July 2024 and May
    2026 (e.g. 20260114, 20260209, 20260426, 20260508). The homepage link is replaced with a new upload
    for each issue, at irregular intervals.
revisit: 'Rerun fetch:check: on 2026-11-04 the homepage still linked the 11 October 2026 issue (24 days
  old, freshness stale). If it stays weeks behind, note the posting rhythm.'
revisit_after: 2026-11-16
research:
- method: fetch:check with page-pdfs on the homepage (first-listed)
  url: https://www.ststanislausnewark.com/
  checked: '2026-11-04'
  outcome: found
  next_action: Rerun fetch:check; if the homepage still links the 11 October issue, consider whether the
    parish posts only occasionally
  retry_when: After the next Sunday the parish posts an issue
  revisit_after: 2026-11-16
bulletin_status: available
---

## Publisher

The parish makes its own bulletin: a four-page Polish/English PDF with a text layer and no printer's footer. The 11 October 2026 issue (the one linked as 'Download Bulletin' on the homepage, read 4 November 2026) has a page-1 masthead that names 'St. Stanislaus Bishop & Martyr Roman Catholic Church', 146 Irvine Turner Boulevard, Newark, alone, with Rev. Tomasz Koszalka as pastor. Its Mass-intention page lists Sunday 9:00, 10:30 and 12:00 and weekday Masses, all at St. Stanislaus.

## Worship sites

`st-stanislaus-newark`, 146 Irvine Turner Boulevard. GCatholic's Queen of Angels (18496, 44 Irvine Turner Blvd), which the batch plan placed next to it, does not appear in the bulletin. It closed in 2012 and was demolished in 2016 (`excluded/queen-of-angels-newark`).

## Website and bulletin provider

A Wix site that links one bulletin PDF at a time from the homepage, as an undated `_files/ugd/` upload. Provider `other`, `page-pdfs` on the homepage (`first-listed`). fetch:check on 2026-11-04 picked the 11 October 2026 issue (transport ok, PDF, date read from the text, freshness stale at 24 days). That is the parish's newest issue, so the recipe is right, but the parish is behind in posting. Wayback's captures show the link replaced by a new upload regularly through 2024-2026.

## Not yet confirmed

How often the parish posts: the latest issue was 24 days old on 4 November 2026. See `revisit`.
