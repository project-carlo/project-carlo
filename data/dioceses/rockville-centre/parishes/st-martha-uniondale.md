---
name: St. Martha
website: https://saintmartha.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://saintmartha.org/news/bulletin#st-martha']
group: ''
evidence:
- url: https://saintmartha.org/news/bulletin/509-32nd-sunday-in-ordinary-time-2026/file
  seen: 2026-11-13
  quote: Fr. Rony Fabien, Pastor
  note: 'Issue for the 32nd Sunday in Ordinary Time, November 8, 2026 (14 pages, Microsoft Publisher 2021).
    Page 1: ''Visit www.saintmartha.org'', main church number (516) 481-2550, parish staff. Its collection
    report lists the weekend Masses: 5:00 PM (English), 7:00 PM (Spanish), 7:30 AM (English), 9:00 AM
    (Spanish), 11:00 AM (English), 12:30 PM (Creole). No full Mass schedule is printed. Downloaded through
    Chrome (tools/browser_get.py).'
- url: https://saintmartha.org/
  seen: 2026-11-13
  note: 'Home page (read with parish-site-access visit.py; probe url answers 403): Weekend Mass Saturday
    Vigil 5:00 pm (English), 7:00 pm (Spanish); Sunday 7:30 am (English), 9:00 am (Espanol), 11:00 am
    (English), 12:30 pm (Creole); Weekdays 8:30 am (English Mon-Fri).'
- url: https://saintmartha.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin page, read with visit.py: issues newest first as /news/bulletin/<n>-<title>/file,
    the newest 509-32nd-sunday-in-ordinary-time-2026, then 508-31st..., 507-30th...'
research:
- method: fetch:check, page-pdfs on the Solutio bulletin page
  url: https://saintmartha.org/news/bulletin
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Rerun fetch:check once a collector reads Solutio /file links
  retry_when: pnpm diocese gaps shows a collector for joomla-file-endpoint
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (page-pdfs on /news/bulletin) failed: "No PDF
    links found on bulletin page: https://saintmartha.org/news/bulletin". The issues are /news/bulletin/<n>-<title>/file
    links, which Chrome downloads with tools/browser_get.py. The issue is made in Microsoft Publisher
    2021; no printer listing.'
  url: https://saintmartha.org/news/bulletin/509-32nd-sunday-in-ordinary-time-2026/file
publication_reviews:
- parish: queen-of-the-most-holy-rosary-roosevelt
  decision: separate
  evidence:
  - url: https://saintmartha.org/news/bulletin/509-32nd-sunday-in-ordinary-time-2026/file
    seen: 2026-11-13
    note: 'The 8 November 2026 masthead names St. Martha alone: ''Visit www.saintmartha.org'', Fr. Rony
      Fabien, Pastor, with its own staff and Mass collection list.'
  - url: https://www.qtmhr.com/news/bulletin/337-32nd-sunday-in-ordinary-time-2026/file
    seen: 2026-11-13
    note: The 8 November 2026 masthead names Queen of the Most Holy Rosary, Roosevelt alone, with its
      own Mass schedule and staff (page 1, read as an image).
---

## Publisher

St. Martha, Uniondale publishes its own weekly bulletin, made in Microsoft Publisher 2021 and posted on its Solutio (Joomla) site; it carries no printer's name. The newest issue on 2026-11-13, `https://saintmartha.org/news/bulletin/509-32nd-sunday-in-ordinary-time-2026/file` (14 pages, "32nd Sunday in Ordinary Time—November 8, 2026"), has on page 1 "Visit www.saintmartha.org", "main church number: (516) 481-2550" and "Fr. Rony Fabien, Pastor", with Deacon Hernst Bellevue for the English/Creole baptismal program. It prints no Mass schedule; its collection report lists the weekend Masses: 5:00 PM (English), 7:00 PM (Spanish), 7:30 AM (English), 9:00 AM (Spanish), 11:00 AM (English), 12:30 PM (Creole). The parish home page gives the same weekend Masses (Saturday Vigil 5:00 and 7:00 pm; Sunday 7:30, 9:00, 11:00 am and 12:30 pm) and weekdays 8:30 am Monday-Friday.

## Worship sites

One: the church at 546 Greengrove Avenue (`st-martha-uniondale-church`). The bulletin and site name no other place where Mass is said (Bethany Hall is a parish hall). The diocesan locator (directory:54), GCatholic (16925) and the drvc.org Mass-times page list only this church.

## Shared pastor with Queen of the Most Holy Rosary

Fr. Rony Fabien is pastor of both this parish and Queen of the Most Holy Rosary, Roosevelt (`queen-of-the-most-holy-rosary-roosevelt`), and Deacon Hernst Bellevue serves both. They publish two bulletins: the 8 November 2026 issues are separate files on separate sites (saintmartha.org issue 509, qtmhr.com issue 337) with different covers, staff lists and schedules; this one names St. Martha alone, and it advertises a Spanish Advent retreat "at the Queen of the Most Holy Rosary Parish located at 196 West Centennial Ave in Roosevelt" as another parish's venue. So two rows, recorded as `separate` in `publication_reviews`.

## Website and bulletin provider

saintmartha.org is the locator's and Mass-times page's link; GCatholic's stmarthauniondale.org does not resolve (`probe url` DEAD-DNS, 2026-11-13). `probe url` answers 403 on saintmartha.org; visit.py reads it. The bulletin page lists issues newest first as `/news/bulletin/<n>-<title>/file`, which Chrome downloads (tools/browser_get.py) but `fetch:check` can't: on 2026-11-13 it reported "No PDF links found on bulletin page". The row is `unsupported` with `fetch_gap` `joomla-file-endpoint`, following the diocese's rule for Solutio sites with no printer listing.

## Not yet confirmed

The drvc.org Mass-times page adds a 7:00 PM Spanish Mass on Sunday and gives weekdays Monday-Saturday; the bulletin's collection list and the parish site have the 7:00 pm Spanish Mass on Saturday and weekdays Monday-Friday, and those are followed. Nothing else open.
