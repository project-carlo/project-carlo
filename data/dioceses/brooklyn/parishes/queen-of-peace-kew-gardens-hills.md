---
name: Queen of Peace (Kew Gardens Hills)
website: https://queenofpeace-queens.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q7 (Queens East)
evidence:
- url: https://queenofpeace-queens.org/bulletins
  seen: 2026-11-06
  quote: NOTHING TO SHOW
  note: Tilma (webstudio) site; rendered with visit.py, the 'Our Bulletins' section shows 'NOTHING TO
    SHOW'. The page data embedded in the homepage gives the 'Bulletins' collection (id 5116) with totalCount
    0.
- url: https://queenofpeace-queens.org/mass-times
  seen: 2026-11-06
  quote: Sunday, 8:30AM & 11:00AM
  note: 'Mass Times page (rendered with visit.py): Saturday Vigil 4:00PM; Sunday 8:30AM & 11:00AM; weekdays
    Monday-Saturday 8:30AM; ''Misa en español todos los viernes.'' Footer: Queen of Peace, 141-36 77th
    Avenue, Flushing, NY 11367.'
- url: https://parishesonline.com/organization/queen-of-peace-church-11367
  seen: 2026-11-06
  note: 'probe po: org ''Queen of Peace Church'' (lpi 0018000000Qc02IAAR, 141-36 77th Ave) newest issue
    2022-11-19 (file 03-00573112022.pdf, container 03/0057). probe container 03/0057 found no issue in
    the 12 Sundays to 2026-11-08 (all 403), while the same probe found 20261108B.pdf in live container
    04/0247: the LPi bulletin stopped in November 2022.'
revisit: Recheck https://queenofpeace-queens.org/bulletins and the ParishesOnline org for a bulletin
revisit_after: 2026-12-07
research:
- method: visit.py on the Tilma bulletins page and homepage; probe po queen-of-peace-church-11367; probe
    container 03/0057 with a live-container control; Discover Mass church pages queen-of-peace-flushing-ny
    and queen-of-peace-kew-gardens-hills-ny (404); GCatholic's queenofpeacechurch.org (DEAD-DNS)
  url: https://queenofpeace-queens.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Reload the Tilma bulletins page and probe po queen-of-peace-church-11367; if a bulletin
    appears, set provider (Tilma page-pdfs or parishes_online) and run fetch:check. The parish Facebook
    page (facebook.com/Queen-of-Peace-Kew-Gardens-Hills-New-York-103118264674820) was not read and may
    post bulletins.
  retry_when: The site's Bulletins collection lists an issue, or a later check of the Facebook page finds
    bulletins
  revisit_after: 2026-12-07
bulletin_status: not-found
---

## Publisher

No current bulletin found (checked 2026-11-06). The parish's Tilma site has an "Our Bulletins" section that renders "NOTHING TO SHOW"; the page data in the homepage gives its Bulletins collection a totalCount of 0. Its ParishesOnline org `queen-of-peace-church-11367` (LPi container 03/0057) has issues only up to 19 November 2022, and `probe container 03/0057` found none in the 12 Sundays to 8 November 2026 while the same probe found the current issue of live container 04/0247. Discover Mass has no page under the obvious slugs (404), and GCatholic's website `queenofpeacechurch.org` no longer resolves. The 2022 org and container are recorded in evidence, not as publication ids, since they are not a current bulletin.

## Worship sites

One church, Queen of Peace, 141-36 77th Avenue. The site's Mass Times page (read 2026-11-06) gives Saturday Vigil 4:00PM, Sunday 8:30AM & 11:00AM, Monday-Saturday 8:30AM, and names no other place. The diocese directory, the deanery list (Q7), GCatholic 16658 and Mass finder 142 list this one church.

## Website and bulletin provider

`no_bulletin` (Settled policy 4: kept in the records, left off the site). The website is the Tilma bulletins page, where issues would appear; Tilma pages list cards newest first, so `page-pdfs https://queenofpeace-queens.org/bulletins` is the likely recipe if they do.

## Not yet confirmed

The parish Facebook page was not read; it may post a bulletin or weekly announcements. See `research` and the revisit on 2026-12-07.
