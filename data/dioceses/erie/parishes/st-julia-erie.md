---
name: St. Julia Parish
website: https://www.stjuliaerie.com
bulletin_provider: parishes_online
provider_id: st-julia-church
publication: ['po-org:st-julia-church', 'lpi:0018000000QxBkXAAV', 'po-container:14/1164']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/14/1164/20261025B.pdf
  seen: 2026-10-23
  quote: 3750 WEST LAKE ROAD
  note: 'Page 1 masthead of the 25 October 2026 issue (4 pages): ''Saint Julia Parish'', ''3750 WEST LAKE
    ROAD (RECTORY: 638 ROSLYN AVE.) ERIE, PENNSYLVANIA 16505'', ''ANTICIPATED MASS: SATURDAY, 4:00 PM
    / SUNDAY MASS: 9:00 AM / DAILY MASS: 8:00 AM MONDAY THROUGH FRIDAY''. Names St. Julia alone.'
- url: https://container.parishesonline.com/bulletins/14/1164/20261025B.pdf
  seen: 2026-10-23
  quote: 'SUNDAY MASS: 9:00 AM'
  note: 'Same masthead. Mass intentions: ''Sat. 31 Oct: (No Daily Mass, Sunday anticipated Mass at 4 p.m.)''
    and ''Anticipated Mass Saturday, Oct. 31 at 4 pm and Sunday, Nov. 1 at 9 am.'''
- url: https://www.stjuliaerie.com/
  seen: 2026-10-23
  note: The parish home page embeds the ParishesOnline bulletin widget with LPi id 0018000000QxBkXAAV
    (its link also reaches bulletins.html; curl of that page returned 0 bytes, 2026-10-23). probe po shows
    that organization is slug st-julia-church, 'St. Julia Parish', 3750 West Lake Rd., Erie 16505, container
    14/1164, latest issue 2026-10-25.
- url: https://www.eriercd.org/Parish10311-St-Julia.html
  seen: 2026-10-23
  note: 'Diocese directory record 10311 (also GCatholic 24526): one parish record, no mission, partner
    or secondary church. The directory''s mailing address is the rectory, 638 Roslyn Ave.'
- url: https://discovermass.com/church/saint-julia-erie-pa/
  seen: 2026-10-23
  quote: no bulletins available
  note: A Discover Mass page exists for St. Julia but carries no bulletin ('no bulletins available' in
    the copy of the page saved by the survey on 2026-10-23), so the ParishesOnline container is the only
    live channel.
promoted: 2026-10-23
research:
- method: pnpm fetch:check --diocese erie --parish st-julia-erie --expected-identity 'Saint Julia' --expected-issue-date
    2026-10-25 (headed Chrome)
  url: https://parishesonline.com/publication-page/st-julia-church
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF (container 14/1164, 20261025B.pdf), identity matched on page 1,
    issue date observed as 2026-10-25; freshness reads 'future' only because the Sunday issue is posted
    two days early on the reference date 2026-10-23.
---

## Publisher

St. Julia Parish, Erie publishes its own weekly bulletin through ParishesOnline (organization st-julia-church, container 14/1164). I read the 25 October 2026 issue on 2026-10-23: the masthead names 'Saint Julia Parish' with the very Rev. Nicholas J. Rouch, S.T.D., V.G. as pastor and Deacon Jerome Peterson, and the content is about this parish only. The directory shows one parish record (10311) with no partner or secondary church, and Rouch is not among the multi-parish pastors summarised from the clergy PDF in diocese.md (I did not reread the PDF; the bulletin's staff list names only this parish).

## Worship sites

One church, St. Julia at 3750 West Lake Road. The masthead gives Saturday 4:00 PM anticipated Mass, Sunday 9:00 AM, and daily Mass 8:00 AM Monday through Friday (no daily Mass on Saturdays). The bulletin's references to St. Jude the Apostle Church (faith formation for grades 6-12, 814-833-0927) are to a different parish, outside this batch.

## Website and bulletin provider

The directory's website `http://www.stjuliaerie.com` resolves (200, redirect to https://www.stjuliaerie.com/), and its Bulletins page embeds the ParishesOnline widget for LPi 0018000000QxBkXAAV; `probe po` shows that is organization st-julia-church (title 'St. Julia Parish', 3750 West Lake Rd.), container 14/1164, with weekly issues through 2026-10-25. All three ids are one bulletin.

## Address note

The directory puts the parish at 3750 West Lake Rd. but its mailing address and GCatholic say 638 Roslyn Ave. The bulletin masthead resolves it: 3750 West Lake Road is the church and 638 Roslyn Ave. is the rectory. OpenStreetMap agrees: a place_of_worship way 'Saint Julia Catholic Church' at 3750 West Lake Road, and a separate building at 638 Roslyn Avenue about 55 m west.

## Not yet confirmed

Nothing open for the row itself.
