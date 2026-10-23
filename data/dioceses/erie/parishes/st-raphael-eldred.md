---
name: St. Raphael Parish
website: https://www.straphaeleldred.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.straphaeleldred.org/weeklybulletin.php
  seen: 2026-10-23
  quote: No Bulletin found.
  note: The parish's diocese-hosted site (St. Raphael, Eldred Parish; 16 First St.; trams3@hotmail.com;
    (814) 225-4231) has a Weekly Bulletin page that says 'No Bulletin found.' The home page's Latest News
    also says 'No News Found'. The site has no other bulletin link; its header links a Facebook page (St-Raphael-Parish-Missions-St-Mary-and-St-Theresa-881024421977940),
    which showed only a login wall.
- url: https://parishesonline.com/organization/st-raphael-church-16731
  seen: 2026-10-23
  note: 'probe po st-raphael-church-16731 (LPi 0018000000QxBkpAAF, 16 1st St, Eldred; website the parish
    site): ''no publications: this organization does not publish a bulletin here now''. st-therese-church-16748
    (LPi 0018000000QxBksAAF, 105 S Puritan St, Shinglehouse; same website): the same.'
- url: https://discovermass.com/church/st-raphael-eldred-pa/
  seen: 2026-10-23
  quote: There are currently no bulletins available for St Raphael.
  note: The pages for St. Mary (saint-mary-sartwell-pa) and St. Theresa (st-theresa-shinglehouse-pa) say
    the same for their own names.
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Brown, Rev. Thomas E.
  note: 'Clergy list updated 8/7/2026: ''Brown, Rev. Thomas E. / Pastor ... St. Raphael, Eldred'' (one
    assignment). Funeral notices for 2025-2026 name him as celebrant at St. Raphael and St. Theresa.'
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  note: 'Printable directory dated 6 Oct 2026, Eldred: St. Raphael Parish, 16 First St., ''Daily: Monday,
    Tuesday, Wednesday, and first Friday at 9 a.m. - St. Raphael, Eldred; Thursday at 9 a.m. - St. Theresa,
    Shinglehouse; Saturday: 4:30 p.m.; Sunday: 9 a.m. - St. Mary, Eldred''; secondary missions St. Mary
    Church (630 Newell Creek Road; Sunday 9 a.m.) and St. Theresa Church (111 S. Puritan St., Shinglehouse;
    Sunday 11 a.m.).'
- url: https://www.eriercd.org/images/sections/bishop/pdf/DECREE_MergingSt.TheresaShinglehouseintoSt.RaphaelEldred.pdf
  seen: 2026-10-23
  quote: EFFECTING THE MERGER OF SAINT THERESA PARISH (SHINGLEHOUSE)
  note: 'Merger decree (2016, effective 13 Feb 2017): St. Theresa Parish merged into St. Raphael Parish,
    Eldred; the decree describes St. Raphael as having ''its mission in Sartwell'' (St. Mary). Structure
    only; no bulletin.'
revisit: Look again for a bulletin channel for St. Raphael, Eldred (weeklybulletin.php, ParishesOnline,
  Discover Mass, parish Facebook page)
revisit_after: 2027-01-15
research:
- method: curl of https://www.straphaeleldred.org/weeklybulletin.php and the home, About Us, Calendar
    and Sacraments pages; probe url; probe po on ParishesOnline orgs st-raphael-church-16731 and st-therese-church-16748
    (found by the search API at the church coordinates); Discover Mass pages st-raphael-eldred-pa, saint-mary-sartwell-pa,
    st-theresa-shinglehouse-pa; DuckDuckGo searches in headed Chrome for the parish name plus 'bulletin';
    the parish Facebook page link from the site header
  url: https://www.straphaeleldred.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: not-found
  next_action: Check the Facebook page by a public post URL (the page opens only a login wall in headed
    Chrome), or ask the parish office at (814) 225-4231; re-run probe po for the two orgs
  retry_when: weeklybulletin.php lists a PDF, either ParishesOnline org shows an issue, a Discover Mass
    page lists a bulletin, or a public Facebook post links a bulletin
bulletin_status: not-found
---

## Publisher

No bulletin was found for St. Raphael Parish, Eldred, or its two missions. The parish's diocese-hosted site (straphaeleldred.org) has a Weekly Bulletin page that says 'No Bulletin found.'; the two ParishesOnline organizations that carry its churches' addresses (`st-raphael-church-16731`, `st-therese-church-16748`) publish nothing; Discover Mass pages for St. Raphael, St. Mary (Sartwell) and St. Theresa say 'no bulletins available'; web searches (2026-10-23) found only aggregator Mass-time pages. The parish's Facebook page (linked from its site) shows a login wall to the sandbox browser, so it may carry a bulletin that was not seen. This row is `no_bulletin`: kept in the records with its three churches, left off the site (settled policy 4). It is not evidence that no bulletin exists.

## Worship sites

Three churches with public Mass under one pastor (Rev. Thomas E. Brown): St. Raphael, 16 First St., Eldred (parish church); St. Mary, 630 Newell Creek Rd., in the hamlet of Sartwell (directory and GCatholic file it under Eldred; Sunday 9 a.m.); and St. Theresa, 111 S. Puritan St., Shinglehouse (merged into St. Raphael in 2017; Sunday 11 a.m., Thursday 9 a.m.). Mass times are the diocese directory's only. Public Masses at St. Raphael and St. Theresa are corroborated by funeral notices (Donald A. Colebert, funeral Mass at St. Raphael on 17 April 2026, legacy.com / Mascho Funeral Home; Robert Brooks, funeral Mass at St. Theresa on 10 June 2025, Wellsville Regional News). No 2026 funeral notice for St. Mary, Sartwell, was found; see its church record.

## Website and bulletin provider

`no_bulletin`. `website` is the parish's own diocese-hosted site.

## Not yet confirmed

A bulletin channel. Retry on the trigger in `research`.
