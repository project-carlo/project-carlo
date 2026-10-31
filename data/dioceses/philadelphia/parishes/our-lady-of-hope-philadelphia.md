---
name: Our Lady of Hope Parish
website: https://www.olhcatholic.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://www.olhcatholic.org/bulletins#our-lady-of-hope']
group: ''
evidence:
- url: https://www.olhcatholic.org/bulletins
  seen: 2026-10-29
  quote: Bulletin 102526.pdf
  note: 'Google Sites page ''Bulletins'': dated entries newest first from 10/25/26 back to 12/21/25 (and
    empty headings 11/15/26, 11/8/26, 11/1/26 above them), each an embedded drive.google.com/file/d/<id>/preview
    file. The first embedded file downloads from drive.google.com/uc?export=download as a 4-page PDF with
    a text layer (md5 baf6c548...).'
- url: https://www.olhcatholic.org/bulletins
  seen: 2026-10-29
  note: The 25 October 2026 issue's page 1 masthead names 'OUR LADY OF HOPE CATHOLIC PARISH, Church of
    the Holy Child, 5200 North Broad Street, Philadelphia, PA 19141', Tel. 215-329-8100, Rev. Andrew Labatorio,
    Parochial Administrator, and shows Masses Saturday 4:00 PM English; Sunday 9:00 AM English, 11:00
    AM Spanish; weekdays 8:00 AM, 'NO MONDAY MASS'. It names no other church.
- url: https://www.olhcatholic.org/home
  seen: 2026-10-29
  quote: Weekdays (Tuesday-Friday) 8:00 AM - English (CHAPEL)
  note: 'Parish home page: Saturdays 4:00 PM English; Sundays 9:00 AM English and 11:00 AM Spanish; weekday
    Mass in the chapel.'
- url: https://archphila.org/parish/our-lady-of-hope-philadelphia/
  seen: 2026-10-28
  note: 'Directory page (updated 2 months ago): 5200 N. Broad St., Philadelphia 19141; ''Rev. Andrew Labatorio,
    C.I.C.M. (Parochial Administrator)''; Vigil Saturdays 4:30 PM, Sundays 8:30, 10:30 (Spanish), 12:30
    PM, which differs from the parish''s own 4:00, 9:00 and 11:00. No John Patrick listing exists for
    it (scan of ids 1-1300).'
revisit: Check whether the resolver reads a Google Sites page that embeds each Sunday as a Drive /preview
  iframe, or whether the parish posts a link/folder or moves its bulletin to a John Patrick listing, ParishesOnline
  or eCatholic.
revisit_after: 2027-01-15
research:
- method: pnpm fetch:check --diocese philadelphia --parish our-lady-of-hope-philadelphia with provider
    other, page-pdfs on olhcatholic.org/bulletins
  url: https://www.olhcatholic.org/bulletins
  checked: '2026-10-29'
  outcome: unsupported-format
  next_action: Re-run fetch:check if the resolver gains support for Google Sites Drive /preview iframes,
    or if the parish links a shared Drive folder (google_drive row) or another host
  retry_when: The page offers an anchor or folder link instead of embedded iframes, or the resolver reads
    Drive preview iframes
- method: visit.py in Chrome on the bulletins page, links matched on drive.google
  url: https://www.olhcatholic.org/bulletins
  checked: '2026-10-29'
  outcome: unsupported-format
  next_action: None until the page changes; the issues are iframes (drive.google.com/file/d/<id>/preview),
    with no anchor, and no shared folder is named
  retry_when: The parish site is rebuilt or a bulletin host appears
- method: John Patrick listing scan (ids 1-1300), directory website, home page text
  url: https://www.church-bulletin.org/
  checked: '2026-10-29'
  outcome: not-found
  next_action: Ask no one; look again only if the parish site links a publisher
  retry_when: The parish site links church-bulletin.org, ParishesOnline or eCatholic
- method: 'Manual read: first embedded Drive file downloaded from drive.google.com/uc?export=download
    (probe get) and read with pdftotext'
  url: https://www.olhcatholic.org/bulletins
  checked: '2026-10-29'
  outcome: found
  next_action: None
  retry_when: ''
bulletin_status: unsupported-format
publication_reviews:
- parish: st-james-elkins-park
  decision: separate
  evidence:
  - url: https://www.olhcatholic.org/bulletins
    seen: 2026-10-29
    note: 'The 25 October 2026 issue on the parish''s Bulletins page is the bulletin for Our Lady of Hope
      alone: its masthead names ''OUR LADY OF HOPE CATHOLIC PARISH, Church of the Holy Child, 5200 North
      Broad Street'' and its Masses are Saturday 4:00 PM, Sunday 9:00 AM and 11:00 AM; the 4-page file
      (md5 baf6c548...) is a different document from St. James''s listing-56 issue.'
---

## Publisher

Our Lady of Hope Parish (Church of the Holy Child), 5200 N. Broad St., Philadelphia 19141, posts its own weekly bulletin on its Google Site, olhcatholic.org/bulletins, as one embedded Drive PDF per Sunday (10/25/26 newest). The 25 October 2026 issue has a text layer and a masthead 'OUR LADY OF HOPE CATHOLIC PARISH, Church of the Holy Child, 5200 North Broad Street'. It is not printed by John Patrick Publishing; the scan of listings 1-1300 found no Our Lady of Hope.

## One bulletin or two with St. James, Elkins Park?

Two; see st-james-elkins-park. Rev. Andrew Labatorio serves both. St. James's issue is the John Patrick listing 56 file, headed 'SAINT JAMES THE GREAT CHURCH, 8320 Brookside Road, Elkins Park'. This issue names only Our Lady of Hope and its own Masses and intentions, and it says nothing of Elkins Park. A shared pastor is not a shared bulletin (settled rule).

## Worship sites

One church: the Church of the Holy Child at 5200 N. Broad St. The 'Chapel' in the bulletin ('Sanctuary Lights ... Chapel: for the immigrants') and the home page's weekday Mass '(CHAPEL)' are a room of this building with no separate address or Mass line, so no second church row. No other site is named.

## Website and bulletin provider

Google Sites page with embedded Drive file previews. The pipeline can't read it. The page embeds each Sunday as an iframe (`drive.google.com/file/d/<id>/preview`), not as a link, so `page-pdfs` found no PDF (fetch:check `resolve_failed`: 'No PDF links found on bulletin page') and Chrome sees only the iframes. No folder is shared. The row is `no_bulletin` with `bulletin_status: unsupported-format` (settled policy 4): a person can read the bulletin, and this record keeps its evidence for when the resolver or the page changes. The `publication` id is a `url:` with a fragment naming the publisher, since no other identity exists.

## Not yet confirmed

How to fetch it by machine: see `research`. Mass times on the church row come from the 25 October 2026 issue and the parish's home page, which agree.
