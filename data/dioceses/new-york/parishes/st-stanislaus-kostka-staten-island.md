---
name: St. Stanislaus Kostka Parish
website: https://stanislawkostkasi.org/
bulletin_provider: other
provider_id: page-pdfs https://stanislawkostkasi.org/bulletin
publication: ['url:https://stanislawkostkasi.org/bulletin']
group: St. Stanislaus Kostka Parish
revisit: 'The live HTTP resolver and production PDF download succeed, but the normally weekly archive stops September 20, 2026 (18 days old on October 8). Parish office parish@stanislawkostkasi.org / 718-447-3937 must confirm whether September 27 and October 4 were unpublished or posted elsewhere; the linked Facebook page does not expose readable posts in this session.'
revisit_after: 2026-10-14
evidence:
- url: https://stanislawkostkasi.org/bulletin
  seen: 2026-10-08
  quote: September 20, 2026
  note: 'Fresh T3 browser archive and actual HTTP fetch-check both select September 20. The production PDF fetch downloaded 922836 bytes successfully. Archive also lists September 13, September 6, August 30, August 23, August 16 and August 9: weekly cadence with occasional gaps, not a documented monthly publication.'
- url: https://stanislawkostkasi.org/wp-content/uploads/bulletins/2026/2026-09-20.pdf
  seen: 2026-10-07
  quote: ST . STANISLAUS KOSTKA CHURCH
  note: Current archive issue 2026-09-20, read on October 7, 2026. Text extracted from the PDF, including
    the named publisher and Mass schedule.
promoted: 2026-10-08
---

## Publisher

St. Stanislaus Kostka Parish publishes the issue linked above. Its dated bulletin, rather than a canonical merger or account name, determines this publisher row. The current archive was read on October 7, 2026.

The newest issue actually linked by the site's archive is September 20, 2026, not October 4. That two-week lag is recorded rather than inventing a newer issue URL. The current homepage repeats the same public Mass schedule.

## Worship sites

- St. Stanislaus Kostka Church (`churches/st-stanislaus-kostka-staten-island.md`): 10:00 AM - English.

## Website and bulletin provider

The parish homepage https://stanislawkostkasi.org/ links the active channel recorded in `publication`. Provider: `other`; pinned recipe or account: `page-pdfs https://stanislawkostkasi.org/bulletin`. The dated PDF was successfully downloaded and read;

On October 8, 2026, `uv run python -m pdf_extract fetch-check --parish st-stanislaus-kostka-staten-island` ran the actual HTTP resolver, not reconstructed anchors or saved-page replay. It returned `ok`, selected the September 20 PDF linked above and downloaded 922836 bytes through the production PDF-fetch path. A fresh T3 browser independently displayed the same latest issue. The recipe is operational; the publication's freshness remains a separate problem.

## Not yet confirmed

The issue is 18 days old as of October 8, 2026. The visible archive sequence September 20, 13, 6, August 30, 23, 16 and 9 establishes a normally weekly channel with occasional historical gaps. It does not justify treating this as monthly cadence. The archive links only its own PDFs and its parish Facebook page; the older archive is not a replacement channel. The current homepage supplies a schedule but not a newer bulletin. The remaining blocker is publisher confirmation of the missing September 27 and October 4 issues or the alternate channel, via parish@stanislawkostkasi.org / 718-447-3937. Successful fetch is not described as current-week coverage.
