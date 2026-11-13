---
name: Assumption of the Blessed Virgin Mary
website: https://www.abvmcentereach.com/about-us/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.abvmcentereach.com/about-us/bulletin#assumption-bvm']
group: ''
evidence:
- url: https://www.abvmcentereach.com/about-us/bulletin/61-november-8-2026/file
  seen: 2026-11-13
  quote: 'Saturdays: 5:30 PM'
  note: '8 November 2026 issue (7 pages, Creator Affinity 3.3.3, downloaded in Chrome). Page 1 (image,
    rendered): ''ASSUMPTION OF THE BLESSED VIRGIN MARY'', ''20 Chestnut Street, Centereach, NY 11720 631-585-8760
    www.abvmcentereach.com'', ''Rev. Joseph Alenchery, Pastor''. Page 2: ''We celebrate EUCHARIST Saturdays:
    5:30 PM Sundays: 9:30, 11:30 AM Weekdays: Mon—Thurs 9:00 AM''. No printer or advertiser pages.'
- url: https://www.abvmcentereach.com/about-us/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url gets 403): newest first, ''New November 8,
    2026'' -> /about-us/bulletin/61-november-8-2026/file, then November1, October 25 ...'
research:
- method: pdfinfo and pdftotext of the 8 November 2026 issue for a printer; visit.py of the site for an
    LPi, ParishesOnline or John Patrick listing
  url: https://www.abvmcentereach.com/about-us/bulletin
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), then
    run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post and failed: "No PDF
    links found on bulletin post page: .../61-november-8-2026/file" (the /file link is the PDF, which
    Chrome downloads with tools/browser_get.py). The issue is parish-made (Affinity); no printer listing.'
  url: https://www.abvmcentereach.com/about-us/bulletin/61-november-8-2026/file
---

## Publisher

Assumption of the Blessed Virgin Mary, 20 Chestnut Street, Centereach makes its own weekly bulletin (8 November 2026 issue, `https://www.abvmcentereach.com/about-us/bulletin/61-november-8-2026/file`, downloaded in Chrome 2026-11-13: 7 pages, Creator Affinity 3.3.3, no printer's mark or advertising pages). Page 1 (an image, read rendered) has the masthead "ASSUMPTION OF THE BLESSED VIRGIN MARY", "20 Chestnut Street, Centereach, NY 11720" and "Rev. Joseph Alenchery, Pastor".

## Worship sites

One row: the church (`assumption-of-the-bvm-centereach-church`). Page 2 gives "We celebrate EUCHARIST Saturdays: 5:30 PM Sundays: 9:30, 11:30 AM Weekdays: Mon—Thurs 9:00 AM" with no other place named. The diocesan locator (directory:70), GCatholic (16824) and the Mass-times page list the same one church. The Mass-times page (read 2026-11-12) still gives a fuller schedule (Saturday 5:30 PM; Sunday 8:15, 9:30, 11:00 AM, 12:30 PM); the bulletin is current and is followed.

## Website and bulletin provider

www.abvmcentereach.com is a Solutio (Joomla) site: `probe url` gets 403, `visit.py` reads it. Issues are listed newest first at /about-us/bulletin as one `/file` link per Sunday. `fetch:check` (2026-11-13) found the 8 November post and failed: "No PDF links found on bulletin post page". The PDF is made by the parish (Affinity) and the site embeds no publisher, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

The 8 November issue was the newest posted on 2026-11-13.
