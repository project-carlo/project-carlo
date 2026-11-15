---
name: St. Gertrude Church
revisit: Ask the St. Damien parish office (860-688-4905) or search the Windsor land records / Hartford
  Courant for whether St. Gertrude church at 550 Matianuck Ave still has any Mass, or was closed, relegated
  or sold after the October 2020 merger.
revisit_after: 2027-02-01
roster: ['gcatholic:22238']
evidence:
- url: https://gcatholic.org/churches/usa-01/22238
  seen: 2026-11-13
  quote: 550 Matianuck Ave., Windsor, Connecticut 06095-3599
  note: GCatholic still lists 'St. Gertrude' as a church of the archdiocese.
- url: https://windsorcatholic.org/about-us/
  seen: 2026-11-13
  quote: In October of 2020, St. Gertrude Parish was subsumed into St. Damien parish
  note: Says the parish merged; says nothing about the church building.
- url: https://container.parishesonline.com/bulletins/03/0353/20261115B.pdf
  seen: 2026-11-13
  note: The 15 November 2026 St. Damien bulletin's masthead (page 2) gives Masses at St. Gabriel and St.
    Joseph only; the word Gertrude appears only as the saint of 16 November on page 3.
parish: st-damien-of-molokai-windsor
line1: 550 Matianuck Avenue
city: Windsor
state: CT
postal_code: 06095
research:
- method: archdiocese WordPress API search (posts?search=Gertrude, relegation, profane) and DuckDuckGo
    searches for St. Gertrude Windsor closed/sold/final Mass
  url: https://archdioceseofhartford.org/wp-json/wp/v2/posts?search=Gertrude
  checked: '2026-11-13'
  outcome: not-found
  next_action: Ask the parish office or search Windsor news and land records for the building's status
  retry_when: A relegation decree or news item about St. Gertrude, Windsor appears, or the St. Damien
    bulletin mentions the building
- method: 'DuckDuckGo search (''St. Gertrude church Windsor Connecticut 550 Matianuck'', and a sold/closing
    variant): only Mass-time aggregators, one labelling it ''CLOSED - go to: www.windsorcatholic.org''
    (not a source)'
  url: https://html.duckduckgo.com/html/
  checked: '2026-11-14'
  outcome: not-found
  next_action: Ask the St. Damien office or search Windsor land records and Hartford Courant archives
    for the building's status
  retry_when: A newspaper archive search, land records or the parish office is available
- method: 'Archdiocese news and public notices, WordPress posts API search (archdioceseofhartford.org/wp-json/wp/v2/posts?search=...)
    for the church name: no decree or report of it'
  checked: '2026-11-14'
  outcome: not-found
  url: https://archdioceseofhartford.org/wp-json/wp/v2/posts?search=Gertrude
  next_action: Ask the St. Damien office or search Windsor land records for the building's status
  retry_when: The parish office or land records are available
---

## What is known

St. Gertrude, 550 Matianuck Ave, Windsor is in GCatholic (22238) but not in the archdiocese's parish finder. St. Damien of Molokai's about page (read 2026-11-13) says "In October of 2020, St. Gertrude Parish was subsumed into St. Damien parish". The 15 November 2026 St. Damien bulletin (container 03/0353, page 2) and its site's Mass Times page give Masses only at St. Gabriel and St. Joseph.

## Why it is not decided

All of that is absence: no source read says the church closed, was relegated by decree or was sold. The archdiocese's public notices (searched for Gertrude, relegation, profane) carry no decree for it, and web searches turned up only aggregator listings with old schedules. Until something states its status it stays open; see `revisit`.
