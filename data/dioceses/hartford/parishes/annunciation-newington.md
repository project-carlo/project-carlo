---
name: Annunciation Parish
website: https://annunciationnewington.com/bulletins/
bulletin_provider: other
provider_id: linked-issue-page
publication: []
group: ''
evidence:
- url: https://cdn.diocesanweb.org/beacon/annunciationnew/wp-content/uploads/2026/11/0600AnnunciationNovember-15FINAL-2026.pdf
  seen: 2026-11-13
  quote: CHURCH OF HOLY SPIRIT
  note: 'Page 1 masthead of the 15 November 2026 issue (text layer): "ANNUNCIATION PARISH", Parish Office
    626 Willard Ave.; CHURCH OF ST. MARY 626 Willard Avenue; CHURCH OF HOLY SPIRIT 183 Church Street;
    Mass Times Daily Monday-Friday 9:00 am HS, Saturday Vigil 4:00 pm HS, Sunday 8:00 am SM, 9:15 am HS,
    10:30 am SM, 12:00 pm HS.'
- url: https://www.church-bulletin.org/bulletin/annunciation-parish-newington-ct-06111/2026-11-15.pdf
  seen: 2026-11-13
  note: The same 15 November 2026 issue as printed by church-bulletin.org (12 pages with ads, scanned,
    no text layer); page 1, read by rendering it, has the same masthead and Mass Times.
- url: https://annunciationnewington.com/bulletins/
  seen: 2026-11-13
  note: The Bulletins page links church-bulletin.org/?id=600 and yearly pages (/2023-2/, /2024-2/, /bulletins/2025-2/,
    /2026-2/); /2026-2/ links 46 self-uploaded PDFs oldest first, newest 0600AnnunciationNovember-15FINAL-2026.pdf.
bulletin_status: available
---

## Publisher

Annunciation Parish, Newington publishes one weekly bulletin, printed by church-bulletin.org (publisher id 600; file names on the parish site start `0600Annunciation`). The 15 November 2026 issue's page 1 masthead reads "ANNUNCIATION PARISH, Thirty-Third Sunday In Ordinary Time, November 15, 2026", Parish Office 626 Willard Ave., Newington.

## Worship sites

Two, both named on page 1 with their addresses and Masses: Church of St. Mary, 626 Willard Avenue (Sunday 8:00 and 10:30 am; `st-mary-newington`) and Church of Holy Spirit, 183 Church Street (Monday to Friday 9:00 am, Saturday Vigil 4:00 pm, Sunday 9:15 am and 12:00 pm; `holy-spirit-newington`). These are the directory's two churches of the parish (29, 44) and GCatholic's 22158 and 22157. The Hartford Courant's 7 May 2017 list: "St. Mary and Holy Spirit merging to form Annunciation."

## Website and bulletin provider

`other`, recipe `linked-issue-page` (printed by `fetch:check` on 2026-11-13, which followed the Bulletins page's church-bulletin.org/?id=600 link and picked `church-bulletin.org/bulletin/annunciation-parish-newington-ct-06111/2026-11-15.pdf`, this week's issue). That copy is scanned (no text layer), so the pipeline must read it as images. The parish also uploads a text-layer copy to its diocesanweb yearly page (/2026-2/, oldest first); `page-pdfs https://annunciationnewington.com/2026-2/` would read text, but the page moves each January, so the church-bulletin.org link was pinned instead.

## Not yet confirmed

Nothing open.
