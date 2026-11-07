---
name: St. Joseph
website: https://sanjosepaterson.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://sanjosepaterson.org/bulletins
  seen: 2026-11-05
  quote: 399 Market Street, Paterson, NJ, 07501
  note: Read with parish-site-access visit.py (probe url gets 403; eCatholic site 11440). The page shows
    only the headings 'Bulletin' and 'Archive' and the footer 'St. Joseph Catholic Church, 399 Market Street'; its links
    are the menu (Home, About, Horario de Misas, Photos, Staff, Contact Us) and no bulletin file.
- url: https://sanjosepaterson.org/mass-times
  seen: 2026-11-05
  quote: 12:00 PM Spanish Choir A
  note: 'Horario de Misas page: Sunday 9:30 AM Spanish and 12:00 PM Spanish; Monday-Friday 7:00 PM Spanish;
    Saturday 12:00 PM Spanish. Footer ''St. Joseph Catholic Church, 399 Market Street, Paterson, NJ, 07501''.'
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: Finder pin directory:11440 'St. Joseph, Paterson', 399 Market Street, Paterson 07501, website
    https://sanjosepaterson.org/; same Mass times.
revisit: Reload https://sanjosepaterson.org/bulletins with visit.py and probe files.ecatholic.com/11440/bulletins/<Sunday>.pdf;
  if issues appear, set provider ecatholic, publication ecatholic:11440, and run fetch:check.
revisit_after: 2027-02-01
research:
- method: parish-site-access visit.py on /bulletins (text and link list) and the home page (--bulletin,
    link list)
  url: https://sanjosepaterson.org/bulletins
  checked: '2026-11-05'
  outcome: not-found
  next_action: Reload the /bulletins page and its Archive
  retry_when: On the revisit date, or when the site or finder links a bulletin
- method: 'issues.py ecatholic ecatholic:11440: every Sunday 4 Oct - 8 Nov 2026, Saturdays 17 Oct - 7
    Nov 2026, and 2 Aug, 30 Aug, 27 Sep 2026 (all 403, not posted)'
  url: https://files.ecatholic.com/11440/bulletins/20261108.pdf
  checked: '2026-11-05'
  outcome: not-found
  next_action: Probe the coming Sundays' file names again
  retry_when: On the revisit date
bulletin_status: not-found
---

## Publisher

No bulletin found. St. Joseph, Paterson runs an eCatholic site (site id 11440, the finder pin id) whose Bulletin page, read 2026-11-05 with parish-site-access visit.py, shows the headings "Bulletin" and "Archive" and no issues; the site menu has seven pages and none is a bulletin. `files.ecatholic.com/11440/bulletins/<YYYYMMDD>.pdf` answered 403 (not posted) for every Sunday 4 October - 8 November 2026, Saturday-dated names, and three Sundays August-September 2026. See `research`.

## Worship sites

One church, `st-joseph-paterson` (399 Market Street), whose Horario de Misas page (2026-11-05) lists Sunday 9:30 AM and 12:00 PM, Monday-Friday 7:00 PM and Saturday 12:00 PM, all in Spanish. The finder (directory:11440) and GCatholic (19006) list this one church; the OSM school beside it (Saint Joseph's School, Olive Street) is not a worship site.

## Website and bulletin provider

`https://sanjosepaterson.org/` (the finder's website; eCatholic behind Cloudflare). Provider `no_bulletin`: public Mass but no bulletin posted, so promote keeps the row and its church off the site until one turns up. If issues appear they will be `ecatholic:11440`.

## Not yet confirmed

Whether the parish prints a bulletin it doesn't post (the office, 973-278-0030, could say). The revisit on 2027-02-01 rereads the Bulletin page and the eCatholic file names.
