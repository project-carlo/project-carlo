---
name: St. Sebastian (Woodside)
website: https://saintsebastianwoodside.org/
bulletin_provider: parishes_online
provider_id: st-sebastian-church-11377
publication: ['po-org:st-sebastian-church-11377', 'lpi:0018000000QxB9fAAF', 'po-container:03/4071']
group: Deanery Q2 (Queens West)
evidence:
- url: https://container.parishesonline.com/bulletins/03/4071/20261108B.pdf
  seen: 2026-11-06
  quote: Saint Sebastian Roman Catholic Church
  note: '8 November 2026 issue, 12 pages. Page 1 masthead: ''58–02 Roosevelt Ave, Woodside, NY 11377'',
    ''Rectory: 39–63 57th Street'', Schedule of Masses (Sat 5:00pm English, 6:30pm Español; Sun 8:30am,
    10:30am, 12:00pm Español, 1:30pm, 6:00pm; Mon-Fri 9:00am, 12:00pm; Sat 9:00am, 12:00pm Español). Below
    it, a contact block for ''Corpus Christi Roman Catholic Church'', 31–30 61st Street, website ccwoodsideny.org,
    with no Mass times. Page 10 ''Parish Mass Schedule November 14-15'' lists celebrants for St. Sebastian
    and for Corpus Christi (Sun 8:45 AM, 11:00 AM, 12:30 PM). Page 11-12 footer ''St. Sebastian Church
    | 03-4071''.'
- url: https://parishesonline.com/organization/st-sebastian-church-11377
  seen: 2026-11-06
  note: 'probe po: org ''St. Sebastian Church'', lpi 0018000000QxB9fAAF, container 03/4071, website saintsebastianwoodside.org,
    address 58-02 Roosevelt Avenue, Queens 11377; weekly issues 2026-10-04 to 2026-11-08.'
- url: https://saintsebastianwoodside.org/bulletin-3/
  seen: 2026-11-06
  quote: ss-20261101B_s.pdf
  note: 'Parish site''s bulletin page (WordPress, dFlip flipbook, titled ''Parish Bulletin – November
    1st, 2026'') shows the LPi file ss-20261101B_s.pdf, whose footer reads ''St. Sebastian Church | 03-4071'':
    a repost of the container issue.'
research:
- method: probe po st-sebastian-church-11377; probe container 03/4071
  url: https://parishesonline.com/organization/st-sebastian-church-11377
  checked: '2026-11-06'
  outcome: found
- method: fetch:check parishes_online org st-sebastian-church-11377 (picked 20261108B.pdf, this weekend's
    issue)
  url: https://container.parishesonline.com/bulletins/03/4071/20261108B.pdf
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
publication_reviews:
- parish: corpus-christi-woodside
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/4071/20261108B.pdf
    seen: 2026-11-06
    note: The 8 November 2026 masthead (page 1) names Saint Sebastian Roman Catholic Church, 58-02 Roosevelt
      Ave, with St. Sebastian's schedule alone (weekdays 9:00 am and 12:00 pm) and St. Sebastian's intentions
      on page 3; Corpus Christi appears only as a contact block and in the page 10 celebrant list.
  - url: https://container.parishesonline.com/bulletins/03/9001/20261108B.pdf
    seen: 2026-11-06
    note: The 8 November 2026 masthead (page 1) names Corpus Christi Roman Catholic Church, 31-30 61st
      Street, with its own Mass schedule (Sunday 8:45, 11:00, 12:30; Mon-Sat 8:00 am) and its own weekday
      intentions; St. Sebastian appears only 'In Partnership With' as a contact block.
---

## Publisher

St. Sebastian publishes a weekly LPi bulletin, ParishesOnline container 03/4071 under org `st-sebastian-church-11377` (lpi 0018000000QxB9fAAF). I read the 8 November 2026 issue (read 2026-11-06): page 1 masthead "Saint Sebastian Roman Catholic Church, 58–02 Roosevelt Ave, Woodside", "Rectory: 39–63 57th Street"; pages 11-12 footer "St. Sebastian Church | 03-4071". The parish site's bulletin page (`/bulletin-3/`, a dFlip flipbook) reposts the same LPi file (`ss-20261101B_s.pdf`, same footer).

Canonically this is the merged parish of St. Sebastian–Corpus Christi (the diocese's directory lists "St. Sebastian – Corpus Christi"; the academy note on page 2 says "St. Sebastian–Corpus Christi"), one pastor (Very Rev. Patrick J. West) for both churches. But Corpus Christi still publishes its own bulletin (LPi container 03/9001, its own masthead, weekday Masses and intentions), so under the settled Brooklyn rule it is its own row, `corpus-christi-woodside`, with a `separate` review below.

## Worship sites

One church, St. Sebastian, 58-02 Roosevelt Ave (`st-sebastian-woodside`). Page 1's Schedule of Masses is St. Sebastian's alone; the Corpus Christi block on page 1 gives only its address, phone and website. Page 10's celebrant list for 14-15 November covers both churches, as does Corpus Christi's own issue: the Corpus Christi church goes with the bulletin whose masthead and schedule are its own (`corpus-christi-woodside`). No mission or chapel is named.

## Website and bulletin provider

`parishes_online` with provider_id `st-sebastian-church-11377`; website is the parish site, which reposts the issues. `fetch:check` result is in research.

## Not yet confirmed

Nothing open.
