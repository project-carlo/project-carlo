---
name: Notre Dame of Mt. Carmel
website: https://ndcarmel.com/
bulletin_provider: other
provider_id: page-pdfs https://ndcarmel.com/parish-updates
publication: ['ecatholic:10966']
group: ''
evidence:
- url: https://files.ecatholic.com/10966/documents/2026/10/Parish%20Update%20October%2021%202026-1.pdf
  seen: 2026-11-04
  quote: 'Parish Update: October 21, 2026'
  note: '20-page weekly issue. Page 1 text is the title above; page 2 is an image (read rendered): masthead
    ''Notre Dame of Mt. Carmel Church, 75 Ridgedale Ave., Cedar Knolls, NJ'', Mass Schedule Mon-Sat 12:00
    PM, Saturday 5:00 PM Vigil, Sunday 7:30 AM, 9:30 AM (Family Mass), 11:30 AM, 6:00 PM (with Contemporary
    Worship); Adoration in St. Benedict''s Chapel. Names no other church.'
- url: https://ndcarmel.com/parish-updates
  seen: 2026-11-04
  note: The parish's eCatholic site (site id 10966, behind Cloudflare; read in headed Chrome with visit.py).
    The Parish Updates page lists weekly PDFs newest first; the newest, files.ecatholic.com/10966/documents/2026/10/Parish%20Update%20October%2021%202026-1.pdf,
    is linked with the label 'October' (and a second copy without the -1 suffix has no label), then 'October
    14, 2026', 'September 29, 2026' and weekly back to October 2025. No 28 October issue was listed on
    4 November.
- url: https://ndcarmel.com/bulletins
  seen: 2026-11-04
  note: The site's Bulletins page lists eCatholic bulletins/<YYYYMMDD>.pdf files only to 20200531 (31
    May 2020); issues.py ecatholic ecatholic:10966 got 403 for 18 Oct-8 Nov 2026. The parish replaced
    the bulletin with the Parish Update.
- url: https://files.ecatholic.com/10966/documents/2026/11/Parish%20Update%20November%203%202026.pdf?t=1793829629000
  seen: 2026-11-07
  quote: 'Parish Update: November 3, 2026'
  note: '24-page weekly issue: the pick of fetch:check with page-pdfs on the Parish Updates page. Page
    2 is an image (read rendered): masthead ''Notre Dame of Mt. Carmel Church, 75 Ridgedale Ave., Cedar
    Knolls, NJ'', with the same Mass schedule. Names no other church.'
promoted: 2026-11-07
research:
- method: fetch:check with recipe page-pdfs https://ndcarmel.com/parish-updates (with and without filename=Parish*Update*.pdf)
  url: https://ndcarmel.com/parish-updates
  checked: '2026-11-04'
  outcome: unsupported-format
  next_action: Rerun fetch:check; if it picks the newest Parish Update (the label carries its date, or
    the resolver reads URL-encoded file names), set bulletin_provider other with this recipe and clear
    fetch_gap
  retry_when: The parish posts an issue with a dated label, or the page-pdfs resolver learns to date links
    from URL-encoded file names
- method: fetch:check with recipe page-pdfs https://ndcarmel.com/parish-updates (with and without filename=Parish*Update*.pdf)
  url: https://ndcarmel.com/parish-updates
  checked: '2026-11-07'
  outcome: found
bulletin_status: available
---

## Publisher

Notre Dame of Mt. Carmel, Cedar Knolls publishes a weekly "Parish Update" PDF in place of a bulletin, dated on Tuesdays and posted to its eCatholic site's documents folder (site id 10966). The newest on 4 November 2026, `https://files.ecatholic.com/10966/documents/2026/10/Parish%20Update%20October%2021%202026-1.pdf` (20 pages), opens "Parish Update: October 21, 2026". Its page 2 (an image, read rendered) is the masthead "Notre Dame of Mt. Carmel Church, 75 Ridgedale Ave., Cedar Knolls, NJ" with the Mass schedule: Mon-Sat 12:00 PM, Saturday 5:00 PM Vigil, Sunday 7:30, 9:30 (Family Mass), 11:30 AM and 6:00 PM. It is the parish's bulletin in all but name; the eCatholic `bulletins/` archive on `/bulletins` stops at 31 May 2020.

## Worship sites

- `notre-dame-of-mt-carmel-cedar-knolls`: the only church in the schedule. St. Benedict's Chapel, where adoration is held, has no Mass listed and no separate address; it is part of the church.

The diocese's finder (directory:10966) and GCatholic (18952) list this one church.

## Website and bulletin provider

`other`, recipe `page-pdfs https://ndcarmel.com/parish-updates`. `fetch:check` on 2026-11-07 picked the 3 November 2026 issue, 4 days old. On 2026-11-04 it had picked the 14 October issue over the 21 October one, whose links are labelled "October" and nothing; the date parser now reads URL-encoded file names, which closed the `undated-link-label` gap.

## Not yet confirmed

Nothing about the bulletin. Issues aren't posted every week: none was listed for 28 October by 4 November.
