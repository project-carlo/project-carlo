---
name: St. Cecilia, Englewood
website: https://www.stceciliachurch.com/
bulletin_provider: parishes_online
provider_id: st-cecilia-church-07631
publication: ['po-org:st-cecilia-church-07631', 'lpi:0018000000QxABsAAN', 'po-container:03/4014']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/4014/20261101B.pdf
  seen: 2026-11-03
  quote: Ministered to by the Carmelites
  note: '1 November 2026 LPi issue (4 pages, text layer). Page 1 masthead ''ST. CECILIA CHURCH'', ''Parish
    Office: 55 W. Demarest Avenue Englewood, NJ 07631'', ''November 1, 2026''; Mass schedule Monday -
    Saturday 8:30AM, Saturday 5:00 PM Vigil, Sunday 9:00 AM, 11:00 AM Spanish, 1:00 PM Spanish, 6:00 PM;
    served by Rev. Roberto Mejia, O. Carm., Administrator. Page 4 footer ''St. Cecilia Church | 03-4014''.
    No other church named; ''Fairview'' and ''Baptist'': 0 hits.'
- url: https://parishesonline.com/organization/st-cecilia-church-07631
  seen: 2026-11-03
  note: 'probe po: ''St. Cecilia Church'', 55 W Demarest Ave, Englewood, New Jersey 07631, website https://stceciliachurch.com/,
    ids lpi:0018000000QxABsAAN and po-container:03/4014; issues 1 Nov, 25 Oct, 18 Oct, 11 Oct 2026.'
- url: https://www.stceciliachurch.com/bulletins
  seen: 2026-11-03
  note: eCatholic site (id 25501) bulletin archive, not linked from the site's menus, stops at March 13,
    2022 (files.ecatholic.com/25501/bulletins/20220313.pdf, a J.S. Paluch issue, ad-page footer '511331
    St Cecilia Church'). issues.py found no eCatholic issue for 18 Oct-8 Nov 2026.
- url: https://container.parishesonline.com/bulletins/03/4014/20230604B.pdf
  seen: 2026-11-03
  note: 'Earliest issue in container 03/4014 (probe container: 4 June 2023 answers 200, every Sunday 9
    April-28 May 2023 answers 403 while the container is live). No mention of Fairview or St. John the
    Baptist (grep: 0 hits).'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

LPi prints St. Cecilia's weekly bulletin (ParishesOnline container 03/4014, org `st-cecilia-church-07631`). I read the 1 November 2026 issue: page 1 masthead 'ST. CECILIA CHURCH', 'Faith and Good Works Since 1866', 'Ministered to by the Carmelites', parish office 55 W. Demarest Avenue, Englewood, 'November 1, 2026', one Mass schedule, Rev. Roberto Mejia, O. Carm., Administrator; page 4 footer 'St. Cecilia Church | 03-4014'.

An earlier lead asked whether St. Cecilia's 2023 issues show a shared schedule with St. John the Baptist, Fairview (whose temporary administrator came from St. Cecilia in January 2023). Neither archive covers that period: the eCatholic archive ends 13 March 2022 (then printed by J.S. Paluch, code 511331), and LPi container 03/4014 starts 4 June 2023. The 4 June 2023 and 1 November 2026 issues don't mention Fairview. Fairview now has its own pastor and bulletin, so this doesn't affect either row.

## Worship sites

- St. Cecilia, 55 West Demarest Avenue (`st-cecilia-englewood`): Saturday 5:00pm vigil; Sunday 9:00am, 11:00am (Spanish), 1:00pm (Spanish), 6:00pm; Monday-Saturday 8:30am.

The directory (41) and GCatholic (18400) list only this church. The 'Office of Concern' at 85 West Demarest Avenue (rear) in the masthead is the parish's social-service office, not a worship site.

## Website and bulletin provider

https://www.stceciliachurch.com/ is the parish's eCatholic site (id 25501; the bare domain answers 403 to probe get, www. works). No menu on it links a bulletin; its unlinked /bulletins archive stopped in March 2022. The current bulletin is on ParishesOnline, so the provider is `parishes_online` with the org slug, and the eCatholic id stays out of `publication` (the playbook's rule for an eCatholic site that is only the website).

Fetch check (2026-11-03, headed): transport ok, PDF, picked container.parishesonline.com/bulletins/03/4014/20261101B.pdf, the 1 November 2026 issue read above (date observed 2026-11-01); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it.

## Not yet confirmed

Nothing open for the current row. Whether St. Cecilia and Fairview shared a bulletin in January-May 2023 is unknowable from these archives (see Publisher).
