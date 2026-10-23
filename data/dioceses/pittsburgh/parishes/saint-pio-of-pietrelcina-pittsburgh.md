---
name: Saint Pio of Pietrelcina Parish
website: https://padrepioparish.org
bulletin_provider: parishes_online
provider_id: st-pio-of-pietrelcina-15201
publication: ['po-org:st-pio-of-pietrelcina-15201', 'lpi:0018000000Qc005AAB', 'po-container:14/0730',
  'po-org:st-maria-goretti-parish', 'lpi:001C00000107BF1IAM']
group: Saint Pio of Pietrelcina Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/0730/20261025B.pdf
  seen: 2026-10-23
  quote: St. Pio of Pietrelcina, Pittsburgh, PA 14-0730
  note: 'LPi ad-page footer (pages 15-16) of the 25 October 2026 issue, container 14/0730, 16 pages. Pages
    1-14 are images with no text layer, so the masthead is not quotable. Rendered page 1 (read 2026-10-23):
    cover headed ''ST. PIO OF PIETRELCINA PARISH OF THE CENTRAL DEANERY'', ''OCTOBER 25 | 2026 THIRTIETH
    SUNDAY IN ORDINARY TIME'', footer ''Parish Office: 225-37th St Pgh 15201 | Saint Augustine Church:
    234-37th St Pgh 15201''.'
- url: https://container.parishesonline.com/bulletins/14/0730/20261025B.pdf
  seen: 2026-10-23
  note: 'Rendered page 3 ''SUNDAY EXPERIENCE / Liturgy Schedule & Priest Intentions'': Saturday 24 Oct
    4:00 pm Fr. Joseph; Sunday 25 Oct 8:00 am, 9:30 am, 11:30 am; weekday Masses 6:30 am (Mon-Fri; Tuesday
    and Thursday with novenas), 11:30 am (Mon-Fri and Sat) and 6:30 pm (Tue, Wed, Thu); Saturday 31 Oct
    4:00 pm. One intentions list for the whole parish, no church named. Page 2 is a First Friday Mass
    and Holy Hour flyer (Friday 6 November, 6:30 PM Mass) giving ''St Padre Pio Parish 225 37th St., Pittsburgh,
    PA 15201''.'
- url: https://parishesonline.com/organization/st-pio-of-pietrelcina-15201
  seen: 2026-10-23
  note: 'probe po: org ''St. Pio of Pietrelcina Parish'' (lpi 0018000000Qc005AAB, 225 37th Street, website
    www.padrepioparish.org), container 14/0730, latest issue 2026-10-25. The old org st-maria-goretti-parish
    (lpi 001C00000107BF1IAM, title ''CLOSED PERMANENTLY'', 4712 Liberty Avenue) lists the same issues
    in the same container: a predecessor account for the same bulletin, so both are recorded.'
- url: https://padrepioparish.org/
  seen: 2026-10-23
  note: 'Read in headed Chrome (visit.py --bulletin; probe url gets 403): diocese-provided eCatholic site
    (ecatholic:22384, which is also the id of the address-less Mass Finder pin ''St. Padre Pio Parish'').
    Its ''Bulletins'' link goes to the ParishesOnline org st-pio-of-pietrelcina-15201 (publications reported:
    po-org:st-pio-of-pietrelcina-15201, ecatholic:22384), so the bulletin is on ParishesOnline; ecatholic:22384
    is not recorded as a publication id.'
- url: https://diopitt.org/saint-pio-of-pietrelcina-parish
  seen: 2026-10-23
  note: 'Diocese parish page (read in headed Chrome for the directory roster; diopitt.org answers 403
    to recheck): one church, Saint Augustine Church (Lawrenceville), 234 37th Street, Saturday Vigil 4:00
    p.m., Sunday 8:00, 9:30, 11:30 a.m.; Reverend Paul Zaborowski, O.F.M. Cap. (Administrator); phone
    412-682-0929. Matches the bulletin.'
- url: https://diopitt.org/saint-maria-goretti
  seen: 2026-10-23
  quote: This ended on January 1, 2024 when St. Maria Goretti Parish merged with Our Lady of the Angels
    Parish, Lawrenceville to form the new St. Pio of Pietrelcina Parish.
  note: 'Diocese history page (headed Chrome; diopitt.org 403s recheck): the parish''s two predecessors.'
research:
- method: 'probe po st-matthew-church-15201 (lead from scout 13: 5322 Carnegie St, Pittsburgh 15201);
    DuckDuckGo search on the address'
  url: https://parishesonline.com/organization/st-matthew-church-15201
  checked: '2026-10-23'
  outcome: not-found
  next_action: 'None for this row: the org has no container and no issues, so it identifies no bulletin;
    search results call 5322 Carnegie St a former St. Matthew (Lawrenceville) parish, ''CLOSED'' on Mass
    Times USA, and appear in no roster here.'
  retry_when: The org gains a container or a bulletin names a church at 5322 Carnegie St
bulletin_status: available
---

## Publisher

Saint Pio of Pietrelcina Parish (formed 2024-01-01 from Our Lady of the Angels, Lawrenceville and St. Maria Goretti, Bloomfield, per the diocese's history page) publishes one weekly bulletin on ParishesOnline container 14/0730. Read 2026-10-23: the 25 October 2026 issue (16 pages) is image pages with a cover headed 'ST. PIO OF PIETRELCINA PARISH OF THE CENTRAL DEANERY'; only the two ad pages have a text layer, and their footer reads 'St. Pio of Pietrelcina, Pittsburgh, PA 14-0730'. The parish's own site links the ParishesOnline org. Two LPi orgs resolve to the container (the parish's and the 'CLOSED PERMANENTLY' St. Maria Goretti account); both are one bulletin. One row, one church.

## Worship sites

One church: Saint Augustine, Lawrenceville (234 37th St by the directory and the cover; the parish office at 225 37th St is the same block and GCatholic's address for the church). The Mass schedule on page 3 prints times with no church names, matching the directory's weekend times for Saint Augustine. The parish's three predecessor-parish buildings in Bloomfield and Garfield are all closed (St. Joseph, Immaculate Conception, St. Lawrence O'Toole: see excluded records). Our Lady of the Angels is the parish's predecessor in Lawrenceville and its building is St. Augustine's. The Mass Finder's address-less 'St. Padre Pio Parish' pin (massfinder:22384, the parish's eCatholic id) is parish-level and was deliberately left unlinked.

## Website and bulletin provider

padrepioparish.org is a diocese-provided eCatholic site (id 22384) behind Cloudflare; the bulletin lives on ParishesOnline (provider_id st-pio-of-pietrelcina-15201). The fetch check result is in scratch/map-pittsburgh/scouts/20/manifest.json.

## Not yet confirmed

The issue is image-only, so `recheck` can find only the ad-page footer. The weekly Mass times were read from the rendered page 3 image.
