---
name: St. Mary of the Assumption, Katonah
website: https://stmarykatonah.com
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stmarykatonah-my.sharepoint.com/:f:/p/office/EkVru5Q3-_BDivkRCF4VEUEBqt80znOHFrQeIYO4yg5SLQ']
group: ''
evidence:
- url: https://stmarykatonah-my.sharepoint.com/:f:/p/office/EkVru5Q3-_BDivkRCF4VEUEBqt80znOHFrQeIYO4yg5SLQ
  seen: 2026-11-08
  quote: 20261108.pdf
  note: 'Folder ''S M Bulletin - CURRENT YEAR'' rendered in headed Chrome; files 20260830.pdf to 20261108.pdf.
    The 8 November issue downloaded and read: cover ''November 8, 2026'', Mass intentions 7-15 November
    (Saturday 8:30 AM, 4:00 PM, 5:15 PM; Sunday 7:30, 9:00, 11:00 AM; weekdays 8:30 AM); page 8 job line
    ''027D (JA) - St. Mary, Katonah''. The file is not publicly addressable, so recheck can''t find this
    quote in a PDF.'
- url: https://stmarykatonah.com/liturgy-and-sacraments/
  seen: 2026-11-08
  quote: St. Matthias Church Mass
  note: 'Parish Mass page: St. Mary''s Church Masses, 55 Valley Rd (Saturday 8:30 AM, 5:15 PM; Sunday
    7:30, 9:00, 11:00 AM; Mon-Fri 8:30 AM) and St. Matthias Church Mass, 109 Babbitt Rd, Bedford Hills
    (Saturday 4:00 PM).'
- url: https://stmarykatonah.com
  seen: 2026-11-08
  quote: Browse
  note: Homepage; its Browse button links the OneDrive bulletin folder.
research:
- method: fetch-check resolver from main (provider other, automatic) on the homepage and the OneDrive
    folder link
  url: https://stmarykatonah-my.sharepoint.com/:f:/p/office/EkVru5Q3-_BDivkRCF4VEUEBqt80znOHFrQeIYO4yg5SLQ
  checked: '2026-10-31'
  outcome: unsupported-format
  next_action: Re-run fetch:check once a OneDrive/SharePoint shared-folder collector exists
  retry_when: A OneDrive shared-folder collector lands on main
- method: Bon Venture sponsor site (no parish lookup) and web search for a sponsor page
  url: http://sponsors.bonventure.net/
  checked: '2026-11-08'
  outcome: not-found
  next_action: Look for a sponsors.bonventure.net/?page= link on stmarykatonah.com
  retry_when: The parish site adds a Bulletin link other than the OneDrive folder
bulletin_status: unsupported-format
fetch_gap:
  kind: onedrive-shared-folder
  seen: 2026-11-08
  url: https://stmarykatonah-my.sharepoint.com/:f:/p/office/EkVru5Q3-_BDivkRCF4VEUEBqt80znOHFrQeIYO4yg5SLQ
  note: 'The weekly PDFs (named YYYYMMDD.pdf by Sunday, newest 20261108.pdf on 2026-11-08) sit in an anonymous
    OneDrive/SharePoint shared folder linked by the homepage''s Browse button. No collector reads it:
    fetch:check with provider other (2026-10-31) found no bulletin link on the homepage or the folder.
    Files download only in the folder''s guest session through _layouts/15/download.aspx?SourceUrl=<path>.'
---

## Publisher

St. Mary of the Assumption, Katonah publishes a weekly 8-page bulletin, printed by Bon Venture (page 8 job line "027D (JA) - St. Mary, Katonah"). The parish homepage https://stmarykatonah.com links it with a "Browse" button to an anonymous OneDrive folder, "S M Bulletin - CURRENT YEAR", which on 8 November 2026 listed one PDF per Sunday from 20260830.pdf to 20261108.pdf. The 8 November issue (downloaded through the folder's guest session and read 8 November) has the cover "November 8, 2026" and Mass intentions for 7 to 15 November: Saturday 8:30 AM, 4:00 PM and 5:15 PM; Sunday 7:30, 9:00 and 11:00 AM; weekdays 8:30 AM. Its pages name St. Mary's Church, 55 Valley Road, and the parish website.

## Worship sites

- [St. Mary of the Assumption](../churches/st-mary-of-the-assumption-katonah.md), 55 Valley Road, Katonah: every Mass but Saturday 4:00 PM.
- [St. Matthias](../churches/st-matthias-bedford-hills.md), 109 Babbitt Road, Bedford Hills, the parish's mission chapel: Saturday 4:00 PM.

The bulletin's intentions do not say where each Mass is. The attribution comes from the parish's Liturgy and Sacraments page (read 8 November), which lists "St. Mary's Church Masses, 55 Valley Rd": Saturday 8:30 AM and 5:15 PM, Sunday 7:30, 9:00, 11:00 AM, Mon-Fri 8:30 AM, and "St. Matthias Church Mass, 109 Babbitt Rd": Saturday 4:00 PM. The bulletin's times match it exactly. The archdiocese's map lists the same two places under this parish ("St. Mary's Church" and "St. Matthias Mission Chapel"). The parish offices at 99 Valley Road hold no Mass.

## Website and bulletin provider

`unsupported`, with `fetch_gap` `onedrive-shared-folder`: the issues sit in a OneDrive/SharePoint shared folder, and no collector reads one (main's `drive-folder` reads Google Drive only). fetch:check's resolver with provider `other` (31 October) found no bulletin link on either the homepage or the folder link. A file downloads only inside the folder's guest session, via `_layouts/15/download.aspx?SourceUrl=/personal/office_stmarykatonah_com/Documents/S M Bulletin - CURRENT YEAR/<YYYYMMDD>.pdf`; the file names are the Sunday's date, so a collector could date them.

The October research saw the folder end at 20260920.pdf on October 8; by 8 November the September 27 to November 8 issues had all been uploaded, so the parish does keep it current, if sometimes late. No Bon Venture sponsor page for the parish was found (the sponsor site has no parish lookup; a web search found none), Discover Mass lists no issues, and stmarykatonah.com/bulletins is a 404.

## Not yet confirmed

A Bon Venture sponsor page (`sponsors.bonventure.net/?page=<n>`) for this parish would be readable by `page-pdfs` and would replace the gap; none was found.
