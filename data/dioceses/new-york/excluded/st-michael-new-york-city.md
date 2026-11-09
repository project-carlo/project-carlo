---
name: St. Michael
reason: other
line1: 424 W 34th St.
city: New York City
state: NY
postal_code: '10001'
decided: 2026-10-08
roster: ['gcatholic:16280', 'directory:4930']
evidence:
- url: https://gcatholic.org/churches/usa-02/16280
  seen: 2026-10-07
  quote: 'GCatholic Church ID: 16280'
  note: Roster identity only, not present public Mass evidence.
- url: https://stmichaelnyc.org/
  seen: 2026-10-08
  quote: temporarily closed for partial renovation and the installation of a new boiler.
  note: Church-operated notice read October 8, 2026; explicit suspension, not merger inference.
- url: https://stmichaelnyc.org/
  seen: 2026-10-08
  quote: there is no plan to close St. Michael
  note: Notice expressly denies permanent closure; no reopening date supplied.
- url: https://stmichaelnyc.org/
  seen: 2026-11-09
  quote: St. Michael's Church is temporarily closed for partial renovation and the installation of a new
    boiler.
  note: Homepage read in headed Chrome (visit.py) on 2026-11-09 under the heading CHURCH TEMPORARILY CLOSED;
    same notice as October 8, still with no reopening date and still denying permanent closure.
revisit: Re-read the stmichaelnyc.org homepage notice and /mass-times (headed Chrome) for a dated reopening;
  on 2026-11-09 the CHURCH TEMPORARILY CLOSED notice was unchanged since October 8.
revisit_after: 2027-01-11
research:
- method: 'Homepage in headed Chrome (visit.py --text) and a web search for a 2026 reopening of St. Michael,
    West 34th Street: the closure notice is unchanged and no reopening news was found'
  url: https://stmichaelnyc.org/
  checked: '2026-11-09'
  outcome: found
  next_action: Keep the temporary exclusion (reason other); re-read the homepage and /mass-times
  retry_when: The homepage drops the CHURCH TEMPORARILY CLOSED notice, /mass-times lists Masses, or archny.org
    news reports the reopening
---

## Temporary suspension, not permanent closure

The church-operated homepage read October 8 expressly suspends public use for partial renovation and a new boiler, and denies permanent closure. Exclude temporarily with reason `other`, not `closed` or `no-bulletin`. Its notice gives 212-563-2575 for reopening notifications but no last-Mass or completion date.

## Publication checked

The /bulletins widget has no issues; /sunday-bulletin-archive holds liturgical issues labeled 2022. These do not override the current suspension.

## Reopening condition

A dated announcement of resumed public Mass at this West 34th Street building is required to restore an active venue. On 2026-11-09 the homepage (read in headed Chrome) still carried the unchanged CHURCH TEMPORARILY CLOSED notice, and a web search found no reopening news, so the next reading is set two months out. This is not the Russian Catholic St. Michael at 266 Mulberry Street.
