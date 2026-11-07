---
name: St. Francis de Sales ? current bulletin connector
parish: st-francis-de-sales-new-york-city
city: New York City
state: NY
revisit: On October 8, 2026 the production resolver against the actual archive HTML returned https://stfrancis96.org/s/_Bulletin-2-August-2026.pdf
  under page-pdfs (first-listed, dated August 2), not the verified October 4 issue. dated-post and linked-issue-page
  both returned NoBulletin. Current parish-linked Elvanto /file/<UUID>/ addresses have no .pdf suffix
  and are not among document URL forms accepted by the current collector. A recipe pinned to the October
  file alone would not follow future issues. A supported Elvanto collector or readable current PDF mirror
  is required, followed by a successful current-issue resolver/download check.
revisit_after: '2026-10-15'
evidence:
- url: https://tithely-5e3b3d31cd9bd-316835.elvanto.net/file/e2cb9771-e08a-49bc-a829-d5c29c4d9efe/
  seen: '2026-10-08'
  quote: Francis de Sales
  note: October 4, 2026 issue page 1 masthead Saint Francis de Sales Catholic Church and issue date.
- url: https://tithely-5e3b3d31cd9bd-316835.elvanto.net/file/e2cb9771-e08a-49bc-a829-d5c29c4d9efe/
  seen: '2026-10-08'
  quote: 135 East 96th Street
  note: Page 18 church address.
- url: https://tithely-5e3b3d31cd9bd-316835.elvanto.net/file/e2cb9771-e08a-49bc-a829-d5c29c4d9efe/
  seen: '2026-10-08'
  quote: 9:00am, 11:00am,
  note: Page 2 Sunday schedule adds 12:30 PM Spanish; weekday 8:30 AM Monday/Tuesday/Thursday/Friday.
---

## Actual current publication

The October 4, 2026 bulletin was read October 8 at the PDF URL in the evidence below. Masthead, public Mass and address quotes retain their exact page references in that evidence. The current archive is https://stfrancis96.org/bulletin.

## Production check and exact blocker

On October 8, 2026 the production resolver against the actual archive HTML returned https://stfrancis96.org/s/_Bulletin-2-August-2026.pdf under page-pdfs (first-listed, dated August 2), not the verified October 4 issue. dated-post and linked-issue-page both returned NoBulletin. Current parish-linked Elvanto /file/<UUID>/ addresses have no .pdf suffix and are not among document URL forms accepted by the current collector. A recipe pinned to the October file alone would not follow future issues. A supported Elvanto collector or readable current PDF mirror is required, followed by a successful current-issue resolver/download check.

The corresponding parish is on no_bulletin ingestion hold. No closure or absence of actual publication is inferred. This connector question is independent of the settled church identity.
