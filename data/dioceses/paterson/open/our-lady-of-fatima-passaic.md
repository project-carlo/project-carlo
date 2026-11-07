---
name: Our Lady of Fatima
revisit: Ask the parish office (973-472-0815) or find a bulletin notice whether any Mass is still celebrated
  in the former Our Lady of Fatima church at 32 Exchange Place, or whether it closed or was sold; then
  make it a church of our-lady-of-fatima-st-nicholas-passaic or exclude it as closed with the source.
revisit_after: 2027-02-01
roster: ['gcatholic:18995']
evidence:
- url: https://gcatholic.org/churches/usa-03/18995
  seen: 2026-11-05
  note: GCatholic 18995 Our Lady of Fatima, 32 Exchange Pl., Passaic (Plus Code 87G7VV5G+84), 1954; parish
    1972.
- url: https://files.ecatholic.com/14272/bulletins/20220612.pdf
  seen: 2026-11-05
  quote: Our Lady of Fatima R.C.
  note: '12 June 2022 issue, page 1 sidebar: Office: Our Lady of Fatima R.C. Church, 32 Exchange Place;
    the Masses are listed beside St. Nicholas R.C. Church, 153 Washington Pl.'
- url: https://www.church-bulletin.org/bulletin/our-lady-of-fatima-saint-nicholas-roman-catholic-church-passaic-nj-07055/2026-11-01.pdf
  seen: 2026-11-05
  quote: 153 Washington Place, Passaic, NJ 07055
  note: 1 November 2026 masthead gives only the St. Nicholas address; one Mass schedule, no other place
    named. The 18 October 2026 issue (all 6 pages) has no mention of Exchange Place.
- url: https://1j1pea.sites.ecatholic.com/
  seen: 2026-11-05
  quote: 'Office/Mailing Address: 32 Exchange Pl. Passaic, NJ 07055'
  note: Legacy St. Nicholas site, read with visit.py.
- url: https://fatimanicholas.org/historia-de-nuestra-parroquia
  seen: 2026-11-05
  note: 'Parish history: the former Dutch Reformed church at Exchange and Park was bought and dedicated
    as Our Lady of Fatima on 23 October 1960; the history says nothing of its use after the 2022 merger.'
parish: our-lady-of-fatima-st-nicholas-passaic
line1: 32 Exchange Place
city: Passaic
state: NJ
postal_code: '07055'
research:
- method: thebeacon.net site search via probe get for Fatima Nicholas Passaic
  url: https://thebeacon.net/?s=Fatima+Nicholas+Passaic
  checked: '2026-11-05'
  outcome: access-blocked
  next_action: Search The Beacon (diocesan paper) for the 2022 Fatima-St. Nicholas merger article and
    what it says of the Exchange Place church
  retry_when: The Beacon search loads, or a browser search is available
- method: The Beacon WordPress API search via probe get (search=Fatima Nicholas; search=Fatima limited
    to June 2021 - June 2023; search=Exchange Place); read the three 2026 articles on the parish
  url: https://beaconnj.org/wp-json/wp/v2/posts?search=Fatima%20Nicholas&_fields=date,link,title
  checked: '2026-11-05'
  outcome: not-found
  next_action: Ask the parish office (973-472-0815) whether any Mass is celebrated at 32 Exchange Place,
    or read a future bulletin for a notice about the building
  retry_when: A bulletin or diocesan notice names the Exchange Place church, or a phone check is possible
---

## What is known

Our Lady of Fatima church, 32 Exchange Place (corner of Park), was dedicated on 23 October 1960 (parish history page, read 2026-11-05) and was the church of Our Lady of Fatima parish (GCatholic 18995). Since the 2022 merger with St. Nicholas, the bulletin gives the Masses with St. Nicholas church: the 12 June 2022 issue lists "St. Nicholas R.C. Church 153 Washington Pl." beside the schedule and "Office: Our Lady of Fatima R.C. Church 32 Exchange Place"; the 1 November 2026 masthead gives 153 Washington Place only, with one schedule and no other place, and the 18 October 2026 issue never mentions Exchange Place. The legacy St. Nicholas site calls 32 Exchange Pl. the "Office/Mailing Address". The finder's pin for the merged parish (directory:14272) sits at 32 Exchange Place but carries the St. Nicholas schedule; it is linked to `st-nicholas-passaic`.

## Why it is not decided

Nothing read shows Mass in the building now, but nothing says it closed, was sold or was relegated either: the bulletin and site use it only as the office address. Checked: the 1 November and 18 October 2026 bulletins, the 12 June 2022 bulletin, the parish site's home, Mass times and history pages, the legacy St. Nicholas site. The Beacon (beaconnj.org, searched through its WordPress API on 2026-11-05 by reconcile) has no merger article from 2021-2023 and nothing on Exchange Place; its 2026 articles on the parish (Easter Vigil, 30 May confirmations, the bishop's 16 August visit) name the parish but never the church building. Not checked: the parish office.
