---
name: FEST Pittsburgh (FestPGH)
reason: other
line1: ''
city: Pittsburgh
state: PA
postal_code: ''
decided: 2026-10-23
roster: ['massfinder:38958']
evidence:
- url: https://diopitt.org/massfinder
  seen: 2026-10-23
  note: Mass Finder pin id 38958, 'FEST Pittsburgh', city Pittsburgh, no street address, coordinates 0,0,
    website https://festpgh.org/ (rosters/massfinder.json). The pin names an event site, not a church.
- url: https://festpgh.org/
  seen: 2026-10-23
  quote: FestPGH music and arts festival on Saturday, September 19, 2026, in F.N.B. Stadium
  note: Home page (403 to curl; read in headed Chrome). Continues '(formerly Highmark Stadium, Pittsburgh's
    South Shore) ... Bishop Eckman will celebrate Mass. The event is free but requires an RSVP and digital
    ticket.' The Mass was a one-day part of the festival, 34 days before this check.
---

## Why it is excluded

FEST Pittsburgh (FestPGH) is a diocesan one-day Catholic music and arts festival, not a worship site. Its site (read 2026-10-23) describes a festival on Saturday 19 September 2026 in F.N.B. Stadium, with Switchfoot headlining, at which 'Bishop Eckman will celebrate Mass'. The diocese's Mass Finder carries it as a pin with no address and 0,0 coordinates (id 38958), apparently because the event was entered as a place. A one-off event Mass in a stadium is not a place with recurring public Mass, and the stadium is not a church; the site gives no regular Mass. Reason is `other` because none of the standard reasons (closed, office, another jurisdiction) fits an event.

## What would change this

Nothing expected: the pin is an event listing. If FestPGH became a recurring event with Mass the dataset wanted to track, it would still be an event, not a church row.
