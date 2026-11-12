---
name: Cathedral of St. John the Baptist
website: https://rcdopcathedral.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://rcdopcathedral.org/bulletins
  seen: 2026-11-05
  note: Read with parish-site-access visit.py (probe url gets 403; eCatholic site 11263). The Bulletin
    page lists 15 files, the newest https://files.ecatholic.com/11263/bulletins/20200315.pdf, the oldest
    20191208.pdf; nothing after 15 March 2020. The site's menu (home page link list) has no bulletin item.
- url: https://rcdopcathedral.org/mass-schedule-1
  seen: 2026-11-05
  quote: Daily Spanish Mass is celebrated inside the Chapel of Our Lady.
  note: 'Mass & Sacramental Life page: Saturday 4:30 PM English, 6:00 PM Spanish; Sunday 8:30 AM English,
    10:00 AM Spanish, 11:30 AM English, 1:00 PM Spanish; daily 12:30 PM English, 7:00 PM Spanish.'
- url: https://patersoncathedral.org/bulletins
  seen: 2026-11-05
  note: The second domain named on the cathedral's Facebook page loads the same eCatholic site 11263 and
    the same list ending 20200315.pdf.
- url: https://www.facebook.com/CathedralPaterson
  seen: 2026-11-05
  note: 'Facebook page ''Cathedral of St. John the Baptist'', 381 Grand St, Paterson, read logged out
    with visit.py: intro and a post dated 4 November 2026 visible; no bulletin seen in the visible text.'
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:11263 'Cathedral of St. John the Baptist', 381 Grand Street, Paterson 07505,
    website https://rcdopcathedral.org/; Mass times as on the parish's page.
revisit: Reload https://rcdopcathedral.org/bulletins with visit.py and probe files.ecatholic.com/11263/bulletins/<Sunday>.pdf;
  if issues appear, set provider ecatholic, publication ecatholic:11263, and run fetch:check.
revisit_after: 2027-02-01
research:
- method: parish-site-access visit.py on /bulletins (link list) and the home page menu, on both rcdopcathedral.org
    and patersoncathedral.org
  url: https://rcdopcathedral.org/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reload the /bulletins page and look for a bulletin item in the menu
  retry_when: On the revisit date, or when the site or finder links a bulletin
- method: 'issues.py ecatholic ecatholic:11263: every Sunday 4 Oct - 8 Nov 2026, Saturdays 17 Oct - 7
    Nov 2026, and 2 Aug, 30 Aug, 27 Sep 2026 (all 403, not posted)'
  url: https://files.ecatholic.com/11263/bulletins/20261108.pdf
  checked: '2026-11-05'
  outcome: not-found
  next_action: Probe the coming Sundays' file names again
  retry_when: On the revisit date
- method: visit.py on the Facebook page, logged out (intro and latest post only)
  url: https://www.facebook.com/CathedralPaterson
  checked: '2026-11-05'
  outcome: not-found
  next_action: Look through the page's posts for bulletin images or PDFs
  retry_when: Facebook shows more of the page publicly
bulletin_status: not-found
---

## Publisher

No current bulletin found. The cathedral's eCatholic site (site id 11263, the finder pin id) has a Bulletin page, read 2026-11-05 with parish-site-access visit.py, whose 15 files run from `20191208.pdf` to `20200315.pdf` (`https://files.ecatholic.com/11263/bulletins/20200315.pdf`, 6 pages, sacraments and parish notices); nothing later is listed and the site menu has no bulletin item. `files.ecatholic.com/11263/bulletins/<YYYYMMDD>.pdf` answered 403 (not posted) for every Sunday 4 October - 8 November 2026, Saturday-dated names, and three Sundays August-September 2026. patersoncathedral.org, named on the Facebook page, is the same site. See `research`.

## Worship sites

One church, `cathedral-st-john-the-baptist-paterson` (381 Grand Street). The Mass & Sacramental Life page (2026-11-05) gives Saturday 4:30 PM English and 6:00 PM Spanish, Sunday 8:30 AM, 10:00 AM, 11:30 AM and 1:00 PM, and daily 12:30 PM English and 7:00 PM Spanish, adding "Daily Spanish Mass is celebrated inside the Chapel of Our Lady": a chapel within the cathedral, not a separate site. The finder lists this one pin (directory:11263); GCatholic omits the cathedral. Our Lady of Victories' administrator is also a cathedral parochial vicar (rcdop.org priest directory), which does not make a shared bulletin: neither posts one.

## Website and bulletin provider

`https://rcdopcathedral.org/` (the finder's website; eCatholic behind Cloudflare). Provider `no_bulletin`: public Mass but no bulletin posted since March 2020, so promote keeps the row and its church off the site until one turns up. No publication id is recorded; if issues reappear they will be `ecatholic:11263`.

## Not yet confirmed

Whether the cathedral prints a bulletin it doesn't post (the office, 973-345-4070, could say), or posts one on Facebook or Flocknote (rcdopcathedral.flocknote.com) beyond what a logged-out view shows. The revisit on 2027-02-01 rereads the Bulletin page and the eCatholic file names.
