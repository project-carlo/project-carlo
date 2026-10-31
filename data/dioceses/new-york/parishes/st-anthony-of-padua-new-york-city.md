---
name: St. Anthony of Padua
website: https://www.stanthony.nyc/
bulletin_provider: no_bulletin
provider_id: ''
publication:
- url:https://www.stanthony.nyc/bulletins/
revisit: Follow the current DearFlip PDF source or obtain a corrected conventional PDF anchor. Test automatic current-issue selection and download before enabling fetch; do not pin the October-only PDF or select the stale August anchor.
revisit_after: '2026-10-17'
evidence:
- url: https://www.stanthony.nyc/wp-content/uploads/2026/10/october4.pdf
  seen: '2026-10-08'
  quote: OCTOBER 4, 2026
  note: Actual two-page image-only PDF; both spreads visually read October 8, page 1 issue date, not URL
    inference.
- url: https://www.stanthony.nyc/wp-content/uploads/2026/10/october4.pdf
  seen: '2026-10-08'
  quote: ST. ANTHONY OF PADUA CHURCH
  note: Page 1 front-cover masthead, visually transcribed.
- url: https://www.stanthony.nyc/wp-content/uploads/2026/10/october4.pdf
  seen: '2026-10-08'
  quote: 'Sunday: 9:00 and 11:00 am'
  note: Page 1 public Sunday schedule, followed by 1 PM Spanish; Saturday 5 PM and Tuesday-Friday 8 AM/12:10
    PM.
- url: https://www.stanthony.nyc/wp-content/uploads/2026/10/october4.pdf
  seen: '2026-10-08'
  quote: 155 SULLIVAN STREET
  note: Page 1 distinguishes church 155 from parish office 154 Sullivan Street.
- url: https://www.stanthony.nyc/wp-content/uploads/2026/10/october4.pdf
  seen: '2026-10-08'
  quote: NO MASSES ON MONDAYS
  note: Page 2 current intentions, October 3-10, confirm the page 1 weekday schedule.
---

## Actual current publisher

The actual two-page image-only bulletin at https://www.stanthony.nyc/wp-content/uploads/2026/10/october4.pdf was visually read in both spreads October 8, 2026. Page 1 names St. Anthony of Padua Church and October 4, 2026. Page 2 prints October 3-10 intentions and no Masses on Mondays. The parish archive https://www.stanthony.nyc/bulletins/ embeds this October file in escaped DearFlip script markup, although its conventional Latest Bulletin anchor still points to August 16 and older download anchors point to July/June files. The October issue resolves the former publication-identity question; the visible old anchor is not the actual newest issue.

## Public worship and address disagreement

Page 1 prints Saturday 5 PM; Sunday 9 AM/11 AM and 1 PM Spanish; Tuesday-Friday 8 AM/12:10 PM. It explicitly distinguishes church 155 Sullivan Street from office 154. The primary homepage calls its location 154 and its menu lists Spanish 1:30 PM, whereas the current PDF and homepage Spanish invitation say 1 PM. Preserve these source disagreements: current issue controls the dated schedule and church/office distinction, verification flags remain false.

## Connector hold

On October 8 the supported page-pdfs recipe at https://www.stanthony.nyc/bulletins/ selected August-16-Bulletin.pdf (first-listed, August 16), not the actual October file, because the stale ordinary PDF anchors mask the DearFlip script source. linked-issue-page returned NoBulletin. Local urllib additionally failed TLS trust, while the current October PDF downloaded under verified-TLS HTTP with httpx; no expired server certificate is asserted. The independent collector stale-pick failure, not local client trust, is why this publisher has a no_bulletin ingestion hold. A collector that follows the current DearFlip source, or corrected current conventional PDF link, is required; a static October-only file recipe would not follow future publication.
