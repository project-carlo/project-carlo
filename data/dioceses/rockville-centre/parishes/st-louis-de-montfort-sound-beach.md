---
name: St. Louis de Montfort
website: https://www.stlouisdm.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stlouisdm.org/bulletin#st-louis-de-montfort']
group: ''
evidence:
- url: https://www.stlouisdm.org/bulletin/509-november-8-2026/file
  seen: 2026-11-13
  quote: 75 New York Avenue Sound Beach, NY 11789
  note: '8 November 2026 issue (16 pages, Creator Microsoft Office Publisher 2007 / Acrobat Distiller,
    downloaded in Chrome). Page 1 masthead: ''ST. LOUIS DE MONTFORT CHURCH, 75 New York Avenue Sound Beach'';
    Rev. Msgr. Christopher J. Heller, Pastor. Mass: Monday-Friday 8:30am in the Chapel; Saturday 5:00pm
    in Church; Sunday 7:30am, 10:00am and 12:00 Noon. Back page: ''#247 FOR ADVERTISING: THE CHURCH BULLETIN
    INC.''.'
- url: https://www.stlouisdm.org/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url gets 403): newest first, ''pdf November 8
    2026'' -> /bulletin/509-november-8-2026/file, then November 1, October 25 ...'
research:
- method: pdftotext of the 8 November 2026 issue for a printer mark (4lpi.com, LPi footer, John Patrick);
    visit.py of the site for an embedded publisher
  url: https://www.stlouisdm.org/bulletin
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), then
    run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (as provider other, unpinned) followed the 8
    November /file link and failed: ''No PDF links found on bulletin page: .../509-november-8-2026/file''
    (the /file link is the PDF, which Chrome downloads with tools/browser_get.py). Printed by The Church
    Bulletin Inc. (job #247), which posts no listing.'
  url: https://www.stlouisdm.org/bulletin/509-november-8-2026/file
---

## Publisher

St. Louis de Montfort, 75 New York Avenue, Sound Beach publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#247 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts its own copy. The 8 November 2026 issue (`https://www.stlouisdm.org/bulletin/509-november-8-2026/file`, downloaded in Chrome 2026-11-13; 16 pages, Publisher 2007 via Acrobat Distiller, text layer readable) has the page 1 masthead "ST. LOUIS DE MONTFORT CHURCH, 75 New York Avenue Sound Beach, NY 11789" and names Rev. Msgr. Christopher J. Heller, Pastor. No other parish is named; `group` is empty.

## Worship sites

One. The masthead's "OUR REGULAR MASS SCHEDULE" gives "Monday-Friday: 8:30am in the Chapel / Saturday Mass: 5:00pm in Church" and Sunday 7:30am, 10:00am and 12:00 Noon. The Chapel is a room of the parish at the same address (the issue also holds classes and meetings "in the Chapel"; no other address is given), so it is not a separate worship site; all Masses are counted at the church (`st-louis-de-montfort-sound-beach-church`). The diocesan locator, GCatholic and the diocese's Mass-times page list only this church.

## Website and bulletin provider

www.stlouisdm.org is a Solutio (Joomla) site (`probe url` gets 403; `visit.py` reads it). /bulletin lists issues newest first, each linking straight to its `/file` PDF. The printer posts no listing and the issue carries no LPi or John Patrick mark, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

`fetch:check` (2026-11-13, as provider `other`) followed the 8 November `/file` link and failed: "No PDF links found on bulletin page".

## Not yet confirmed

The 8 November issue was the newest posted on 2026-11-13. That the Chapel is on the church grounds is inferred from the bulletin (no separate address); the parish site was not checked for a map.
