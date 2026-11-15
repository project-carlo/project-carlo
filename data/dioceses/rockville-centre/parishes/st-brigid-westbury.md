---
name: St. Brigid
website: https://saintbrigid.net/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://saintbrigid.net/bulletin#st-brigid-westbury']
group: ''
evidence:
- url: https://saintbrigid.net/bulletin/864-november-15-2026/file
  seen: 2026-11-13
  quote: Our Lady's Chapel is located in our school building at 101
  note: 'Issue for 15 November 2026 (22 pages, made in Marq; downloaded with tools/browser_get.py). Page
    1 is an image: ''St. Brigid''s R.C. Church / 33rd Sunday in Ordinary Time / XXXIII Domingo del Tiempo
    Ordinario / 15 November 2026''. Page 22 ''We Celebrate the Eucharist (Mass)'': Saturday Evening (Church
    - Post Avenue) 5:00 pm (English) - 7:00 pm (Spanish); Sunday (Church - Post Avenue) 8:00 am (English/Italian)
    - 10:00 am (English) - 11:45 am (English) - 2:30 pm (Kreyol) - 6:00 pm (English); Sunday (Our Lady''s
    Chapel in the School - 101 Maple Avenue) 7:30 am (Spanish) - 9:15 am (English) - 11:00 am (Spanish)
    12:45 pm (Spanish); Daily Mass Monday-Friday 7 a.m. and 12:10 p.m. (St. Brigid''s Church).'
- url: https://saintbrigid.net/bulletin
  seen: 2026-11-13
  note: 'Bulletin page (403 to probe url; read with parish-site-access visit.py) lists issues newest first
    as /bulletin/<n>-<month>-<d>-<yyyy>/file: 864-november-15-2026, 861-november-8-2026, 858-november-1-2026
    ...'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Joomla site. fetch:check on 2026-11-13 found the 15 November post but failed: ''No PDF links
    found on bulletin post page: https://saintbrigid.net/bulletin/864-november-15-2026/file'' (the /file
    link is the PDF; the host answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.
    The issue is made in Marq; no printer listing.'
  url: https://saintbrigid.net/bulletin/864-november-15-2026/file
---

## Publisher

St. Brigid, Westbury publishes its own weekly bilingual bulletin (made in Marq, so self-made) on its site. The newest issue on 2026-11-13, `https://saintbrigid.net/bulletin/864-november-15-2026/file` (22 pages), has an image cover reading "St. Brigid's R.C. Church / 33rd Sunday in Ordinary Time / XXXIII Domingo del Tiempo Ordinario / 15 November 2026". Page 22, "We Celebrate the Eucharist (Mass)", gives the schedule for two places: the church on Post Avenue (Saturday 5:00 PM English and 7:00 PM Spanish; Sunday 8:00 English/Italian, 10:00, 11:45 AM, 2:30 PM Kreyol and 6:00 PM; weekdays 7:00 AM and 12:10 PM; Wednesday 7:30 PM Spanish; Saturday 8:00 AM) and "Our Lady's Chapel in the School - 101 Maple Avenue" (Sunday 7:30 Spanish, 9:15 English, 11:00 Spanish, 12:45 PM Spanish).

## Worship sites

Two: the church at 75 Post Avenue (`st-brigid-westbury-church`) and Our Lady's Chapel in the parish school at 101 Maple Avenue (`our-ladys-chapel-westbury-church`), which has four Sunday Masses of its own (page 21 of the same issue: "Our Lady's Chapel is located in our school building at 101 Maple Avenue"). The diocesan locator (directory:37) and GCatholic (16933) list only the church; the drvc.org Mass-times page lists the chapel's Masses under St. Brigid ("Sunday (Our Lady Chapel)"). The Ruthenian St. Andrew the Apostle in Westbury (GCatholic 17200) is another jurisdiction's and is handled in the eastern-catholic batch.

## Website and bulletin provider

The site is a Joomla site whose bulletin list links each issue at `/bulletin/<n>-<date>/file`; `probe url` gets 403, while Chrome (`visit.py`, `browser_get.py`) reads the page and downloads the PDFs. The cover page is an image; the schedule and text pages have a text layer.

The provider is `unsupported` with fetch gap `joomla-file-endpoint`: `fetch:check` (2026-11-13) on the site reached the 15 November post but reported "No PDF links found on bulletin post page: https://saintbrigid.net/bulletin/864-november-15-2026/file", since the `/file` link is itself the PDF. The bulletin is made in Marq (PDF Creator) with no printer's marks, so there is no ParishesOnline or John Patrick listing to use instead (playbook rule for Solutio/Joomla sites). When a collector reads `/file` endpoints, set provider `other` with `page-pdfs https://saintbrigid.net/bulletin` and rerun `fetch:check`.

## Not yet confirmed

Nothing open.
