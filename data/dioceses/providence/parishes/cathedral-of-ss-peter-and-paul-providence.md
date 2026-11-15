---
name: Cathedral of SS. Peter and Paul, Providence
website: https://www.providencecathedral.org/bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.providencecathedral.org/bulletin
publication: ['url:https://www.providencecathedral.org/bulletin']
group: ''
evidence:
- url: https://www.providencecathedral.org/_files/ugd/a29c27_469bf0a49bbc49b49d65964a7b6bb90b.pdf
  seen: 2026-11-15
  quote: NOVEMBER 15, 2026
  note: '3-page issue with a text layer, linked from the Wix /bulletin page. Page 1 masthead: ''CATHEDRAL
    OF SAINTS PETER AND PAUL ... 30 Fenner Street Providence, Rhode Island 02903''; WEEKEND MASSES Saturday
    5PM, Sunday 10AM, 1PM, 6PM; WEEKDAY MASSES Monday - Friday 12PM. Rector Msgr. Raymond B. Bastia.'
- url: https://www.providencecathedral.org/_files/ugd/a29c27_cf4629e04fe543a69244f9c387dbed1b.pdf
  seen: 2026-11-15
  quote: NOVEMBER 8, 2026
  note: The previous issue, the second PDF linked from the /bulletin page; same masthead and schedule.
revisit: Rerun fetch:check after 22 November 2026 and confirm page-pdfs still picks the first-listed (newest)
  issue.
revisit_after: 2026-11-24
bulletin_status: available
---

## Publisher

The Cathedral posts its own 3-page bulletin as PDFs on its Wix site (https://www.providencecathedral.org/bulletin). The 15 November 2026 issue (https://www.providencecathedral.org/_files/ugd/a29c27_469bf0a49bbc49b49d65964a7b6bb90b.pdf, text layer, read with `probe pdf`) has the masthead "CATHEDRAL OF SAINTS PETER AND PAUL ... NOVEMBER 15, 2026 ... 30 Fenner Street Providence, Rhode Island 02903", Rev. Msgr. Raymond B. Bastia, Rector. The 8 November issue is also linked.

## Worship sites

One church, the Cathedral at 30 Fenner Street: weekend Masses Saturday 5PM, Sunday 10AM, 1PM, 6PM; weekday Masses Monday-Friday 12PM (15 November page 1). The page-2 intentions list only these times. The finder popup mentions First Friday adoration in the Bishop's Chapel; no Mass is scheduled there, so it is not a separate worship site.

## Website and bulletin provider

`other`, recipe `page-pdfs https://www.providencecathedral.org/bulletin`. The page links the current and previous issue as hashed Wix files (`_files/ugd/a29c27_<hash>.pdf`). `fetch:check` on 2026-11-15 ("page-pdfs on https://www.providencecathedral.org/bulletin: first-listed") downloaded the 15 November 2026 issue (a29c27_469bf0a4...pdf); it reports freshness `unknown` because the hashed names carry no date, but page 1 reads "NOVEMBER 15, 2026". The finder's homepage is http://www.providencecathedral.org; GCatholic gives http://www.cathedralprovidence.org.

## Not yet confirmed

Whether the newest issue stays first-listed when the next one is posted: rerun `fetch:check` after 22 November 2026.
