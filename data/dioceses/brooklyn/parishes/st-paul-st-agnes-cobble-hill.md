---
name: St. Paul & St. Agnes (Cobble Hill)
website: https://stpaulstagnes-brooklyn.org/bulletins
bulletin_provider: other
provider_id: page-pdfs https://stpaulstagnes-brooklyn.org/bulletins
publication: ['url:https://stpaulstagnes-brooklyn.org/bulletins']
group: Deanery B3 (Brooklyn West)
evidence:
- url: https://stpaulstagnes-brooklyn.org/system/resources/W1siZiIsIjIwMjYvMTAvMDUvMWZlaTF3emNoM18yN3RoX1N1bmRheV9PVF8yMDI2LnBkZiJdXQ/27th%20Sunday%20OT%202026.pdf
  seen: 2026-11-06
  note: '4 October 2026 issue, ''27th Sunday in Ordinary Time'' (2 pages, images; read with render.py).
    Page 1 masthead ''Saint Paul and Saint Agnes'', ''One parish - Two churches'': Saint Paul, 234 Congress
    Street, Brooklyn, NY 11201, Est. 1836; Saint Agnes, 433 Sackett Street, Brooklyn, NY 11231, Est. 1878.
    Mass schedule: Saint Paul Monday through Saturday 12 noon, Saturday 5:30 PM Vigil, Sunday 10:45 AM
    (French); Saint Agnes Sunday 10:30 AM (English, ''NEW TIME! As of OCT 04'') and 12:15 PM (Spanish).
    Pastor Rev. Fr. Paul Anel. Self-made issue, no publisher footer.'
- url: https://stpaulstagnes-brooklyn.org/bulletins
  seen: 2026-11-06
  quote: October 04, 2026
  note: 'Tilma bulletins page, cards ''<Month DD, YYYY>'' newest first: October 04, 2026; September 06,
    2026; June 28, 2026; May 31, 2026; August 17, 2025; August 10, 2025 ... The parish posts issues irregularly,
    not weekly.'
- url: https://parishesonline.com/organization/st-paul-st-agnes-church-11201
  seen: 2026-11-06
  note: probe po on st-paul-st-agnes-church-11201, st-paul-and-st-agnes-11201 and st-paul-church-11201
    found no org.
revisit: Check /bulletins for an issue after 4 October 2026; if none is posted by mid-December, consider
  no_bulletin per the playbook's stale-Tilma rule.
revisit_after: 2026-11-20
research:
- method: fetch:check page-pdfs on the Tilma /bulletins page
  url: https://stpaulstagnes-brooklyn.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Re-run fetch:check and read the newest card's date; if an issue newer than 4 October 2026
    is posted, the row is current; if none by mid-December 2026, record no_bulletin with bulletin_status
    not-found, keeping this recipe in next_action.
  retry_when: After the weekend of 14-15 November 2026
  revisit_after: 2026-11-20
bulletin_status: available
---

## Publisher

The parish publishes its own bulletin (no publisher footer) and posts it on its Tilma site's /bulletins page. The newest issue posted, 4 October 2026 (27th Sunday in Ordinary Time, 2 image pages, read 2026-11-06 with render.py), has the masthead "Saint Paul and Saint Agnes", "One parish - Two churches", with Saint Paul, 234 Congress Street, and Saint Agnes, 433 Sackett Street, and Rev. Fr. Paul Anel as Pastor.

## Worship sites

Two churches, both in the 4 October 2026 Mass schedule: Saint Paul (Monday-Saturday 12 noon, Saturday 5:30 PM vigil, Sunday 10:45 AM in French) and Saint Agnes (Sunday 10:30 AM English, new time as of 4 October, and 12:15 PM Spanish). The diocese's directories list the parish once, at St. Paul's 234 Congress Street; GCatholic lists both churches (16763, 16770); the Mass finder lists St. Agnes (792).

## Website and bulletin provider

`other`, `page-pdfs https://stpaulstagnes-brooklyn.org/bulletins`: the Tilma page lists date cards ('October 04, 2026 / Download') newest first, with PDFs under `<site>/system/resources/<token>/`. `fetch:check` (2026-11-06) picked the first-listed card, the 4 October 2026 issue, with freshness unknown. The issues are images only, so the pipeline has to read them as images.

## Not yet confirmed

Whether the bulletin is still weekly. The site posts it irregularly: 4 October, 6 September, 28 June and 31 May 2026, then August 2025. On 2026-11-06 the newest issue was about five weeks old, so fetch picks a past issue. It is recorded as `other` because that issue is recent and its schedule is the current one (the St. Agnes time change took effect 4 October). The research item and `revisit_after` 2026-11-20 schedule a recheck. If nothing newer is posted by mid-December, apply the playbook's stale-Tilma rule (no_bulletin, not-found). No ParishesOnline org was found.
