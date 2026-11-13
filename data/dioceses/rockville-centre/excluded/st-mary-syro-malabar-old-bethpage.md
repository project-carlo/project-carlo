---
name: St. Mary's Syro-Malabar Catholic Church
reason: other-jurisdiction
line1: 926 Round Swamp Rd
city: Old Bethpage
state: NY
postal_code: '11804'
decided: 2026-11-13
roster: ['gcatholic:16999']
evidence:
- url: https://gcatholic.org/churches/usa-02/16999
  seen: 2026-11-13
  quote: 24 Westminster Rd., West Hempstead, New York 11552
  note: 'GCatholic church 16999 (last updated 2026-11-09): Church of St. Mary (Syro-Malabar); Jurisdiction:
    Syro-Malabar Diocese of Saint Thomas the Apostle of Chicago; within the territory of the Roman Diocese
    of Rockville Centre; History: 1994, Using the building: Church of St. Thomas the Apostle, West Hempstead;
    website stmaryssyromalabar.org.'
- url: https://web.archive.org/web/20250404231238/https://www.stmaryssyromalabar.org/Contact
  seen: 2026-11-13
  quote: 926 Round Swamp Rd
  note: The community's own Contact page (Wayback snapshot of 4 April 2025, read with visit.py) gives
    the church address as 926 Round Swamp Rd, Old Bethpage, NY 11804. The live site did not answer probe
    url or the browser on 2026-11-13.
- url: https://www.facebook.com/SMSMCC/
  seen: 2026-11-13
  note: 'Found through a DuckDuckGo search (page not opened): the search snippet for the community''s
    Facebook page reads "St. Mary''s Syro-Malabar Church 926 Round Swamp Road, Old Bethpage, NY".'
- url: https://www.stawh.church/bulletin/231-11-15-2026/file
  seen: 2026-11-13
  note: 'Per the lead from an earlier map job: the 15 November 2026 St. Thomas the Apostle, West Hempstead
    bulletin has Latin Masses at 24 Westminster Rd and does not mention the Syro-Malabar community.'
research:
- method: probe url and visit.py on the community's site
  url: https://www.stmaryssyromalabar.org/
  checked: '2026-11-13'
  outcome: access-blocked
  next_action: Read the live site's Contact and Mass Schedule pages to confirm the community still worships
    at 926 Round Swamp Rd
  retry_when: The site answers (it timed out over http and https)
---

## Why it is excluded

GCatholic (church 16999, read 2026-11-13) lists St. Mary, Syro-Malabar, with "Jurisdiction: Syro-Malabar Diocese of Saint Thomas the Apostle of Chicago", "within the territory of the Roman Diocese of Rockville Centre", and history "1994 Using the building: Church of St. Thomas the Apostle, West Hempstead" at 24 Westminster Rd. It belongs to an Eastern Catholic eparchy, so under the diocese's rule for Eastern communities in shared buildings (diocese.md, *Rules settled*) its roster entry goes here as other-jurisdiction. The Latin St. Thomas the Apostle parish still has public Mass at 24 Westminster Rd (15 November 2026 bulletin), so that building keeps its church row `st-thomas-the-apostle-west-hempstead-church` under the Latin parish.

## Name and address

The sources disagree on where the community worships. GCatholic gives the shared St. Thomas the Apostle building, 24 Westminster Rd, West Hempstead. The community's own site (Contact page, Wayback snapshot of 4 April 2025) gives "926 Round Swamp Rd, Old Bethpage, NY 11804", and the search snippet for its Facebook page gives the same address. The St. Thomas bulletin of 15 November 2026 does not mention the Syro-Malabar community. This record follows the community's own site, the newer source, and records Old Bethpage; GCatholic's West Hempstead entry probably dates from before the move. Who owns the Old Bethpage building was not checked; `pnpm diocese search` finds nothing at Round Swamp Rd or in Old Bethpage in these records. An earlier job saw Syro-Malabar Masses in the New Hyde Park bulletin at Holy Spirit; that is probably another Syro-Malabar community, and it was not checked here.

## What would change this

Nothing about the eparchy's services. If the Old Bethpage address turns out to be a Latin church with its own public Mass, that building would get a church row under its Latin parish, and this record would stay for the eparchy's entry.

## Not yet confirmed

The live site (stmaryssyromalabar.org) timed out on 2026-11-13, so the 2025 snapshot is the newest copy of its address read here; see `research`.
