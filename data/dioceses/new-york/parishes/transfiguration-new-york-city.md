---
name: Transfiguration New York City
website: https://www.transfigurationnyc.org/bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.transfigurationnyc.org/bulletin
publication: ['ecatholic:32400']
group: ''
evidence:
- url: https://www.transfigurationnyc.org/bulletin
  seen: 2026-10-08
  quote: THIS WEEK'S BULLETIN
  note: Actual rendered menu and singular bulletin page inspected in the collaborative browser; direct HTTP recheck is Cloudflare-blocked. The current button links the October 4 document, not the empty plural /bulletins archive.
- url: https://files.ecatholic.com/32400/documents/2026/10/10.4.26%20Bulletin-2.pdf
  seen: 2026-10-08
  quote: October 04, 2026
  note: Stable eCatholic files-host rendition downloaded and text read on pages 1-3; page 1 gives the issue date, 29 Mott Street and Mass schedule. Eight pages total, all with readable text layers.
- url: https://www.transfigurationnyc.org/documents/2026/10/10.4.26%20Bulletin-2.pdf
  seen: 2026-10-08
  quote: October 04, 2026
  note: Eight-page PDF downloaded; pages 1-3 read. Page 1 gives 29 Mott Street and the Transfiguration Mass timetable; page 3 mentions St. James only as a pilgrimage pickup point, not a second Mass location. Direct recheck may return 403; the files-host rendition above is independently readable.
- url: https://files.ecatholic.com/32400/documents/2026/10/10.4.26%20Bulletin-1.pdf
  seen: 2026-10-07
  quote: 29 Mott Street, New York, NY 10013
- url: https://files.ecatholic.com/32400/documents/2026/10/10.4.26%20Bulletin-1.pdf
  seen: 2026-10-07
  quote: October 04, 2026
promoted: 2026-10-08
---

## Publisher

The October 4, 2026 masthead identifies Transfiguration New York City at the quoted address. Current issue read, not a canonical-merger inference.

## Worship sites

The named church has its public Mass schedule in this issue. No additional buildings are inferred from a directory merger label.

## Website and bulletin provider

The official navigation links the singular `/bulletin` page and its current button links the document PDF quoted above. The eCatholic provider appends `/bulletins`; that plural archive is empty in both actual HTTP HTML and the rendered browser on October 8. The old provider therefore did not resolve this publisher even though its issue exists. The supported `other` provider with the pinned `page-pdfs` recipe reads the actual document listing. Publication identity `ecatholic:32400` is retained because the documents belong to that site; storage hosting and the collector used to read the listing are different facts.

## Not yet confirmed

On October 8, a targeted resolver check reconstructed the observed rendered bulletin-button subtree and passed it to the actual `other` resolver with the pinned recipe. It selected `10.4.26 Bulletin-2.pdf` and the production download function retrieved a valid 7,270,929-byte PDF. This is a reconstructed-subtree check plus a real PDF download, not a complete live-browser `fetch-check` run: unauthenticated direct HTTP retrieval of the singular listing was blocked with 403, while the collaborative browser rendered it. The URL-date diagnostic reported October 10 from the directory/filename numbers; the actual page-1 masthead says October 04, 2026 and is the issue-date evidence. Do not call this an October 10 issue based on that diagnostic.

Additional worship sites require their own current public Mass evidence.
