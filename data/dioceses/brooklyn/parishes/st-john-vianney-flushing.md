---
name: St. John Vianney (Flushing)
website: https://stjvcflushing.org/
bulletin_provider: unsupported
provider_id: ''
publication: []
group: Deanery Q4 (Queens East)
evidence:
- url: https://drive.google.com/uc?export=download&id=1zIVQqqZP2da8z0G-9EVNiclyBEg-IC1n
  seen: 2026-11-05
  quote: ST. JOHN VIANNEY R.C. CHURCH NOVEMBER 8, 2026
  note: 'Google Drive file the site''s ''Current Bulletin'' menu item links (drive.google.com/file/d/1zIVQqqZP2da8z0G-9EVNiclyBEg-IC1n/view),
    4 pages, the 8 November 2026 issue. Page 1 masthead: ''ST. JOHN VIANNEY R.C. CHURCH'', 140-10 34th
    Avenue, Flushing, N.Y. 11354, Rev. Vincent Nguyen, CSJB - Pastor; one WEEKEND MASS SCHEDULE/WEEKDAY
    MASS SCHEDULE (English, Spanish, Mandarin, Cantonese) naming no other church.'
- url: https://stjvcflushing.org/english
  seen: 2026-11-05
  note: 'Next.js site (English, Spanish and Chinese pages). The header menu ''堂訊|Bulletin|Boletín'' is
    built in JavaScript: ''Current Bulletin'' takes its link from a published Google Sheet (docs.google.com/spreadsheets/d/e/2PACX-1vTluNW8isxYojYEx3z66U02bxHM4l4m0Bhkn7qIaGZ2vskpFGz_jR63NERCZhC2gWbGPZksC-Gjy50c/pub?output=csv,
    which held the Drive file link above on 2026-11-05), and ''Archived Bulletins'' links the Drive folder
    1o55ZqkffiVYXQHl6VkjvwMJFHheMoCSo (''Bulletin''), whose listing shows files named YYYYMMDD.pdf from
    20201129.pdf. All three language pages share the one bulletin menu.'
research:
- method: fetch:check unpinned on https://stjvcflushing.org/
  url: https://stjvcflushing.org/
  checked: '2026-11-05'
  outcome: unsupported-format
  next_action: Rerun fetch:check once a collector reads a link from a published Google Sheet or a JavaScript-built
    menu
  retry_when: A collector for sheet-held or JavaScript-menu bulletin links lands
- method: fetch:check with 'drive-folder https://drive.google.com/drive/folders/1o55ZqkffiVYXQHl6VkjvwMJFHheMoCSo'
    picked 20201129.pdf (first-listed); the folder's embeddedfolderview listing ends at 20230305.pdf,
    so the archive is not kept current
  url: https://drive.google.com/embeddedfolderview?id=1o55ZqkffiVYXQHl6VkjvwMJFHheMoCSo#list
  checked: '2026-11-05'
  outcome: not-found
  next_action: Recheck the folder listing for 2026 files
  retry_when: The parish resumes uploading issues to the archive folder
- method: 'fetch:check with page-pdfs on the published Google Sheet (pub?output=csv: ''Download is starting'';
    pubhtml: no PDF links)'
  url: https://docs.google.com/spreadsheets/d/e/2PACX-1vTluNW8isxYojYEx3z66U02bxHM4l4m0Bhkn7qIaGZ2vskpFGz_jR63NERCZhC2gWbGPZksC-Gjy50c/pub?output=csv
  checked: '2026-11-05'
  outcome: unsupported-format
  next_action: Set provider other with a recipe that reads the sheet's link, run fetch:check, and clear
    fetch_gap once it picks this week's issue
  retry_when: A collector that reads a URL from a published Google Sheet CSV lands
bulletin_status: available
fetch_gap:
  kind: js-menu-drive-file
  seen: 2026-11-05
  note: 'The site''s ''Current Bulletin'' link exists only in JavaScript: the Next.js header reads a published
    Google Sheet (pub?output=csv) holding one Google Drive file link, which changes with the issue. fetch
    finds no bulletin link on the homepage; page-pdfs on the sheet''s CSV starts a download and on its
    pubhtml finds no PDF; the ''Archived Bulletins'' Drive folder stops at 20230305.pdf, so drive-folder
    picks a 2020 file.'
  url: https://drive.google.com/file/d/1zIVQqqZP2da8z0G-9EVNiclyBEg-IC1n/view
---

## Publisher

St. John Vianney publishes its own weekly bulletin as a PDF on Google Drive, linked from its site's bulletin menu. The issue the site linked on 2026-11-05 is dated 8 November 2026 (page 2 header "ST. JOHN VIANNEY R.C. CHURCH NOVEMBER 8, 2026"); page 1 has "ST. JOHN VIANNEY R.C. CHURCH", "140-10 34th Avenue", Flushing, N.Y. 11354, Rev. Vincent Nguyen, CSJB - Pastor.

## Worship sites

One church. Page 1's WEEKEND MASS SCHEDULE/WEEKDAY MASS SCHEDULE lists Masses in English, Spanish, Mandarin and Cantonese (Saturday 3:30 PM Mandarin, 5:00 PM English; Sunday 8:00 AM Cantonese, 9:30 AM English, 11:00 AM Spanish, 12:45 PM Mandarin; weekday 8:30 AM and 12:00 PM), naming no other church. The diocese directory, deanery list, GCatholic 16726 and Mass finder 1146 list only this church.

## Language editions

One multilingual issue (English, Spanish, Chinese). The site's English, Spanish and Chinese pages share one bulletin menu with one 'Current Bulletin' link. The archive folder also holds a few Chinese-titled files from 2022-2023; no separate current Chinese edition is linked.

## Website and bulletin provider

`unsupported`, with a `fetch_gap` (`js-menu-drive-file`). stjvcflushing.org is a Next.js app whose bulletin menu exists only in JavaScript: 'Current Bulletin' reads a published Google Sheet (CSV) holding the current Drive file link, and 'Archived Bulletins' links Drive folder 1o55ZqkffiVYXQHl6VkjvwMJFHheMoCSo, whose files end at 20230305.pdf. On 2026-11-05 fetch:check found no bulletin link unpinned, picked a 2020 file with `drive-folder`, and got nothing with `page-pdfs` on the sheet (CSV download / pubhtml). See research.

## Not yet confirmed

Nothing about the parish itself; only the collection, which waits on a collector (see research and fetch_gap).
