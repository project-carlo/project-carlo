---
name: St. Anthony – St. Alphonsus (Greenpoint)
website: https://stanthony-stalphonsus-brooklyn.org/
bulletin_provider: other
provider_id: page-pdfs https://stanthony-stalphonsus-brooklyn.org/bulletins
publication: []
group: Deanery B1 (Brooklyn West)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMzAvOTVhNnNsdHV6N19BbnRob255QWxwam9uc3VzMTFfMS5wZGYiXV0/AnthonyAlpjonsus11-1.pdf
  seen: 2026-11-07
  quote: '#110  FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY 11704-1104'
  note: '1 November 2026 issue (8 pages). Page 1: ''Rectory: 862 Manhattan Avenue Brooklyn, New York 11222'',
    website stanthony-stalphonsus-brooklyn.org, Pastor Rev. Mukalel J. Benny, CMI; one Mass Schedule (Mon-Fri
    9:30am; Mon, Wed, Thurs 12:30 pm; Friday 7:30 pm Spanish; Saturday 9:30 am & 5:30 pm; Sunday 9:30
    am, 11:00 am Spanish, 12:30 pm); ''Solemnity of All Saints November 1st, 2026''. Page 2 intentions
    31 Oct to 6 Nov. Page 8 footer is the quote.'
- url: https://stanthony-stalphonsus-brooklyn.org/bulletins
  seen: 2026-11-07
  quote: Bulletin for Sunday, November 1st, 2026
  note: Tilma /bulletins, cards newest first (1 Nov, 25 Oct, 18 Oct, 11 Oct, 4 Oct 2026 ...), each linking
    a files.tilmaplatform.com PDF; the 1 Nov file's token decodes to an upload on 2026/10/30.
- url: https://parishesonline.com/organization/st-anthony-st-alphonsus-church
  seen: 2026-11-07
  note: 'probe po: LPi org ''St. Anthony / St. Alphonsus Church'' (lpi 0018000000QxB7gAAF), 862 Manhattan
    Ave, website stanthony-stalphonsus-brooklyn.org, with no publications. Not a publication id: the bulletin
    is printed by The Church Bulletin Inc.'
revisit: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later (the newest posted
  on 2026-11-12 was older than 8 November).
revisit_after: 2026-11-17
research:
- method: fetch:check other page-pdfs on the Tilma /bulletins page
  url: https://stanthony-stalphonsus-brooklyn.org/bulletins
  checked: '2026-11-07'
  outcome: found
- method: 'Reconcile: headed fetch:check of every Brooklyn row picked the issue dated 2026-11-01; the
    bulletin page lists no newer issue than the one picked'
  url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMzAvOTVhNnNsdHV6N19BbnRob255QWxwam9uc3VzMTFfMS5wZGYiXV0/AnthonyAlpjonsus11-1.pdf
  checked: '2026-11-12'
  outcome: not-found
  next_action: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later
  retry_when: After the weekend of 14-15 November 2026
bulletin_status: available
---

## Publisher

St. Anthony – St. Alphonsus posts a weekly bilingual (English/Spanish) bulletin printed by The Church Bulletin Inc. on its Tilma site. I read the 1 November 2026 issue (read 2026-11-07): page 1 gives the rectory at 862 Manhattan Avenue, the parish website and "Rev. Mukalel J. Benny, CMI" as pastor, with one Mass schedule; page 8's footer reads "#110 FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY". The Church Bulletin Inc. has no online container, so there is no publication id. An LPi org `st-anthony-st-alphonsus-church` exists for the parish but has no issues, so it is not recorded as a publication.

## Worship sites

One church, 862 Manhattan Avenue. The page 1 schedule (Mon-Fri 9:30 am; Mon, Wed, Thu 12:30 pm; Friday 7:30 pm Spanish; Saturday 9:30 am and 5:30 pm; Sunday 9:30 am, 11:00 am Spanish, 12:30 pm) names no other building, and the site's Mass Times page gives the same times.

Ruled out:

- Holy Family, 21 Nassau Avenue (GCatholic 16609). The archives list says Holy Family, Greenpoint "Merged with St. Anthony St. Alphonsus, 2011", but this bulletin never mentions it (searched the 1 November issue for "Holy Family", "Nassau", "Damiano" and "Shalom"). The building is now San Damiano Mission, run by the Shalom Catholic Community with its own schedule and no bulletin: `excluded/san-damiano-mission-greenpoint`.
- St. Alphonsus church on Kent Street, closed in 1975 (archives list), now a Polish and Slavic cultural center (The Tablet, 2018). No roster lists it.

## Website and bulletin provider

`other`, `page-pdfs https://stanthony-stalphonsus-brooklyn.org/bulletins`. Issues are uploaded a day or two before their Sunday (1 November on 30 October).

`fetch:check` (2026-11-07) resolved "page-pdfs on https://stanthony-stalphonsus-brooklyn.org/bulletins: current" and picked `AnthonyAlpjonsus11-1.pdf`, the 1 November 2026 issue (issue date observed, freshness `fresh`; identity `unverified`, which I checked by reading its page 1). The 8 November issue was not yet posted on the Saturday I checked.

## Not yet confirmed

Nothing open.
