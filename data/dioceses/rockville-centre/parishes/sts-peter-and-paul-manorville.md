---
name: Sts. Peter and Paul
website: https://www.saintspeterandpaul.org/home/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.saintspeterandpaul.org/home/bulletin#sts-peter-and-paul']
group: ''
evidence:
- url: https://www.saintspeterandpaul.org/home/bulletin/529-november-08-2026/file
  seen: 2026-11-13
  quote: Weekly Schedule at Sts. Peter and Paul
  note: '8 November 2026 issue (6 pages, Creator Canva, downloaded in Chrome; no advertisers or printer
    mark). Page 1: office hours, www.saintspeterandpaul.org, ''Rev. Matthew Considine, SMM - Pastor''.
    Page 2 Mass intentions (November 7-15, 2026): Saturday 5:00 PM; Sunday 9:00 AM, 11:00 AM, 7:00 PM;
    Monday ''No Mass''; Tuesday-Thursday 9:00 AM. Page 3: ''Saints Peter and Paul RC Church''.'
- url: https://www.saintspeterandpaul.org/home/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url gets 403): newest first, ''pdf music ministry''
    (Thanksgiving Day music), ''pdf November 08, 2026'' -> /home/bulletin/529-november-08-2026/file, ''pdf
    November 01, 2026'', ''pdf November Music 2026'' ... Music sheets are mixed in with the bulletins.'
research:
- method: pdftotext of the 8 November 2026 issue for a printer mark (4lpi.com, LPi footer, John Patrick,
    Church Bulletin Inc.); visit.py of the site for an embedded publisher
  url: https://www.saintspeterandpaul.org/home/bulletin
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), choosing
    dated items over the music sheets, then run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (as provider other, unpinned) found the 8 November
    post and failed: ''No PDF links found on bulletin post page: .../529-november-08-2026/file'' (the
    /file link is the PDF, which Chrome downloads with tools/browser_get.py; monthly music sheets share
    the list). The bulletin is parish-made (Canva, no printer), so there is no other listing.'
  url: https://www.saintspeterandpaul.org/home/bulletin/529-november-08-2026/file
---

## Publisher

Sts. Peter and Paul, 781 Wading River Road, Manorville publishes its own weekly bulletin, made in-house in Canva (6 pages, no advertisers or printer's mark). The 8 November 2026 issue (`https://www.saintspeterandpaul.org/home/bulletin/529-november-08-2026/file`, downloaded in Chrome 2026-11-13) has no cover masthead: page 1 gives the office hours, www.saintspeterandpaul.org and "Rev. Matthew Considine, SMM - Pastor"; page 3 is headed "Saints Peter and Paul RC Church" and "Weekly Schedule at Sts. Peter and Paul". No other parish is named; `group` is empty.

## Worship sites

One. The Mass intentions for November 7-15 (page 2) run Saturday 5:00 PM; Sunday 9:00 AM, 11:00 AM and 7:00 PM; Tuesday to Thursday 9:00 AM (Monday "No Mass"), and the issue names no other place ("Confession at the Church"; "The chapel is always open for silent prayer" is a chapel at the parish, with no Mass listed there). All Masses are counted at the church (`sts-peter-and-paul-manorville-church`). The diocesan locator, GCatholic and the diocese's Mass-times page list only this church.

## Website and bulletin provider

www.saintspeterandpaul.org is a Solutio (Joomla) site (`probe url` gets 403; `visit.py` reads it). /home/bulletin lists issues newest first, each linking straight to its `/file` PDF, with monthly music sheets ("November Music 2026", "music ministry") in the same list. The bulletin is parish-made, so there is no printer's listing; following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

`fetch:check` (2026-11-13, as provider `other`) found the 8 November post and failed: "No PDF links found on bulletin post page".

## Not yet confirmed

The 8 November issue was the newest bulletin posted on 2026-11-13.
