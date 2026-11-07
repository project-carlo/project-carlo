---
name: St. John the Evangelist, Mahopac
website: https://sjtemahopac.flocknote.com/home/notes
bulletin_provider: no_bulletin
provider_id: ''
publication:
- url:https://sjtemahopac.flocknote.com/home/notes
group: ''
evidence:
- url: https://sjtemahopac.flocknote.com/note/38887047/file/656720/10112026final.pdf
  seen: '2026-10-10'
  quote: 'Saturday Evening Vigil: 4:00 p.m.'
  note: October 11, 2026 full bulletin downloaded and read October 10. Masthead locates Church of St.
    John the Evangelist at 221 East Lake Boulevard. Sunday schedule 7:30, 9, 10:15 Polish, 11:30 AM and
    5:30 PM; the accompanying current note cancels the Polish Mass for October 11 only.
- url: https://sjtemahopac.flocknote.com/note/38887047
  seen: '2026-10-10'
  quote: 'Please note: The Polish Mass is cancelled this Sunday.'
  note: October 11 issue published October 9, 2026, 2:30 PM; latest item in public /home/notes and anonymous
    /home/api/mynotes feed on October 10. A real full-issue PDF, unlike the HTML-only Rye/IHM publications.
revisit: 'A current full-issue PDF is proven. Implement/review an anonymous Flocknote notes-feed collector:
  /home/api/mynotes exposes latest note IDs; /note/<ID> links a stable /file/<ID>/<filename>.pdf that
  redirects to a fresh signed S3 URL. The existing page-pdfs collector finds no candidate on the current
  feed; do not pin one October 11 note forever or treat sjte.online TLS failure as no publication.'
revisit_after: '2026-10-17'
---

## Publisher and actual current PDF

The public Flocknote Notes feed was opened in owned T3 tab tab_2. Its latest item is Bulletin and Mass Schedule for 10/11/2026, published October 9 at 2:30 PM. The full PDF linked from note 38887047 was downloaded successfully by HTTP and its masthead and Mass intentions read. This is a standalone Mahopac publisher; Discover Mass?s empty archive is not a no-publication finding.

## Automatic fetch safeguard

The existing served-HTML PDF collector returns zero candidates for /home/notes; the rendered feed also has no PDF anchors, and clicking a feed card asks for login. Public individual notes and the anonymous feed API do work without authentication. A reviewed feed-to-note-to-file collector is needed; no_bulletin temporarily disables automatic PDF ingestion, not a factual assertion that no bulletin exists. Do not use the expiring signed S3 URL as website or pin the single October 11 note as a perpetual archive.

The Flocknote home?s old sjtemahopac.org link now redirects to unrelated jmwa.org Japanese content; do not adopt it as the parish website. sjte.online currently fails HTTPS. The stable public Flocknote channel avoids both dead-domain leads.

## Worship site

[St. John the Evangelist](../churches/st-john-the-evangelist-mahopac.md) is the established worship site. Its record documents the 221/225 address discrepancy and the separate chapel services; no separate chapel building is invented.
