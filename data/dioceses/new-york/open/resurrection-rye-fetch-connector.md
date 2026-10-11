---
name: Resurrection Rye automatic fetch connector
revisit: 'The parish does publish a current readable HTML bulletin on Flocknote. Automatic PDF fetching
  is deliberately disabled: the tested page-pdfs recipe failed because the archive links HTML, not a PDF.
  Find a current PDF rendition or add a reviewed HTML connector before enabling fetch; do not classify
  the active church as closed or assert that no bulletin exists.'
revisit_after: 2026-10-15
roster: []
evidence:
- url: https://resrye.org/churchbulletins
  seen: 2026-10-08
  quote: October 4, 2026 Resurrection Church Bulletin
  note: Rendered official index inspected; the October 4, September 27 and September 20 entries all link Flocknote HTML notes, not PDF issues.
- url: https://resrye.flocknote.com/note/38786342
  seen: 2026-10-08
  quote: RESURRECTION CHURCH BULLETIN
  note: Followed the official index to the final parish-specific Flocknote URL. Complete note body and all anchors/iframes inspected; no linked PDF rendition or PDF attachment was present.
- url: https://new.flocknote.com/note/38786342
  seen: 2026-10-07
  quote: RESURRECTION CHURCH BULLETIN October 4, 2026
  note: Issue identity and current site-specific Mass schedule; see explanation.
- url: https://new.flocknote.com/note/38786342
  seen: 2026-10-07
  quote: Sunday, October 4th 7:30 am
  note: Issue identity and current site-specific Mass schedule; see explanation.
parish: resurrection-rye
---

## What is known

The parish does publish a current readable HTML bulletin on Flocknote. Automatic PDF fetching is deliberately disabled: the tested page-pdfs recipe failed because the archive links HTML, not a PDF. Find a current PDF rendition or add a reviewed HTML connector before enabling fetch; do not classify the active church as closed or assert that no bulletin exists.

## October 8 follow-up: format, not missing publication

The official index was opened again in the collaborative browser, followed to its redirected parish-specific Flocknote note, and the complete rendered note and outbound links were inspected. The October 4 publication contains the full weekly Mass intentions and parish notices as HTML. Its embedded media are YouTube videos, not a bulletin PDF. The official index's three recent entries are Flocknote notes. The secondary Resurrection listing at https://discovermass.com/church/resurrection-rye-ny/ was also fetched successfully and exposed no downloadable issue; this secondary absence is not evidence that the parish stopped publishing.

The remaining blocker is an ingestion-format implementation, not an unanswered research probe: the fetch pipeline stores, compacts and classifies PDFs, and its tested `page-pdfs` collector cannot ingest this HTML publication. Before enabling it, either obtain an actual parish PDF channel or review and test an explicit HTML-to-PDF/text ingestion path that preserves the issue date, complete schedule and provenance, rejecting login/error pages. Do not substitute a screenshot, unrelated PDF or the Mass Intentions link retained in the note, which points to September 19-26 rather than this issue's October 3-10 intentions.

## Off-site safeguard

Under the October 7 off-site policy, this publisher and its church remain in the curated evidence records but are omitted from the live CSVs and site, without promoted stamps, until a supported safe channel is available.

Resolve the format/full-issue selection question and test the resulting connector on the current publication before enabling automatic fetch. This is a pipeline question, not a second physical church or an absence-based exclusion.
